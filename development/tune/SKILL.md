---
name: tune
description: >-
  Harness retro — turn recurring agent mistakes into one-line fixes. Mines
  recent session transcripts (plus the bugfix log and past runs) for
  repeated corrections, permission friction, and rules that get violated
  anyway, then proposes ranked changes one at a time: a CLAUDE.md rule, an
  allowlist entry, a script replacing repeated prose, a new-skill
  candidate, or a deletion that no longer earns its context cost. Nothing
  applies without approval; accepted/rejected findings persist in
  out/tune/learnings.md. Use when the user says "/tune", "improve my
  setup", "why does claude keep doing X", or after a frustrating session.
  done's one-line retro catches one lesson at ship time; tune is the
  periodic audit of the whole harness.
---

# tune — the harness retro

`/tune` — audit the current project's harness against recent sessions
`/tune all` — widen across every project under `~/.claude/projects/`

Answer one question: **what keeps going wrong across sessions, and what
one-line change would make it impossible next time?** Correcting the agent
fixes one session; correcting the harness fixes every session after it.
The evidence is already on disk — the transcripts recorded every
correction, every retyped instruction, every permission prompt. This skill
reads them so the user doesn't repeat them.

## Step 0 — Scope, then inventory

**Scope:** default is the current project's transcripts — the last ~10
sessions or 2 weeks, whichever is smaller — from
`~/.claude/projects/<project-dir>/*.jsonl` (the dir name is the project
path with `/` → `-`). `/tune all` widens to every project; mining gets
shallower per project, say so.

**Inventory the harness first** — findings only mean something against the
baseline. Read: user + project `CLAUDE.md`, the installed skills (names +
descriptions), `settings.json` / `settings.local.json` (permissions,
hooks). Also read `out/tune/learnings.md` (past accepted/rejected — don't
re-propose what was rejected), `out/tune/principles.md` if present
(promoted cross-cutting principles — a lens for judging new findings),
and `out/dev/bugfix-log.md` if present (recurring root causes are harness
findings too).

## Step 1 — Mine the transcripts (cheap models, parallel)

Bulk transcript reading is a job for a **cheap model, not the frontier
one** — spawn the miners with `model: haiku`, one per evidence stream,
concurrently:

- **Corrections:** user messages that correct, redo, or undo the agent's
  work — especially the same correction phrased across different sessions.
  The strongest signal there is.
- **Friction:** permission prompts approved again and again, commands the
  user retypes, tool errors hit repeatedly (a broken alias, a missing
  binary, a path that's always wrong the first time).
- **Ignored rules:** places where a `CLAUDE.md` rule already exists and
  the transcript shows it being violated anyway — prose that failed needs
  a mechanism, not more prose.
- **Re-derived procedures:** multi-step sequences the agent works out from
  scratch in session after session — candidates for a script or a skill.
- **Dead weight:** rules and skills that never once became relevant in the
  mined window.

Each miner returns findings as: **what happened, quoted transcript lines,
session dates, occurrence count.** Full evidence goes to
`out/tune/.work/<stream>.md`; rank from the files, not the summaries.

## Step 2 — Cross-reference and rank

- **Two-strike rule:** a mistake made once is noise; twice is a pattern.
  No proposal from a single occurrence — park it in learnings.md as
  "watching" instead.
- **Check against the inventory:** if a rule already covers the finding
  and was ignored, the proposal escalates to a stronger mechanism (script,
  allowlist, hook) — never a second sentence saying the same thing.
- **Rank by cost:** occurrences × disruption. A correction retyped five
  times outranks an elegant refactor of the rules file.
- **Deletions rank alongside additions.** A bloated CLAUDE.md degrades the
  agent — every rule costs context in every session. A rule whose incident
  class has disappeared is a finding. Name the class a cut falls into:
  **Conflict** (two layers pulling opposite ways — quote both sides),
  **Duplicate** (keep the copy nearest its point of use), **Obvious**
  (restates what the code or the model's defaults already show),
  **Judgement-now** (a blanket worst-case rule a current model calls better
  from context), or the vanished incident class above — first match in that
  order wins. A line that fits none is a **Gotcha** — load-bearing; it
  survives this run.

## Step 3 — Propose, one at a time

Present findings **one at a time, highest impact first** — evidence
(quoted, dated), the proposed change as an **exact diff or text**, where
it goes, and the **one-line principle** the finding generalizes to: the
transferable "why" that would prevent the whole incident class, not just
this instance. The user approves, rejects, or edits each before the next
is shown. Apply only on an explicit yes.

The escalation ladder — always the *weakest mechanism that will actually
work*:

1. **CLAUDE.md rule** — for a two-strike mistake prose can prevent. One
   line, imperative, specific.
2. **Permission allowlist entry** — for a safe command prompted repeatedly.
3. **Script replacing prose** — for a procedure the agent re-derives; a
   deterministic script is cheaper and can't be misremembered.
4. **Hook** — only for must-never-happen actions; prose cannot block, hooks
   can.
5. **New-skill candidate** — when a CLAUDE.md section has grown into a
   procedure; sketch the skill, don't build it unbidden.
6. **Deletion** — of a rule, hook, or skill that no longer earns its cost.

**Prove the rules bite** — for the mechanical rungs (allowlist, script,
hook), applying isn't done: with the change in place, inject the exact
violation it exists to catch, observe the block or failure, revert the
injection, observe green again. A config that doesn't fail on its violation
is a no-op wearing a diff.

After the session, update `out/tune/learnings.md`:

```markdown
| Date | Finding | Proposal | Principle | Verdict | Provenance |
|------|---------|----------|-----------|---------|------------|
| 2026-07-06 | `cat` fails (bat alias), 4 sessions | rule: use Read tool, never cat | prefer harness tools over shell equivalents | accepted | sessions 06-28→07-03 |
| 2026-07-06 | user rejects auto-PR-body edits | (rejected — user prefers manual) | — | rejected | — |
```

The **Provenance** column is what makes rules retire-able: a future run
that sees the incident class gone can propose the deletion.

**Promote recurring principles.** When two or more *accepted* rows — from
this run or any earlier one — share a principle (the same idea, not
necessarily the same words) that isn't already in `out/tune/principles.md`,
propose adding it there: the two-strike rule applied one level up, with
the same explicit-yes gate as every other change:

```markdown
- Prefer harness tools over shell equivalents — findings 2026-07-06, 2026-07-14
```

One line per principle, each citing the findings that earned it. Future
runs read the file in Step 0 and weigh new findings against it; sessions
that author or rewrite skills and rules read it as a pre-write checklist.
A principle retires only when its **incident class** has vanished —
pruning its source rows from learnings.md is housekeeping, not evidence —
and retire-ability applies one level up too. Keep the file under ~15
lines: a principles file too long to skim is a rules file wearing a new
name.

## Guardrails

- **Nothing applied without an explicit yes.** This skill edits the user's
  configuration — the one place "just do it" is never acceptable.
- **Evidence or it isn't a finding.** Every proposal carries quoted
  transcript lines with dates; "I noticed you often..." without a quote is
  not presented.
- **Deletions as readily as additions.** A run that only ever adds rules is
  doing it wrong.
- **Privacy is structural.** Transcripts stay local; quotes land only in
  `out/tune/` files — ensure that path is gitignored (quotes come from the
  user's private sessions) — and are never sent anywhere.
- **learnings.md stays under ~100 lines.** Prune resolved entries oldest
  first; it's a steering file the next run reads, not an archive.
- **Respect the ladder.** Reaching for a hook when a rule would do adds
  rigidity; adding a rule when a script would do adds context cost. The
  weakest sufficient mechanism wins.
