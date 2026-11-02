---
name: learner-profile-teach
description: Personalized teaching companion for the existing teach skill. Use for learning, teaching, course design, next lesson, research derivation, electromagnetic computation, code engineering, tool integration, planning, decision-making, cognition, emotion regulation, and Chinese teaching intents such as 教我, 教会我, 带我学, 学一下, 讲一下, 给我上一课, 继续上一课, 帮我理解. Syncs the stable learner profile from Obsidian before reading profile references, adapts teach-skill lessons to the learner, records self-explanation evidence, and proposes stable profile updates only after review.
---

# Learner Profile Teach

Use this skill as the personalization layer around `teach`. It supplies the
stable learner model; `teach` manages the current course workspace; Obsidian
stores durable notes, concept cards, derivations, review evidence, Bases views,
and profile update proposals.

## Loading Workflow

At the start of a learning, teaching, research-derivation, or cognition/planning
task:

1. Run the Obsidian profile sync script:
   ```bash
   cd ~/.codex/skills/learner-profile-teach
   python3 scripts/sync_learner_profile.py
   ```
2. If sync returns `STATUS=low` or exits nonzero, stop before teaching and ask
   the user to resolve the reported issue.
3. Read `references/global-profile.md`.
4. Read `references/teaching-protocol.md` for lessons, courses, next lesson, or
   teaching requests.
5. Read `references/research-workflow.md` for research, derivation,
   engineering, implementation, validation, or tool-integration work.
6. Read `references/cognition-and-planning.md` for planning, future direction,
   decision-making, emotion regulation, or cognitive improvement.
7. Read the current teach workspace state when available.
8. Use current user messages as the highest-priority signal when they conflict
   with older profile notes.

Load only references relevant to the task. Do not load every reference by
default.

## Obsidian Integration

When a task writes durable learning material, use the Obsidian integration
references as needed:

- Read `references/obsidian-integration.md` for vault layout and artifact split.
- Read `references/obsidian-properties-schema.md` before writing Obsidian notes.
- Read `references/obsidian-linking-policy.md` before writing lesson, concept,
  derivation, review, or profile-proposal notes.
- Read `references/obsidian-bases.md` when creating, repairing, or querying
  `.base` files.
- Read `references/obsidian-cli-protocol.md` when using the `obsidian` CLI.
- Read `references/validation.md` before declaring Obsidian work complete.
- Read `references/gotchas.md` when sync, CLI, Bases, or profile-update behavior
  looks surprising.

Prefer bundled scripts for repeatable Obsidian operations:

```bash
python3 scripts/write_obsidian_note.py --help
python3 scripts/generate_learning_bases.py --help
python3 scripts/generate_learning_canvas.py --help
python3 scripts/validate_obsidian_learning_system.py --help
python3 scripts/install_or_repair.py --help
```

## Lesson Protocol

For substantial lessons, follow `references/teaching-protocol.md`.

End substantial lessons by asking the user to:

1. Explain the core concept in their own words.
2. Transfer it to one research, engineering, management, planning, or life
   scenario.
3. Name one unclear, uncertain, or disputable point.

Use the answer to identify knowledge boundaries, learning pace, interest
signals, and difficulty patterns. Keep ordinary lesson outcomes in the teach
workspace and Obsidian; do not immediately update the stable profile.

## Five-Lesson Review

Do not update the stable learner profile after every lesson.

After every five substantial lessons in a course or learning thread:

1. Read `references/update-protocol.md`.
2. Use `templates/five-lesson-review.md`.
3. Inspect the last five lesson notes, learning records, Obsidian notes, and
   user self-explanations.
4. Decide whether stable, cross-course evidence warrants a profile update.
5. If yes, draft `templates/profile-update-proposal.md` into the Obsidian source
   `Self/learner-profile/proposals/`.
6. Ask the user to confirm before editing stable profile files.

No silent profile updates. Profile updates require explicit user confirmation
unless the user directly asks to write a specific update.
