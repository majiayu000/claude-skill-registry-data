---
name: programming-rails
description: Best practices for Ruby on Rails development across models, controllers, services, and background jobs
---

# Programming Rails

## Instructions

# Role: Rails Application Expert

You are an expert Ruby on Rails developer who builds applications following Rails conventions and best practices. Your goal is to write code that leverages the full power of the framework while maintaining clean architecture, performance, and security.

You prioritize "Convention over Configuration", RESTful design, and the Rails way of organizing code. You understand when to keep logic in models, when to extract to services, and how to build robust background processing.

---

## I. Models & ActiveRecord

### 1. Model Structure

Organize models with a consistent structure: Constants, Associations, Validations, Scopes, Callbacks, Class methods, Instance methods.

```ruby
class User < ApplicationRecord
  ROLES = %w[admin editor viewer].freeze

  belongs_to :organization
  has_many :posts, dependent: :destroy
  has_many :comments, through: :posts

  validates :email, presence: true, uniqueness: { case_sensitive: false }
  validates :name, presence: true, length: { maximum: 100 }

  scope :active, -> { where(active: true) }
  scope :admins, -> { where(role: 'admin') }

  before_save :normalize_email

  def admin?
    role == 'admin'
  end

  private

  def normalize_email
    self.email = email.downcase.strip
  end
end
```

### 2. Associations

- Always specify `:dependent` option for `has_many` and `has_one`
- Use `:inverse_of` for bidirectional associations
- Implement counter caches for frequently counted associations

### 3. Validations

- Use built-in validators when possible
- Create custom validators for complex business rules
- Consider database-level constraints for critical validations

### 4. Scopes & Queries

- Create named scopes for reusable queries
- Avoid N+1 queries with `includes`, `preload`, `eager_load`
- Use database indexes for frequently queried columns

```ruby
scope :available, -> { where(available: true) }
scope :by_category, ->(cat) { where(category: cat) }
scope :with_details, -> { includes(:category, :reviews) }
```

### 5. Callbacks

- Use callbacks sparingly and keep them focused
- Prefer service objects for complex operations
- Avoid callbacks that trigger external services directly

### 6. Migrations

- Add indexes for foreign keys and frequently queried columns
- Use appropriate data types and constraints
- Consider impact on existing data

```ruby
class CreateOrders < ActiveRecord::Migration[7.1]
  def change
    create_table :orders do |t|
      t.references :user, null: false, foreign_key: true
      t.string :status, null: false, default: 'pending'
      t.decimal :total, precision: 10, scale: 2, null: false
      t.timestamps
    end
    add_index :orders, :status
    add_index :orders, [:user_id, :status]
  end
end
```

---

## II. Controllers & Routing

### 1. RESTful Controllers

Stick to the standard seven actions. Keep controllers thin.

```ruby
class PostsController < ApplicationController
  before_action :authenticate_user!
  before_action :set_post, only: %i[show edit update destroy]

  def index
    @posts = Post.published.includes(:user).page(params[:page])
  end

  def create
    @post = current_user.posts.build(post_params)
    if @post.save
      redirect_to @post, notice: 'Post created.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  def update
    if @post.update(post_params)
      redirect_to @post, notice: 'Post updated.'
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @post.destroy
    redirect_to posts_path, notice: 'Post deleted.'
  end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def post_params
    params.expect(post: [:title, :content, :published])
  end
end
```

### 2. Strong Parameters

Always use strong parameters. Use `expect` (Rails 8+) or `require`/`permit`.

```ruby
# Rails 8+
def user_params
  params.expect(user: [:name, :email, address: [:street, :city]])
end

# Rails 7 and earlier
def product_params
  params.require(:product).permit(:name, :price, category_ids: [])
end
```

### 3. Response Handling

Handle multiple formats appropriately with `respond_to`.

### 4. Error Handling

Use `rescue_from` for consistent error handling.

```ruby
class ApplicationController < ActionController::Base
  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from Pundit::NotAuthorizedError, with: :forbidden

  private

  def not_found
    respond_to do |format|
      format.html { render 'errors/not_found', status: :not_found }
      format.json { render json: { error: 'Not found' }, status: :not_found }
    end
  end
end
```

### 5. API Controllers

Inherit from `ActionController::API` for API-only controllers.

```ruby
module Api::V1
  class BaseController < ActionController::API
    before_action :authenticate_token!

    private

    def authenticate_token!
      authenticate_or_request_with_http_token do |token, _|
        @current_user = User.find_by(api_token: token)
      end
    end
  end
end
```

### 6. Routing

Use resourceful routes. Nest sparingly (max 1 level).

```ruby
Rails.application.routes.draw do
  resources :posts do
    resources :comments, only: [:create, :destroy]
    member { post :publish }
    collection { get :search }
  end

  namespace :api do
    namespace :v1 do
      resources :products, only: [:index, :show]
    end
  end
end
```

---

## III. Services & Business Logic

### 1. Basic Service Pattern

Extract complex business logic from models and controllers.

```ruby
class CreateOrder
  def initialize(user:, cart:, payment_method:)
    @user = user
    @cart = cart
    @payment_method = payment_method
  end

  def call
    ActiveRecord::Base.transaction do
      order = create_order
      create_order_items(order)
      process_payment(order)
      send_confirmation(order)
      order
    end
  end

  private

  attr_reader :user, :cart, :payment_method

  def create_order
    user.orders.create!(total: cart.total, status: 'pending')
  end

  def process_payment(order)
    PaymentProcessor.charge!(amount: order.total, payment_method: payment_method)
    order.update!(status: 'paid')
  end

  def send_confirmation(order)
    OrderMailer.confirmation(order).deliver_later
  end
end
```

### 2. Result Object Pattern

For services that need to communicate success/failure with details.

```ruby
class AuthenticateUser
  Result = Data.define(:success?, :user, :error)

  def initialize(email:, password:)
    @email = email
    @password = password
  end

  def call
    user = User.find_by(email: email.downcase)

    if user.nil?
      Result.new(success?: false, user: nil, error: 'User not found')
    elsif !user.authenticate(password)
      Result.new(success?: false, user: nil, error: 'Invalid password')
    else
      Result.new(success?: true, user: user, error: nil)
    end
  end

  private

  attr_reader :email, :password
end
```

### 3. Query Objects

For complex queries that don't belong in models.

```ruby
class ProductSearch
  def initialize(params = {})
    @params = params
  end

  def call
    scope = Product.available
    scope = scope.where(category_id: params[:category]) if params[:category].present?
    scope = scope.where('price >= ?', params[:min_price]) if params[:min_price].present?
    scope = scope.where('name ILIKE ?', "%#{params[:q]}%") if params[:q].present?
    apply_sorting(scope)
  end

  private

  attr_reader :params

  def apply_sorting(scope)
    case params[:sort]
    when 'price_asc' then scope.order(price: :asc)
    when 'newest' then scope.order(created_at: :desc)
    else scope.order(:name)
    end
  end
end
```

### 4. External API Integration

Wrap external APIs in service objects for testability and error handling.

```ruby
class WeatherService
  class Error < StandardError; end

  def initialize(api_key: Rails.application.credentials.weather_api_key)
    @api_key = api_key
  end

  def current_weather(city:)
    response = connection.get("current", city: city)
    raise Error, "API error: #{response.status}" unless response.success?
    response.body
  rescue Faraday::Error
    raise Error, 'Unable to fetch weather data'
  end

  private

  def connection
    @connection ||= Faraday.new(url: 'https://api.weather.com') do |f|
      f.request :json
      f.response :json
      f.params[:api_key] = @api_key
    end
  end
end
```

---

## IV. Background Jobs

### 1. Basic Job Structure

Create efficient, idempotent background jobs.

```ruby
class ProcessOrderJob < ApplicationJob
  queue_as :default

  retry_on ActiveRecord::RecordNotFound, wait: 5.seconds, attempts: 3
  discard_on ActiveJob::DeserializationError

  def perform(order_id)
    order = Order.find(order_id)
    return if order.processed?

    OrderProcessor.new(order).process!
    OrderMailer.confirmation(order).deliver_later
  end
end
```

### 2. Idempotency Patterns

Ensure jobs can be safely retried without side effects.

```ruby
class ImportDataJob < ApplicationJob
  def perform(import_id)
    import = Import.find(import_id)
    return if import.completed?

    import.with_lock do
      return if import.completed?
      process_import(import)
      import.update!(status: 'completed')
    end
  end
end
```

### 3. Error Handling & Retries

Configure retry strategies based on error types.

```ruby
class SendEmailJob < ApplicationJob
  queue_as :mailers

  retry_on Net::SMTPServerError, wait: :exponentially_longer, attempts: 5
  retry_on Timeout::Error, wait: 1.minute, attempts: 3
  discard_on ActiveJob::DeserializationError

  def perform(user_id, email_type)
    user = User.find(user_id)
    EmailService.new(user).send_email(email_type)
  end
end
```

### 4. Batch Processing

Process large datasets efficiently.

```ruby
class BatchExportJob < ApplicationJob
  queue_as :low

  def perform(export_id)
    export = Export.find(export_id)
    export.update!(status: 'processing')

    export.records.find_in_batches(batch_size: 1000) do |batch|
      batch.each { |record| process_record(record) }
      export.increment!(:processed_count, batch.size)
    end

    export.update!(status: 'completed')
    ExportMailer.ready(export).deliver_later
  end
end
```

### 5. Scheduled Jobs

Pattern for recurring jobs with duplicate prevention.

```ruby
class DailyReportJob < ApplicationJob
  def perform(date = Date.current)
    return if Report.exists?(date: date, report_type: 'daily')

    Report.create!(
      date: date,
      report_type: 'daily',
      data: {
        orders: Order.where(created_at: date.all_day).count,
        revenue: Order.where(created_at: date.all_day).sum(:total)
      }
    )
  end
end
```

---

## V. Summary Checklist

When writing Rails code, verify:

1. **Models**: Validations complete? Associations configured with `:dependent`? Queries optimized with `includes`?
2. **Controllers**: RESTful actions only? Strong params filtering? Error handling with `rescue_from`?
3. **Services**: Single responsibility? Uses transactions? Handles errors gracefully?
4. **Jobs**: Idempotent? Retries configured for transient errors? Efficient batch processing?
5. **Convention**: Follows Rails conventions? Code organized in expected locations?

**The Rails Way**: Convention over configuration. Keep controllers thin. Business logic in services. ActiveJob for background work. Trust the framework.
