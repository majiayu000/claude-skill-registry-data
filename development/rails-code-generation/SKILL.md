---
name: Rails Code Generation
description: This skill should be used when the user asks to "generate Rails code", "create a model", "create a controller", "add a migration", "write Rails tests", "set up background jobs", "configure Rails app", or discusses Rails conventions, best practices, ActiveRecord patterns, Hotwire/Stimulus, ViewComponent, RSpec testing, or Ruby on Rails development. Based on Evil Martians' AGENTS.md.
version: 1.0.0
---

# Rails Code Generation Standards

Practical standards for AI-assisted Rails development from Evil Martians. Generated code should be so simple and clear that reading it feels like reading well-written documentation.

## Core Principles

1. **Follow Rails conventions** - Leverage the framework, don't fight it
2. **Use domain language** - Name models after business concepts (Participant vs User, Cloud vs GeneratedImage)
3. **Keep logic at appropriate layers** - Models for business logic, controllers for HTTP, jobs for async
4. **Write readable code** - Code should be self-documenting without comments
5. **Normalize data properly** - One concern per table, use foreign keys and constraints

## Quick Reference

### File Structure

```
app/models/           # Including namespaced classes (Cloud::CardGenerator)
app/controllers/      # Namespaced for auth scoping (Participant::CloudsController)
app/jobs/             # Background work with ActiveJob
app/forms/            # Multi-model operations only
app/policies/         # Complex authorization (ActionPolicy)
app/views/            # ERB + ViewComponent
app/frontend/         # Stimulus controllers, styles
config/configs/       # Anyway Config classes
```

**Critical**: No `app/services/`, `app/contexts/`, or `app/operations/` folders. Extract complex operations to namespaced model classes.

### Model Organization Order

1. Gems/DSL extensions
2. Associations (with `counter_cache: true`)
3. Enums (for state machines)
4. Normalizations (Rails 7.1+)
5. Validations
6. Scopes
7. Callbacks
8. Delegations
9. Public methods
10. Private methods

### Controller Target

5-10 lines per action. No business logic. Guard clauses for early returns.

```ruby
def create
  return head :forbidden unless current_participant.can_create_cloud?

  @cloud = current_participant.clouds.create!(cloud_params)
  CloudProcessingJob.perform_later(@cloud)
  redirect_to @cloud
end
```

### Technology Stack

**Required gems**: Rails, Puma, Propshaft, PostgreSQL, Hotwire (Turbo + Stimulus), ViewComponent, Vite Rails, SolidQueue, ActionPolicy, Anyway Config, RSpec + FactoryBot, Standard, Nanoid + FriendlyID, HTTParty

**Forbidden**: Devise, CanCanCan, ActiveAdmin, service object gems, state machine gems, dry-types/Virtus

## Building Block References

Consult these reference files for detailed patterns:

| Reference | Content |
|-----------|---------|
| `references/stack.md` | Complete gem list, file structure, forbidden patterns |
| `references/models.md` | Model organization, enums, validations, extraction patterns |
| `references/controllers.md` | Thin controllers, namespacing, guard clauses |
| `references/database.md` | Schema design, constraints, indexes, migrations |
| `references/jobs.md` | ActiveJob::Continuable, workflow orchestration |
| `references/views.md` | Hotwire, ViewComponent, Stimulus patterns |
| `references/forms-queries.md` | Form objects, query objects, when to use |
| `references/testing.md` | RSpec organization, what to test |
| `references/configuration.md` | Anyway Config patterns, environment variables |
| `references/anti-patterns.md` | Common mistakes with alternatives, deployment checklist |

## Decision Flowchart

**Where does this logic belong?**

- Single model operation → Model method
- Multi-model transaction → Form object
- External API call → Namespaced model class (e.g., `Cloud::CardGenerator`)
- Async work → Job (orchestrates, doesn't execute)
- Complex query → Query object or scope
- Authorization → Policy (ActionPolicy)
- Configuration → Anyway Config class

**When to extract from model?**

- Method > 15 lines → Extract to namespaced class
- Calls external API → Extract to namespaced class
- Shared across models → Extract to concern or module

## Code Generation Checklist

Before generating Rails code, verify:

- [ ] Models named after business domain concepts?
- [ ] Model follows organization order?
- [ ] States implemented as enums?
- [ ] Controllers under 10 lines per action?
- [ ] Complex logic extracted appropriately?
- [ ] Database normalized with FK constraints?
- [ ] Counter caches on has_many associations?
- [ ] Workflows orchestrated through jobs?
- [ ] Configuration via Anyway Config (not ENV)?
- [ ] Tests organized by type (model/request/system)?

## Usage

When generating Rails code:

1. Check `references/stack.md` to verify gem choices
2. Follow patterns in the relevant building block reference
3. Consult `references/anti-patterns.md` to avoid common mistakes
4. Run through the checklist above before finalizing

For specific patterns, read the appropriate reference file based on what component is being generated.
