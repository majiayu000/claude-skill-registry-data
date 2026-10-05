---
name: content-model-planner
description: "Plan CMS content models — entity types, field architecture, content relationships."
version: 0.1.0
---

# Content Model Planner

Planner skill for designing content model architectures *before* implementing them.

Use this skill to design content models that are editorial-friendly, maintainable, scalable, and migration-safe.

## JTBD (Jobs To Be Done)

### Primary Job
When I need to build or redesign a CMS content model but haven't yet resolved how entities should be composed, which fields should be shared, or how editorial workflows should map to the structure,
I want a complete content model architecture plan before any CMS configuration starts,
so I can avoid the field duplication, entity proliferation, and editorial confusion that harden into technical debt once the model is live.

### Secondary Jobs
- When the same content concept keeps appearing across multiple entity types with slightly different field names and no clear reuse strategy, I want a field architecture that eliminates duplication at the source, so I can stop maintaining the same metadata in five places.
- When I'm migrating content from one platform to another and the old model doesn't map cleanly, I want a new model designed with migration safety in mind — circular references identified, cardinality conflicts resolved, rollback possible — before the data move begins.
- When editors are confused about which content type to use or are working around the model rather than with it, I want a design that matches how they actually organize and publish content, not how the CMS categorizes features.

### Job Layers
- Functional: Produce a complete content model specification covering entity type definitions with composition justifications, shared field architecture, taxonomy integration, reference mapping, editorial workflow alignment, caching strategy, migration plan, and governance model.
- Emotional: Reduce the anxiety of CMS configuration decisions that are expensive to undo — choosing the wrong composition pattern, creating circular references, or building a model editors find unusable.
- Social: Helps the user present a model that developers, content strategists, and editorial staff can all understand and agree on, with each type's existence justified rather than assumed.

### This Skill Is For
- A user designing a new CMS content model who needs entity types, field bundles, and taxonomy vocabularies locked before a developer begins CMS configuration.
- A user redesigning an existing model that has grown through entity proliferation, field duplication, or naming chaos without a unifying architecture.
- A user planning a content migration who needs the target model designed with mapping, conflict resolution, and rollback built in.
- A user whose model is technically valid but editorially broken: editors don't know which type to use, fields are duplicated across types, or workflow states don't match how content actually moves.

### This Skill Is NOT For
- A user with an existing content model who needs a quality verdict rather than a new plan; use `content-model-critic` instead.
- A user needing a quick one-off CMS field addition with no architecture question in scope.

### Paired With
- `content-model-critic`: Use after the content model is designed to audit entity boundaries, field reuse, taxonomy coupling, reference patterns, and workflow alignment before implementation.
- `taxonomy-planner`: Use when the unresolved problem is vocabulary structure and classification design rather than entity composition and field architecture.
- `search-discovery-planner`: Use when the content model needs to provide specific fields for a search index and the two systems need to be designed in tandem.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| New content model with no existing architecture | The skill defines entity types, composition patterns, field bundles, taxonomy vocabularies, and reference relationships | A complete model specification ready for CMS configuration |
| Redesigning a model with proliferation or duplication | The skill audits current entities for consolidation opportunities, then redesigns with field reuse and naming conventions | A refactoring plan with before/after entity mapping |
| Planning a content migration | The skill designs the target model with migration mapping, cardinality conflict resolution, and rollback strategy | A migration-safe model with an executable mapping table |
| Model is built but editors can't use it effectively | The skill surfaces the workflow mismatches and field architecture gaps, then designs corrections | A fix plan targeting the specific editorial friction points |

### When to Escalate
- If the user already has an implemented or drafted model and needs it reviewed rather than redesigned, escalate to `content-model-critic`.
- If the unresolved problem is classification and vocabulary design rather than entity composition and field architecture, escalate to `taxonomy-planner`.

## Purpose

Design content models strategically, not reactively:

- **Define the scope**: What content types exist? What are editorial workflows?
- **Choose composition patterns**: When is something a type vs bundle vs paragraph vs component?
- **Plan field architecture**: Which fields are shared? Create field bundles for reuse.
- **Integrate taxonomies**: Design vocabularies that are reusable, not coupled to one type.
- **Map entity references**: Identify relationships, circular dependencies, query patterns.
- **Align editorial workflows**: Model the way editors actually work, not force them into patterns.
- **Plan for performance**: Design caching strategy, identify N+1 query risks, ensure scalability.
- **Enable migration**: Create data models that can migrate cleanly between platforms.
- **Document governance**: Who owns types? How are new fields approved? What's the naming convention?
- **Design for growth**: Will this model scale to 10x content volume?

This skill produces a detailed content model specification that guides implementation and prepares for content-model-critic review.

## Use_When

- Planning a new content model for a CMS platform (Drupal, WordPress, Contentful, Statamic, custom headless)
- Redesigning an existing content model that has grown confusing or constraining
- Consolidating or merging multiple content models from different systems
- Migrating content from one platform to another and need to design the new model
- Architecting a platform with complex content relationships (products, reviews, related content)
- Designing editorial workflows where content management structure is critical
- Planning a multi-tenant or multi-brand platform with shared content model
- Building a knowledge base or documentation system with reusable components
- Creating a platform with faceted navigation requiring careful taxonomy design
- Establishing content governance, naming conventions, and composition patterns

## Do_Not_Use_When

- You've already created a content model and want architectural critique (use content-model-critic instead)
- You need a quick ad-hoc structure for one-off content without formal governance
- The content set is too small to warrant architecture planning (simple blog with 2-3 post types)
- You're just learning content modeling basics (use content-modeling standards reference instead)
- You're implementing a specific CMS feature (use drupal-planner for Drupal-specific implementation)

## Companion_Skills

- **content-model-critic**: Use AFTER designing content model to review architecture, identify entity proliferation, field duplication, taxonomy coupling, workflow misalignment, circular references, performance risks
- **taxonomy-planner**: Use when planning complex vocabulary structures that integrate with content model
- **drupal-planner**: Use when implementing content model in Drupal (content types, fields, paragraphs)
- **wordpress-planner**: Use when implementing content model in WordPress (post types, taxonomies, meta fields)

## Steps

1. **Define content scope and platform context**: Provide context about:
   - What content types exist or are needed? (articles, products, people, events, pages, etc.)
   - CMS platform (Drupal, WordPress, Contentful, custom headless?) and version?
   - Current content volume and growth trajectory?
   - Editorial team size and workflow patterns?
   - Any existing model pain points (proliferation, duplication, confusion)?

2. **Understand current state (if redesigning)**: Share information about:
   - Current entity types and field structure
   - Current pain points (too many types, field duplication, naming chaos, etc.)
   - Which content types are rarely used? Which are causing editorial confusion?
   - How do editors currently organize their work?
   - Any integration constraints or API requirements?

3. **Invoke the content-model-planner subagent**: Delegate to subagent with full planning protocol:
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

4. **Return planning output**: Present the structured content model design with:
   - Scope & Platform Context
   - Existing Architecture Analysis (if applicable)
   - Entity Type Definitions (table: Name | Purpose | Composition Pattern | Justification)
   - Entity Relationship Diagram (text-based)
   - Field Architecture (shared fields, field bundles, naming convention)
   - Taxonomy Integration Strategy
   - Editorial Workflow Alignment
   - Reference Architecture (relationships, cardinality, circularity assessment)
   - Caching & Performance Strategy
   - CMS Implementation Details
   - Migration Plan (if applicable)
   - Content Governance Model
   - Testing Strategy
   - Implementation Tasks (ordered, with checkpoints)
   - Contract Appendix

The plan guides implementation and CMS configuration. Use content-model-critic to review the completed model.

## Tool_Usage

When invoking content-model-planner:
- Use Read to load existing content models, entity type definitions, field schemas, taxonomy structures
- Use Read to load editorial workflow documentation, CMS documentation, performance requirements
- Use Grep to search for field naming patterns, analyze naming consistency across types
- Use Bash to analyze entity type count, field reuse patterns, reference relationship mapping
- Build a comprehensive understanding of current architecture and editorial workflows before planning

## Related_Skills

- **content-model-critic**: Post-design review of entity types, field architecture, taxonomy coupling, workflow alignment, references, performance, migration readiness
- **taxonomy-planner**: When designing reusable vocabulary structures
- **drupal-planner**: When implementing content model in Drupal
- **wordpress-planner**: When implementing content model in WordPress
- **data-planner**: When designing underlying data schema for headless or custom systems
