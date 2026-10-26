---
name: interpret-e2e-result
model: claude-sonnet-4-6
description: Reads an e2e benchmark run log and explains what happened — which expected findings the agent recovered and which it missed (read from its final tree, not the judge's grade), what proof conclusion it wrote, why it stopped, and the most likely cause (agent reasoning regression, /research routing regression, sub-skill regression, FamilySearch data drift, or single-run jitter). Points the user at the exact tool call and narration turn to read next. Use when the user says "what happened in this e2e run", "interpret this e2e result", "why did this fixture fail", or "read the latest e2e runlog". Do NOT use to author or modify a fixture (use author-e2e-fixture), to interpret a unit-test scratch run (those are developer-facing — read the run log directly), to grade a single research question in a live project (use the relevant analysis skills like timeline or conflict-resolution), or to grade this run into its calibration annotation (use grade-e2e-run — this skill only explains the result and never writes the .ann.json).
---

# Interpret E2E Result

**Narration:** Read `researcher_profile.narration_guidance` from `research.json` if one exists in the working folder; otherwise default to concise narration.

Reads the files an e2e run produces and tells the user what happened in
plain language, with pointers to the exact turn to read.

Each run writes three files to `eval/runlogs/e2e/<test-id>/`:

| File | Content |
|------|---------|
| `run-<ts>.json` | Structured result. **Read only the harness facts from it — `stop_reason`, `tool_calls[]`, `narration[]`, `usage`, `blocked_tree_reads[]`, `blocked_context_calls[]`, `error`, `compliance`, `guardrail_bypass_violations[]`. Do NOT read `judge_output`, `verdict`, or `outcome` (see "Stay blind to the judge").** |
| `run-<ts>.final-tree.gedcomx.json` | The agent's final tree — the ground truth for what it recovered |
| `run-<ts>.final-research.json` | The agent's final `research.json`, including the proof conclusion it wrote |

- When `narration[]` is absent (runs before 2026-08-03), read the
  `run-<ts>.transcript.md` sibling if present, otherwise `tool_calls[]` alone.

This skill reads files; it does not call any MCP tools.

## Stay blind to the judge

**Do not read or report the judge's grade for the run you are interpreting.**
That means all of:

- `judge_output` — the `per_finding` labels, `rationale`, and `proof_quality`
  score;
- the top-level **`verdict`** — this is the judge's genealogical conclusion
  verbatim;
- the top-level **`outcome`** — the gate, which since the §8 detectors were
  demoted simply IS `verdict`, so reporting it leaks the verdict always rather
  than only when `compliance` is `pass`.

Those are the judge's *grades*: the thing the maintainer calibrates, and
unnecessary for explaining what the agent did. The human grade comes first
(`/grade-e2e-run`, blind) and must stay independent of the judge. Your report
says which expected findings the tree recovered, which is what the grader
labels, so it comes after the grade. If you also surface the judge's labels, a
later re-grade is anchored and the calibration number is corrupted.

**`compliance` and `guardrail_bypass_violations` are NOT judge output** — read
and report them freely (Step 2d). They are a deterministic harness check on
whether the GPS guardrail skills ran, computed from the tool-call log and the
final project files, and the grader does not score them.

**This prohibition covers the run under interpretation, not the corpus.** When
Step 5 asks you to compare against a previously-passing run, identify that
prior run from its committed `.ann.json` — a human's grade, which cannot leak
the current run's judge output. Do not open a prior run's `run-<ts>.json`
`verdict` to find one.

You have everything the user needs without the judge:

- **What the agent recovered / missed** — compare the final tree to
  `expected-findings.json` yourself. The tree is ground truth; report presence
  or absence as *facts*, not as a verdict.
- **The proof conclusion** — read what the agent *wrote* in `final-research.json`
  (`proof_summaries`). That's the agent's own claim, not a grade.
- **Why it stopped, what it did** — `stop_reason`, `tool_calls`,
  `blocked_tree_reads`, `blocked_context_calls`, `usage` are harness facts, not
  judge output.

## What to do

**Ground every claim in the run-log files — do not invent specifics.** You are
reporting what happened, not reconstructing a plausible story. `stop_reason`,
tool counts, and cost come from `run-<ts>.json` (harness fields only). What the
agent found / missed comes from the final tree vs `expected-findings.json`.
Anything more specific — *which* collections were searched, *which* records were
found, *which* index confirmed a date — must come from
`tool_calls[].args`/`response_summary`, `narration[]`, or `final-research.json`
(the agent's proof summaries and log entries name the actual sources, with ARKs
— quote/cite those). If a specific source name isn't in any of those files,
don't assert it; a plausible-sounding collection name you didn't actually read
is a fabrication.

### Step 1 — Locate the run log

If the user pointed at a specific `run-<ts>.json`, or a `scratch_<ts>.json` (the
harness's name for a run the judge skipped), use it. Otherwise ask which fixture
and which timestamp, or take the most recent if only one is present.

**Grade first.** When the run owes a grade, tell the user to run `/grade-e2e-run`
first and stop. Do not produce the per-finding report. A run owes a grade when all
of these hold: it is under `eval/runlogs/e2e/` (a quarantine directory is not the
corpus); it is a `run-<ts>.json`, not a `scratch_` file; its
`run-<ts>.final-tree.gedcomx.json` sibling is on disk; its top-level `stop_reason`
(not `usage.stop_reason`) is not `host_slept`; and no `run-<ts>.ann.json` is on
disk. These are the exemptions `check_added_runlogs_graded` applies in
`eval/harness/scripts/check_e2e_fixtures.py`, read from the files on disk rather
than from a commit, so a run that is not committed yet still owes its grade.
Otherwise interpret as below, and also when the user says they will not grade
this run or is mining a unit test from it.

**A slept run.** When the top-level `stop_reason` is `host_slept`, go straight to
Step 3's `host_slept` entry. It is the whole interpretation, so skip every other
step.

The fixture's `expected-findings.json` lives in `eval/tests/e2e/<id>/`.
Read it alongside the run so you can compare expected vs found yourself.

### Step 2 — Summarize what the agent recovered

Compare the final tree to each `required: true` finding in
`expected-findings.json` and state, as facts, which the tree contains and which
it doesn't. This is recall — *did the tree end up with the stripped facts?* Do
not quote a judge verdict; describe what you see:

- **All required findings present** — the run recovered the answer. Say so in a
  sentence, then describe the proof conclusion (Step 2b): a recovered answer
  with a thin or missing proof is worth flagging.
- **Some present** — name which it recovered and which it missed; the misses
  are what to investigate (Step 4).
- **None present** — the run recovered nothing. The agent stalled or went
  sideways; `stop_reason` usually explains.
- **No tree at all** (`run-<ts>.final-tree.gedcomx.json` missing) — the agent
  crashed before producing tree state. Read the last `narration` entries and
  `error` for the crash.

For a fixture with **negative findings** (`polarity: "avoid"` in
`expected-findings.json`), the correct outcome is the tree **not** asserting the
wrong candidate — absent, or present only as a rejected hypothesis. If the tree
asserts it, the agent over-claimed; call that out specifically — it's the
failure that matters most.

### Step 2b — Describe the agent's proof conclusion

Read the agent's `proof_summaries` from `final-research.json` and summarize the
conclusion it *wrote* — the claim, the evidence it cites, and the
confidence/tier it asserted. Report observable characteristics as facts (e.g.
"rests on a single 1910 census entry," "notes an unresolved date conflict,"
"claims a `proof_argument` tier"). **Do not score its soundness** (1 / 2 / 3) —
that is what `/grade-e2e-run` scores. If no proof summary was written, say so;
it's not itself a failure, just nothing to describe.

### Step 2c — Note any blocked tree-reads or context-writes

Check `blocked_tree_reads` in `run-<ts>.json`. The harness blocks
`person_read` / `person_search` / `person_ancestors` during a run so the
agent can't read the stripped answer off the live tree (it must research
from records). Each entry is a denied attempt.

- **Empty** — the agent didn't try to shortcut. Normal; say nothing.
- **Non-empty** — the agent *tried* to read the tree but was blocked, so the
  answer, if recovered, was still earned from records. But flag it: a healthy
  `/research` flow shouldn't reach for `person_read` on the subject during an
  autonomous run. Repeated attempts may indicate the skill is leaning on
  tree-reading instead of records, which is worth a look at the `/research` primer.

Then check `blocked_context_calls` — the twin denied by a different guard. Every
entry carries `blocked_by: "context"`, but **two different guards land here and
`blocked_by` cannot tell them apart. Read the entry's `tool`:**

- **`research_append`** — an owned-section write: a caller wrote a section it does
  not own. This is the arm that actually fires; every entry in the committed
  corpus is one. **Not** evidence of a spawn failure, and the shipped plugin hook
  holds the same rule, so a user would hit it too. Do not assume the main thread:
  `owner_denied` has four rules — `routed`, `out_of_lane`, `declaration` and
  `owned_field` (a field routed on presence, `project.status`) — and
  `out_of_lane` fires for a **named subagent** reaching outside its own lanes.
  `tool` is `research_append` for all four, so it cannot tell them apart — read
  `narration[]` for the rule and `tool_calls[]` for the caller.
- **`image_read`** — the one subagent-only tool, called on the main thread. No
  agent owns it, so this is the router reaching for a scan inline instead of
  calling `image_transcribe`, not a spawn failure. Not observed in the committed
  corpus. Older runs may also show `extraction_append` here, from before it left
  the subagent-only set.

Same shape as above (`{tool, args, blocked_by}`), and the denied attempt also
shows up in `narration[]` with `kind: "blocked"`.

- **Empty** — normal; say nothing.
- **Non-empty** — a call was denied and that work was not done. Flag it, and say
  which arm: an owned-section `research_append` is an ownership slip, not a spawn
  failure, so name the caller from `tool_calls[]` rather than assuming the main
  thread. A blocked `image_read` is the router reaching for a scan instead of
  calling `image_transcribe`; no agent owns it, so it is not a spawn failure. In
  an older run a blocked `extraction_append` did point at a `record-extractor`
  spawn failure. Read the matching `narration[]` turn: it shows what the router
  was trying to do, and for an owned-section write it names which rule fired.

### Step 2d — Note any GPS guardrail bypasses

Check `compliance` and `guardrail_bypass_violations[]` in `run-<ts>.json`.
This is a harness check, not a judge grade: it asks whether the agent actually
invoked the GPS guardrail skills whose effects appear in the final project
state — `person-evidence`, `conflict-resolution`, `proof-conclusion` and
`research-exhaustiveness`. `gps-mentor` is not among them: it runs only when the
user asks for a second opinion, so a run with no critique is not a violation.

- **`compliance: "pass"`** — nothing to say.
- **`compliance: "fail"`** — report each violation string as a fact. This is
  worth calling out even when the tree recovered everything: the agent reached
  the right answer by a route that skipped the doctrine, so the *result* is
  fine and the *process* is not. Say both plainly; they are separate findings
  and this skill is the only place the user will see the second one.
- **`compliance` absent** (a run log written before this axis existed) — say
  nothing; it was never checked.
- **`harness_schema_version` 6 or below** — a "was never successfully invoked"
  violation for an agent the run spawned typed and without error (an
  `Agent`/`Task` call whose `subagent_type` is that name and whose `is_error` is
  not `true`) is the retired Skill-only rule, not a bypass: today's detector
  credits that spawn. Check `tool_calls` for the spawn and say so instead of
  reporting it as a skipped step. An untyped or errored spawn is still a bypass.

Do not translate a compliance failure into a pass/fail judgement of the run
overall — that is the `outcome` gate, which is judge-derived and off-limits.

### Step 2e — Note whether the answer came from provided documents

If the fixture has a `provided-documents/` folder (bundled external
captures — Ancestry PDFs, Find A Grave pages the FS tools can't reach),
check `tool_calls` for `Read` of those filenames. **How
the answer was obtained is part of the result**, so say it plainly:

- **A finding came from a provided PDF** — note it (e.g. "the burial
  came from the bundled Find A Grave capture, not a live FS record").
  That's the intended path for external-only evidence, not a problem —
  but a reviewer should know which findings rested on bundled docs vs.
  live research, because only the live-research part reflects agent
  capability against FamilySearch.
- **A provided doc the run needed was never read** — flag it: the agent
  may have missed the bundled evidence, which can explain a miss the
  tool calls otherwise make look like a search failure.

If the fixture has no `provided-documents/`, skip this step.

### Step 3 — Explain the stop_reason

Translate `stop_reason` into something a researcher can act on:

- `completed` — agent set `project.status == "completed"`. Happy path,
  proof-conclusion fired. Look at the final tree to judge quality.
- `natural_end` — SDK ended the conversation but the agent didn't
  declare done. Either the agent thought it was done without setting
  the flag (skill regression), or the conversation drifted to silence.
  Check the last few `narration` entries.
- `inactivity` — agent went silent for the inactivity cap window
  (default ~10 min). It's stuck. `tool_calls_before` counts the calls that
  preceded an entry, so for the last call — index `len(tool_calls) - 1` — the
  narration that followed it carries `tool_calls_before == len(tool_calls)`.
  That entry is usually where the issue shows.
- `timeout` — wall-clock cap fired (default 120 min; a fixture's `caps` can
  override). Either the question is too big for the cap or the agent looped.
  Skim the tail of `tool_calls` for repeating patterns.
- `tool_cap` — agent hit the per-run tool-call cap (default 300).
  Almost always means looping. Read the last 20 tool calls; the loop
  shape is usually obvious.
- `cost_cap` — spent past the cost threshold. **Not an interruption** — it
  is a post-hoc label (the cost-cap row of the stop-reason table in
  `docs/specs/e2e-test-spec.md`), so read `usage.stop_reason` to see how the
  run actually ended before calling it unfinished.
- `max_turns` — SDK turn limit fired. Rare; usually means a
  conversational loop rather than a tool loop.
- `error` — SDK or harness exception. Read `result.error` for the
  message and the last `narration` entries for the surrounding context.
- `host_slept` — **an environment failure, not a research result.** The
  harness counted at least the inactivity cap's worth of host sleep
  (`usage.counted_sleep_seconds`), labeled the run `host_slept` and skipped
  the judge. The run is left out of outcome rates and owes no grade. Tell the
  researcher to commit its three files with no `.ann.json`, keep the machine
  awake (`eval/README.md`, "Keep the machine awake during a run") and re-run.
  The whole interpretation is this paragraph: do not report what the run
  recovered, and do not read its misses as agent failures.
- `mcp_unavailable` — **an environment failure, not a research result.**
  The genealogy MCP tools were absent from the session, so the agent had
  no way to search anything. Tell the researcher to **re-run the test —
  not to re-research the case**, and to run `make e2e-preflight` for the
  server's own error text.
  **You will not be handed a run log for this**: such a run writes no
  files at all (e2e-test-spec.md §6, the retention rule under the
  `stop_reason` table), so it reaches a genealogist as terminal output.
  If you are asked to interpret one, the whole interpretation is the
  paragraph above — do not go looking for missing findings, and do not
  read the starting tree as the agent's output.

### Step 4 — Compare expected vs found (when the tree is missing some findings)

For each entry in the fixture's `expected-findings.json`, look at the
agent's `run-<ts>.final-tree.gedcomx.json` and decide:

- **Found** — the agent's tree contains the expected person / relationship /
  fact, possibly with different wording or a different source path.
- **Missed** — the agent didn't surface the finding at all. Worth
  asking why: did it search the right collections? Did it find the
  right candidate and then dismiss it? Did it never reach the right
  step?
- **Recorded off-shape** — the agent found the right answer but put it
  somewhere the finding's shape doesn't expect (e.g. on a stub person
  rather than the principal). Diagnosis: finding shape, not agent capability.

For each `missed` finding, search `narration[].text` and
`tool_calls[].args`/`response_summary` for the relevant person name or
place. The agent often *touched* the right evidence but didn't conclude
from it; that turn is the diagnostic moment.

### Step 5 — Identify the most likely cause

First decide which situation you're in, because the causes differ:

**First run of this fixture (no prior passing run to compare against).**
"Regression / drift / jitter" don't apply — there's no baseline. The
useful questions are about *this* run:

- **It never researched** — the agent stopped after setup (e.g. wrote a
  question, then `stop_reason: natural_end` with no `record_search` /
  `fulltext_search` in `tool_calls`). The GPS loop didn't advance.
  Pointer: tool counts (no FS search tools) + the last `narration` entry.
- **It ran out of budget** — `stop_reason` is `max_turns` / `timeout` /
  `tool_cap`. It researched but didn't finish. Pointer: high
  turn/tool counts; check whether `proof-conclusion` was ever reached.
  (`cost_cap` is deliberately not in this list — it is applied after the
  run has already ended, so it never cut a run short.)
- **The evidence wasn't recoverable** — it searched genuinely but the
  finding isn't findable from records (and isn't a `provided-documents/`
  case). The fixture may be unsolvable as authored — a fixture problem,
  not an agent one.
- **Recorded off-shape** — see Step 4 (finding-shape issue).

**A previously-passing fixture now failing (you have a prior run to diff).**
These are the regression causes:

- **Agent reasoning regression** — the agent took different decisions
  on the same evidence than a prior passing run. Pointer: diff
  `tool_calls[]` against the last passing run for the same fixture.
- **`/research` skill regression** — the agent skipped a GPS step or
  picked the wrong sub-skill. Read the ordered sub-skills the agent ran
  from `run-<ts>.json`'s `tool_calls` — the `Skill` entries' `args.skill`
  **and** the typed `Agent`/`Task` entries' `args.subagent_type` (strip a
  `genealogy-research:` prefix), in order:
  `[tc['args'].get('skill') if tc['tool']=='Skill' else (tc['args'].get('subagent_type') or 'UNTYPED').split(':')[-1] for tc in tool_calls if tc['tool'] in ('Skill','Agent','Task')]`.
  The orchestrator spawns every destination its routing table spells
  `@plugin:<name>` directly as an agent, so a `Skill`-only list misses them. If `proof-conclusion` never appears on either route, that's the
  smoking gun; an `UNTYPED` spawn standing where it should be is a bypass; if
  `question-selection` is missing where a gap needed one, that's another.
- **Sub-skill regression** — the right sub-skill ran but produced
  worse output than before. Pointer: the relevant `tool_calls` block
  compared to the prior run.
- **FamilySearch data drift** — same tool calls, different results.
  FS may have reindexed or a contributor may have edited the live
  tree. Pointer: `tool_calls[].response_summary` differs from the prior
  run. The agent isn't at fault. First compare `harness_schema_version`
  on both runs. Across the `1` → `2` boundary the capture format
  changed, not the data — roughly half of all captures differ there, so
  do not read a `response_summary` diff across it. The `4` → `5`
  boundary likewise moves `response_summary`, but only for
  `image_transcribe`: `5` preserves the full `transcription` where `4`
  truncated it at 500 chars, so a transcribe-call diff across it is the
  capture change, not FS drift. The `7` → `8` boundary does the same for
  `Agent`/`Task` calls: `8` keeps the subagent's full return where `7` cut it
  at 500 chars. The later
  `tool_calls[].is_error` boundary does **not** affect
  `response_summary`, so a drift comparison still holds across it; what
  it does move is `compliance` — no longer `outcome` — and the guardrail violation
  counts, which get stricter once the key is present (an errored call no
  longer counts as a successful invocation). That boundary is the commit
  main `4541a4c5`, not cleanly a version — a `3` log has the key, a `2`
  log has it only if written after that commit.
- **Single-run jitter** — Anthropic models are non-deterministic and
  this harness can't pin `temperature=0`. A single finding flipping
  recovered / not-recovered may just be variance. Recommend a re-run
  before drawing conclusions.

If the evidence isn't conclusive, say so — don't force a diagnosis.

### Step 6 — Recommend the next action

Pick the cheapest next step that would actually resolve the
ambiguity:

- Re-run the fixture (cheap and decisive if you suspect jitter).
- Diff against the last passing run log (cheap; commits make this
  easy).
- Point the user at a specific turn: the `tool_calls` index `i`, and the
  `narration` entries with `tool_calls_before == i + 1` (the prose that
  followed that call).
- Update the fixture's `README.md` to record what shifted if it
  looks like FS data drift.
- File a regression issue if the cause looks like an agent or
  sub-skill regression.

The run and its `run-<ts>.ann.json` land in the same PR; CI blocks a run that
produced a tree without its `.ann.json` (a treeless or `host_slept` run is exempt).

## What you do not do

- Do not read or report the judge's grade for this run: `judge_output`
  (per_finding / rationale / proof_quality), the top-level `verdict`, or the
  `outcome` gate. `compliance` and `guardrail_bypass_violations[]` are harness
  facts and ARE reportable (Step 2d).
  Explain the run from the tree, the agent's proof conclusion, and the harness
  facts — never the judge's grades.
- Do not edit fixtures or skills — interpretation only. If the
  diagnosis points at a fixture problem (e.g. a finding's description is
  too literal to match the tree), tell the user and suggest
  `/author-e2e-fixture` to revise.
- Do not run the e2e harness yourself. The user runs the harness
  on the host where FS credentials and the compiled MCP server live;
  you only read the artifacts it produces.
- Do not pad the output. A clean recovery gets a one-line summary; a
  run with misses gets the analysis above. Skip sections that don't apply.

## Example

User: "Why did the <slug> run fail?"

You should:
1. Read `eval/runlogs/e2e/<slug>/run-<latest>.json` (harness
   fields only — skip `judge_output`, `verdict`, and `outcome`) and check that
   `run-<latest>.ann.json` exists.
2. Read `eval/tests/e2e/<slug>/expected-findings.json` and the
   final tree; the tree contains **none** of the required findings.
3. See `stop_reason: tool_cap`.
4. Skim the last 30 entries in `tool_calls` — agent is looping
   on `place_search` for "Augusta County" with three near-duplicate
   queries.
5. Tell the user: "Recovered none of the required findings; stopped at the
   tool cap (300 calls). Agent looped on `place_search` from turn 47 onward —
   three near-duplicate queries for Augusta County. Likely cause: `/research`
   skill regression (place-disambiguation guidance is weaker than the last
   passing run). Recommend diffing `tool_calls[]` against the previous green
   run for this fixture before changing the skill."

## Re-invocation behavior

**Writes:** nothing. This skill is read-only — it reads an e2e run
log (harness fields only, never `judge_output` / `verdict` / `outcome`), the
agent's final tree and
research files, and the fixture's `expected-findings.json`, and explains the
result in-session. It calls no MCP tools and edits no fixtures, skills, or
project files.

**On repeat invocation:** safe to run as often as needed. Each call is
a fresh read of the run-log artifacts.

**Do not duplicate:** N/A — no writes.
