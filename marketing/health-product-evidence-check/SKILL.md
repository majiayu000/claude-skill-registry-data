---
name: health-product-evidence-check
description: Automatically evaluate a health-related product, medicine-like item, supplement, cream/gel, brace, tape, massager, electrotherapy device, wearable, exercise/rehabilitation aid, or wellness product when the user shares a photo, label, link, or asks "işe yarar mı", "almaya değer mi", "10 üzerinden kaç", "zararlı mı", "reçeteli mi", "SGK karşılıyor mu", or "fiyatı iyi mi". Verify exact product/variant, ingredients or technical parameters, regulatory category, claims, finished-product evidence versus ingredient evidence, safety, contraindications, independent testing, advertising/affiliate incentives, current price, prescription and reimbursement status. Use medical evidence, market pricing, and evidence-integrity skills as needed. Do not diagnose, prescribe, or infer an unreadable label.
---

# Health Product Evidence Check

Answer the practical question: what the exact product is, what credible evidence says it can and cannot do, whether it fits the user's intended use, and whether the price is justified.

Read [references/product-evidence-framework.md](references/product-evidence-framework.md). Use `$research-medical-evidence` for clinical effectiveness/safety, `$market-pricing-analysis` for comparable current prices, `$physio-clinical-copilot` for fit within a rehabilitation case, and `$evidence-integrity-guard` for the final claim/citation audit.

## Workflow

1. **Resolve exact identity.** Record brand/manufacturer, product name, model/variant, concentration/strength, form, size/count, lot/expiry when relevant, market/jurisdiction, and intended use. From photos, state what is legible and ask for another image if a decisive field is unreadable.
2. **Classify the product.** Determine whether it is a medicine, medical device, supplement, cosmetic, food, exercise equipment, wellness product, or ambiguous. Verify current regulator/manufacturer records; marketplace category and visual appearance are not enough.
3. **Decompose claims.** Separate objective specifications, manufacturer claims, mechanism claims, clinical outcome claims, safety claims, and user-fit questions. Do not let “clinically tested” stand without an exact study and tested version.
4. **Match evidence to the exact item.** Distinguish:
   - evidence on the finished product and exact dose/settings;
   - evidence on one ingredient/component;
   - evidence on the broader product class;
   - theory or marketing with no patient-important outcome evidence.
5. **Assess effect and safety.** Match population, indication, comparator, outcomes, duration, dose, adverse effects, contraindications, interactions, device warnings, and meaningful effect size. Distinguish statistical from clinical importance.
6. **Audit incentives.** Identify seller/manufacturer pages, sponsored or affiliate reviews, coupon content, undisclosed commercial ties, and copied claims. Use them for declared specs/claims only; seek independent evidence for effectiveness and quality.
7. **Verify practical status.** For “reçeteli mi?”, reimbursement, recall, registration, allowed claims, warranty, or current price, check the current official Turkish authority/payer/manufacturer record and dated retailers as appropriate. Do not extrapolate from another country or an old rule.
8. **Compare value.** Normalize price per dose/use/unit and compare like-for-like alternatives. Include required consumables, warranty, durability, service, return conditions, and whether a simpler evidence-based option achieves the same goal.
9. **Conclude for the stated use.** State who may benefit, who should avoid or obtain professional review, what outcome is realistic, what is unknown, and the least costly sensible next step.

## Scoring without false precision

If the user requests a score, give three labeled rounded scores rather than one decorative number:

- **Kanıt gücü /10:** directness, quality, consistency, and clinical relevance of evidence.
- **Beklenen fayda /10:** likely magnitude for the stated goal and population, not universal effectiveness.
- **Fiyat/değer /10:** current total cost versus credible benefit and alternatives.

Then give one overall recommendation—`ALMAYA DEĞER`, `KOŞULLU`, `GEREKSİZ/DAHA İYİ ALTERNATİF VAR`, or `YETERSİZ BİLGİ`—with confidence. A score must not conceal uncertainty or safety limits.

## Hard rules

- Never infer product identity, ingredients, concentration, expiry, approval, or authenticity from an unclear image.
- Never treat registration or legal sale as proof of effectiveness, or lack of reimbursement as proof of ineffectiveness.
- Never transfer evidence from an ingredient to the finished product without dose/formulation/applicability limits.
- Never recommend starting, stopping, or changing a medicine. Route medication interactions and individualized use to the prescriber/pharmacist.
- For red flags, severe reactions, poisoning, electric/thermal injury, worsening neurological/cardiorespiratory symptoms, or another emergency possibility, stop routine product analysis and give appropriate urgent action.
- Do not use marketplace reviews as proof of medical benefit. They may reveal recurring usability or failure patterns only when identity and independence are considered.

## Output

Lead with the verdict and exact product identity. Then show evidence for the exact product versus its ingredients/class, realistic benefit, key risks/fit, commercial-incentive limitations, current prescription/reimbursement/price status when requested, alternatives, scores if requested, confidence, and what missing fact could change the verdict.
