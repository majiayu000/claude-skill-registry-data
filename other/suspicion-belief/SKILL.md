---
name: suspicion-belief
description: "Use for reusable suspicion belief recipes in software and coding-agent work."
---

# Suspicion & belief modeling — recipes (generic tier)

On-demand recipes (1). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Don't conflate navigation failure with target ownership; make 'wrong commitment' sticky
`generic` · ⚠ _session-derived, unverified_

Do not collapse two distinct failure modes into one conclusion: an action that fails on first attempt may mean a transient/preliminary condition was not met (e.g. an agent never actually reached the target rectangle -- a navigation failure), not that the action is fundamentally invalid (e.g. the target belongs to someone else). Use a first-attempt failure to trigger a RETRY of the precondition (re-navigate) before concluding the target is invalid; treating the transient failure as permanent evidence corrupts belief. Conversely, once a conclusion is legitimately reached that a target is not actionable, make that knowledge STICKY -- persist it and prevent re-committing to the same target rather than recomputing and re-forgetting each visit, since persistent negative beliefs prevent oscillation.
  <sub>sources: opencode:ses_1fecece4dffe779FmeajgdwhMD</sub>
