---
name: risk-audit
description: Absolute safety gate for every Solana token. Runs a fail-closed checklist and returns only CLEAR, CONDITIONAL, or KILL. Used exclusively by the RISK Bot. A KILL cannot be overridden.
---

# Risk Audit

## Purpose
Prevent capital destruction from rugs, honeypots, malicious authorities, and concentrated insider dumps.

## Preferred Tool Path
```bash
python /workspace/pumpgrok/tools/authority_check.py --mint <TOKEN_MINT> [--rpc <URL>]
```
Parse the JSON. If `hasMintAuthority` or `hasFreezeAuthority` is true → strong KILL signal.

## Mandatory Checklist (run every time)
1. Mint authority – must be null / revoked
2. Freeze authority – must be null / revoked
3. LP status – burned or locked ≥ 6–12 months; quantify %
4. Sell / transfer tax – preferably 0 %; hard fail above 5–10 %
5. Honeypot / cannot-sell indicators
6. Top-10 holders (ex-LP) concentration – flag if > 20–25 %
7. Bundler / insider cluster detection
8. Deployer wallet history if visible
9. Token-2022 extensions – document any
10. Liquidity depth relative to intended size

## Output Schema
```
LEAD / TICKET-ID: ...
Verdict: CLEAR | CONDITIONAL | KILL
Residual Risks: 
1. ...
Evidence: [source + UTC]
Conditions (if CONDITIONAL): ...
Self-Audit: All 10 checks completed: YES / NO
```

## Never
- Soften a KILL because of narrative or FOMO
- Allow any other Bot to proceed past a KILL
- Skip or approximate any of the 10 checks
