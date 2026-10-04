---
name: mapi-score-calculator
description: Calculate the Maryland Aggregate Pathology Index (MAPI) on a deceased donor procurement kidney biopsy to predict graft survival and decide single vs dual vs discard allocation. Trigger when a clinician asks "what's the MAPI score", "interpret donor kidney biopsy", "should I use this marginal kidney", "MAPI cutoff for transplant", "procurement biopsy scoring", or has histology results from a deceased donor kidney and needs an objective grading.
---

# MAPI Score Calculator — Deceased Donor Kidney Biopsy

Use this skill when a **procurement biopsy** has been performed on a deceased donor kidney (typically a marginal/ECD donor) and an objective histological grading is needed to decide:

- **Single kidney transplant** (low risk)
- **Dual kidney transplant** (intermediate risk)
- **Discard** (high risk)

The Maryland Aggregate Pathology Index (MAPI) is the scoring system recommended by ISOT 2025 for marginal deceased donor kidney evaluation.

---

## STEP 1 — Ensure biopsy adequacy

A reliable MAPI requires:

- **Wedge biopsy** (preferred) or **needle core biopsy** with adequate cortex.
- **≥25 glomeruli** for valid glomerulosclerosis assessment.
- **At least one artery** for arteriolar scoring.
- Both kidneys assessed if dual transplant is being considered.

If the biopsy is inadequate → repeat or proceed on clinical grounds alone.

---

## STEP 2 — Score the four histological components

| Component | Finding | Points |
|---|---|---|
| **Glomerulosclerosis** | <15% | 0 |
|  | 15–20% | 4 |
|  | >20% | 7 |
| **Tubular atrophy** | Absent | 0 |
|  | <50% of cortex affected | 1 |
|  | ≥50% of cortex affected | 3 |
| **Interstitial fibrosis** | Absent | 0 |
|  | Mild (Banff ci1, 6–25%) | 2 |
|  | Moderate–severe (Banff ci2/ci3, >25%) | 5 |
| **Arteriolar narrowing / hyalinosis** | Absent | 0 |
|  | Wall thickening less than the diameter of the lumen | 2 |
|  | Wall thickening greater than the diameter of the lumen | 4 |

**MAPI total = sum of all four components** (range 0–19).

---

## STEP 3 — Interpret the score

| MAPI | Risk band | Approximate 5-yr graft survival | Action |
|---|---|---|---|
| **<7** | Low | ~90% | ✅ **Use as single kidney transplant** |
| **7–11** | Intermediate | ~70–80% | ⚠️ **Dual kidney transplant** (en bloc or paired single) — OR allocate single only to lower-immunological-risk recipient |
| **>11** | High | <70% | ❌ **Discard**, or dual transplant only if recipient has no alternative |

---

## STEP 4 — Combine with clinical context

Histology is one input — combine with:

- Donor age (>70 raises threshold for single use)
- KDRI / KDPI if available
- Cold ischaemia time
- Recipient sensitisation, age, and waiting time
- Macroscopic appearance of kidney (vasculature, parenchyma)

**ISOT 2025 guidance:** if procurement biopsy is not feasible, base the decision on **clinical severity, degree of oliguria, and need for dialysis** in the donor.

---

## STEP 5 — Document the decision

Output should include the MAPI score, the four component scores, the risk band, and the allocation decision.

---

## CLINICAL GUARDRAILS

- **MAPI is for marginal/ECD donors** — not needed for standard criteria donors.
- **The score is one tool, not the entire decision** — a MAPI of 8 in a 35-year-old donor with brief CIT is very different from MAPI 8 in a 72-year-old after 20 hours of CIT.
- **Glomerulosclerosis dominates the score** — if >20% globally sclerosed glomeruli, the score is already ≥7 regardless of other components.
- **Dual kidney transplant adds technical complexity and anastomosis time** — weigh this against the expected graft survival benefit.
- **A single reading is operator-dependent** — where possible, get a transplant pathologist (not a general pathologist on call) to score.
- **AKI changes the picture** — see the AKI donor decision skill; tubular injury from AKI can over-inflate the tubular atrophy score on frozen section.

---

## OUTPUT TEMPLATE

```
DONOR: [age, sex, comorbidities, cause of death, CIT]
BIOPSY: [type, glomerulus count, adequacy]

Glomerulosclerosis: __% → __ points
Tubular atrophy: __ → __ points
Interstitial fibrosis: __ → __ points
Arteriolar narrowing: __ → __ points

MAPI total: __ / 19
Risk band: [Low / Intermediate / High]

Decision: [Single KT / Dual KT / Discard]
Justification: [combine MAPI + clinical context]
```

---

## SOURCE

Munivenkatappa RB, Schweitzer EJ, Papadimitriou JC, et al. The Maryland aggregate pathology index: a deceased donor kidney biopsy scoring system for predicting graft failure. *American Journal of Transplantation* 2008;8(11):2316–2324. DOI: 10.1111/j.1600-6143.2008.02370.x

Referenced in: Balwani MR, Kute VB, Shrimali J, et al. ISOT position statement on the feasibility of an organ for transplantation from brain-dead deceased donors: a Delphi consensus. *The Lancet Regional Health – Southeast Asia* 2025;39:100628 (Supplementary Table S4, marginal donor kidney evaluation).
