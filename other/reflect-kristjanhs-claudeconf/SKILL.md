---
name: reflect
description: ONLY on /reflect or retro step 4. Propose skill improvements.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion
---

# Reflect Skill

Analyze the current session and propose improvements to skills based on what worked, what didn't, and edge cases discovered.

## Trigger

Run `/reflect` or `/reflect [skill-name]` after a session where you used a skill.

Additional commands:
- `/reflect on` - Enable automatic end-of-session reflection
- `/reflect off` - Disable automatic reflection
- `/reflect status` - Check if auto-reflect is enabled

## Workflow

### Step 1: Identify the Skill

If skill name not provided, ask:

```
Which skill should I analyze this session for?
- frontend-design
- code-reviewer
- [other]
```

### Step 2: Analyze the Conversation

Look for these signals in the current conversation:

#### Corrections (HIGH confidence):
- User said "no", "not like that", "I meant..."
- User explicitly corrected output
- User asked for changes immediately after generation

#### Successes (MEDIUM confidence):
- User said "perfect", "great", "yes", "exactly"
- User accepted output without modification
- User built on top of the output

#### Edge Cases (MEDIUM confidence):
- Questions the skill didn't anticipate
- Scenarios requiring workarounds
- Features user asked for that weren't covered

#### Preferences (accumulate over sessions):
- Repeated patterns in user choices
- Style preferences shown implicitly
- Tool/framework preferences

### Step 3: Propose Changes

Present findings using accessible colors (WCAG AA 4.5:1 contrast ratio):

```
┌─ Skill Reflection: [skill-name] ───────────────────┐
│                                                    │
│ Signals: X corrections, Y successes                │
│                                                    │
│ Proposed changes:                                  │
│                                                    │
│ 🔴 [HIGH] + Add constraint: "[specific constraint]"│
│ 🟡 [MED]  + Add preference: "[specific preference]"│
│ 🔵 [LOW]  ~ Note for review: "[observation]"       │
│                                                    │
│ Commit: "[skill]: [summary of changes]"            │
│                                                    │
└────────────────────────────────────────────────────┘

Apply these changes? [Y/n] or describe tweaks
```

#### User Response Options:
- `Y` – Apply changes + integrate surrounding instructions, then commit locally (user pushes from host)
- `n` – Skip this update
- Or describe any tweaks to the proposed changes

### Step 4: If Approved

1. Read the current skill file at its **canonical dotfiles path** (`~/projects/dotfiles/skills/[skill-name]/SKILL.md`) — CLAUDE.md § Dotfile symlink discipline.
2. Apply the changes using the Edit tool.
3. **Integrate — no contradictions left behind.** Before committing, sweep the surrounding instructions (other steps in the file; numbering/range references like "Steps 2–4"; silence/close/scope notes;
   and **every other file that names the changed behaviour** — `grep` the concept)
   and update them in the same burst so nothing now contradicts, double-counts, or dangles against the edit.
   Full discipline → `~/.claude/references/skills-management.md` §"Integrate Every Edit". A partial edit that leaves a contradiction is a defect.
4. Commit locally (dotfiles repo): `git -C ~/projects/dotfiles add … && git -C ~/projects/dotfiles commit -m "[skill]: [change summary]"`. **Do NOT `git push` from the session** — the user pushes dotfiles from the host (CLAUDE.md "Git push credentials").
5. Confirm: "Skill updated + committed to dotfiles — push from host when ready."

### Step 5: If Declined

Drop it. If it must survive the session, stage it as a `type: feedback` memory file — that layer already has a drain (a later `/retro` graduates it into its target once that target is reachable). Never open a per-skill observations log: nothing reads it, nothing prunes it, and no admission rule governs it.

## Toggle Commands

### `/reflect on`

Enable automatic end-of-session reflection:
1. Create/update `~/.claude/reflect-skill-state.json` with `{"enabled": true, "updatedAt": "[timestamp]"}`
2. Confirm: "Auto-reflect enabled. Sessions will be analyzed automatically when you stop."

### `/reflect off`

Disable automatic reflection:
1. Update `~/.claude/reflect-skill-state.json` with `{"enabled": false, "updatedAt": "[timestamp]"}`
2. Confirm: "Auto-reflect disabled. Use /reflect manually to analyze sessions."

### `/reflect status`

Check current status:
1. Read `~/.claude/reflect-skill-state.json`
2. Report: "Auto-reflect is [enabled/disabled]" with last updated timestamp

**Note:** The state file is saved in the global Claude user directory (`~/.claude/`) so it persists across plugin upgrades.

## Important Notes

- Always show the exact changes before applying
- Never modify skills without explicit user approval
- Every applied change integrates with its surroundings — no contradictions left behind (Step 4.3)
- Commit messages should be concise and descriptive
- Commit locally; the user pushes dotfiles from the host (never `git push` from the session)