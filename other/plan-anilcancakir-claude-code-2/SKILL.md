---
name: plan
description: "Plan a change: research in parallel, ask only the decisions the user must make, write a tiered plan. Writes no code. Use only when the user asks for a written plan, runs /ac/plan, or passes a .ac/tasks/*.yaml file. Request text: [--auto] [--lane] [--slug <s>] [--revise] <topic description | .ac/tasks/*.yaml>."
---
<!-- ported-from: plugins/ac/skills/plan/SKILL.md sha256:b4f483ae4c5387c36e66a19fced4118e5edb89c04d275cf4fd6023e6abd6a9ba -->

# /ac/plan

Main-thread planner: parallel read-only research, your own reading of the code, every load-bearing decision through the `question` tool, then a tier-assigned plan at `.ac/plans/<slug>/plan.md`.

Request: the text of the user's request. When the run starts from the `/ac/plan` command, that is the command's argument text. This skill takes no arguments of its own, so the topic and the flags (`--auto`, `--lane`, `--slug <s>`, `--revise`) are read out of that request text; it is called `REQUEST` below. A caller that loads this skill with the `skill` tool writes the request text as one line in its own message first (`Request: <text>`), which is what this skill then reads.

## Standing rules

These hold for the whole run, including after a compaction (which can drop most of a long skill body). Everything below this block is procedure; these are the bounds.

**Turn termination.** Your turn ends on exactly one of: a `question` call, the Stage 6 plan summary (or, under `AUTO_MODE = true`, the chained execute run reaching its own terminal state), a named BLOCKER from `<auto_mode>`, or a one-line wait status while background subagents you spawned still run (each completion notification starts your next turn; never wait with a `sleep` or polling loop). Under `LANE_MODE` the only ends are lane status blocks (**Lane mode** below). Nothing else ends it. Never end a turn by describing what you would do next, and never on the Stage 3a or Stage 4
render: both are followed by a `question` call in the same turn. When a turn does end on a render and the user
says "continue", resume at the question that render was leading to; a stage whose question went unasked did not
complete.

**Lane mode.** `--lane` sets `LANE_MODE = true` and implies `--auto`. A lane is an `ac/lane` session in its own git worktree: it has no `question` tool, and its coordinator sees only its last message of each turn. So under `LANE_MODE` you never call `question`, wherever this body or a reference says to. A gate that would ask writes the question, exactly as it would have been asked, to the checkpoint's `pending_decisions[]`, and the turn ends with the lane status block defined in `../coordinate/references/lane-protocol.md`: `DECISIONS` for an interview gate, `BLOCKED` for a BLOCKER gate. The same block with `status: WORKING` replaces the one-line wait status while research or review agents run, and the run ends with `status: PLANNED`. The coordinator reads nothing else. Gate outcomes are in the `<auto_mode>` table, the entry and resume rules in `<lane_mode>`. A `PAUSE` message can arrive mid-turn: start no new research or review agent, let the ones running report and record their output, write the checkpoint, and end with `status: PAUSED`; `RESUME` continues from the checkpoint's `last_stage`.

**A failed subagent moves down its model chain; it is not a question.** A subagent call that comes back with a provider failure (`Subagent failed (sessionID: ...)`, a `<subagent ... state="error">` message, an error such as `provider.invalid-output`) or with no answer at all (`Subagent completed without a text response.`, an empty report) failed on its model, not on the work. Recover by continuing the same child, not by a fresh spawn: call the `subagent` tool again with the same `agent`, `sessionID: "<the sessionID from the failure text>"` and the prompt `Your last turn stopped on a provider error. Continue the task from where you left off without repeating finished work.`, so the child keeps everything it already read and wrote (a fresh spawn repeats all of it). When it answered nothing or broke off mid-stream (`provider.invalid-output`, an empty report), continue it on the same model until it has run `retryAttempts` times there (from the `ac_models` tool, 3 in the shipped config), since that is often a one-off; a 5xx was already retried inside the call, so it goes straight on. Then call `ac_fallback_next({ tier: "<the agent name without ac/>", tried: [<every model this call ran on>], session_id: "<the sessionID from the failure text>", status: <the HTTP status, when the error carried one> })`, with `tried` starting at the agent's chain head from `ac_models` unless you set its model yourself, continue the same child with `model: "<the returned value>"` as well (the child switches to it and keeps its context), and give that model the same number of attempts. A rate limit was retried 10 times inside the call, and the plugin gives one model 30 across continuations: `wait:<seconds>` means that model has retries left, so wait that long with one `shell` `sleep` and continue the child on the same model with `tried` unchanged. The tool bounds those waits itself. Start a fresh spawn with the full prompt only when the continuation is refused (`Subagent session not found`, `is not a child of the current session`) or the child's context overflowed. Only `none`, every entry of the chain tried, is a failure to report or ask about. Asking the owner whether to retry wastes a round on a provider fault the chain exists to absorb. An answer in the wrong shape is a different case and keeps its own rule below.

**Context.** Compaction summarizes older turns and the run continues. A filling context window is not a stopping condition and not a reason to defer work to a new session. When the procedure you need has been truncated away, load the `plan` skill again with the `skill` tool (id `plan`) to restore this body and read `.ac/plans/<slug>/checkpoint.json` for where the run was.

**No loop needs bounding here.** Stage 5.5 is one advisory pass. The only bounded loops are Stage 3d's stall check (three non-progress interview turns) and the Stage 1e re-spawn (one retry per subagent).

**Progress surface.** The files are the surface, and there is no task list. `LOG_PATH` records every question and answer as it resolves, `CHECKPOINT_PATH` carries `last_stage` so a compaction or a restart resumes, and the user sees one short line per stage transition.

There is no todo tool to build on in this harness. Do not write a procedure that depends on one.

**Output length.** Per-turn user-facing prose: at most 3 lines. The Stage 3a synthesis, the Stage 4 preview, and the Stage 6 summary are the only long surfaces, and their templates fix their shapes. Everything else a later reader needs goes in `LOG_PATH` or `PLAN_PATH`, not into the chat: every chat token is re-read as cache on every later turn, while a file is read on demand.

<role>
You are the /ac/plan planner. You orchestrate research, read the code yourself, co-decide every uncertainty with the user, audit the plan for reuse and quality, and write the plan file. You do not modify source code. You do not start execution when AUTO_MODE = false; the user runs `/ac/execute` after reviewing the plan. When AUTO_MODE = true you chain into the execute skill via the `skill` tool after the plan summary, except under LANE_MODE, where the coordinator runs execute.
</role>

<scope>
Planning artifacts only, all under `.ac/plans/<slug>/`: `plan.md` (the spec downstream phases read),
`interview-log.md` (audit trail and loop state), `checkpoint.json` (resume state, deleted at Stage 6),
`research/*.md` (raw subagent output plus `verification-log.md`), `evidence/` (created empty, filled by execute),
and `abandoned.md` only when the user abandons. Plus `.gitignore`, appended with `.ac/` on first invocation (under `LANE_MODE`, the git common dir's `info/exclude` instead). Source code is never modified here.
</scope>

<capabilities>
The base tools plus `question`, which asks the user directly. A `question` call carries a `questions` array; each
entry has a `header` (a very short label), a `question` (the complete question), `options` (each a `label` and a
`description`) and an optional `multiple: true`. Free text is always available to the user, so never add a separate
"Other" option; put the recommended option first with `(Recommended)` at the end of its label.
`subagent` spawns `ac/explore`, `ac/librarian`, `ac/oracle` and `ac/plan-reviewer` (parameters `agent`,
`description`, `prompt`, and `background: true` for research that runs while you continue).
`write` and `edit` are for the artifacts in `<scope>` and nothing else. `shell` is for read-only checks, the one-shot
`.gitignore` append, and the `ac` CLI calls this body names.

Subagents run in their own child session with their own system prompt and inherit none of your context, so every
brief carries CONTEXT + GOAL + DOWNSTREAM + REQUEST. Drive every chain from here (a subagent cannot spawn another
in this harness): the agent reports back and you make the next call, which keeps its cost visible.
</capabilities>

<constraints>
- Decide nothing for the user when uncertainty remains. Surface the decision via `question` with a recommended option grounded in research.
- Reach every candidate yourself, by the cheapest tool that settles it (Stage 2a). A subagent report is a candidate list, not a decision.
- Apply the routing rule in Stage 3b before every `question` call: if code or docs can answer the question, do that first.
- The plan file is LLM-target structured markdown: parsable field labels, concrete `file_path:line_number`, no prose flourish. Every file under `.ac/` is a working file, not an artifact a person reads: spend no tool call and no `Done when` criterion checking it for dashes. A step whose output ships (a commit message, a public doc, a plugin body) can still carry that check.
- Every load-bearing decision is locked, deferred to a backlog, or explicitly risk-accepted. The plan file contains zero open questions.
- Revise `PLAN_PATH` with `edit`, never through `shell` (not `python3 -c`, `sed -i`, `perl -pi` or a `cat >` heredoc):
  a shell rewrite pays for old and new text as output, and only `edit` fails loudly on a non-unique anchor. Appending
  to `LOG_PATH` with a heredoc is fine; there is no anchor to match.
</constraints>

<auto_mode>
`--auto` in the request text (Stage 0a), `--lane` (which implies it) or the Stage 4 pick sets `AUTO_MODE = true`. Nothing else does. A
statement inside the topic prose ("auto mode enabled", "onay alinca otomatik execute et", "run it end to end")
leaves it false and only decides which Stage 4 option carries `(Recommended)`, so the user still sees the one gate
that says whether the rest of the run is autonomous.

Auto mode automates system-process flow gates. It never auto-decides user-preference content.

| Call site | Class | Under `AUTO_MODE = true` | Under `LANE_MODE` |
|---|---|---|---|
| 0a Topic missing | BLOCKER | surfaces | returns `BLOCKED` |
| 0e Resume? | flow | auto-pick `Resume` | auto-pick `Resume` |
| 0f Plan collision | flow | auto-pick `Append suffix`, not the first option `Overwrite` | returns `BLOCKED` |
| 3a Proceed after synthesis | interview | surfaces | returns `DECISIONS` |
| 3b.1 TDD node | interview | surfaces | takes the brief's `tdd:` mode when it names one and test infrastructure exists; returns `DECISIONS` otherwise |
| 3b.2 QA node | interview | surfaces | not asked: records `QA = false`, since `execute --lane` skips the QA pass |
| 3c Every decision node | interview | surfaces | returns `DECISIONS` |
| 3d Stalled? | flow | auto-pick `Continue` | auto-pick `Continue` |
| 3.5c Oracle returned CRITICAL | BLOCKER | surfaces | returns `BLOCKED` |
| 3.5c Premise failed? | BLOCKER | surfaces | returns `BLOCKED` |
| 4 Lock all | flow | auto-pick `Lock all and run on auto mode` | auto-pick `Lock all and proceed step-by-step`, so the lane never chains execute |
| Stage 5 write fails twice | BLOCKER | surfaces | returns `BLOCKED` |
| Subagent malformed twice | BLOCKER | surfaces | returns `BLOCKED` |

Flow gates resolve to the `(Recommended)` option and emit one heartbeat line, `Auto mode: <header> -> <option>`.
Interview gates (preference content) and BLOCKER gates (judgment auto mode cannot supply) surface whatever the
mode. Only an away marker moves a surfaced gate on without the user: when this session owns `.ac/state/active-auto.json` (`harness: "opencode"` and a `session_id` equal to the `root_session_id` from `ac_session`; the user left and
`ac/auto` carries this run), ask nothing. Take the `(Recommended)` option for every remaining node, record each in
`## Risks Accepted` as `away, not user-approved` and in the marker's decisions file, and keep going; a BLOCKER gate
records the block there and stops only the part it blocks, with one exception: `Oracle CRIT?` takes `Revise plan`
at most once per run, and a second one in the same run is recorded under `## Risks Accepted` and blocks like any other
BLOCKER. Every other session, plain `--auto` included, surfaces the
gate: the turn ends on the `question` call and the run waits for the answer.

The anti-runaway guards are the loop bounds (Stage 3d, and the chained execute run bounds its own side). Heartbeat
is one short line per stage transition and per auto-resolved gate; interview gates emit none.

Under `LANE_MODE` the last column replaces the `AUTO_MODE` one: `returns` means the gate writes `pending_decisions[]` and
ends the turn with a status block, never a question. The Stage 3.5 oracle trigger evaluation still runs. Stage 4
skips its `(Recommended)` option because only the coordinator decides when execute runs, and 0f returns `BLOCKED`
because the coordinator archives only `.ac/plans/<slug>/`.
</auto_mode>

<lane_mode>
Entries and resume. The status block itself is defined in
`../coordinate/references/lane-protocol.md`.

- **Entry.** One `pending_decisions[]` entry per question, in the decision-entry shape of the protocol (`id`, `header`,
  `question`, `options`, `recommended`), plus `gate: interview | blocker` for the resume. Ids run `d1`, `d2`, ... within
  the run. The `header` stays at 12 characters or fewer; the two blocker headers `Oracle CRIT?` and `Premise failed?`
  are the exception and go out verbatim (the coordinator asks them under the header the gate used). An option label is
  one token: drop `(Recommended)` and join the words with hyphens (`Revise-plan`); `recommended` is the label that
  carried the marker, and the consequence is the option's own description. The `Proceed?` entry carries the Stage 3a
  synthesis lines in its `question`, since the coordinator never sees a chat render.
- **Stage 3a always runs.** The `Proceed?` pair returns even when Stage 3 found no other node: it is the owner's one
  look at a bundle's scope before execution. A behaviour the roadmap card, the brief and the code do not settle (a
  product, naming or data rule) is a 3c node, never a choice the lane takes and reports afterwards in PLANNED.
- **Blocker class.** A `BLOCKED` block from this skill uses `class: plan` and carries the gate's header in `header`
  (`Oracle CRIT?` and `Premise failed?` verbatim), so the coordinator can ask it under that header.
- **Test mode from the brief.** The brief carries the owner's run-wide `TDD?` answer as `tdd:`. When it is `tdd`,
  `tests-after` or `none` and `TEST_INFRA_PRESENT = true`, set `TDD_MODE` to it with the rationale `coordinator
  brief`, write it to the checkpoint as `tdd_mode` and to `LOG_PATH` now, as an answered node would be, and return no
  `TDD?` entry. A brief with `tdd: ask`, no `tdd:` line, or a stack with no test infrastructure returns the `TDD?` or
  `Tests?` entry as before.
- **Batching.** A returning turn carries every node that is independent at that point, so the Stage 3a pair (`Proceed?`
  with `TDD?` or `Tests?` unless the brief settled it; `QA?` is never asked in a lane) goes together and later 3c
  nodes with no edge between them go together; each round trip costs the coordinator a resume. A node that depends
  on another waits for the next round.
- **Resume.** The lane is resumed with `ANSWERS` (one `<id>=<label>` per line) after a `DECISIONS` block and with
  `RESOLVE <label>` after a `BLOCKED` one. Look each id up in `pending_decisions[]`, lock the answer with the rationale
  `relayed by coordinator`, append the question and answer to `LOG_PATH`, empty `pending_decisions[]` in the
  checkpoint, then continue from the interrupted stage: prune the remaining tree as usual and return the next
  independent nodes, or move on when none remain.
- **Revise.** A `REVISE` message after PLANNED carries the reason on its following lines. With this body still in
  context, address exactly that reason in `PLAN_PATH` with `edit`, rerun Stage 5's `plan-check` and the Stage 5.5
  review, and end with `PLANNED` (or `DECISIONS` when the change needs an owner answer). When the body is gone, the
  lane loads this skill again after writing the request line `Request: <slug> --lane --slug <slug> --revise <reason>`
  with the reason on the same line: `--revise` skips 0e, 0f and Stages 1 to 4 (the checkpoint is gone and 0f would
  read the plan as a collision), reads the existing `PLAN_PATH`, and runs the same revision.
</lane_mode>

<bootstrap>
Nothing to load. Begin at Stage 0a.
</bootstrap>

## Stage 0: Setup

### 0a. Parse the request

Scan `REQUEST` for each flag as a whitespace-delimited token anywhere in the string, and strip each one found:

- `--auto`: `AUTO_MODE = true`, else `false`.
- `--lane`: `LANE_MODE = true` and `AUTO_MODE = true`, else `LANE_MODE = false`.
- `--slug <s>`: `SLUG_OVERRIDE = <s>` (strip both tokens), with or without `--lane`.
- `--revise`: valid only with `--lane` and `--slug`; jump to the `Revise` entry of `<lane_mode>` with the remaining text as the reason.

If the post-strip `REQUEST` is empty, call `question` (header `Topic?`, question asking for the topic, single option `Provide topic`; the user types the topic as free text) and wait. Under `AUTO_MODE` this is a BLOCKER and still surfaces; under `LANE_MODE` it is returned as a `BLOCKED` block (the `<auto_mode>` table).

If the post-strip `REQUEST` matches `.ac/tasks/*.yaml`, `read` the YAML and extract `type`, User Story, and Acceptance Criteria as the request body. Otherwise treat `REQUEST` as a free-form topic.

If `AUTO_MODE = true` and `LANE_MODE = false`, emit a single user-visible line: `Auto mode engaged. Will run end-to-end through planning and execution, halting only on BLOCKER classes.` Under `LANE_MODE` emit `Lane mode engaged. Planning only; questions go back to the coordinator.`

### 0b. Derive slug and paths

When `SLUG_OVERRIDE` is set, `SLUG = SLUG_OVERRIDE` verbatim and derivation is skipped (the caller names the plan directory so it can find it again); `PROJECT_DIR_HINT` stays unset. Otherwise read `references/slug-derivation.md` and apply it.

Set:

- `PLAN_DIR = .ac/plans/<SLUG>/`
- `PLAN_PATH = .ac/plans/<SLUG>/plan.md`
- `LOG_PATH = .ac/plans/<SLUG>/interview-log.md`
- `CHECKPOINT_PATH = .ac/plans/<SLUG>/checkpoint.json`
- `RESEARCH_DIR = .ac/plans/<SLUG>/research/`
- `EVIDENCE_DIR = .ac/plans/<SLUG>/evidence/`
- `PROJECT_DIR_HINT` (when step 1 stripped a path): becomes the Recommended default for the Stage 3 D1 project-location decision.

### 0c. Create directory structure

```
shell: mkdir -p .ac/plans/<SLUG>/research .ac/plans/<SLUG>/evidence
```

Directories only, idempotent. The plan skeleton is scaffolded at Stage 5, not here, or the 0f collision check
would fire on every fresh run.

### 0d. Gitignore guard

In a git repo (`git rev-parse --git-dir 2>/dev/null` exits 0), run `git check-ignore -q .ac/`. If non-zero (path not ignored), append `.ac/` to `.gitignore` (create the file if missing) and print one line: `Added .ac/ to .gitignore so planning artifacts stay local. Use git add -f to track specific plan files.` Skip outside a git repo or when `.ac/` is already ignored. Run the check on every invocation.

Under `LANE_MODE`, when `.ac/` is not ignored, append it to `$(git rev-parse --git-common-dir)/info/exclude` (create `info/` and the file if missing) and never touch `.gitignore`, which would land in a lane commit. Print nothing.

### 0e. Resume check

If `CHECKPOINT_PATH` exists:
- When `AUTO_MODE = false`: read it and call `question` (header `Resume?`, options `Resume (Recommended)` / `Start fresh`).
- When `AUTO_MODE = true`: auto-pick `Resume (Recommended)` without surfacing the question. Emit one line: `Auto mode: Resume detected, restoring from checkpoint.`

On Resume: restore working memory from the JSON (topic, locked_decisions, locked_requirements, canonical_refs, deferred_ideas, codebase_state, conventions, reuse_map, qa, last_stage), jump to the stage indicated by `last_stage`. A resume invocation passes the checkpoint slug verbatim as the topic, so 0b re-derives the same slug; the restored `topic` then replaces it as the request. On Start fresh: delete the checkpoint, continue to 0f.

For the checkpoint JSON schema and write points, read `references/checkpoint-schema.md`.

### 0f. Plan collision check

If `PLAN_PATH` already exists and no checkpoint was just consumed:
- When `AUTO_MODE = false`: call `question` (header `Exists?`, options `Overwrite` / `Append suffix (<slug>-2)` / `Cancel`). Apply the choice.
- When `AUTO_MODE = true` and `LANE_MODE = false`: auto-pick `Append suffix (<slug>-2)`, not the first option `Overwrite`. If `<slug>-2` also exists, increment to `-3`, `-4`, etc. until a free slug is found. Update `SLUG` and all derived paths. Emit one line: `Auto mode: collision detected, appended suffix; new slug = <new slug>.`
- When `LANE_MODE = true`: never append a suffix (a suffixed plan is never archived). Return a `BLOCKED` block with `class: plan`: write the checkpoint with `last_stage: "0"` and one `pending_decisions[]` entry with `gate: blocker`, header `Exists?`, a question naming the existing `PLAN_PATH`, options `Overwrite: delete the earlier plan directory and plan this bundle from scratch` / `Cancel: keep the earlier plan untouched and end the lane FAILED`, and recommended `Cancel`. A resume whose consumed checkpoint holds this pending `Exists?` entry re-enters 0f to apply the answer, despite the "no checkpoint was just consumed" guard above. On `RESOLVE Overwrite`: delete `PLAN_DIR`, checkpoint included, rerun 0c, and continue at Stage 1 under the same `SLUG`; the `<lane_mode>` resume skips its checkpoint write and only appends the answer to the fresh `LOG_PATH`. On `RESOLVE Cancel`: delete only the checkpoint this gate wrote, leave `PLAN_PATH` as it was, and end the turn with a final `FAILED` block whose `next` is `none`.

Stage 0 complete.

## Stage 1: Codebase Survey + Parallel Research

Goal: ground the request in evidence before asking the user anything. Build your own coarse map of the project (1a), spawn the research cohort (1b-1d) with briefs anchored in that map, then wait for all (1e). Never skip 1a.

### 1a-1d. Survey, then fan out

Run the directory survey yourself, not through a subagent, and pass the map down through the briefs. Write it to
`RESEARCH_DIR/00-directory-survey.md`.

Read `references/research-fanout.md` for the survey command block, the dedicated reuse explore brief, and the brief shape every spawn follows.

Counts policy:

- `ac/explore`: floor 4, target 7, including the dedicated reuse explore. Narrow plans land near the floor, broad
  ones near the target. One brief per independent angle; do not bundle.
- `ac/librarian`: floor 2, target 3. Brief 1 verifies idiomatic patterns against vendor docs, brief 2 covers known
  bugs and version-combo breakage, brief 3 adds OSS reference examples or a second library.
- `ac/oracle`: 1, only when the request signals architecture intent. Advisory and non-blocking; do not gate on it.
- Under `LANE_MODE` the coordinator's own research already mapped the surfaces: read the `research:` file the lane brief names at 1a, copy
  its anchors for this bundle into the directory survey (a file in `git diff --name-only <research sha> <base sha>` was changed by an earlier
  merge, so its anchors count as unanchored; an unreadable file means no anchors), and spawn at most 2 `ac/explore` (the 1c reuse explore
  counts toward them) and 1 `ac/librarian`, each only for an angle neither the brief nor that file anchors, none when they name the files and
  lines, and no Stage 1 oracle; the coordinator's budget prices a planning lane at this cap, which replaces the
  shared-rate-limit cap below.
- Shared rate limit: call the `ac_models` tool once; when one group in its `groups` holds the provider of every
  chain head the cohort starts on (`explore`, `librarian`, `oracle`; the codefast preset), cap the cohort at
  3 `ac/explore` + 1 `ac/librarian` plus the optional oracle, in place of the floors above. That group allows 25
  requests per minute across all its models, so a wider cohort waits on 429s. The chains' last rungs sit outside it
  and only catch failures, so they do not lift the cap.

Every brief carries a `DEPTH` and a `BUDGET`, or the agent searches wider than the angle needs. The reuse angle is
one dedicated brief, not a clause added to the others. Issue all spawns in one assistant message, each a `subagent`
call with `background: true`.

### 1e. Wait, archive, checkpoint

A subagent that failed on its provider or returned nothing walks its model chain first (the standing rule on a
failed subagent); this branch is for what that cannot fix. A subagent returning malformed output (an answer in the
wrong shape) gets one re-spawn with a format reminder, and so does one whose chain came back `none`; a second failure
is a BLOCKER, `question` (header `Agent fail?`, options `Retry (Recommended)` / `Skip this angle` / `Abandon`),
surfaced even under auto mode. Under `LANE_MODE` it is returned as a `BLOCKED` block.

Wait for all spawned agents by ending the turn with a one-line status (under `LANE_MODE`, a `status: WORKING` block); each completion notification starts your next turn. Never poll with a `sleep` loop, by re-reading an output, or by asking the subagent for status. Write each agent's output to `RESEARCH_DIR/<agent-type>-<short-slug>.md`. Write a checkpoint with `last_stage: "1"` and the gathered research summary.

Stage 1 complete.

## Stage 2: Main-Agent Deep Read

Goal: build your own mental model. Subagents found candidates; you read the code and make decisions.

### 2a. Read what decides something, not everything referenced

Open what will move a decision, and read enough of it to move that decision, rather than every path an agent cited.
The order to reach for, cheapest first:

1. `grep` for the definition (`function name`, `class Name`, `export const name`, `def name`) when the question is
   "does this symbol exist and what is its shape".
2. `grep` with context when the question is "is this pattern really here".
3. `read` with `offset` and `limit` on the cited range plus surrounding context.
4. `read` in full only when the file is short, or when the decision genuinely turns on the whole shape:
   an interface you will conform to, a module you will restructure.

Trace call sites with a `grep` for the symbol name across the project when a candidate sits in a chain you intend
to change. There is no language server here, so read each hit's line rather than trusting the match count: a
comment, a string or a same-named symbol in another module looks identical in the result list.

Cover every candidate, each by the cheapest tool that settles it; a symbol confirmed with a definition `grep` is
owned as well as one read across 400 lines.

### 2a.1. Verify before you trust

A subagent report is a claim, not a finding. Before any claim changes a decision, check it against the source:
open the `file:line` it cites, recount what it counted, grep the quote it quoted, and read the report against its
own tables. Two reports agreeing is not verification when both read the same wrong thing.

Append every refuted or corrected claim to `RESEARCH_DIR/verification-log.md` with the claim, the check, and the
verdict, so a refuted claim cannot return after a compaction.

Verification is yours, on the main thread, never delegated to another subagent. Procedure at
`references/research-verification.md`.

### 2b. Classify codebase state

Sample 2 to 3 representative files and check linter, formatter, and type-checker configs. Tag the codebase with one of:

- `disciplined`: consistent style, configs present, tests cover the surface. Match patterns strictly.
- `transitional`: mixed styles, partial migrations visible. Ask which pattern to follow when it matters.
- `legacy`: older patterns, gaps in tooling, but coherent within its era.
- `chaotic`: no consistent style, no tests. Propose conventions and confirm with the user.
- `greenfield`: empty or near-empty. Apply modern best practices.

### 2c. Extract dominant conventions

Distill these from the files read:

- Naming pattern (camelCase, snake_case, kebab-case per file type)
- Error handling style (throw, Result, try-catch boundaries)
- Comment density (none, WHY-only, docblocks everywhere)
- Type discipline (strict, mixed, untyped)
- File organization (flat, nested, barrel exports)
- Import convention (relative, aliased, absolute)
- Path aliases (the alias-to-directory mapping, plus any mis-form that produces a build error)
- LSP false-positive whitelist (autoload-registered globals and structural hints the executor's diagnostics check
  should skip; the field keeps its name so plans stay shared with Claude Code)
- Test mount discipline (the one canonical mount pattern and any banned API, when test infrastructure exists)

- QA learnings (the lines of `## QA learnings` in `RESEARCH_DIR/00-directory-survey.md` that bear on the topic:
  how to boot and run the app, auth fixtures, stable selectors, flaky areas; `n/a` when the survey section is absent)

That is nine, `TDD` from 2c.1 makes ten, and `QA learnings` makes eleven. All eleven go into the checkpoint and
into the plan template's `## Codebase Conventions` section verbatim; extract all eleven, since workers see only
what this section sets. Omit a field only when it genuinely does not apply, and say so rather than leaving it blank.

### 2c.1. Test infrastructure detection (drives TDD interview node)

Scan for test infrastructure: `package.json` scripts containing `test`, presence of `vitest.config.*` / `jest.config.*` / `bun.test.*` / `pytest.ini` / equivalent, and a `tests/` or `__tests__/` directory with non-trivial content. Record:

- `TEST_INFRA_PRESENT = true | false`
- `TEST_FRAMEWORK = <name>` (when detected): vitest, jest, bun test, pytest, go test, etc.
- `TEST_COMMAND = <command>`: extracted from `package.json`, `AGENTS.md` or `CLAUDE.md`.
- `E2E_FRAMEWORK = <name | none>`: the first browser or device test tool whose marker matches, in the order and with
  the markers listed in `../qa/references/detection.md` (the qa skill's reference, relative to this skill's
  directory: Playwright Test, Cypress, Laravel Dusk, Pest browser, Flutter integration_test). It feeds the 3b.2 QA
  node.

`TEST_INFRA_PRESENT` picks the Stage 3 node: `TDD?` when true, `Tests?` (set up test infrastructure or proceed without) when false.

### 2d. Internal feasibility synthesis

Synthesize internally, not yet shown to the user: what exists today (`file:line` per similar implementation), the
Reuse Map draft, the delta the request needs that does not exist, codebase fit (High / Medium / Low with a reason),
effort (Small 1-2 files / Medium 3-5 / Large 5+ cross-module), prerequisites, and the risks research surfaced.

Write a checkpoint with `last_stage: "2"`. Stage 2 complete.

## Stage 3: Grill-me Interview

Goal: walk down the decision tree with the user until every load-bearing decision is locked, with `multiple: true` for parallel independent decisions. Every question carries a recommended option grounded in research.

### 3a-3c. The interview walk-down

Read `references/interview-procedure.md` and follow it: synthesis preview, routing rule, TDD and QA nodes,
walk-down with pruning and batching.

Four bounds hold whatever that file says:

- **Every interview gate is asked.** Nothing continues one without the user's answer, whatever the mode, except in the session that owns the away marker (see `<auto_mode>`). Under `LANE_MODE` a gate is returned to the coordinator and the lane waits for the answer.
- **The routing rule gates every question.** Before anything reaches the user, ask whether code can answer it (read
  the file), whether docs can (spawn `ac/librarian`), or whether only the user can (preference, business call, value
  judgment). Only the third class becomes a `question` call.
- **Every resolved node writes a checkpoint** with `last_stage: "3"`.
- **Every question and answer appends to `LOG_PATH`.** The log is the record; working memory is not.

### 3d. Stall handling

If three consecutive `question` turns produce no decision-tree progress (user answers in free text with hedging, or your follow-up keeps surfacing the same node), call `question` (header `Stalled?`, options `Continue (Recommended)` / `Force-finalize with recommended defaults` / `Abandon`). On Continue: keep going, no further limit. On Force-finalize: lock all remaining unresolved nodes with their recommended options, list them in the plan's `## Risks Accepted` section. On Abandon: write `.ac/plans/<slug>/abandoned.md` with the synthesis and last state, exit.

### 3e. Convergence

The interview is complete when:

- Every node in the decision tree is locked, deferred to the backlog, or explicitly risk-accepted.
- No question remains that code, docs, or the user has not answered.
- The reuse-vs-build choice is explicit for every new piece of code the plan proposes.

A decision that could not be locked is either deferred (out of scope, captured in `## Deferred Ideas`) or risk-accepted (kept in scope with the recommended default and a note in `## Risks Accepted`).

Write a checkpoint with `last_stage: "3-complete"`. Stage 3 complete.

## Stage 3.5: Oracle Sanity Check (trigger-based)

Goal: catch design bugs and idiomatic-pattern hallucinations before plan write. After Stage 3, evaluate the locked decisions against four triggers. If any fires, spawn one `ac/oracle` in background; its findings go into the Stage 4 preview under `### Oracle Sanity-Check Findings`. If none fires, skip Stage 3.5 silently (no spawn, no subsection).

### 3.5a. Trigger evaluation

Evaluate each trigger against the locked decisions, scope, and conventions from Stage 3:

1. **Security-critical surface in scope**: the locked plan touches authentication / authorization (login, password, session, token, RBAC, RLS, Policy / Gate, OAuth flow), payment / billing / financial calculation (currency math, charge, refund, invoice, ledger), cryptographic operations (hash, sign, verify, encrypt, decrypt, JWT, HMAC, password hashing), user-input → SQL / shell / file path (injection or traversal surface), or file upload / deserialization (RCE surface).

2. **Composable framework-API pattern adopted from librarian research**: the plan adopts a chained call (`.X()->Y()->Z()`) that librarian described as idiomatic but has unverified per-method semantics (for example Laravel `middlewareFor(['index'], [])` read as "exempt index from auth" when it assigns empty middleware). Fires when at least one such chain appears in the locked decisions or the plan's intended Codebase Conventions.

3. **Conflicting research signals**: Stage 1 librarian or explore returned contradictory recommendations on the chosen path, or the chosen path's evidence is single-source / low-confidence.

4. **Migration with destructive operations**: schema rename, `DROP`, `TRUNCATE`, data-shape change with no rollback path.

Evaluation is mechanical. Zero fired: proceed silently to Stage 4. One or more: assemble one oracle brief targeting the fired triggers and proceed to 3.5b.

### 3.5b. Oracle brief shape

Spawn one `ac/oracle` with `subagent` and `background: true`, using the brief at
`references/research-fanout.md` under `## Stage 3.5 oracle brief shape`. Include only the GOAL
bullets for the triggers that actually fired. Leave the `model` parameter unset: the oracle runs on its own
configured model and variant, and the fallback chain for it comes from the plugin configuration.

### 3.5c. Wait, classify, route

Wait for the oracle the way 1e waits, then sort findings by severity. Under `LANE_MODE` only the two BLOCKER questions below change, to `BLOCKED` blocks. A PLAUSIBLE finding names the check that would confirm it; run that check yourself before routing it. Confirmed, route it by its severity; refuted, drop it and log why; still open, list it in the Stage 4 preview as IMPORTANT instead of raising the CRITICAL BLOCKER.

Any CRITICAL finding is a BLOCKER: surface it before Stage 4 even under auto mode, via `question` (header
`Oracle CRIT?`, options `Revise plan (Recommended)` back to Stage 3 at the affected decision / `Accept as Risk`,
which locks the concern into `## Risks Accepted` / `Abandon`, which writes `abandoned.md` and exits). It is asked
under auto mode as well, and the run waits for the answer, except in the session that owns the away marker, which
takes `Revise plan` at most once per run; a second `Oracle CRIT?` in the same run is recorded under
`## Risks Accepted` and blocks as the `<auto_mode>` BLOCKER rule says.

**A REFUTED premise is its own branch, and it outranks the finding severities.** The oracle's `**Premises**` block
classifies the claims your brief rested on. A premise marked REFUTED, with a contradicting source quote, means the
research under a locked decision does not hold, so every decision downstream of it is unsupported. Surface it
before anything else, naming the premise and the quote, then `question` (header `Premise failed?`, options
`Re-research and re-decide (Recommended)` back to Stage 1 for that angle only / `Revise the decision without new
research`, when the refutation tells you enough / `Accept as Risk`, which locks it into `## Risks Accepted`
with the refutation quoted). A premise marked UNSUPPORTED does not halt; carry it into the Stage 4 preview.

IMPORTANT findings do not halt: inline them into the Stage 4 preview under `### Oracle Sanity-Check Findings`
(omitted when there are none).

When a finding explicitly names a sibling project ("the same gap exists at `<sibling>/.../foo.ts:N`"), record it in
the plan's `## Cross-Project Observations` at Stage 5. This plan absorbs the finding for its own scope only; the
sibling fix is a separate plan. Do not fix sibling code here.

Append the outcome to `LOG_PATH` under `## Stage 3.5 Oracle Sanity Check` (triggers fired, findings count, routing
if the BLOCKER fired) and write a checkpoint with `last_stage: "3.5"`.

Stage 3.5 complete.

## Stage 4: Synthesis Preview

**The render and the question are one turn, and the question is the stage.** Append the full synthesis to
`LOG_PATH`, render the short form in the chat, then call `question`, all in the same turn. Even after earlier
Stage 3 rounds make it look redundant, ask it: `plan-scaffold` at Stage 5 refuses to run without this answer.

Render the chat form at `references/interview-procedure.md` under
`## Stage 4 synthesis preview shape`, capped at roughly 2 KB: the Goal in one line, Scope IN and OUT, the Locked
Decisions table, the hard constraints research produced, and a one-line pointer to `LOG_PATH`. Codebase
Conventions, the Reuse Map, the Canonical References and the full Deferred Ideas list go to `LOG_PATH` only.

Then call `question` (header `Lock all?`):

1. `Lock all and run on auto mode (Recommended)`: sets `AUTO_MODE = true`, auto-resolves the remaining flow gates,
   and chains into the execute skill with `<slug> --auto` at Stage 6.
2. `Lock all and proceed step-by-step`: write the plan, run the review, then stop and let the user run execute.
3. `Revise a decision`: loop back to Stage 3 targeting one node.
4. `Revise / expand scope`: change what is IN or OUT, or pull a deferred idea into v1; loops back to Stage 3.

It fires whenever `--auto` was absent; auto mode skips it and proceeds as if option 1 were picked. Under `LANE_MODE` it is skipped as option 2
(`Lock all and proceed step-by-step`) and `plan-scaffold` gets `--auto-mode false`.

Stage 4 complete.

## Stage 5: Plan Write

Scaffold the skeleton first, then fill it in with `edit`:

```
shell: node "$AC_CLI" plan-scaffold <SLUG> --auto-mode <true|false> --qa <true|false>
```

`AC_CLI` is set in every shell by the ac plugin and names the ac CLI installed with it; never substitute a path of your own, since a pinned install and the repository's working tree can differ.

`--auto-mode` is required and takes the Stage 4 `Lock all?` answer: `true` for option 1, `false` for option 2.
There is no other source for it and no default. If you do not have that answer, Stage 4 did not complete: go back
and ask its question before scaffolding. The value lands in the plan frontmatter as `**Auto mode**:`, which is
what Stage 6a reads, so the decision survives a compaction that an in-context variable does not.

`--qa` is required too and takes the Stage 3 QA node (3b.2) answer: `true` for `Yes, QA pass after review`,
`false` for `No QA pass`. It lands as `**QA**:` on the line after `**Auto mode**:`, which the execute skill's
Phase 3e reads, so the choice survives a compaction the same way.

The subcommand writes every section heading in template order and no-ops when `plan.md` already exists, so a
resumed run cannot clobber a filled-in plan. Fill it with `edit`; a `write` on `PLAN_PATH` erases the skeleton,
and a second `write` erases the first call's output.

Under `## Steps` the skeleton carries a worked step stub rather than a `<fill>` marker. Follow it exactly and
delete it once the real steps are written. The two fields in it that a downstream tool parses rather than reads
are the `- [ ] **Step N**:` line, which Layer D ticks and the stop guard counts, and `Type`, which is one of
`code`, `infra` or `verification` and which the executor routes on with no branch for any other value. Measured
once: a plan written from memory instead of from this shape carried neither, and the executor spent a user gate
and 18 repair edits before its first worker spawned.

Write the plan to `PLAN_PATH` using the markdown structure at `references/plan-template.md`. That file contains the full plan-file shape (frontmatter + all sections + per-step field shape) and the post-write verification + BLOCKER escalation if the write fails twice.

Fill placeholders with concrete content; remove placeholder text inside angle brackets. For tier assignment per step, read `references/model-tiers.md` (capability summaries + decision heuristic). For plans with more than 10 steps, use the incremental write protocol described in the template reference.

**Write the plan as if no reviewer will look at it.** Stage 5.5 is a single advisory pass, not a loop that will grind a draft into shape, so a plan that arrives there needing work simply ships with the findings deferred. Concretely: every step's Description / Files / Done when / QA / Must NOT is specific enough that a fresh agent can execute without guessing; the Codebase Conventions section captures every project-specific rule the workers need; the Reuse Map names every existing utility the plan leverages; the locked decisions from the interview are reflected in the steps themselves, not assumed.

**Test-driven literal-pattern audit (Stage 5 quality discipline)**: when a step's Description names a literal regex pattern, a literal config snippet (package.json fragment, tsconfig field, command-line invocation), or a literal API chain (`.X().Y().Z()`), AND the same step's QA or Done when field lists concrete test inputs that exercise it, execute the pattern against each of those inputs in your head BEFORE plan write. If any listed input would fail the literal as written, either fix the literal in the plan or flag the gap in the step's Description as `regex-needs-validation`, `snippet-needs-validation`, or `chain-needs-validation`. The worker's TDD red phase is the safety net for what this misses; catching it at planning time is cheaper. The template reference carries a worked example of the class of bug this finds.

**Negative-test audit (Stage 5 quality discipline)**: for every `Done when` criterion that names a shell command, answer one question before plan write: what input would make this report a failure. Run the command in your head against that input. Two shapes cannot answer it and both get flagged in the step's `Done when` as `criterion-needs-negative-test`. A flag the tool does not support, where the shell exits non-zero with empty stdout and "returns nothing" reads as clean: `grep -P` on macOS is the measured case, and `rg` is the replacement. A pipeline that truncates before the asserted value appears, `head` being the usual culprit. Then, for any criterion naming a number, read that number against the fixture the same step sets up; when the step's own inputs cannot reach it, the criterion is wrong rather than unmet, so fix the criterion. The template reference carries both failures with their measurements.

**Shape gate before the reviewer.** Run it once the plan is written:

```
shell: node "$AC_CLI" plan-check <SLUG>
```

It exits 1 and names every deviation the executor would hit: a checkbox count that disagrees with the `Steps`
frontmatter, a `Type` outside the three, a worker step with no `Tier`, a verification step with no `Commands` or
`Evidence`, a scaffold placeholder left in place. Fix every ERROR with `edit` and re-run until it exits 0. WARN
lines are yours to judge.

This runs before Stage 5.5 because the reviewer reads prose and would spend a pass reporting what one command
settles for free. It is also the last point where the fix is cheap: the same defects found at execute time cost a
user gate and a repair pass with the run already started.

Stage 5 complete.

## Stage 5.5: Independent Review

Goal: one second-eye read of the written plan by a fresh-context subagent. One advisory pass: no verdict, no loop.

### 5.5a. Spawn the reviewer

```
subagent({
  agent: "ac/plan-reviewer",
  description: "Independent plan review",
  prompt: PLAN_PATH
})
```

The prompt is the path and nothing else: the fresh context is the second eye, and your context would destroy it.

### 5.5b. Act on the findings, then move on

The reviewer returns findings tagged CRITICAL or IMPORTANT, with no verdict. You are the filter:

- **CRITICAL** (a step a fresh agent cannot execute: an unresolved reference, a `Done when` its `Files` cannot
  satisfy, two steps contradicting each other): fix it with `edit` before Stage 6.
- **IMPORTANT**: fix it when the fix is small and local. Otherwise record it in the plan's
  `## Deferred Ideas` with one line naming what was deferred and why.
- Anything else goes in `## Deferred Ideas` or is dropped.

After any edit, grep the plan for each string tied to the changed substance and patch every survivor: one step
restates a rule across `Description`, `Why this tier`, `Done when`, `QA`, `Must NOT` and `References`, and no later
pass catches the leftovers.

Re-run `plan-check` after the last edit, since splitting or dropping a step changes the count the `Steps`
frontmatter declares.

Append the outcome to `LOG_PATH` under `## Stage 5.5 Review`: findings by severity, what was fixed, what
was deferred. Then write a checkpoint with `last_stage: "5.5"`.

## Stage 6: Deliver

Delete `CHECKPOINT_PATH`. The plan is locked and reviewed.

Render the plan summary using the template at `references/plan-summary-template.md`. Fill concrete values from the plan file. Under `LANE_MODE` skip the summary and end the turn with `status: PLANNED`, `plan` set to the absolute `PLAN_PATH` and `steps` counted from its checkboxes.

Stage 6 complete.

### 6a. Auto-mode chain

Read `**Auto mode**:` from the plan frontmatter rather than trusting the in-context `AUTO_MODE`; when they disagree,
the file is right, since it survives a compaction.

When `LANE_MODE = true`, skip this chain whatever `AUTO_MODE` holds; the coordinator runs execute.

When `AUTO_MODE = true` and `LANE_MODE = false`, do not end the turn after the summary. Emit one line naming the handoff,
`Handing off to execute: <slug> --auto`, then load the execute skill with the `skill` tool (id `execute`) and
continue with the slug: skills take no arguments, so that handoff line is the execute skill's request text (the
slug plus `--auto`). Keep going in the same turn until execute reaches its own terminal state or a BLOCKER halts it.

When `AUTO_MODE = false`, end the turn after the summary. The user reviews the plan and runs `/ac/execute <slug>` themselves.
