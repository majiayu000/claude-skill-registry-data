---
name: skill-reflect
description: Capture a friction log immediately after finishing a skill session — what was improvised, what the user corrected, what edge cases the skill missed, and what changes would help. Writes a structured session log to ~/.claude/skill-sessions/<plugin>/sessions/<skill-name>/ so it can be read by the evolver from the skills repo later. Works in any project, not just the skills repo. Use whenever you've just finished running a skill and want to capture what happened while the session is fresh. Triggers on "/skill-reflect", "reflect on this session", "log this session", "write a session log", "capture skill friction", or any phrase asking to record what happened during a skill run.
version: 0.1.1
---

# Skill Reflect

You run immediately after a skill session ends. Your job is to mine the conversation that just happened, extract the friction points, and write a structured log to disk so the evolver can read it later. The session is still in context — use it.

---

## Phase 1: Resolve the skill

The user invokes this as `/skill-reflect <skill-name>` (e.g., `/skill-reflect qa`). If they didn't provide a skill name, ask: "Which skill should I write a session log for?"

Once you have the name, find its owning plugin. Try scanning the working directory first (works if you're in the skills repo):

```bash
ls -d plugins/*/skills/<skill-name>/ 2>/dev/null
```

- **One match** — record the plugin name (the second path segment, e.g. `plugins/<plugin>/skills/...`).
- **Multiple matches** — ask the user to qualify: "I found `<skill-name>` in both `<plugin-a>` and `<plugin-b>` — which one? (e.g., `<plugin-a>/skill-name`)"
- **No match** — before asking the user, check whether you're in the skills repo on the wrong branch: run `git branch --show-current`. If `plugins/` exists but the scan found nothing, the skill's plugin may live on an unmerged branch — switch to the correct branch and re-scan. Only if the branch check doesn't resolve it, ask: "Which plugin does `<skill-name>` belong to? (`delivery`, `writing`, `track`, or `meta`)" and use their answer as the plugin name.

---

## Phase 2: Reflect on the session

Review the current conversation — the skill run is still in context. Work through each of the four questions below. Be specific: quote or paraphrase actual moments from the conversation rather than speaking in generalities. A vague log is useless to the evolver.

### 2.1 What did you have to improvise?

Look for steps you added on the fly that weren't instructed by the SKILL.md — decisions you made without a written rule to follow, phases you invented, tools you reached for that the skill didn't mention. Improvisation is a signal the SKILL.md has a gap.

*Hint: scan for moments where you reasoned "I'll also…", "it makes sense to…", or added a step that wasn't in a numbered phase.*

### 2.2 What did the user correct?

Look for explicit corrections, redirections, and pushback: "no", "wait", "actually", "that's not right", "don't do that", or any message where the user steered you away from what you were doing. Each correction is a place where the skill's instructions were unclear, missing, or wrong.

### 2.3 What edge cases came up that the skill didn't anticipate?

Look for situations you had to navigate that the SKILL.md didn't prepare you for — ambiguous inputs, missing context, unusual project state, dependencies the skill assumed existed but didn't, questions you had to ask that a better-written skill would have answered upfront.

### 2.4 What specific changes would help?

Based on the above, propose concrete improvements to the SKILL.md. Be specific about what would change: a new step in a phase, a clarification to an existing instruction, a fallback for an edge case, a new question to ask upfront. Vague suggestions ("improve the instructions") are not useful — name the section and describe the change.

---

## Phase 3: Write the log

Get the current timestamp:

```bash
date -u +"%Y-%m-%dT%H-%M"
```

Create the directory and write the log:

```bash
mkdir -p ~/.claude/skill-sessions/<plugin>/sessions/<skill-name>
```

Write to `~/.claude/skill-sessions/<plugin>/sessions/<skill-name>/<timestamp>.md` using this exact structure:

```markdown
---
skill: <skill-name>
plugin: <plugin>
date: <YYYY-MM-DD>
session_summary: <one sentence describing what was done in this session>
---

## What I had to improvise

<your findings from 2.1, or "Nothing notable." if clean>

## User corrections

<your findings from 2.2, or "No corrections." if clean>

## Edge cases not anticipated

<your findings from 2.3, or "None encountered." if clean>

## Proposed improvements

<your findings from 2.4, or "No changes recommended." if clean>
```

If all four sections are empty (a clean run with no friction), still write the log — a record of clean sessions is signal too.

---

## Phase 4: Confirm

Tell the user:

1. The full path of the file written.
2. The single most actionable friction point from this session, in one sentence. If the session was clean, say so.

Example:
> Session log written to `~/.claude/skill-sessions/delivery/sessions/qa/2026-06-04T14-32.md`.
> Top friction: the skill didn't handle the case where no Linear issue could be inferred from the branch name — Claude had to ask, and a fallback prompt should be in Phase 0.

---

## What to skip

- Don't modify the SKILL.md itself — that's the evolver's job, not yours.
- Don't summarize the whole session — focus on friction, not narrative.
- Don't be diplomatic. If the skill's instructions were unclear, say so plainly.
