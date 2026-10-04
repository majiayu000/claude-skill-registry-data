---
description: Write an end-of-session recap to .claude/last-session.md. Triggered by /wrap, "wrap up", "recap this session", or automatically by the Stop hook via the .claude/.wrap-pending marker.
disable-model-invocation: true
allowed-tools: Read Write Edit Bash
---

You are the `/wrap` skill. Write a session recap that survives to the next session.

## Triggers

- Slash form: `/wrap`
- Natural language: "wrap up", "recap this session", "let's call it"
- Retroactive (via SessionStart): if `.claude/.wrap-pending` exists from a previous session

## Mode A: Live invocation (end of current session)

### Step 1: Substantive-check

Briefly assess whether this session covered substantive work. If you've made fewer than ~3 file edits or git operations, ask the user:

> "You've only just started — are you sure you want to wrap up? There's not much to recap yet."

Continue only on confirmation.

### Step 2: Draft the recap

Compose a recap from your conversation context using this format exactly:

`# Last session — <YYYY-MM-DD>`

Then sections:

`## What we did` — 2-4 bullets of substantive work, not micro-steps.

`## Decisions made` — any "from now on" / "we chose X over Y" moments — even unsaved ones.

`## In flight` — anything unfinished, with enough context to resume.

`## Next time, start with` — one concrete next action.

### Step 3: Show the draft

Present the recap to the user for approval:

> "Here's the recap I'll save. Look right? (yes / edits)"

Apply edits if requested. Re-show if substantial changes were made.

### Step 4: Save

Write `.claude/last-session.md`, overwriting any previous recap.

### Step 5: Offer to save "from now on" decisions

If the recap's "Decisions made" section contains any "from now on" / "always X" lines that aren't already in CLAUDE.md's Preferences, offer one by one:

> "I noticed you decided '<decision>' during this session. Want me to remember that across future sessions too?"

On yes, invoke the `/remember` skill with that decision text. On no, move on.

### Step 6: Confirm

> "Recap saved. You'll see 'Where we left off' at the start of your next session."

## Mode B: Retroactive (called from SessionStart hook detecting .wrap-pending)

### Step 1: Read the marker

`.claude/.wrap-pending` is a key=value file:

`SESSION_END=<unix-timestamp>`
`SUBSTANTIVE_TURNS=<integer>`
`FILES_TOUCHED=<comma-separated paths>`

### Step 2: Ask the user

> "Last session ended without a recap. It had <N> substantive turns. Want me to put together a quick summary based on the git activity? (yes / no / skip forever)"

- yes → continue to Step 3.
- no → delete `.claude/.wrap-pending`; move on.
- skip forever → write a flag to `.claude/onboarding-log.md` so future SessionStart hooks know not to offer retroactive recaps; delete `.wrap-pending`.

### Step 3: Reconstruct context from git

Run:
- `git log --since="<SESSION_END timestamp minus a few hours>" --pretty=format:'%h %s'`
- `git diff --stat <commit-before-SESSION_END>..HEAD` (best-effort)

Use the FILES_TOUCHED list and commit messages to draft the same recap format as Mode A. Be explicit about uncertainty: prefix any inferred bullets with "Probably: ".

### Step 4: Show and save

Same as Mode A Steps 3-6. After saving, delete `.claude/.wrap-pending`.

## Edge cases

- **Stop hook fired but user opens new session days later.** SESSION_END timestamp shows. Surface the age: "Last session ended 4 days ago." Let the user decide whether to bother reconstructing.
- **`.claude/last-session.md` already has a recap newer than `.wrap-pending`.** Delete `.wrap-pending` silently; do nothing.
- **Force-quit detected (no SESSION_END).** Treat as zero substantive turns; do nothing.
