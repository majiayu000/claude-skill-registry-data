---
name: drupal-config-executor
type: executor
model: claude-opus-4-8
description: "Execute Drupal configuration changes from drupal-planner specs."
---

# Drupal Config Executor Skill

## When to Use

**Primary triggers:**
- "generate drupal config", "scaffold content type", "create drupal fields"
- "generate config yaml", "drupal config from plan"
- "execute this content model plan", "build this content type"
- User has a drupal-planner.content-model spec and wants config YAML generated
- User describes a content type directly and wants config files produced

---

## Use When

- You have a completed drupal-planner.content-model spec and want to generate the config YAML files
- You have a completed drupal-planner.taxonomy spec and want vocabulary + facet config
- You have a completed drupal-planner.search spec and want Search API config
- You want to scaffold a content type directly without running the planner first (simple cases only)
- You need config YAML files for an existing content model design document

---

## Do Not Use When

- You need to **design** a content model — use `drupal-planner.content-model` first
- You need to **review** existing Drupal config — use `content-model-critic` or `drupal-critic`
- You need **custom module PHP code** (hooks, services, plugins) — use the OMC executor agent
- You need **theme scaffolding** (SDC components, Twig, CSS) — future `drupal-theme-executor`
- You need **migration YAML** — use `drupal-migration-planner` for the spec, then implement manually

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Have a content-model plan, need config YAML | This skill — generates all config files |
| Need to design the content model first | Use `drupal-planner.content-model`, then come back |
| Have config YAML, need quality review | Use `content-model-critic` + `drupal-critic` |
| Need custom module code, not config | Use OMC executor agent or manual implementation |
| Need to migrate existing content to new model | Use `drupal-migration-planner` for the plan |

---

## What You Get

- **Config YAML files** for all entity types, fields, form displays, view displays, taxonomy vocabularies, Search API indexes
- **Dependency-ordered manifest** listing all generated files and their import order
- **Deviation log** documenting any places the generated config differs from the planner spec
- **Critic handoff command** — ready to run `/content-model-critic` + `/drupal-critic` on the output

---

## Input Modes

### Mode 1: Planner Spec (Preferred)
Provide the output from `drupal-planner.content-model`, `.taxonomy`, or `.search`. The executor parses the structured tables (Entity Type Definitions, Field Architecture, Taxonomy Integration) and generates config YAML matching the spec exactly.

### Mode 2: Direct Request (Simple Cases)
Describe the content type directly: "Create an Event content type with title, date range, location reference, body, and image fields." The executor generates config using sensible Drupal defaults. For complex content models with many entity types, redirects to `drupal-planner.content-model`.

---

## Companion Skills

- **drupal-planner.content-model** (upstream): Designs the content model that this executor implements
- **drupal-planner.taxonomy** (upstream): Designs taxonomy architecture
- **drupal-planner.search** (upstream): Designs search configuration
- **content-model-critic** (downstream): Reviews generated config for entity proliferation, field duplication, composition patterns
- **drupal-critic** (downstream): Reviews generated config for Drupal best practices

---

## meta-router Registry Note

Listed under the **Executors** table.
Trigger signals: `generate drupal config, scaffold content type, create drupal fields, generate config yaml, drupal config from plan`
