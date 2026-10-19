---
name: imposter-tactics
description: "Use for imposter tactics recipes in scripted Coworld policy optimization."
---

# Imposter tactics — recipes (loop tier)

On-demand recipes (1). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Turn opponent scouting into IF-THEN counter-rules, and guard identity exchange in the policy layer
`loop`

When scouting an opponent policy, convert each identified weakness into a concrete IF-opponent-condition-THEN-our-counter-action rule and state whether it generalizes across seeds, so scouting yields directly actionable counter-play rather than descriptive notes. Relatedly, put information-leak guards for sensitive multi-party interactions (e.g. role/identity exchange in social-deduction games) in the POLICY layer, not only the strategy layer: abort the protocol when a hostile or unknown party is present and the room occupant count exceeds a safe threshold.
  <sub>sources: coworld-source-repos.crewrift-upload/optimizers/instructions/mvp/explo, codex:019e0817-8cba-79c2-aed4-d8bb6a4261d0</sub>
