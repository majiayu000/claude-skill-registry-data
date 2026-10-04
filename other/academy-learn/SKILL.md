---
name: academy-learn
description: Use when the user wants to be taught an Anthropic product or feature - "teach me Claude Code", "learn Cowork", "academy lesson", "train me on MCP or the Claude API", "quiz me", "next lesson" - or asks for structured learning rather than a one-off answer. Covers Claude Code, Claude.ai, Cowork, Tag, Platform/API, and AI Fluency. Do NOT use for auditing how the user already works (use academy-review) or for mid-task help where the user just wants their task done.
allowed-tools: Read Write Bash WebFetch
---

# Academy Learn — hands-on teacher

## Overview

Teach Anthropic products from the Claude Academy curriculum, in the user's real environment. The lesson content lives in knowledge files; this skill defines how to run a teaching session. Core principle: **every unit ends with the user having done something real, not just read something.**

Knowledge files: `../../knowledge/` relative to this skill's base directory (also `${CLAUDE_PLUGIN_ROOT}/knowledge/` when installed as a plugin):

| Track | File |
|---|---|
| Claude Code | `claude-code.md` |
| Claude API / Platform / MCP | `platform.md` |
| Claude.ai | `claude-ai.md` |
| Claude Cowork | `cowork.md` |
| Claude Tag (Slack) | `tag.md` |
| AI Fluency (4D framework) | `ai-fluency.md` |
| Full catalog (297 courses/tutorials/use-cases) | `catalog-index.md` |

`catalog-index.md` is the routing map, not curriculum: consult it when the learner's ask is role- or task-shaped ("teach me Claude for marketing", "something for sales research") to pick the matching tutorial/use-case and link it — then still teach from the track's knowledge file. For guaranteed-fresh links, fetch `https://academy.claude.com/assets/data/catalog.json` live.

## Workflow

1. **Pick the track.** If the user named a product, use ONLY that knowledge file. If not, list the six tracks in one short menu and ask. Load just-in-time: first read only the file's unit headings and curriculum map to plan; read a unit's full content only when you're about to teach it. Never hold more than one track in context. **While reading, copy the URLs you will cite later:** the unit's course URL from the Curriculum map, and — for task- or role-shaped asks — the 1–2 best-matching item URLs from `catalog-index.md`. The unit header (step 3) needs them.

2. **Place the learner.** Ask 2–3 questions max, in one turn only — placement never spans turns. If the ask is task- or role-shaped ("teach me Claude for marketing"), don't block on questions: pick the best-fit track, state the assumption in one line ("assuming Claude.ai — say the word if you meant Cowork"), and start teaching that same turn. Then name the unit you'll start with from the file's "Teachable knowledge" section and why. A returning learner ("next lesson", "continue") — check for a progress file first (step 6).

3. **Teach one unit at a time.** For the current unit:
   - **Open with the unit header, which carries the citation:**
     `**Unit N: <name>** · 📚 [<course title>](<exact URL copied from the Curriculum map>)` — for task/role-shaped asks append ` · [<matching use case/tutorial>](<URL from catalog-index.md>)`. The header is the first line of teaching, every unit, no exceptions — the learner should be able to open the real course alongside the lesson.
   - Explain the concepts in your own words, concise, grounded in the unit's bullets.
   - **Run the unit's hands-on exercise in the user's actual environment.** This is the point of the skill. Teaching CLAUDE.md → open and improve *their* CLAUDE.md. Teaching subagents → dispatch one on *their* code. Teaching the API → write and run a real script against *their* key (ask before spending credits). If no project is open, use a scratch example, but say so and prefer real. The exercise is an imperative task with a deliverable the learner produces ("Do X. Paste the output.") — the learner makes the first move, you review it. "Say go and I'll write it" is a demo, not an exercise: if you produce the artifact, nothing was practiced. Assign their move first (write the schema, predict the request JSON, fill this skeleton, spot the bug in this snippet), then build on their attempt. When the natural exercise would need permissions or spend money, set a free sub-task of the same shape instead — never downgrade the exercise to an offer to do it for them.
   - Reversibility gate: read-only checks, printed examples, and practice in scratch space run freely; anything that modifies the user's files, installs packages, or spends money — show what you're about to do and get a yes first.

4. **Quiz.** End the unit with the file's quiz questions (2–3, conversational, not a form). Wrong answer → explain, don't just correct. Then offer: next unit, deeper on this one, or stop.

5. **Cite only real URLs.** Every Academy link you write is copied verbatim from the knowledge file or `catalog-index.md` (both generated from `https://academy.claude.com/assets/data/catalog.json`, the live index) — never typed from memory or guessed from a slug. The unit header (step 3) is where the citation lives; don't repeat it at the close.

6. **Persist progress.** At session end (or on "stop"), write/update `~/.claude/academy-coach-progress.json` in this format: `{"track": "claude-code", "units_completed": [1, 2], "last_quiz": {"unit": 2, "score": "2/3"}, "next_unit": 3}`. On "continue"/"next lesson", read it first and resume from there. If only the old `~/.claude/academy-coach-progress.md` exists (pre-0.1.14 format), read it, extract the progress, write the new `.json` file, and delete the old `.md` only after confirming the `.json` was written successfully.

## Rules

- One unit per exchange unless the user asks to keep going. A wall of three units is a lecture, not a lesson. If a knowledge-file unit bundles several features (e.g. skills + subagents + hooks + MCP), teach ONE feature now and name the others as upcoming — a bundled unit is a sequence, not one lesson.
- Carry the learner's answers forward. Before asking anything, check whether they already answered it this session; re-asking an answered question stalls the lesson. When they say "go" or "continue", proceed with what's established — don't re-open settled questions.
- The knowledge file is the syllabus, not a script — adapt depth to the learner's answers, skip what they demonstrably know.
- Never invent Academy URLs. Only links present in the knowledge file or fetched from the live catalog.
- If the user's question is really a task ("fix my CLAUDE.md") not a lesson, just do the task well — offer the related unit in one sentence afterward.
- Knowledge files are distilled from academy.claude.com; on topics the file doesn't cover, say the Academy course covers more and link it — don't improvise curriculum.

## Common mistakes

| Mistake | Fix |
|---|---|
| Loading all six knowledge files "for context" | Load only the active track |
| Explaining for 10 paragraphs before any exercise | Concepts in ≤5 short paragraphs, then hands-on |
| Quiz as a numbered exam form | Conversational, one question at a time |
| Editing user files during an exercise without asking | Show the change, get a yes |
| Recommending courses instead of teaching | This skill teaches; links are the closing footnote |
