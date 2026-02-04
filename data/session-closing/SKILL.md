---
name: session-closing
description: End-of-session ritual. Reflect while context is rich, then seal. Triggers on /close, 'wrap up', 'let's finish', or context nearly full. Pairs with /open and /close. (user)
---

# /close

Capture learnings while context is rich, then commit and exit.

## Structure

```
Gather  → todos, beads, git, drift
Orient  → reflect (AskUserQuestion)
Decide  → crystallize actions from reflections (STOP — must present before executing)
Act     → execute, handoff, commit
```

---

## Pre-flight: Return Home (MANDATORY)

You may have `cd`'d during work. Your system prompt contains `Working directory: /path/...` in the `<env>` block — this is immutable, where the session actually started.

1. Extract that exact path from your system prompt
2. Run: `~/.claude/skills/session-management/scripts/check-home.sh "/that/path"`
3. If `CD_REQUIRED=true`, run `cd <HOME_DIR>` immediately

**Do not skip. Do not trust pwd. Do not reason about whether you moved back. The script is authoritative.**

---

## 1. Gather

Check session state:

- **TodoWrite** — what's done, what's incomplete?
- **Beads** — any in_progress? Should they close or get notes?
- **Git** — uncommitted files? Unpushed commits?
- **Drift** — what did /open (or /ground) say we'd do vs what we did?

Surface stale artifacts: screenshots, temp files, old sketches, superseded plans.

---

## 2. Orient

Reflection via AskUserQuestion — user selection creates genuine engagement:

```
AskUserQuestion([
  {
    header: "Looking Back",
    question: "Which backward reflections should I answer?",
    multiSelect: true,
    options: [
      { label: "All of these", description: "Full retrospective" },
      { label: "What did we forget?", description: "Dropped intentions" },
      { label: "What did we miss?", description: "Blind spots" },
      { label: "What could we have done better?", description: "Quality gaps" }
    ]
  },
  {
    header: "Looking Ahead",
    question: "Which forward reflections should I answer?",
    multiSelect: true,
    options: [
      { label: "All of these", description: "Full prospective" },
      { label: "What could go wrong?", description: "Risks, fragile bits" },
      { label: "What won't make sense later?", description: "Clarity gaps" },
      { label: "What will we wish we'd done?", description: "Missed opportunities" }
    ]
  }
])
```

Respond to selected questions genuinely — the selection makes them real asks, not template following.

Don't rush this. The reflection is where value compounds.

---

## 3. Decide

**STOP.** Do not proceed to Act without completing this phase.

From Gather + Orient, crystallize actions into two buckets:

```
AskUserQuestion([
  {
    header: "Do Now",
    question: "Which need current context?",
    multiSelect: true,
    options: [
      // Actions that benefit from current session context:
      { label: "Close bead-xyz with resolution", description: "Have context for good notes" },
      { label: "Document X in CLAUDE.md", description: "Details fresh in mind" },
      { label: "None", description: "Nothing needs doing now" }
    ]
  },
  {
    header: "File for Later",
    question: "Which should become beads?",
    multiSelect: true,
    options: [
      // Work that matters but doesn't need current context:
      { label: "Glossary quality pass", description: "Needs dedicated session" },
      { label: "Refactor Y", description: "Fresh thinking required" },
      { label: "None", description: "Handoff captures everything" }
    ]
  }
])
```

**Do Now** = needs current context (closing beads with good notes, documenting while fresh)
**File for Later** = matters but can wait (create bead with title, defer to future session)

User gets explicit choice over timing. "Not now" ≠ abandoned.

---

## 4. Act

Execute in order:

### 4a. Execute "Now" items
Do the selected quick fixes, close beads, create beads.

### 4b. Reflect dialogue
Share what stood out:
> "What stood out to me this session:
> - [specific observation]
> - [pattern or connection]
>
> What do you think?"

Be discursive if user engages. This is the learning capture.

### 4c. Write handoff
Path: `~/.claude/handoffs/-{PROJECT_PATH}/{timestamp}.md`

```markdown
# Handoff — {DATE}

## Done
- [Completions in verb form]

## Gotchas
[What would trip up next Claude]

## Risks
[What could go wrong with what we built]

## Next
[Direction for next session]

## Commands
```bash
# Optional — verification or continuation that might help
```

## Reflection
**Claude observed:** [What stood out]
**User said:** [Their response]
```

### 4d. Commit
If git dirty:
- Stage relevant files (including handoff)
- Commit with standard message + co-authorship
- Push if user approves

### 4e. Exit
Session complete.

---

## Mirrors

| Phase | /open | /ground | /close |
|-------|-------|---------|--------|
| Gather | Handoff, beads, script | Todos, beads, drift | Todos, beads, git, drift |
| Orient | "Where we left off" | "What's drifted" | Reflect (AskUserQuestion) |
| Decide | User picks direction | Continue or adjust | Crystallize actions (STOP) |
| Act | Draw-down → TodoWrite | Update beads, reset | Execute, handoff, commit |
