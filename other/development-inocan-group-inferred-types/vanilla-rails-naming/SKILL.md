---
name: vanilla-rails-naming
description: Use when naming classes, methods, routes in vanilla Rails codebases - fixes concern verb/noun confusion, bang method misuse, custom action anti-patterns
---

# Vanilla Rails Naming

37signals naming patterns from production Basecamp codebases (Fizzy, HEY, Basecamp).

**Scope:** These are 37signals-specific conventions. They differ from generic Rails guides and may contradict advice from other sources. When in doubt, follow these patterns for vanilla Rails codebases.

## Core Pattern: State as Resource

State changes (pin, close, assign) become **resources**, not actions:

```ruby
# ❌ WRONG - Custom actions
resources :cards do
  member do
    post :pin
    post :close
  end
end

# ✓ RIGHT - Singular resources
resources :cards do
  resource :pin      # POST=create, DELETE=destroy
  resource :closure  # POST=close, DELETE=reopen
end
```

This creates the naming cascade:
- Concern: `Closeable` (adjective)
- Model: `Closure` (noun)
- Controller: `ClosuresController` (plural of noun)
- Routes: `resource :closure` (singular)

## Quick Reference

| Type | Pattern | Example | ❌ Wrong |
|------|---------|---------|----------|
| **Concern** | Adjective (-able/-ible ONLY) | `Pinnable`, `Closeable`, `Assignable` | `Pinning`, `Pinnish`, `Pinlike`, `PinManager` |
| **State Model** | Noun | `Pin`, `Closure`, `Assignment` | `CardPin`, `CloseRecord` |
| **State Method** | Plain verb (no !) | `card.close`, `card.pin` | `card.close!`, `card.pin!` |
| **Async Enqueue** | `*_later` | `notify_watchers_later` | `notify_watchers_async` |
| **Sync Execute** | Plain or `*_now` | `notify_watchers` or `notify_watchers_now` | - |
| **Controller** | Plural noun | `PinsController`, `ClosuresController` | `PinController` (singular) |
| **Routes** | `resource` (singular) | `resource :closure` | `post :close` |

## Common Violations

### ❌ Violation 1: Verb/Noun Concerns
**Rationalization:** "It describes the behavior being added"

```ruby
# ❌ WRONG - Verb/noun/other adjective forms
module Card::Pinning      # verb -ing
module Card::PinManager   # Manager/Handler/Logic
module Card::Pinnish      # wrong adjective form

# ✓ RIGHT - Adjective with -able/-ible ONLY
module Card::Pinnable
  def pin_by(user); end
end
```

**If concern name doesn't end in -able/-ible, STOP and rename immediately.**

### ❌ Violation 2: Bang Methods for State
**Rationalization:** "Rails uses bangs for state changes (save!)"

```ruby
# ❌ WRONG - Contradicts 37signals style
def pin!
  pins.create!(user: Current.user)
end

# ✓ RIGHT - Plain method
def pin_by(user)
  pins.find_or_create_by!(user: user)
end
```

**Why no bangs:** `save!` is about error handling (raise vs return false). State methods like `close` don't need this distinction.

**Counter-argument:** "But my tech lead says Rails conventions use bangs!" - 37signals patterns differ from generic Rails guides. In production Basecamp code, state methods use plain verbs. Follow the codebase style.

### ❌ Violation 3: Custom Route Actions
**Rationalization:** "Member routes for individual card actions"

```ruby
# ❌ WRONG - Custom actions break REST
resources :cards do
  member do
    post :pin
    delete :unpin
  end
end

# ✓ RIGHT - Singular resource
resources :cards do
  resource :pin, only: [:create, :destroy]
end
```

### ❌ Violation 4: Missing _later Pattern
**Problem:** Not recognizing async enqueue pattern

```ruby
# ❌ WRONG - Unclear if async
def notify_watchers
  NotifyWatchersJob.perform_later(self)
end

# ✓ RIGHT - _later suffix on enqueue method
def notify_watchers_later
  NotifyWatchersJob.perform_later(self)
end

def notify_watchers  # Called by job, does actual work
  # actual notification logic
end
```

**Compound verbs:** `_later` always goes at the end:
```ruby
def pin_and_notify_later    # ✓ RIGHT
def notify_after_pin_later  # ✓ RIGHT
def later_notify_pin        # ❌ WRONG
```

## Complete Example

For "pinning cards":

```ruby
# app/models/card/pinnable.rb
module Card::Pinnable
  extend ActiveSupport::Concern

  included do
    has_many :pins, dependent: :destroy
  end

  def pin_by(user)
    pins.find_or_create_by!(user: user)
  end

  def unpin_by(user)
    pins.find_by(user: user)&.destroy
  end
end

# app/models/pin.rb
class Pin < ApplicationRecord
  belongs_to :card
  belongs_to :user
end

# app/controllers/cards/pins_controller.rb
class Cards::PinsController < ApplicationController
  def create
    @pin = @card.pin_by(Current.user)
  end

  def destroy
    @card.unpin_by(Current.user)
  end
end

# config/routes.rb
resources :cards do
  resource :pin, only: [:create, :destroy], module: :cards
end
```

## File Locations

```
app/models/card/closeable.rb           # Card-specific concern
app/models/concerns/eventable.rb       # Shared concern
app/models/closure.rb                  # State record
app/controllers/cards/closures_controller.rb
```

## Red Flags - STOP and Rename

**If you see ANY of these, STOP immediately and rename before proceeding:**

- Concern NOT ending in `-able` or `-ible`
  - Including: `-ing`, `-er`, `-ish`, `-like`, `Logic`, `Management`, `Handler`, `Service`
- State method with bang suffix (e.g., pin!, close!, assign!)
- Routes using member/collection blocks for state changes
- Async method without `_later` suffix
- Controller mismatch: plural name with singular resource (`ClosureController` instead of `ClosuresController`)

**Sunk cost fallacy:** "I already implemented it wrong" - Rename now. Cost of renaming < cost of confusion later.

**Pattern check:** Does the naming cascade flow correctly?
- Concern (adjective -able/-ible) → Model (noun) → Controller (plural noun) → Route (singular resource)

## Commit Messages

Present tense, lowercase, no type prefixes:

```
✓ add pin feature to cards
✓ extract closeable concern
✓ fix closure validation
✓ update card pinning logic
✓ remove unused pin methods
✓ rename pinning concern to pinnable

❌ feat: Add pin feature        # no conventional commit prefixes
❌ Added pin feature            # no past tense
❌ [FEATURE] Pin cards          # no brackets/tags
❌ Add Pin Feature              # no title case
❌ adding pin feature           # no -ing form
```

**Time pressure:** "Need to commit fast" - Still follow the format. Takes 2 seconds to fix.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Rails conventions say to use bangs" | 37signals style differs. Follow the codebase patterns. |
| "Pinnable sounds weird, I'll use Pinnish" | Only -able/-ible adjectives. Rename immediately. |
| "Already implemented as Pinning" | Rename now. Sunk cost < confusion cost. |
| "Team will understand PinManagement" | No. Use Pinnable. Pattern must be consistent. |
| "This is complex, needs a service" | Concerns handle complexity fine. See actual Fizzy code. |
| "Member routes are clearer" | Singular resources are the pattern. Follow it. |
| "Commit message format doesn't matter" | It does. Present tense, lowercase, no prefixes. |
| "Close enough, ship it" | Wrong names compound. Fix now. |
