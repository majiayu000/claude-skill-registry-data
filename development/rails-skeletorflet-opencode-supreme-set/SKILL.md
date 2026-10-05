---
name: rails
description: Ruby on Rails web framework. Use when building Rails apps, ActiveRecord models, migrations, RESTful routes, Hotwire/Stimulus/Turbo, Action Cable, or RSpec testing.
---

## rails

MVC framework prioritizing conventions over configuration for rapid web development.

### Core Concepts
- MVC architecture: Models handle data, Views render templates, Controllers manage request flow
- ActiveRecord ORM: convention-based object-relational mapping, auto-generates queries from associations
- Migrations: version-controlled schema changes, rollback support, Ruby DSL instead of raw SQL
- RESTful routes: `resources :posts` generates 8 standard CRUD routes automatically

### Common Patterns
- Hotwire/Stimulus/Turbo: server-rendered HTML with minimal JavaScript, Turbo Streams for live updates
- Action Cable WebSockets: real-time features via pub/sub channels integrated with Active Job
- Service objects: extract complex business logic from controllers/models into dedicated classes
- Concern modules: share behavior across models/controllers via `ActiveSupport::Concern`

### Best Practices
- Fat model, thin controller: keep business logic in models/services, controllers stay lean
- RSpec over MiniTest: domain-specific language with readable expectations and context blocks
- Database-level constraints: add unique indexes and foreign keys beyond ActiveRecord validations
- Environment-specific configs: use credentials.yml.enc for secrets, dotenv for local dev

### Common Code Patterns
- `before_action :require_login` for controller-level authentication guards
- `has_many :through` for many-to-many relationships with join models
