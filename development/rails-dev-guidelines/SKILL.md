---
name: rails-dev-guidelines
description: Rails MVC patterns, ActiveRecord, conventions, and best practices
---

# Rails Development Guidelines

## Purpose

This skill ensures consistent, maintainable Rails code following conventions and best practices for the application.

## When to Use This Skill

- Creating or modifying models, controllers, or other Rails components
- Implementing business logic or data access patterns
- Working with ActiveRecord associations, validations, or queries
- Creating migrations or modifying the database schema
- Implementing background jobs or service objects
- Following Rails conventions and idiomatic patterns

## Core Rails Conventions

### Directory Structure

```
app/
├── models/          # Business logic and data models
├── components/      # View components (ViewComponent gem)
├── controllers/     # Request handling and response rendering
├── views/           # Templates (ERB, Turbo)
├── helpers/         # View helpers
├── jobs/            # Background jobs
├── mailers/         # Email sending
├── services/        # Complex business logic
├── queries/         # Complex database queries
├── forms/           # Form objects for complex forms
└── concerns/        # Shared modules (models & controllers)
```

## Model Development Checklist

When creating or modifying a model:

- [ ] Use singular name (e.g., `User`, not `Users`)
- [ ] Place validations before associations and callbacks
- [ ] Use database-level constraints with migrations
- [ ] Add indexes for foreign keys and frequently queried columns
- [ ] Use scopes for reusable queries
- [ ] Keep concerns in `app/models/concerns/`
- [ ] Write comprehensive model specs with factories

## Controller Development Checklist

When creating or modifying a controller:

- [ ] Use RESTful routes when possible
- [ ] Keep actions thin (extract to services/queries)
- [ ] Use strong parameters (`params.require().permit()`)
- [ ] Set instance variables only for view data
- [ ] Use `before_action` for authentication/authorization
- [ ] Handle errors with `rescue_from` or inline rescues
- [ ] Write request specs for all endpoints

## Core Principles

### 1. Fat Models, Skinny Controllers

❌ **Don't** put business logic in controllers:
```ruby
# app/controllers/users_controller.rb
def create
  @user = User.new(user_params)
  @user.email = params[:email].downcase
  @user.role = 'member'
  @user.save

  UserMailer.welcome_email(@user).deliver_later
  Analytics.track_signup(@user)

  redirect_to @user
end
```

✅ **Do** move logic to models or services:
```ruby
# app/controllers/users_controller.rb
def create
  @user = User.create_with_defaults(user_params)

  if @user.persisted?
    redirect_to @user, notice: 'Welcome!'
  else
    render :new, status: :unprocessable_entity
  end
end

# app/models/user.rb
class User < ApplicationRecord
  after_create :send_welcome_email
  after_create :track_signup

  def self.create_with_defaults(params)
    user = new(params)
    user.email = user.email.downcase
    user.role ||= 'member'
    user.save
    user
  end

  private

  def send_welcome_email
    UserMailer.welcome_email(self).deliver_later
  end

  def track_signup
    Analytics.track_signup(self)
  end
end
```

### 2. Use Service Objects for Complex Operations

❌ **Don't** cram complex workflows into models:
```ruby
class Order < ApplicationRecord
  def process_payment
    # 50+ lines of payment processing logic
  end
end
```

✅ **Do** extract to service objects:
```ruby
# app/services/order_processor.rb
class OrderProcessor
  def initialize(order)
    @order = order
  end

  def process
    return false unless valid?

    ActiveRecord::Base.transaction do
      charge_payment
      update_inventory
      send_confirmation
    end

    true
  rescue PaymentError => e
    @order.errors.add(:base, e.message)
    false
  end

  private

  def valid?
    @order.valid? && @order.items.any?
  end

  # ... more private methods
end
```

### 3. Strong Parameters Are Required

❌ **Don't** use raw params:
```ruby
def create
  User.create(params[:user])  # Security vulnerability!
end
```

✅ **Do** use strong parameters:
```ruby
def create
  @user = User.new(user_params)
  # ...
end

private

def user_params
  params.require(:user).permit(:email, :name, :role)
end
```

### 4. Use Database Constraints

❌ **Don't** rely only on ActiveRecord validations:
```ruby
# app/models/user.rb
validates :email, uniqueness: true
```

✅ **Do** add database constraints too:
```ruby
# db/migrate/xxx_create_users.rb
create_table :users do |t|
  t.string :email, null: false
  t.timestamps
end

add_index :users, :email, unique: true

# app/models/user.rb
validates :email, presence: true, uniqueness: true
```

### 5. Avoid N+1 Queries

❌ **Don't** lazy load associations in loops:
```ruby
@users = User.all
@users.each do |user|
  puts user.posts.count  # N+1 query!
end
```

✅ **Do** eager load associations:
```ruby
@users = User.includes(:posts).all
@users.each do |user|
  puts user.posts.count  # No extra queries
end
```

## Anti-Patterns

### ❌ Don't Use Callbacks for Business Logic
Callbacks make models hard to test and reason about. Use service objects instead.

### ❌ Don't Skip Validations
Never use `save(validate: false)` or `update_column` unless absolutely necessary.

### ❌ Don't Put SQL in Controllers
Extract complex queries to query objects or scopes.

### ❌ Don't Use `find_by_sql` Without Reason
Use ActiveRecord query interface when possible.

### ❌ Don't Expose Internal IDs
Use slugs or UUIDs for public-facing URLs.

## Quick Reference: Common Patterns

### Associations
```ruby
belongs_to :user
has_many :posts
has_many :comments, through: :posts
has_one :profile, dependent: :destroy
```

### Validations
```ruby
validates :email, presence: true, uniqueness: true, format: { with: URI::MailTo::EMAIL_REGEXP }
validates :age, numericality: { greater_than: 18 }
validates :terms, acceptance: true
```

### Scopes
```ruby
scope :active, -> { where(active: true) }
scope :recent, -> { order(created_at: :desc).limit(10) }
scope :by_role, ->(role) { where(role: role) }
```

### Callbacks (Use Sparingly)
```ruby
before_validation :normalize_email
after_create :send_notification
after_destroy :cleanup_associated_data
```

## Navigation Guide

Need help with:
- **ActiveRecord Associations** → See `resources/associations.md`
- **Validations & Constraints** → See `resources/validations.md`
- **Query Optimization** → See `resources/queries.md`
- **Service Objects Pattern** → See `resources/service-objects.md`
- **Background Jobs** → See `resources/background-jobs.md`
- **Security Best Practices** → See `resources/security.md`

## Resource Files

1. **associations.md** - Detailed guide on ActiveRecord associations
2. **validations.md** - Validation patterns and database constraints
3. **queries.md** - Query optimization and avoiding N+1 queries
4. **service-objects.md** - Service object patterns for complex logic
5. **background-jobs.md** - Solid Queue and background job patterns
6. **security.md** - Security best practices for Rails

## Related Skills

- **rspec-testing-guidelines** - For writing comprehensive tests
- **devise-auth-patterns** - For authentication implementation
- **database-design-patterns** - For schema design and migrations
- **security-best-practices** - For security concerns

---

**Status**: Core skill (~450 lines) | 6 resource files
