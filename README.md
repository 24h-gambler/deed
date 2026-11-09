# Deed

**The licensed data supply layer for vertical AI.**

> Buyers post a data request. Creators submit rights-cleared data. Deed verifies quality and rights, licenses the dataset, and pays creators a revenue share. No token. No user-to-user trading. No coercion.

## The problem

Vertical AI labs need domain-specific, rights-cleared, verifiable data. Today they buy it through:
- Crowd-labeling vendors (Scale, Surge, Mercor) — expensive, slow, general-purpose.
- Scraping — legally risky, no consent, no provenance.
- In-house collection — does not scale.

Creators and experts have the data — Korean voice, K-beauty images, clinical notes, legal annotations — but no clean way to license it. Generic consumer data marketplaces fail because random uploads do not match demand, rights are unclear, and prices are too low.

## The solution

**Demand-pulled data licensing.**

1. A buyer posts a **Data Request**: domain, spec, quantity, quality bar, rights, budget, deadline.
2. Creators submit data against the request. AI + human QC checks quality, duplicates, PII, and rights.
3. Deed assembles the accepted data into a dataset and licenses it to the buyer.
4. Creators get paid a **revenue share** (50–70%) in KRW/fiat.
5. The buyer gets provenance, consent records, and a license — not a data dump.

## Why now

- **Vertical models need vertical data.** General models are commoditizing; the bottleneck is proprietary, domain-specific, verifiable data.
- **Regulation is tightening.** PIPA/GDPR make consent, provenance, and deletion non-negotiable.
- **Creators need monetization.** The creator economy is looking for revenue beyond ads and subscriptions.
- **Korea/Asia data is scarce.** Korean voice, K-beauty, and expert annotations are hard for global labs to source legally.

## YC fit

**AI data infrastructure for vertical foundation models.** Deed is the licensed data supply layer that vertical AI labs and enterprises use to own their intelligence — with rights, provenance, and fair creator payouts.

## Run the demo

Zero dependencies. Python 3.11+.

```bash
python app/server.py
```

Open <http://127.0.0.1:8000>.

1. Create a data request (e.g., "Korean skincare reviews + photos").
2. Submit data as a creator.
3. Accept a submission; license the dataset.
4. See the creator payout and platform ledger.

Smoke test:

```bash
python scripts/smoke_test.py
```

## Repository map

- [docs/BLUEPRINT.md](docs/BLUEPRINT.md) — one-page visual blueprint.
- [docs/PRODUCT.md](docs/PRODUCT.md) — buyer, creator, pricing, competition.
- [docs/LEGAL.md](docs/LEGAL.md) — rights, consent, license terms, prohibited data.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system, data model, API, QC, payout.
- [docs/PLAN.md](docs/PLAN.md) — 90-day and 12-month execution plan.
- [docs/YC.md](docs/YC.md) — YC narrative, market, ask.
- [docs/KR_SUMMARY.md](docs/KR_SUMMARY.md) — Korean summary.
- [app/](app/) — runnable demo server + UI.

## Status

Pre-seed. Blueprint v1.0. First domain: Korean voice / K-beauty / expert annotations. First buyers: vertical AI labs and brands. First creators: Korean creators and domain experts.

## Principles

1. **Demand first.** No random uploads; only requests with a buyer and a budget.
2. **Rights first.** License, not assignment; consent, provenance, deletion.
3. **Creators paid.** 50–70% of net license revenue, in KRW/fiat.
4. **No token.** No speculation, no user-to-user trading, no price appreciation.
5. **QC is the product.** Quality and rights are why buyers pay.

---

**KR 요약** — Deed는 버티컬 AI 기업이 필요로 하는 데이터를 B2B 요청 기반으로 공급하는 라이선싱 마켓이다. 구매자가 요청하면 크리에이터가 권리 있는 데이터를 올리고, 검수·라이선스 후 원화로 수익을 받는다. 토큰·코인·유저 간 거래는 없다.
