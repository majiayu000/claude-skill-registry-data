---
name: shaping
description: Use after brainstorming to apply vanilla-rails patterns to a feature, producing structured handoff for implementation planning. Invoke with /shape.
---

# /shape

**Position in workflow:**
1. `superpowers:brainstorming` → explores what, clarifies requirements
2. **`/shape` (this)** → applies patterns, defines right things to do
3. `superpowers:writing-plans` → detailed implementation steps

**When invoked, execute this workflow. Do not skip phases.**

---

## Phase 1: Confirm Scope

If brainstorming already happened, summarize:
- Problem being solved
- What's in/out of scope
- Who can use this

If not, ask these questions before proceeding.

---

## Phase 2: Discover Applicable Skills

Check each vanilla-rails skill. For each, state whether it applies:

**Always apply:**
- **work-breakdown** - How to split into PRs
- **testing** - Test patterns
- **style** - Code style conventions
- **naming** - Naming conventions

**Apply if relevant:**
- **data-modeling** - Adding tables, migrations, schema decisions?
- **delegated-types** - 5+ content types comingling in feeds/timelines?
- **models** - Adding model behavior, state tracking, concerns?
- **controllers** - Adding endpoints, state changes, resources?
- **views** - ERB templates, partials, Turbo Streams?
- **jobs** - Background processing needed?
- **hotwire** - Dynamic UI updates?
- **writing-affordances** - 3+ related methods or prefix clusters?

**Say:** "These skills apply: [list]. Loading each to apply patterns."

---

## Phase 3: Apply Patterns

For each applicable skill, invoke it and document the decision:

```
**data-modeling:** UUID primary key, account_id, state-as-records
**models:** State as records → `has_one :pin`, not `pinned: boolean`
**models:** Concern as adjective → `Card::Pinnable`
**controllers:** Resource extraction → `resource :pinning`
**naming:** Resource noun → `Pin` (create = pin, destroy = unpin)
```

Ask the user to confirm or adjust decisions.

---

## Phase 4: Break Down Work

Using work-breakdown patterns, propose PRs:

```
PR 1: "Add pinning to cards" (migration + model + concern + tests) - 4 files
PR 2: "Add UI for pinning cards" (controller + views + tests) - 4 files
PR 3: "Sort pinned cards first" (scope + view + tests) - 3 files
```

**Check:** Does any PR title have "and"? Split it.

---

## Phase 5: Output Shaping Document

Write to `docs/shaping/YYYY-MM-DD-feature-name.md`:

```markdown
# [Feature] Shaping

## Scope
- Problem: [what problem this solves]
- In scope: [list]
- Out of scope: [list]
- Users: [who can use this]

## Pattern Decisions
[from Phase 3 - which skills applied and how]

## PRs
[from Phase 4 - ordered list of PRs with file counts]

## Open Questions
[any unresolved items]
```

---

## Phase 6: Handoff to Planning

Ask: "Ready to create implementation plan?"

If yes, invoke `superpowers:writing-plans` with the shaping document as context.

The writing-plans skill will create detailed, step-by-step implementation tasks for each PR.

---

## Skill Reference

| Skill | When to Apply |
|-------|---------------|
| data-modeling | New tables, migrations, schema |
| delegated-types | 5+ types in unified timeline/feed |
| models | State tracking, concerns, associations |
| controllers | Endpoints, resources, state changes |
| views | ERB templates, partials, collection rendering |
| jobs | Background processing |
| hotwire | Dynamic UI, Turbo frames/streams |
| writing-affordances | 3+ related methods, prefix clusters |
| work-breakdown | Always (PR structure) |
| testing | Always |
| style | Always |
| naming | Always (new code) |

---

**Remember:** This is a command. Execute each phase in order. Do not skip to code.
