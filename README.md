# Deed

**The licensed data supply layer for vertical AI.**

> Buyers post a data request or browse the open catalog. Creators upload any supported data type, keep ownership, and get paid when the data is licensed. No token. No user-to-user trading. No coercion.

## The problem

Vertical AI labs need domain-specific, rights-cleared, verifiable data. Today they buy it through:
- Crowd-labeling vendors (Scale, Surge, Mercor) — expensive, slow, general-purpose.
- Scraping — legally risky, no consent, no provenance.
- In-house collection — does not scale.

Creators and experts have the data — Korean voice, K-beauty images, clinical notes, legal annotations — but no clean way to license it. Generic consumer data marketplaces fail because random uploads do not match demand, rights are unclear, and prices are too low.

## The solution

**Two supply modes, one license engine.**

**1. Request mode (B2B pull).**
- A buyer posts a **Data Request**: domain, spec, quantity, quality bar, rights, budget, deadline.
- Creators submit data against the request.
- AI + human QC checks quality, duplicates, PII, and rights.
- Deed assembles the accepted data into a dataset and licenses it to the buyer.

**2. Open catalog (self-serve push).**
- A creator uploads any supported data type: image, text, audio/voice, video, annotations, or document.
- The creator sets a price and the license scope.
- Deed runs QC and lists the data in the open catalog.
- Buyers browse, filter, and license what they need.

**3. License at upload, paid on use.**
- At upload, the creator grants Deed a **non-exclusive, sublicensable license** to license the data to buyers.
- The creator keeps ownership and can delist future use.
- **No payment until a buyer licenses the data.** Then the creator gets 50–70% of net license revenue; Deed keeps 30–40%.
- The buyer gets provenance, consent records, and a defined license — not a data dump.

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

1. **Open catalog**: upload a Korean skincare photo set (image), set a price, and license it.
2. **Request mode**: post a data request, submit data as a creator, accept a submission, and license the dataset.
3. See the creator payout and the double-entry ledger.

The demo has both modes: a self-serve listing and a buyer request.

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

1. **Demand + catalog.** B2B requests for certainty; open catalog for variety.
2. **Rights first.** License at upload, not assignment; consent, provenance, deletion; creator can delist future use.
3. **Pay on use.** Listing is free; creators are paid when a buyer licenses the data.
4. **Creators paid.** 50–70% of net license revenue, in KRW/fiat.
5. **No token.** No speculation, no user-to-user trading, no price appreciation.
6. **QC is the product.** Quality and rights are why buyers pay.

---

**KR 요약** — Deed는 버티컬 AI 기업이 필요로 하는 데이터를 B2B 요청 기반으로 공급하는 라이선싱 마켓이다. 구매자가 요청하면 크리에이터가 권리 있는 데이터를 올리고, 검수·라이선스 후 원화로 수익을 받는다. 토큰·코인·유저 간 거래는 없다.
