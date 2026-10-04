---
name: skillshilp-create
description: Expert architect for creating new production-quality Agent Skills. Use when designing new skills, converting reusable prompts into skills, or architecting modular skill collections. Not for modifying existing skills.
license: MIT
metadata:
  author: Vignesh Prasad
  github: https://github.com/ViGi-P/skillshilp
  version: "2.1.1"
  purpose: meta-skill
---

# Skillshilp Create

Design Agent Skills as reusable software components, not large prompts.

Your objective is to produce Agent Skills that are discoverable, composable, maintainable, deterministic, and token-efficient.

Use this skill only for **creating new skills**. If the primary task is to modify, refactor, review, or improve an existing skill, use **skillshilp-edit** instead.

If official documentation is available, treat it as the source of truth. Otherwise, follow the provided specification.

---

# Principles

| Prefer | Avoid |
|--------|-------|
| Single responsibility | God skills |
| Progressive disclosure | Bloated `SKILL.md` files |
| Modular design | Overlapping responsibilities |
| Focused references | Duplicate documentation |
| Searchable descriptions | Generic descriptions |
| Minimal Bash scripts | Large code blocks in Markdown |
| Reusable assets | Embedded templates or schemas |
| Deterministic workflows | Ambiguous instructions |
| Token efficiency | Repetition |

Every file should have a clear purpose. Avoid introducing directories, files, or abstractions that do not meaningfully improve maintainability or reuse.

Prefer concise examples over broad explanations. Treat context as a scarce shared resource.

---

# Workflow

## 1. Evaluate

Determine whether the request should become an Agent Skill.

An Agent Skill should represent a reusable capability that another agent can reliably discover and invoke.

If the request is better solved by a script, template, document, workflow, or one-off prompt, recommend that instead.

If the intended use is unclear, derive or ask for 2–3 realistic user requests before designing the skill. Use those examples to identify the repeatable workflow, activation criteria, required inputs, expected outputs, and reusable resources.

Define:

- responsibility
- intended users
- activation criteria
- inputs
- outputs
- constraints
- dependencies
- edge cases

If multiple unrelated capabilities are identified, split them into separate skills with clearly defined responsibilities.

---

## 2. Design

Design the architecture before writing any files.

Set the right degree of freedom:

- Use `SKILL.md` for flexible workflow guidance.
- Use `references/` for detailed knowledge that is only sometimes needed.
- Use `scripts/` for repeated, deterministic, or fragile operations.
- Use `assets/` for reusable output materials.

Prefer minimal Bash for scripts. If Bash cannot express the operation safely, document the requirement and ask before choosing another runtime.

Map concrete examples to reusable artifacts:

- Repeated command sequence → `scripts/`
- Long domain/API/schema knowledge → `references/`
- Template, boilerplate, or sample input → `assets/`
- Core activation and workflow rules → `SKILL.md`

Create only the directories that add value.

### Skill Directory

A skill is a directory whose required entry point is `SKILL.md`.

Typical portable skill layout:

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

The skill directory itself is independent of the directory used by an agent or client to discover it.

 For project-level skills, `.agents/skills/<skill-name>/` is a widely adopted cross-client convention, but it is not required by the Agent Skills specification. Clients may use their own discovery directories.

 When creating a skill in a project, use the host/client's documented skill directory when one is provided. Do not hard-code `.agents/skills/` when the environment specifies another location.

 When creating a standalone or distributable skill, create the skill directory itself and do not add a client-specific parent directory unless requested.

Do not create `README.md` or other auxiliary documentation unless the user requests distribution-facing docs.

Decide where each piece of information belongs.

### `SKILL.md`

Keep concise.

Include only:

- activation criteria
- workflow
- critical rules
- validation
- references to supporting files

### `references/`

Store information intended to be read by the model, such as:

- technical documentation
- APIs
- algorithms
- schemas
- workflows
- FAQs
- design guidance

### `scripts/`

Store executable logic only when it materially improves reliability or repeatability.

Scripts should be minimal Bash, validate inputs, document dependencies, fail predictably, and avoid embedding large prompts where executable code is more appropriate.

### `assets/`

Store reusable resources, such as:

- templates
- configuration files
- diagrams
- sample data
- example documents

Do not add product-specific metadata, client configuration, or product-specific helper scripts when portability is the goal.

---

## 3. Implement

Generate:

- the skill directory at the requested or host-provided destination
- valid frontmatter
- concise `SKILL.md`
- supporting reference files
- scripts when appropriate
- assets when appropriate

Do not assume that the skill repository's source directory, the skill's installation directory, and the client's discovery directory are the same location.

Descriptions should clearly explain:

- what the skill does
- when another agent should activate it
- what makes it distinct from similar skills

Assume the description will be used for automatic discovery.

Use only portable Agent Skills frontmatter.

---

## 4. Validate

Before finalizing, verify that the skill is:

- specification compliant
- discoverable
- single responsibility
- modular
- composable
- maintainable
- progressively disclosed
- minimally duplicated
- token-efficient

When a skill directory exists on disk, run:

```bash
scripts/validate-skill.sh <skill-dir>
```

`<skill-dir>` refers to the skill directory itself, not its parent discovery directory. For example, `.agents/skills/my-skill/` is the skill directory; `.agents/skills/` is its discovery directory.

Validate against:

`references/constraints.md`

Review common architectural patterns:

`references/patterns.md`

Check for common design mistakes:

`references/skill-smells.md`

If any issue is found, revise the design before returning the skill.

For complex or fragile skills, forward-test with realistic user requests. Give validators the skill and raw task artifacts, not expected answers or your diagnosis.

---

# Output

Prefer creating or modifying files directly when the environment allows it.

If files were written, provide:

1. Changed paths
2. Validation results
3. Brief design notes explaining important architectural decisions

If files cannot be written or the user asks for generated content, provide:

1. Complete directory tree
2. Complete contents of every generated file
3. Valid relative file references
4. Brief design notes

Do not dump full file contents for files already written unless explicitly requested.

---

# Final Check

Before returning the skill, ask:

> If this skill were published in a large public registry, would another agent reliably discover it, understand when to activate it, compose it with other skills, and successfully execute it without additional explanation?

If the answer is not an unqualified **yes**, continue refining the design.
