---
name: bug-stub
category: planning
model: claude-haiku-5-5
userInvocable: true
description: Turn a free-text bug description into a paste-ready ticket stub — a short title and a one-paragraph summary — with no code discovery, no fix, and no commit. Use right after finding a bug, before any tracker ticket exists, to get text you can file yourself and then feed into no-ticket requirements gathering.
argument-hint: "<bug description>"
allowed-tools: "AskUserQuestion"
---

# Bug Stub

Arguments: $ARGUMENTS

## Purpose

You just found a bug. There's no ticket for it yet, and you don't want to
stop and write one by hand. This command turns your free-text description
into a title and summary you can paste into your own tracker (Jira, Linear,
GitHub Issues, whatever you use) — nothing more.

**This command does not investigate the bug.** It performs no code
discovery, proposes no fix, and makes no commit. If you want the
bug actually investigated and fixed, use `/troubleshoot` instead — that
command reads the codebase and reasons about root cause. This one only
reshapes what you already told it.

## Process

### Step 1: Parse the description

Same parse shape as `/troubleshoot`'s Phase 1 — this command borrows only
that step, not anything past it. Extract from `$ARGUMENTS` (or ask if
$ARGUMENTS is empty):

- **What:** What component/endpoint/feature is broken?
- **Expected:** What should happen?
- **Actual:** What actually happens?
- **Repro:** Steps to reproduce, if given.

If `$ARGUMENTS` is empty or too thin to extract these, use AskUserQuestion
to ask for a one- or two-sentence description before continuing. Do not
guess at missing details — an invented "expected" or "actual" would make
the stub actively misleading to whoever files it.

### Step 2: Generate the stub

Produce exactly two pieces of text:

- **Title** — 80 characters or fewer, no markdown formatting (no backticks,
  no bold, no headers — plain text a tracker's title field will accept
  as-is). Describe the observable symptom, not the fix.
- **Summary** — one paragraph covering what was expected, what actually
  happened, and how to reproduce it. No headers, no bullet list —
  a single paragraph, since it is meant to be pasted as a ticket
  description, not rendered as a mini-document.

Print both, clearly labeled:

```
Title:
{title}

Summary:
{summary}
```

### Step 3: Offer the handoff (output chaining)

Offer — do **not** auto-run:

> Stub ready. Want me to start requirements gathering from it? →
> `/create-requirements --no-ticket`
> Otherwise, copy the title/summary above into your tracker.

Only invoke another skill on explicit confirmation. If confirmed, print a
handoff banner naming the exact next command and **stop** (same shape as
`/meeting`'s `/epic` handoff — never invoke the next skill directly):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Handing off to /create-requirements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:   {title}
Summary: {summary}

Next: run /create-requirements --no-ticket "{title}: {summary}"
No ticket number needed yet — a provisional draft session is created, and
you can reconcile it with a real ticket later once one exists.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The stub text is directly usable as that command's input — no
reformatting needed between what this command prints and what
`--no-ticket` expects as a feature description.

Then **stop**. Do not run any further steps — `/create-requirements` takes
over when the user runs it.
