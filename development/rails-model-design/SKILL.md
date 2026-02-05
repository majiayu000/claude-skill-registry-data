---
name: rails-model-design
description: Design ActiveRecord models with proper validations, associations, scopes, and domain methods. Use when creating new models, refactoring model structure, or adding model-level business logic.
---

# Rails Model Design Specialist

Specialized in designing clean, well-structured ActiveRecord models.

## When to Use This Skill

- Creating new ActiveRecord models
- Defining model associations (belongs_to, has_many, etc.)
- Adding validations and custom validators
- Implementing scopes and query methods
- Adding domain-specific methods to models
- Refactoring model structure

## Core Principles

- **Fat Model, Skinny Controller**: Business logic belongs in models
- **Single Responsibility**: Each model represents one domain concept
- **Validation**: Ensure data integrity at model level
- **Associations**: Define relationships clearly
- **Scopes**: Encapsulate common queries

## Implementation Guidelines

### Basic Model Structure

```ruby
# app/models/order.rb
class Order < ApplicationRecord
    # Associations
    belongs_to :user
    has_many :order_items, dependent: :destroy
    has_many :products, through: :order_items

    # Validations
    validates :status, inclusion: { in: %w[pending confirmed shipped delivered cancelled] }
    validates :total_amount, numericality: { greater_than: 0 }
    validates :user, presence: true

    # Scopes
    scope :recent, -> { order(created_at: :desc) }
    scope :by_status, ->(status) { where(status: status) }
    scope :active, -> { where(status: %w[pending confirmed shipped]) }

    # Domain methods
    def confirm!
        update!(status: 'confirmed', confirmed_at: Time.current)
    end

    def calculate_total
        order_items.sum { |item| item.quantity * item.price }
    end

    def can_cancel?
        %w[pending confirmed].include?(status)
    end
end
```

### Associations

```ruby
# One-to-Many
class User < ApplicationRecord
    has_many :posts, dependent: :destroy
    has_many :comments, dependent: :destroy
end

class Post < ApplicationRecord
    belongs_to :user
    has_many :comments, dependent: :destroy
end

# Many-to-Many
class Post < ApplicationRecord
    has_many :post_tags
    has_many :tags, through: :post_tags
end

class Tag < ApplicationRecord
    has_many :post_tags
    has_many :posts, through: :post_tags
end

# Polymorphic Association
class Comment < ApplicationRecord
    belongs_to :commentable, polymorphic: true
end

class Post < ApplicationRecord
    has_many :comments, as: :commentable
end

class Article < ApplicationRecord
    has_many :comments, as: :commentable
end
```

### Validations

```ruby
class User < ApplicationRecord
    # Presence
    validates :name, presence: true

    # Format
    validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }

    # Uniqueness
    validates :email, uniqueness: { case_sensitive: false }

    # Length
    validates :password, length: { minimum: 8, maximum: 128 }

    # Numericality
    validates :age, numericality: { only_integer: true, greater_than: 0 }

    # Custom validation
    validate :email_must_be_company_domain

    private

    def email_must_be_company_domain
        unless email.ends_with?('@company.com')
            errors.add(:email, 'must be a company email')
        end
    end
end
```

### Scopes and Class Methods

```ruby
class Post < ApplicationRecord
    # Simple scopes
    scope :published, -> { where(published: true) }
    scope :recent, -> { order(created_at: :desc) }

    # Parameterized scopes
    scope :by_author, ->(author_id) { where(author_id: author_id) }
    scope :created_after, ->(date) { where('created_at > ?', date) }

    # Combining scopes
    scope :recent_published, -> { published.recent }

    # Class methods for complex queries
    def self.popular(limit = 10)
        joins(:likes)
            .group(:id)
            .order('COUNT(likes.id) DESC')
            .limit(limit)
    end
end
```

### Callbacks (Use Sparingly)

```ruby
class User < ApplicationRecord
    # Good: Simple, side-effect-free callbacks
    before_save :normalize_email
    before_validation :strip_whitespace

    # Avoid: Complex logic or external service calls
    # Use service objects instead

    private

    def normalize_email
        self.email = email.downcase.strip if email.present?
    end

    def strip_whitespace
        self.name = name.strip if name.present?
    end
end
```

## Tools to Use

- `Read`: Read existing models
- `Write`: Create new model files
- `Edit`: Modify existing models
- `Bash`: Generate models and run migrations
- `mcp__serena__find_symbol`: Find model definitions and methods

### Bash Commands

```bash
# Generate model
bundle exec rails generate model User name:string email:string

# Run migration
bundle exec rails db:migrate

# Run model tests
bundle exec rspec spec/models/user_spec.rb

# Rails console for testing
bundle exec rails console
```

## Workflow

1. **Understand Domain**: Identify entities and relationships
2. **Write Tests First**: Use `rails-rspec-testing` skill
3. **Generate Model**: Use Rails generator or create manually
4. **Define Associations**: Set up model relationships
5. **Add Validations**: Ensure data integrity
6. **Create Scopes**: Encapsulate common queries
7. **Add Domain Methods**: Implement business logic
8. **Run Tests**: Ensure all tests pass

## Related Skills

- `rails-rspec-testing`: For writing model tests
- `rails-query-optimization`: For optimizing model queries
- `rails-database-indexes`: For adding database indexes
- `rails-transactions`: For transaction management

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Define associations before validations
- Use `dependent: :destroy` or `dependent: :nullify` appropriately
- Validate presence of `belongs_to` associations
- Use scopes for reusable queries
- Keep callbacks simple and side-effect-free
- Prefer service objects for complex logic
- Add indexes for foreign keys and frequently queried columns
