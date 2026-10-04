---
name: sdlc-check
description: Invoked explicitly by /check. Reports whether the input a phase needs is good enough to start, without doing the phase's work. Names every missing or unclear item by file, section and the role that normally answers it. Use it at a handoff, before picking up someone else's document.
argument-hint: "<phase> [FEAT-ID]"
disable-model-invocation: true
---

# /check — is this input good enough to start?

The handoff command. A Tech Lead picking up a PO's PRD runs `/check srs PTK-001` and
finds out in one screen whether the PRD can support an SRS, and exactly what is missing
if it cannot — **without generating anything.**

## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.

> Read-only. Skip gate Step 4 (CHECKPOINT), and skip gate Step 2.7 — running the input
> check *is* this skill's job, so it runs it directly in Step 2 rather than as an entry
> condition.

---

## Step 1 — Resolve what to check

`<phase>` is one of `framework.yaml` → `input_contracts` keys: `intake`, `prd`, `srs`,
`techdocs`, `code`, `testcases`, `unit`, `acceptance`, `review`.

Accept the command name as an alias — `/check /srs`, `/check srs` and `/check sdlc-srs`
all mean the same phase. People think in commands, not phase ids.

With no `FEAT-ID`, use `active_feature` from `current.yaml`. With no phase, report the
readiness of **every** phase whose source documents exist — a one-screen answer to "where
is this feature actually blocked", which is often the real question.

## Step 2 — Run the input check

Follow `.agent/steps/input-check.md` in full, including Step 6 (record the gaps in the
source document's open-questions table and, for blocking gaps, in `findings.tsv`).

Recording matters more here than anywhere else. `/check` is run at a handoff, and a
handoff is exactly the moment when the answer needs to survive the terminal being closed
and reach the person who owns it.

## Step 3 — Report

Print the readiness report from `input-check.md` Step 5, then add:

```
  Owner of this phase        : {owner_role}
  Owner of the input document: {owner_role of the producing phase}

  Blocking gaps by role:
    PO/BA      2   R2 success signal, R6 unanswered question Q3
    Tech Lead  0

  Verdict: NOT_READY — 2 blocking gaps, both owned by PO/BA.
  Hand back to the PO with the two questions above, or answer them in
  docs/prd/PRD-PTK-001-summarizer.md and re-run.
```

The by-role grouping is the point. It answers the question a person actually has at a
handoff — *"is this mine to fix, or do I hand it back?"* — without making them read the
whole document.

## Step 4 — Do not fix anything

`/check` reads and reports. It never edits a document to close a gap, never generates the
phase's output, and never asks a question interactively.

Recording gaps into the source's open-questions table (input-check Step 6) is additive
and is not a fix: it appends questions marked `[auto]`, and never touches a line a person
wrote.

---

## Also useful for

- **Before a handoff.** The PO runs `/check srs PTK-001` before telling the Tech Lead the
  PRD is ready, and closes the gaps first. Cheaper than a round trip.
- **Picking up a stalled feature.** `/check` with no phase shows every phase's readiness
  at once, so you can see where it actually stopped rather than guessing from the last
  command someone ran.
- **A document written entirely outside the framework.** Someone wrote an SRS in an editor
  and pasted it into `docs/srs/`. `/check techdocs` says whether it holds up, with no
  requirement that `/srs` ever ran.

## Boundaries

- Never generate the phase's output. That is the phase's command.
- Never mark a gap resolved. Only the person who edits the document does that.
- Never report `READY` for a requirement you could not evaluate. Report it as `unclear`
  and say why — a readiness check that overstates readiness is worse than none, because
  the next phase then fails further downstream where the cause is harder to see.
