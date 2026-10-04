---
name: writing-skills
description: Use when creating a new skill, editing an existing skill, or writing the agent/command that wraps one.
---

# Writing Skills

## Overview

A skill is a reusable reference guide for a proven technique, pattern, or discipline that
future agents (and you) find and apply. **A skill is NOT a narrative of how you solved
something once.**

**Writing a skill is TDD applied to documentation:** pressure-test an agent *without* the
skill and watch it do the wrong thing (RED), write the skill addressing exactly those
failures (GREEN), then close the loopholes it still finds (REFACTOR). If you never watched an
agent fail without the skill, you don't know the skill teaches the right thing.

## When to create one
**Create when:** the technique wasn't obvious, you'd reference it across tasks, it applies
broadly, and it's a *judgment call* (not enforceable by a linter).
**Don't create for:** one-off solutions; standard practice documented elsewhere;
project-specific conventions (those go in `AGENTS.md`); anything a regex/`mix` check could
enforce mechanically.

## The description field is the most important line

The `description` is what an agent reads to decide whether to load the skill. **Describe ONLY
when to use it — never summarize what it does or its workflow.**

Why it matters: when a description summarizes the process, agents follow the *description* and
skip the body. A real case: a description saying "code review between tasks" made an agent do
ONE review when the skill body specified TWO. Stripping the summary fixed it.

```yaml
# ❌ summarizes workflow — agents follow this and skip the body
description: Use for TDD — write test first, watch it fail, write minimal code, refactor
# ✅ triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

Rules: start with "Use when…"; third person; concrete triggers/symptoms; describe the
*problem* not language-specific tokens; keep technology-agnostic unless the skill itself is
specific; include searchable keywords (error strings, symptoms, synonyms); under ~500 chars.

## Structure
Frontmatter: only `name` (letters/numbers/hyphens, verb-first/gerund — `creating-skills` not
`skill-creation`) and `description`. Body: `## Overview` (what + core principle in 1–2
sentences), `## When to Use`, then the technique — tables/lists for reference, fenced code for
examples, numbered lists for linear steps. End with common mistakes.

## Keep it tight
- Be concise — aim well under 500 words for normal skills. Frequently-loaded ones, tighter.
- **Cross-reference instead of repeating:** name the other skill (e.g. "use the
  `test-driven-development` skill") — never `@`-link a file (that force-loads it and burns
  context).
- One excellent, runnable, well-commented example beats five mediocre ones. Don't reimplement
  it in many languages; don't write fill-in-the-blank templates. For this project, prefer
  Elixir/ExUnit examples.
- Use a small flowchart ONLY for a non-obvious decision or a loop where you'd stop too early —
  never for reference material, code, or linear steps.

## Verify
After writing, re-read with fresh eyes: does the description give triggers-only? Could an
agent follow it without getting stuck? Is anything a narrative rather than a reusable
technique? `wc -w .claude/skills/<name>/SKILL.md` to sanity-check length. Fix inline.
