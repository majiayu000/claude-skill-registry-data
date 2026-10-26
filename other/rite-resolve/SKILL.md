---
name: rite-resolve
description: User-invoked resume verb for answering, dropping, or batch-resolving open `questions.md` gates.
argument-hint: "<qid> \"<answer>\"  |  --drop <qid> [\"<reason>\"]  |  --batch <plain-text-file>"
user-invocable: true
disable-model-invocation: true
---
<!-- loads: {"always":["devrites-lib/reference/standards/core.md","rite-resolve/reference/answer-protocol.md"],"triggers":{"standards":["devrites-lib/reference/standards/afk-hitl.md","devrites-lib/reference/standards/documentation.md"]},"rootOnly":["devrites-lib/reference/standards/afk-hitl.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --skill rite-resolve` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.

# /rite-resolve: answer the human gate

`/rite-resolve` resumes an **async** human gate: a checkpoint that already paused and
**stopped the session** (an AFK blocking/escalating/irreversible queue, or a HITL pause
left unanswered), plus `--batch`. When `/rite-build` asks a question **inline**
via `AskUserQuestion` and the human is present, that pick resolves the gate **in place** through
the `devrites-engine state resolve` writer. You don't type `/rite-resolve` for it. For the async case this
skill takes the human's answer (or `--drop` / `--batch`), writes it to `questions.md`, updates
`state.md` (clears `Awaiting human`, sets `Status: running`), and recommends the next command.

It has one verb, one source of truth (`questions.md`), and one cursor (`state.md`). The
full AFK / HITL contract lives in
[`afk-hitl.md`](../devrites-lib/reference/standards/afk-hitl.md).

## Rules consulted (read on demand from `.claude/skills/devrites-lib/reference/standards/`)

Pull these via `Read` when shaping the resolve:

- [`afk-hitl.md`](../devrites-lib/reference/standards/afk-hitl.md): gate taxonomy, `questions.md` schema, AFK exception rules.
- [`documentation.md`](../devrites-lib/reference/standards/documentation.md): record decisions and rationale where the answer changes scope.

## Operating rules

- **Requires an active workspace.** Read `.devrites/ACTIVE` first; if empty, **STOP** and
  tell the user to run `/rite-spec <feature>` first. If the slug has no `questions.md`,
  report the missing required artifact and stop.
- **One mutation per call.** A single qid (or `--batch` file) per invocation; never
  silently coalesce multiple human decisions into one log entry.
- **Never overwrite an answered question.** If the qid's `status` is `answered` or
  `dropped`, refuse with the existing answer; ask the user to open a new qid that
  references the old one (the file is the audit trail).
- **If the answer materially changes scope, architecture, or acceptance**, route it
  through the Spec Drift Guard (`/rite-plan repair`) **after** writing the answer: do
  not modify `spec.md` / `plan.md` inside this skill.
- **The script is the source of truth.** Always invoke
  `devrites-engine state resolve`. It keeps `questions.md` + `state.md` consistent and emits the
  next-action recommendation. The one `state.md` field this skill may write by hand is the
  unblocked slice's `Slice mode` (step 4, the named exception); everything else goes through
  the script, never by hand.
- **Human gates are for human-only decisions, not the agent's work.** A `questions.md` entry the
  human must answer is a genuine decision (a scope / design / risk call only the human can make),
  not a task the agent can do. If a question is really agent-doable ("should I write the
  test?", "go implement X"), do not record a human answer that returns the agent's work to it:
  flag the mis-tag and route it to the right skill (`/rite-build`, `/rite-plan unblock`,
  `devrites-debug-recovery`). The human resolves decisions; the agent does the work.

## Workflow

0. **Read `.claude/skills/devrites-lib/reference/standards/core.md`** (operating rules + persistence discipline) before
   touching the workspace.
   Then read the explicit or active workspace's `state.md` directly.
1. **Parse arguments.** `$ARGUMENTS` is one of:
   - `<qid> "<answer>"`: answer the single open question.
   - `--drop <qid>` (optional `"<reason>"`): mark the question `dropped`; record
     the reason inline.
   - `--batch <plain-text-file>`: bulk resolve, one entry per qid (see
     [`reference/answer-protocol.md`](reference/answer-protocol.md) for the batch
     format).
2. **Load context.** Read `state.md`, `questions.md`, and the relevant slice from
   `tasks.md`. Confirm the qid is `status: open`. If `state.md` `Status` is not
   `awaiting_human` and the question's `gate` is `blocking`, surface the inconsistency
   before proceeding (don't auto-repair: flag it).
3. **Apply explicit consent.** Supplying `<qid> "<answer>"`, `--drop`, or `--batch` is the
   user's explicit consent for this local workspace mutation. Echo the qid, answer/drop,
   and slice being unblocked, then continue immediately; do not ask the user to confirm the
   command they just typed.
4. **Mutate.** Run `devrites-engine state resolve --human` with those arguments (a human is resolving). It:
   - flips the qid's `status` to `answered` / `dropped` and stamps `answered_at` + `answer` + `answered_by: human`;
   - if the qid is in `state.md`'s `Awaiting human` block (single-question pause), clears
     that block and sets `Status: running`;
   - appends a `Log` line to `state.md`.

   **Writer failure:** command not found or nonzero exit → STOP. Do not hand-edit
   `Slice mode`, `questions.md`, or `state.md`; report the exact command, its exit code,
   and the decisive stderr line, and recommend `/rite-doctor`. Both files stay as the
   writer left them.
   **Completion:** zero exit, or the failure reported with no hand edit.

   On resume, and only after a zero exit, also clear or update the unblocked slice's `Slice mode` in `state.md`: if
   the answer lets the slice proceed, drop the pause-time `Slice mode` so `/rite-build`
   re-derives it on the next selection; if the answer re-shapes how the slice should be
   built, set `Slice mode` to match.
5. **Post-resolve hand-off.** If the answer changes product behavior or acceptance →
   recommend `/rite-plan repair`. Otherwise → recommend the slice's natural next action
   (typically `/rite-build` for the slice that was awaiting).
   **Completion:** the resolved state contains exactly one next command.
6. **STOP.** User-invoked `/rite-resolve` does not run `/rite-build` itself: the
   user re-enters the workflow explicitly. A controlling `/rite-autocomplete`
   caller invokes the same `devrites-engine state resolve` writer internally (never with `--human`) and
   continues; it must not emit this skill as a user handoff for a question that
   already names a ranked recommended option.

> **Mid-flight discipline.** Don't edit `spec.md` / `plan.md` to "incorporate" the
> answer. That's `/rite-plan repair`. Don't silently retry a build after the answer
> lands: the user types the next command. Don't merge two open questions into one
> answered entry: each question is independently auditable.
