# Three-minute demo script

```bash
python app/server.py
```

Open <http://127.0.0.1:8000>.

---

## 0:00–0:30 — The problem

> "Vertical AI is bottlenecked by data, not models. Labs need domain-specific, rights-cleared, verified data. Today they scrape, buy from general vendors, or collect in-house. Creators have the data but no clean way to license it."

Show the **post a data request** form.

## 0:30–1:00 — Demand first

Keep the defaults:

- Buyer: `K-Beauty AI`
- Title: `Korean skincare reviews + photos`
- Domain: `beauty`
- Quantity: `1000`
- Unit price: `500`
- Rights: `AI training, 2 years, global, no resale`

Click **Post request**.

> "Every dataset starts with a buyer, a spec, a rate, and a deadline. No random uploads."

## 1:00–1:45 — Creator submits

Click the request. In **Creator: submit data**:

- Creator: `Mina K.`
- File: `mina_001.jpg`
- Note: `front-facing, natural light, consent attached`

Click **Submit data**.

> "The creator submits against the request. QC checks quality, duplicates, PII, and consent. The platform accepts or rejects."

Show QC score and **Accept**.

## 1:45–2:30 — License and payout

Click **License dataset**.

> "The buyer licenses the accepted dataset. The creator gets 60% of net license revenue; the platform gets 40%. No token, no user-to-user trading."

Show the result: `Licensed 1 units · GMV ₩500 · creator ₩300 · platform ₩200`.

## 2:30–3:00 — Ledger and close

Scroll to **Payout ledger**.

> "Every license writes double-entry postings: client cash, creator payable, platform revenue. The ledger balances to the won. This is the trust layer for buyers and creators."

Close:

> "Deed is the licensed data supply layer for vertical AI. Demand first, rights first, creators paid."

---

## What to say if asked "is this real?"

- The demo uses simulated QC and payouts, but the request → submission → acceptance → license → ledger flow is real.
- Production QC, consent records, KYC, and payouts are in [ARCHITECTURE.md](ARCHITECTURE.md) and [LEGAL.md](LEGAL.md).
- The first 90 days: 3 buyers, 100 creators, 1,000 accepted units, first revenue.

## What not to say

- "Anyone can upload anything." No — only request-backed submissions.
- "We use a token." No.
- "We are a scraping company." No.
- "We can serve every domain today." No — one domain first.
