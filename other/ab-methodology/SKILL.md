---
name: ab-methodology
description: "Use for Crewrift-specific ab methodology recipes when optimizing a player."
---

# A/B methodology & attribution — recipes (crewrift tier)

On-demand recipes (1). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Match episode comparability conditions; use pickup VOR, all-identical meetings, and same-role twins as cheap signals
`crewrift` · ⚠ _session-derived, unverified_ · tool: `cogames pickup`

When comparing crewrift episodes for the same crewborg policy, only compare episodes sharing the same policy id, same game id, and maxTicks >= 2000 — short episodes (maxTicks=400) score very differently (partial task counts, no kill windows) and contaminate the comparison. Use `cogames pickup` against a `--pool` of policies to get a relative value-over-replacement (VOR) number rather than plain scrimmage when you want relative strength. To judge meeting/social-deduction quality (chat + vote dynamics), use an all-agents-identical setup since meeting dynamics only emerge when all participants share the loop. And running two copies of the same policy in the SAME role within one match gives a free built-in A/B of which behaviors are robust vs luck-dependent: two imposters of one policy diverged sharply (0 kills+ejected vs 3 kills+survived) purely from spawn position, cheaply revealing robustness without separate matches.
  <sub>sources: claude-code:309519c5-1e0c-4dfe-b7df-126611184851, claude-code:b1fb3772-05cf-4de7-b1d7-a0732e2a61e3, codex:019e1591-004e-7040-b768-062bd8e6acd4, claude-code:91f456a7-41e8-4a89-98e9-44e379160b15</sub>
