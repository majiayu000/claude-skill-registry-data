---
name: rails-error-handling
description: Implement comprehensive error handling with specific rescue blocks, structured error responses, and proper logging. Use when handling exceptions, implementing error recovery, or building robust error handling strategies.
---

# Rails Error Handling Specialist

Specialized in implementing robust error handling for Rails applications.

## When to Use This Skill

- Implementing service object error handling
- API error responses
- Controller exception handling
- Background job error recovery
- Validation error handling

## Core Principles

- **Specific Rescue Blocks**: Catch specific exceptions
- **Fail Fast**: Don't hide errors
- **Informative Messages**: Provide helpful error information
- **Logging**: Log errors with context
- **User-Friendly**: Show safe messages to users

## Implementation Guidelines

### Service Object Error Handling

```ruby
class DataImportService
    class ValidationError < StandardError; end
    class ProcessingError < StandardError; end

    def call
        validate_input!
        process_data
        Result.success(data: processed_data)
    rescue ValidationError => e
        Result.failure(error_type: :validation, message: e.message)
    rescue ActiveRecord::RecordInvalid => e
        Result.failure(error_type: :database, message: e.message)
    rescue ProcessingError => e
        # WHY: Log processing errors for debugging
        Rails.logger.error("Processing failed: #{e.message}\n#{e.backtrace.join("\n")}")
        Result.failure(error_type: :processing, message: 'Data processing failed')
    rescue StandardError => e
        # WHY: Catch unexpected errors, log details but return safe message
        Rails.logger.error("Unexpected error: #{e.class} - #{e.message}\n#{e.backtrace.join("\n")}")
        Result.failure(error_type: :unexpected, message: 'An unexpected error occurred')
    end

    private

    def validate_input!
        raise ValidationError, 'Input required' if input.blank?
        raise ValidationError, 'Invalid format' unless valid_format?
    end

    def valid_format?
        # Validation logic
    end
end
```

### Controller Error Handling

```ruby
class ApplicationController < ActionController::Base
    # WHY: Centralized error handling for common exceptions
    rescue_from ActiveRecord::RecordNotFound, with: :record_not_found
    rescue_from ActiveRecord::RecordInvalid, with: :record_invalid
    rescue_from ActionController::ParameterMissing, with: :parameter_missing

    private

    def record_not_found(exception)
        Rails.logger.warn("Record not found: #{exception.message}")
        respond_to do |format|
            format.html { redirect_to root_path, alert: 'Record not found' }
            format.json { render json: { error: 'Not found' }, status: :not_found }
        end
    end

    def record_invalid(exception)
        Rails.logger.warn("Invalid record: #{exception.message}")
        respond_to do |format|
            format.html { redirect_back fallback_location: root_path, alert: exception.message }
            format.json { render json: { errors: exception.record.errors }, status: :unprocessable_entity }
        end
    end

    def parameter_missing(exception)
        Rails.logger.warn("Missing parameter: #{exception.param}")
        respond_to do |format|
            format.html { redirect_to root_path, alert: 'Required parameter missing' }
            format.json { render json: { error: "Missing parameter: #{exception.param}" }, status: :bad_request }
        end
    end
end
```

### API Error Responses

```ruby
module Api
    class BaseController < ActionController::API
        rescue_from StandardError, with: :internal_server_error
        rescue_from ActiveRecord::RecordNotFound, with: :not_found
        rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
        rescue_from ActionController::ParameterMissing, with: :bad_request

        private

        def not_found(exception)
            render json: {
                error: {
                    type: 'not_found',
                    message: exception.message
                }
            }, status: :not_found
        end

        def unprocessable_entity(exception)
            render json: {
                error: {
                    type: 'validation_error',
                    message: 'Validation failed',
                    details: exception.record.errors.as_json
                }
            }, status: :unprocessable_entity
        end

        def bad_request(exception)
            render json: {
                error: {
                    type: 'bad_request',
                    message: exception.message
                }
            }, status: :bad_request
        end

        def internal_server_error(exception)
            # WHY: Log full error details for debugging
            Rails.logger.error("Internal error: #{exception.class} - #{exception.message}\n#{exception.backtrace.join("\n")}")

            # WHY: Return safe error message to client
            render json: {
                error: {
                    type: 'internal_server_error',
                    message: 'An unexpected error occurred'
                }
            }, status: :internal_server_error
        end
    end
end
```

### Custom Error Classes

```ruby
# app/errors/application_error.rb
class ApplicationError < StandardError
    attr_reader :error_code, :status

    def initialize(message = nil, error_code: nil, status: :internal_server_error)
        super(message)
        @error_code = error_code
        @status = status
    end
end

# app/errors/authentication_error.rb
class AuthenticationError < ApplicationError
    def initialize(message = 'Authentication failed')
        super(message, error_code: 'AUTH_001', status: :unauthorized)
    end
end

# app/errors/authorization_error.rb
class AuthorizationError < ApplicationError
    def initialize(message = 'Not authorized')
        super(message, error_code: 'AUTH_002', status: :forbidden)
    end
end

# Usage
raise AuthenticationError if token.blank?
raise AuthorizationError unless current_user.admin?
```

### Error Handling with Transactions

```ruby
def transfer_funds(from_account, to_account, amount)
    ActiveRecord::Base.transaction do
        from_account.withdraw!(amount)
        to_account.deposit!(amount)
        Transfer.create!(from: from_account, to: to_account, amount: amount)
    end
    Result.success
rescue ActiveRecord::RecordInvalid => e
    # WHY: Transaction automatically rolled back
    Rails.logger.error("Transfer failed: #{e.message}")
    Result.failure(error: 'Transfer validation failed', details: e.record.errors)
rescue InsufficientFundsError => e
    Result.failure(error: 'Insufficient funds')
rescue StandardError => e
    Rails.logger.error("Unexpected transfer error: #{e.message}\n#{e.backtrace.join("\n")}")
    Result.failure(error: 'Transfer failed')
end
```

### Validation Error Handling

```ruby
class UsersController < ApplicationController
    def create
        @user = User.new(user_params)

        if @user.save
            redirect_to @user, notice: 'User created'
        else
            # WHY: Render form with validation errors
            render :new, status: :unprocessable_entity
        end
    end

    def update
        @user = User.find(params[:id])

        if @user.update(user_params)
            redirect_to @user, notice: 'User updated'
        else
            render :edit, status: :unprocessable_entity
        end
    end
end
```

### Background Job Error Handling

```ruby
class DataProcessingJob < ApplicationJob
    retry_on StandardError, wait: :exponentially_longer, attempts: 5
    discard_on ActiveRecord::RecordNotFound

    def perform(data_id)
        data = Data.find(data_id)
        process_data(data)
    rescue ProcessingError => e
        # WHY: Mark data as failed for manual review
        data.update(status: 'failed', error_message: e.message)
        Rails.logger.error("Processing failed for data #{data_id}: #{e.message}")
        # Don't re-raise, job is done
    rescue StandardError => e
        # WHY: Log error and let retry mechanism handle it
        Rails.logger.error("Unexpected error processing data #{data_id}: #{e.message}")
        raise  # Re-raise for retry
    end
end
```

### Logging Best Practices

```ruby
class OrderProcessingService
    def call
        Rails.logger.info("Processing order #{order.id}")

        result = process_order

        if result.success?
            Rails.logger.info("Order #{order.id} processed successfully")
        else
            # WHY: Include context for debugging
            Rails.logger.error(
                "Order processing failed",
                order_id: order.id,
                user_id: order.user_id,
                error: result.error
            )
        end

        result
    rescue => e
        # WHY: Log full exception with backtrace
        Rails.logger.error({
            message: "Unexpected error processing order",
            order_id: order.id,
            exception: e.class.name,
            error: e.message,
            backtrace: e.backtrace.first(10)
        })
        raise
    end
end
```

## Error Monitoring Integration

```ruby
# Using Sentry/Bugsnag
class ApplicationController < ActionController::Base
    rescue_from StandardError do |exception|
        # WHY: Report to error monitoring service
        Sentry.capture_exception(exception)

        # Then handle normally
        render file: 'public/500.html', status: :internal_server_error, layout: false
    end
end
```

## Tools to Use

- `Read`: Read existing error handling code
- `Edit`: Modify error handling logic
- `Bash`: Test error scenarios
- `mcp__serena__find_symbol`: Find error handling patterns

### Bash Commands

```bash
# Run error handling tests
bundle exec rspec spec/services/data_import_service_spec.rb

# Check logs
tail -f log/development.log

# Test in console
bundle exec rails console
```

## Workflow

1. **Identify Error Scenarios**: List potential failures
2. **Write Tests**: Test both success and failure paths
3. **Implement Specific Rescues**: Catch specific exceptions
4. **Add Logging**: Log errors with context
5. **User Messages**: Return appropriate messages
6. **Test**: Verify error handling works
7. **Monitor**: Track errors in production

## Related Skills

- `rails-service-objects`: Service error handling
- `rails-background-jobs`: Job error handling
- `rails-rspec-testing`: Testing error scenarios

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Use specific rescue blocks, not blanket rescue
- Log errors with sufficient context
- Don't expose sensitive information in error messages
- Use custom error classes for domain-specific errors
- Test both success and failure paths
- Return appropriate HTTP status codes
- Use error monitoring in production
- Document expected exceptions
- Handle validation errors gracefully
- Re-raise errors when appropriate
