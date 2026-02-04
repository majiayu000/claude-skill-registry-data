---
name: rails-state-machines
description: Implement state machines for managing complex workflows and state transitions. Use when models have distinct states with defined transitions, business rules for state changes, or event-driven workflows.
---

# Rails State Machines Specialist

Specialized in implementing state machines using AASM gem for complex workflows.

## When to Use This Skill

- Managing order workflows (pending → confirmed → shipped → delivered)
- User account states (inactive → active → suspended)
- Document approval processes
- Payment processing states
- Any domain with well-defined state transitions

## Core Principles

- **Explicit States**: Clearly defined states
- **Controlled Transitions**: Events trigger state changes
- **Guards**: Validate transitions
- **Callbacks**: Execute logic on state changes
- **Single Source of Truth**: State stored in database

## Implementation Guidelines

### Basic State Machine

```ruby
# Gemfile
gem 'aasm'

# app/models/order.rb
class Order < ApplicationRecord
    include AASM

    aasm column: :status do
        state :pending, initial: true
        state :confirmed, :shipped, :delivered, :cancelled

        event :confirm do
            transitions from: :pending, to: :confirmed
            after do
                # WHY: Update confirmation timestamp and send notification
                update!(confirmed_at: Time.current)
                OrderMailer.confirmation_email(self).deliver_later
            end
        end

        event :ship do
            transitions from: :confirmed, to: :shipped
            after do
                update!(shipped_at: Time.current)
                notify_shipping_service
            end
        end

        event :deliver do
            transitions from: :shipped, to: :delivered
            after do
                update!(delivered_at: Time.current)
            end
        end

        event :cancel do
            transitions from: [:pending, :confirmed], to: :cancelled
            after do
                refund_payment
                restore_inventory
            end
        end
    end

    private

    def notify_shipping_service
        # Shipping service integration
    end

    def refund_payment
        # Payment refund logic
    end

    def restore_inventory
        # Restore inventory logic
    end
end
```

### Usage in Controllers

```ruby
class OrdersController < ApplicationController
    def confirm
        @order = Order.find(params[:id])

        if @order.may_confirm?
            @order.confirm!
            redirect_to @order, notice: 'Order confirmed'
        else
            redirect_to @order, alert: 'Cannot confirm order'
        end
    rescue AASM::InvalidTransition => e
        redirect_to @order, alert: e.message
    end
end
```

### Guards (Conditional Transitions)

```ruby
class Order < ApplicationRecord
    include AASM

    aasm do
        state :pending, initial: true
        state :processing, :completed

        event :process do
            # WHY: Only allow processing if payment succeeded
            transitions from: :pending, to: :processing, guard: :payment_successful?
        end

        event :complete do
            # WHY: Require all items shipped before completion
            transitions from: :processing, to: :completed, guard: :all_items_shipped?
        end
    end

    def payment_successful?
        payment&.status == 'successful'
    end

    def all_items_shipped?
        order_items.all?(&:shipped?)
    end
end
```

### Multiple Transitions for Same Event

```ruby
class Document < ApplicationRecord
    include AASM

    aasm do
        state :draft, initial: true
        state :under_review, :approved, :rejected

        event :submit do
            # WHY: Route to review if complete, else stay in draft
            transitions from: :draft, to: :under_review, guard: :complete?
            transitions from: :draft, to: :draft, unless: :complete?

            after do
                notify_reviewers if under_review?
            end
        end

        event :review do
            transitions from: :under_review, to: :approved
            transitions from: :under_review, to: :rejected
        end
    end

    def complete?
        title.present? && content.present?
    end
end
```

### Error Handling

```ruby
class Order < ApplicationRecord
    include AASM

    aasm do
        state :pending, initial: true
        state :processing, :completed, :failed

        event :process do
            transitions from: :pending, to: :processing

            error do |e|
                # WHY: Log error and transition to failed state
                Rails.logger.error("Order processing failed: #{e.message}")
                self.error_message = e.message
                may_fail? ? fail! : raise
            end

            after do
                charge_payment
            end
        end

        event :fail do
            transitions from: :processing, to: :failed
        end
    end

    def charge_payment
        # May raise exception
        PaymentService.charge(self)
    end
end
```

### State Scopes

```ruby
class Order < ApplicationRecord
    include AASM

    aasm do
        state :pending, initial: true
        state :confirmed, :shipped, :delivered, :cancelled
        # ... events ...
    end

    # Automatically creates scopes
    # Order.pending
    # Order.confirmed
    # Order.shipped
end

# Usage
Order.confirmed.where(user: current_user)
```

### State Queries

```ruby
# Check current state
order.aasm_state  # => "confirmed"
order.pending?    # => false
order.confirmed?  # => true

# Check possible transitions
order.aasm.states(permitted: true)  # => [:shipped, :cancelled]

# Check if transition allowed
order.may_ship?      # => true
order.may_deliver?   # => false

# Get current event
order.aasm.current_event  # => :ship
```

## Testing State Machines

```ruby
# spec/models/order_spec.rb
RSpec.describe Order, type: :model do
    describe 'state machine' do
        let(:order) { create(:order) }

        it 'starts in pending state' do
            expect(order).to be_pending
        end

        describe '#confirm' do
            it 'transitions from pending to confirmed' do
                expect { order.confirm! }
                    .to change { order.aasm_state }
                    .from('pending').to('confirmed')
            end

            it 'updates confirmed_at timestamp' do
                expect { order.confirm! }
                    .to change { order.confirmed_at }
                    .from(nil)
            end

            it 'sends confirmation email' do
                expect(OrderMailer).to receive(:confirmation_email)
                order.confirm!
            end
        end

        describe '#ship' do
            it 'cannot ship pending order' do
                expect(order.may_ship?).to be false
            end

            it 'can ship confirmed order' do
                order.confirm!
                expect(order.may_ship?).to be true
            end
        end
    end
end
```

## Tools to Use

- `Read`: Read existing state machine code
- `Write`: Create new state machine models
- `Edit`: Modify state machines
- `Bash`: Run tests and migrations

### Bash Commands

```bash
# Add AASM gem
bundle add aasm

# Generate migration for state column
bundle exec rails generate migration AddStatusToOrders status:string

# Run tests
bundle exec rspec spec/models/order_spec.rb
```

## Workflow

1. **Identify States**: Define all possible states
2. **Define Events**: List state transitions
3. **Write Tests**: Test each transition
4. **Implement State Machine**: Add AASM to model
5. **Add Callbacks**: Implement after/before logic
6. **Add Guards**: Implement conditional transitions
7. **Test**: Verify all transitions work

## Related Skills

- `rails-model-design`: Understanding model structure
- `rails-service-objects`: Complex transition logic
- `rails-background-jobs`: Async operations after transitions
- `rails-rspec-testing`: Testing state machines

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Define initial state explicitly
- Use guards for conditional transitions
- Add callbacks for side effects
- Test all transitions and guards
- Use `may_event?` to check before transitioning
- Handle `AASM::InvalidTransition` exceptions
- Keep state machine logic in the model
- Use scopes for querying by state
