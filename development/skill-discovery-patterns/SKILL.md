---
name: Skill Discovery Patterns
description: How the Rails Enterprise Dev plugin discovers and uses project skills dynamically
version: 1.0.0
---

# Skill Discovery Patterns

## Overview

The Rails Enterprise Dev plugin is **generic and reusable** across all Rails projects. It automatically discovers and uses skills from your project's `.claude/skills/` directory, adapting its behavior to whatever patterns and knowledge are available.

## Discovery Process

### 1. Automatic Skill Scanning

At workflow start, the plugin scans `.claude/skills/` to find available skills:

```bash
# Plugin executes skill discovery
bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/discover-skills.sh

# Categorizes skills by naming patterns:
# - core_rails: rails-conventions, rails-error-prevention
# - data_layer: activerecord-patterns, *model*, *database*
# - service_layer: service-object-patterns, api-development-patterns
# - async: sidekiq-async-patterns, *job*, *async*
# - ui: viewcomponents-specialist, hotwire-patterns, tailadmin-patterns
# - i18n: localization, *translation*
# - testing: rspec-testing-patterns, *spec*, *test*
# - domain: Any skill not matching known patterns
```

### 2. Skill Inventory Storage

Discovered skills are stored in settings file for quick access:

```yaml
# .claude/rails-enterprise-dev.local.md
---
available_skills:
  core:
    - rails-conventions
    - rails-error-prevention
    - codebase-inspection
  data:
    - activerecord-patterns
  service:
    - service-object-patterns
    - api-development-patterns
  ui:
    - viewcomponents-specialist
    - hotwire-patterns
    - tailadmin-patterns
  domain:
    - manifest-project-context  # Auto-detected!
---
```

### 3. Dynamic Skill Invocation

Throughout the workflow, agents check for and use available skills:

```markdown
## Example: Database Implementation Phase

1. Check skill inventory: activerecord-patterns available? YES
2. Invoke skill: "I need guidance from activerecord-patterns skill for implementing User model"
3. Extract patterns: N+1 prevention, association patterns, validation strategies
4. Delegate to Data Lead agent with skill context
5. Validate implementation against skill best practices
```

## Skill Categories

### Core Rails Skills (Universal)

**Purpose**: Fundamental Rails patterns applicable to all projects

**Skills**:
- `rails-conventions` - MVC architecture, naming conventions, file organization
- `rails-error-prevention` - Common pitfalls, preventive checklists
- `codebase-inspection` - Pre-implementation analysis procedures

**When Used**: All workflows (inspection, planning, validation)

**Example Invocation**:
```
Before planning, invoke rails-conventions skill to understand:
- Service object patterns in this project
- Controller organization
- Testing conventions
```

### Data Layer Skills

**Purpose**: Database schema, models, queries, associations

**Skills**:
- `activerecord-patterns` - Query optimization, associations, scopes
- Custom: `*model*`, `*database*`, `*schema*`

**When Used**: Database migration and model implementation phases

**Example Invocation**:
```
For User authentication model, invoke activerecord-patterns:
- How to prevent N+1 queries
- Association patterns for has_many :through
- Scope best practices
- Validation strategies
```

### Service Layer Skills

**Purpose**: Business logic, API design, service objects

**Skills**:
- `service-object-patterns` - Service layer architecture
- `api-development-patterns` - RESTful API, serialization
- Custom: `*service*`, `*api*`

**When Used**: Service and controller implementation phases

**Example Invocation**:
```
For payment processing service, invoke service-object-patterns:
- Callable concern usage
- Namespace patterns ({Domain}Manager::{Action})
- Error handling strategies
- Transaction management
```

### Async Skills

**Purpose**: Background jobs, queues, schedulers

**Skills**:
- `sidekiq-async-patterns` - Background job design
- Custom: `*job*`, `*async*`, `*queue*`

**When Used**: Background job implementation phase

**Example Invocation**:
```
For invoice generation job, invoke sidekiq-async-patterns:
- Job idempotency patterns
- Retry strategies
- Queue priority configuration
- Scheduled job patterns
```

### UI Skills

**Purpose**: Components, views, frontend frameworks

**Skills**:
- `viewcomponents-specialist` - ViewComponent architecture
- `hotwire-patterns` - Turbo Frames, Streams, Stimulus
- `tailadmin-patterns` - TailAdmin UI framework
- Custom: `*component*`, `*view*`, `*ui*`, `*frontend*`

**When Used**: Component and view implementation phases

**Example Invocation**:
```
For user profile component, invoke:
1. viewcomponents-specialist - Component structure, method exposure
2. tailadmin-patterns - UI styling, color schemes, card layouts
3. hotwire-patterns - Real-time updates with Turbo Streams

Extract:
- TailAdmin card patterns (bg-blue-50, rounded corners)
- ViewComponent slots for customization
- Stimulus controller for interactions
```

### I18n Skills

**Purpose**: Internationalization, localization, translations

**Skills**:
- `localization` - Multi-language support, RTL, pluralization
- Custom: `*i18n*`, `*translation*`

**When Used**: Localization implementation phase

**Example Invocation**:
```
For Arabic translation support, invoke localization:
- YAML structure for translations
- RTL CSS patterns
- Locale switcher component
- Date/time formatting
- Pluralization rules
```

### Testing Skills

**Purpose**: Test strategies, specs, coverage

**Skills**:
- `rspec-testing-patterns` - Unit, integration, system tests
- Custom: `*spec*`, `*test*`

**When Used**: Test implementation phase

**Example Invocation**:
```
For comprehensive test suite, invoke rspec-testing-patterns:
- Factory patterns
- Shared examples
- Request spec structure
- System test patterns
- Mocking strategies
```

### Domain Skills (Project-Specific)

**Purpose**: Business domain knowledge, project-specific context

**Skills**: Any skill not matching known patterns
- `manifest-project-context` - Manifest LMS domain knowledge
- `ecommerce-domain` - E-commerce business logic
- `healthcare-domain` - Healthcare compliance, HIPAA
- Custom project domains

**When Used**: Inspection and planning phases (optional context)

**Example Invocation**:
```
For shipment tracking feature, invoke manifest-project-context:
- Understanding Task model (shipments)
- Bundle concept (delivery routes)
- Carrier relationships
- State machine flows
- Locality/Zone geography
```

## Graceful Degradation

**If a skill is not available**, the plugin continues with agent's general knowledge:

```markdown
## Example: Project Without tailadmin-patterns

User: /rails-dev add dashboard

Workflow:
1. Check for tailadmin-patterns skill → NOT FOUND
2. Check for custom UI skill → NOT FOUND
3. Log: "No UI framework skill found, using general Rails view patterns"
4. Proceed with standard Rails ERB views
5. Suggest: "Consider adding tailadmin-patterns skill for consistent UI"
```

**No workflow failure** - plugin adapts to available skills.

## Custom Skill Integration

### Adding Project-Specific Skills

1. Create skill directory:
```bash
mkdir -p .claude/skills/my-custom-skill
```

2. Add SKILL.md with patterns:
```markdown
---
name: My Custom Patterns
description: Our team's coding standards
---

# My Custom Patterns

## Service Layer
- Always use dry-transaction gem
- Include CustomLogging concern
...
```

3. Plugin auto-discovers on next run:
```bash
/rails-dev add feature
# Plugin scans .claude/skills/
# Finds: rails-conventions, activerecord-patterns, my-custom-skill
# Uses my-custom-skill during implementation
```

### Naming Conventions for Auto-Categorization

**Data layer skills**:
- `activerecord-*`
- `*-model-*`
- `*-database-*`
- `*-schema-*`

**Service layer skills**:
- `service-*`
- `*-service-*`
- `api-*`
- `*-api-*`

**UI skills**:
- `*-component*`
- `*-view*`
- `*-ui-*`
- `*-frontend-*`
- `hotwire-*`
- `turbo-*`
- `stimulus-*`

**Domain skills** (anything else):
- `*-domain`
- `*-context`
- `*-business-*`
- Project-specific names

## Multi-Project Example

### Project A: Manifest LMS (Full Stack)

```
.claude/skills/
├── rails-conventions/
├── rails-error-prevention/
├── codebase-inspection/
├── activerecord-patterns/
├── service-object-patterns/
├── api-development-patterns/
├── sidekiq-async-patterns/
├── viewcomponents-specialist/
├── hotwire-patterns/
├── tailadmin-patterns/       ← TailAdmin UI
├── localization/
├── rspec-testing-patterns/
├── devops-lead/
├── requirements-writing/
└── manifest-project-context/ ← Domain specific
```

**Plugin adapts**: Full feature set with all skills

### Project B: Simple API (Minimal)

```
.claude/skills/
├── rails-conventions/
├── activerecord-patterns/
├── service-object-patterns/
├── api-development-patterns/
└── rspec-testing-patterns/
```

**Plugin adapts**: API-focused workflow, no UI skills used

### Project C: Different UI Framework

```
.claude/skills/
├── rails-conventions/
├── activerecord-patterns/
├── bootstrap-patterns/       ← Bootstrap instead of TailAdmin
└── jquery-patterns/          ← jQuery instead of Hotwire
```

**Plugin adapts**: Uses bootstrap-patterns and jquery-patterns for UI

## Skill Invocation Protocol

### Format for Agent Skill Requests

```markdown
I need guidance from the [skill-name] skill for [specific task].

Context:
- Feature: User authentication
- Component: JWT service
- Phase: Service implementation

Questions:
- What service pattern should I follow?
- How to handle token refresh?
- Where to store refresh tokens?

This will inform Backend Lead agent when implementing AuthManager::GenerateToken service.
```

### Skill Response Integration

```markdown
Based on [skill-name] skill guidance:

Patterns to follow:
1. Use Callable concern (from service-object-patterns)
2. Namespace: AuthManager (from project conventions)
3. Return Result object (from service-object-patterns)

Implementation requirements:
- JWT expiry: 15 minutes (access), 7 days (refresh)
- Store refresh tokens in encrypted database column
- Invalidate on logout

Passing this to Backend Lead for implementation.
```

## Workflow Integration

### Phase-Specific Skill Usage

**Inspection Phase:**
```markdown
Skills invoked:
- codebase-inspection (mandatory if available)
- rails-conventions (understand patterns)
- domain skills (business context)

Purpose: Understand existing codebase before planning
```

**Planning Phase:**
```markdown
Skills invoked:
- rails-error-prevention (preventive checklist)
- rails-conventions (pattern selection)
- requirements-writing (if user stories needed)
- domain skills (business rules)
- phase-specific skills (api, ui, async based on feature type)

Purpose: Create implementation plan with skill-informed decisions
```

**Implementation Phase:**
```markdown
Skills invoked per layer:
- Database: activerecord-patterns, domain skills
- Models: activerecord-patterns, domain skills
- Services: service-object-patterns, api-development-patterns
- Jobs: sidekiq-async-patterns
- Components: viewcomponents-specialist, ui framework skills
- Views: ui framework skills, hotwire-patterns, localization
- Tests: rspec-testing-patterns

Purpose: Ensure each layer follows established patterns
```

**Review Phase:**
```markdown
Skills invoked:
- rails-error-prevention (validation checklist)
- All used implementation skills (verify adherence)

Purpose: Validate implementation against skill guidelines
```

## Benefits of Skill Discovery

1. **Portability**: Same plugin works across all Rails projects
2. **Flexibility**: Adapts to available skills and patterns
3. **Extensibility**: Easy to add project-specific knowledge
4. **Consistency**: All implementations reference same skills
5. **Knowledge Capture**: Skills document team conventions
6. **Onboarding**: New developers reference skills
7. **Quality**: Consistent patterns across codebase

## Troubleshooting

### Skill Not Found

**Symptom**: Plugin says "Skill not available: my-skill"

**Solution**:
1. Check skill exists in `.claude/skills/my-skill/`
2. Ensure SKILL.md file present
3. Restart Claude Code
4. Re-run skill discovery: `bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/discover-skills.sh`

### Skill Not Categorized Correctly

**Symptom**: Domain skill categorized as UI skill

**Solution**:
1. Rename skill to match category patterns
2. Or: Accept categorization (doesn't affect functionality)
3. Plugin still invokes skill based on content, not category

### Multiple Domain Skills

**Symptom**: Project has multiple domain skills

**Solution**:
- Plugin invokes all domain skills during inspection/planning
- Agents synthesize information from all domain skills
- This is normal for large/complex projects

## Summary

The skill discovery system makes the Rails Enterprise Dev plugin:
- **Generic**: Works with any Rails project
- **Adaptive**: Uses whatever skills available
- **Extensible**: Easy to add custom patterns
- **Resilient**: Graceful degradation if skills missing
- **Maintainable**: Skills separate from plugin code

**Key principle**: Plugin provides workflow orchestration, skills provide project-specific knowledge.
