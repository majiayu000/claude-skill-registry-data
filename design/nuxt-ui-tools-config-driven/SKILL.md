---
name: nuxt-ui-tools-config-driven
description: Use this skill for internal architecture work around config-driven, registry-driven, and pattern-driven feature design in the nuxt-ui-tools repository. Covers how to organize variant-heavy features, where to put implementations, and how to keep both internals and public APIs standardized.
---

# nuxt-ui-tools Config-Driven Design

Use this skill when the task is primarily about:

- feature architecture
- variant-heavy logic
- config or registry design
- splitting giant branching code
- organizing filters, columns, actions, or future feature kinds

## Read First

- `AGENTS.md`
- `.agents/skills/nuxt-ui-tools-maintainer/SKILL.md`
- `.agents/skills/nuxt-ui-tools-config-driven/references/core-pattern.md`
- `.agents/skills/nuxt-ui-tools-config-driven/references/feature-organization.md`
- `.agents/skills/nuxt-ui-tools-config-driven/references/registry-contracts.md`

## Purpose

This skill exists because config/registry-driven design is one of the core architectural rules of this repository.

The goal is to make:

- feature growth predictable
- variants easy to add
- pipelines easy to test
- public APIs easier to document and adopt
