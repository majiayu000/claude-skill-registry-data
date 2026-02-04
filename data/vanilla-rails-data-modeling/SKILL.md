---
name: vanilla-rails-data-modeling
description: Use when designing database schema, writing migrations, or making data storage decisions - enforces UUIDs, account_id multi-tenancy, state-as-records, no foreign keys, and proper index patterns
---

# Vanilla Rails Data Modeling

Database schema conventions following production 37signals patterns. Design for multi-tenancy, auditability, and operational flexibility.

## UUID Primary Keys

**All tables use UUIDs** - no auto-incrementing integers.

```ruby
# ❌ BAD - default integer
create_table :cards do |t|
  t.string :title
end

# ✅ GOOD - explicit UUID
create_table :cards, id: :uuid do |t|
  t.string :title
end
```

**UUID format:** UUIDv7 (timestamp-ordered), base36 encoded as 25-character strings.

**Why UUIDs:**
- No ID enumeration attacks
- Merge-safe across environments
- Timestamp ordering preserved (UUIDv7)
- No sequence contention under load

**Fixture considerations:** Fixtures need deterministic UUIDs that sort "older" than runtime records. Use a custom generator based on fixture name hash.

## Multi-Tenancy via account_id

**Every tenant-scoped table has `account_id`** - no exceptions for tables containing user data.

```ruby
create_table :cards, id: :uuid do |t|
  t.uuid :account_id, null: false  # Always present
  t.uuid :board_id, null: false
  t.string :title
  t.timestamps
end
```

**Tables WITHOUT account_id** (global/cross-tenant):
- `identities` - email addresses span accounts
- `sessions` - tied to identity, not account
- `magic_links` - authentication, not tenant data

**Automatic scoping:** Use `Current.account` and ApplicationRecord to scope queries:

```ruby
class ApplicationRecord < ActiveRecord::Base
  def self.default_scope
    if Current.account
      where(account_id: Current.account.id)
    else
      all
    end
  end
end
```

**Common mistake:** Forgetting account_id on join tables:

```ruby
# ❌ BAD - missing account_id
create_table :taggings, id: :uuid do |t|
  t.uuid :card_id, null: false
  t.uuid :tag_id, null: false
end

# ✅ GOOD - includes account_id
create_table :taggings, id: :uuid do |t|
  t.uuid :account_id, null: false
  t.uuid :card_id, null: false
  t.uuid :tag_id, null: false
end
```

## State as Records (NOT Booleans)

**Critical:** Don't use boolean columns for state. Create state records that capture who/when.

```ruby
# ❌ BAD
add_column :cards, :closed, :boolean, default: false

# ✅ GOOD
create_table :closures, id: :uuid do |t|
  t.uuid :account_id, null: false
  t.uuid :card_id, null: false
  t.uuid :user_id        # who closed it
  t.timestamps           # when closed
end
add_index :closures, :card_id, unique: true
```

**State table examples from production:**

| Table | State | Unique Constraint |
|-------|-------|-------------------|
| `closures` | card is closed | `card_id` (one per card) |
| `card_goldnesses` | card is highlighted | `card_id` |
| `card_not_nows` | card is postponed | `card_id` |
| `pins` | user pinned card | `[card_id, user_id]` (per user) |
| `card_activity_spikes` | card has recent activity | `card_id` |
| `board_publications` | board is public | `board_id` |

**Pattern:** Unique constraint determines has_one vs has_many:
- `unique: card_id` → `has_one :closure`
- `unique: [card_id, user_id]` → `has_many :pins` (one per user)

## Index Strategy

**Lead with account_id** in composite indexes for tenant-scoped queries:

```ruby
# ❌ BAD - account_id not leading
add_index :cards, [:status, :account_id]

# ✅ GOOD - account_id leads
add_index :cards, [:account_id, :status]
add_index :cards, [:account_id, :last_active_at, :status]
```

**Polymorphic indexes** - always `[type, id]`:

```ruby
add_index :events, [:eventable_type, :eventable_id]
add_index :mentions, [:source_type, :source_id]
add_index :storage_entries, [:recordable_type, :recordable_id]
```

**Unique constraints** - prevent duplicates at database level:

```ruby
# Binary state (one per item)
add_index :closures, :card_id, unique: true

# Per-user state
add_index :pins, [:card_id, :user_id], unique: true

# Tenant-scoped uniqueness
add_index :cards, [:account_id, :number], unique: true
add_index :tags, [:account_id, :title], unique: true
```

**Compound query patterns:**

```ruby
# Timeline queries
add_index :events, [:board_id, :action, :created_at]

# Notification queries
add_index :notifications, [:user_id, :read_at, :created_at],
  order: { read_at: :desc, created_at: :desc }
```

## No Foreign Key Constraints

**Explicitly avoid foreign key constraints** - use application-level integrity.

```ruby
# ❌ BAD - foreign key constraint
t.references :card, foreign_key: true

# ✅ GOOD - no constraint
t.uuid :card_id, null: false
add_index :table, :card_id
```

**Why no foreign keys:**
- Prevents deadlocks during bulk operations
- Allows flexible deletion order
- Simplifies data migrations
- Production 37signals pattern

**Maintain integrity via:**
- `dependent: :destroy` in associations
- Application validations
- Nullify or cascade in application code

## Join Table Patterns

**Two patterns based on whether join needs its own identity:**

### Pattern 1: Pure HABTM (no ID, no account_id)

Use for simple many-to-many without metadata:

```ruby
# For filters (saved search criteria)
create_table :boards_filters, id: false do |t|
  t.uuid :board_id, null: false
  t.uuid :filter_id, null: false
end
add_index :boards_filters, :board_id
add_index :boards_filters, :filter_id
```

**Naming:** `plural_plural` alphabetically (`assignees_filters`, `boards_filters`)

### Pattern 2: has_many :through (with ID and account_id)

Use when join records need:
- Their own timestamps
- Additional metadata
- Tenant scoping
- Event tracking

```ruby
create_table :taggings, id: :uuid do |t|
  t.uuid :account_id, null: false
  t.uuid :card_id, null: false
  t.uuid :tag_id, null: false
  t.timestamps
end
add_index :taggings, [:card_id, :tag_id], unique: true
```

**Naming:** Singular noun (`taggings`, `assignments`, `accesses`)

**Decision guide:**

| Need | Pattern |
|------|---------|
| Just link two things | `id: false` HABTM |
| Track when linked | `id: :uuid` with timestamps |
| Track who linked | Add `user_id` column |
| Account scoping | Add `account_id` column |

## Polymorphic Associations

**Use meaningful names** that describe the relationship:

| Name | Meaning | Example |
|------|---------|---------|
| `eventable` | thing the event is about | Event tracks Card change |
| `source` | where it came from | Notification from Event |
| `container` | what holds it | Entropy config for Board |
| `searchable` | what is searchable | SearchRecord for Card |
| `recordable` | what it's attached to | StorageEntry for Comment |
| `owner` | who owns it | StorageTotal for Account |

**Schema pattern:**

```ruby
create_table :events, id: :uuid do |t|
  t.uuid :account_id, null: false
  t.string :eventable_type, null: false
  t.uuid :eventable_id, null: false
  # ...
end
add_index :events, [:eventable_type, :eventable_id]
```

**Model pattern:**

```ruby
class Event < ApplicationRecord
  belongs_to :eventable, polymorphic: true
end

class Card < ApplicationRecord
  has_many :events, as: :eventable
end
```

## Counter Caches and Denormalization

**Use manual increment/decrement** - not Rails' `counter_cache:` option:

```ruby
# In model callback or explicit method
class Card < ApplicationRecord
  after_create :increment_account_counter

  private
    def increment_account_counter
      account.increment!(:cards_count)
    end
end
```

**Why manual counters:**
- More control over when counts update
- Can batch updates
- Explicit about side effects

**Denormalized fields examples:**
- `accounts.cards_count` - avoid COUNT(*) queries
- `account_join_codes.usage_count` - track usage
- `search_records.content` - denormalized for fulltext

## Settings and Config Tables

**Polymorphic config with inheritance:**

```ruby
# entropies table - config for Account OR Board
create_table :entropies, id: :uuid do |t|
  t.uuid :account_id, null: false
  t.string :container_type, null: false  # "Account" or "Board"
  t.uuid :container_id, null: false
  t.bigint :auto_postpone_period, default: 2592000  # 30 days
  t.timestamps
end
add_index :entropies, [:container_type, :container_id], unique: true
```

**Fallback pattern:**

```ruby
class Board < ApplicationRecord
  def auto_postpone_period
    entropy&.auto_postpone_period || account.auto_postpone_period
  end
end
```

**Per-user settings table:**

```ruby
create_table :user_settings, id: :uuid do |t|
  t.uuid :account_id, null: false
  t.uuid :user_id, null: false
  t.integer :bundle_email_frequency, default: 0
  t.string :timezone_name
  t.timestamps
end
```

## Migration Conventions

**Prefer `change` method** - Rails handles reversibility:

```ruby
# ✅ GOOD - reversible
def change
  add_column :cards, :due_on, :date
  add_index :cards, [:account_id, :due_on]
end
```

**Use `up/down` only when needed:**

```ruby
# When change isn't reversible
def up
  remove_column :cards, :legacy_field
end

def down
  add_column :cards, :legacy_field, :string
end
```

**Always specify UUID type for references:**

```ruby
# ❌ BAD - assumes integer
t.references :card

# ✅ GOOD - explicit UUID
t.uuid :card_id, null: false
add_index :table, :card_id
```

**Index separately when table is large:**

```ruby
# For new tables - inline is fine
create_table :small_table, id: :uuid do |t|
  t.uuid :card_id, null: false, index: true
end

# For existing large tables - separate migration
add_index :large_table, :new_column, algorithm: :concurrently
```

## Quick Reference

| Decision | Pattern |
|----------|---------|
| Primary key | `id: :uuid` always |
| Tenant column | `account_id` on all tenant tables |
| State tracking | Separate table, not boolean |
| Binary state | `unique: true` on parent_id |
| Per-user state | `unique: [parent_id, user_id]` |
| Foreign keys | None - app-level integrity |
| Simple join | `id: false`, no account_id |
| Rich join | `id: :uuid`, with account_id |
| Polymorphic index | `[type, id]` compound |
| Query index | Lead with `account_id` |
| Counter cache | Manual `increment!` |
| Config inheritance | Polymorphic container with fallback |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Integer primary keys | Use `id: :uuid` |
| Boolean for state | Create state record table |
| Missing account_id | Add to all tenant tables |
| Foreign key constraints | Remove - use app-level |
| Index without account_id lead | Reorder with account_id first |
| Rails counter_cache | Use manual increment! |
| HABTM for tracked joins | Use has_many :through with ID |
| Generic polymorphic name | Use semantic name (eventable, source) |

## Sharding Pattern (Advanced)

For large tables, shard by account:

```ruby
# 16 identical tables
(0..15).each do |shard|
  create_table "search_records_#{shard}", id: :uuid do |t|
    t.uuid :account_id, null: false
    t.text :content
    # ...
  end
  add_index "search_records_#{shard}", [:account_key, :content, :title],
    type: :fulltext
end
```

**Shard routing via CRC32:**

```ruby
def shard_for(account_id)
  Zlib.crc32(account_id.to_s) % 16
end
```

**Use case:** Fulltext search without Elasticsearch - MySQL native fulltext across 16 shards.
