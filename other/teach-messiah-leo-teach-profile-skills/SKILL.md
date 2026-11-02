---
name: teach
description: Teach the user a new skill or concept in a stateful workspace. Use for "teach me", "help me learn", lessons, courses, next lesson, learning plans, study workflows, 教我, 教会我, 带我学, 学一下, 讲一下, 给我上一课, 继续上一课. When learner-profile-teach is installed, use it first for Obsidian learner-profile sync and personalization, then manage the course workspace, lessons, records, references, and Obsidian mirrored notes.
---

# Teach

The user has asked to learn something over one or more sessions. Treat the
current directory as the course workspace.

## Companion Profile

When `learner-profile-teach` is installed, use it before substantial teaching:

1. Run its Obsidian profile sync workflow.
2. Read the relevant learner-profile references.
3. Return here to manage the course workspace and lesson artifacts.

If the companion skill is unavailable, continue with `teach` and say that
personalized profile sync was skipped.

## Teaching Workspace

Maintain these files and folders as needed:

- `MISSION.md`: why the user is learning this topic. Use
  `MISSION-FORMAT.md`.
- `RESOURCES.md`: trusted sources and communities. Use
  `RESOURCES-FORMAT.md`.
- `learning-records/*.md`: decision-grade learning records. Use
  `LEARNING-RECORD-FORMAT.md`.
- `lessons/*.html`: self-contained lesson artifacts.
- `reference/*.html`: durable reference documents, cheat sheets, algorithms, or
  glossaries.
- `NOTES.md`: local course notes and teaching preferences.

## Obsidian Mirror Rule

Obsidian is part of the deliverable when the user asks to record lessons,
thoughts, derivations, course progress, concept cards, or review evidence. Use
the configured vault from the companion profile skill, an explicit user path, or
a local `~/Documents/Coffers` vault when it exists.

Use the Obsidian integration references from `learner-profile-teach` when
available:

- `references/obsidian-properties-schema.md`
- `references/obsidian-linking-policy.md`
- `references/obsidian-cli-protocol.md`
- `references/obsidian-bases.md`
- `references/validation.md`

Write course material under the vault's `Skills/` folder unless the user
specifies another vault path or topic folder. Keep Obsidian notes recall-
oriented: concise headings, key definitions, small examples, self-test
questions, and links to course/concept/proposal evidence. Verify written notes
with `obsidian` CLI when available.

## Teaching Method

Tie every lesson to the mission. If the mission is unclear, interview the user
before writing `MISSION.md`.

For substantial lessons:

1. Teach one tightly scoped concept or skill.
2. Use trusted resources before relying on memory.
3. Explain the minimal terminology, definition, common confusion, small example,
   domain transfer, and practice loop.
4. Build storage strength with retrieval, spacing, and interleaving where useful.
5. Ask for the user's self-explanation and use it to decide whether to correct,
   deepen, or move on.

## Reference Documents

Create reference documents for durable reusable knowledge, not for session logs.
Glossaries are canonical language for the workspace; add a term only once the
user can use it correctly.

## Boundaries

Do not let lessons become loose motivational summaries. Do not record mere
coverage as learning. Do not silently change the mission or the stable learner
profile. Confirm meaningful mission changes and leave profile updates to the
companion profile workflow.
