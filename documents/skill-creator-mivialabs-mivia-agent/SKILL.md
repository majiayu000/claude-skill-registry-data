---
name: skill-creator
description: Author a new project skill with valid frontmatter, a usable procedure, a matching Claude alias, and passing repository gates.
triggers:
  - create a skill
  - author a new skill
  - write a SKILL.md
  - add a project skill
  - make a skill for this repository
  - scaffold a skill procedure
short-description: Author and validate a project skill
argument-hint: "Skill purpose, users, and required tools"
user-invocable: true
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - write_file
  - run_command
---

# Skill Creator

Create one project skill under `.agents/skills/<name>/`. This skill is for
interactive authoring only. Do not invoke it from a workflow step. The
workflow write-tool blocklist applies to workflow agent steps, as described in
`.mivia/mivia.toml.example`; it does not provide the same control for an
interactive session. Keep the work in the interactive session and follow the
repository policy in `.agents/rules/10-security-privacy.md`.

## Procedure

1. Gather the requirements.

   Record the skill purpose, users, likely request wording, required tools,
   whether a user may invoke it directly, and the smallest useful output.
   Search `.agents/skills/` for a skill with the same purpose or title. Do not
   create a duplicate skill. Read the closest existing skills for tone and
   body shape.

2. Read the contracts.

   Read `internal/skills/skill_markdown.go` for the current frontmatter
   contract and `docs/architecture/skills.md` for discovery, alias, tool, and
   invocation rules. Cite these files in the new skill when their details are
   needed. Do not copy their full contents into the skill.

   The loader silently truncates model-facing text at its configured limits.
   Check the current limits in `internal/skills/skill_markdown.go` and keep
   `name`, `description`, each trigger, and the joined trigger block within
   those limits. A truncation can remove the words that make a skill select
   correctly, so treat every limit as a correctness rule.

3. Design the frontmatter.

   Use only keys accepted by `internal/skills/skill_markdown.go`. Set a short,
   exact `name` that matches the directory. Write a specific description.
   Make triggers pushy enough to select the skill for the real request, but
   narrow enough to avoid unrelated requests. Choose `user-invocable` from the
   requirements. Add `argument-hint` and `short-description` only when they
   help the selection surface. Declare every required tool in `tools:`.

   Keep the body's `Tool surface` section equal to the frontmatter `tools:`
   list. The list is metadata for agent-skill binding. It does not grant a
   tool. A role that later grants this skill must list every declared tool in
   its own `tools:` list; `make verify-agent` checks this subset contract.

4. Write the canonical skill.

   Create `.agents/skills/<name>/SKILL.md` with the frontmatter and a body a
   model can follow without this session's context. State the purpose, scope,
   procedure, verification, and what the skill never does. Use ASD-STE100:
   short sentences, direct verbs, known words, and no decorative prose.
   Keep repository-specific facts as links to their canonical sources.

5. Write the Claude alias in the same change.

   Create `.claude/skills/<name>/SKILL.md` as a plain file. Copy the
   canonical frontmatter byte for byte. After the closing delimiter, use only
   this pointer body:

   ```text
   This skill is defined in `.agents/skills/<name>/SKILL.md`.

   Read that file now and follow it exactly. It is the only definition. This file
   is an alias so Claude Code can find the skill. Bundled resources live beside
   the canonical file.
   ```

   Do not create `.mivia/skills/`. Do not use a symlink. The alias contract and
   the reason for the plain file are defined in
   `docs/architecture/skills.md` and checked by
   `scripts/verify_skill_tree.py`.

6. Validate the result.

   Read both files back. Check that the frontmatter is identical, the name
   matches the directory, the tool list and `Tool surface` match, and the
   body has a complete procedure. Run the actual gates:

   ```text
   python3 scripts/verify_skill_tree.py
   python3 scripts/verify_agent_config.py
   make verify-agent
   ```

   Run any focused contract test reported by those gates. Fix every failure
   before you call the skill done. Do not claim that a gate passed unless the
   command ran and returned success.

## Tool surface

`read_file`, `list_dir`, `grep`, `glob`, `find_references`, `write_file`,
`run_command`.

This list is the frontmatter `tools:` list, and the two must stay equal.

## What this skill never does

- It never runs as a workflow step.
- It never creates `.mivia/skills/`.
- It never commits or pushes.
- It never writes outside the requested `.agents/skills/<name>/` and
  `.claude/skills/<name>/` files.
- It never stores secrets, keys, tokens, passwords, or credentials.
