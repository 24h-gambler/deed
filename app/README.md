# Deed — runnable demo

Zero dependencies. Python 3.11+.

## Run

```bash
python app/server.py
```

Open <http://127.0.0.1:8000>.

## Demo flow

1. **Post a request** (buyer): "Korean skincare reviews + photos", 1,000 units, ₩500/unit.
2. **Submit data** (creator): `mina_001.jpg`, note "front-facing, natural light, consent attached".
3. **Accept** the submission. QC score is shown; the platform decides.
4. **License dataset**. The server computes:
   - gross = accepted units × unit price
   - creator 60%, platform 40%
   - double-entry ledger postings
5. Check the **payout ledger**: total debits = total credits.

## API

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | health check |
| POST | `/api/requests` | create a data request |
| GET | `/api/requests` | list requests |
| GET | `/api/requests/{id}` | request + submissions |
| POST | `/api/requests/{id}/submissions` | creator submits data |
| POST | `/api/submissions/{id}/accept` | accept submission |
| POST | `/api/submissions/{id}/reject` | reject submission |
| POST | `/api/requests/{id}/license` | license dataset + payouts |
| GET | `/api/ledger` | ledger summary |
| GET | `/api/stats` | GMV, creator paid, platform revenue |

### Create request

```json
{
  "buyer": "K-Beauty AI",
  "title": "Korean skincare reviews + photos",
  "domain": "beauty",
  "spec": "1,000 reviews with a face photo, natural light, 1080px+, consent attached",
  "quantity": 1000,
  "unit_price_krw": 500,
  "rights": "AI training, 2 years, global, no resale",
  "deadline": "2026-12-01"
}
```

### Submit

```json
{
  "creator": "Mina K.",
  "file_name": "mina_001.jpg",
  "note": "front-facing, natural light, consent attached"
}
```

## Smoke test

```bash
python scripts/smoke_test.py
```

Starts the server on port 8011 with a temporary database, creates a request, submits two datasets, accepts one, licenses it, and asserts the ledger balances.

## What this demonstrates

- Demand-pulled request → submission → QC → license → payout.
- Acceptance workflow with QC score.
- Revenue share: 60% creator / 40% platform.
- Double-entry ledger: client cash, creator payable, platform revenue.

## What it does not do

- No real files, consent records, or KYC.
- No real payouts or tax withholding.
- No production QC (PII, CSAM, duplicate detection).
- SQLite, not Postgres.

Production design: [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).
