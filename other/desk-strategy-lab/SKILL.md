---
name: desk-strategy-lab
description: Lightweight rules and paper-trading support for entry filters, position sizing, and exit logic. Allows the desk to experiment without touching live capital until rules are proven.
---

# Desk Strategy Lab

## Paper Mode
When engagement = paper, never call SNIPER for a real send.
Log the simulated fill with:
```bash
python /workspace/pumpgrok/tools/paper_sim.py --action buy|sell --ticket <ID> \
  --mint <mint> --size-usd <usd> --price <price> ...
```

## Changing Rules
Any change must be written into a dated file under research/ and requires explicit human approval before promotion to micro-live.
