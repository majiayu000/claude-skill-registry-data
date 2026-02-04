---
name: vanilla-rails-controllers
description: Use when writing Rails controllers, adding controller actions, or implementing state changes (close, archive, publish, assign) - enforces resource extraction instead of custom actions
---

# Vanilla Rails Controllers

**Core principle:** State changes are resources. Model state changes with CRUD operations on resource controllers, never custom actions.

## When to Use

Use this skill when:
- Adding any state change to a model (close, archive, publish, assign, follow, etc.)
- Creating new controller actions
- Routing state transitions

**Red flags - STOP and extract a resource:**
- Adding `post :close`, `post :archive`, `patch :activate`
- Adding custom actions to existing resource routes
- Thinking "it's just a boolean toggle"
- Time pressure rationalizing "can refactor later"

## Resource Extraction Pattern

**The 37signals pattern:** Every state change becomes its own resource controller.

```ruby
# ❌ BAD - custom actions (typical Rails tutorials)
resources :cards do
  post :close
  post :reopen
  post :archive
  post :unarchive
end

# ✅ GOOD - state as resource (37signals pattern)
resources :cards do
  resource :closure, only: [:create, :destroy]
  resource :archival, only: [:create, :destroy]
end
```

**Why singular `resource`?** Each card has at most ONE closure state, ONE archival state. Singular resource = no ID in URL.

**Why `only: [:create, :destroy]`?** Creating resource = entering state. Destroying resource = leaving state.

## Thin Controllers Calling Model Methods

Controllers delegate to intention-revealing model API. Keep business logic in models.

```ruby
# ❌ BAD - ActiveRecord calls in controller
class Cards::ArchivalsController < ApplicationController
  def create
    @card = Card.find(params[:id])
    @card.update(archived: true)  # Business logic in controller
    redirect_to board_cards_path(@card.board)
  end
end

# ✅ GOOD - delegate to model
class Cards::ArchivalsController < ApplicationController
  include CardScoped  # Sets @card from params

  def create
    @card.archive  # Intention-revealing model method

    respond_to do |format|
      format.turbo_stream
      format.json { head :no_content }
    end
  end

  def destroy
    @card.unarchive

    respond_to do |format|
      format.turbo_stream
      format.json { head :no_content }
    end
  end
end
```

**Model implements business logic:**

```ruby
module Card::Archivable
  extend ActiveSupport::Concern

  included do
    has_one :archival, dependent: :destroy
    scope :archived, -> { joins(:archival) }
    scope :active, -> { where.missing(:archival) }
  end

  def archived?
    archival.present?
  end

  def archive(user: Current.user)
    unless archived?
      transaction do
        create_archival! user: user
        track_event :archived, creator: user
      end
    end
  end

  def unarchive
    archival&.destroy if archived?
  end
end
```

## Strong Parameters with params.expect()

Use `params.expect()` instead of `params.require().permit()`:

```ruby
# ❌ BAD - old Rails pattern
def card_params
  params.require(:card).permit(:title, :description, :column_id)
end

# ✅ GOOD - Rails 8+ params.expect
def card_params
  params.expect(card: [:title, :description, :column_id])
end
```

## Common State Resource Patterns

| State Change | Resource Name | create = | destroy = |
|--------------|---------------|----------|-----------|
| Close/Reopen | `closure` | close | reopen |
| Archive/Unarchive | `archival` | archive | unarchive |
| Pin/Unpin | `pinning` or `pin` | pin | unpin |
| Publish/Unpublish | `publication` | publish | unpublish |
| Assign/Unassign | `assignment` | assign | unassign |
| Follow/Unfollow | `subscription` | subscribe | unsubscribe |
| Mark/Unmark as golden | `goldness` | gild | ungild |

## Common Rationalizations (STOP)

| Excuse | Reality |
|--------|---------|
| "It's just a boolean toggle - resource is overkill" | Booleans ARE state. State changes ARE resources. Pattern applies. |
| "I've seen `post :close` in Rails guides" | Standard Rails != 37signals Rails. Follow the codebase pattern. |
| "Creating a whole controller adds complexity" | 15 lines of controller is NOT complex. Clear, intention-revealing code. |
| "Time pressure - customer demo tomorrow" | Writing it wrong takes same time. Doing it right the first time is FASTER. |
| "Can refactor to resources later" | You won't. Do it right now while context is fresh. |
| "Direct `update()` is more readable" | `@card.archive` is MORE readable than `@card.update(archived: true)`. |
| "Association/table overhead for a boolean" | Tracks WHO and WHEN. Enables auditing, activity timeline, proper scopes. Worth it. |
| "Migration adds extra step" | One migration is NOT extra work. It's standard implementation. Do it. |

**All of these mean: Extract resource, delegate to model. No exceptions.**

## Real-World Examples from Fizzy

**Closing cards:**
```ruby
# routes.rb
resources :cards do
  resource :closure
end

# app/controllers/cards/closures_controller.rb
class Cards::ClosuresController < ApplicationController
  include CardScoped

  def create
    @card.close
    respond_to do |format|
      format.turbo_stream
      format.json { head :no_content }
    end
  end

  def destroy
    @card.reopen
    respond_to do |format|
      format.turbo_stream
      format.json { head :no_content }
    end
  end
end

# app/models/card/closeable.rb
module Card::Closeable
  def close(user: Current.user)
    unless closed?
      transaction do
        create_closure! user: user
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
end
```

## Implementation Checklist

When adding state change to a model:

- [ ] Extract resource (singular if card has one state, plural if many)
- [ ] Add route: `resource :archival, only: [:create, :destroy]`
- [ ] Create migration for state table (see Migration Pattern below)
- [ ] Create resource controller in namespace (e.g., `Cards::ArchivalsController`)
- [ ] Implement `create` (enter state) and `destroy` (leave state) actions
- [ ] Controllers delegate to model methods (`@card.archive`, not `@card.update`)
- [ ] Create model concern with intention-revealing methods
- [ ] Use `has_one :archival` association for state tracking
- [ ] Add scopes (`.archived`, `.active`) for querying
- [ ] Use `params.expect()` for strong parameters (if needed)

## Migration Pattern

State resources need a join table tracking when the state was entered and by whom:

```ruby
# db/migrate/TIMESTAMP_create_card_archivals.rb
class CreateCardArchivals < ActiveRecord::Migration[8.0]
  def change
    create_table :card_archivals, id: :uuid do |t|
      t.uuid :card_id, null: false
      t.uuid :user_id
      t.timestamps

      t.index [:card_id], unique: true
    end
  end
end
```

**Note:** Table name follows pattern: `card_` + plural of resource name
- `resource :closure` → table `closures` (not `card_closures`)
- `resource :goldness` → table `card_goldnesses` (prefixed because goldness is namespaced)
- `resource :archival` → table `card_archivals` (prefixed for clarity)

## Quick Reference

**Naming formula:**
- Route: `resource :STATE_NAME` (singular)
- Controller: `Cards::STATE_NAMEsController` (ALWAYS plural - `ClosuresController`, `ArchivalsController`)
- Controller file: `app/controllers/cards/STATE_NAMEs_controller.rb`
- Model: `def STATE_VERB` (e.g., `def archive`, `def close`)
- Association: `has_one :STATE_NAME`
- Migration: `create_table :card_STATE_NAMEs` or `create_table :STATE_NAMEs`

**Controller template:**
```ruby
class Cards::STATEsController < ApplicationController
  include CardScoped

  def create
    @card.enter_state
    respond_to do |format|
      format.turbo_stream
      format.json { head :no_content }
    end
  end

  def destroy
    @card.leave_state
    respond_to do |format|
      format.turbo_stream
      format.json { head :no_content }
    end
  end
end
```
