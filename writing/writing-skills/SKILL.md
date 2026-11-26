---
name: writing-skills
description: >-
  Writes or tightens a Claude Code skill: short description, tight steps, tested triggers. Use when the user asks to create, write, improve or shrink a SKILL.md or a project skill, or says a skill never fires. Not for using a skill.
license: Apache-2.0
metadata:
  level: "meta"
  uses: ""
  agents: ""
  tokens: "703"
---

Writes a skill that is short, fires when it should, and changes behaviour the model would not show unaided. Draft, test, then keep.

## Steps
1. *Always.* Ask whether a skill is the right layer: a one-sentence fact goes to a CLAUDE.md line, a mechanical rule to a hook, a path-bound rule to `.claude/rules/`. A skill is for a repeated multi-step procedure or a method. Say which layer and why.
2. Read what is there: existing skills' names and descriptions (collisions), the CLAUDE.md contract. For a rewrite, read the whole source skill first and keep every line that changes behaviour.
3. Draft `.claude/skills/<name>/SKILL.md` (kebab-case name = folder). Frontmatter: `name`, `description`, optional `license`; add `disable-model-invocation: true` only for skills with side effects that must run on request. No `model`, no XML in the description.
4. Description, at most 250 characters: what it does, then "Use when" with 2-4 situations in the user's own words, then "Not for" the nearest neighbour. Scope by situation, not by naming other skills.
5. Body in this order, empty parts dropped: one-line purpose; Steps (numbered, imperative, each checkable; the first steps marked *always* are the short path for small tasks); Rules (at most 5, "never X: reason"); Branches ("If <condition>, read `references/<x>.md`", one level deep); Report (at most 5 lines, last line "Not checked: …"). Read paths and commands from the project's CLAUDE.md instead of hard-coding them.
6. Cut: rationale, history, examples, generic advice, anything the model infers from the code, anything already in CLAUDE.md. Target 300-800 tokens (chars / 4); above 1,500 split branches into `references/` (each under 1,000 tokens, linked from the body).
7. Test before keeping: write 5 prompts that must fire it and 5 that must not (include the nearest neighbour's). Run each with `claude -p "<prompt>" --output-format stream-json --verbose` and look for a `Skill` tool call; then one realistic task and check the result. A prompt that misses on a stronger model is a description problem: rewrite the description, not the body.
8. A fire count that stays low, or a task result no better than a one-line CLAUDE.md rule: recommend the one-line rule instead.

## Rules
- Never put side effects (delete, install, settings) in a skill without a confirm step or the manual flag; for commit and push the manual flag is not enough, add an explicit "ask before committing" step.
- Never copy text from a source without checking its license; keep a credit line.
- Never add rules the model already follows; test before adding.
- One skill, one job; a skill that needs "and" in its description is two skills.
- Scripts only to replace prose or to save tokens, after a before/after comparison.

## Report
- Layer chosen, file written, description length, token count.
- Trigger results (fired / total) and the task result.
- Not checked: <…>
