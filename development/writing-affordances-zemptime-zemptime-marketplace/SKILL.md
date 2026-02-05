---
name: writing-affordances
description: Use when refactoring fat Rails models with repetitive prefixes like entropy_*, notification_*, or multi-association coordination. Extracts PORO wrappers that group operations around nouns/concepts.
---

# Writing Affordances

Extract PORO wrappers that group 3+ operations around a noun/concept, keeping parent model focused.

**Announce:** "I'm using the writing-affordances skill to evaluate this for affordance extraction."

## Detection Triggers

- 3+ methods share prefix: `entropy_calculate`, `entropy_remind`, `entropy_cleanup`
- Methods coordinate 2+ associations (`assignments` + `watches` + `events`)
- Fat model with mixed conceptual domains
- Related methods but connection non-obvious

**Don't use for:** Single trait (use concern) | Single association (use extension) | 1-2 methods (use plain method)

## Decision Heuristics

Ask yourself:

1. **"Can I pass this around?"** - Would `notify(description)` be clearer than `notify(event)`?
2. **"Do I call it or does Rails?"** - Explicit calls = Affordance | Callbacks/validations = Concern
3. **"Prefix cluster?"** - `entropy_*` methods = Extract `entropy` affordance (prefix = noun)
4. **"Call site clarity?"** - `card.entropy.auto_clean_at` vs `card.entropy_auto_clean_at`
5. **"Need infrastructure + operations?"** - Concern provides associations/callbacks, affordance provides API

See @detecting.md for complete decision framework.

## Pattern Comparison

| Pattern | Use When | Example | Key Question |
|---------|----------|---------|--------------|
| **Affordance** | Group operations around noun | `card.entropy.auto_clean_at` | "Can I pass this around?" |
| **Concern** | Infrastructure or implicit behavior | `Searchable` (callbacks only) | "Does Rails call it implicitly?" |
| **Concern + Affordance** | Both infrastructure AND operations | Concern sets up associations, affordance provides API | "Need both?" |
| **Association Ext** | Single association operations | `card.comments.recent` | "Only touching one has_many?" |

## Critical Constraints

**Violating these = wrong pattern:**

- **3+ methods minimum** - Don't create single-method affordances
- **PORO only** - No ActiveRecord inheritance
- **Parent is ONLY dependency** - `Card::Entropy.new(card)`, not `new(card, user)`
- **Don't memoize parameterized** - `entropy(as_of: date)` should NOT use `||=`

## Quick Pattern

```ruby
# Before: Methods scattered in model or prefix smell
card.entropy_auto_clean_at
card.entropy_days_before_reminder
card.entropy_reminder_sent?

# After: Affordance
card.entropy.auto_clean_at
card.entropy.days_before_reminder
card.entropy.reminder_sent?

# Entry point in concern
module Card::Entropic
  def entropy
    Card::Entropy.for(self)  # Factory pattern
  end

  def entropic?
    entropy.present?
  end
end

# PORO affordance class
class Card::Entropy
  attr_reader :card, :auto_clean_period

  class << self
    def for(card)
      return unless card.last_active_at
      new(card, card.auto_postpone_period)
    end
  end

  def initialize(card, auto_clean_period)
    @card = card
    @auto_clean_period = auto_clean_period
  end

  def auto_clean_at
    card.last_active_at + auto_clean_period
  end

  def days_before_reminder
    (auto_clean_period * 0.25).seconds.in_days.round
  end
end
```

## Verification

Non-obvious checks before completion:

- [ ] 3+ related methods (not single-method wrapper)
- [ ] Parameterized affordances NOT memoized
- [ ] Class documentation with usage examples
- [ ] Tests: both isolated and integration

## Sub-documents

- @detecting.md - Full decision framework with clarifying questions
- @implementing.md - File organization, naming, concerns + affordances patterns
