---
name: vanilla-rails
description: Use when building Rails + Hotwire applications - covers REST routing, thin controllers, rich models, Turbo Streams/Frames, and Stimulus patterns from 37signals
---

# Rails + Hotwire Patterns

## Overview

Patterns from 37signals' approach to Rails development. Emphasizes REST purity, thin controllers calling rich models, and Hotwire for dynamic interfaces without heavy JavaScript.

**Read `vanilla-rails.md`** for complete patterns and examples (~3000 tokens).

## When to Use This Skill

Use when working on Rails applications with Hotwire:

- Adding new routes, controllers, or actions
- Implementing Turbo Streams or Turbo Frames
- Writing Stimulus controllers
- Organizing model concerns
- Building real-time features with broadcasts

## Quick Reference

### Routing

Model actions as resources. Custom actions become nested resources:

```ruby
# Instead of: post :close, :reopen on cards
resources :cards do
  resource :closure  # create = close, destroy = reopen
end
```

### Controllers

Thin controllers call rich model methods:

```ruby
class Cards::ClosuresController < ApplicationController
  def create
    @card.close(user: Current.user)
  end

  def destroy
    @card.reopen(user: Current.user)
  end
end
```

### Models

Small, focused concerns. One behavior per concern:

```ruby
class Card < ApplicationRecord
  include Closeable, Watchable, Pinnable
end
```

### Turbo Streams

Array-based DOM IDs for scoped targets:

```erb
<%= turbo_stream.replace [@card, :container], partial: "cards/container" %>
```

### Stimulus

Private methods with `#`, dispatch events for coordination:

```javascript
export default class extends Controller {
  #timer

  open() {
    this.dispatch("show")
  }
}
```

## Core Principles

1. **REST purity** - Actions are CRUD on resources
2. **Thin controllers** - Controllers call models, models contain behavior
3. **Small concerns** - One behavior per concern
4. **Turbo-first** - Server renders HTML, Turbo handles updates
5. **Stimulus for sprinkles** - JavaScript enhances, doesn't replace

## Bottom Line

Read `vanilla-rails.md` for the complete guide. These patterns work together - routing informs controller design, controllers return Turbo Streams, Stimulus coordinates the UI.
