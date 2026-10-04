---
name: rails
description: "Build Rails applications with Active Record, migrations, controllers, strong parameters, and framework conventions."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["rails", "ruby", "activerecord", "mvc", "api", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Ruby on Rails AI Skill Guide

## Overview & Engine Architecture

Rails is a convention-over-configuration full-stack framework: routing maps to controllers, models use Active Record, and views/JSON serializers form the response. Agents follow Rails conventions (folders, generators, callbacks sparingly), keep business rules in models/services rather than fat controllers, and ship schema changes only via migrations.

```
Router -> Controller -> Model (Active Record)
                \-> Serializer / View -> HTTP
DB <- migrations / schema.rb
```

## When to use this skill

- Building Rails APIs or server-rendered apps
- Adding models, associations, and migrations safely
- Hardening strong parameters and authz (Pundit/CanCanCan)
- Preparing assets/bootsnap for production deploy

## Operational directives

1. Prefer generators (`rails g model|controller|migration`) then edit - stay on rails.
2. Always use strong params; never mass-assign raw `params`.
3. Put irreversible data fixes in data migrations or rake tasks - not only `schema.rb` hope.
4. Keep N+1 queries out with `includes` / `preload` when listing associations.
5. Use `credentials` / ENV for secrets - not committed plaintext.

## Controller + model sketch

```ruby
# app/controllers/items_controller.rb
class ItemsController < ApplicationController
  def create
    item = Item.new(item_params)
    if item.save
      render json: item, status: :created
    else
      render json: { errors: item.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  def item_params
    params.require(:item).permit(:sku, :qty)
  end
end

# app/models/item.rb
class Item < ApplicationRecord
  validates :sku, presence: true, length: { maximum: 64 }
  validates :qty, numericality: { greater_than_or_equal_to: 0 }
end
```

## Commands

```bash
rails new app_name --api
bin/rails db:migrate
bin/rails s
bin/rails test
bin/rails credentials:edit
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Skipping strong params | Mass assignment bugs | `permit` allowlists |
| Callback soup | Hidden side effects | Service objects / jobs |
| N+1 in index | Latency spikes | `includes` |
| Editing prod DB by hand | Drift from migrations | Migration-only changes |

## Best practices

- Use Active Job for email and slow I/O; do not block requests.
- Prefer `has_many` / `belongs_to` with explicit `optional` / `touch` choices.
- Add request specs or system tests for critical flows.
- Match Ruby and Rails majors to what Gemfile.lock and CI install.

## Limitations

- Hotwire/Turbo and API-only modes change front-end assumptions.
- Multi-DB and sharding need explicit Rails multi-database config.
- Engines and large monolith modularization are team-specific.

## Related skills

- `@postgresql` - typical primary store for Rails
- `@docker` - containerizing Puma + assets
- `@graphql-apis` - GraphQL on Rails when REST is not enough
