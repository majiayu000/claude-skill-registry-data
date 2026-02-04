---
name: modes
description: Domain-specific development mode guidelines for UI, API, database, integration, migration, and specialized workflows. Each mode provides tailored principles, checklists, and patterns for different types of development work.
---

# Development Mode Skills

This skill provides domain-specific guidelines that agents activate based on the type of work being performed. Each mode extends core principles with specialized requirements for different development contexts.

## Overview

The mode skills provide specialized guidance for:
- **UI Mode** (ui.yaml) - Frontend, accessibility, SEO, visual components
- **API Mode** (api.yaml) - REST/GraphQL endpoints, API design, versioning
- **Database Mode** (db.yaml) - Schema design, migrations, query optimization
- **Integration Mode** (integration.yaml) - External service integration, OAuth, webhooks
- **Migration Mode** (migration.yaml) - Data migration, version upgrades, rollback procedures
- **Performance Mode** (performance.yaml) - Optimization, caching, load testing
- **QA Mode** (qa.yaml) - Testing strategies, coverage requirements, test automation
- **Security Mode** (security.yaml) - Security audits, vulnerability scanning, penetration testing
- **Release Mode** (release.yaml) - Deployment procedures, release management, rollback

## When to Use

Modes are automatically activated based on work context:

### UI Mode
- **Used by**: Nova, Skye, Finn
- **Triggers**: Frontend changes, accessibility updates, SEO optimization
- **Focus**: Lighthouse scores, ARIA compliance, responsive design

### API Mode
- **Used by**: Skye, Kai, Mina
- **Triggers**: Endpoint creation, API versioning, integration work
- **Focus**: REST/GraphQL standards, documentation, versioning

### Database Mode
- **Used by**: Leo, Skye, Kai
- **Triggers**: Schema changes, migrations, query optimization
- **Focus**: Data integrity, indexing, rollback safety

### Integration Mode
- **Used by**: Mina, Iris, Kai
- **Triggers**: External service integration (Stripe, Shopify, AWS, etc.)
- **Focus**: OAuth flows, webhook handling, error resilience

### Migration Mode
- **Used by**: Blake, Leo, Kai
- **Triggers**: Database migrations, version upgrades, data transfers
- **Focus**: Rollback procedures, data validation, zero-downtime

### Performance Mode
- **Used by**: Kai, Nova, Theo
- **Triggers**: Optimization work, performance issues, load testing
- **Focus**: Caching strategies, bundle optimization, resource usage

### QA Mode
- **Used by**: Finn, Eden
- **Triggers**: Test creation, coverage validation, quality gates
- **Focus**: Unit/integration/E2E tests, coverage thresholds

### Security Mode
- **Used by**: Iris, Mina, Blake
- **Triggers**: Security audits, vulnerability scans, auth changes
- **Focus**: Secret management, SBOM generation, penetration testing

### Release Mode
- **Used by**: Blake, Eden, Theo
- **Triggers**: Deployment preparation, release coordination
- **Focus**: Changelog generation, deployment verification, rollback readiness

## Mode Structure

Each mode YAML file contains:

```yaml
name: mode-name
extends: [core-skills]           # Inherited core principles
description: |
  Mode-specific description
used_by: [Agent1, Agent2]        # Which agents use this mode
triggers:                         # When to activate this mode
  - trigger_condition_1
  - trigger_condition_2
inputs_required:                  # Required context
  - input_1
  - input_2
outputs:                          # Expected deliverables
  - output_1
  - output_2
principles:                       # Mode-specific guidelines
  - principle_1
  - principle_2
checklist:                        # Validation requirements
  - [ ] checklist_item_1
  - [ ] checklist_item_2
patterns:                         # Common solutions
  - "Pattern description"
hooks:                            # Integration points
  - hook_name
```

## Usage

Agents reference specific modes based on work type:

```markdown
# Nova working on UI
See `skills/modes/ui.yaml` for accessibility and performance requirements

# Leo working on database
See `skills/modes/db.yaml` for migration and schema design guidelines

# Mina integrating Stripe
See `skills/modes/integration.yaml` for OAuth and webhook patterns
```

## File Structure

```
skills/modes/
├── SKILL.md (this file)
├── ui.yaml          # Frontend/accessibility/SEO
├── api.yaml         # REST/GraphQL endpoints
├── db.yaml          # Database schema/migrations
├── integration.yaml # External service integration
├── migration.yaml   # Data migration procedures
├── performance.yaml # Optimization strategies
├── qa.yaml          # Testing requirements
├── security.yaml    # Security audits
└── release.yaml     # Deployment procedures
```

## Mode Inheritance

Modes extend core skills:
- **All modes** inherit from core principles
- **Specific modes** may extend additional core skills (e.g., ui.yaml extends performance, review-checklist, documentation)
- **Agents** apply both core and mode-specific guidelines

## Best Practices

1. **Context-aware activation** - Modes activate based on work type, not manual selection
2. **Layered guidance** - Core principles + mode-specific requirements
3. **Agent specialization** - Each agent knows which modes to apply
4. **Validation gates** - Each mode defines success criteria and checklists
5. **Pattern reuse** - Common solutions documented for consistency

## Integration with Agents

Agents automatically apply relevant modes:
- **Nova** (UI/UX) → ui.yaml, performance.yaml
- **Leo** (Database) → db.yaml, migration.yaml
- **Mina** (Integration) → integration.yaml, security.yaml
- **Blake** (Release) → release.yaml, qa.yaml
- **Iris** (Security) → security.yaml, integration.yaml
- **Finn** (QA) → qa.yaml, performance.yaml
- **Kai** (Architecture) → api.yaml, db.yaml, performance.yaml
- **Skye** (Implementation) → ui.yaml, api.yaml, db.yaml (context-dependent)

## Example Workflow

When Nova receives a UI task:
1. Activates **ui.yaml** mode
2. Inherits principles from **core/performance.yaml**, **core/review-checklist.yaml**
3. Applies Lighthouse A11y ≥ 95 requirement
4. Validates keyboard/screen-reader flows
5. Checks meta tags and OG/Twitter cards
6. Measures CLS < 0.1, LCP within budget

This ensures consistent, high-quality output across all UI work.
