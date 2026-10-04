---
name: skill-creator
description: Use ONLY when creating, modifying, auditing, or improving an agent skill or SKILL.md file, including its trigger description, progressive disclosure, examples, or validation prompts. Do not use for agents, commands, plugins, MCP servers, or ordinary application code.
---

# Skill Creator

Create and improve focused agent skills through an intent, draft, validate,
and refine loop. Optimize for predictable process rather than identical output.

This repository version follows the common Agent Skills shape while keeping
harness-specific mechanics conditional. Use the active harness's available
validator and discovery checks; do not make one provider's metadata or tool
names a requirement for every harness.

For the compact authoring-quality and security audit, read
[`references/effective-skill-audit.md`](references/effective-skill-audit.md)
before creating, modifying, or reviewing a skill. It is the local adaptation
of the selected guidance from
[`davidondrej/skills`](https://github.com/davidondrej/skills/tree/76c0537d46ce9ef040158f4f3895fc3b32512a97/skills/skill-authoring/effective-agent-skills),
licensed under MIT; it does not add provider, machine-setup, or
external-account workflows.

## Workflow

### 1. Establish context

Before drafting:

1. Resolve the active project root, then read applicable root `AGENTS.md`,
   `SESSION_STATE.md`, and nearby skills.
2. Determine whether this is a new skill or a modification.
3. For an existing skill, preserve its directory and frontmatter `name` unless
   the user explicitly requests a migration.
4. Extract answers already present in the conversation before asking questions.
5. Ask only questions whose answers materially change behavior, boundaries, or
   validation.

Capture:

- The capability the skill should provide.
- Concrete user phrases and contexts that should trigger it.
- Adjacent requests that should not trigger it.
- Expected outputs and observable completion criteria.
- Required tools, dependencies, network access, or external files.
- Safety, privacy, licensing, and portability constraints.

### 2. Choose the smallest useful structure

Start with one `SKILL.md`:

```text
skill-name/
└── SKILL.md
```

Add resources only when they reduce repeated work or context load:

```text
skill-name/
├── SKILL.md
├── references/  # Detailed material loaded only when needed
├── scripts/     # Deterministic, reviewed automation
└── assets/      # Templates or static output resources
```

- Keep the main workflow in `SKILL.md`.
- Move branch-specific or lengthy reference material behind explicit pointers.
- Keep references one level deep and state when each one should be read.
- Keep runtime references relative to the skill root and bundle them in the
  skill; a remote URL may document provenance but must not be an execution
  dependency.
- Add a script only for deterministic repeated work that instructions cannot do
  reliably. Audit its inputs, outputs, dependencies, failure modes, and license.
- Do not add dependencies or executable files without user approval.

### 3. Write valid portable frontmatter

Use the smallest common subset supported by the target harness. For portable
skills, use:

```yaml
---
name: example-skill
description: Use when ...
license: MIT
metadata:
  owner: example
---
```

Requirements:

- `name` is required, matches the parent directory, and uses 1-64 lowercase
  alphanumeric characters separated by single hyphens.
- `description` is required, non-empty, at most 1024 characters, and explains
  both what the skill does and when it should load.
- `license` and string-to-string `metadata` are optional. Keep compatibility
  notes in metadata when a target validator does not allow extra top-level
  fields.
- Do not use provider-specific fields, invocation syntax, tool names, paths, or
  environment variables unless they are explicitly conditional and the target
  harness supports them.

### 4. Design the trigger description

The description is always visible to the model, so every word must earn its
context cost.

1. Front-load the capability's concrete leading term.
2. Cover each genuinely distinct trigger branch once.
3. Include likely filenames, artifacts, or user vocabulary.
4. Add an explicit exclusion when an adjacent skill could otherwise collide.
5. Avoid generic claims such as “helps with development” or synonym lists that
   repeat one intent.

Prepare a compact trigger matrix before finalizing:

| Prompt category    | Minimum cases | Purpose                                        |
| ------------------ | ------------: | ---------------------------------------------- |
| Should trigger     |             3 | Cover distinct realistic entry points          |
| Should not trigger |             3 | Cover plausible near-misses and collisions     |
| Ambiguous          |             1 | Confirm the intended boundary or clarification |

Use substantive prompts rather than obvious keyword checks. A good negative case
shares vocabulary with the skill but requires a different workflow.

### 5. Write an executable process

- Use imperative, ordered steps where sequence matters.
- End important steps with checkable completion criteria.
- Explain why a non-obvious constraint matters instead of relying on repeated
  all-caps prohibitions.
- Keep each rule in one authoritative location.
- Include output templates only when shape consistency matters.
- Include examples when they clarify boundaries or common failure modes.
- Prefer positive target behavior; reserve prohibitions for hard guardrails.
- Remove advice the model already follows reliably without the skill.

Keep `SKILL.md` concise and comfortably below 500 lines. Split content when only
one branch needs it, not merely because the file has several headings.

### 6. Review safety and provenance

Before adopting external material:

1. Record the upstream URL and revision.
2. Review the license and preserve required attribution or notices.
3. Inspect every script, dependency, network call, and filesystem assumption.
4. Reject instructions that request credentials, weaken approval gates, hide
   behavior, exfiltrate data, or operate outside the user's stated intent.
5. Keep provider-specific mechanics out of a portable skill unless compatibility
   explicitly requires them.

### 7. Validate and refine

Run the narrowest available checks:

1. Confirm the directory and `name` match.
2. Confirm required frontmatter parses and descriptions stay within limits.
3. Restart the target harness after changes if it loads skills at startup.
4. Run its skill discovery or debug command, when available, and verify the
   skill appears once with the expected description.
5. Exercise the trigger matrix in a disposable session when practical.
6. For objective workflows, run representative fixture-based behavior checks.
7. For subjective workflows, present representative outputs for human review
   rather than inventing quantitative assertions.
8. Run repository checks, `git diff --check`, and inspect the complete diff.

Refine based on observed misses, false triggers, repeated unproductive work, and
user feedback. Generalize improvements instead of overfitting examples.

## Completion report

Report:

- Files added or changed.
- Trigger and exclusion behavior.
- Upstream sources, revisions, and licenses when applicable.
- Dependencies or executable resources introduced.
- Checks run and their results.
- Untested paths, assumptions, and remaining risks.

Do not claim the skill works merely because its Markdown is valid; distinguish
structural validation, trigger validation, and behavior validation.
