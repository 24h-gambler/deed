#!/usr/bin/env python3
"""
Deed — runnable demo server (zero dependencies).

Run:
    python app/server.py
Then open:
    http://127.0.0.1:8000

This is a demo, not production. SQLite, simulated QC, no auth, no real money.
"""

import argparse
import json
import mimetypes
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.environ.get("DEED_DB", os.path.join(DATA_DIR, "deed.db"))


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def r2(value):
    return round(float(value) + 1e-9, 2)


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id TEXT PRIMARY KEY,
                buyer TEXT NOT NULL,
                title TEXT NOT NULL,
                domain TEXT NOT NULL,
                spec TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price_krw REAL NOT NULL,
                rights TEXT NOT NULL,
                deadline TEXT,
                status TEXT NOT NULL DEFAULT 'OPEN',
                created_at TEXT NOT NULL,
                licensed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                creator TEXT NOT NULL,
                file_name TEXT NOT NULL,
                note TEXT,
                qc_score REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ledger_entries (
                id TEXT PRIMARY KEY,
                source_type TEXT NOT NULL,
                source_id TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS postings (
                id TEXT PRIMARY KEY,
                entry_id TEXT NOT NULL,
                account TEXT NOT NULL,
                debit REAL NOT NULL DEFAULT 0,
                credit REAL NOT NULL DEFAULT 0,
                currency TEXT NOT NULL DEFAULT 'KRW'
            );
            """
        )
        conn.commit()


def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def qc_score(file_name, note):
    score = 0.70
    score += min(len((note or "").strip()) / 200.0, 0.15)
    ext = os.path.splitext(file_name or "")[1].lower()
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".wav", ".mp3", ".txt", ".csv", ".json"}:
        score += 0.10
    if "consent" in (note or "").lower():
        score += 0.05
    return round(min(score, 0.99), 2)


def create_request(payload):
    buyer = (payload.get("buyer") or "").strip()
    title = (payload.get("title") or "").strip()
    domain = (payload.get("domain") or "").strip()
    spec = (payload.get("spec") or "").strip()
    quantity = int(payload.get("quantity") or 0)
    unit_price = float(payload.get("unit_price_krw") or 0)
    rights = (payload.get("rights") or "AI training, 2 years, global, no resale").strip()
    deadline = (payload.get("deadline") or "").strip()

    if not buyer or not title or not domain or not spec:
        raise ValueError("buyer, title, domain, and spec are required")
    if quantity <= 0 or unit_price <= 0:
        raise ValueError("quantity and unit_price_krw must be positive")

    request_id = "req_" + uuid.uuid4().hex[:12]
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO requests
            (id, buyer, title, domain, spec, quantity, unit_price_krw, rights, deadline, status, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
            (request_id, buyer, title, domain, spec, quantity, unit_price, rights, deadline, "OPEN", now_iso()),
        )
        conn.commit()
    return get_request(request_id)


def list_requests():
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT r.*,
                   (SELECT COUNT(*) FROM submissions s WHERE s.request_id = r.id) AS submission_count,
                   (SELECT COUNT(*) FROM submissions s WHERE s.request_id = r.id AND s.status = 'ACCEPTED') AS accepted_count
            FROM requests r
            ORDER BY r.created_at DESC
            LIMIT 50
            """
        ).fetchall()
        return [row_to_dict(r) for r in rows]


def get_request(request_id):
    with connect() as conn:
        request = conn.execute("SELECT * FROM requests WHERE id = ?", (request_id,)).fetchone()
        if not request:
            raise ValueError("request not found")
        submissions = conn.execute(
            "SELECT * FROM submissions WHERE request_id = ? ORDER BY created_at DESC", (request_id,)
        ).fetchall()
        data = row_to_dict(request)
        data["submissions"] = [row_to_dict(s) for s in submissions]
        return data


def create_submission(request_id, payload):
    creator = (payload.get("creator") or "").strip()
    file_name = (payload.get("file_name") or "").strip()
    note = (payload.get("note") or "").strip()
    if not creator or not file_name:
        raise ValueError("creator and file_name are required")

    with connect() as conn:
        request = conn.execute("SELECT * FROM requests WHERE id = ?", (request_id,)).fetchone()
        if not request:
            raise ValueError("request not found")
        if request["status"] != "OPEN":
            raise ValueError("request is not open")
        submission_id = "sub_" + uuid.uuid4().hex[:12]
        score = qc_score(file_name, note)
        conn.execute(
            """
            INSERT INTO submissions
            (id, request_id, creator, file_name, note, qc_score, status, created_at)
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (submission_id, request_id, creator, file_name, note, score, "PENDING", now_iso()),
        )
        conn.commit()
    return get_request(request_id)


def set_submission_status(submission_id, status):
    with connect() as conn:
        submission = conn.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,)).fetchone()
        if not submission:
            raise ValueError("submission not found")
        conn.execute("UPDATE submissions SET status = ? WHERE id = ?", (status, submission_id))
        conn.commit()
        return get_request(submission["request_id"])


def add_entry(conn, source_type, source_id, postings):
    entry_id = "jrn_" + uuid.uuid4().hex[:12]
    conn.execute(
        "INSERT INTO ledger_entries (id, source_type, source_id, created_at) VALUES (?,?,?,?)",
        (entry_id, source_type, source_id, now_iso()),
    )
    for account, debit, credit in postings:
        conn.execute(
            "INSERT INTO postings (id, entry_id, account, debit, credit, currency) VALUES (?,?,?,?,?,?)",
            ("pst_" + uuid.uuid4().hex[:12], entry_id, account, r2(debit), r2(credit), "KRW"),
        )
    return entry_id


def license_request(request_id):
    with connect() as conn:
        request = conn.execute("SELECT * FROM requests WHERE id = ?", (request_id,)).fetchone()
        if not request:
            raise ValueError("request not found")
        if request["status"] == "LICENSED":
            raise ValueError("request already licensed")
        accepted = conn.execute(
            "SELECT * FROM submissions WHERE request_id = ? AND status = 'ACCEPTED'", (request_id,)
        ).fetchall()
        if not accepted:
            raise ValueError("no accepted submissions to license")

        count = len(accepted)
        gross = r2(count * request["unit_price_krw"])
        creator_share = r2(gross * 0.60)
        platform_share = r2(gross - creator_share)

        add_entry(
            conn,
            "license",
            request_id,
            [
                ("client_cash", gross, 0),
                ("creator_payable", 0, creator_share),
                ("platform_revenue", 0, platform_share),
            ],
        )
        add_entry(
            conn,
            "payout",
            request_id,
            [
                ("creator_payable", creator_share, 0),
                ("creator_cash", 0, creator_share),
            ],
        )
        add_entry(
            conn,
            "sweep",
            request_id,
            [
                ("operating_cash", platform_share, 0),
                ("client_cash", 0, platform_share),
            ],
        )
        conn.execute(
            "UPDATE requests SET status = 'LICENSED', licensed_at = ? WHERE id = ?",
            (now_iso(), request_id),
        )
        conn.commit()

    return {
        "request_id": request_id,
        "licensed_units": count,
        "gross_krw": gross,
        "creator_share_krw": creator_share,
        "platform_share_krw": platform_share,
    }


def ledger_summary():
    with connect() as conn:
        accounts = conn.execute(
            "SELECT account, SUM(debit) AS debit, SUM(credit) AS credit FROM postings GROUP BY account ORDER BY account"
        ).fetchall()
        totals = conn.execute("SELECT SUM(debit) AS debit, SUM(credit) AS credit FROM postings").fetchone()
        entries = conn.execute("SELECT * FROM ledger_entries ORDER BY created_at").fetchall()
        result_entries = []
        for entry in entries:
            postings = conn.execute(
                "SELECT account, debit, credit, currency FROM postings WHERE entry_id = ?",
                (entry["id"],),
            ).fetchall()
            result_entries.append(
                {
                    "entry_id": entry["id"],
                    "source_type": entry["source_type"],
                    "source_id": entry["source_id"],
                    "created_at": entry["created_at"],
                    "postings": [row_to_dict(p) for p in postings],
                }
            )
        return {
            "accounts": [row_to_dict(a) for a in accounts],
            "total_debit": r2(totals["debit"] or 0),
            "total_credit": r2(totals["credit"] or 0),
            "balanced": abs((totals["debit"] or 0) - (totals["credit"] or 0)) < 0.01,
            "entries": result_entries,
        }


def stats():
    with connect() as conn:
        requests_count = conn.execute("SELECT COUNT(*) AS c FROM requests").fetchone()["c"]
        submissions_count = conn.execute("SELECT COUNT(*) AS c FROM submissions").fetchone()["c"]
        accepted_count = conn.execute("SELECT COUNT(*) AS c FROM submissions WHERE status = 'ACCEPTED'").fetchone()["c"]
        licensed = conn.execute("SELECT COUNT(*) AS c FROM requests WHERE status = 'LICENSED'").fetchone()["c"]
        gross = conn.execute("SELECT COALESCE(SUM(debit), 0) AS s FROM postings WHERE account = 'client_cash'").fetchone()["s"]
        creator_paid = conn.execute("SELECT COALESCE(SUM(debit), 0) AS s FROM postings WHERE account = 'creator_payable'").fetchone()["s"]
        platform = conn.execute("SELECT COALESCE(SUM(credit), 0) AS s FROM postings WHERE account = 'platform_revenue'").fetchone()["s"]
        return {
            "requests": requests_count,
            "submissions": submissions_count,
            "accepted": accepted_count,
            "licensed_requests": licensed,
            "gross_krw": r2(gross),
            "creator_paid_krw": r2(creator_paid),
            "platform_revenue_krw": r2(platform),
        }


class Handler(BaseHTTPRequestHandler):
    server_version = "DeedDemo/1.0"

    def log_message(self, fmt, *args):
        print("[deed] " + fmt % args)

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _serve_file(self, path):
        if path == "/":
            path = "/static/index.html"
        if not path.startswith("/static/"):
            self.send_error(404, "Not found")
            return
        rel = path[len("/static/"):]
        full = os.path.abspath(os.path.join(STATIC_DIR, rel))
        if not full.startswith(STATIC_DIR + os.sep):
            self.send_error(403, "Forbidden")
            return
        if not os.path.isfile(full):
            self.send_error(404, "Not found")
            return
        mime, _ = mimetypes.guess_type(full)
        with open(full, "rb") as fh:
            body = fh.read()
        self.send_response(200)
        self.send_header("Content-Type", mime or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        try:
            if path == "/api/health":
                self._send_json(200, {"ok": True, "service": "deed-demo", "time": now_iso()})
            elif path == "/api/requests":
                self._send_json(200, {"requests": list_requests()})
            elif path.startswith("/api/requests/"):
                request_id = path.split("/")[3]
                self._send_json(200, get_request(request_id))
            elif path == "/api/ledger":
                self._send_json(200, ledger_summary())
            elif path == "/api/stats":
                self._send_json(200, stats())
            else:
                self._serve_file(path)
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception as exc:
            self._send_json(500, {"error": type(exc).__name__ + ": " + str(exc)})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/requests":
                self._send_json(201, create_request(payload))
            elif path.startswith("/api/requests/") and path.endswith("/submissions"):
                request_id = path.split("/")[3]
                self._send_json(201, create_submission(request_id, payload))
            elif path.startswith("/api/submissions/") and path.endswith("/accept"):
                submission_id = path.split("/")[3]
                self._send_json(200, set_submission_status(submission_id, "ACCEPTED"))
            elif path.startswith("/api/submissions/") and path.endswith("/reject"):
                submission_id = path.split("/")[3]
                self._send_json(200, set_submission_status(submission_id, "REJECTED"))
            elif path.startswith("/api/requests/") and path.endswith("/license"):
                request_id = path.split("/")[3]
                self._send_json(200, license_request(request_id))
            else:
                self.send_error(404, "Not found")
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception as exc:
            self._send_json(500, {"error": type(exc).__name__ + ": " + str(exc)})


def main():
    parser = argparse.ArgumentParser(description="Deed demo server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    args = parser.parse_args()
    init_db()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print("Deed demo running at http://%s:%d" % (args.host, args.port))
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
