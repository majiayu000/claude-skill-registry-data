---
name: data-science-refit
description: "Use for data science refit recipes in scripted Coworld policy optimization."
---

# Data-science refit (outer loop) — recipes (loop tier)

On-demand recipes (13). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Decode CvC replays correctly: zlib not gzip, and walk RLE shape-varying time-series
`loop` · ⚠ _session-derived, unverified_

Cogs-vs-Clips league replays are zlib-compressed (zlib.decompress(path.read_bytes()) then json.loads), living at experiments/league_replays/replays/<episode_id>.json.z with metadata at experiments/league_replays/metadata/<episode_id>.json. Object time-series (location/inventory/tag_ids) are run-length encoded storing [tick,value] only when the value CHANGED, so read value-at-tick-T as the largest entry whose tick<=T -- never assume one entry per tick. Junction location is a static [x,y] while an agent's is a time series (handle both shapes); a junction can hold net:cogs AND net:clips at once, so split territory into four states (cogs-only/clips-only/contested/neither) rather than subtracting (which yields negative counts); and there is no per-agent death count -- infos.alive is one end-of-episode bool, so detect deaths by counting hp-inventory 0-transitions.
  <sub>sources: opencode:ses_1fa64e46bffev9gR04uQlcT6kk</sub>

#### 2. Attribute CvC events carefully: alignment is logged one tick late, and metric scopes differ
`loop` · **negative result** · ⚠ _session-derived, unverified_

Two recurring CvC attribution traps. (1) To attribute a junction alignment to an agent, do NOT match the agent's logged position to the junction cell at the alignment tick -- the simulator records the alignment one tick AFTER the agent bumped it, so the agent is already adjacent; use a 4-neighbor adjacency check and also test the agent's position at tick-1. (2) Do not mix metric scopes: metadata's our_avg_metrics is averaged over OUR agents only (read our_agent_ids), but infos.agent[<metric>] is replay-wide over all 8 agents (our team plus partner), so mixing them silently double-counts the partner. The most reliable per-our-agent throughput stats come from summing inventory 'gained' deltas across the run-length series, not from pre-aggregated infos.attributes.
  <sub>sources: opencode:ses_1fa64e46bffev9gR04uQlcT6kk</sub>

#### 3. Filter -100 connect-failure episodes before any pooling or analysis
`loop` · ⚠ _session-derived, unverified_

A score of -100 means CONNECT-FAILURE, not bad play, so drop those episodes before pooling, fitting, or judging. A degenerate episode scores connect-failed players -100 and everyone else 0 (e.g. [0,0,0,0,0,0,-100,-100]) graded across the lobby; this hit ~half the episodes in one experience-request batch AND the main league at once, so it was infra-wide, not player-specific.
  <sub>sources: claude-code:f70c9801-7ee7-499b-97f9-4fd0848a6b8e</sub>

#### 4. Treat death as a first-class multiplicative cost; score territory games on tick-junctions
`loop` · **negative result** · ⚠ _session-derived, unverified_

In territory-control coworld games the dominant late-game failure is agents dying into long inactive tails (max no-motion 5,000-7,000+ ticks in a 10k game), so ALWAYS compare deaths and max-no-motion alongside score. Each death drops then regains gear = 2 inventory transitions, so agents that appeared to 'switch roles' 19-107x/match (53 deaths ~ 106 transitions) were not switching -- the real problem was death rate; each death costs ~150 ticks of recovery (~9 deaths/agent = ~1350 lost ticks vs ~5.5 best). The right scoreboard metric is tick-junctions (alignments x average hold time), NOT raw alignment count: alpha_cog V14 added A* nav, aligned ~60% more junctions and gained ~80% more hearts yet scored LOWER because deaths doubled (11.5->24.3/agent) and retention dropped ~15%. Death-loop signature: miners losing more cargo than gained (965 vs 912) and re-equipping ~2.3x more.
  <sub>sources: opencode:ses_1fc6f16cfffe03SKAcP78Ua0IK, opencode:ses_1ff2ef8c8ffej7zC4A18jgSDFv, opencode:ses_1ffba12c8ffegXTM7TLJ7oigMW</sub>

#### 5. Probe the game engine directly for ground truth instead of re-vendoring its parser
`loop` · ⚠ _session-derived, unverified_

Probe the engine for authoritative state rather than re-implementing its parsing or guessing replay format from samples -- find the format source-of-truth in the game's own code. When the engine is in another language (e.g. Nim), have a Python script emit a tiny temporary engine-language program INSIDE the engine checkout (inheriting its import path / --path:src), compile it to read internal state (e.g. SimServer.walkMask), serialize raw, then build the player-side artifact from that. Pick a state-rich game (paint_arena, cogs-vs-clips) when bootstrapping extractors; among_them is hardest because its replays are INPUT-ONLY binary streams (time/player/key-bitmask plus joins/leaves/hash checkpoints) with no semantic events -- extracting kills/votes requires re-simulating recorded inputs against the original config.
  <sub>sources: codex:019eaee5-b54e-79f2-bf0f-ac59a6a1eae2, claude-code:93aaeccd-fa2d-4581-8f93-3e77e556db21</sub>

#### 6. Test every malformed-field path in replay/grader code, and define interestingness per game
`loop` · ⚠ _session-derived, unverified_

A grader/extractor reading coworld replay or results must specify AND test every missing/malformed-field path, not just the happy path: CvC inventory values are numeric resource IDs (map through item_names, guarding for item_names missing/wrong-shape or an ID absent); define behavior and add a test for when BOTH results.scores and replay.infos.episode_rewards are missing; and compact-history helpers over [[step,value],...] need defined behavior for reversed pairs, missing step 0, duplicate steps, and null fields. Define interestingness per game: PaintArena = (top final score - runner-up) / (width*height) clamped to 0..1; Cogs-vs-Clips has no single canonical metric, so combine several dependency-free replay-derived per-player-difference signals (score spread, total-reward spread, inventory/resource differences, role/gear acquisition, health/death spread, junction color-control changes).
  <sub>sources: auggie:79765dce-4e98-40f6-8606-5cd33f51d4c5, codex:019e66c3-638e-7e70-afdf-8f6df9299f6a</sub>

#### 7. Coworld pipeline artifact flow and the four-column extractor parquet contract
`loop` · ⚠ _session-derived, unverified_

Coworld pipeline flow: replay+results -> extractor -> parquet stats; then parquet+replay+results -> reporter -> HTML; then manifest + many parquet/replay/results -> optimizer. The extractor's parquet is the dense signal BOTH the reporter and optimizer consume, so its output design directly constrains what the optimizer can learn. It emits exactly four required columns: ts (int64 tick or unix-ms, per-game), player (int16 slot, -1 for global facts), key (string event/fact name), and value (a JSON-encoded string the consumer json.loads per row). The column is `player`, NOT `player_slot` (early READMEs saying player_slot are wrong). Games may add richer columns but downstream relies only on those four.
  <sub>sources: claude-code:93aaeccd-fa2d-4581-8f93-3e77e556db21</sub>

#### 8. Structure the refit pipeline as idempotent crash-safe stages with quality gates downstream of collection
`loop`

Structure a player-weight refit pipeline as discrete idempotent re-runnable stages (scrape episode corpus -> expand replays -> build dataset -> fit -> eval -> vendor weights into the agent); gitignore rebuildable intermediates and commit only the small vendored deliverable. Make each stage crash-safe: scraping is idempotent and append-only with a per-round ledger (skip fully-scraped rounds, list newest-first since recency matters), with NO quality gate (gates belong downstream); expansion skips ok episodes, retries hash_failed only under a different ref, checkpoints the manifest periodically (e.g. every 50), and writes via temp-file-then-atomic-rename so an interrupted run never leaves a half-written cache; dataset assembly gates inclusion on an explicit completeness flag (drop hash-failed/truncated, log skip counts) and catches per-episode corruption to continue past one bad replay.
  <sub>sources: personal_labs/crewrift_lab/WORKING_CONTEXT.md, personal_labs/crewrift_lab/suspicion_lab/README.md, personal_labs/crewrift_lab/suspicion_lab/tools/scrape_corpus.py, personal_labs/crewrift_lab/suspicion_lab/tools/expand_corpus.py (+2)</sub>

#### 9. Match offline constants to the live game and version-match the replay expander
`loop`

An offline study's findings only transfer if its constants match the live game's (e.g. grid cell size, approach-window ticks, isolation radius must equal the game's named constants). The state-snapshot cadence chosen at replay expansion (e.g. --snapshot-every, default 24 ticks) becomes the sample_unit_ticks the model assumes, so pick it deliberately and keep it consistent across the whole corpus -- changing it mid-corpus silently changes the unit of every count/duration feature. The replay-expansion binary must be version-matched to the game build that produced the replays; record a per-episode hash_failed status on a build-hash mismatch because that episode came from a different build and its expanded evidence cannot be trusted.
  <sub>sources: personal_labs/crewrift_lab/suspicion_lab/tools/button_runner_study.py, personal_labs/crewrift_lab/suspicion_lab/tools/expand_corpus.py, personal_labs/crewrift_lab/suspicion_lab/README.md</sub>

#### 10. Gate unattended champion-refit on hard quality bars; treat fitted weights as non-stationary
`loop`

Gate an unattended nightly champion-refit loop on hard checks that abort and leave the current champion untouched on ANY failure: e.g. CV AUC >= 0.70, training corpus >= 500 games, the full agent test suite passing, and a local smoke test -- only after all pass should it vendor weights, build, upload, and submit (corpus-size and AUC bars must pass before fit output is accepted). Treat weights fit to a league field as non-stationary because the field evolves: date-stamp corpus segments, prefer recent games, and plan an explicit refit cadence. As a confidence signal, track directional stability of cues across corpus sizes -- if every cue keeps its sign from an interim small-sample fit to the full corpus (e.g. 341-game interim to 1,857-game full), that indicates real directions not small-sample artifacts.
  <sub>sources: personal_labs/crewrift_lab/suspicion_lab/README.md, personal_labs/crewrift_lab/crewborg/data/suspicion_weights.json, personal_labs/crewrift_lab/crewrift/crewborg/docs/designs/suspicion-le</sub>

#### 11. CvC score and metric field locations across the three stat buckets
`loop` · ⚠ _session-derived, unverified_

For a Cogs-vs-Clips player, the episode score lives at data['missions'][0]['mission_summary']['per_episode_per_policy_avg_rewards']['0'][0], and key decision metrics are split across three buckets that must ALL be parsed: avg_game_stats (e.g. cogs/aligned.junction.gained), avg_time_averaged_game_stats (e.g. cogs/aligned.junction.held, clips/aligned.junction.held), and per-policy avg_agent_metrics (heart.gained, miner.gained, aligner.gained, scout.gained, status.death, action.noop.success, action.move.failed, hp.amount, status.max_steps_without_motion, cell.unique_visited).
  <sub>sources: codex:019e1579-a737-7b70-bf0e-172ff04307cf</sub>

#### 12. Validate the metric-to-objective link, and attribute mean/median divergence to specific tail matches
`loop`

Do not optimize an intermediate metric before confirming it maps to the objective: counterintuitive correlations (e.g. dying more while scoring more) are signal not noise, and the 'safe' intuitive metric can be the losing one -- validate the link before treating the metric as a target. A change can have a correct mechanism yet regress the tournament mean while improving the median: cargo batching raised median +4.61 but dropped mean -1.39 by reintroducing tail risk (one 2.02-score match where both your agents mined and the team had only the partner's lone aligner), so when mean and median diverge attribute the gap to specific tail matches via replay inspection before judging. And a self-play A/B win may not generalize: 'concentrate mining on K=2 scarcest elements wins' was strongly self-play-supported but contributed only ~0.5 pts/match (below noise) once partner-induced tournament variance dominated -- tag self-play-only conclusions as dubious until tournament replay data confirms them.
  <sub>sources: player_labs/best_practices.md, archive/cogames_playground/alpha_cog/docs/paper/paper.md</sub>

#### 13. Record join-disambiguation assumptions and report full benchmark distributions with worst-case replay URLs
`loop`

When joining leaderboard rows to active memberships and a player has multiple, prefer substatus=='champion', otherwise the newest active membership by created_at -- and record this disambiguation assumption in the final report so the join logic is auditable. When summarizing a policy benchmark, compute the requester score per episode against the episode max, track ties for top score, and report completed/requested count, failed count, mean/median/min/max requester score, per-policy averages, and replay URLs for the worst outliers so bad cases can be inspected directly.
  <sub>sources: players_checkouts/players/players/crewrift/crewborg/docs/experience-re</sub>
