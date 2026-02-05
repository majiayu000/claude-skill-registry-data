---
name: rails-form-objects
description: Create Form Objects for complex form handling, multi-model forms, and validation logic. Use when forms involve multiple models, complex validations, or require business logic beyond simple CRUD operations.
---

# Rails Form Objects Specialist

Specialized in implementing Form Objects pattern for complex form handling.

## When to Use This Skill

- Multi-model forms (e.g., user registration with profile and settings)
- Complex validation logic beyond model validations
- Forms requiring business logic or side effects
- Virtual attributes not directly mapped to database columns
- Forms with conditional validations

## Core Principles

- **ActiveModel Integration**: Include `ActiveModel::Model` for validation support
- **Single Responsibility**: Each form handles one specific form submission
- **Composition**: Coordinate multiple models
- **Validation**: Centralize form-specific validation logic
- **Testability**: Easy to test independently

## Implementation Guidelines

### Basic Form Object

```ruby
# app/forms/user_registration_form.rb
class UserRegistrationForm
    include ActiveModel::Model

    attr_accessor :email, :password, :password_confirmation, :terms_accepted
    attr_accessor :profile_name, :profile_bio

    validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
    validates :password, length: { minimum: 8 }
    validates :password_confirmation, presence: true
    validates :terms_accepted, acceptance: true
    validates :profile_name, presence: true

    # WHY: Ensure password and confirmation match before processing
    validate :passwords_match

    def save
        return false unless valid?

        ActiveRecord::Base.transaction do
            user = create_user
            create_profile(user)
            send_welcome_email(user)
            user
        end
    rescue ActiveRecord::RecordInvalid => e
        # WHY: Add model errors to form object for unified error handling
        errors.add(:base, e.message)
        false
    end

    private

    def passwords_match
        if password != password_confirmation
            errors.add(:password_confirmation, "doesn't match password")
        end
    end

    def create_user
        User.create!(
            email: email,
            password: password
        )
    end

    def create_profile(user)
        UserProfile.create!(
            user: user,
            name: profile_name,
            bio: profile_bio
        )
    end

    def send_welcome_email(user)
        WelcomeMailer.welcome_email(user).deliver_later
    end
end
```

### Controller Integration

```ruby
# app/controllers/registrations_controller.rb
class RegistrationsController < ApplicationController
    def create
        @form = UserRegistrationForm.new(registration_params)

        if @form.save
            redirect_to dashboard_path, notice: 'Registration successful'
        else
            render :new
        end
    end

    private

    def registration_params
        params.require(:user_registration).permit(
            :email, :password, :password_confirmation,
            :terms_accepted, :profile_name, :profile_bio
        )
    end
end
```

### View Integration

```erb
<!-- app/views/registrations/new.html.erb -->
<%= form_with model: @form, url: registrations_path, local: true do |f| %>
  <%= f.label :email %>
  <%= f.email_field :email %>
  <%= f.error_messages_for :email %>

  <%= f.label :password %>
  <%= f.password_field :password %>
  <%= f.error_messages_for :password %>

  <%= f.label :profile_name %>
  <%= f.text_field :profile_name %>
  <%= f.error_messages_for :profile_name %>

  <%= f.check_box :terms_accepted %>
  <%= f.label :terms_accepted, "I accept the terms" %>
  <%= f.error_messages_for :terms_accepted %>

  <%= f.submit "Register" %>
<% end %>
```

## Tools to Use

- `Read`: Read existing form objects and related models
- `Write`: Create new form object files
- `Edit`: Modify existing form objects
- `Bash`: Run tests for form objects
- `mcp__serena__find_symbol`: Find related models and validators

### Bash Commands

```bash
# Create forms directory
mkdir -p app/forms

# Run form object tests
bundle exec rspec spec/forms/user_registration_form_spec.rb
```

## Workflow

1. **Identify Complex Form**: Determine if form needs Form Object pattern
2. **Write Tests First**: Use `rails-rspec-testing` skill
3. **Define Attributes**: Declare all form attributes with `attr_accessor`
4. **Add Validations**: Implement form-specific validations
5. **Implement Save Method**: Coordinate model creation/updates
6. **Handle Errors**: Propagate errors to form object
7. **Test**: Ensure all tests pass

## Related Skills

- `rails-rspec-testing`: For writing form object tests
- `rails-model-design`: For understanding model interfaces
- `rails-transactions`: For transaction coordination
- `rails-service-objects`: For complex business logic within forms

## Coding Standards

See [Rails Coding Standards](../_shared/rails-coding-standards.md)

## TDD Workflow

Follow [TDD Workflow](../_shared/rails-tdd-workflow.md)

## Key Reminders

- Include `ActiveModel::Model` for validation support
- Use transactions for multi-model operations
- Propagate model errors to form object
- Keep form logic separate from models
- Test form objects independently
- Use strong parameters in controllers
