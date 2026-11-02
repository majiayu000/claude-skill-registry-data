---
name: skill-generator
description: Reactant direct-entry skill authoring utility. Use when the user directly asks to create a project-local Reactant tag skill from a natural-language description; it has no inline tag form and is never dispatched by execute or execute-one.
---

# Skill Generator

## Entry Boundary

This is a direct entry skill, alongside `execute` and `execute-one`. It is not
a Reactant tag skill or document router. Activate it only from an explicit
user request to create a Reactant project-local skill, such as:

```text
/skill-generator a translate skill that preserves citations and LaTeX commands
```

There is no inline form for this entry skill. `execute` and `execute-one` must
never select or dispatch an apparent generator annotation in an authored
document. Do not read, consume, or edit a document merely to obtain the
generator request.

The generated directory is a standard Agent Skill. The router agent discovers
the new worker by reading project skill roots on its next invocation; there is
no registry and no programmatic tag scanner.

## Input

Accept the user's direct natural-language description of the new skill and the
current project root. If the intended behavior, name, or file effects are
materially ambiguous, clarify them before creating files.

## Workflow

1. Read the description and `references/skill-contract.md` in this skill
   directory. Infer the requested behavior without reducing the description to
   a machine tag grammar.
2. Choose a name made of lowercase letters or numbers separated by single
   hyphens. It must not be a reserved name (`execute`, `execute-one`,
   `skill-generator`, `chat-user`, `resolve`, `chat-model`, `comment`) or
   collide with another skill unless the user explicitly requests an allowed
   override.
3. Inspect the project-local skill root and create `.reactant/skills/` if it
   does not exist.
4. Write `.reactant/skills/<name>/SKILL.md` according to the contract: YAML
   frontmatter with a matching `name`, a description explicitly limiting
   activation to router-dispatched tags, an `Activation Boundary` section,
   tag examples, input behavior, workflow, scope-modifier and context-reference
   handling, consumption behavior, and clean failure behavior. Add supporting
   `scripts/`, `references/`, or assets only when the skill needs them; keep the
   skill self-contained.
5. Validate the directory by reading it against the structural contract:
   frontmatter, naming, required behavior, self-containment, and reserved-name
   rules. If an optional structural Agent Skills or Reactant validator is
   available, it may be run as an additional check. Such a validator must not
   scan authored documents or classify annotations.
6. Fix any structural errors and validate again. If the skill cannot be made
   valid, remove only the incomplete directory created by this invocation and
   report the diagnostics.
7. Report the created path and the generated worker's annotation form. Do not
   modify an authored document as part of generation.

## Rules

- Generated skills are tag-only workers; this generator does not create new
  entry skills.
- Validation is structural only. Reactant does not semantically verify what a
  generated skill will produce at runtime.
- Phase 1 skill generation and routing require no Python runtime or vendored
  `reactant_core.py`.
- On failure, do not leave an incomplete generated directory. Preserve all
  pre-existing project files and report the problem.
