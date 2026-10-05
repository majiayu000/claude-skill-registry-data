---
name: handoff
description: Use when ending or pausing a Claude Code session whose work must continue in a fresh session — user says "create a handoff", "write a handoff", "I'm ending this session", "prepare for a fresh session", "hand this off", or "/handoff" — or when starting a session in a project that already contains a HANDOFF.md at the root ("resume", "pick up where we left off", "continue from the handoff"). Also relevant when a session shows degradation symptoms — Claude contradicted an earlier decision, re-explored something already established, hallucinated file contents, or the user says the session "feels off", "is getting confused", or "context is running low".
---

# Handoff

## Overview

Write (or resume from) a `HANDOFF.md` at the project root so a fresh Claude Code session can continue this work **without repeating dead ends**. The file is written for the next Claude session, not for the human.

**Core principle: this skill runs when your memory is least reliable. Nothing goes in the file from memory alone — every claim is verified against the repo NOW, or explicitly marked as unverified.**

## Mode selection

- `HANDOFF.md` exists at project root AND this session did NOT just write it → **RESUME mode**
- Otherwise → **CREATE mode**

## Proactive suggestion rule

If you notice degradation (you contradicted an earlier decision, re-derived something already settled, misremembered a file), say ONE sentence — *"This session may be degrading (⟨specific symptom⟩). Want me to run /handoff so a fresh session picks up cleanly?"* — and STOP. Never write the file without confirmation.

## CREATE mode

### Step 1 — Archive any existing handoff

If `HANDOFF.md` exists at root:
1. Read its **Failed approaches** and **Known traps** sections. Carry forward entries still relevant and unresolved — re-tagged `[?]` unless re-verified in Step 2.
2. Move the file to `.handoffs/<ISO-timestamp>-handoff.md` (create the directory if needed).
3. If a `.gitignore` exists and lacks `.handoffs/`, add it.

### Step 2 — Verify BEFORE writing (anti-hallucination protocol)

Do this before drafting a single line. The rule: **a claim may be tagged `[V]` only if confirmed by a command or file read during THIS handoff run.** What you merely remember is `[?]`.

1. **Orient in reality.** Git repo: run `git status`, `git log --oneline -15`, `git diff --stat`. No git: list the directories you believe you touched and re-read those files. Reconstruct what actually changed vs. what you believe changed.
2. **Re-read, don't recall.** Re-open every file the handoff will mention. Any quoted code or line number must come from the fresh read. File not where memory says? That's a caught hallucination — correct it, don't paper over it.
3. **Re-run ground truth.** Run the project's test/build/lint command. "Tests pass" is written only from output produced in this run — otherwise it's `[?]`.
4. **No invention.** Can't verify it and don't clearly remember it? Omit it. An honest gap beats confident fiction.
5. If many claims end up `[?]`, write at the top: "Low-confidence handoff — verify aggressively."

### Step 3 — Write HANDOFF.md

Copy `assets/HANDOFF.template.md` structure exactly. Fill every section; the template's HTML comments show what a good vs. useless entry looks like — read them, then delete them from the output.

**Length budget: target ≤250 lines (~2,000 words); hard ceiling 400 lines.** The handoff must fit in a fresh context alongside CLAUDE.md and initial exploration. Over budget? Cut in this order: drop narrative prose → compress Decisions to one line each → NEVER cut Failed approaches, Known traps, Verified state, or Next steps.

**Quality gate — apply to every entry before keeping it:** *"Would a stranger with only this line avoid the mistake we made?"* If not, add the file, the line, the reason, or delete the entry.

## RESUME mode

1. **Read HANDOFF.md fully** before doing any other work.
2. **Re-verify — the file may be stale or was written by a degraded model.** Run `git log`/`git status`/`git diff` against the SHA in the header; re-run the tests. Confirm each `[V]` claim still holds; resolve `[?]` claims if cheap. Report drift explicitly: "handoff said X, repo now shows Y."
3. **Surface the Open questions** to the user. Do not guess past a blocked step.
4. **Confirm the plan.** Restate next steps adjusted for drift; get a go-ahead.
5. **Proceed.** Leave HANDOFF.md in place — the next CREATE run archives it.

## Rationalizations — all of these mean STOP

| Excuse | Reality |
|---|---|
| "I remember the session clearly, no need to re-verify" | This skill runs precisely because memory is degraded. Verify or tag `[?]`. |
| "Tests were passing earlier" | Earlier ≠ now. Re-run them or write `[?]`. |
| "A summary is enough — 'fixed several bugs'" | A stranger can't avoid a dead end from a summary. Which bug, which file, which failed approach first. |
| "Context is nearly full, skip verification to save tokens" | An unverified handoff poisons the NEXT session too. Verification is the non-negotiable part; cut prose instead. |
| "The old handoff is outdated, just delete it" | Archive it. Its dead-ends section may be the only record of what not to retry. |
| "I'll pad thin sections so the file looks complete" | Invention is worse than a gap. Write "not started, no design chosen" honestly. |
| "The user is in a hurry — auto-run the handoff" | Suggest, never auto-execute. One sentence, then stop. |

## Red flags — catch yourself

- Writing a file path or line number you didn't re-read this run
- Typing "tests pass" without test output in this run's transcript
- An entry with no file reference and no specific reason
- HANDOFF.md creeping past 400 lines
- Resuming work without having re-run verification against the header SHA
