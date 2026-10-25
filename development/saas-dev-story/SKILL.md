---
name: saas-dev-story
description: "Implements one story in code with tests, following its ADRs. Use when the user says to build, implement or start working on a story. Not for checking readiness beforehand or closing the story after."
argument-hint: "[story-path]"
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-dev-story/../../hooks/yaml-helper.sh" resolve_config *), Bash(bash .claude/scripts/story-facts.sh *), Bash(bash .claude/scripts/adr-status.sh *), Bash(bash .claude/scripts/md-section.sh *), Bash(bash .claude/scripts/session-state.sh *), Bash(bash .claude/scripts/review-receipts.sh hash *), Bash(nextjs *), Bash(mkdir -p production/qa/evidence/*)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,automation,workflow,qa.level,gate_level,engine_values,specialists,perf_budgets,system_overrides`

Resolved above — use as-is. No block → defaults in
`.claude/docs/config-resolution.md`.

Ask with the question tool. Without one, list the options numbered and end your turn
to wait. A skipped or dismissed question is not an answer: ask again in plain text.

# Dev Story

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Implements one story: checks it can start, marks it In Progress, hands the code to
the right programmer agent with a brief built from the story, then checks the
result parses and looks right, and hands off.

**Writes** (each after an ask that names it): the story's `Status`, `Last Updated`
and `## Files`, and its `production/sprint-status.yaml` entry. The programmer agents
write the code and tests under the code root and test root
(`.claude/docs/code-root-resolution.md`). The session checkpoint and the evidence
stamp are written without an ask.
**Next:** `/saas-story-done [story-path]`; at `standard` and `full`, `/saas-code-review
[files]` first.

Asks follow `.claude/docs/automation-modes.md` (collaborative always asks, guided
asks on major choices, autonomous logs and goes on; `automation_always_ask`
categories always ask).

Checklist (copy it and tick as you go):

```
- [ ] Phase 1: story found, tier resolved
- [ ] Phase 2: prerequisites checked (ADR, manifest, dependencies)
- [ ] Phase 3: story marked In Progress (one ask)
- [ ] Phase 4: programmer and stack specialist chosen
- [ ] Phase 5: work handed out with a full brief
- [ ] Phase 6: finished? parse check, run and look, one Run result line
- [ ] Phase 7: summary, ## Files, checkpoint, closing block
```

## Phase 1: The story

The text typed after the skill name is the story path. With nothing typed, take the
story the checkpoint in `production/session-state/active.md` names and confirm it:
"Continuing work on [title] — is that correct?" None there: ask "Which story are we
implementing?" with the `TODO` rows of `bash .claude/scripts/story-facts.sh --all`
as options. No story file under `production/epics/` at all: stop with
"No stories found in `production/epics/` — run `/saas-create-stories [epic-slug]` to make them (at `standard` and `full`, run `/saas-create-epics` first if there is no epic yet)."

`bash .claude/scripts/story-facts.sh <story-path>` gives its type, layer, TR-IDs,
ADRs and dependencies. Then read the story in full.

**Tier.** `workflow` for the story's system, keyed on the PRD filename stem of its
`PRD:` path (`design/prd/<stem>.md` → `<stem>`; the `[system]` of its TR-ID only when
there is no PRD path): that system's `system_overrides` row if there is one, else the
project value. Say it in your first reply: `Tier: workflow [value]`. That value, never
`rigor` or `qa.level`, picks the Phase 2 column and the closing Next step.

## Phase 2: Can it start?

| Input | `full` | `standard` | `minimal` |
|---|---|---|---|
| TR registry `docs/architecture/tr-registry.yaml` | missing: **stop**, "Run `/saas-architecture-review` to bootstrap it" | optional | not expected |
| The ADR the story names | missing, `Proposed`, `Deprecated` or `Superseded`: **stop** | the same, only when the story names one | the same, only when the story names one |
| Control manifest `docs/architecture/control-manifest.md` | missing: warn, go on | missing: warn, go on | not expected |

A story whose ADR field reads `N/A — [reason]` names none.

**The ADR.** `bash .claude/scripts/adr-status.sh <ADR id>` gives its status and
`version`. Stop messages: `Proposed` — "ADR-NNNN is still Proposed. Accept it with
`/saas-architecture-decision accept ADR-NNNN` before implementing." `Deprecated` or
`Superseded` — "ADR-NNNN is [status]; point the story at [successor] (edit its ADR
field; `/saas-create-stories` never rewrites an existing story) before implementing."
`NOT_FOUND` — "ADR file not found. Run `/saas-architecture-decision`, or correct the
story's ADR field."

**Do not open the ADR.** The story's ADR Decision Summary and Implementation Notes
are what the programmer reads instead. Compare the ADR's `version` with the story's
`ADR Version`:

- equal, or the story has no `ADR Version` (written before the stamp), or both are
  `unversioned`: trust the story. Note the last two in the summary ("summary
  trusted unverified").
- they differ, or the ADR is `unversioned` but the story names a date: read
  `references/version-mismatch.md`. On a match, do not load it.

Never treat an absent stamp as a stale one: unknown falls back to the story, and
`/saas-story-readiness` and `/saas-code-review` are the checks that catch drift later.

**The manifest.** When it exists, compare its `Manifest Version` line with the
story's. They differ: read `references/version-mismatch.md`.

**Dependencies.** For each path on the story's Depends on line,
`bash .claude/scripts/story-facts.sh <path>`. Not `COMPLETE`: ask "[this story]
depends on [dependency], which is [status], not Complete. How do you want to go
on?" Options: Proceed anyway — I accept the risk / Stop — I'll finish the
dependency first / It is done, the status was never updated — mark it Complete.
Stop: the story is BLOCKED (Phase 7), no agent. Mark it: ask "May I set [path]
Status to Complete?" first. Proceed: note it under Deviations. `NOT_FOUND`: warn
"Dependency story not found: [path]".

Any stop above: no agent runs. Go to Phase 7 and write the BLOCKED checkpoint.

## Phase 3: Mark it In Progress

Before any agent, ask once: "May I mark this story In Progress? This sets `Status`
and `Last Updated` in [story path] and its entry in `production/sprint-status.yaml`,
and at the end lists the files changed under its `## Files`." Leave the sprint file
out of the question when it does not exist. Put what you will do next before the
question: the question is the last thing in the reply. On yes:

- `bash .claude/scripts/md-section.sh set-field <story> Status "In Progress"`, then
  `set-field <story> "Last Updated" <YYYY-MM-DD> --after Status`. At `minimal` the
  story file is the only record of progress.
- `production/sprint-status.yaml`: this story's entry gets `status: in-progress` and
  the top-level `updated` today. No file: say `Sprint status not updated:
  production/sprint-status.yaml absent`.

Declined: change neither, print `Story not marked In Progress — declined` in the
summary, and go on.

## Phase 4: Who implements it

**Config/Data stories need no agent.** Show each value change as from → to, ask "May
I write [data file]?", and edit it. Go to Phase 6.

| Story | Programmer agent |
|---|---|
| Foundation layer, any type | `cloud-infra-engineer` |
| Type UI | `frontend-engineer` |
| Type Visual/Feel | `backend-engineer` |
| Core or Feature, core business workflow | `backend-engineer` |
| Core or Feature, LLM integration or ML | `ai-engineer` |
| Core or Feature, networking | `api-integrations-specialist` |

**The stack specialist, for every code story.** From the `specialists` line above:
`code` (`specialists.code`, the language specialist: it tells a Next.js TypeScript project
from a Python or Go one), plus `database` when the story
touches schemas or migrations and `ui` for a UI story; `primary` (the generic engine
specialist) when `code` is `unset`. Name no specialist from memory: the line is the project's
choice. Every value `unset` and no `primary`: say "No stack specialist configured"
and go on without one.

## Phase 5: Hand out the work

Hand the implementation to the programmer agent. The brief points at files; never
paste whole documents into it.

- **Objective:** implement [story path] against its acceptance criteria, within its
  Out of Scope boundaries.
- **Sources:**
  1. The story file. It carries the criteria, the boundaries and the QA test cases.
  2. Each TR-ID (`TR-[system]-NNN`) to look up: in
     `docs/architecture/tr-registry.yaml`, the lines matching `id: <TR-ID>\s*$`.
     Its `requirement` text is the source of truth, not text quoted in the story.
  3. The ADR guidance, **inline**: the story's ADR Decision Summary and
     Implementation Notes. Never the ADR path.
  4. The control manifest's [Layer] Layer Rules, by section.
  5. `naming.*` in `project.yaml` and the `perf_budgets` line above.
  6. The test file path from the story's Test Evidence section.
- **Tests,** by `qa.level`, for Logic and Integration stories:
  - `minimal`: "Do not write a test file for this story — test evidence is waived at
    `qa.level: minimal`." Say it: an omitted line and a forgotten one look the same
    to the agent.
  - `standard`: "Write the test at [path] with the code. Each acceptance criterion
    needs at least one test function." Naming per engine from
    `.claude/rules/test-standards.md`. No random seeds, no time-dependent
    assertions, no external I/O.
  - `full`: the same, and "every criterion must be covered: `/saas-story-done` blocks on
    any untested one."
- **Output:** the files created or changed, the test functions written, any
  question or blocker, and whether it finished.
- **Boundaries:** write code only under the resolved code root and tests only under
  the test root. Code root unresolved: write nothing and report it. Touch no file
  outside the story's scope: report the need instead. Doc comments on public APIs.
  An architectural choice the ADR does not cover: report the plan, don't decide it.
  No helper or abstraction for a one-time use, no error handling for cases that
  cannot happen (validate at input and data-file boundaries only), and general logic,
  never a value special-cased so a test passes.

**Say what the brief leaves out, to both readers.** Inputs Phase 2 found absent
(the TR registry, an ADR, the manifest) are left out: tell the agent "No [input] is
passed — it does not exist at this tier; do not go looking for it", and tell the
user one line before handing out: `Briefing omits: [inputs] — implementing against
the acceptance criteria and the [PRD | brief].`

**Then hand the engine check to the specialist** once the programmer reports.
Brief: check the changed files for engine-API use that is wrong or changed in
[engine + version], against `docs/engine-reference/<engine>/`; return a list of
file, line, problem, fix; edit nothing. A problem that breaks a criterion goes back
to the programmer once; the rest go in the summary.

### Recursive Propose–Probe–Compose Mode (`--recursive`)
When invoked as `/saas-dev-story [slug] --recursive` (strongly recommended for Tier-1 mission-critical stories such as auth, billing, and database migrations):
1. **Propose Dual Orthogonal Candidates**:
   - **Candidate A (INV — Invariant Focus)**: Prioritizes defensive validation, strict Zod schemas, explicit HTTP error boundaries, database transaction locks, and sanitization.
   - **Candidate B (DOM — Domain Focus)**: Prioritizes modern idiomatic framework patterns (Next.js 15 Server Actions, Supabase RLS helpers, Stripe v2024 webhooks).
2. **Zero-Token Local Probing**:
   - Run `bash .claude/scripts/ts-parse-check.sh <file>` on both candidates.
   - Check AST parsing and type compliance locally with zero LLM token cost.
3. **Behavioral Composition**:
   - The `lead-engineer` contrasts both rollouts, merges Candidate A's defensive guards with Candidate B's idiomatic ergonomics, and commits the unified solution.

## Phase 6: Check the result

**Did the agent finish?** It stopped early, hit a limit, or its report ends
mid-task: the story is **INCOMPLETE**. Say so as the headline, list what exists,
name the breakage, offer to resume the agent. Never print "Implementation Complete"
over it, and leave the status as it is.

**Did it write what it said?** First verify the artifact: a file the agent's report
names that is not on disk is a failed step, however fluent the report: resume the agent and name the missing
file. A report of BLOCKED, an error, or "cannot complete": say so at once, go no
further past what it blocks, and give a partial report
(`.claude/docs/error-recovery-protocol.md`). Scope too large: split it with
`/saas-create-stories`. The ADR and the story disagree: report the conflict; never guess.

**Is the test there?** At `qa.level: standard` and `full`, for a Logic or Integration
story, look for the file at the Test Evidence path. Missing: at the type's BLOCKING
level on the `gate_level` line, flag "story unverifiable — test required before
`/saas-story-done`"; at ADVISORY, note it as a recommendation. At `minimal` there is
nothing to check: tests are waived.

**Does it parse?** Run the check whose exit code answers it, and report the
command, the exit code and any error lines:

- **Next.js / TypeScript:** run `bash .claude/scripts/ts-parse-check.sh <each changed file>`.
  Exit 1 means a file has syntax or structural parse errors. When `commands.build` or
  `npm run build` is available, optionally run a dry-run check.
- **FastAPI / Python:** run `bash .claude/scripts/ts-parse-check.sh <each changed file>` (uses `python -m py_compile`).
- **Syntax verification:** report `parse VERIFIED` only when `ts-parse-check.sh` exits 0 for all changed files.
  Never infer from reading the code that it parses.

**Run it and look** (`.claude/docs/run-and-observe.md`). For every story a user
can see (every Visual/Feel and UI story, and any other with a surface): navigate
straight to the page, route, or component the story touched, capture a screenshot straight into
`production/qa/evidence/[story-slug]/` (`[story-slug]` is the story file's name
without `.md`; `mkdir -p` the folder first), stamp it with
`bash .claude/scripts/review-receipts.sh hash <each changed file> > production/qa/evidence/[story-slug]/stamp.txt`,
then open the image and compare it with the criteria. Not waived at `qa.level:
minimal`. Report exactly one line, plain text starting `Run result:` (no bold:
`/saas-story-done` reads it as written):

- `Run result: OBSERVED — <what was on screen>` with the retained path;
- `Run result: NOT VERIFIED — <reason>` (no engine, nothing captured); at the
  default gate level this blocks a Visual/Feel or UI story at `/saas-story-done`;
- `Run result: N/A — <reason>` for a story with nothing observable; the reason says
  why nothing is (`/saas-story-done` does not accept "it's a Logic story").

Only the feel half of a Visual/Feel criterion (timing, weight) is DEFERRED to
`/saas-team-qa`: a still cannot show it.

This skill pre-approves `nextjs` on PATH. An engine run through `engine.path` or
the executable `commands.test` names asks first: the user approves it once, or
adds `Bash(<that executable> *)` to `.claude/settings.local.json`.

## Phase 7: Summary, files, checkpoint

```
## Implementation Complete: [title]

**Files changed**:
- `[code root path]` — created / modified ([what])
- `[test path]` — [N] test functions
**Test evidence**: waived at `qa.level: minimal` — no test was required or written   (Logic/Integration at minimal, instead of the test line)
**Verification**: [command] — [exit code and result | parse NOT VERIFIED — <reason>]

**Acceptance criteria**:
- [x] [criterion] — [file:function | test name | OBSERVED in <image path>]
- [ ] [criterion] — DEFERRED: feel, needs a usability test
**Deviations**: [None | files outside scope, an accepted dependency or version risk]
**Engine risks**: [None | the specialist's findings]
**Blockers**: [None | each]
```

At `qa.level: standard` and `full`, add: "Run your test suite and confirm the new
tests pass before `/saas-story-done`: it checks that the test file exists, and runs
nothing." At `minimal` leave that out: there are no tests to run. For a Visual/Feel
or UI story with no retained image, add: "A retained screenshot under
`production/qa/evidence/[story-slug]/` is required before `/saas-story-done`" (and, for
Visual/Feel, the sign-off in `production/qa/evidence/[story-slug]-evidence.md`).

**`## Files`.** Replace the section's body with the list of changed code and test
files, one per line, as the Phase 3 ask said:
`bash .claude/scripts/md-section.sh replace <story> "Files"` with the list on stdin.
A story with no such section: add `## Files` and the list at its end, with a file
edit, never a shell command (a shell write skips the project's write checks). Skip
this when the Phase 3 ask was declined.

**The checkpoint**, on every outcome. Pipe the block to
`bash .claude/scripts/session-state.sh checkpoint`, which replaces the old one:

```
**Updated:** [date]
**Branch:** `[current git branch]`
**Current task:** /saas-dev-story — [story path] ([title])
**Next step:** [the Next step below]
**Blocked on:** [nothing, or the blocker]
**Files in progress:** [changed files, comma-separated]
**Run result:** [OBSERVED — … | NOT VERIFIED — … | N/A — …, as in the closing block: /saas-story-done reads it here]
**Open questions:** [none, or one line each]
```

**The run's last reply ends with this block**, the only place the `Run result:` line
is printed: print it nowhere else in the reply. The Next step goes by the tier you stated in Phase 1 (the `workflow` line,
never `rigor` or `qa.level`). The Next step: at `minimal`, `/saas-story-done [path]`. At `standard` and `full`,
`/saas-code-review [files]`, then `/saas-story-done [path]`. INCOMPLETE: `/saas-dev-story [path]`
to resume. BLOCKED: the action that unblocks it (`/saas-architecture-decision accept
ADR-NNNN`, the dependency to finish, the diff to review).

```
Story: [path] — [Implemented | INCOMPLETE — <breakage> | BLOCKED — <reason>]
Run result: [OBSERVED — … | NOT VERIFIED — … | N/A — …]
Next step: [Implemented, Tier: workflow minimal → /saas-story-done [path] | Implemented, Tier: workflow standard or full → /saas-code-review [changed files], then /saas-story-done [path] | INCOMPLETE → /saas-dev-story [path] to resume | BLOCKED → the unblocking action]
```
