---
name: holder-and-flow-analysis
description: Analyse early buyers, top-holder concentration, wallet clusters, and smart-money flows. Used by WHALE after RISK CLEAR or CONDITIONAL.
---

# Holder and Flow Analysis

## Preferred Tool Path
```bash
python /workspace/pumpgrok/tools/holder_check.py --mint <TOKEN_MINT> --limit 20
```

## Output Schema
```
LEAD / TICKET-ID: ...
Smart-Money Signal: High | Medium | Low | None
Supporting Addresses: ...
Clusters Detected: yes/no + description
UTC Timestamp: ...
Hand-off: CHIEF + RISK
```

## Never
- Authorise a buy
- Override a RISK KILL
- Treat pure social mentions as smart-money evidence
