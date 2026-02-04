---
name: rails-transactions
description: Implement database transactions for data consistency and atomicity. Use when operations must succeed or fail together, coordinating multiple database operations, or ensuring data integrity across models.
---

# Rails Transaction Management Specialist

Specialized in implementing safe, atomic database transactions.

## When to Use This Skill

- Operations that must all succeed or all fail (e.g., fund transfers)
- Coordinating updates across multiple models
- Ensuring data consistency and integrity
- Rollback scenarios on error
- Complex business operations requiring atomicity

## Core Principles

- **Atomicity**: All operations succeed or all fail
- **Consistency**: Database remains in valid state
- **Isolation**: Transactions don't interfere with each other
- **Durability**: Committed changes persist

## Implementation Guidelines

### Basic Transaction

```ruby
def transfer_funds(from_account, to_account, amount)
    ActiveRecord::Base.transaction do
        from_account.withdraw!(amount)
        to_account.deposit!(amount)
        Transfer.create!(
            from: from_account,
            to: to_account,
            amount: amount
        )
    end
end
```

### Transaction with Explicit Rollback

```ruby
def process_order(order)
    ActiveRecord::Base.transaction do
        order.update!(status: 'processing')
        payment = charge_payment(order)

        # WHY: Rollback if payment fails
        raise ActiveRecord::Rollback unless payment.successful?

        order.update!(status: 'confirmed')
        inventory.decrement_stock(order.items)
        send_confirmation_email(order)
    end
end
```

### Nested Transactions

```ruby
def create_company_with_users(company_data, users_data)
    ActiveRecord::Base.transaction do
        company = Company.create!(company_data)

        # WHY: Inner transaction for user creation
        users_data.each do |user_data|
            ActiveRecord::Base.transaction(requires_new: true) do
                User.create!(user_data.merge(company: company))
            end
        end

        company
    end
end
```

### Transaction with Locking

```ruby
def reserve_seat(seat_id, user_id)
    ActiveRecord::Base.transaction do
        # WHY: Lock seat record to prevent race conditions
        seat = Seat.lock.find(seat_id)

        raise 'Seat already reserved' if seat.reserved?

        seat.update!(reserved: true, user_id: user_id)
        Reservation.create!(seat: seat, user_id: user_id)
    end
end
```

### Isolation Levels

```ruby
def generate_report_with_consistent_data
    # WHY: Use REPEATABLE READ to ensure data consistency during report generation
    ActiveRecord::Base.transaction(isolation: :repeatable_read) do
        sales_data = Sale.all.to_a
        inventory_data = Inventory.all.to_a

        generate_report(sales_data, inventory_data)
    end
end
```

## Error Handling in Transactions

```ruby
def process_batch(items)
    results = { success: [], failed: [] }

    ActiveRecord::Base.transaction do
        items.each do |item|
            begin
                process_item(item)
                results[:success] << item
            rescue => e
                # WHY: Log error but continue processing other items
                Rails.logger.error("Failed to process item #{item.id}: #{e.message}")
                results[:failed] << { item: item, error: e.message }
            end
        end
    end

    results
end
```

## Tools to Use

- `Read`: Read existing transaction code
- `Edit`: Modify transaction logic
- `Bash`: Run tests with transaction scenarios
- `mcp__serena__find_symbol`: Find transaction usage

### Bash Commands

```bash
# Run transaction tests
bundle exec rspec spec/models/account_spec.rb

# Test in Rails console
bundle exec rails console
```

## Workflow

1. **Identify Atomic Operations**: Determine what must succeed/fail together
2. **Write Tests First**: Test both success and failure scenarios
3. **Wrap in Transaction**: Use `ActiveRecord::Base.transaction`
4. **Add Error Handling**: Handle exceptions appropriately
5. **Test Rollback**: Verify rollback works correctly
6. **Consider Locking**: Add locks if race conditions possible

## Related Skills

- `rails-service-objects`: Transactions often used in services
- `rails-error-handling`: Error handling within transactions
- `rails-model-design`: Understanding model operations

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Always use transactions for multi-model operations
- Use `raise ActiveRecord::Rollback` for explicit rollback
- Consider `lock` for race condition prevention
- Test both success and failure scenarios
- Be aware of transaction nesting behavior
- Use appropriate isolation levels for specific needs
- Avoid long-running operations in transactions
