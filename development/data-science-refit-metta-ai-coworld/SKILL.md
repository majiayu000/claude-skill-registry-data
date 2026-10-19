---
name: data-science-refit
description: "Use for data science refit recipes when optimizing a Coworld player."
---

# Data-science refit (outer loop) — recipes

On-demand recipes (21). Each is a trigger→action heuristic; pull the relevant one when its situation arises. Tier tags and ⚠ (unverified) as in AGENTS.md.

#### 1. Decode CvC replays correctly: zlib not gzip, and walk RLE shape-varying time-series
`loop` · ⚠ _session-derived, unverified_

Cogs-vs-Clips league replays are zlib-compressed (zlib.decompress(path.read_bytes()) then json.loads), living at experiments/league_replays/replays/<episode_id>.json.z with metadata at experiments/league_replays/metadata/<episode_id>.json. Object time-series (location/inventory/tag_ids) are run-length encoded storing [tick,value] only when the value CHANGED, so read value-at-tick-T as the largest entry whose tick<=T -- never assume one entry per tick. Junction location is a static [x,y] while an agent's is a time series (handle both shapes); a junction can hold net:cogs AND net:clips at once, so split territory into four states (cogs-only/clips-only/contested/neither) rather than subtracting (which yields negative counts); and there is no per-agent death count -- infos.alive is one end-of-episode bool, so detect deaths by counting hp-inventory 0-transitions.
  <sub>sources: opencode:ses_1fa64e46bffev9gR04uQlcT6kk</sub>

#### 2. Attribute CvC events carefully: alignment is logged one tick late, and metric scopes differ
`loop` · **negative result** · ⚠ _session-derived, unverified_

Two recurring CvC attribution traps. (1) To attribute a junction alignment to an agent, do NOT match the agent's logged position to the junction cell at the alignment tick -- the simulator records the alignment one tick AFTER the agent bumped it, so the agent is already adjacent; use a 4-neighbor adjacency check and also test the agent's position at tick-1. (2) Do not mix metric scopes: metadata's our_avg_metrics is averaged over OUR agents only (read our_agent_ids), but infos.agent[<metric>] is replay-wide over all 8 agents (our team plus partner), so mixing them silently double-counts the partner. The most reliable per-our-agent throughput stats come from summing inventory 'gained' deltas across the run-length series, not from pre-aggregated infos.attributes.
  <sub>sources: opencode:ses_1fa64e46bffev9gR04uQlcT6kk</sub>

#### 3. Take labels and joins from authoritative ID fields, never from manifests or list position
`loop` · **negative result**

Position- and manifest-based joins silently mismatch data to the wrong player/role -- a recurring corruption bug. Crewrift player_manifest roles are join-time and always read 'crew', so a manifest-based label silently zeroed all imposter labels and corrupted a model fit; take ground-truth roles from per-tick player_state rows instead. For episode scores, join by the authoritative per-policy identifier (policy_version_id / the API's per-policy scores field), NEVER by Player1..Player8 array position, because rotate_seats:true moves a policy through every seat; aggregate league standings by participant on policy_version_id broken out by crew/imposter role.
  <sub>sources: claude-code:0e7b14ca-ffd5-4137-9456-47485d3c6f87, codex:019e4c28-d516-7ca0-b145-153c152b4f43, codex:019eaea8-4f78-7072-b4b0-539df963b7df, player_labs/best_practices.md</sub>

#### 4. Pick the authoritative source per field: event-derived vs result-derived is not uniform
`loop` · **negative result** · ⚠ _session-derived, unverified_

Score-derived and event-derived metrics silently disagree, and neither is uniformly right -- choose per column and reconcile. For kills/timing, parse the replay event timeline (one analysis inferred 243 kills from final scores but the event stream gave the true 260, hash-validated); but fields built from intermediate events can OVERCOUNT (crew_tasks_remaining from task-completion events overcounted and had to be taken from final replay results). Build reconciliation into the tooling and check it before quoting numbers (a trusted run reported 560/560 processed, 0 replay errors, 0 hash failures, 0 event-vs-result mismatches).
  <sub>sources: codex:019e9656-7cfc-7032-ae70-82b6dbc0a053</sub>

#### 5. Never judge a policy on one aggregate score: decompose by role/opponent/submetric and against the corpus
`loop` · ⚠ _session-derived, unverified_

An aggregate score hides the story; decompose by role (the single most important cut), by opponent, and by behavioral sub-metric, then contextualize against the corpus distribution before judging. In a crewborg:v11 case the aggregate (wins most games) hid that as crew it won 5/5 but scored ~22 points below every opponent (Hedges g ~ -3.4) and as imposter lost all 5 with zero kills hitting the -10 floor. Establish baselines first (e.g. corpus mean 29.5, best 47.7, worst 1.64) so a 22.1 reads as below-average rather than being evaluated in isolation.
  <sub>sources: claude-code:3c867a71-3057-4e87-a149-4185e82ee728, opencode:ses_1ffba12c8ffegXTM7TLJ7oigMW</sub>

#### 6. Apply statistical rigor to policy comparisons: leaderboards on raw means are mostly noise
`loop`

Report effect sizes (not just means), run BOTH a mean-based (Welch t) and rank-based (Mann-Whitney) test, apply multiple-comparison correction (Benjamini-Hochberg), and pool matched batches for power. Top crewrift imposters cluster tightly: after BH correction across 28 pairwise comparisons only one pair separated by the rank test at q<0.05 and zero Welch tests survived, so with ~40-100 episodes per player 'best imposter' claims on raw means are mostly noise. Materialize results as SQLite tables (imposter_summary with per-player n/mean/sd/quartiles/win%/kills; imposter_pairwise with Hedges' g, Cliff's delta, Wasserstein distance in score points, and corrected p-values), not just printouts.
  <sub>sources: codex:019e941c-8eb9-7402-a77f-8fe75a5d19bf, player_labs/best_practices.md</sub>

#### 7. Read distribution shape, not just stdev; and re-verify every cited number, tagging its source
`loop`

Before treating higher variance as risk, inspect distribution shape: a rising stdev with unchanged median signals a one-sided upside outlier (good), not added downside, so report min/max alongside mean/sd. On any long write-up re-run the analysis to verify every figure -- multiple drafted numbers were wrong on recompute (junction gain 27%->23.3%, death-rate correlation 0.72->0.86). Two recurring traps: conflating team totals with per-agent values, and conflating per-match means with leaderboard scores. Cached match-means drift BELOW the live leaderboard because it keeps accumulating after the snapshot (V16 cached 31.75 vs leaderboard 34.06), so use leaderboard values for headline numbers, cached data for per-match detail, and state which source each number uses.
  <sub>sources: opencode:ses_1fa6f7b71ffeMqiFWPAD235jUs, archive/cogames_playground/alpha_cog/experiments/notebook/tournaments/</sub>

#### 8. Filter -100 connect-failure episodes before any pooling or analysis
`loop` · ⚠ _session-derived, unverified_

A score of -100 means CONNECT-FAILURE, not bad play, so drop those episodes before pooling, fitting, or judging. A degenerate episode scores connect-failed players -100 and everyone else 0 (e.g. [0,0,0,0,0,0,-100,-100]) graded across the lobby; this hit ~half the episodes in one experience-request batch AND the main league at once, so it was infra-wide, not player-specific.
  <sub>sources: claude-code:f70c9801-7ee7-499b-97f9-4fd0848a6b8e</sub>

#### 9. Treat death as a first-class multiplicative cost; score territory games on tick-junctions
`loop` · **negative result** · ⚠ _session-derived, unverified_

In territory-control coworld games the dominant late-game failure is agents dying into long inactive tails (max no-motion 5,000-7,000+ ticks in a 10k game), so ALWAYS compare deaths and max-no-motion alongside score. Each death drops then regains gear = 2 inventory transitions, so agents that appeared to 'switch roles' 19-107x/match (53 deaths ~ 106 transitions) were not switching -- the real problem was death rate; each death costs ~150 ticks of recovery (~9 deaths/agent = ~1350 lost ticks vs ~5.5 best). The right scoreboard metric is tick-junctions (alignments x average hold time), NOT raw alignment count: alpha_cog V14 added A* nav, aligned ~60% more junctions and gained ~80% more hearts yet scored LOWER because deaths doubled (11.5->24.3/agent) and retention dropped ~15%. Death-loop signature: miners losing more cargo than gained (965 vs 912) and re-equipping ~2.3x more.
  <sub>sources: opencode:ses_1fc6f16cfffe03SKAcP78Ua0IK, opencode:ses_1ff2ef8c8ffej7zC4A18jgSDFv, opencode:ses_1ffba12c8ffegXTM7TLJ7oigMW</sub>

#### 10. Probe the game engine directly for ground truth instead of re-vendoring its parser
`loop` · ⚠ _session-derived, unverified_

Probe the engine for authoritative state rather than re-implementing its parsing or guessing replay format from samples -- find the format source-of-truth in the game's own code. When the engine is in another language (e.g. Nim), have a Python script emit a tiny temporary engine-language program INSIDE the engine checkout (inheriting its import path / --path:src), compile it to read internal state (e.g. SimServer.walkMask), serialize raw, then build the player-side artifact from that. Pick a state-rich game (paint_arena, cogs-vs-clips) when bootstrapping extractors; among_them is hardest because its replays are INPUT-ONLY binary streams (time/player/key-bitmask plus joins/leaves/hash checkpoints) with no semantic events -- extracting kills/votes requires re-simulating recorded inputs against the original config.
  <sub>sources: codex:019eaee5-b54e-79f2-bf0f-ac59a6a1eae2, claude-code:93aaeccd-fa2d-4581-8f93-3e77e556db21</sub>

#### 11. Test every malformed-field path in replay/grader code, and define interestingness per game
`loop` · ⚠ _session-derived, unverified_

A grader/extractor reading coworld replay or results must specify AND test every missing/malformed-field path, not just the happy path: CvC inventory values are numeric resource IDs (map through item_names, guarding for item_names missing/wrong-shape or an ID absent); define behavior and add a test for when BOTH results.scores and replay.infos.episode_rewards are missing; and compact-history helpers over [[step,value],...] need defined behavior for reversed pairs, missing step 0, duplicate steps, and null fields. Define interestingness per game: PaintArena = (top final score - runner-up) / (width*height) clamped to 0..1; Cogs-vs-Clips has no single canonical metric, so combine several dependency-free replay-derived per-player-difference signals (score spread, total-reward spread, inventory/resource differences, role/gear acquisition, health/death spread, junction color-control changes).
  <sub>sources: auggie:79765dce-4e98-40f6-8606-5cd33f51d4c5, codex:019e66c3-638e-7e70-afdf-8f6df9299f6a</sub>

#### 12. Coworld pipeline artifact flow and the four-column extractor parquet contract
`loop` · ⚠ _session-derived, unverified_

Coworld pipeline flow: replay+results -> extractor -> parquet stats; then parquet+replay+results -> reporter -> HTML; then manifest + many parquet/replay/results -> optimizer. The extractor's parquet is the dense signal BOTH the reporter and optimizer consume, so its output design directly constrains what the optimizer can learn. It emits exactly four required columns: ts (int64 tick or unix-ms, per-game), player (int16 slot, -1 for global facts), key (string event/fact name), and value (a JSON-encoded string the consumer json.loads per row). The column is `player`, NOT `player_slot` (early READMEs saying player_slot are wrong). Games may add richer columns but downstream relies only on those four.
  <sub>sources: claude-code:93aaeccd-fa2d-4581-8f93-3e77e556db21</sub>

#### 13. Select C for calibration not ranking, evaluate only out-of-fold, and ship the transform contract
`loop` · tool: `suspicion_lab/tools/fit.py`

A suspicion posterior is consumed downstream as a probability, so select L1 strength C by ranking on mean CV log-loss (calibration), breaking ties with AUC -- not on AUC alone; after fitting, print an out-of-fold calibration table (predicted-probability bucket vs actual positive rate) and compare the fitted intercept against the empirical prior logit to catch miscalibration before shipping. Evaluate vote/decision quality ONLY on out-of-fold posteriors so the shipping gate is not inflated by in-sample fit, and run held-out meeting decisions through a vote-policy grid, shipping only policies that beat the always-skip baseline on net parity. Ship the input-transform contract (BIN_SPEC edges, LINEAR_CLIP ceiling) INSIDE the weights JSON and mirror it exactly in the runtime scorer -- offline fit and live agent must apply identical transforms or the weights are meaningless; clip count features to a bounded range (LINEAR_CLIP=5) so one extreme game cannot dominate.
  <sub>sources: personal_labs/crewrift_lab/suspicion_lab/tools/fit.py, personal_labs/crewrift_lab/suspicion_lab/tools/eval.py, personal_labs/crewrift_lab/suspicion_lab/README.md</sub>

#### 14. Structure the refit pipeline as idempotent crash-safe stages with quality gates downstream of collection
`loop`

Structure a learning/refit pipeline as discrete idempotent re-runnable stages (scrape-corpus -> expand-replays -> build dataset -> logistic fit -> eval -> vendor weights.json into the agent); gitignore rebuildable intermediates and commit only the small vendored deliverable. Make each stage crash-safe: scraping is idempotent and append-only with a per-round ledger (skip fully-scraped rounds, list newest-first since recency matters), with NO quality gate (gates belong downstream); expansion skips ok episodes, retries hash_failed only under a different ref, checkpoints the manifest every 50, and writes via temp-file-then-atomic-rename so an interrupted run never leaves a half-written cache; dataset assembly gates inclusion on an explicit trace_complete completeness flag (drop hash-failed/truncated, log skip counts) and catches per-episode corruption to continue past one bad replay.
  <sub>sources: personal_labs/crewrift_lab/WORKING_CONTEXT.md, personal_labs/crewrift_lab/suspicion_lab/README.md, personal_labs/crewrift_lab/suspicion_lab/tools/scrape_corpus.py, personal_labs/crewrift_lab/suspicion_lab/tools/expand_corpus.py (+2)</sub>

#### 15. Match offline constants to the live game and version-match the replay expander
`crewrift`

An offline study's findings only transfer if its constants match the live game's: e.g. 32px grid cell = agent_tracking.GRID_CELL_SIZE, 250-tick approach window = SEARCH_LEAD_TICKS, 48px isolation radius = opportunity.BASE_ISOLATION_RADIUS. The state-snapshot cadence chosen at expansion (--snapshot-every, default 24 ticks) becomes the sample_unit_ticks the model assumes, so pick it deliberately and keep it consistent across the whole corpus -- changing it mid-corpus silently changes the unit of every count/duration feature. The replay-expansion binary must be version-matched to the game build that produced the replays; record a per-episode hash_failed status on a build-hash mismatch because that episode came from a different build and its expanded evidence cannot be trusted.
  <sub>sources: personal_labs/crewrift_lab/suspicion_lab/tools/button_runner_study.py, personal_labs/crewrift_lab/suspicion_lab/tools/expand_corpus.py, personal_labs/crewrift_lab/suspicion_lab/README.md</sub>

#### 16. Gate unattended champion-refit on hard quality bars; treat fitted weights as non-stationary
`crewrift`

Gate an unattended nightly champion-refit loop on hard checks that abort and leave the current champion untouched on ANY failure: CV AUC >= 0.70, training corpus >= 500 games, the full agent test suite passing, and a local smoke test -- only after all pass should it vendor weights, build, upload, and submit (the corpus-size and AUC bars must pass before fit.py output is accepted). Treat weights fit to a league field as non-stationary because the field evolves: date-stamp corpus segments, prefer recent games, and plan an explicit refit cadence. As a confidence signal, track directional stability of cues across corpus sizes -- in the crewrift refit every cue kept its sign from the 341-game interim fit to the full 1,857-game corpus, indicating real directions not small-sample artifacts.
  <sub>sources: personal_labs/crewrift_lab/suspicion_lab/README.md, personal_labs/crewrift_lab/crewborg/data/suspicion_weights.json, personal_labs/crewrift_lab/crewrift/crewborg/docs/designs/suspicion-le</sub>

#### 17. Crewrift event log layout: detect missed votes from results first, expand replays only for survivors
`crewrift` · ⚠ _session-derived, unverified_

The Crewrift expand-replay event log (crewrift-events/v1, per-episode JSONL) carries vote_called_button (player=caller slot, ts=tick), kill, body_state, and player_state samples (x,y,room,kill_cooldown,button_calls_used) plus map_geometry; reconstruct a runner's button approach by walking that player's player_state samples backward from their vote_called_button tick (confirmed config: kill_cooldown_ticks 500, button_calls 1, imposter_count 2). When hunting missed votes, detect from episode result fields FIRST (results.json has per-slot vote_timeout, vote_skip, vote_players; scan keyed by policy_version_id NOT seat slot because rotate_seats moves the player) and expand_replay only the few episodes still suspicious. When a format stores only config plus join/leave/input records, first check whether the results artifact exposes imposter/crew arrays directly; otherwise recover role/task assignment from the container startup logs (often a compact assignment table) or by re-running the sim's start routine from the replay config.
  <sub>sources: claude-code:ef964049-4e16-4c32-b7f1-32871349d20a, codex:019eaea8-4f78-7072-b4b0-539df963b7df, codex:019ea9af-7020-7550-b427-d3478fed2057</sub>

#### 18. CvC score and metric field locations across the three stat buckets
`crewrift` · ⚠ _session-derived, unverified_

For a Cogs-vs-Clips player, the episode score lives at data['missions'][0]['mission_summary']['per_episode_per_policy_avg_rewards']['0'][0], and key decision metrics are split across three buckets that must ALL be parsed: avg_game_stats (e.g. cogs/aligned.junction.gained), avg_time_averaged_game_stats (e.g. cogs/aligned.junction.held, clips/aligned.junction.held), and per-policy avg_agent_metrics (heart.gained, miner.gained, aligner.gained, scout.gained, status.death, action.noop.success, action.move.failed, hp.amount, status.max_steps_without_motion, cell.unique_visited).
  <sub>sources: codex:019e1579-a737-7b70-bf0e-172ff04307cf</sub>

#### 19. Validate the metric-to-objective link, and attribute mean/median divergence to specific tail matches
`loop`

Do not optimize an intermediate metric before confirming it maps to the objective: counterintuitive correlations (e.g. dying more while scoring more) are signal not noise, and the 'safe' intuitive metric can be the losing one -- validate the link before treating the metric as a target. A change can have a correct mechanism yet regress the tournament mean while improving the median: cargo batching raised median +4.61 but dropped mean -1.39 by reintroducing tail risk (one 2.02-score match where both your agents mined and the team had only the partner's lone aligner), so when mean and median diverge attribute the gap to specific tail matches via replay inspection before judging. And a self-play A/B win may not generalize: 'concentrate mining on K=2 scarcest elements wins' was strongly self-play-supported but contributed only ~0.5 pts/match (below noise) once partner-induced tournament variance dominated -- tag self-play-only conclusions as dubious until tournament replay data confirms them.
  <sub>sources: player_labs/best_practices.md, archive/cogames_playground/alpha_cog/docs/paper/paper.md</sub>

#### 20. Put asset/palette constants in the loader and assert layout at import time
`generic`

Put game-palette constants and atlas slot indices in the data/asset-loader module that owns them rather than in a compute-kernel module, and have the atlas loader assert at import time that the loaded JSON layout matches the named constants, so drift between named indices and the actual atlas layout fails loudly at startup instead of silently mis-decoding pixels.
  <sub>sources: players_checkouts/players/archive/players/among_them/coborg/PLAN.md</sub>

#### 21. Record join-disambiguation assumptions and report full benchmark distributions with worst-case replay URLs
`loop`

When joining leaderboard rows to active memberships and a player has multiple, prefer substatus=='champion', otherwise the newest active membership by created_at -- and record this disambiguation assumption in the final report so the join logic is auditable. When summarizing a policy benchmark, compute the requester score per episode against the episode max, track ties for top score, and report completed/requested count, failed count, mean/median/min/max requester score, per-policy averages, and replay URLs for the worst outliers so bad cases can be inspected directly.
  <sub>sources: players_checkouts/players/players/crewrift/crewborg/docs/experience-re</sub>
