---
name: vanilla-rails-style
description: Use when refactoring Ruby/Rails code, organizing methods, deciding on guard clauses vs if/else, or following 37signals conventions - these patterns are counter to standard Ruby style guides
---

# Vanilla Rails Style

**These conventions CONTRADICT standard Ruby style guides.** They reflect production 37signals/Basecamp code.

## When to Use

You're writing Ruby/Rails code for 37signals-style projects. Symptoms that trigger this skill:
- Refactoring methods with guard clauses
- Organizing private methods in a class
- Deciding whether to add a bang to method name
- Structuring controllers and models
- Creating background jobs

## Counter-Intuitive Patterns

These patterns violate what most Ruby developers consider "best practice":

| Pattern | 37signals Way | Standard Ruby Way |
|---------|---------------|-------------------|
| Conditionals | Prefer if/else | Prefer guard clauses |
| Private indentation | Indent under `private` | No indentation (Rubocop) |
| Bang methods | Only with counterpart | Flag "dangerous" actions |
| Method order | Invocation sequence | Alphabetical |
| Controllers | Thin + rich models | Service objects |

## Red Flags - STOP and Reconsider

If you're about to do any of these, you're violating 37signals style:

| Red Flag | Instead, Do This |
|----------|------------------|
| Add guard clauses (`return unless`, `return if`) | Use if/else (unless at method start with complex body) |
| Remove indentation from private methods | Indent 2 spaces under `private` |
| Add bang to a method without counterpart | Use plain name (e.g., `close` not `close!`) |
| Alphabetize private methods | Order by invocation sequence |
| Create a service object as special artifact | Move logic to model, call from controller |

**These violations require explicit approval. Don't deviate without discussion.**

## Quick Reference

| Situation | 37signals Way | See Section |
|-----------|---------------|-------------|
| Early return needed? | if/else (or guard at method start if body complex) | Expanded Conditionals |
| Private methods? | Indent 2 spaces under `private` | Private Indentation |
| Ordering methods? | Invocation sequence (caller before callee) | Method Ordering |
| New controller action? | Create new resource instead | CRUD Controllers |
| Complex business logic? | Rich model method, thin controller | Controller/Model |
| Destructive method name? | No bang unless counterpart exists | Bang Methods |
| Background job? | Use `_later`/`_now` pattern | Background Jobs |

## Code Style Patterns

### Expanded Conditionals (NOT Guard Clauses)

**Prefer `if/else` over guard clauses** - opposite of most Ruby advice:

```ruby
# Good (37signals style)
def todos_for_new_group
  if ids = params.require(:todolist)[:todo_ids]
    @bucket.recordings.todos.find(ids.split(","))
  else
    []
  end
end

# Bad
def todos_for_new_group
  ids = params.require(:todolist)[:todo_ids]
  return [] unless ids
  @bucket.recordings.todos.find(ids.split(","))
end
```

**Why:** Guard clauses can be hard to read, especially when nested.

**Exception - Guard Clauses ARE Allowed When BOTH:**
- Return is RIGHT AT THE BEGINNING of the method (first line after method def), AND
- Main method body is NOT TRIVIAL (5+ lines of substantial logic)

```ruby
# Allowed - guard at start, complex body below
def after_recorded_as_commit(recording)
  return if recording.parent.was_created?

  if recording.was_created?
    broadcast_new_column(recording)
  else
    broadcast_column_change(recording)
  end
end
```

**Multiple guard clauses - convert to nested if/else:**

```ruby
# Bad - multiple guard clauses
def process_payment(params)
  amount = params[:amount]
  return { error: "Missing amount" } unless amount

  method = params[:method]
  return { error: "Missing method" } unless method

  valid = validate_payment(amount, method)
  return { error: "Invalid" } unless valid

  charge(amount, method)
end

# Good - nested if/else
def process_payment(params)
  if amount = params[:amount]
    if method = params[:method]
      if validate_payment(amount, method)
        charge(amount, method)
      else
        { error: "Invalid" }
      end
    else
      { error: "Missing method" }
    end
  else
    { error: "Missing amount" }
  end
end
```

### Private Method Indentation (YES, Really)

**Indent methods under `private`** - counter to Rubocop default:

```ruby
class SomeClass
  def some_method
    # ...
  end

  private
    def private_method_1
      # indented 2 spaces
    end

    def private_method_2
      # indented 2 spaces
    end
end
```

**Important:** No newline after `private` keyword.

**Exception - Module with ONLY Private Methods:**

```ruby
module SomeModule
  private

  def some_private_method
    # not indented
    # blank line after private
  end
end
```

### Method Ordering

**Order by invocation sequence, not alphabetically:**

1. `class` methods
2. `public` methods (with `initialize` at the very top)
3. `private` methods (ordered by call sequence)

```ruby
class SomeClass
  def self.class_method
    # class methods first
  end

  def initialize
    # initialize first among instance methods
  end

  def some_method
    method_1
    method_2
  end

  private
    def method_1
      method_1_1
      method_1_2
    end

    def method_1_1
      # appears after caller (method_1)
    end

    def method_1_2
      # appears after method_1_1
    end

    def method_2
      # appears after method_1 (called second)
    end
end
```

**Why:** Invocation order shows execution flow. Makes code easier to trace.

### Bang Methods (Restrictive Rule)

**Only use bang when non-bang counterpart exists:**

```ruby
# Good - has counterpart
save / save!
update / update!

# Bad - no counterpart, just use `close`
def close!
  # wrong - there's no `close` method
end

# Good - single method, no bang
def close
  # destructive action, but no bang needed
end
```

**Why:** Don't use bang to flag "destructive actions". Many destructive Ruby/Rails methods lack it.

## Architecture Patterns

### CRUD Controllers (Resource-Oriented)

**Model actions as CRUD on resources.** When action doesn't map to standard CRUD verb, introduce new resource:

```ruby
# Bad - custom actions
resources :cards do
  post :close
  post :reopen
end

# Good - new resource
resources :cards do
  resource :closure
end
```

### Controller/Model Interaction (Vanilla Rails)

**Thin controllers, rich domain models.** No service objects as special artifacts.

**Plain Active Record is fine:**

```ruby
class Cards::CommentsController < ApplicationController
  def create
    @comment = @card.comments.create!(comment_params)
  end
end
```

**Complex behavior - clear model APIs:**

```ruby
class Cards::GoldnessesController < ApplicationController
  def create
    @card.gild
  end
end
```

**Form objects when truly needed (e.g., coordinating multiple models):**

```ruby
# Signup coordinates Identity + User creation
Signup.new(email_address: email_address).create_identity
```

Don't create service objects as default pattern. Prefer rich model methods.

### Background Jobs (_later/_now Pattern)

**Shallow job classes delegating to models:**

- Suffix `_later` for methods that enqueue jobs
- Suffix `_now` for synchronous counterpart

```ruby
module Event::Relaying
  extend ActiveSupport::Concern

  included do
    after_create_commit :relay_later
  end

  def relay_later
    Event::RelayJob.perform_later(self)
  end

  def relay_now
    # actual logic here
  end
end

class Event::RelayJob < ApplicationJob
  def perform(event)
    event.relay_now
  end
end
```

## Common Mistakes

### Guard Clause in Middle of Method

```ruby
# WRONG - guard clause after other logic
def process
  setup_data
  return unless valid?
  execute_action
end

# RIGHT - if/else shows full flow
def process
  setup_data
  if valid?
    execute_action
  end
end
```

### Private Method Not Indented

```ruby
# WRONG - no indentation under private
class Processor
  def process
    # ...
  end

  private
  def helper
    # ...
  end
end

# RIGHT - indent under private
class Processor
  def process
    # ...
  end

  private
    def helper
      # ...
    end
end
```

### Bang Without Counterpart

```ruby
# WRONG - no close method exists
class Account
  def close!
    update(closed: true)
  end
end

# RIGHT - no bang needed
class Account
  def close
    update(closed: true)
  end
end
```

### Alphabetical Method Order

```ruby
# WRONG - alphabetized
class Builder
  def build
    prepare
    format
    output
  end

  private
    def format
      # ...
    end

    def output
      # ...
    end

    def prepare
      # ...
    end
end

# RIGHT - invocation order
class Builder
  def build
    prepare
    format
    output
  end

  private
    def prepare
      # ...
    end

    def format
      # ...
    end

    def output
      # ...
    end
end
```

## Common Rationalizations

| You'll Think | Reality |
|--------------|---------|
| "Guard clauses are Ruby best practice" | 37signals prefers if/else for readability, especially with nesting |
| "Early returns reduce nesting" | Nested if/else shows complete logic flow |
| "Rubocop doesn't indent private methods" | 37signals style intentionally differs from Rubocop |
| "Bang means dangerous/destructive" | Only use ! when you have both safe and dangerous variants |
| "Alphabetical order helps find methods" | Invocation order helps trace execution flow |
| "I should extract a service object" | Keep logic in models, controllers call rich model APIs |
| "Service objects separate concerns" | Only use when truly justified, not as default pattern |

## Philosophy

37signals optimizes for **reading code**, not writing it. These conventions:

- Make execution flow explicit (invocation ordering)
- Show complete logic in one place (if/else over guard clauses)
- Reduce indirection (rich models over service layers)
- Maintain visual consistency (private indentation)

**These rules apply to ALL new code. Apply these patterns strictly. Don't deviate without explicit approval.**

## Self-Check Before Committing

- [ ] Used if/else instead of guard clauses (except single guard at method start with complex body)
- [ ] Indented all private methods under `private` keyword
- [ ] Ordered methods by invocation sequence, not alphabetically
- [ ] Only added bang to methods with non-bang counterparts
- [ ] Kept business logic in models, not service objects
- [ ] Used resource-oriented routing (no custom controller actions)
