---
name: vanilla-rails-jobs
description: Use when writing background jobs or async operations - enforces thin job wrappers (3-5 lines) that delegate to models using _later/_now naming pattern
---

# Vanilla Rails Jobs

**Jobs are thin wrappers (3-5 lines). ALL business logic lives in models.**

## The Pattern

```ruby
# Model concern - WHERE THE LOGIC LIVES
module Card::ClosureNotifications
  extend ActiveSupport::Concern

  included do
    after_update :notify_watchers_later, if: :just_closed?
  end

  # _later: Enqueues the job
  def notify_watchers_later
    Card::ClosureNotificationJob.perform_later(self)
  end

  # _now: Contains ALL business logic
  def notify_watchers_now
    watchers.each do |watcher|
      CardMailer.closure_notification(watcher, self).deliver_now
      Notification.create!(user: watcher, card: self, action: 'closed')
    end
  end

  private
    def just_closed?
      saved_change_to_status? && closed?
    end
end

# Job - ONLY delegates (3 lines)
class Card::ClosureNotificationJob < ApplicationJob
  def perform(card)
    card.notify_watchers_now
  end
end
```

## Why Jobs Stay Thin

**Testability:** Test `_now` synchronously (no job infrastructure needed)
**Reusability:** Call `_now` in console, tests, anywhere
**Debuggability:** Stack traces point to model, not job framework

## Naming Convention

| Method | Purpose |
|--------|---------|
| `action_later` | Enqueues job |
| `action_now` | Actual logic (called by job, ALWAYS create for testing) |
| `action` | No async version |

**Flow:** Callback → `_later` → enqueue job → job calls `_now` → logic executes

## Red Flags - STOP and Fix

If you see ANY of these, you're doing it wrong:

- [ ] Job longer than 5 lines (except ActiveJob config like `retry_on`)
- [ ] Business logic in job (queries, conditionals, loops)
- [ ] Job creates/updates records
- [ ] Job sends emails directly
- [ ] Job calls multiple models directly
- [ ] No `_later`/`_now` naming
- [ ] Passing IDs to job instead of objects
- [ ] Logic split between job and model
- [ ] Job has error handling beyond `retry_on`/`discard_on`
- [ ] Model missing `_now` method ("I don't need it")

**ALL of these mean: Move logic to model. Job should only delegate.**

## Common Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| Logic in job | Logic in model | Jobs = thin wrappers |
| `perform(card_id)` then `Card.find` | `perform(card)` | Let ActiveJob serialize |
| 20+ line job | 3-5 line job | Logic belongs in domain model |
| `send_notifications` | `send_notifications_later` | Naming shows async intent |
| Job has conditionals | Model has conditionals | Domain logic in domain model |

## Examples: Wrong vs Right

### ❌ WRONG: Fat job with business logic
```ruby
class Card::ClosureNotificationJob < ApplicationJob
  def perform(card_id, closer_id)
    card = Card.find(card_id)
    card.watchers.each do |watcher|
      CardMailer.closure_notification(watcher, card).deliver_now
      Notification.create!(user: watcher, card: card, action: 'closed')
    end
    card.update!(last_notification_sent_at: Time.current)
  end
end
```

**Problems:** 12 lines of logic, re-queries by ID, hard to test, not reusable, no `_later`/`_now`

### ✅ RIGHT: Thin job delegates to model
```ruby
# Job (3 lines)
class Card::ClosureNotificationJob < ApplicationJob
  def perform(card)
    card.notify_watchers_now
  end
end

# Model (where logic belongs)
def notify_watchers_later
  Card::ClosureNotificationJob.perform_later(self)
end

def notify_watchers_now
  watchers.each do |watcher|
    CardMailer.closure_notification(watcher, self).deliver_now
    Notification.create!(user: watcher, card: self, action: 'closed')
  end
  update_column(:last_notification_sent_at, Time.current)
end
```

**Benefits:** Job is 3 lines, testable without jobs, reusable in console

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "Jobs are meant to contain async work logic" | Jobs are infrastructure. Models contain business logic. |
| "Notification logic belongs in notification job" | Domain logic belongs in domain models, not infrastructure. |
| "Models shouldn't know about email delivery" | Models orchestrate their domain. Mailers handle delivery details. |
| "This follows separation of concerns" | Concern = business vs infrastructure, not job vs model. |
| "The _later/_now pattern adds indirection" | It adds clarity and reusability. Worth it. |
| "Most Rails apps structure jobs this way" | We follow vanilla Rails: rich models, thin everything else. |
| "30 lines is small for a job" | 30 lines is huge. Jobs should be 3-5 lines. |
| "Keeps models thin" | Models should be rich. Jobs should be thin. |
| "This spans multiple models, no natural home" | Primary model orchestrates. See multi-model example. |
| "This is a utility job, no model exists" | Use class methods on relevant model. See cleanup example. |
| "Error handling belongs in jobs" | Use ActiveJob retries. Domain errors in models. |
| "I don't need _now for this" | You need it for testing. Always create _now. |
| "This calls external APIs, not domain logic" | API integration IS domain logic. Model orchestrates. |

## Edge Cases

### Multi-Model: Primary model orchestrates
```ruby
class User::DigestJob < ApplicationJob
  def perform(user); user.send_digest_now; end
end

def send_digest_now
  cards = boards.flat_map { |b| b.cards.mine(self) }
  DigestMailer.send(self, cards).deliver_now
end
```

### Utility/Cleanup: Use class methods
```ruby
class Session::CleanupJob < ApplicationJob
  def perform; Session.cleanup_expired_now; end
end

def self.cleanup_expired_now
  where("created_at < ?", 30.days.ago).delete_all
end
```

### Error Handling: ActiveJob retries + model errors
```ruby
class Card::SyncJob < ApplicationJob
  retry_on ExternalAPI::Error, wait: 5.minutes
  def perform(card); card.sync_to_external_system_now; end
end

def sync_to_external_system_now
  ExternalAPI.update_task(external_id, attributes)
rescue ExternalAPI::Error => e
  errors.add(:base, "Sync failed: #{e.message}")
  raise
end
```

## When You're About to Violate This

**STOP if you're thinking:**
- "I'll put the logic in the job because it's async work"
- "This job needs to query/update records"
- "The model would get too big"
- "It's clearer to have everything in one place"
- "I don't need the _later/_now pattern for this simple case"
- "This spans multiple models, no natural home"
- "This is a utility job, no model exists"
- "Error handling belongs in jobs"
- "I don't need _now because I won't call it directly"

**ALL of these mean: You're about to write a fat job. Stop. Put logic in model.**

## Quick Check

Good job checklist:
- [ ] 3-5 lines total
- [ ] Only calls one model method
- [ ] Receives model instance (not ID)
- [ ] No queries, conditionals, or loops
- [ ] Model has `_later` method
- [ ] Model has `_now` method with logic (ALWAYS, even if only async path)

If ANY checkbox fails, refactor: move logic to model.
