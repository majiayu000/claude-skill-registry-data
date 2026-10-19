---
name: data-science-refit
description: "Use for Crewrift-specific data science refit recipes when optimizing a player."
---

# Data-science refit (outer loop) — recipes (crewrift tier)

On-demand recipes (2). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Select C for calibration not ranking, evaluate only out-of-fold, and ship the transform contract
`crewrift` · tool: `suspicion_lab/tools/fit.py`

A suspicion posterior is consumed downstream as a probability, so select L1 strength C by ranking on mean CV log-loss (calibration), breaking ties with AUC -- not on AUC alone; after fitting, print an out-of-fold calibration table (predicted-probability bucket vs actual positive rate) and compare the fitted intercept against the empirical prior logit to catch miscalibration before shipping. Evaluate vote/decision quality ONLY on out-of-fold posteriors so the shipping gate is not inflated by in-sample fit, and run held-out meeting decisions through a vote-policy grid, shipping only policies that beat the always-skip baseline on net parity. Ship the input-transform contract (BIN_SPEC edges, LINEAR_CLIP ceiling) INSIDE the weights JSON and mirror it exactly in the runtime scorer -- offline fit and live agent must apply identical transforms or the weights are meaningless; clip count features to a bounded range (LINEAR_CLIP=5) so one extreme game cannot dominate.
  <sub>sources: personal_labs/crewrift_lab/suspicion_lab/tools/fit.py, personal_labs/crewrift_lab/suspicion_lab/tools/eval.py, personal_labs/crewrift_lab/suspicion_lab/README.md</sub>

#### 2. Crewrift event log layout: detect missed votes from results first, expand replays only for survivors
`crewrift` · ⚠ _session-derived, unverified_

The Crewrift expand-replay event log (crewrift-events/v1, per-episode JSONL) carries vote_called_button (player=caller slot, ts=tick), kill, body_state, and player_state samples (x,y,room,kill_cooldown,button_calls_used) plus map_geometry; reconstruct a runner's button approach by walking that player's player_state samples backward from their vote_called_button tick (confirmed config: kill_cooldown_ticks 500, button_calls 1, imposter_count 2). When hunting missed votes, detect from episode result fields FIRST (results.json has per-slot vote_timeout, vote_skip, vote_players; scan keyed by policy_version_id NOT seat slot because rotate_seats moves the player) and expand_replay only the few episodes still suspicious. When a format stores only config plus join/leave/input records, first check whether the results artifact exposes imposter/crew arrays directly; otherwise recover role/task assignment from the container startup logs (often a compact assignment table) or by re-running the sim's start routine from the replay config.
  <sub>sources: claude-code:ef964049-4e16-4c32-b7f1-32871349d20a, codex:019eaea8-4f78-7072-b4b0-539df963b7df, codex:019ea9af-7020-7550-b427-d3478fed2057</sub>
