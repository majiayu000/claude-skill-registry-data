---
name: taxonomy-planner
description: "Plan taxonomy/classification schemes — hierarchy, term relationships, governance rules."
version: 0.1.0
---

# Taxonomy Planner

Planner skill for designing classification and taxonomy systems *before* implementing them.

Use this skill to design taxonomies that organize content intuitively, remain editorially manageable, and support discovery for users.

## JTBD (Jobs To Be Done)

### Primary Job
When I need to build or redesign a taxonomy but haven't yet resolved how deep the hierarchy should go, whether vocabularies should be controlled or free, or how to keep editors from creating synonym duplicates over time,
I want a complete taxonomy design plan before content volume grows,
so I can avoid the orphan terms, overlapping categories, and governance chaos that make taxonomies unusable once they scale.

### Secondary Jobs
- When multiple vocabularies exist across a content model and it's unclear how they relate, overlap, or conflict, I want a vocabulary architecture that makes their relationships explicit and their boundaries clear, so editors know which vocabulary applies to which classification decision.
- When migrating content from an old taxonomy to a new one, I want the term mapping resolved — including many-to-one consolidations, ambiguous assignments, and deprecated terms — before the migration runs, so I don't end up with content stranded without valid categories.
- When a taxonomy needs to power both editorial classification and user-facing faceted navigation, I want a design that serves both audiences, so the same vocabulary works for editors applying terms and users filtering by them.

### Job Layers
- Functional: Produce a complete taxonomy design specification covering vocabulary strategy, hierarchy depth and breadth, term count, mutual exclusivity rules, controlled vs. free tagging decisions, naming conventions, editorial interface, faceted navigation specs, governance model, migration mapping, and testing plan.
- Emotional: Reduce the anxiety of watching a taxonomy degrade over time — "React", "ReactJS", "react.js", "react-js" all existing as separate tags because no governance was set up at the start.
- Social: Helps the user present a classification structure that editorial staff will actually use consistently, users will find intuitive to navigate, and developers can implement without ambiguity.

### This Skill Is For
- A user designing a new taxonomy who needs hierarchy depth, vocabulary strategy, governance rules, and editorial interface specified before any terms are created in the CMS.
- A user redesigning an existing taxonomy that has grown unmanageable: too many levels, orphan terms, synonym proliferation, or faceted navigation that overwhelms users.
- A user migrating content between platforms who needs a term mapping table — including conflict resolution for ambiguous cases — before the data move.
- A user building faceted navigation who needs the taxonomy designed to work for both editorial classification and user-facing filtering simultaneously.

### This Skill Is NOT For
- A user with an existing taxonomy who needs a quality verdict rather than a new design; use `taxonomy-critic` instead.
- A user needing a quick ad hoc categorization with no governance or scale requirements.

### Paired With
- `taxonomy-critic`: Use after the taxonomy is designed to audit hierarchy soundness, term overlap, coverage gaps, and governance before launch.
- `content-model-planner`: Use when the unresolved problem is entity and field architecture rather than classification structure — taxonomies integrate into content models but the two are distinct design problems.
- `search-discovery-planner`: Use when the taxonomy needs to power search facets and the two systems need to be designed in tandem.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| New taxonomy with no existing structure | The skill defines vocabulary strategy, hierarchy, term count, governance, and editorial interface | A complete taxonomy specification ready for CMS implementation |
| Redesigning an unmanageable existing taxonomy | The skill audits current structure for consolidation opportunities, then redesigns with governance built in | A refactoring plan with old-to-new term mapping |
| Planning a content migration | The skill produces a term mapping table with conflict resolution rules and ambiguous-case handling | A migration-safe mapping table with a rollback plan |
| Taxonomy must serve both editors and faceted navigation | The skill designs vocabulary structure that works for both editorial classification and user-facing filtering | A dual-purpose taxonomy spec with editorial interface and facet display specifications |

### When to Escalate
- If the user already has an implemented or drafted taxonomy and needs it reviewed rather than redesigned, escalate to `taxonomy-critic`.
- If the unresolved problem is entity and field architecture rather than classification structure, escalate to `content-model-planner`.

## Purpose

Design taxonomies strategically, not reactively:

- **Define the scope**: What content is being classified? What are the business/editorial goals?
- **Choose structure**: Flat vs. deep? Single vocabulary vs. multiple? Controlled vs. open tagging?
- **Ensure mutual exclusivity**: Can content belong to multiple categories? Where?
- **Plan for exhaustiveness**: Does every content item fit somewhere? What about edge cases?
- **Optimize editorial usability**: Can editors find and apply terms quickly without confusion?
- **Enable discovery**: Do taxonomies power useful faceted navigation and search filtering?
- **Design for growth**: Will this taxonomy scale as content grows and new categories emerge?
- **Support governance**: Who adds terms? How are approvals handled? What's controlled vs. free?
- **Plan migration**: Can existing content be remapped to new categories during migration?
- **Consider language**: Does the structure work across multiple languages?

This skill produces a detailed taxonomy design specification that guides implementation.

## Use_When

- Planning a new taxonomy or vocabulary system for a content platform
- Redesigning an existing taxonomy that's become unmanageable or confusing
- Migrating content from one system to another and need term mapping
- Building a platform with faceted navigation and need to plan the taxonomy structure
- Designing a knowledge base, documentation system, or content hub taxonomy
- Creating product hierarchies, e-commerce categories, or service classifications
- Establishing controlled vocabularies for specific content types or domains
- Planning how multiple taxonomies interact (e.g., categories + tags + topics)

## Do_Not_Use_When

- You've already created a taxonomy and want critique (use taxonomy-critic instead)
- You need a quick ad-hoc categorization system with no governance
- The content set is too small to warrant formal taxonomy planning
- You're just learning taxonomy design basics (use taxonomy-standards reference instead)

## Companion_Skills

- **taxonomy-critic**: Use AFTER designing taxonomies to review structure, governance, and gaps
- **content-model-critic**: Use when planning content models that depend on taxonomy relationships
- **search-discovery-critic**: Use to evaluate how taxonomies support search and discovery
- **drupal-planner**: Use when implementing taxonomies in Drupal vocabularies

## Steps

1. **Define the scope and goals**: Provide context about:
   - What content is being classified? (Blog posts, products, knowledge base articles, etc.)
   - What are the primary business/editorial goals? (Browsable navigation, search filtering, content organization, etc.)
   - Who uses the taxonomy? (Editors, content managers, search algorithms, end users)
   - Any constraints? (Multilingual requirements, API limitations, CMS constraints, etc.)

2. **Understand the current state**: Share information about:
   - Existing taxonomy or classification system (if any)
   - Current pain points (too many categories, confusion, poor governance, etc.)
   - Migration requirements (need to map old terms to new ones?)
   - Scale and growth projections (how much content will grow?)

3. **Invoke the taxonomy-planner subagent**: Delegate to subagent with the full planning protocol:
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

4. **Return planning output**: Present the structured taxonomy design with:
   - Scope and classification goals
   - Existing state analysis and pain points
   - Proposed vocabulary structure (hierarchy, terms, relationships)
   - Editorial implementation specs (how editors apply terms)
   - Faceted navigation design (if applicable)
   - Governance model (who adds terms, approval process)
   - Migration mapping (if transitioning from old taxonomy)
   - Testing and validation plan

The plan guides implementation. Use taxonomy-critic to review the completed taxonomy.

## Tool_Usage

When invoking taxonomy-planner:
- Use Read to load existing taxonomy documentation, data models, or category lists
- Use Grep to search for current taxonomy terms or category assignments
- Use Bash to analyze term usage patterns (frequency, orphaned terms, etc.)
- Understand the content landscape thoroughly before designing new structures

## Related_Skills

- **taxonomy-critic**: Post-design review of taxonomy structure, governance, and usability
- **content-model-critic**: When taxonomy is part of larger content model
- **search-discovery-critic**: When evaluating taxonomy's support for search and discovery
- **drupal-planner**: When implementing taxonomies in Drupal
