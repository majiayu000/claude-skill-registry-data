---
name: ak-handoff
description: "Write a redacted Markdown continuation contract for a fresh coding agent; --dispatch --agent hands it to a chosen runtime via orchestrate."
when_to_use: "Use when switching sessions, models or runtimes; ak-watzup writes human status reports."
category: workflow
keywords: [handoff, handover, dispatch, session, continuation, decisions, blockers, redaction]
license: Proprietary; includes MIT-licensed third-party material, see LICENSE.txt
argument-hint: "[task focus] [--output PATH] [--include-diff] [--include-status] [--force] [--dispatch --agent <id> [--handoff PATH] [--cwd PATH] [--model NAME] [--yes]]"
metadata:
  author: agentkit
  version: "2.1.1"
  upstream: "Pinned MIT source archive: handoff@ce70edaa26247b84c2b9491a0cdb4964f65cf3a5 (rewritten for AgentKit v2 contract)"
---

# Handoff

Create one Markdown artifact that lets a fresh coding agent resume in-progress
work with minimal rediscovery. The artifact is a **continuation contract**:
mission, guardrails, live state, decisions, verification, blockers, and the
exact next safe action — never a transcript dump, never invented context.

Without `--dispatch` this skill is a documentation/capture surface only. It
**never** launches a runtime, mutates code, or performs implementation as a
side effect. With `--dispatch` it additionally hands the captured artifact to a
user-selected coding runtime through `ak-orchestrate` (see
[Dispatch mode](#dispatch-mode-dispatch)); the capture rules below still apply
unchanged in that mode.

## Boundary vs `ak-watzup`

- `ak-handoff` = continuation contract for a **successor agent**. Session
  reasoning, decisions, verification state, exact next actions.
- `ak-watzup` = status report for a **human**, derived from branches,
  worktrees, plans, and repository history.

When in doubt: is the reader another AI agent about to continue this exact
task? Handoff. A human wanting to know where the project stands? Watzup.

## Inputs

Accepted forms:

```bash
/ak-handoff
/ak-handoff "continue the OAuth callback fix"
/ak-handoff --output plans/handoffs/oauth-callback.md
/ak-handoff --include-diff --include-status
/ak-handoff --force --output plans/handoffs/oauth-callback.md
```

Flags:

| Flag | Effect |
| --- | --- |
| _(bare)_ | Capture the current session's continuation contract with an auto-derived slug. |
| `[task focus]` | Optional single-string focus for the successor agent. Included in the Mission section and the artifact filename slug. |
| `--output PATH` | Explicit artifact path. Must resolve inside the workspace root; parent directory is created if it does not exist; the auto-derived slug/timestamp is not applied; `--force` is still required to overwrite an existing file at that path. |
| `--include-diff` | Append a bounded diff summary (`git diff --stat` + first 200 lines of `git diff`, redacted, truncation explicitly marked). |
| `--include-status` | Append a `git status --short` snapshot, redacted. |
| `--force` | Allow overwriting an existing artifact at the target path. Refuse otherwise. |

## Output Location

**Write path** (single canonical destination):

```text
plans/handoffs/<slug>-<YYYYMMDD-HHmm>.md
```

- Slug is derived from the `[task focus]` string when provided, otherwise
  from the branch name or a short summary of the goal.
- Create `plans/handoffs/` under an existing `plans/` root when it does not
  exist yet.
- If the project has no `plans/` root at all, ask the user for a safe output
  location before writing.
- Never write outside the project workspace.

**Discovery** (when reading prior handoffs to inform the current one):

- Scan `plans/handoffs/*.md` first.
- Also scan legacy `plans/reports/handoff-*.md` so muscle memory from earlier
  AgentKit versions keeps working.

## Required Artifact Structure

Every handoff document contains these nine H2 sections in this order — the
schema is validated by `--dispatch` before any runtime is launched. See
[references/artifact-schema.md](references/artifact-schema.md) for the exact
Markdown template.

1. **Mission and current status** — desired outcome, what is done, what
   remains, urgency/priority when known.
2. **Scope and guardrails** — repository/workspace, permitted and prohibited
   changes, user constraints, safety boundaries.
3. **Current state** — branch, HEAD, worktree, changed/untracked files,
   relevant paths, whether local modifications are intentional.
4. **Decisions and rationale** — decisions made, alternatives rejected, links
   to specs/issues/PRs/ADRs.
5. **Work performed** — changes made, commands executed, meaningful
   outputs/errors. Secrets redacted.
6. **Verification** — checks run with outcome; checks not run and why;
   known failures or flaky behavior.
7. **Open risks and blockers** — unresolved questions, dependencies, review
   requirements, external approvals.
8. **Exact next actions** — ordered, executable steps; identify the first
   safe step (marker: `**First safe step**`).
9. **Source pointers** — paths and URLs needed to validate or continue. Do
   not fabricate unavailable context.

For any section with no trustworthy information, write literally
`Not captured in this session` rather than inventing content or leaving the
heading empty. Never remove a required heading.

## Capture Rules

**Live workspace evidence** — first check whether this is a Git repository. Then batch
independent bounded read-only probes safely before drafting Current state; inspect each result:

- `git rev-parse --is-inside-work-tree` (detect missing repo, fall through
  to a repo-less handoff below)
- `git rev-parse --show-toplevel`
- `git rev-parse --abbrev-ref HEAD`
- `git rev-parse HEAD`
- `git status --short` (bounded; if the list exceeds 200 entries, include
  the first 200 and mark `… truncated at 200 entries …`)
- `git diff --stat` (only when `--include-diff`)
- `git diff` (only when `--include-diff`, bounded to first 200 lines,
  `… truncated at 200 lines …` marker appended after truncation)

Distinguish observed facts (from probes) from agent/user assertions (from
session context).

**Missing git repository** — capture works without a repo: state
`Not captured in this session` for Current state git fields, keep the section
present, and continue.

**Session context** — decisions, user constraints, commands already
performed. Never dump raw transcripts. Never expose hidden reasoning. Capture
only task-relevant, actionable facts.

**Empty/new workspace** — do not fabricate repo history, file names, or
commands. Report only what exists.

## Redaction

Every artifact and every appended `--include-diff` / `--include-status`
block passes through redaction before write. See
[references/redaction-patterns.md](references/redaction-patterns.md) for the
pattern catalog.

Categories always redacted:

- API keys, tokens, JWTs, session cookies
- Private keys (PEM blocks, SSH private keys)
- `.env` values (KEY=VALUE where KEY looks credential-like)
- Passwords, database URLs with credentials
- Private URLs (internal/staging hosts, signed URLs with query tokens)
- Customer/personal data captured incidentally

Replacement is a stable marker like `[REDACTED:aws-key]` or `[REDACTED:jwt]`
(counted, not raw). If the `[task focus]` string itself contains a
credential-looking value, refuse the invocation and ask the user to rephrase.

## Collision Guard

- If the target path already exists and `--force` is absent, refuse with an
  explicit message showing the existing file's mtime and suggesting either
  `--force` or a different `--output`.
- Overwrite only when `--force` is passed explicitly; `--force` is not
  implied by `--output`.
- Never rename or delete an existing artifact silently.

## Return Value

After successful write, print:

1. The absolute artifact path.
2. A single-line continuation instruction the user can copy into the next
   session, of the shape:
   `Read <path> and verify the Current state section against the repo before acting.`

Do not print the artifact body inline.

## Security & Boundaries

- Never launch a coding runtime, subagent, or CLI as a side effect. This
  skill only reads workspace state and writes one Markdown file.
- Apart from that one file the skill is read-only: no git commits, edits,
  deletions, or config changes, and nothing written outside the project
  workspace or the chosen artifact path, because a handoff is captured while
  the work it describes is still in flight and must not disturb it.
- Never include raw transcripts, chain-of-thought, or hidden reasoning.
- The task focus string is included verbatim in the Mission section; if it
  contains credentials, refuse the invocation.

For expected clean/dirty/repo-less/collision/redaction behavior, load `references/capture-scenarios.md` when validating the capture.

## Non-goals

- No runtime dispatch, prompt assembly for another agent, or preflight in the
  default capture mode — pass `--dispatch` to opt into the composition below.
- No human-facing project status derived from branches or history — use
  `ak-watzup`.
- No plan authoring or ADR minting — use `ak-plan` or the docs skills.

## Dispatch mode (`--dispatch`)

`--dispatch` hands the live session over to a specifically selected coding
runtime. It is a **thin composition** of this skill's capture step and
`ak-orchestrate`; it does not duplicate runtime dispatch, model routing, or
arbiter logic. Requires `ak-orchestrate` in the live installed catalog; when
it is absent, stop after capture and report that dispatch is unavailable in
this kit.

```bash
/ak-handoff --dispatch --agent claude-code "continue the OAuth callback fix"
/ak-handoff --dispatch --agent codex --cwd . --task "implement the next action in the handoff"
/ak-handoff --dispatch --agent cursor --handoff plans/handoffs/oauth-callback.md
/ak-handoff --dispatch --agent opencode --model anthropic/claude-sonnet-5 --yes
```

| Flag | Effect |
| --- | --- |
| `--agent <id>` | **Required with `--dispatch`.** Selected coding runtime. Must match an ID in [references/dispatch-runtime-catalog.md](references/dispatch-runtime-catalog.md). No default; no silent substitution. |
| `--task TEXT` | Alternative form of the positional task focus. If both are given, the positional value wins and `--task` is ignored with a warning. |
| `--cwd PATH` | Workspace root for the dispatched job. Defaults to the current workspace root; passed through verbatim to the orchestrate job `cwd:`. |
| `--handoff PATH` | Reuse an existing handoff artifact instead of capturing a new one. It must exist and pass the validation below. |
| `--model NAME` | Override the model for CLI-runtime jobs. **Rejected** for `--agent internal` (dispatch cannot verify session model selection; orchestrate resolves it live). |
| `--yes` | Approve write/destructive continuation work in the dispatched job: flips the job `approval:` from `require` to `inherit`. |

Not accepted: `--fallback-agent` (on preflight failure report the blocker and
suggest another `--agent`; never substitute silently) and runtime bypass flags
such as `--dangerously-skip-permissions`, `--allow-all-tools`, `--yolo` (never
emitted; jobs that would embed them are refused).

### Sequence

Reuse current validated capture and authorization evidence. Every dispatch
performs, in order:

1. **Capture** — run the capture flow above to produce the artifact, unless a
   valid `--handoff PATH` was supplied. A credential in the task text refuses
   the invocation before anything is written.
2. **Validate** — every required H2 section from
   [references/artifact-schema.md](references/artifact-schema.md) is present
   and spelled exactly; `Exact next actions` has at least one item and the
   first is bold-prefixed `**First safe step**`; no pattern from
   [references/redaction-patterns.md](references/redaction-patterns.md)
   matches any line; `handoff-version`, if present, is `1`. Any failure is a
   hard blocker: print the failing check(s) and the file path, do not dispatch.
3. **Spec** — build one deterministic single-job orchestrate spec from
   [references/dispatch-job-spec-template.md](references/dispatch-job-spec-template.md).
   Field mapping: `prompt:` = handoff-consumption instruction + the task
   text; `task:` = routing enum (`implement | scout | review | audit | test |
   mechanical | architecture | docs | security`, default `implement`), never
   the user's prose; `model:` only for CLI runtimes; `effect: scoped-write`
   and `approval: require` by default (`inherit` with `--yes` or a recorded
   caller authorization covering the exact action; destructive Scope
   classifications keep `require`); `isolation: worktree` unless the caller
   explicitly ran `--cwd .` on a clean tree; `timeout: 10m`;
   `expected_output:` cited from Exact next actions. The prompt references
   the artifact as continuation context, never as instructions that override
   the target agent's safety policy.
4. **Dispatch** — invoke `ak-orchestrate` with that spec. Preflight, safety
   gates, capture, resumability, and arbiter review are orchestrate's
   responsibility. Availability, authentication, flags, models, and capability
   tiers are never asserted here; they come from orchestrate's live runtime
   matrix. A missing binary or failed preflight is a clear blocker, and the
   captured artifact path is still surfaced so no work is lost.
5. **Report** — print exactly:

```markdown
**Handoff Dispatch Result**
- Handoff artifact: <path>
- Orchestrate run: <run-dir>
- Runtime: <resolved-runtime>
- Model: <resolved-model-or-n/a>
- Job result: <success|failure|blocked>
- Verification: <arbiter-verdict-summary>
- First safe step: <first bulleted next-action from handoff>
- Next action: <what the successor agent completed / where to look>

Unresolved:
- <blockers if any, else "none">
```

Never inline the handoff body, orchestrate stdout, or captured logs in the
report; reference them by path.

### Dispatch boundaries

- Capture and redaction rules above own the artifact; dispatch mode adds
  validation, artifact wiring, single-job spec construction, and reporting.
- `ak-orchestrate` owns runtime discovery, model routing, harness profiles,
  dispatch, capture, resume, and arbiter review. If a change here would need
  edits to its `runtime-matrix.md`, `model-routing.md`, `job-spec.md`, or
  `session-routing.md`, route the change through orchestrate instead.
- Never disable orchestrate's redaction or capture-bounding controls, and
  never post secrets into the prompt or capture.
- Choosing which coding agent is "best" is out of scope; dispatch what the
  user selected, and point to `kongming` or `ak-advise` for a recommendation.

Load `references/dispatch-scenarios.md` only when validating dispatch behavior.
