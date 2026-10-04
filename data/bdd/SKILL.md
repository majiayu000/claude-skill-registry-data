---
description: BDD spec authoring — create, update, or delete .feature files following best practices
argument-hint: [scope description or path to spec area]
---

# BDD Skill

Single authority for Behavior-Driven Development spec authoring. Creates, updates, or deletes `.feature` files in the `spec/` pipeline following BDD best practices. This skill is invoked **before** implementation skills (`/fix`, `/refactor`, `/reel`) because behavior specs drive development.

---

## Determine Scope

**Check if scope was provided (accessible as `$ARGUMENTS`):**

**If scope is provided ($ARGUMENTS is not empty):**
- Use the provided description to focus spec work
- Examples: `spec/active/installer/`, `add login feature`, `remove deprecated API`

**If no scope provided ($ARGUMENTS is empty):**
- Ask user: "What behavior needs to be specified? (e.g., new feature, changed behavior, removed capability)"
- Wait for user response

---

## Phase 1: Assess Spec Impact

Determine what kind of spec change is needed:

### 1. Identify Affected Feature Files

Search `spec/active/` and `spec/todo/` for existing feature files related to the scope:

- Read relevant `.feature` files in the affected domain subdirectory
- Check if behavior is already specified (scenario exists)
- Check if existing scenarios need updating (behavior changed)
- Check if scenarios should be deleted (behavior removed)

### 2. Classify the Change

**New behavior** → Create new scenarios (or new feature file) in `spec/todo/`
**Changed behavior** → Update existing scenarios in `spec/active/`
**Removed behavior** → Delete scenarios from `spec/active/`
**Mixed** → Combination of the above

### 3. Present Assessment

Summarize what spec changes are needed. Present a picker:

Use AskUserQuestion with header "BDD scope", options:
1. "Proceed with spec changes" — Write the feature file changes as assessed
2. "Adjust scope" — Modify which specs to create/update/delete

---

## Phase 2: Personas (Database/State-Store Projects Only)

**This phase applies only when the project has a database or state storage backend.** Skip entirely for projects without persistent state. Personas define the actors and objects that appear in Given steps — they must be defined before writing feature files that reference them.

### Detect State Storage Presence

Check for indicators that the project uses a database or state store:

**Python projects:** Scan `pyproject.toml` or `requirements.txt` for ORM/driver dependencies (`sqlalchemy`, `django`, `peewee`, `tortoise-orm`, `mongoengine`, `psycopg2`, `pymysql`, `pymongo`, `redis`)

**General indicators:**
- Migration directories (`alembic/`, `migrations/`, `prisma/migrations/`)
- Config files (`alembic.ini`, `database.yml`, `ormconfig.json`, `knexfile.js`)
- Environment variables in `.env` or config: `DATABASE_URL`, `REDIS_URL`, `MONGO_URI`
- Docker services in `docker-compose.yml`: `postgres`, `mysql`, `redis`, `mongo`, `elasticsearch`

**If no indicators found:** Personas are narrative aids only — use them in the "As a [role]" Feature narrative and scenario names, but do not create persona files or seed data. Skip the rest of this phase.

### Persona Types

**Actor personas** — people who interact with the system:
- Users, customers, admins, operators, guests
- Define: name, credentials, role, permissions, profile attributes
- Map to the "As a [role]" narrative in Feature descriptions

**Object personas** — domain entities with specific states:
- Products, orders, subscriptions, contracts, configurations
- Define: name, key attributes, state, relationships
- Named archetypes that appear frequently across scenarios (e.g., "expired subscription", "high-value order")

### Persona File Location and Format

Persona files live at project root `personas/`, organized by type:

```
personas/
  actors/          — People who interact with the system
  objects/         — Domain entities with specific states
```

**Format-agnostic** — use whichever format matches the project's conventions:

**Gherkin (`.feature`)** — BDD-native approach. Personas as scenarios with Given steps. Step definitions handle database seeding. Best for teams already comfortable with Gherkin.

```gherkin
Feature: Customer personas
  Scenario: Alice the premium customer
    Given a user "Alice" with email "alice@example.com"
    And "Alice" has role "premium_customer"
    And "Alice" has subscription plan "annual"

  Scenario: Bob the free-tier user
    Given a user "Bob" with email "bob@example.com"
    And "Bob" has role "free_user"
```

**YAML (`.yml`)** — Data-oriented approach. A fixture loader reads persona definitions and seeds the database. Best for large persona sets or data-heavy projects.

```yaml
alice:
  type: user
  name: Alice
  email: alice@example.com
  role: premium_customer
  plan: annual

bob:
  type: user
  name: Bob
  email: bob@example.com
  role: free_user
```

**JSON (`.json`)** — Machine-friendly variant of YAML. Same structure, different syntax. Best when tooling expects JSON.

### Persona Authoring Conventions

**Keep persona definitions minimal:**
- Only specify attributes that are semantically meaningful for the persona's role
- Let factories or defaults fill in the rest — avoids brittleness when schema changes
- A "premium customer" persona defines role and plan, not every database column

**Use trait composition over persona explosion:**
- Define a base persona (e.g., "Alice") with core attributes
- Apply traits in step definitions for variations: `Given "Alice" with an expired payment method`
- Do NOT create separate personas for every slight variation (Alice-with-expired-card, Alice-with-two-addresses, etc.)

**Name personas descriptively:**
- Actor names should be vivid and memorable: "Alice", "Bob", not "User1", "User2"
- Object names should encode their key trait: "expired subscription", "high-value order"
- The name alone should tell the reader what makes this persona interesting

### Step Definition Patterns

Step definitions resolve persona names to seeded data. The implementation depends on the persona file format:

**For Gherkin personas:** Run the persona feature file as a setup step (or call shared Given steps directly). The step definitions create database records.

**For YAML/JSON personas:** A fixture or conftest function loads the persona file, iterates definitions, and seeds records via ORM or raw SQL. Example pattern for pytest-bdd:

```python
# conftest.py
@given(parsers.parse('"{persona_name}" is logged in'), target_fixture='current_user')
def givenPersonaLoggedIn(persona_name, db_session):
    persona = PERSONAS[persona_name]  # loaded from YAML
    user = UserFactory(**persona)
    db_session.add(user)
    db_session.flush()
    return user
```

### Test Isolation

- Seed reference data (roles, plans, config) at session scope
- Seed scenario-specific persona data at function scope with transaction rollback
- Never share mutable persona state between scenarios
- Each scenario gets fresh persona instances — never reuse database records across scenarios

### Anti-Patterns to Avoid

- **Over-specifying:** Defining every field when only 2-3 matter. Breaks when schema changes.
- **Shared mutable state:** Scenarios reading/writing the same persona record without isolation.
- **Persona explosion:** Dozens of personas for slight variations. Use trait composition instead.
- **Tight schema coupling:** Persona files mirroring column names. Use a factory indirection layer.
- **Hidden setup:** Burying critical preconditions in shared fixtures far from the scenario. Keep business-relevant setup visible.

---

## Phase 3: Write Feature Files

### Conventions

All feature files must follow these conventions:

**File organization:**
- One feature per file, organized by domain in subdirectories
- Filename: lowercase, hyphenated, `.feature` extension (e.g., `user-authentication.feature`)
- New features go in `spec/todo/<domain>/` (created during development)
- Active specs live in `spec/active/<domain>/`
- Domain subdirectories mirror the codebase's logical structure

**Feature structure:**
```gherkin
Feature: Short business-readable title
  As a [role]
  I want [capability]
  So that [benefit]

  Background:
    Given [shared preconditions — only if ALL scenarios share them]

  # Rule: Business rule grouping  (behave users: comment out Rule: lines — not supported)

    @id:abcd1234
    Scenario: Descriptive behavior outcome
      Given [context]
      When [action]
      Then [expected outcome]
```

**Tagging (lines preceding each Scenario):**
- `@id:<8-char-hex>` — Mandatory. Generate via `~/.claude/scripts/bdd.sh --generate-id spec/`
- `@depends-on:<id>` — Optional. One per line. Establishes task ordering.
- `@acceptance:<shell-command>` — Optional. Overrides BDD framework auto-detection for verification.

**Writing style — DECLARATIVE, not imperative:**
- Describe WHAT behavior is expected, not HOW to interact with the UI
- Use business language, not technical implementation details
- A product owner should be able to read and validate the scenario
- Use vivid persona names (e.g., "Alice") not abstract labels (e.g., "User A")

**Scenario guidelines:**
- Each scenario must be independent and self-contained
- Keep to 3-5 steps: one Given block, one When, one Then
- Scenario names describe the behavior and expected outcome
- No scenario should depend on another having run first
- Do not test implementation details (database tables, CSS selectors, API internals)

**When to use each construct:**
- `Background:` — Only Given steps shared by ALL scenarios in the feature. Keep short (1-4 lines).
- `Rule:` — Group scenarios illustrating a single business rule (Gherkin 6+, pytest-bdd compatible; **not supported by behave** — comment out `Rule:` lines if automating with behave)
- `Scenario Outline:` with `Examples:` — Data-driven scenarios with 3+ variations of the same behavior pattern
- Separate feature files — When a file exceeds ~10 scenarios, split by sub-domain

**Anti-patterns to avoid:**
- Imperative style (clicking buttons, filling fields) — use declarative behavior descriptions
- Conjunction steps ("When I login and navigate to settings") — split into separate steps
- Incidental details (specifying every field when only one matters)
- Too many steps (more than 5 indicates testing multiple behaviors)
- Testing implementation (referencing internal methods, database schema, etc.)

### ID Generation

For each new scenario, generate a unique ID:

1. Run `~/.claude/scripts/bdd.sh --generate-id spec/` to get a collision-free 8-char hex ID
2. Place the `@id:<hex>` tag on the line immediately before the `Scenario:` line
3. Never reuse or manually craft IDs — always generate them

### Creating New Feature Files

1. Determine the domain subdirectory (create if needed under `spec/todo/`)
2. Generate `@id:` tags for each scenario
3. Write the feature file following all conventions above
4. Add `@depends-on:` tags where scenarios have ordering requirements
5. Add `@acceptance:` tags only when the default BDD framework detection is insufficient

### Updating Existing Feature Files

1. Read the current feature file from `spec/active/`
2. Modify scenarios to reflect the changed behavior
3. Preserve existing `@id:` tags (IDs are stable across refactors)
4. Add new `@id:` tags only for new scenarios
5. Update scenario names and steps to match new behavior
6. Remove scenarios for deleted behavior

### Deleting Feature Files or Scenarios

1. Remove the scenario (or entire file) from `spec/active/`
2. Use `git rm` for tracked files
3. Verify no other scenarios have `@depends-on:` references to deleted IDs

---

## Phase 4: Verify and Summarize

After writing spec changes:

1. **Show summary** of what was created/updated/deleted
2. **List the feature files** and scenario counts affected
3. **Confirm the spec changes are ready** for the implementation skill to proceed
4. **Stage spec changes** — Run `git add` on any new or modified `.feature` files created/updated in this session. This ensures spec files are tracked even in new projects where `spec/` didn't previously exist.

If this skill was invoked as a prerequisite to another skill (`/fix`, `/refactor`, `/reel`), indicate that spec authoring is complete and the calling workflow should continue.

---

## Integration with Other Skills

This skill is the **mandatory first step** in behavior-driven workflows:

- `/design` Phase 4 → invokes `/bdd` to write specs → then invokes `/fix`, `/refactor`, or `/reel`
- `/fix` → invokes `/bdd` first (specify expected behavior) → then implements the fix
- `/refactor` → invokes `/bdd` first (verify/update specs if behavior surface changes) → then refactors

Invocation is **mandatory by default**. Callers must always invoke `/bdd` rather than pre-deciding to skip. If no spec changes are needed, `/bdd` will assess that and proceed without modifications.

**Opt-out:** To disable mandatory BDD checks, add `skip-bdd-checks: true` to the project's `CLAUDE.md` or the developer's `CLAUDE.local.md`. When present, `/fix`, `/refactor`, and `/design` will skip the `/bdd` invocation.

The `/bdd` skill can also be invoked standalone to audit or update specs independently.

---

## Example Usage

```
/bdd                                    # Prompts for scope
/bdd add user login feature             # Create new feature spec
/bdd spec/active/installer/             # Audit/update installer specs
/bdd remove deprecated v1 API           # Delete specs for removed behavior
```
