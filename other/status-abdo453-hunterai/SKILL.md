---
name: "status"
description: "Show engagement dashboard with program info, scope, brain state, findings, agent activity, and cost estimate."
---

# Status

*Sourced from h-mmer-pentest-agents*

Show the engagement status dashboard.

Run `uv run python3 ../../tools/statusline.py` to display the full dashboard.

After displaying, offer relevant next actions based on the state:
- If no scope: suggest `/sync`
- If no brain: suggest `/brain init`
- If no findings: suggest `/quickscan` or `/fullscan`
- If findings but no reports: suggest `/report`
- If exhausted vectors are high: suggest focusing on untested areas

## Top-Tier Dashboard Bar

Status should drive the next decision.

Always surface:
- highest-value untested target
- strongest confirmed finding not yet reported
- chain-pending feeders
- stale recon or scope data
- blockers requiring user action
- cost burn versus validated output
- evidence gaps before submission

End with exactly three recommended next actions ordered by expected value. Avoid generic "continue hunting" unless the target and vuln class are named.

