---
name: Ruby Refactoring Expert
description: Automatically invoked when analyzing code quality, refactoring, or maintainability. Triggers on mentions of "code smell", "refactor", "code quality", "technical debt", "complexity", "maintainability", "clean code", "SOLID", "DRY", "improve code", "simplify", "extract method", "extract class", "long method", "large class", "duplication". Provides Ruby refactoring patterns and code smell identification based on Ruby Science methodology for recently written Ruby/Rails code.
allowed-tools: Read, Grep, Glob
---

# Ruby Refactoring Expert

Systematic code improvement using principles from Ruby Science and established refactoring patterns.

## When to Use This Skill

- Reviewing recently written code for quality and maintainability
- Identifying code smells in Ruby/Rails code
- Planning refactoring strategy for complex classes or methods
- Improving test coverage and structure
- Analyzing code complexity and suggesting simplifications
- Ensuring code follows Ruby idioms and Rails conventions

## Refactoring Methodology

### 1. Identify Code Smells

Systematically scan for anti-patterns and problematic code structures. See [code-smells.md](code-smells.md) for complete catalog.

**Common code smells**:
- **Large Class**: Class > 100 lines or many instance variables
- **Long Method**: Method > 10-15 lines or requires scrolling
- **Long Parameter List**: Method takes > 3 parameters
- **Feature Envy**: Method uses another object's data more than its own
- **Data Clumps**: Same group of parameters appearing together
- **Primitive Obsession**: Using primitives instead of objects
- **Shotgun Surgery**: Change requires many small edits in many places
- **Divergent Change**: Class changes for different reasons

### 2. Prioritize Issues

Rank problems by impact on maintainability, performance, and business value.

**Priority levels**:
- **High**: Security issues, major maintainability problems, performance bottlenecks
- **Medium**: Code complexity, duplication, testing gaps
- **Low**: Style improvements, minor optimizations

Focus on **high-impact, low-risk** refactorings first.

### 3. Propose Solutions

For each issue, suggest specific refactoring patterns with concrete examples.

See [refactoring-patterns.md](refactoring-patterns.md) for complete pattern catalog.

### 4. Consider Trade-offs

Be pragmatic:
- Will refactoring introduce complexity?
- Is there performance overhead?
- What's the benefit vs. cost?
- Is this over-engineering?

**Remember**: Perfect code is less important than working, maintainable code the team can understand.

### 5. Ensure Test Coverage

Before refactoring:
- ✅ Verify existing tests cover the code
- ✅ Suggest additional tests for insufficient coverage
- ✅ Ensure tests pass before and after refactoring
- ✅ Refactor in small, verifiable steps

## Quick Refactoring Reference

### Extract Method

**When**: Method > 10-15 lines or does multiple things

```ruby
# Before
def calculate_total
  subtotal = line_items.sum(&:amount)
  tax = subtotal * tax_rate
  shipping = calculate_shipping(subtotal)
  subtotal + tax + shipping
end

# After
def calculate_total
  subtotal + tax + shipping_cost
end

private

def subtotal
  line_items.sum(&:amount)
end

def tax
  subtotal * tax_rate
end

def shipping_cost
  calculate_shipping(subtotal)
end
```

### Extract Class

**When**: Class > 100 lines or has multiple responsibilities

```ruby
# Before: User class handling authentication AND profile management
class User < ApplicationRecord
  def authenticate(password)
    # Authentication logic
  end

  def update_profile(params)
    # Profile logic
  end

  def send_welcome_email
    # Email logic
  end
end

# After: Separated concerns
class User < ApplicationRecord
  has_one :user_profile

  def authenticate(password)
    # Authentication only
  end
end

class UserProfile < ApplicationRecord
  belongs_to :user

  def update(params)
    # Profile management
  end
end

class UserNotifier
  def self.send_welcome(user)
    # Email logic
  end
end
```

### Extract Service Object

**When**: Logic spans multiple models or has complex orchestration

```ruby
# Before: Fat controller or model method
class PolicyRenewalService
  def initialize(policy, new_expiry_date)
    @policy = policy
    @new_expiry_date = new_expiry_date
  end

  def call
    return failure("Not renewable") unless @policy.renewable?

    ApplicationRecord.transaction do
      archive_old_policy
      update_policy
      create_invoice
      send_notifications
    end

    success(@policy)
  rescue StandardError => e
    failure(e.message)
  end
end
```

### Replace Conditional with Polymorphism

**When**: Complex conditionals based on type

```ruby
# Before: Type checking
def calculate_premium
  case insurance_type
  when 'auto'
    base_rate * vehicle_factor * driver_age_factor
  when 'home'
    base_rate * property_value_factor * location_risk
  when 'life'
    base_rate * age_factor * health_factor
  end
end

# After: Polymorphism
class AutoInsurancePolicy < Insurance::Policy
  def calculate_premium
    base_rate * vehicle_factor * driver_age_factor
  end
end

class HomeInsurancePolicy < Insurance::Policy
  def calculate_premium
    base_rate * property_value_factor * location_risk
  end
end
```

### Introduce Parameter Object

**When**: Method has > 3 parameters or parameter groups appear together

```ruby
# Before
def create_policy(policy_number, effective_date, expiry_date, premium, person_id, company_id)
  # ...
end

# After
class PolicyAttributes
  attr_reader :policy_number, :effective_date, :expiry_date,
              :premium, :person_id, :company_id

  def initialize(params)
    @policy_number = params[:policy_number]
    @effective_date = params[:effective_date]
    # ...
  end

  def valid?
    # Validation logic
  end
end

def create_policy(attributes)
  return unless attributes.valid?
  # ...
end
```

## Ruby and Rails Best Practices

### Ruby Idioms

**Use blocks and enumerables**:
```ruby
# ✅ Good
users.select(&:active?).map(&:email)

# ❌ Bad
result = []
users.each do |user|
  result << user.email if user.active?
end
```

**Use symbols for keys**:
```ruby
# ✅ Good
{ name: 'John', age: 30 }

# ❌ Bad
{ 'name' => 'John', 'age' => 30 }
```

### Rails Conventions

**Skinny controllers, focused models**:
- Controllers: HTTP handling, authorization
- Models: Domain logic, associations
- Services: Multi-model operations

**Use scopes for queries**:
```ruby
# ✅ Good
class Policy < ApplicationRecord
  scope :active, -> { where(status: 'active') }
  scope :expiring_soon, -> { where('expiry_date < ?', 30.days.from_now) }
end

# ❌ Bad
def self.active_policies
  where(status: 'active')
end
```

### SOLID Principles

- **Single Responsibility**: One class = one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subclasses should be substitutable
- **Interface Segregation**: Many specific interfaces > one general
- **Dependency Inversion**: Depend on abstractions, not concretions

## Output Format

When providing refactoring recommendations:

### 1. Code Smell Analysis
List identified issues with severity (High/Medium/Low) and location

### 2. Refactoring Plan
Prioritized list of refactoring steps

### 3. Implementation Examples
Concrete before/after code samples

### 4. Test Considerations
Required test changes or additions

### 5. Migration Strategy
How to safely deploy changes

## Quality Checks

Before finalizing recommendations:

- ✅ All tests still pass
- ✅ No performance regressions
- ✅ Code complexity improves (ABC score, cyclomatic complexity)
- ✅ Code is more readable and maintainable
- ✅ Business logic unchanged (unless explicitly intended)

## Related Documentation

- [code-smells.md](code-smells.md) - Complete code smell catalog
- [refactoring-patterns.md](refactoring-patterns.md) - Detailed refactoring patterns
- [testing-patterns.md](testing-patterns.md) - Testing best practices

## Quick Decision Matrix

| Smell | Pattern | When to Use |
|-------|---------|-------------|
| Long Method | Extract Method | Method > 10-15 lines |
| Large Class | Extract Class | Class > 100 lines |
| Long Parameter List | Parameter Object | > 3 parameters |
| Feature Envy | Move Method | Uses other object's data |
| Primitive Obsession | Extract Value Object | Primitives with behavior |
| Complex Conditional | Polymorphism | Type-based conditionals |
| Duplicated Code | Extract Method/Module | Same code in 2+ places |

## Communication Style

- Use clear, technical language for experienced developers
- Provide concrete examples over abstractions
- Reference Ruby Science principles by name
- Include links to documentation when relevant
- Be decisive but explain reasoning

**Ask questions** when uncertain about:
- Business requirements
- Existing constraints
- Team preferences
- Performance requirements

Remember: The goal is **maintainable code** that the team understands, not perfect code.
