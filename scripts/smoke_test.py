#!/usr/bin/env python3
"""Smoke test for the Deed demo.

Starts the server with a temporary SQLite database, runs
request -> submission -> accept -> license -> ledger, and asserts the ledger balances.
"""

import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8011
BASE = "http://127.0.0.1:%d" % PORT


def request(method, path, payload=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    db_path = os.path.join(tempfile.gettempdir(), "deed_smoke_%d.db" % os.getpid())
    if os.path.exists(db_path):
        os.remove(db_path)

    env = os.environ.copy()
    env["DEED_DB"] = db_path
    server = os.path.join(ROOT, "app", "server.py")
    proc = subprocess.Popen(
        [sys.executable, server, "--port", str(PORT)],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        for _ in range(40):
            try:
                if request("GET", "/api/health").get("ok"):
                    break
            except Exception:
                time.sleep(0.25)
        else:
            raise RuntimeError("server did not start on port %d" % PORT)

        created = request(
            "POST",
            "/api/requests",
            {
                "buyer": "K-Beauty AI",
                "title": "Korean skincare reviews + photos",
                "domain": "beauty",
                "spec": "1,000 reviews with a face photo, natural light, 1080px+, consent attached",
                "quantity": 1000,
                "unit_price_krw": 500,
                "rights": "AI training, 2 years, global, no resale",
                "deadline": "2026-12-01",
            },
        )
        request_id = created["id"]
        assert created["status"] == "OPEN", created

        first = request(
            "POST",
            "/api/requests/%s/submissions" % request_id,
            {
                "creator": "Mina K.",
                "file_name": "mina_001.jpg",
                "note": "front-facing, natural light, consent attached",
            },
        )
        second = request(
            "POST",
            "/api/requests/%s/submissions" % request_id,
            {
                "creator": "Joon P.",
                "file_name": "joon_001.jpg",
                "note": "consent attached, studio light",
            },
        )
        assert len(second["submissions"]) == 2, second

        submission_id = first["submissions"][0]["id"]
        accepted = request("POST", "/api/submissions/%s/accept" % submission_id, {})
        accepted_count = len([s for s in accepted["submissions"] if s["status"] == "ACCEPTED"])
        assert accepted_count == 1, accepted

        licensed = request("POST", "/api/requests/%s/license" % request_id, {})
        assert licensed["licensed_units"] == 1, licensed
        assert licensed["gross_krw"] == 500, licensed
        assert licensed["creator_share_krw"] == 300, licensed
        assert licensed["platform_share_krw"] == 200, licensed

        asset = request(
            "POST",
            "/api/assets",
            {
                "creator": "Mina K.",
                "title": "Korean skincare photo set",
                "data_type": "image",
                "domain": "beauty",
                "description": "front-facing, natural light, consent attached",
                "file_name": "mina_set_01.jpg",
                "price_krw": 500,
            },
        )
        assert asset["status"] == "LISTED", asset

        catalog = request("GET", "/api/assets")
        assert len(catalog["assets"]) == 1, catalog

        asset_license = request(
            "POST",
            "/api/assets/%s/license" % asset["id"],
            {"buyer": "Catalog Buyer"},
        )
        assert asset_license["gross_krw"] == 500, asset_license
        assert asset_license["creator_share_krw"] == 300, asset_license
        assert asset_license["platform_share_krw"] == 200, asset_license

        ledger = request("GET", "/api/ledger")
        assert ledger["balanced"], ledger
        assert abs(ledger["total_debit"] - ledger["total_credit"]) < 0.01, ledger

        stats = request("GET", "/api/stats")
        assert stats["requests"] == 1, stats
        assert stats["submissions"] == 2, stats
        assert stats["accepted"] == 1, stats
        assert stats["licensed_requests"] == 1, stats
        assert stats["assets"] == 1, stats
        assert stats["licensed_assets"] == 1, stats
        assert stats["gross_krw"] == 1000, stats
        assert stats["creator_paid_krw"] == 600, stats
        assert stats["platform_revenue_krw"] == 400, stats

        print("PASS")
        print("request=%s submissions=2 accepted=1" % request_id)
        print(
            "request license gross=%s creator=%s platform=%s"
            % (licensed["gross_krw"], licensed["creator_share_krw"], licensed["platform_share_krw"])
        )
        print(
            "asset=%s gross=%s catalog=1" % (asset["id"], asset_license["gross_krw"])
        )
        print(
            "ledger debit=%s credit=%s balanced=%s"
            % (ledger["total_debit"], ledger["total_credit"], ledger["balanced"])
        )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        if os.path.exists(db_path):
            os.remove(db_path)


if __name__ == "__main__":
    main()
