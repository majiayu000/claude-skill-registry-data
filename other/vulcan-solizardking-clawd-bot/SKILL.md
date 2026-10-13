---
description: "Entry-point skill for Phoenix perpetuals through Vulcan/Rise SDK inside solana-clawd. Use before answering or acting on Vulcan, Phoenix DEX, Solana perps, paper trading, live trading, margin, TP/SL, TWAP, grid, TA strategies, or perps agent setup."
---
# Vulcan Skill Pack

Canonical source: `../../vulcan-cli-master/skills/vulcan/SKILL.md`

Load order for solana-clawd perps work:

1. Read `../../vulcan-cli-master/CONTEXT.md`.
2. Read `../../vulcan-cli-master/skills/INDEX.md`.
3. Read this entry skill's canonical source.
4. Load focused skills from `skills/vulcan-*` as needed.

Non-negotiable runtime rules:

- Paper and dry-run modes must never require wallet signing.
- Live/dangerous operations require explicit user approval and Vulcan `--yes` or MCP `acknowledged=true`.
- Before opening exposure, inspect market, margin, and current positions.
- Never guess lot sizes; use `vulcan-lot-size-calculator`.
- Never read, print, export, or infer private keys, wallet passwords, or MCP config secrets.
- Report every execution event and full transaction signature immediately.

This wrapper exists so solana-clawd exposes the bundled Vulcan skill pack from its own `skills/` catalog while preserving Vulcan's upstream docs as authoritative.
