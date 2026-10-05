---
name: jupiter-routing
description: Primary execution path for PumpGrok. Obtain the best route via Jupiter, set slippage and priority fees, verify exact parameters against the approved ticket, and prepare a single-send transaction. Used only by SNIPER and EXIT.
---

# Jupiter Routing

## Purpose
Execute the single approved buy (or later sell) with the best available price and controlled risk.

## Preferred Tool Path
```bash
python /workspace/pumpgrok/tools/jupiter_quote.py \
  --input-mint <INPUT> --output-mint <OUTPUT> --amount <LAMPORTS> --slippage-bps <BPS>
```
Also estimate fee:
```bash
python /workspace/pumpgrok/tools/priority_fee.py --multiplier 1.25 --max-micro 50000
```

## Preconditions (ALL must be true)
1. RISK Verdict = CLEAR (or CONDITIONAL conditions met)
2. Explicit human message containing ticket ID + mint + size + max slippage
3. CHIEF confirmation that daily-loss limit is not breached
4. Live quote obtained within the last 30–60 seconds

## Rules
- Submit once only
- On any timeout or unknown result → do NOT retry; report “UNKNOWN RESULT – reconcile by signature”
- Immediately hand the filled position to RUG + EXIT

## Never
- Retry without a new human approval
- Change size or mint
- Execute on a different token than approved
