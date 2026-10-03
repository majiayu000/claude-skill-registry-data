---
name: nuxt-ui-tools-reactivity
description: Use this skill for internal Vue reactivity and state-model work in the nuxt-ui-tools repository. Covers lean reactivity, query-state integration, when to use computed vs watch vs shallowRef, VueUse usage, and how to simplify over-layered state models.
---

# nuxt-ui-tools Reactivity

Use this skill when the task is primarily about:

- reactive state design
- table/query-state integration
- removing reactive waste
- deciding between `computed`, `watch`, `ref`, and `shallowRef`
- VueUse adoption

## Read First

- `AGENTS.md`
- `.agents/skills/nuxt-ui-tools-maintainer/SKILL.md`
- `.agents/skills/nuxt-ui-tools-reactivity/references/lean-reactivity.md`
- `.agents/skills/nuxt-ui-tools-reactivity/references/query-state-integration.md`
- `.agents/skills/nuxt-ui-tools-reactivity/references/vueuse.md`

## Purpose

This skill exists to keep runtime state direct, explainable, and fast enough.

The goal is not just "make it reactive".
The goal is:

- minimal state duplication
- minimal bridging layers
- clear ownership of reactive values
- easy explanation and easy refactoring
