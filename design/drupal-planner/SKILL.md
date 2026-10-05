---
description: Plan Drupal implementations — entities, config, migrations, cache, permissions.
name: drupal-planner
---

# Drupal Planner

## Overview

drupal-planner helps you design Drupal implementations before writing code. It produces architecture plans that specify entity types, field relationships, module decisions, config schemas, permission models, cache strategies, and migration paths — precise enough that a developer can implement them without architectural guessing.

For focused subsystem planning, use the dot-notation sub-planners:
- `/drupal-planner.content-model` — Drupal content model architecture (entity types, bundles, paragraphs, field architecture)
- `/drupal-planner.taxonomy` — Drupal taxonomy architecture (vocabularies, term hierarchies, faceted navigation)
- `/drupal-planner.theme` — Drupal theme architecture (base theme, components, CSS, preprocess, assets)
- `/drupal-planner.canvas` — Canvas Code Component architecture (component definition, props, data fetching, composability, deploy)
- `/drupal-planner.search` — Drupal search architecture (Search API, Solr/Elasticsearch, facets, Views)

## Sub-Planner Routing

When the user's request is clearly focused on one subsystem, suggest the appropriate sub-planner:

| Signal | Route To |
|--------|----------|
| "content model", "entity types", "content types", "paragraphs", "field architecture", "bundles" | `/drupal-planner.content-model` |
| "taxonomy", "vocabularies", "classification", "tagging", "categories", "facets" | `/drupal-planner.taxonomy` |
| "theme", "templates", "CSS", "Twig", "SDC", "design system", "frontend" | `/drupal-planner.theme` |
| "Canvas", "Canvas Code Component", "component definition", "component props", "component composability", "Canvas styling", "component upload" | `/drupal-planner.canvas` |
| "search", "Search API", "Solr", "Elasticsearch", "discovery", "autocomplete" | `/drupal-planner.search` |
| General feature, module, migration, or multi-concern request | Stay with `/drupal-planner` (covers all 10 phases) |

When a request spans multiple subsystems (e.g., "plan a new events system" touches content model + taxonomy + search), use the main `/drupal-planner` for the overall architecture and suggest sub-planners for deep-dive phases.

## Purpose

Use Drupal Planner when you need to:
- Design a new feature (e.g., "add product reviews with ratings")
- Plan a new content type, config entity, or field structure
- Make contrib vs custom decisions
- Plan a configuration schema for a custom module
- Design a migration from an existing site
- Plan permission and access control models
- Design a caching strategy for performance-critical features
- Plan hooks, plugins, services, and event subscribers
- Refactor an existing Drupal architecture to fix performance or maintainability issues

## Use_When

- User says "plan the architecture for X", "design the data model for Y", "how should we structure Z in Drupal"
- User is about to build a new Drupal module, custom entity type, or config entity
- User needs to decide between contrib modules and custom code
- User is migrating from an existing site and needs to plan the content model
- User is designing a feature that spans multiple entity types or modules
- User has a drupal-critic REVISE finding and needs architectural fixes
- User is implementing a permission model or access control strategy
- User needs to plan cache tags/contexts for a performance-critical feature

## Do_Not_Use_When

- User wants to review existing Drupal code for bugs/style/correctness — use drupal-critic instead
- User wants to write Drupal code or implement a feature — use their development workflow instead
- User wants general Drupal knowledge (what's an entity? how does the cache API work?) — answer directly
- User is just asking a question, not designing something — answer directly instead

## Companion_Skills

**Sub-planners (for focused subsystem planning):**
- `drupal-planner.content-model`: Deep content model architecture
- `drupal-planner.taxonomy`: Taxonomy and classification architecture
- `drupal-planner.theme`: Theme and frontend architecture
- `drupal-planner.canvas`: Canvas Code Component architecture
- `drupal-planner.search`: Search and discovery architecture

**Design phase (always use if installed):**
- `brainstorming` (obra/superpowers): Explore multiple Drupal architectures before committing.
- `writing-plans` (obra/superpowers): Convert the Drupal design into implementation tasks.

**Code understanding:**
- `code-archaeology` (flonat/claude-research): Understand existing Drupal modules before planning modifications.

**Implementation:**
- `test-driven-development` (obra/superpowers): TDD for Drupal with PHPUnit and Kernel tests.
- `executing-plans` (obra/superpowers): Batch execution with checkpoints.

**Verification:**
- `drupal-critic` (drupal-critic): Harsh code review at checkpoints.
- `drupal-coding-standards` (zivtech-claude-skills): Drupal coding standards compliance.

## Steps

1. **Identify the scope**: Determine what Drupal implementation needs planning. If no arguments provided, ask the user what they want to plan.

2. **Route check**: If the request is clearly focused on content model, taxonomy, theme, or search, suggest the appropriate sub-planner. If it spans multiple concerns, proceed with the full planner.

3. **Check for companion skills**: Check if brainstorming, code-archaeology are installed. If brainstorming is available AND this is a new feature (not a fix), invoke it first.

4. **Understand the context**:
   - If modifying/extending existing code, invoke code-archaeology first to understand current entity structure, modules, services, hooks
   - Detect Drupal version from composer.json or code (Drupal 7, 10, 11, CMS)
   - Identify existing conventions: entity types, field naming, module structure, config export strategy
   - Understand what's driving the architecture: performance requirements? Multi-tenancy? Legacy migration? SEO? Content workflow?

5. **Route to planner agent**: Delegate planning to the drupal-planner agent.
   - **With oh-my-claudecode (preferred)**: `Agent(subagent_type="oh-my-claudecode:drupal-planner", model="opus", prompt=<planning_prompt>)`
   - **Without oh-my-claudecode**: `Agent(subagent_type="drupal-planner", model="opus", prompt=<planning_prompt>)`

6. **Return the plan**: Present the plan document to the user and offer execution options.

## Tool_Usage

- Use the Agent tool to delegate planning to a subagent with the full protocol
- Use Read to examine existing modules, entity types, hooks, and services if modifying existing code
- Use Grep to find patterns: entity types, bundle definitions, hook implementations, service definitions
- Use Bash to analyze composer.json for Drupal version detection, module dependencies
- Write the plan document to `docs/plans/` in the project

## References

- [Contrib Evaluation Rubric](references/contrib-evaluation-rubric.md) — Decision framework for contrib vs custom module decisions
- [Drupal Planning Rubric](references/drupal-planning-rubric.md) — Quality checklist for planning output
- [Sub-Planner Routing Map](references/sub-planner-routing-map.md) — Detailed routing logic for sub-planner selection

## Final_Checklist

- [ ] Did I understand the feature scope and risk level?
- [ ] Did I route to the right planner (main vs sub-planner)?
- [ ] Did I analyze existing architecture (if modifying code)?
- [ ] Did I detect the Drupal version (7, 10, 11, CMS)?
- [ ] Does every entity type have a one-sentence purpose and relationships documented?
- [ ] Does every custom module justify why a contrib module doesn't solve it?
- [ ] Does the permission model exist with role→permission→rationale mapping?
- [ ] Does every config item have a classification (simple config vs config entity vs state)?
- [ ] Does the cache strategy specify tags, contexts, and max-age for each cacheable item?
- [ ] Does the migration plan (if needed) have idempotency and rollback strategy?
- [ ] Did I plan the theme/render (templates, preprocess, accessibility)?
- [ ] Did I break down implementation into TDD tasks with review checkpoints?
- [ ] Did I identify drupal-critic review checkpoints at appropriate stages?
