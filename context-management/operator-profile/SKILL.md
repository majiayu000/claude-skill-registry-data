---
skill_id: operator-profile
name: Operator Profile
description: "Learn and apply how the operator works — operator preference, working style, communication preference, \"remember my preference\", \"I prefer\", \"don't do that again\", \"that's not how I work\". Read at session start, updated at session end."
version: 1.0.0
category: operator-profile
office: All (cross-office)
lead_agent: behavioral-designer
triggers:
  - operator preference
  - working style
  - communication preference
  - remember my preference
  - I prefer
  - don't do that again
  - that's not how I work
collaborates_with:
  - behavioral-designer
  - session-memory
  - memory-palace
---

# Operator Profile — Personalization Intelligence

> Office: All (cross-office, always active)
> Source: NousResearch/hermes-agent Honcho architecture
> Purpose: Build a deepening model of the operator across sessions

## Purpose

Models the operator's identity, working style, preferences, and rejected patterns. Every Maxim session reads the profile at start and updates it at end. The operator profile is what makes Maxim feel like it knows you — not just knows its domain.

## File Locations

| File | Path | Purpose | Update Frequency |
|---|---|---|---|
| OPERATOR.md | `.mxm-operator-profile/OPERATOR.md` | Master identity: name, role, expertise, goals | On change |
| preferences.md | `.mxm-operator-profile/preferences.md` | Output format, verbosity, tool preferences | Every session |
| rejected-patterns.md | `.mxm-operator-profile/rejected-patterns.md` | Patterns operator has corrected or rejected | Append-only |
| communication-style.md | `.mxm-operator-profile/communication-style.md` | How operator phrases requests, response format | Every session |

## Session Start Protocol

When any session begins (after session-memory loads):

1. Read `.mxm-operator-profile/OPERATOR.md` — load identity and expertise
2. Read `.mxm-operator-profile/preferences.md` — load output preferences
3. Read `.mxm-operator-profile/rejected-patterns.md` — load what NOT to do
4. Apply personalization silently — do not announce "I read your profile"

## Session End Protocol

When any session ends (after session-memory writes):

1. Review the session for preference signals:
   - Did the operator correct an output format? → Update preferences.md
   - Did the operator reject an approach? → Append to rejected-patterns.md
   - Did the operator express a new preference? → Update preferences.md
   - Did the operator share new context about themselves? → Update OPERATOR.md
2. Write updates to the relevant file(s)
3. If MemPalace is available: store preference facts in `maxim/operator` room
4. If claude-mem is available: preferences get persisted via claude-mem automatically

## Preference Signal Detection

Watch for these patterns during any session:

| Signal | Example | Action |
|---|---|---|
| Explicit correction | "No, I want it shorter" | Update preferences.md |
| Rejection | "Don't do that again" | Append to rejected-patterns.md |
| Style preference | "I prefer tables over lists" | Update preferences.md |
| Format preference | "Always use markdown headers" | Update preferences.md |
| Expertise signal | "I've been doing this for 10 years" | Update OPERATOR.md |
| Tool preference | "Use Python, not Node" | Update preferences.md |
| Pace preference | "Move faster, skip explanations" | Update communication-style.md |

## Rules

1. **Never delete** from rejected-patterns.md — only append
2. **Never announce** profile reads — apply silently
3. **Never override** explicit session instructions with profile preferences
4. **Always update** at session end if any preference signal detected
5. **Profile is per-project** — `.mxm-operator-profile/` lives in each project folder
6. **Profile is gitignored** — personal preferences are not committed

## Integration with Other Skills

| Skill | Integration |
|---|---|
| session-memory | Operator profile update runs AFTER session memory writes |
| memory-palace | Preference facts stored in MemPalace `maxim/operator` room |
| behavioral-designer | Reads profile to apply personalized behavioral science |
| content-creation | Reads communication-style.md for tone matching |
| engineering | Reads preferences.md for code style preferences |

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
