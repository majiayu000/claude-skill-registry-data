---
name: dl-scoring
description: Scoring v3 hotLeadScore (5 axes, poids, signaux enrichment)
paths:
  - "src/core/services/scoring*"
  - "src/core/services/matching*"
---

# Scoring v3 — hotLeadScore

Formula (5 axes, 2026-03-26):
```
0.22 x need + 0.25 x fundability(+opco+mecenat) + 0.18 x urgency + 0.15 x reachability + 0.20 x enrichment
```

## Enrichment signals
- DPE passoire (dl_dpe_tertiaire)
- CNIL controls/dept (dl_cnil_controles)
- Qualiopi formation (dl_organismes_formation)
- EPCI status (dl_epci)
- ERP accessibility (dl_erp_accessibilite)

## Entity Cards (Zod-validated JSONB)
- `EntityCard` — organisation profile (scores, summaries, provenance)
- `SubventionCard` — funding program (eligibility, amounts, dates)
- `MarcheCard` — procurement contract (buyer, CPV, renewal prediction)
- `TerritoryCard` — department profile (stats, sectors, financeurs)
