---
name: code-review
description: >-
    Owns the local review cycle over three engines — CodeRabbit, Greptile, and Macroscope
    (`.coderabbit.yaml`, `.greptile/`, `.macroscope/`). Use on any request to review, and
    whenever those config files are read, edited, or authored — this skill owns their schemas
    and rule grammar.
---

# [CODE_REVIEW]

One rail carries the whole cycle: every engine round normalizes into one finding schema, and each round distills its refuted classes and lessons into the reviewer configs so the next round runs harder.

## [01]-[ROUTING]

[REFERENCES]:
- [01]-[CODERABBIT](references/coderabbit.md): `.coderabbit.yaml` config, the `--agent` stream, and the rich finding store
- [02]-[GREPTILE](references/greptile.md): `.greptile/` cascade, the `--json` envelope and status oracle, and the MCP bridge
- [03]-[MACROSCOPE](references/macroscope.md): `.macroscope/` concern files, the stream grammar, and worktree custody

[TEMPLATES]: each template is self-contained for its own agent; a fact one of them carries is never restated here.
- [01]-[FIX](templates/fix.md): universal fixer template — conduct law, corpus fills, and both dispatch shards
- [02]-[CLOSE](templates/close.md): universal closer template — weight-sized arming, land-or-refute stance
- [03]-[HARVEST](templates/harvest.md): per-round reviewer-harvest dispatch — round-instance slots and both transports
- [04]-[REFUTED_CLASSES](templates/refuted-classes.yaml): refuted-class registry compiled into classifier, recurrence detector, and rulings roster

[SCRIPTS]:
- [01]-[REVIEW_RAIL](scripts/review_rail.py): verb rail printing one JSON receipt per verb

[AGENT]:
- `.claude/agents/reviewer-harvest.md`: owns the DISTILL leg

## [02]-[CYCLE]

Every session is its own campaign: rounds number from 1, the session's first launch deletes any pre-existing `.cache/review/` state whole — never archived, never resumed, never numbered from — and the campaign close deletes it again once the final round's `round` row prints its delta. Mid-campaign round dirs survive until then: normalize provenance, `--dedup-against`, and the harvest recurrence census read prior rounds.

Commits follow the user's request and the file scope it names; each round otherwise reviews the tree as it stands, every landing staying uncommitted.

Step order never proves a drain, the owning receipt does: `reconcile` surfaces `routing.pending`, `round` refuses `routing-undrained` while it is non-empty, and `harvest`/`round` refuse a partial shard-report set.

[STEP_1]-[LAUNCH]: `launch --reviewer <engine> --scope <scope> --follow --normalize` spawns one engine round at its canonical scope; the receipt proves the spawn, and the follow exits 0 only on `completed`, landing the findings receipt in the same verb. Bare `launch` prints `watch_cmd` instead: it self-exits at the terminal phase, its exit re-invokes the agent, and `findings --normalize --round N` lands the receipt.
- KNOB: engine choice and `--focus`.

[STEP_2]-[NORMALIZE]: `findings --normalize` per completed round; `gather --all-live|--reviewer <names>|--rounds <numbers>` unions completed normalized rounds into one pre-normalized round every later step targets — `--all-live` takes every engine round with no ledger row and no prior gather, pass `--rounds` when older rounds sit open. `findings --digest --round N` prints the round read — severity counts, class fires, folder cuts, top rows per severity — where engine rotation and shard count decide; query filters answer every targeted read, never hand-jq over `findings.json`.
- WATCH: provenance histogram before any count judgment — a flat total decomposes into `relitigation|refuted_remint|new_work|late_discovery`, and rising new-work beside falling relitigation is convergence.
- KNOB: `--dedup-against`.

[STEP_3]-[SLICE]: `slice --round N` cuts balanced per-shard manifests with stamped ids and a dispatch-ready `shard-<letter>-brief.md` each; `shards --fill` then emits each shard's corpus data for template fill; files, owning packages with `.api` overlays, substrate `.api`, doctrine roots, unplaced files.
- WATCH: severity and folder balance across shards.
- KNOB: explicit `--shards`, one per balanced folder slice up to the ceiling — small slices direct freed capacity into capability depth, never early finish.

[STEP_4]-[FIX]: one keeper per shard under `templates/fix.md`, dispatched concurrently from the briefs on either transport, codex mechanics the delegate-codex skill's, each writing `<round-dir>/shard-<letter>-report.json`.
- WATCH: `shards --spawns` proves each shard's miner passes; a lost report relaunches once, and a second failure is hand-repaired, since every downstream verb refuses a partial shard-report set.
- KNOB: template wording.
- Codex shards run the config-default model and effort unflagged under the full user config; miner spawns need the multi-agent depth row, so deviate only for purely mechanical slices. Each shard returns only its report path — the codex shard's `-o` capture, the claude shard's own final write.

[STEP_5]-[RECONCILE]: `reconcile --round N` exits 0 only when `bijective: true` proves every stamped id carries exactly one verdict; `missing`/`phantom` name the defecting shard, `files`/`strays` name cross-territory writes, and `routing` states the closer drain `{total, drained, verdicts, pending}`.
- WATCH: verdict-mix honesty — fixed-versus-upgraded inflation, citation-backed push-back share; `report_valid: false` beside a `fault` is a decode failure to repair first.

[STEP_6]-[CLOSERS]: shard-report `routing[]` rows alone arm this stage, so a finding `reconcile` reports dropped or phantom lands as a hand-added routing row before the cut. `slice --closers --round N` cuts the rows into file-disjoint territories (`close-<letter>.json` and brief); closers dispatch concurrently under `templates/close.md`, sized by row weight, each writing `<round-dir>/close-<letter>-report.json` answering by the brief's stamped keys, and `reconcile` re-runs to prove the drain empty.
- WATCH: honest land-versus-refute — a mined candidate that cannot ground is refuted with its citation, never forced.
- KNOB: closer sizing.

[STEP_7]-[DISTILL]: `harvest --round N` assembles the feed and memory proposals (`round --harvest` in one verb); dispatch under `templates/harvest.md`.
- WATCH: diff-sample touched blocks — density rose, integrations weave, additions earned; the `trimmed` self-report verifies against the diff.
- KNOB: agent-file wording, the single versioned tuning surface.

[STEP_8]-[VERIFY]: `registry --apply --rows <path>` lands only a clean set, append-only, refusing whole and naming each fault; `registry --check --rows <path>` diagnoses the refusal, bare `registry --check` lints the standing yaml and proves each row's `landed_surfaces` claim. `verify --round N` proves each surface-ledger guard in its surface's own oracle.
- WATCH: an ineffective row marks failed wording — harden the owner and re-verify before `round`, since the close is one-shot.
- KNOB: guard wording at its owning surface.

[STEP_9]-[CLOSE]: `round [--harvest] [--defer-routing] --round N` appends the `rounds.jsonl` row and prints the delta; it refuses `routing-undrained` while routing rows lack closer verdicts unless `--defer-routing` records the deferral.
- WATCH: findings trending down while capability rows rise is the goal line.
- Campaign close dispatches `/custodian` bare over the round's working diff for one-way touchpoint and ownership custody across the reviewer-config and doctrine surfaces; its receipt returns to the orchestrator and never feeds the harvest.

[STEP_10]-[NEXT]: grade the round on the [GRADING] axes, then pick the next engine — recurrence judges per engine, counts flattening under one engine rotate the next round to another, and `--focus` aims a round within one; greptile rides early rounds, before the accumulated diff meets its size caps.
- WATCH: plateau under a hardened config.
- KNOB: rotation and focus.

[FRAMING]: both framings ride every surface — negative framing kills false-positive classes through do-not-flag guards citing the refuting ruling, positive framing steers toward house demands through hunt axes and hit-shape rosters. Hit-shape rosters land on every surface regardless of what an engine emits, fixer miners execute them.

[GRADING]: REVIEW-THE-REVIEWER grades every round on the round row's typed fields, each naming its oracle, so a between-rounds template edit reads as prompt-change to behavior-change mechanically. CodeRabbit emits no missing-capability findings under any `path_instructions` wording; capability-direction rides Macroscope check-run agents and Greptile structured rules.
- Round axes and oracles: `fp_share`/`relitigation_share` (pre-prune provenance histogram), `novel_quality` (accepted-verdict share over novel-provenance rows), `hunt_axis_fire` (fixer-stamped improvement axes), `shape_fire` (fixer-stamped ledger `shape`; `ShardStat.shapes` counts each shard's unstamped gap), `wall_spread` (shard wall times; an outlier exceeds twice the median), `prompts` (content hashes of the dispatch templates and the `reviewer-harvest` agent).
- Finding strength stays a judgment sample, never a computed grade: `anchored` and `actionable` are rail-stamped bits, while discriminating (the claim states why the shape is wrong) and novelty read by operator judgment — a computed stand-in fabricates the grade.
- Fixer shards grade on five per-model axes in `grades` beside the raw `by_model` verdict rollup — `depth_of_fix` (`upgraded` over `fixed` + `upgraded`), `scope_clean` (phantom-free shards), `refute_cited` (evidence-carrying `refuted` rows), `gate_clean`, `bijective` — so the claude-versus-codex comparison is one jq group; upgraded claims surviving diff re-read stay the orchestrator's judgment axis.
- Prose FP classes live as `corpus: prose` registry rows citing the docgen defect catalog, graded by the same recurrence machinery.

## [03]-[VERBS]

Every round-scoped verb accepts `--round N` and `--dir`, printing one JSON receipt; a refusal exits nonzero carrying `{code, detail}`. `REVIEW_RAIL_BUNDLE` points a relocated copy of the script back at the bundle's `templates/` and registry.

```bash template
rail() { uv run "${CLAUDE_SKILL_DIR}/scripts/review_rail.py" "$@"; }   # shell state dies per tool call — re-define per shell, or use the literal path
rail launch --reviewer <engine> --scope <scope> [--focus <text-or-file>] [--follow [--json] [--normalize]]
rail status --follow --round <N> [--json] [--normalize]
rail findings --normalize --round <N> [--dedup-against <M>]
rail findings --digest --round <N>
rail findings --file '<glob>' --severity <floor> --claim '<regex>' [--in claim|fix|both] --round <N> [--json]
rail slice [--shards 3] [--recut] --round <N>
rail shards --fill --round <N>
# fixer shards dispatch here (orchestrator): each prompt cites its shard-<letter>-brief.md; each shard writes <round-dir>/shard-<letter>-report.json
rail reconcile --round <N>
rail shards --spawns [--shard <name>] --round <N>
rail slice --closers [--shards 2] [--recut] --round <N>
# closers dispatch here: each cites its close-<letter>-brief.md and writes <round-dir>/close-<letter>-report.json
rail reconcile --round <N>                 # re-run: proves the closer drain empty
rail harvest --round <N>
# dispatch the reviewer-harvest agent on the feed; persist its ledger as <round-dir>/surface-ledger.json
rail registry --apply --rows <path>
rail verify --round <N>
rail round [--harvest] [--defer-routing] --round <N>
```

```bash template
rail launch --reviewer coderabbit --scope uncommitted
rail launch --reviewer greptile --scope base:<prior-boundary>
rail launch --reviewer macroscope --scope base:<default-branch>
rail status --follow --all-live            # exits when every live round is terminal
rail findings --normalize --round <N>      # once per engine round
rail gather --all-live                     # union round: fingerprint collapse, corroborators, max severity
# slice / reconcile / closers / harvest / verify / round then target the gather round
```

`launch` refuses an unsupported engine-scope pair and a live same-engine round; the scope family is `all|committed|uncommitted|base:<ref>|base-commit:<sha>`, every `--reviewer` takes the `cr|gt|ms` aliases, and conflicting selectors refuse `bad-flag` on `status`/`kill`. `--focus` takes inline text or a file path — greptile rides `--instructions`, coderabbit a round-scoped `-c` instruction file, and macroscope refuses `--focus` before any preflight side effect.

[CODERABBIT]: sweeps working-tree quality and style at full breadth every run — a retry re-spends quota; canonical round `--scope uncommitted`, full scope family accepted. `launch` resolves and injects a base for every working-tree scope. One hard changed-file cap (300, counted pre-filter) refuses oversized scopes, so a tree past the cap reviews under another engine or after the user's own commit narrows it.

[GREPTILE]: hunts cross-file logic over the commits already on the branch against a base; canonical round `--scope base:<prior-boundary>`, `committed` reviews against the repo default, and `base:`/`base-commit:` refs take any committish.
- Scope is a base..HEAD range, so a cumulative campaign pins one base — `base-commit:<campaign-boundary>` held across rounds — and the whole accumulated delta reviews as one change regardless of commit count, with cross-round dedup and provenance keeping adjudicated rows out of shards.
- Client-side size caps refuse a range past them, and a tree carrying no commits past the base returns a clean empty round.

[MACROSCOPE]: streams AST-level correctness in place — fixes land in the files the review read; canonical round `--scope base:<default-branch>` spanning committed branch work and uncommitted edits, `uncommitted` for tree-only — an in-place run without a base on a branch reviews almost nothing.

Terminal phases are `completed|failed|refused|stalled|timed-out|killed`; a receipt short of `completed` names its fault `signature`, `remedy`, and engine `exit_code`, and `status --follow --all-live` exits 0 only when every followed round completed. `--json` on any follow streams one `StatusReceipt` JSON line per phase change or minute pulse for a piping orchestrator; the terminal receipt prints either way.

Bare `status` resolves the single live round, else the highest-numbered on disk; several live rounds refuse `ambiguous` naming them — pass `--round`, `--reviewer`, or `--all-live`. `kill` (same selectors, same `no-round`/`ambiguous` selection refusals) escalates SIGTERM to SIGKILL over the process group, sweeps detached engine survivors and macroscope worktrees, and reaps a stalled or timed-out round whose engine still breathes; per round it refuses a gather round (`no-process`) and a round whose process group is gone (`already-closed`).

`findings --normalize` gates on `completed` and refuses an already-sliced round. Minting strips each engine's constant fix-preamble (one `ENGINE_PREAMBLES` row per preamble) and carries content fields only; the receipt `source` names the store a raw payload re-reads from.

`scope_misfire` on the receipt flags zero rows over a dirty scope; an exit-0 zero-comment envelope over a clean scope is ordinary success. Normalize refuses `dedup-collapse` when over half of eight or more admitted rows drop as intra-round fingerprint duplicates — engine format drift, never real duplication.

Bare `findings` reprints the admission summary. `--top N` bounds the digest's per-severity rows, and the query filters compose with `--digest` — both print human-scan text, `--json` the typed form. `--in` scopes the `--claim` regex, defaults to `both`, and refuses without `--claim`. `gather` takes exactly one selector, and every source must be `completed` and normalized.

`slice [--shards N] --balance count|loc` partitions by folder affinity — grouping deepens past common prefixes and splits oversized folders at sub-folder seams until shards balance, so N shards over at least N findings always cut N non-degenerate shards. It clears stale shard artifacts only after the cut proves out, and each manifest carries the corpus-matched settled-rulings roster; a registry row tagged `corpus` slices only into shards whose file set resolves to that corpus.

`slice --closers` instead keys one row per routed demand as `<shard-letter>:<target_file>`, groups by target file, and greedy-packs whole files into territories; an omitted `--shards` derives the count, clamped to the distinct-file ceiling, and the cut never rewrites `findings.json`.

`reconcile` covers all shards bare. `shards` takes exactly one of `--fill` or `--spawns` with an optional `--shard <name>` filter (a bare letter reads as `shard-<letter>`); its spawn oracle is the codex rollout store — the per-shard events stream records zero spawns by design and is never consulted — and a `fault` of `no-events|no-session|no-rollout` is a per-shard fact, not a refusal.

`round` refuses a duplicate close and fails loud on findings without shard reports. `verify` takes exactly one of `--rule <text> [--path <file>]` (greptile cascade check) or `--round N` (all-surface ledger check). `selftest` proves the rail's pure contracts beside the harvest law's two spellings, exiting nonzero naming each failed proof and the law line a one-sided edit diverged.

## [04]-[SHARD_CONTRACT]

Per shard the rail writes `shard-<letter>.json` and `shard-<letter>-brief.md`; dispatch writes `task-<letter>.md`, `shard-<letter>-report.json`, `shard-<letter>-events.jsonl`, and `shard-<letter>-stderr.log`. Each report is the machine intake `reconcile`, `harvest`, and the reviewer-harvest agent parse, written as the shard's final act:

```json signature
{
  "ledger": [{"id": "", "file": "", "severity": "", "verdict": "fixed|upgraded|pushed-back|already_resolved", "note": "", "shape": "substitution|collapse|completion"}],
  "improvements": [{"page": "", "pattern": "", "what": "", "axis": ""}],
  "refuted": [{"claim": "", "evidence": ""}],
  "capability": [],
  "routing": [{"target_file": "", "needed_change": ""}],
  "uncertain": [],
  "files": [],
  "gate_clean": true,
  "model": "",
  "wall_s": 0.0
}
```

`axis` and `shape` are fixer-stamped, never inferred; a blank `shape` counts under `unstamped` in `ShardStat.shapes`. `files` is the shard's touched roster, not its assigned set.

Each `capability` row carrying a `members`, `roster`, or `symbols` list feeds the `reference_*` memory proposals; `uncertain` alone carries no mined structure, its rows reprinted verbatim by the feed. `model` keys the grade cohorts casefolded at reconcile.

Per territory the rail writes `close-<letter>.json` and `close-<letter>-brief.md`; each closer writes `close-<letter>-report.json`:

```json signature
{"rows": [{"id": "<shard-letter>:<target_file>", "verdict": "landed|refuted|already-landed|blocked", "note": ""}], "files": []}
```

`id` echoes the brief's stamped key, and a bare target path in `id` or `file` joins as fallback; the drain counts a row answered under any verdict.

## [05]-[DISTILL]

Round dirs sit outside reviewer-harvest's write territory, so project its returned surface ledger into `<round-dir>/surface-ledger.json` yourself as `[{surface, text, path}]` rows — `surface` an engine name or alias, `text` the shortest guard substring unique on the surface, `path` blank falling to the engine's own oracle.

Project one row per landed addition and consolidation — `corpus` rows never project, a ruling, index repair, or card proving itself on disk with no engine oracle; a receipt whose `source` is `surface-ledger` marks a malformed row (blank text or an unmapped surface name), never failed wording.

- [REGISTRY]: `harvest` proposes new rows in the feed, `registry --check --rows` proves them (matcher compile, schema, dedup, each named surface resolving to its engine oracle on disk), and a judgment-bearing merge into an existing row is a hand edit re-proved by bare `registry --check`, which refuses `unmirrored` until every engine carries the class — a proposal's roster fills as its guards land.
- [RAIL_GAPS]: rail gaps a round exposes harden the script.
- [VERIFY]: `verify --round` re-proves each landed guard — a `.coderabbit.yaml` `path_instructions` clause by text, a greptile rule by substring over the resolved `greptile config` output (never by id — org rules re-key to server UUIDs) falling back to full-text over `.greptile/config.json` and `.greptile/rules.md` when the cascade truncates or a scoped rule never resolves at the probe path, the receipt `source` naming the oracle that matched, a macroscope topic file by presence and content, a blank path scanning `.macroscope/**/*.md` whole.
- [FEED_OUTPUTS]: provenance and corroboration histograms feed review-the-reviewer — a class one engine raises and rounds keep refuting marks that engine's false-positive tendency, and multi-engine corroboration marks high-confidence work.
- [PROPOSALS]: `memory-proposals/` under the round dir carries candidate memory files the orchestrator curates, never the live memory dir — the campaign memory (`project_cr_review_cycle_machine`) is the destination owner, taking verdicts and class calibrations as merged rulings, never narration, and a proposal duplicating a repo-owned fact dies at curation.
