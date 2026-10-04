---
name: skillshilp-edit
description: Expert editor for improving production-quality Agent Skills. Use when reviewing, refactoring, modernizing, or maintaining existing Agent Skills while preserving their intended behaviour. Not for creating new skills.
license: MIT
metadata:
  author: Vignesh Prasad
  github: https://github.com/ViGi-P/skillshilp
  version: "2.1.1"
  purpose: meta-skill
---

# Skillshilp Edit

Improve Agent Skills as reusable software components, not large prompts.

Your objective is to preserve intended behaviour while making Agent Skills more discoverable, composable, maintainable, deterministic, and token-efficient.

Use this skill only for **editing existing Agent Skills**. If the primary task is to create a new skill from ideas, requirements, reusable prompts, or specifications, use **skillshilp-create** instead.

If official documentation is available, treat it as the source of truth. Otherwise, follow the provided specification.

---

# Principles

| Prefer | Avoid |
|--------|-------|
| Minimal targeted changes | Unnecessary rewrites |
| Behaviour preservation | Breaking existing workflows |
| Single responsibility | God skills |
| Progressive disclosure | Bloated `SKILL.md` files |
| Modular design | Overlapping responsibilities |
| Focused references | Duplicate documentation |
| Searchable descriptions | Generic descriptions |
| Minimal Bash scripts | Large code blocks in Markdown |
| Reusable assets | Embedded templates or schemas |
| Deterministic workflows | Ambiguous instructions |
| Token efficiency | Repetition |

Preserve working behaviour unless a change is explicitly requested or clearly required to improve correctness, maintainability, or specification compliance.

Prefer concise examples over broad explanations. Treat context as a scarce shared resource.

---

## Preservation Rules

Unless explicitly requested, preserve:

- the skill's primary responsibility
- activation criteria
- public behaviour
- directory structure
- file names
- relative references
- documented workflows

Only introduce structural changes when they provide a clear improvement in correctness, maintainability, discoverability, or specification compliance.

### Skill Location

Treat the skill directory and its parent discovery directory as separate concerns.

The skill directory is the directory containing `SKILL.md` and its supporting resources. Its parent directory is determined by the host or client.

`.agents/skills/` is a widely adopted cross-client convention for project- and user-level skill discovery, but it is not required by the Agent Skills specification.

When editing an existing skill:

- preserve the skill directory and its contents unless a change is required
- do not move a skill merely to make its parent directory `.agents/skills/`
- do not introduce `.agents/`, `.claude/`, `.github/`, or another client-specific discovery directory inside the skill
- preserve the host's existing discovery location unless relocation is explicitly requested
- when creating or moving a skill as part of the requested change, follow the host/client's documented discovery convention

When preserving product-specific metadata conflicts with a portability objective, remove or isolate it only when the request clearly asks for portability.

---

# Workflow

## 1. Evaluate

Understand the existing Agent Skill before making changes.

Determine:

- current responsibility
- intended users
- activation criteria
- public behaviour
- requested modifications
- constraints
- dependencies
- compatibility concerns

If the intended behaviour is unclear, derive or ask for 2–3 realistic user requests before editing. Use those examples to identify what must keep working and what can change.

If the requested changes significantly expand the skill's responsibility, recommend splitting it into multiple skills instead.

---

## 2. Plan

Plan the smallest set of changes required to satisfy the request.

Avoid redesigning the skill unless explicitly instructed.

When modifying the architecture:

- preserve existing behaviour where practical
- preserve activation criteria unless intentionally changing them
- preserve file organization unless a better structure provides clear value
- avoid introducing unnecessary directories or files

Set the right degree of freedom:

- Use `SKILL.md` for flexible workflow guidance.
- Use `references/` for detailed knowledge that is only sometimes needed.
- Use `scripts/` for repeated, deterministic, or fragile operations.
- Use `assets/` for reusable output materials.

Prefer minimal Bash for scripts. If Bash cannot express the operation safely, document the requirement and ask before choosing another runtime.

When a larger redesign is justified, explain why.

---

## 3. Implement

Modify only the files affected by the requested changes.

When appropriate:

- update `SKILL.md`
- update reference files
- update scripts
- update assets
- improve descriptions for discoverability
- remove duplication
- modernize outdated structures

Ensure all relative references remain valid.

Use only portable Agent Skills frontmatter.

---

## 4. Review

Before finalizing, verify that the updated skill is:

- specification compliant
- behaviour preserving
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

Validate against:

`references/constraints.md`

Review common architectural patterns:

`references/patterns.md`

Check for common design mistakes:

`references/skill-smells.md`

If any issue is found, revise before returning the updated skill.

For complex or fragile changes, forward-test with realistic user requests. Give validators the skill and raw task artifacts, not expected answers or your diagnosis.

---

# Output

Prefer modifying files directly when the environment allows it.

If files were written, provide:

1. Changed paths
2. Validation results
3. Summary of changes made
4. Brief design notes explaining significant architectural decisions

If files cannot be written or the user asks for generated content, provide:

1. Updated directory tree (only if it changed)
2. Complete contents of every modified file
3. Valid relative file references
4. Summary of changes made
5. Brief design notes

Do not dump full file contents for files already written. Do not regenerate unchanged files unless explicitly requested.

---

# Final Check

Before returning the updated skill, ask:

> Does this preserve the original responsibility, activation criteria, and intended behaviour of the Agent Skill while making it easier to discover, understand, maintain, and evolve?

If any existing behaviour was intentionally changed, clearly explain why the change was necessary.

If the answer is not an unqualified **yes**, continue refining the changes.
