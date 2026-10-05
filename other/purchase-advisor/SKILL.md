---
name: purchase-advisor
description: "Purchase and price-value advice incl. health products. Alayım mı, fiyatı iyi mi, almaya değer mi, muadili var mı, işe yarar mı, SGK karşılıyor mu."
---

# Purchase Advisor

Answers "alayım mı?", "fiyatı iyi mi?", "almaya değer mi?", "muadili var mı?" and "işe yarar mı?" with current evidence.

## Choose the module

- General products, services, subscriptions, websites, competitor pricing, value for money → `market-pricing-analysis`.
- Health-related products (supplement, cream/gel, brace, tape, massager, electrotherapy/TENS/EMS, wearable, exercise or rehabilitation aid, medicine-like item) → `health-product-evidence-check`, plus `market-pricing-analysis` for the price part.

Device setup or compatibility → `personal-tech-copilot`. Securities → `yigit-investment-copilot`.

## Shared rules

- Pin the exact product: brand, model code, variant, size or dose, seller, country.
- Prices must be current and dated; normalize to total cost (shipping, subscription, unit price, installments).
- Separate independent evidence from seller or influencer claims; label ads and affiliate links.
- Give a clear verdict — AL / BEKLE / ALMA / ALTERNATİF — with the two or three decisive reasons, the best alternative, and when not to buy.
- Scores (e.g. "10 üzerinden") only when the evidence supports them; explain the scale.

## Module map

Open only the module(s) the request needs and read the module file completely before acting. Several modules may combine in one task.

| Module | Use when | File |
|---|---|---|
| `market-pricing-analysis` | Automatically analyze product, service, subscription, marketplace, or competitor pricing when the user asks "fiyatı iyi mi", "almaya değer mi", "en ucuz/kaliteli hangisi… | [MODULE.md](modules/market-pricing-analysis/MODULE.md) |
| `health-product-evidence-check` | Automatically evaluate a health-related product, medicine-like item, supplement, cream/gel, brace, tape, massager, electrotherapy device, wearable, exercise/rehabilitati… | [MODULE.md](modules/health-product-evidence-check/MODULE.md) |

Supporting files (open only when the module points to them):

- `market-pricing-analysis`: [pricing-method.md](modules/market-pricing-analysis/references/pricing-method.md), [quality-evidence.md](modules/market-pricing-analysis/references/quality-evidence.md), [web-research.md](modules/market-pricing-analysis/references/web-research.md); scripts: `modules/market-pricing-analysis/scripts/normalize_prices.py`
- `health-product-evidence-check`: [product-evidence-framework.md](modules/health-product-evidence-check/references/product-evidence-framework.md)
