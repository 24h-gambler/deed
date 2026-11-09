# Three-minute demo script

```bash
python app/server.py
```

Open <http://127.0.0.1:8000>.

---

## 0:00–0:25 — The problem

> "Vertical AI is bottlenecked by data, not models. Labs need domain-specific, rights-cleared, verified data. Today they scrape, buy from general vendors, or collect in-house. Creators have the data but no clean way to license it."

Show the **Open catalog** and **Data request** sections.

## 0:25–1:05 — Open catalog: upload and list

Use the defaults:

- Creator: `Mina K.`
- Title: `Korean skincare photo set`
- Data type: `Image`
- Domain: `beauty`
- Price: `500`
- File: `mina_set_01.jpg`
- Description: `front-facing, natural light, consent attached`

Click **List data**.

> "Creators can list any data type — image, text, audio, video, annotations, document. They set a price and the license scope. Deed runs QC and lists it. No buyer request needed."

Click **License** on the asset.

> "When a buyer licenses it, the creator gets 60%, Deed gets 40%. No payment at upload. The creator keeps ownership and can delist future use."

Show: `₩500` → creator `₩300`, platform `₩200`.

## 1:05–1:45 — Request mode: buyer demand

Use the defaults:

- Buyer: `K-Beauty AI`
- Title: `Korean skincare reviews + photos`
- Quantity: `1000`
- Unit price: `500`
- Rights: `AI training, 2 years, global, no resale`

Click **Post request**.

> "The second mode is demand-pulled. A buyer posts a spec, a rate, a rights scope, and a deadline. Creators submit against it."

Click the request, then submit:

- Creator: `Joon P.`
- File: `joon_001.jpg`
- Note: `consent attached, studio light`

Click **Submit data**.

## 1:45–2:20 — Accept, license, payout

Click **Accept** on the submission.

> "QC checks quality, duplicates, PII, and consent. The platform decides."

Click **License dataset**.

> "The buyer licenses the accepted dataset. Creator 60%, platform 40%."

Show: `Licensed 1 units · GMV ₩500 · creator ₩300 · platform ₩200`.

## 2:20–3:00 — Ledger and close

Scroll to **Payout ledger**.

> "Every license writes double-entry postings: client cash, creator payable, platform revenue. The ledger balances to the won. This is the trust layer for buyers and creators."

Close:

> "Deed is the licensed data marketplace for vertical AI. Buyers request or browse; creators list and get paid when licensed. No token, no user-to-user trading, no data dump."

---

## What to say if asked "is this real?"

- The demo uses simulated QC and payouts, but the request → submission → acceptance → license → ledger flow is real.
- Production QC, consent records, KYC, and payouts are in [ARCHITECTURE.md](ARCHITECTURE.md) and [LEGAL.md](LEGAL.md).
- The first 90 days: 3 buyers, 100 creators, 300 catalog listings, 1,000 accepted units, first revenue.

## What not to say

- "Anyone can upload anything." No — only supported types, with QC and a license.
- "We own the data." No — the creator keeps ownership; Deed gets a license.
- "We pay at upload." No — payment happens when the data is licensed.
- "We use a token." No.
- "We are a scraping company." No.
