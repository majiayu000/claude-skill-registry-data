---
name: "Rails Conventions & Patterns"
description: "Comprehensive Ruby on Rails conventions, design patterns, and idiomatic code standards. Use this skill when writing any Rails code including controllers, models, services, or when making architectural decisions about code organization, naming conventions, and Rails best practices."
---

# Rails Conventions & Patterns Skill

This skill provides authoritative guidance on Ruby on Rails conventions, design patterns, and idiomatic code standards for production applications.

## When to Use This Skill

- Writing new Rails controllers, models, or services
- Refactoring existing Rails code
- Making decisions about code organization
- Choosing between different Rails patterns
- Ensuring code follows Rails conventions
- Reviewing Rails code for convention compliance

## Ruby & Rails Versions

```yaml
ruby: "3.2+ (prefer 3.3+ for YJIT benefits)"
rails: "7.1+ (prefer 8.0+ for new projects)"
```

## Rails 7.x/8.x Modern Features

### Rails 7.1+ Features
```ruby
# Composite Primary Keys
class BookOrder < ApplicationRecord
  self.primary_key = [:shop_id, :id]
  belongs_to :shop
  has_many :line_items, foreign_key: [:shop_id, :order_id]
end

# ActiveRecord::Encryption (sensitive data)
class User < ApplicationRecord
  encrypts :email, deterministic: true
  encrypts :ssn, :credit_card
end

# Horizontal Sharding
class ApplicationRecord < ActiveRecord::Base
  connects_to shards: {
    default: { writing: :primary, reading: :primary_replica },
    shard_two: { writing: :primary_shard_two }
  }
end

# Async Query Loading
posts = Post.where(published: true).load_async
# Do other work
posts.to_a # Wait for results

# Normalize values before validation
class User < ApplicationRecord
  normalizes :email, with: -> { _1.strip.downcase }
  normalizes :phone, with: -> { _1.gsub(/\D/, '') }
end
```

### Rails 8.0+ Features
```ruby
# Improved Solid Queue (built-in job backend)
# config/application.rb
config.active_job.queue_adapter = :solid_queue

# Solid Cache (built-in caching)
# config/application.rb
config.cache_store = :solid_cache_store

# Authentication generator
rails generate authentication

# Built-in rate limiting
class Api::PostsController < Api::BaseController
  rate_limit to: 10, within: 1.minute, only: :create
end

# Per-environment credentials
rails credentials:edit --environment production
```

### Modern Ruby 3.3+ Features
```ruby
# Pattern matching in case expressions
case user
in { role: "admin", active: true }
  grant_full_access
in { role: "user", active: true }
  grant_standard_access
else
  deny_access
end

# Endless method definitions (one-liners)
def full_name = "#{first_name} #{last_name}"
def published? = published_at.present?

# Data class (immutable value objects, Ruby 3.2+)
User = Data.define(:id, :name, :email)
user = User.new(id: 1, name: "Alice", email: "alice@example.com")

# YJIT optimization (Ruby 3.3+)
# config/application.rb
if defined?(RubyVM::YJIT.enable)
  RubyVM::YJIT.enable
end
```

## File Organization Standards

### Models
```yaml
location: "app/models/"
max_lines: 200
guidance: |
  Focus on associations, validations, scopes, and essential callbacks.
  Extract business logic to Service Objects.
  Keep models focused on data persistence and domain rules.
```

### Controllers
```yaml
location: "app/controllers/"
max_lines: 100
guidance: |
  Limit to REST actions. Use before_action for shared logic.
  Complex operations delegate to Service Objects.
  Follow "Skinny Controller, Fat Model (but not too fat)" pattern.
```

## Comprehensive Controller Patterns

### RESTful Controller Structure
```ruby
class PostsController < ApplicationController
  before_action :authenticate_user!
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authorize_post, only: [:edit, :update, :destroy]

  # GET /posts
  def index
    @posts = Post.published.page(params[:page])
  end

  # GET /posts/:id
  def show
    # @post set by before_action
  end

  # GET /posts/new
  def new
    @post = Post.new
  end

  # POST /posts
  def create
    @post = CreatePostService.call(current_user, post_params)

    if @post.persisted?
      redirect_to @post, notice: "Post created successfully"
    else
      render :new, status: :unprocessable_entity
    end
  end

  # GET /posts/:id/edit
  def edit
    # @post set by before_action
  end

  # PATCH /posts/:id
  def update
    if UpdatePostService.call(@post, post_params)
      redirect_to @post, notice: "Post updated successfully"
    else
      render :edit, status: :unprocessable_entity
    end
  end

  # DELETE /posts/:id
  def destroy
    @post.destroy!
    redirect_to posts_url, notice: "Post deleted successfully"
  end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def authorize_post
    authorize @post # Pundit
  end

  def post_params
    params.require(:post).permit(:title, :body, :published)
  end
end
```

### API Controller Patterns
```ruby
# app/controllers/api/base_controller.rb
module Api
  class BaseController < ActionController::API
    include ActionController::HttpAuthentication::Token::ControllerMethods

    before_action :authenticate_api_user!

    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
    rescue_from Pundit::NotAuthorizedError, with: :forbidden

    private

    def authenticate_api_user!
      authenticate_or_request_with_http_token do |token, options|
        @current_user = User.find_by(api_token: token)
      end
    end

    def not_found(exception)
      render json: { error: exception.message }, status: :not_found
    end

    def unprocessable_entity(exception)
      render json: { errors: exception.record.errors }, status: :unprocessable_entity
    end

    def forbidden
      render json: { error: "Forbidden" }, status: :forbidden
    end
  end
end

# app/controllers/api/v1/posts_controller.rb
module Api
  module V1
    class PostsController < Api::BaseController
      def index
        posts = Post.published.page(params[:page])
        render json: PostBlueprint.render(posts, root: :posts)
      end

      def create
        post = CreatePostService.call(current_user, post_params)

        if post.persisted?
          render json: PostBlueprint.render(post), status: :created
        else
          render json: { errors: post.errors }, status: :unprocessable_entity
        end
      end
    end
  end
end
```

### Hotwire Controller Patterns
```ruby
class PostsController < ApplicationController
  # Turbo Stream responses
  def create
    @post = CreatePostService.call(current_user, post_params)

    respond_to do |format|
      if @post.persisted?
        format.turbo_stream
        format.html { redirect_to @post }
      else
        format.turbo_stream { render :form_errors, status: :unprocessable_entity }
        format.html { render :new, status: :unprocessable_entity }
      end
    end
  end

  def update
    respond_to do |format|
      if UpdatePostService.call(@post, post_params)
        format.turbo_stream
        format.html { redirect_to @post }
      else
        format.turbo_stream { render :form_errors, status: :unprocessable_entity }
        format.html { render :edit, status: :unprocessable_entity }
      end
    end
  end
end

# app/views/posts/create.turbo_stream.erb
<%= turbo_stream.prepend "posts", @post %>
<%= turbo_stream.update "new_post_form", "" %>
```

### Nested Resource Controllers
```ruby
class CommentsController < ApplicationController
  before_action :set_post
  before_action :set_comment, only: [:show, :edit, :update, :destroy]

  # GET /posts/:post_id/comments
  def index
    @comments = @post.comments.page(params[:page])
  end

  # POST /posts/:post_id/comments
  def create
    @comment = @post.comments.build(comment_params)
    @comment.user = current_user

    if @comment.save
      redirect_to [@post, @comment]
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def set_post
    @post = Post.find(params[:post_id])
  end

  def set_comment
    @comment = @post.comments.find(params[:id])
  end
end
```

### Controller Concerns
```ruby
# app/controllers/concerns/paginatable.rb
module Paginatable
  extend ActiveSupport::Concern

  included do
    before_action :set_pagination_params
  end

  private

  def set_pagination_params
    @page = params[:page] || 1
    @per_page = params[:per_page] || 25
  end

  def paginate(collection)
    collection.page(@page).per(@per_page)
  end
end

# Usage
class PostsController < ApplicationController
  include Paginatable

  def index
    @posts = paginate(Post.published)
  end
end
```

### Services
```yaml
location: "app/services/"
naming: "{Domain}Manager::{Action} (e.g., OrdersManager::CreateOrder)"
structure: |
  class OrdersManager::CreateOrder
    def initialize(user:, params:)
      @user = user
      @params = params
    end

    def call
      # Single public entry point
      # Returns Result object or raises
    end

    private

    # Small, focused private methods
  end
```

### Methods
```yaml
max_lines: 15
max_params: 4
guidance: "If method needs more params, use a Parameter Object or Hash"
```

## Naming Conventions

```yaml
classes: "PascalCase"
methods: "snake_case"
predicates: "end with ? (e.g., active?, valid?)"
dangerous_methods: "end with ! (e.g., save!, destroy!)"
constants: "SCREAMING_SNAKE_CASE"
private_methods: "Prefix with purpose, not underscore"
```

## Ruby Idioms

### Prefer
- Guard clauses over nested conditionals
- Explicit returns for clarity
- `&.` (safe navigation) over `try`
- Keyword arguments for 2+ parameters
- `Struct`/`Data` for simple value objects
- `frozen_string_literal: true` pragma

### Avoid
- `unless` with `else`
- Nested ternaries
- `and`/`or` for control flow
- Monkey patching in application code

## Pattern Decision Tree

**Always inspect existing codebase patterns before recommending any pattern.**

### Service Object
```ruby
# Use when:
# - Business logic spans multiple models
# - Operation has multiple steps
# - Logic doesn't belong to any single model
# - Need to orchestrate external services

# Avoid when:
# - Simple CRUD operation
# - Logic clearly belongs to one model
# - Single-line delegation

# Inspect first:
# ls app/services/
# Check existing service naming convention
```

### Form Object
```ruby
# Use when:
# - Form spans multiple models
# - Complex validations not tied to persistence
# - Wizard/multi-step forms

# Avoid when:
# - Standard single-model form
# - Simple attribute updates

# Inspect first:
# ls app/forms/ 2>/dev/null
# grep -r 'include ActiveModel' app/ --include='*.rb'
```

### Query Object
```ruby
# Use when:
# - Complex queries with multiple conditions
# - Query logic reused across controllers
# - Query needs composition/chaining

# Avoid when:
# - Simple scope suffices
# - One-off query

# Inspect first:
# ls app/queries/ 2>/dev/null
# grep -r 'class.*Query' app/ --include='*.rb'
```

### Concern
```ruby
# Use when:
# - Truly shared behavior across 3+ unrelated models
# - Behavior is cohesive and self-contained

# Avoid when:
# - Only 1-2 models share the code
# - Behavior is not cohesive
# - Just to 'clean up' a model

# Inspect first:
# ls app/models/concerns/ app/controllers/concerns/
# Check how many models use each concern
```

### Decorator/Presenter
```ruby
# Use when:
# - View logic becoming complex
# - Same presentation logic in multiple views
# - Need to augment model for display

# Avoid when:
# - Simple attribute display
# - One-off formatting

# Inspect first:
# ls app/decorators/ app/presenters/ 2>/dev/null
# grep 'draper' Gemfile
```

## ActionMailer Conventions

### Mailer Structure
```ruby
# app/mailers/user_mailer.rb
class UserMailer < ApplicationMailer
  default from: 'notifications@example.com'

  def welcome_email(user)
    @user = user
    @url = root_url

    mail(
      to: email_address_with_name(@user.email, @user.name),
      subject: 'Welcome to My App'
    )
  end

  def password_reset(user, token)
    @user = user
    @token = token
    @reset_url = edit_password_reset_url(token: @token)

    mail(to: @user.email, subject: 'Password Reset Instructions')
  end

  private

  def email_address_with_name(email, name)
    Mail::Address.new(email).tap { |a| a.display_name = name }.format
  end
end

# app/views/user_mailer/welcome_email.html.erb
<h1>Welcome <%= @user.name %>!</h1>
<p>Click here to get started: <%= link_to 'Get Started', @url %></p>

# app/views/user_mailer/welcome_email.text.erb
Welcome <%= @user.name %>!

Click here to get started: <%= @url %>
```

### Mailer Testing
```ruby
# spec/mailers/user_mailer_spec.rb
RSpec.describe UserMailer, type: :mailer do
  describe '#welcome_email' do
    let(:user) { create(:user, email: 'user@example.com') }
    let(:mail) { UserMailer.welcome_email(user) }

    it 'renders the subject' do
      expect(mail.subject).to eq('Welcome to My App')
    end

    it 'renders the receiver email' do
      expect(mail.to).to eq([user.email])
    end

    it 'renders the sender email' do
      expect(mail.from).to eq(['notifications@example.com'])
    end

    it 'contains user name' do
      expect(mail.body.encoded).to match(user.name)
    end
  end
end
```

### Mailer Previews (Rails 4.1+)
```ruby
# test/mailers/previews/user_mailer_preview.rb
class UserMailerPreview < ActionMailer::Preview
  def welcome_email
    UserMailer.welcome_email(User.first)
  end

  def password_reset
    user = User.first
    token = SecureRandom.urlsafe_base64
    UserMailer.password_reset(user, token)
  end
end

# Visit: http://localhost:3000/rails/mailers/user_mailer/welcome_email
```

### Background Delivery
```ruby
# Deliver later (asynchronous)
UserMailer.welcome_email(@user).deliver_later

# Deliver later with delay
UserMailer.welcome_email(@user).deliver_later(wait: 1.hour)

# Deliver later at specific time
UserMailer.welcome_email(@user).deliver_later(wait_until: Date.tomorrow.noon)

# Deliver now (synchronous)
UserMailer.welcome_email(@user).deliver_now
```

## Background Job Conventions

### ActiveJob Structure
```ruby
# app/jobs/application_job.rb
class ApplicationJob < ActiveJob::Base
  # Global retry configuration
  retry_on StandardError, wait: :exponentially_longer, attempts: 5
  retry_on ActiveRecord::Deadlocked, wait: 5.seconds, attempts: 3

  # Discard specific errors
  discard_on ActiveJob::DeserializationError

  # Global error handling
  rescue_from(Exception) do |exception|
    ErrorTracker.notify(exception)
    raise exception
  end
end

# app/jobs/send_welcome_email_job.rb
class SendWelcomeEmailJob < ApplicationJob
  queue_as :mailers

  def perform(user)
    UserMailer.welcome_email(user).deliver_now
  end
end

# Usage
SendWelcomeEmailJob.perform_later(user)
```

### Sidekiq-Specific Patterns
```ruby
# app/jobs/process_order_job.rb
class ProcessOrderJob < ApplicationJob
  queue_as :orders

  # Sidekiq-specific options
  sidekiq_options retry: 3,
                  backtrace: true,
                  dead: true

  def perform(order_id)
    order = Order.find(order_id)
    OrderProcessor.new(order).process!
  end
end

# config/sidekiq.yml
:queues:
  - critical
  - default
  - mailers
  - low_priority

:schedule:
  daily_cleanup:
    cron: '0 0 * * *'  # Daily at midnight
    class: DailyCleanupJob
```

### Job Testing
```ruby
# spec/jobs/send_welcome_email_job_spec.rb
RSpec.describe SendWelcomeEmailJob, type: :job do
  include ActiveJob::TestHelper

  let(:user) { create(:user) }

  it 'enqueues the job' do
    expect {
      SendWelcomeEmailJob.perform_later(user)
    }.to have_enqueued_job(SendWelcomeEmailJob).with(user)
  end

  it 'sends welcome email' do
    expect {
      perform_enqueued_jobs do
        SendWelcomeEmailJob.perform_later(user)
      end
    }.to change { ActionMailer::Base.deliveries.count }.by(1)
  end

  it 'retries on failure' do
    allow(UserMailer).to receive(:welcome_email).and_raise(StandardError)

    expect {
      SendWelcomeEmailJob.perform_later(user)
    }.to have_enqueued_job(SendWelcomeEmailJob).on_queue(:mailers)
  end
end
```

## Action Cable (WebSocket) Conventions

### Channel Structure
```ruby
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
    end

    private

    def find_verified_user
      if verified_user = User.find_by(id: cookies.encrypted[:user_id])
        verified_user
      else
        reject_unauthorized_connection
      end
    end
  end
end

# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  def subscribed
    # Stream from specific room
    stream_from "chat_#{params[:room_id]}"

    # Or stream for current user
    stream_for current_user
  end

  def unsubscribed
    # Cleanup when channel is unsubscribed
    stop_all_streams
  end

  def speak(data)
    # Receive data from client
    message = current_user.messages.create!(
      content: data['message'],
      room_id: params[:room_id]
    )

    # Broadcast to all subscribers
    ActionCable.server.broadcast(
      "chat_#{params[:room_id]}",
      message: render_message(message)
    )
  end

  private

  def render_message(message)
    ApplicationController.render(
      partial: 'messages/message',
      locals: { message: message }
    )
  end
end
```

### Client-Side JavaScript
```javascript
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

consumer.subscriptions.create(
  { channel: "ChatChannel", room_id: roomId },
  {
    connected() {
      console.log("Connected to chat")
    },

    disconnected() {
      console.log("Disconnected from chat")
    },

    received(data) {
      const messages = document.getElementById('messages')
      messages.insertAdjacentHTML('beforeend', data.message)
    },

    speak(message) {
      this.perform('speak', { message: message })
    }
  }
)
```

### Broadcasting from Models
```ruby
# app/models/message.rb
class Message < ApplicationRecord
  belongs_to :user
  belongs_to :room

  after_create_commit :broadcast_message

  private

  def broadcast_message
    broadcast_append_to(
      [room, :messages],
      target: "messages",
      partial: "messages/message",
      locals: { message: self }
    )
  end
end
```

### Cable Testing
```ruby
# spec/channels/chat_channel_spec.rb
RSpec.describe ChatChannel, type: :channel do
  let(:user) { create(:user) }
  let(:room) { create(:room) }

  before do
    stub_connection(current_user: user)
  end

  it 'successfully subscribes' do
    subscribe(room_id: room.id)
    expect(subscription).to be_confirmed
    expect(subscription).to have_stream_from("chat_#{room.id}")
  end

  it 'broadcasts messages' do
    subscribe(room_id: room.id)

    expect {
      perform :speak, message: 'Hello'
    }.to have_broadcasted_to("chat_#{room.id}")
  end
end
```

## Enhanced Concern Best Practices

### When to Use Concerns
```ruby
# GOOD: Truly shared behavior across unrelated models
# app/models/concerns/publishable.rb
module Publishable
  extend ActiveSupport::Concern

  included do
    scope :published, -> { where(published: true) }
    scope :draft, -> { where(published: false) }

    validates :published_at, presence: true, if: :published?
  end

  def publish!
    update!(published: true, published_at: Time.current)
  end

  def unpublish!
    update!(published: false, published_at: nil)
  end
end

# Used in multiple unrelated models
class Post < ApplicationRecord
  include Publishable
end

class Video < ApplicationRecord
  include Publishable
end

class Podcast < ApplicationRecord
  include Publishable
end
```

### Concern with Dependencies
```ruby
# app/models/concerns/taggable.rb
module Taggable
  extend ActiveSupport::Concern

  included do
    # Dependencies injection
    has_many :taggings, as: :taggable, dependent: :destroy
    has_many :tags, through: :taggings

    scope :tagged_with, ->(tag_name) {
      joins(:tags).where(tags: { name: tag_name })
    }
  end

  # Instance methods
  def tag_names=(names)
    self.tags = names.map { |n| Tag.find_or_create_by(name: n.strip) }
  end

  def tag_names
    tags.pluck(:name)
  end

  # Class methods
  class_methods do
    def most_tagged(limit = 10)
      select('taggable_id, COUNT(*) as tags_count')
        .group('taggable_id')
        .order('tags_count DESC')
        .limit(limit)
    end
  end
end
```

### Controller Concerns
```ruby
# app/controllers/concerns/error_handling.rb
module ErrorHandling
  extend ActiveSupport::Concern

  included do
    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
    rescue_from Pundit::NotAuthorizedError, with: :unauthorized
  end

  private

  def not_found
    respond_to do |format|
      format.html { render 'errors/404', status: :not_found }
      format.json { render json: { error: 'Not found' }, status: :not_found }
    end
  end

  def unprocessable_entity(exception)
    respond_to do |format|
      format.html { render 'errors/422', status: :unprocessable_entity }
      format.json { render json: { errors: exception.record.errors }, status: :unprocessable_entity }
    end
  end

  def unauthorized
    respond_to do |format|
      format.html { redirect_to root_path, alert: 'Not authorized' }
      format.json { render json: { error: 'Not authorized' }, status: :forbidden }
    end
  end
end

# Usage
class ApplicationController < ActionController::Base
  include ErrorHandling
end
```

## Method Visibility Rules

### Public
```ruby
# Callable from anywhere, defines the API
# Controller actions must be public
# Methods called from views must be public
# Service interface methods

# Rails context:
# - Controller: only public methods are routable
# - Model: public methods accessible from controllers/views
# - Component: only public methods callable from templates
```

### Private
```ruby
# Can only be called within the class, without explicit receiver
# Implementation details
# Helper methods not part of public API
# Methods that should never be called externally

# Rails context:
# - Controller: helper methods, before_action callbacks
# - Service: internal computation methods
# - Model: internal validation helpers

# CRITICAL: Private methods CANNOT be called from outside the class.
# If a view needs data, the component MUST have a public method.
```

### Protected
```ruby
# Callable from same class or subclasses
# Methods meant for inheritance
# Rare in typical Rails apps

# Rails context:
# - Occasionally in base controllers/models for shared behavior
```

## Delegation Patterns

### Using delegate
```ruby
# Creates public forwarding methods
# LIMITATION: Cannot delegate to private methods on target

delegate :method1, :method2, to: :target

class Component < ViewComponent::Base
  delegate :total, :count, to: :@service
  
  def initialize(service:)
    @service = service
  end
end
# Now view can call component.total
```

### Wrapper Methods
```ruby
# Use when:
# - Need to transform data
# - Need to add caching
# - Need different method names
# - Need to handle errors

class Component < ViewComponent::Base
  def total
    @service.calculate_total
  rescue ServiceError
    0
  end
end
```

### attr_reader Exposure
```ruby
# Expose the underlying object directly
# Use sparingly - breaks encapsulation

class Component < ViewComponent::Base
  attr_reader :service
  
  def initialize(service:)
    @service = service
  end
end
# View calls: component.service.calculate_total
```

## Rails Request Cycle

```
Request → Route → Controller#action
       → Controller → Service/Model (business logic)
       → Controller → sets @instance_variables
       → Controller → renders View
       → View → calls methods on @variables
       → View → renders Components
       → Component → accesses only its own methods
```

**Key Insight**: Each layer can only access what the previous layer explicitly provides. Views can't magically access service internals.

## Implementation Order

Always implement in dependency order (bottom-up):

```
1. Database migrations (if needed)
2. Models (foundation)
3. Services (business logic)
4. Components (presentation wrappers)
5. Controllers (orchestration)
6. Views (final layer)
7. Tests (verify everything works)
```

**Rationale**: Each layer depends on the ones below it. Implementing bottom-up ensures dependencies exist before they're used.

## Code Quality Standards

### Method Size
- Maximum 15 lines per method
- Single responsibility per method
- Extract complex logic to private helper methods

### Class Size
- Models: max 200 lines
- Controllers: max 100 lines
- Services: max 150 lines

### Parameter Count
- Maximum 4 parameters
- Use keyword arguments for 2+ parameters
- Use Parameter Objects for complex cases

## Form Objects (Expanded)

### Basic Form Object
```ruby
# app/forms/user_registration_form.rb
class UserRegistrationForm
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :email, :string
  attribute :password, :string
  attribute :password_confirmation, :string
  attribute :first_name, :string
  attribute :last_name, :string
  attribute :accept_terms, :boolean

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :password_confirmation, presence: true
  validates :first_name, :last_name, presence: true
  validates :accept_terms, acceptance: true
  validate :passwords_match

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      @user = User.create!(
        email: email,
        password: password,
        first_name: first_name,
        last_name: last_name
      )

      @profile = @user.create_profile!(
        full_name: "#{first_name} #{last_name}"
      )

      SendWelcomeEmailJob.perform_later(@user)
    end

    true
  rescue ActiveRecord::RecordInvalid => e
    errors.add(:base, e.message)
    false
  end

  attr_reader :user, :profile

  private

  def passwords_match
    return if password == password_confirmation

    errors.add(:password_confirmation, "doesn't match password")
  end
end

# Controller usage
def create
  @form = UserRegistrationForm.new(registration_params)

  if @form.save
    redirect_to @form.user, notice: 'Registration successful'
  else
    render :new, status: :unprocessable_entity
  end
end
```

### Multi-Step Wizard Form
```ruby
# app/forms/checkout_wizard.rb
class CheckoutWizard
  include ActiveModel::Model

  STEPS = [:shipping, :payment, :confirmation].freeze

  attr_accessor :current_step
  attr_reader :order

  delegate :shipping_address, :billing_address, :payment_method,
           :shipping_address=, :billing_address=, :payment_method=,
           to: :order

  validates :shipping_address, presence: true, if: :shipping_step?
  validates :payment_method, presence: true, if: :payment_step?

  def initialize(order, current_step: :shipping)
    @order = order
    @current_step = current_step.to_sym
  end

  def next_step
    return if last_step?

    self.current_step = STEPS[STEPS.index(current_step) + 1]
  end

  def previous_step
    return if first_step?

    self.current_step = STEPS[STEPS.index(current_step) - 1]
  end

  def save
    return false unless valid?

    order.save
  end

  def first_step?
    current_step == STEPS.first
  end

  def last_step?
    current_step == STEPS.last
  end

  private

  def shipping_step?
    current_step == :shipping
  end

  def payment_step?
    current_step == :payment
  end
end
```

## Decorators (Expanded)

### Draper Decorator Pattern
```ruby
# Gemfile
gem 'draper'

# app/decorators/application_decorator.rb
class ApplicationDecorator < Draper::Decorator
  delegate_all

  def created_at
    h.content_tag(:time, object.created_at.strftime("%B %d, %Y"),
                  datetime: object.created_at.iso8601)
  end
end

# app/decorators/user_decorator.rb
class UserDecorator < ApplicationDecorator
  def full_name
    "#{object.first_name} #{object.last_name}"
  end

  def profile_link
    h.link_to full_name, h.user_path(object), class: 'user-link'
  end

  def avatar
    if object.avatar.attached?
      h.image_tag object.avatar.variant(resize_to_limit: [100, 100])
    else
      h.image_tag 'default-avatar.png', alt: full_name
    end
  end

  def status_badge
    css_class = object.active? ? 'badge-success' : 'badge-secondary'
    status_text = object.active? ? 'Active' : 'Inactive'

    h.content_tag(:span, status_text, class: "badge #{css_class}")
  end

  def member_since
    "Member since #{object.created_at.strftime('%B %Y')}"
  end
end

# Controller usage
def show
  @user = User.find(params[:id]).decorate
end

# View usage
<%= @user.profile_link %>
<%= @user.avatar %>
<%= @user.status_badge %>
```

### SimpleDelegator Pattern (Without Gems)
```ruby
# app/decorators/user_decorator.rb
class UserDecorator < SimpleDelegator
  def initialize(user, view_context)
    super(user)
    @view_context = view_context
  end

  def full_name
    "#{first_name} #{last_name}"
  end

  def profile_link
    h.link_to full_name, h.user_path(self)
  end

  def formatted_created_at
    created_at.strftime("%B %d, %Y")
  end

  private

  def h
    @view_context
  end
end

# Controller
def show
  user = User.find(params[:id])
  @user = UserDecorator.new(user, view_context)
end
```

## Presenters (Expanded)

### View-Specific Presenter
```ruby
# app/presenters/dashboard_presenter.rb
class DashboardPresenter
  def initialize(user, view_context)
    @user = user
    @view_context = view_context
  end

  def welcome_message
    time_of_day = Time.current.hour < 12 ? 'Morning' : 'Afternoon'
    "Good #{time_of_day}, #{@user.first_name}!"
  end

  def recent_orders
    @recent_orders ||= @user.orders.recent.limit(5).map do |order|
      OrderPresenter.new(order, @view_context)
    end
  end

  def total_spent
    h.number_to_currency(@user.orders.sum(:total))
  end

  def activity_feed
    @user.activities.recent.limit(10).map do |activity|
      {
        icon: activity_icon(activity),
        text: activity_text(activity),
        time: h.time_ago_in_words(activity.created_at)
      }
    end
  end

  def stats
    {
      total_orders: @user.orders.count,
      total_spent: total_spent,
      favorite_category: @user.favorite_category&.name || 'N/A',
      member_since: @user.created_at.year
    }
  end

  private

  def h
    @view_context
  end

  def activity_icon(activity)
    case activity.action
    when 'order_placed' then 'shopping-cart'
    when 'review_posted' then 'star'
    when 'profile_updated' then 'user'
    else 'activity'
    end
  end

  def activity_text(activity)
    case activity.action
    when 'order_placed'
      "You placed order ##{activity.target_id}"
    when 'review_posted'
      "You reviewed #{activity.target.product.name}"
    when 'profile_updated'
      "You updated your profile"
    end
  end
end

# Controller
def dashboard
  @presenter = DashboardPresenter.new(current_user, view_context)
end

# View
<h1><%= @presenter.welcome_message %></h1>

<div class="stats">
  <% @presenter.stats.each do |key, value| %>
    <div class="stat">
      <span class="label"><%= key.to_s.humanize %></span>
      <span class="value"><%= value %></span>
    </div>
  <% end %>
</div>
```

### Collection Presenter
```ruby
# app/presenters/users_index_presenter.rb
class UsersIndexPresenter
  def initialize(users, view_context, filters: {})
    @users = users
    @view_context = view_context
    @filters = filters
  end

  def users
    @decorated_users ||= @users.map { |u| UserDecorator.new(u, h) }
  end

  def total_count
    @users.total_count
  end

  def pagination
    h.paginate(@users)
  end

  def active_filters
    @filters.select { |_, v| v.present? }
  end

  def filter_summary
    return "All users" if active_filters.empty?

    parts = []
    parts << "Role: #{@filters[:role]}" if @filters[:role]
    parts << "Status: #{@filters[:status]}" if @filters[:status]
    parts.join(', ')
  end

  def export_link
    h.link_to 'Export CSV', h.users_path(format: :csv, **@filters),
              class: 'btn btn-secondary'
  end

  private

  def h
    @view_context
  end
end
```

## Repository Pattern

### Basic Repository
```ruby
# app/repositories/user_repository.rb
class UserRepository
  class << self
    def find(id)
      User.find(id)
    end

    def find_by_email(email)
      User.find_by(email: email)
    end

    def active_users
      User.where(active: true).order(created_at: :desc)
    end

    def search(query)
      User.where('name ILIKE ? OR email ILIKE ?', "%#{query}%", "%#{query}%")
    end

    def with_recent_orders(days: 30)
      User.joins(:orders)
          .where('orders.created_at > ?', days.days.ago)
          .distinct
    end

    def create(attributes)
      User.create(attributes)
    end

    def update(user, attributes)
      user.update(attributes)
    end

    def destroy(user)
      user.destroy
    end
  end
end

# Service using repository
class UserRegistrationService
  def initialize(repository: UserRepository)
    @repository = repository
  end

  def call(attributes)
    user = @repository.create(attributes)

    if user.persisted?
      SendWelcomeEmailJob.perform_later(user)
      Result.success(user)
    else
      Result.failure(user.errors)
    end
  end
end
```

### Repository with Complex Queries
```ruby
# app/repositories/order_repository.rb
class OrderRepository
  class << self
    def pending_orders
      Order.where(status: 'pending').order(created_at: :asc)
    end

    def overdue_orders(threshold: 3.days)
      Order.where(status: 'pending')
           .where('created_at < ?', threshold.ago)
    end

    def user_orders(user, status: nil)
      scope = user.orders

      scope = scope.where(status: status) if status.present?
      scope.order(created_at: :desc)
    end

    def revenue_by_month(year: Time.current.year)
      Order.where(status: 'completed')
           .where('EXTRACT(YEAR FROM created_at) = ?', year)
           .group("DATE_TRUNC('month', created_at)")
           .sum(:total)
    end

    def top_customers(limit: 10)
      User.joins(:orders)
          .where(orders: { status: 'completed' })
          .group('users.id')
          .select('users.*, SUM(orders.total) as total_spent')
          .order('total_spent DESC')
          .limit(limit)
    end
  end
end
```

## PORO (Plain Old Ruby Object) Conventions

### Value Objects
```ruby
# app/models/money.rb
class Money
  include Comparable

  attr_reader :amount, :currency

  def initialize(amount, currency: 'USD')
    @amount = BigDecimal(amount.to_s)
    @currency = currency
  end

  def +(other)
    validate_currency!(other)
    Money.new(amount + other.amount, currency: currency)
  end

  def -(other)
    validate_currency!(other)
    Money.new(amount - other.amount, currency: currency)
  end

  def *(multiplier)
    Money.new(amount * multiplier, currency: currency)
  end

  def <=>(other)
    validate_currency!(other)
    amount <=> other.amount
  end

  def to_s
    format('%s%.2f', currency_symbol, amount)
  end

  def ==(other)
    amount == other.amount && currency == other.currency
  end

  private

  def validate_currency!(other)
    return if currency == other.currency

    raise ArgumentError, "Cannot operate on different currencies"
  end

  def currency_symbol
    case currency
    when 'USD' then '$'
    when 'EUR' then '€'
    when 'GBP' then '£'
    else currency
    end
  end
end

# Usage
price = Money.new(19.99)
tax = price * 0.08
total = price + tax # => $21.59
```

### Data Transfer Objects (DTOs)
```ruby
# app/models/user_dto.rb
class UserDTO
  attr_reader :id, :email, :full_name, :role

  def initialize(id:, email:, full_name:, role:)
    @id = id
    @email = email
    @full_name = full_name
    @role = role
  end

  def self.from_model(user)
    new(
      id: user.id,
      email: user.email,
      full_name: "#{user.first_name} #{user.last_name}",
      role: user.role
    )
  end

  def to_h
    {
      id: id,
      email: email,
      full_name: full_name,
      role: role
    }
  end
end

# Or using Ruby 3.2+ Data class
UserDTO = Data.define(:id, :email, :full_name, :role) do
  def self.from_model(user)
    new(
      id: user.id,
      email: user.email,
      full_name: "#{user.first_name} #{user.last_name}",
      role: user.role
    )
  end
end
```

### Result Objects
```ruby
# app/models/result.rb
class Result
  attr_reader :value, :error

  def initialize(success:, value: nil, error: nil)
    @success = success
    @value = value
    @error = error
  end

  def self.success(value = nil)
    new(success: true, value: value)
  end

  def self.failure(error)
    new(success: false, error: error)
  end

  def success?
    @success
  end

  def failure?
    !@success
  end

  def on_success
    yield value if success?
    self
  end

  def on_failure
    yield error if failure?
    self
  end
end

# Service using Result object
class CreateUserService
  def call(params)
    user = User.new(params)

    if user.save
      Result.success(user)
    else
      Result.failure(user.errors)
    end
  end
end

# Usage
result = CreateUserService.new.call(user_params)

result
  .on_success { |user| redirect_to user }
  .on_failure { |errors| render :new }
```

### Policy Objects
```ruby
# app/policies/post_visibility_policy.rb
class PostVisibilityPolicy
  def initialize(user, post)
    @user = user
    @post = post
  end

  def visible?
    return true if @post.published?
    return true if @user&.admin?
    return true if @post.user_id == @user&.id

    false
  end

  def editable?
    return true if @user&.admin?
    return true if @post.user_id == @user&.id

    false
  end
end

# Usage in controller
def show
  @post = Post.find(params[:id])
  policy = PostVisibilityPolicy.new(current_user, @post)

  unless policy.visible?
    redirect_to root_path, alert: 'Not authorized'
  end
end
```

## Quick Reference

### Before Writing Any Code
```bash
# Check existing patterns
ls app/services/
ls app/models/
grep -r 'class.*Service' app/ --include='*.rb' -l | head -10

# Check naming conventions
head -30 $(find app/services -name '*.rb' | head -1)

# Check dependencies
cat Gemfile | grep -v '^#' | grep -v '^$'
```

### Common File Locations
```
app/models/           - ActiveRecord models
app/controllers/      - Controllers
app/services/         - Service objects
app/components/       - ViewComponents
app/queries/          - Query objects
app/forms/            - Form objects
app/presenters/       - Presenters
app/decorators/       - Decorators
app/serializers/      - API serializers
app/jobs/             - Background jobs
app/mailers/          - Action Mailers
app/channels/         - Action Cable channels
app/repositories/     - Repository pattern objects
app/policies/         - Policy objects (business rules)
```
