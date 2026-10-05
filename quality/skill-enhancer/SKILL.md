---
name: skill-enhancer
description: "Audit, stress-test, and improve Codex or Claude skills using source-backed patterns, pressure questions, progressive disclosure, and validation. Use when creating or enhancing a skill, porting a Claude skill to Codex, reviewing SKILL.md quality, improving trigger descriptions, splitting references, adding workflow rigor, or testing whether a skill resists ambiguity."
---

# Skill Enhancer

## Overview

Use this skill to turn a rough or existing skill into a sharper operational workflow. Prefer evidence from the target skill, nearby repo docs, local Claude/Codex skills, and known external skill patterns over generic advice.

When the user asks for a broad comparison, read [references/source-patterns.md](references/source-patterns.md). Otherwise load it only if the current skill needs pattern selection or source-backed justification.

## Workflow

1. Locate the target.
   - Find the skill directory, `SKILL.md`, metadata files, references, scripts, and any linked repo docs.
   - If porting from Claude, inspect frontmatter, allowed tools, command arguments, project rules, and related `.claude/commands` or `.claude/agents` files.
   - If no target exists, scaffold with the local `skill-creator` workflow and then edit.

2. Build the source map.
   - Target skill: what it claims, when it triggers, what workflow it enforces.
   - Local patterns: nearby successful skills, project-specific rules, templates, validation scripts.
   - External patterns: use Matt Pocock for grilling ambiguous plans, Superpowers for skill TDD and verification discipline, and Codex `skill-creator` for local structure and metadata.

3. Resolve ambiguity with a grill loop.
   - Ask one question at a time only when human judgment is required.
   - If the answer can be discovered from files, inspect files instead of asking.
   - Each question must include a recommended answer and the tradeoff it implies.
   - Continue until ambiguity is reasonably solved for the next edit, not until every theoretical edge case is exhausted.

4. Run the enhancement audit.
   - Trigger: frontmatter description says what the skill does and exactly when to use it.
   - Scope: states when to use it, when not to use it, and what inputs it expects.
   - Workflow: gives ordered actions, decision points, and completion criteria.
   - Disclosure: keeps `SKILL.md` lean; moves detailed patterns, examples, or domain rules to one-level references.
   - Tools: prefers deterministic scripts for repeated fragile operations.
   - Interaction: asks only useful questions; provides defaults or recommendations.
   - Safety: protects user edits, secrets, external side effects, and destructive actions.
   - Verification: names concrete checks before claiming completion.

5. Edit the skill.
   - Keep changes scoped to the requested skill unless related metadata or references must change.
   - Preserve useful source-specific practices while converting platform-specific assumptions.
   - Avoid duplicating large reference material in `SKILL.md`; link it instead.
   - Keep supporting files limited to files the agent should actually use.

6. Validate.
   - Run the Codex skill validator for Codex skills when available.
   - Search for unfinished scaffold markers, stale names, and broken relative references.
   - Verify `agents/openai.yaml` still matches the skill and mentions `$skill-name` in `default_prompt`.
   - For behavioral skills, pressure-test at least one realistic prompt. Use subagents only when available and useful.

7. Report completion.
   - Lead with changed files and validation evidence.
   - Summarize the source patterns used only as much as needed.
   - Do not claim the skill works until validation output or a concrete manual inspection supports it.

## Output Shape

For small edits, return changed files plus validation. For larger enhancements, include:

- Source comparison: the 3-6 patterns that materially changed the skill.
- Patch summary: what changed in `SKILL.md`, references, scripts, or metadata.
- Verification: commands run and important results.
- Open risks: missing source access, untested behavior, or assumptions that still matter.
