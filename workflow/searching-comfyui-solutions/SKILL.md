---
name: searching-comfyui-solutions
description: Searches bundled capability-Skill templates and (optionally) trusted web sources for ComfyUI workflow recipes matching a query, then ranks the results conservatively with source provenance. Use whenever the planner encounters a request that does not map cleanly to a bundled capability-Skill goal, or whenever the caller needs to ground a workflow decision in a retrieved recipe. This Skill has network access.
---

# searching-comfyui-solutions

Research-first Skill. Network access is **declared** and must be present in
`policies/skill_provenance.yaml`'s `network_allowlist`.

## When this Skill applies
- The planner found no matching capability-Skill keyword for a clause.
- The caller explicitly asked for search grounding.

## Pipeline
1. `scripts/search_local.py` — greps `.claude/skills/*/templates/` for
   keyword matches; results carry `trust_tier="bundled"`.
2. `scripts/search_web.py` — reads `policies/search_allowlist.yaml`, fetches
   a DuckDuckGo HTML results page (stdlib `urllib.request`), extracts top N
   links; results carry `trust_tier="web_unverified"` plus `retrieved_at`.
3. `scripts/rank_results.py` — merges both sets, prefers local, applies a
   conservative ranking (favors no result over a low-confidence wrong one).

## Conservative ranking rule
If the top hit's score is below a threshold (default 0.3), emit an empty
list — never return a low-confidence result that the planner might anchor
on. Callers should fall back to asking the user.

## Scripts
- `scripts/search_local.py`
- `scripts/search_web.py` (network; allowlist enforced)
- `scripts/rank_results.py`

## Error handling
Network failures return `{"results": [], "error": "..."}` — never raise.
