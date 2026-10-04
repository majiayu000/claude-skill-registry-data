---
name: plan
description: Comprehensive feature planning before implementation. Gathers requirements, designs all layers (domain, data, presentation), identifies data sources, and creates an implementation roadmap with skill references. Use BEFORE creating any new feature to ensure complete understanding and proper architecture.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebFetch
---

# Plan - Feature Planning & Specification

Comprehensive feature planning that understands the WHOLE feature before any implementation begins. Creates a specification document that provides full context to all other skills.

## Why Planning First?

Without planning, each skill works in isolation:
- `/feature-init` creates scaffolds without knowing API structure
- `/api` creates data layer without knowing what UI needs
- Screens get built without knowing what data is available
- **Result**: Mismatches, rework, incomplete interfaces

With planning:
- Domain models match both API structure AND UI needs
- Repository interfaces have exactly the methods required
- Data sources are properly identified upfront
- Implementation order prevents circular dependencies
- **Result**: Clean, complete, working feature

## When to Use This Skill

- **Always** before creating a new feature
- When adding significant functionality to existing features
- When the feature involves multiple data sources
- When the feature has complex user flows
- User asks to "plan", "design", or "architect" a feature

## Workflow

### Phase 1: Discovery

Ask comprehensive questions covering:
- Overview (name, purpose, users)
- Domain model (entities, fields, relationships)
- Data sources (API, Supabase, local storage)
- User flows (screens, navigation, actions)
- Business rules (validation, computed properties)
- Edge cases (empty, offline, cancelled)

**See:** [questions.md](questions.md) for the complete question bank.

### Phase 2: Design

Based on discovery, design each layer:

**Domain Layer:**
- Define entities with all fields and types
- Define repository interface with all needed methods
- Identify enums and value objects

**Data Layer:**
- Identify all data sources
- Design DTOs/Models for each source
- Plan error handling strategy
- Design caching/offline strategy if needed

**Presentation Layer:**
- Define each screen's purpose and data requirements
- Define state types for each screen
- Define provider methods
- Plan navigation flow
- Add "Notes for Design" with constraints (NOT layout)

### Phase 3: Document

Create the specification document at:
```
lib/features/{feature}/.spec.md
```

Or if the feature doesn't exist yet:
```
docs/features/{feature}.spec.md
```

### Phase 4: Implementation Roadmap

List the implementation steps with skill references:

```markdown
## Implementation Order

| Step | Skill | Creates | Depends On |
|------|-------|---------|------------|
| 1 | /domain | Entities, Repository interface | - |
| 2 | /data --source=X | Data layer for source X | 1 |
| 3 | /api | REST API integration | 1 |
| 4 | /screen list | List screen + provider | 1, 2/3 |
| 5 | /screen detail | Detail screen + provider | 1, 2/3 |
| 6 | /i18n | Localized strings | 4, 5 |
| 7 | /testing | Tests | All above |
| 8 | /design | UI polish | 4, 5 |
| 9 | /a11y | Accessibility | 4, 5 |
```

## Commands

```bash
# Create new spec from scratch
/plan {feature_name}

# Review existing spec
/plan {feature_name} --review

# Update spec after changes
/plan {feature_name} --update
```

## Output Format

The planning skill creates a `.spec.md` file with sections for:

1. **Overview** - Feature purpose and scope
2. **Domain Layer** - Entities, enums, repository interface
3. **Data Layer** - Sources, DTOs, implementation strategy
4. **Presentation Layer** - Screens, states, providers
5. **User Flows** - Screen-by-screen interactions
6. **Implementation Order** - Skill invocation sequence
7. **Open Questions** - Anything needing clarification

See [templates.md](templates.md) for the full specification template.

## Integration with Other Skills

After planning is complete, skills read from the spec:

| Skill | Reads From Spec |
|-------|-----------------|
| `/domain` | Entities, Repository interface |
| `/api` | Endpoints, DTOs, error handling |
| `/data` | Data sources, caching strategy |
| `/screen` | Screen designs, states, providers |
| `/i18n` | User-facing text, error messages |
| `/testing` | All layers for test coverage |
| `/design` | Screen layouts, interactions |
| `/a11y` | Interactive elements for labels |

## Checklist

Before finalizing the spec:

- [ ] All entities have complete field definitions
- [ ] Repository interface has all methods UI needs
- [ ] All data sources identified with operations
- [ ] All screens designed with states and actions
- [ ] Navigation flow is complete
- [ ] Error states are handled
- [ ] Empty states are handled
- [ ] Offline behavior defined (if applicable)
- [ ] Implementation order has no circular dependencies
- [ ] Open questions are resolved or documented

## Guides

| Guide | Use For |
|-------|---------|
| [architecture.md](architecture.md) | Established patterns (Clean Architecture, Riverpod, Storage) |
| [templates.md](templates.md) | Specification document template |
| [examples.md](examples.md) | Complete "memories" feature example |
| [questions.md](questions.md) | Discovery question bank by feature type |

## Tips

1. **Don't skip discovery** - Incomplete requirements lead to rework
2. **Be specific about fields** - "id, title, createdAt" not "some fields"
3. **Think about all states** - Loading, empty, error, success
4. **Consider edge cases** - What if offline? What if cancelled?
5. **Document assumptions** - If you're guessing, write it down
6. **Ask when unsure** - Better to clarify than to assume wrong

## Architecture Foundation

The `/plan` skill designs feature-specific architecture that builds on the project's established patterns. See [architecture.md](architecture.md) for:

- Clean Architecture pattern (domain/data/presentation)
- Riverpod AsyncNotifier pattern with disposal safety
- Storage strategy (SecureStorage vs SharedPrefs)
- Feature module structure
- Code style guidelines

The spec should define:
- **What** entities/fields exist for this feature
- **What** data sources are needed
- **What** screens/states/actions exist
- **How** data flows through the layers (repository → provider → screen)

But NOT redefine:
- Overall architecture pattern (already in architecture.md)
- Riverpod notifier structure (already in architecture.md)
- Storage strategy decisions (already in architecture.md)

## What NOT to Include

The `/plan` skill focuses on **requirements and data**. Other skills handle their domains:

| Plan Specifies | Handled By |
|----------------|------------|
| What data/fields exist | Plan ✓ |
| What actions are possible | Plan ✓ |
| What states exist (loading, error, etc.) | Plan ✓ |
| Error types and recovery actions | Plan ✓ |
| Data sources (what, not how) | Plan ✓ |
| How things are laid out visually | `/design` |
| Actual error/success messages | `/i18n` |
| Accessibility labels | `/a11y` |
| Test cases | `/testing` |
| Detailed DTOs, schemas, mappings | `/api` |

**Bad (overstepping):**
> "Grid layout with 3 columns, FAB in bottom-right"
> "Error message: 'Could not upload photo'"
> Detailed Supabase table schema with column types

**Good (requirements only):**
> "Display list of items with sync status indicator"
> "Error type: Upload failed → Recovery: Retry option"
> "Data source: Supabase Database for CRUD operations"

## Related Skills

- `/feature-init` - Initialize feature scaffold (run after /plan)
- `/domain` - Fill in domain layer from spec
- `/data` - Fill in data layer from spec
- `/i18n` - Add localized strings after implementation
- `/testing` - Create tests for all layers
- `/design` - Polish UI after scaffolding
- `/a11y` - Add accessibility after UI is complete
