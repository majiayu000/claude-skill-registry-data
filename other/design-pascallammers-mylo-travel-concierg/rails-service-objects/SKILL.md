---
name: rails-service-objects
description: Design and implement Rails service objects for complex multi-step business logic. Use when business operations span multiple models, require transaction coordination, or need complex error handling with structured results.
---

# Rails Service Objects Specialist

Specialized in creating clean, testable service objects for complex business workflows.

## When to Use This Skill

- Implementing multi-step business processes (e.g., order processing, payment workflows)
- Coordinating operations across multiple models
- Business logic that requires transaction safety
- Complex workflows with multiple success/failure paths
- Operations that need structured result objects

## Core Principles

- **Single Responsibility**: Each service handles one business operation
- **Call Interface**: Use `call` method as the primary interface
- **Result Objects**: Return structured success/failure results
- **Transaction Safety**: Wrap operations in transactions when needed
- **Testability**: Easy to test in isolation

## Implementation Guidelines

### Basic Service Object Structure

```ruby
# app/services/order_processing_service.rb
class OrderProcessingService
    def initialize(order, options = {})
        @order = order
        @options = options
    end

    def call
        ActiveRecord::Base.transaction do
            validate_order!
            charge_payment
            update_inventory
            send_confirmation
            Result.success(@order)
        end
    rescue => e
        Result.failure(e.message)
    end

    private

    # WHY: Ensure order meets business rules before processing
    def validate_order!
        raise ValidationError unless @order.valid? && @order.items.any?
    end

    def charge_payment
        # Payment processing logic
    end

    def update_inventory
        # Inventory update logic
    end

    def send_confirmation
        # Email notification logic
    end
end
```

### Usage Pattern

```ruby
# In controller
def create
    service = OrderProcessingService.new(order, payment_method: params[:payment_method])
    result = service.call

    if result.success?
        redirect_to order_path(result.data), notice: 'Order processed successfully'
    else
        redirect_to cart_path, alert: result.error
    end
end
```

### Result Object Pattern

```ruby
# app/services/result.rb
class Result
    attr_reader :data, :error

    def self.success(data = nil)
        new(success: true, data: data)
    end

    def self.failure(error)
        new(success: false, error: error)
    end

    def initialize(success:, data: nil, error: nil)
        @success = success
        @data = data
        @error = error
    end

    def success?
        @success
    end

    def failure?
        !@success
    end
end
```

## Tools to Use

- `Read`: Read existing service objects and models
- `Write`: Create new service object files
- `Edit`: Modify existing service objects
- `Bash`: Run tests for service objects
- `mcp__serena__find_symbol`: Find related models and services

### Bash Commands

```bash
# Generate service directory (if needed)
mkdir -p app/services

# Run service tests
bundle exec rspec spec/services/order_processing_service_spec.rb
```

## Workflow

1. **Understand Requirements**: Clarify business logic requirements
2. **Write Tests First**: Use `rails-rspec-testing` skill
3. **Verify Tests Fail**: Confirm tests fail correctly
4. **Implement Service**: Create service object with clear interface
5. **Handle Errors**: Implement proper error handling
6. **Return Results**: Use Result objects for structured responses
7. **Run Tests**: Ensure all tests pass
8. **Run Rubocop**: Validate code style

## Related Skills

- `rails-rspec-testing`: For writing service object tests
- `rails-transactions`: For transaction management within services
- `rails-error-handling`: For comprehensive error handling
- `rails-model-design`: For understanding model interfaces

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Keep services focused on single business operation
- Always return Result objects for consistent interface
- Use transactions when coordinating multiple models
- Extract complex logic into private methods
- Write tests before implementation (TDD)
- Use English comments explaining WHY
