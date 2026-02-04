---
name: vanilla-rails-models
description: Use when writing Rails models - enforces state-as-records not booleans, concerns as adjectives namespaced under model, invocation ordering, and private indentation
---

# Vanilla Rails Models

Rich domain models with concerns, following production Basecamp/37signals patterns. Decompose with concerns, not services.

## State as Separate Records (NOT Booleans)

**Critical pattern:** Don't use boolean columns for state. Create state records that capture who/when.

```ruby
# ❌ BAD - boolean column
class AddStarredToCards < ActiveRecord::Migration[7.0]
  def change
    add_column :cards, :starred, :boolean, default: false
    add_column :cards, :starred_at, :datetime
  end
end

class Card < ApplicationRecord
  def star
    update(starred: true, starred_at: Time.current)
  end
end

# ✅ GOOD - state record
class CreateStars < ActiveRecord::Migration[7.0]
  def change
    create_table :stars, id: :uuid do |t|
      t.references :card, null: false, foreign_key: true, type: :uuid
      t.references :user, null: false, foreign_key: true, type: :uuid
      t.timestamps
    end
  end
end

class Star < ApplicationRecord
  belongs_to :card
  belongs_to :user
end

class Card < ApplicationRecord
  has_one :star, dependent: :destroy

  def star(user: Current.user)
    create_star!(user: user) unless starred?
  end

  def starred?
    star.present?
  end
end
```

**Why state records:**
- Captures who (user) and when (created_at) automatically
- Can add metadata later without altering main table
- Explicit presence/absence vs true/false ambiguity
- Database enforces referential integrity

**Use has_one for binary state, has_many for multi-user:**

```ruby
# Binary state (one per item) - use has_one
has_one :closure    # card is either closed or not
has_one :triage     # card is either triaged or not

# Multi-user actions - use has_many
has_many :pins      # multiple users can pin
has_many :watches   # multiple users can watch
has_many :assignments
```

**Common rationalizations to reject:**

| Excuse | Reality |
|--------|---------|
| "Boolean is simpler" | State records capture metadata you'll need later |
| "Just a flag" | Today's flag is tomorrow's "who changed this and when?" |
| "YAGNI" | Capturing who/when is always valuable for state changes |
| "Extra table is overkill" | This is the 37signals pattern. Follow it. |

## Concerns as Adjectives, Namespaced Under Model

**Extract capabilities to concerns** - even for single use. Concerns are for decomposition, not just reuse.

**Name as adjectives** (capabilities), namespace under the model:

```ruby
# ❌ BAD - wrong names
module Starring          # verb, not adjective
module Stars             # noun, not adjective
module Starrable         # not namespaced under model
module Starred           # past participle, describes state not capability

# ✅ GOOD - adjective, namespaced
module Card::Starrable   # adjective, shows Card owns this capability
module Card::Closeable   # can be closed
module Card::Assignable  # can be assigned
module Card::Pinnable    # can be pinned
```

**File location:** `app/models/card/starrable.rb` (NOT `app/models/concerns/starrable.rb`)

**Full example with private methods:**

```ruby
# app/models/card/closeable.rb
module Card::Closeable
  extend ActiveSupport::Concern

  included do
    has_one :closure, dependent: :destroy

    scope :closed, -> { joins(:closure) }
    scope :open, -> { where.missing(:closure) }
  end

  def close(user: Current.user)
    unless closed?
      transaction do
        create_closure!(user: user)
        track_event :closed, creator: user
      end
    end
  end

  def reopen(user: Current.user)
    if closed?
      transaction do
        closure&.destroy
        track_event :reopened, creator: user
      end
    end
  end

  def closed?
    closure.present?
  end

  def closed_by
    closure&.user
  end

  private
    def track_event(action, creator:)
      # private helper methods go in concern, indented
    end
end

# app/models/card.rb
class Card < ApplicationRecord
  include Card::Closeable
  # ... rest of model
end
```

**Multi-user state example:**

```ruby
# app/models/card/pinnable.rb
module Card::Pinnable
  extend ActiveSupport::Concern

  included do
    has_many :pins, dependent: :destroy
  end

  def pinned_by?(user)
    pins.exists?(user: user)
  end

  def pin_by(user)
    pins.find_or_create_by!(user: user)
  end

  def unpin_by(user)
    pins.find_by(user: user)&.destroy
  end
end
```

**When to extract:**
- Feature adds 3+ methods to model
- Clear capability/adjective name exists
- Even if only one model uses it (decomposition, not reuse)
- Model exceeds ~100 lines

**Common mistakes:**

```ruby
# ❌ BAD - verb names
Card::Closing, Card::Assigning

# ✅ GOOD - adjective names
Card::Closeable, Card::Assignable

# ❌ BAD - past participle (describes state)
Card::Assigned, Card::Closed

# ✅ GOOD - adjective (describes capability)
Card::Assignable, Card::Closeable

# ❌ BAD - not namespaced
Starrable, Closeable

# ✅ GOOD - namespaced under model
Card::Starrable, Card::Closeable
```

## Method Ordering by Invocation

Order methods vertically by invocation: callers before callees.

```ruby
class Card < ApplicationRecord
  def close(user: Current.user)
    transaction do
      create_closure!(user: user)
      notify_watchers  # called here
    end
  end

  private
    def notify_watchers  # defined after caller
      watchers.each { |w| notify_user(w) }
    end

    def notify_user(user)  # defined after its caller
      # ...
    end
end
```

**Benefit:** Read top-to-bottom following execution flow.

## Private Method Indentation

Indent private methods under the `private` keyword (no newline after `private`):

```ruby
class Card < ApplicationRecord
  def public_method
    # ...
  end

  private
    def private_method_one
      # indented
    end

    def private_method_two
      # indented
    end
end
```

**In concerns:** Same pattern - private methods indented under `private`

```ruby
module Card::Closeable
  def close
    create_closure!
    notify_team
  end

  private
    def notify_team
      # indented under private
    end
end
```

**Exception:** Module with only private methods - mark `private` at top, add newline, don't indent:

```ruby
module Card::Internal
  private

  def helper_method
    # not indented
  end
end
```

## Class Method Ordering

1. Class methods first
2. Public instance methods (with `initialize` at top if present)
3. Private instance methods

```ruby
class Card < ApplicationRecord
  def self.pending
    where(closure: nil)
  end

  def initialize(attrs = {})
    super
  end

  def close
    # ...
  end

  private
    def notify_watchers
      # ...
    end
end
```

## Quick Reference

| Pattern | Bad | Good |
|---------|-----|------|
| State | `starred: boolean` | `has_one :star` |
| Multi-user | `starred_by_user_ids: []` | `has_many :stars` |
| Concern name | `Starring`, `Stars`, `Starred` | `Starrable` |
| Concern namespace | `module Starrable` | `module Card::Starrable` |
| Concern location | `concerns/starrable.rb` | `card/starrable.rb` |
| Method order | Random | Invocation order |
| Private indent | No indent | Indented under `private` |
| Extraction | "Only if reused" | "3+ methods or >100 lines" |

## Real-World Examples from Production

**Binary state (has_one):**
- Card::Closeable → has_one :closure
- Card::Triageable → has_one :triage
- Card::Golden → has_one :goldness

**Multi-user state (has_many):**
- Card::Pinnable → has_many :pins
- Card::Watchable → has_many :watches
- Card::Assignable → has_many :assignments

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Boolean is simpler than a whole table" | State records capture who/when you'll need later |
| "Concerns are for shared code" | Concerns decompose models, not just for reuse |
| "Global namespace is fine" | Namespacing shows ownership and scales better |
| "Just following Rails guides" | 37signals patterns intentionally differ from Rails defaults |
| "Extraction is premature" | 3+ methods = extract. Decomposition aids understanding |
| "has_many defeats the pattern" | State record pattern works for both has_one and has_many |
| "Adjective doesn't sound right" | Find the right adjective. Not negotiable. |
| "Too much indirection" | This is the 37signals pattern. It's explicit state modeling. Follow it. |
