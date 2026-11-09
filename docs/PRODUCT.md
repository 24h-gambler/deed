# Product

**One-liner** Deed is the licensed data supply layer for vertical AI. Buyers post a data request, creators submit rights-cleared data, and get paid when it is licensed.

---

## 1. Customer

### 1.1 Buyer ICP

| Dimension | Definition |
|---|---|
| Who | Vertical AI labs, AI product teams, brands building domain models |
| Need | Domain-specific, rights-cleared, verifiable data |
| Current spend | Crowd-labeling vendors, scraping, in-house annotation |
| Trigger | Model quality plateaus; legal review blocks scraped data; a new vertical product needs data fast |
| Budget | $10k–500k per dataset |
| Anti-ICP | General-purpose labs that only need web-scale data; buyers who want to own the data outright without licensing |

### 1.2 Creator ICP

| Dimension | Definition |
|---|---|
| Who | Korean creators, domain experts, small studios, clinics, agencies |
| Asset | Photos, voice, reviews, annotations, documents they own or have consent to license |
| Motivation | Monetize data without giving up ownership |
| Trigger | A specific request with a clear rate card; fast payout |
| Anti-ICP | People who want to upload anything and hope it sells; people who do not hold rights |

---

## 2. Problem

**Buyers:** vertical AI teams need data that is:
- domain-specific (Korean beauty, clinical, legal),
- high quality (not a random dump),
- legally clean (consent, rights, provenance),
- fast (weeks, not quarters).

Today they choose between expensive vendors, risky scraping, and slow in-house collection.

**Creators:** they have the data but no clean path to license it. Generic marketplaces pay pennies, obscure usage, and take ownership. The result: supply stays offline.

---

## 3. Solution

**Demand-pulled data licensing.**

1. Buyer posts a request: domain, spec, quantity, quality bar, rights, budget, deadline.
2. Creator submits data. Deed runs AI QC (quality, duplicate, PII) and human review.
3. Deed assembles accepted submissions into a dataset, licenses it to the buyer.
4. Creator gets 50–70% of net license revenue in KRW/fiat.
5. Buyer gets provenance, consent records, and a defined license.

**No token. No user-to-user trading. No upload-first lottery.**

### 3.1 Two supply modes

| Mode | Who starts | Flow | Payment |
|---|---|---|---|
| **Request mode** | Buyer | request → submit → QC → accept → license | on license |
| **Open catalog** | Creator | upload any type → QC → list → buyer licenses | on license |

**Open catalog is not a lottery.** The creator sets a price and license scope; buyers filter by type, domain, QC, and price. Payment happens only when a buyer licenses the data. The creator can delist future use at any time.

### 3.2 Data types

| Type | Examples | QC focus |
|---|---|---|
| **Image** | K-beauty photos, product shots, medical images | resolution, framing, duplicates, faces/PII |
| **Text** | reviews, dialogues, legal/clinical notes | language, toxicity, PII, duplicates |
| **Audio / Voice** | read speech, conversational speech, accents | noise, duration, speaker consent |
| **Video** | demonstrations, procedures, gestures | resolution, consent, faces |
| **Annotations** | labels, bounding boxes, preferences | consistency, inter-annotator agreement |
| **Document** | contracts, forms, receipts | OCR quality, PII, rights |

---

## 4. Pricing

| Item | Price | Notes |
|---|---|---|
| Data license | per-unit or per-dataset | request price or creator-set catalog price |
| Creator share | 50–70% of net license revenue | paid in KRW/fiat **only when licensed** |
| Platform take | 30–40% | QC, rights, sales, payouts |
| Enterprise | annual contract | custom datasets, API |

**Listing is free.** There is no guaranteed income. A creator is paid when a buyer licenses the data; if it does not sell, the creator can delist.

**Example:** 1,000 photos at ₩500 → ₩500,000. Creator 60% = ₩300,000; platform 40% = ₩200,000; QC/payment cost ₩45,000; contribution ₩155,000.

---

## 5. Competition

| Player | What they do | Gap |
|---|---|---|
| Scale / Surge / Mercor | crowd labeling, general data | expensive, general-purpose, not vertical |
| Toloka / Appen | global crowd data | quality variance, no vertical depth |
| Ocean / Bittensor / Grass | crypto data/compute | speculation, not B2B licensed data |
| Scraping vendors | fast, cheap | legal risk, no consent/provenance |
| In-house | control | slow, does not scale |
| Deed | demand-pulled, rights-cleared, vertical | the wedge |

**Moat:** creator network + rights/provenance + QC + buyer contracts. The data itself is not scarce; the **clean, licensed, verified supply** is.

---

## 6. Metrics

| Metric | Target |
|---|---:|
| Buyers with a paid request | 3 in 90 days |
| Creators submitting | 100 in 90 days |
| Acceptance rate | 60%+ |
| Time to deliver | <2 weeks |
| Creator repeat | 30% monthly |
| Buyer repeat | 30% in 90 days |
| Take rate | 30–40% |
| Gross margin | 25–35% |
| Catalog listings | 300 in 90 days |
| Listing-to-license conversion | 10%+ |
| Data GMV | $100k in 6 months |

---

## 7. Risks

| Risk | Mitigation |
|---|---|
| Low data prices | focus on vertical/expert data; bundle QC/rights |
| Multi-homing | creator reputation, fast payouts, request pipeline |
| Buyer concentration | 3+ buyers per domain; enterprise contracts |
| Rights/consent | license terms, consent records, deletion, audit |
| QC cost | AI first, human only on edge cases |
| Privacy (PII) | PII detection, anonymization, sensitive-data policy |
| Competition from vendors | speed, vertical depth, creator payouts |

---

## 8. What we do not build

- A token or a consumer crypto app.
- A user-to-user data trading exchange.
- A scraping company.
- A general-purpose data dump.
- A marketplace without buyer requests.

---

**KR 요약** — 구매자는 버티컬 AI 기업, 크리에이터는 한국 크리에이터·전문가다. Deed는 요청 기반으로 데이터를 모으고, 검수·권리 정리 후 라이선스하며, 크리에이터에게 매출의 50~70%를 원화로 지급한다.
