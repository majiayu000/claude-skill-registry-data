---
name: routes
description: "Skill for the Routes area of Securacy. 12 symbols across 4 files."
---

# Routes

12 symbols | 4 files | Cohesion: 92%

## When to Use

- Working with code in `backend/`
- Understanding how parseROIJustification, downloadbusinessImpactasPDF, load_prompt_template work
- Modifying routes-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `backend/buddlyai/Routes/AppSecController.py` | load_prompt_template, getTopThreeThreatsWithHighestCVSSScore, getMitigationsForTopThreats, getBusinessImpactFromThreatAnalysis, run_threat_analysis (+3) |
| `backend/buddlyai/appsec/downloadresults.py` | parseROIJustification, downloadbusinessImpactasPDF |
| `backend/buddlyai/Routes/ThreatsController.py` | load_threats |
| `backend/buddlyai/DB/DBservice.py` | get_threat_runs_by_user |

## Entry Points

Start here when exploring this area:

- **`parseROIJustification`** (Function) — `backend/buddlyai/appsec/downloadresults.py:703`
- **`downloadbusinessImpactasPDF`** (Function) — `backend/buddlyai/appsec/downloadresults.py:792`
- **`load_prompt_template`** (Function) — `backend/buddlyai/Routes/AppSecController.py:45`
- **`getTopThreeThreatsWithHighestCVSSScore`** (Function) — `backend/buddlyai/Routes/AppSecController.py:55`
- **`getMitigationsForTopThreats`** (Function) — `backend/buddlyai/Routes/AppSecController.py:93`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `parseROIJustification` | Function | `backend/buddlyai/appsec/downloadresults.py` | 703 |
| `downloadbusinessImpactasPDF` | Function | `backend/buddlyai/appsec/downloadresults.py` | 792 |
| `load_prompt_template` | Function | `backend/buddlyai/Routes/AppSecController.py` | 45 |
| `getTopThreeThreatsWithHighestCVSSScore` | Function | `backend/buddlyai/Routes/AppSecController.py` | 55 |
| `getMitigationsForTopThreats` | Function | `backend/buddlyai/Routes/AppSecController.py` | 93 |
| `getBusinessImpactFromThreatAnalysis` | Function | `backend/buddlyai/Routes/AppSecController.py` | 440 |
| `run_threat_analysis` | Function | `backend/buddlyai/Routes/AppSecController.py` | 51 |
| `getSecuracyThreats` | Function | `backend/buddlyai/Routes/AppSecController.py` | 348 |
| `getSecuracyThreats1` | Function | `backend/buddlyai/Routes/AppSecController.py` | 386 |
| `load_threats` | Function | `backend/buddlyai/Routes/ThreatsController.py` | 180 |
| `get_threat_runs_by_user` | Function | `backend/buddlyai/DB/DBservice.py` | 373 |
| `_enrich_threats_with_cvss` | Function | `backend/buddlyai/Routes/AppSecController.py` | 75 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Appsec | 2 calls |

## How to Explore

1. `gitnexus_context({name: "parseROIJustification"})` — see callers and callees
2. `gitnexus_query({query: "routes"})` — find related execution flows
3. Read key files listed above for implementation details
