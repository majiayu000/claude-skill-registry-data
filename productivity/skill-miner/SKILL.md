---
name: skill-miner
description: Mine agent session logs (Claude Code, Codex, OpenCode) for user corrections, recurring failures, user frustration, token-heavy sessions, and repeated manual workflows, then find and score skills that could fix them. Use when asked "what skills am I missing", "mine my session logs", "where do my agents keep failing", "find a skill for X", "which sessions burned the most tokens", or to discover existing skills from skills.sh / Floom / local pools before writing anything new. Pairs with skill-eval-loop, which proves candidates before adoption.
---

# skill-miner

Two jobs: (1) find where the agent actually suffers in real session logs,
(2) find the best existing or drafted skill for each pain point. Never adopt
anything here - that is skill-eval-loop's job, with proof.

## Mine corrections first (where skills win)

```bash
python3 scripts/corrections.py --memory ~/.claude/projects/<proj>/memory --out corrections.json
```

Correction episodes are the moments the user told the agent it got something wrong:
(agent message, user reply). An LLM groups them into themes, marks each one
`knowledge_gap` (fixing it needs THIS user's rules, voice, formats or facts) vs generic,
and maps it to the user's saved rule files (`--memory`). Knowledge-gap themes sort first.
They are what a skill can measurably fix: frontier models already avoid generic mistakes,
so generic-failure evals tie, while a skill carrying the user's rules wins.

- Sources: Claude Code, Codex and OpenCode logs (`--sources claude,opencode,codex`, default:
  all found). `--per-session` caps marathon sessions so one session cannot fill the budget.
- `--no-llm` extracts episodes only (free, used by the nightly timer); `--episodes FILE`
  clusters a saved extraction later.
- The `session_index` also records **which skills each session loaded**, collected in the
  same pass that reads the episodes. skill-eval-loop's recheck needs it to tell a skill
  that earned its improvement from one that was never once loaded while the rate moved
  anyway. Tool and argument spellings differ per source and were read off real sessions,
  not assumed: Claude Code calls the tool `Skill` with the name in `skill`, OpenCode calls
  it `skill` with the name in `name`, and Codex records no skill call at all.
- The `session_index` lists **every** scanned session, not just the ones with episodes,
  and records how many turns the human typed in each. The recheck divides by that index,
  and an episode needs a previous user turn and a previous assistant turn, so a session
  under two typed turns belongs in neither half of the fraction: on real logs those are
  two thirds of all sessions, they carry no episodes, and their share of a window swings
  wildly week to week. Without the count there is no way to drop them, and the rate ends
  up measuring the shape of the work.

## Mine tool errors, anger and spend

```bash
python3 scripts/mine.py --sources claude,opencode,codex --sessions 100 --out failures.json
# root's history on a server: sudo python3 scripts/mine.py --projects /root/.claude/projects ...
```

Output `failures.json`:
- **clusters** - recurring tool errors and user corrections, classified
  `infra` (broken environment: hooks, permissions, rate limits) vs `task`
  (agent behavior a skill could change). Only patterns seen in >=2 sessions.
- **anger** - user messages with frustration markers (wtf, "why is", "!!!",
  German equivalents). Highest-signal source of workflow skills.
- **top_spend_sessions** - sessions ranked by output tokens + error counts.
- **repeated_workflow** clusters - near-identical opening prompts across
  sessions. A workflow done by hand N times is a skill waiting to be written.

Eval-harness sessions and system banners are filtered out automatically.

## Find + score candidates

```bash
python3 scripts/match.py failures.json --index 0 --out candidates.json
python3 scripts/score.py candidates.json failures.json --index 0
```

- `match.py` searches local installs, the getedgehq skills repo, the Floom
  registry, and skills.sh (`npx skills find`, install counts included).
- `score.py` enriches each candidate with its actual SKILL.md (fetched for
  registry hits), the failure evidence, and ledger history, then LLM-scores
  P(measurable improvement) 0-1. Only candidates >=0.5 deserve eval spend.
- A candidate printed with `?` instead of a number scored nothing: the reply could
  not be read as JSON. The reply itself is kept at
  `$FORGE_ROOT/mined/score-failures/<name>.txt` and the line says so. Read that file
  before changing the parser. A decoder's complaint names a column in a reply nobody
  kept, and a parser fixed from the complaint alone is fixed for a guess.
- Nothing matches? `draft.py <clusters.json> --index 0` drafts a minimal candidate
  skill into `$FORGE_ROOT/drafts/`. For correction themes it automatically feeds the
  mapped memory files and the user's verbatim rules as enriched context; add more with
  `--context FILE` (accepted examples, past eval losses). Generic best practice never
  beats a frontier model, so a draft that quotes no user rule is a weak candidate.

## Check the scorer against what the evals decided

```bash
python3 scripts/calibrate.py            # adoption rates per bucket, or "too few to call"
python3 scripts/calibrate.py --check    # did high scores actually predict adoption?
```

`calibrate.py` reads the ledger and reports the adoption rate per bucket - failure
kind, skill provenance, retries of a skill that already lost - and any bucket under
four decided evals comes out as "too few to call" rather than as a rate. A 1-of-1
bucket is noise, and a prior stated with false confidence is worse than no prior.

Both ends of that are now wired up, so the prediction is checkable instead of
decorative:

- **The priors reach the prompt.** `score.py` pastes `calibrate.py`'s measured block
  into its own scoring prompt, so the scorer reasons from this user's base rates
  instead of a general impression of what a good skill looks like. Under eight decided
  evals in total it states that there are too few and scores from the evidence alone.
- **Every prediction is written down.** Each scored candidate appends a row to
  `predictions.jsonl`, which is what `--check` joins to the decisions. A failed model
  call records nothing: a failure is not a prediction of 0, it is no prediction.
- **And an unreadable reply is a failed call, not a zero.** Reading the verdict by
  slicing from the first `{` to the last `}` breaks on a model that answers with the
  object and then keeps going: the slice is valid JSON followed by more, `json.loads`
  rejects all of it, and two real candidates scored 0.00 in a live pass for a judgement
  the model never made. The reply is now parsed to the end of the first complete object,
  and a candidate that still cannot be read is carried as unscored and sorts last,
  rather than being quietly retired at the 0.5 threshold.
- **`--check` reports coverage, not just the gap.** A report that pairs one prediction
  reads the same whether the ledger is young or the scorer is broken, and on this one it
  read that way for weeks: 1 of 19 decided evals had a prediction, and the missing 18 were
  a crash, not a wait. `--check` now prints the fraction and names the decisions with no
  prediction, so the next systematic gap shows up as a number in the same pass that reads
  the gap rather than six weeks later.
- **A brief nobody mined still gets a prediction.** `--skill-dir` reads the cluster out of
  the brief's `source_failure`, which only `draft.py` writes. A brief written by hand has
  no such key, the fallback handed the brief itself back as a cluster, and the next line
  raised `KeyError: 'signature'`. `forge.sh` prints that as "scoring failed, evaluating
  anyway", which reads like one unlucky model call - but 22 of the 37 briefs here have no
  `source_failure`, so the prediction log added to close the prediction-to-decision gap was
  never going to see the majority of decisions, the first run against a real incumbent
  among them. Such a brief now scores against its own task, and the prompt says the missing
  cluster is no evidence either way rather than letting rubric item 3 read an absent
  history as a weak one.
- **Provenance is a class, not a path.** The ledger stores `skill_src` as a filesystem
  path, so bucketing it raw produced one n=1 bucket per draft - a dimension that could
  never say anything. Paths now class into drafted by the loop / already installed
  locally / found in a registry.
- **The prediction is about the skill that gets evaluated.** Writing predictions down
  is worth nothing if they are about other skills. `score.py` only ever saw the
  candidates `match.py` found, and a matched candidate is used only when it scores at
  least 0.5, so the skill that reached the gate was nearly always a draft nobody had
  scored: 8 predictions, 21 decisions, and no pair between them however many evals ran.
  That is not a wiring bug to wait out, it is a design that could not close. `score.py
  <brief> --skill-dir <dir>` scores exactly the skill about to be run, under the
  basename the ledger records it by, from the cluster the brief already carries in
  `source_failure`. `forge.sh` calls it once per eval, so every decision from here on
  has one prediction to pair with. The prediction is recorded, not acted on: skipping
  an eval on a low score needs `--check` to first say these numbers separate winners
  from losers, which is the question this makes askable.

On the live ledger that turns sixteen unusable buckets into one real number: skills
the loop drafted itself pass the gate 9 of 16 (56%), corrections 7 of 10 (70%),
unlabelled failures 3 of 5 (60%); retries, tool errors and registry finds all still
report as too few to call. `tests/test_calibrate.py` covers both halves on fixtures -
stdlib only, no model calls - including that a thin ledger states no priors at all and
that an unwritable prediction log never stops a scoring pass.

## Rules

- Infra-class clusters go to **agent-infra-fixer** (fix the hook/permission/wrapper,
  verify, record in ledger). No skill fixes a broken environment.
- Drafted skills must name task-context triggers in their description -
  "prevents X error" never gets loaded, the agent can't know it will err.
- A candidate is a hypothesis, not an adoption. Hand off to skill-eval-loop.

State lives in `$FORGE_ROOT` (default `~/skill-forge`): mined/, drafts/, ledger.jsonl.
