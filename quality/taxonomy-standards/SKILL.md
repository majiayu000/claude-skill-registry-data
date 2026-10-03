---
name: taxonomy-standards
description: >
  Use when creating tags, categories, or organizational structures for knowledge,
  documentation, or data. This skill provides consistent taxonomy standards across
  all companies and agents, enabling discoverability and cross-referencing.
---

# Taxonomy Standards

## Overview
This skill defines standardized taxonomy rules for organizing knowledge, documentation, and data across the enterprise. Consistent taxonomy ensures information is findable, cross-referencable, and understandable by any agent regardless of their company or domain.

## When to Use
- When creating new documentation, knowledge entries, or skill files
- When tagging content with gigabrain tags
- When organizing files in PARA structure
- When creating classification systems for data or documents
- When resolving taxonomy inconsistencies across the enterprise
- **Don't use when:** Working exclusively within a well-established taxonomic system that doesn't need updates

## Core Procedures

### Step 1: Apply Standard Taxonomy Levels
Use this hierarchy for all organizational structures:
1. **Domain:** High-level category (engineering, security, finance, creative)
2. **Subdomain:** Specific area within domain (structural-engineering, threat-protection)
3. **Type:** What kind of content (procedure, reference, analysis, report)
4. **Topic:** Specific subject matter
5. **Tags:** Cross-cutting attributes (automated, critical, deprecated)

### Step 2: Follow Naming Conventions
| Element | Convention | Example |
|---------|------------|---------|
| Directory | lowercase-with-dashes | `security/threat-protection/` |
| File | lowercase-with-dashes.extension | `incident-response/SKILL.md` |
| Tags | lowercase-with-dashes | `cross-team-collaboration` |
| Agent names | lowercase-with-dashes | `sage-promptforge-chief-architect` |
| Companies | PascalCase | `PromptForge AI`, `DevForge AI` |
| PARA levels | lowercase | `projects/`, `areas/`, `resources/`, `pages/` |

### Step 3: Tag Consistently
Gigabrain tag rules:
- Always include company/agent tag (e.g., `promptforge`, `devforge`)
- Always include domain tag (e.g., `security`, `engineering`)
- Always include content type (e.g., `skill`, `procedure`, `analysis`)
- Add situational tags as relevant (e.g., `cross-company`, `urgent`, `deprecated`)
- Maximum 6 tags per item (avoid over-tagging)
- Minimum 2 tags per item (always company + type)

### Step 4: Validate Taxonomy
Before finalizing:
- [ ] Names follow conventions (lowercase-with-dashes for files/dirs)
- [ ] Tags include required minimum (company + content type)
- [ ] No duplicate or near-duplicate terms used
- [ ] Hierarchy is logical and consistent
- [ ] Item is findable by someone searching for this topic

### Step 5: Handle Edge Cases
- **New category doesn't fit existing taxonomy:** Create new entry at appropriate level, document rationale
- **Multiple valid categorizations:** Pick ONE primary, cross-reference from others
- **Taxonomy changes over time:** Update current items, mark old taxonomy as deprecated

## Quality Checklist
- [ ] All naming conventions followed
- [ ] Required tags present on all items
- [ ] Hierarchy is logical and consistent
- [ ] No duplicate terms in taxonomy
- [ ] Item discoverable by target audience
- [ ] Cross-references provided where appropriate

## Error Handling
- **Error:** Content doesn't fit existing taxonomy
  **Response:** Create new taxonomy entry, document it, announce to knowledge managers
- **Error:** Existing content has inconsistent taxonomy
  **Response:** Update during next content review, don't block delivery for taxonomy cleanup

## Cross-Team Integration
**Related Skills:** knowledge-capture, knowledge-retrieval, file-naming-standards, agent-development-standards
**Used By:** ALL agents creating content, especially Archivists, Librarians, documenters, knowledge managers