---
name: rails-backend-guidelines
description: Rails backend development guidelines for building maintainable Ruby on Rails applications. Use when creating controllers, models, services, concerns, routes, or working with ActiveRecord, background jobs, Action Cable, validations, and Rails conventions. Covers MVC architecture, service objects, RESTful routing, database patterns, and Rails best practices.
---

# Rails Backend Development Guidelines

## Purpose

Establish consistency and best practices for Rails backend development using modern Rails patterns, conventions, and community standards.

## When to Use This Skill

Automatically activates when working on:

- Creating or modifying controllers and actions
- Building models and ActiveRecord queries
- Implementing service objects
- Database migrations and schema changes
- Background jobs with Solid Queue or Active Job
- Action Cable (WebSocket) integration
- Rails concerns and modules
- RESTful routing and API endpoints
- Input validation and strong parameters
- Authentication and authorization

---

## Quick Reference

### New Feature Checklist

- [ ] **Route**: Define RESTful route in `config/routes.rb`
- [ ] **Controller**: Create skinny controller with strong params
- [ ] **Model**: Add validations, associations, scopes
- [ ] **Service**: Extract complex business logic (if needed)
- [ ] **Migration**: Create database schema changes
- [ ] **Tests**: Write model, controller, and integration tests
- [ ] **Authorization**: Implement proper permissions

### New Model Checklist

- [ ] Validations for data integrity
- [ ] Associations (has_many, belongs_to, has_one, etc.)
- [ ] Scopes for common queries
- [ ] Callbacks (use sparingly, prefer service objects)
- [ ] Custom methods for business logic
- [ ] Database indexes for foreign keys and query performance
- [ ] Tests for validations, associations, and methods

---

## Core Principles

### 1. Follow Rails Conventions (Convention over Configuration)

✅ **DO**: Use Rails naming conventions

```ruby
# Model name: Post (singular, CamelCase)
class Post < ApplicationRecord
end

# Table name: posts (plural, snake_case)
# Controller: PostsController (plural, CamelCase + Controller)
# Routes: resources :posts
```

❌ **DON'T**: Fight Rails conventions

```ruby
# Don't do this:
class PostRecord < ApplicationRecord  # Wrong base class name
  self.table_name = 'my_posts'        # Unnecessary customization
end
```

### 2. RESTful Design

✅ **DO**: Use standard RESTful actions

```ruby
# config/routes.rb
resources :posts do
  member do
    post :publish  # POST /posts/:id/publish
  end
  collection do
    get :archived  # GET /posts/archived
  end
end

# Only use: index, show, new, create, edit, update, destroy
# + reasonable custom actions like: publish, archive, restore
```

❌ **DON'T**: Create non-RESTful actions

```ruby
# Don't do this:
get '/posts/get_all_posts'           # Use index
post '/posts/make_new_post'          # Use create
get '/posts/get_post/:id'            # Use show
```

### 3. Skinny Controllers, Smart Models/Services

✅ **DO**: Keep controllers thin

```ruby
class PostsController < ApplicationController
  def create
    @post = current_user.posts.build(post_params)

    if @post.save
      redirect_to @post, notice: 'Post created successfully.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def post_params
    params.require(:post).permit(:title, :body, :published)
  end
end
```

❌ **DON'T**: Put business logic in controllers

```ruby
# Don't do this:
def create
  @post = Post.new(post_params)
  @post.user_id = current_user.id
  @post.slug = @post.title.parameterize
  @post.word_count = @post.body.split.size

  if @post.save
    # Send notification
    UserMailer.new_post_email(@post).deliver_later
    # Update counter cache
    current_user.increment!(:posts_count)
    # Log activity
    ActivityLog.create(user: current_user, action: 'created_post')
    redirect_to @post
  else
    render :new
  end
end
```

### 4. Always Use Strong Parameters

✅ **DO**: Whitelist permitted attributes

```ruby
def post_params
  params.require(:post).permit(:title, :body, :published, tag_ids: [])
end

# For nested attributes:
def post_params
  params.require(:post).permit(
    :title, :body,
    comments_attributes: [:id, :content, :_destroy]
  )
end
```

❌ **DON'T**: Use .permit! or skip parameter filtering

```ruby
# NEVER do this - security vulnerability!
def post_params
  params[:post]        # No filtering
  params.permit!       # Permits everything - dangerous!
end
```

---

## Architecture Patterns

### MVC Flow

```
HTTP Request
    ↓
Routes (config/routes.rb)
    ↓
Controller (thin layer, handles HTTP)
    ↓
Model / Service Object (business logic)
    ↓
ActiveRecord (database operations)
    ↓
PostgreSQL / MySQL / SQLite
    ↓
Response (JSON / HTML / Turbo Stream)
```

### When to Use Service Objects

Use service objects for:

- Complex multi-step operations
- Business logic that spans multiple models
- External API integrations
- Operations that don't fit naturally in a model

```ruby
# app/services/post_publisher.rb
class PostPublisher
  def initialize(post, user)
    @post = post
    @user = user
  end

  def call
    ActiveRecord::Base.transaction do
      @post.update!(published: true, published_at: Time.current)
      notify_subscribers
      log_publication
    end
    true
  rescue ActiveRecord::RecordInvalid => e
    false
  end

  private

  def notify_subscribers
    @post.subscribers.find_each do |subscriber|
      PostMailer.published_notification(@post, subscriber).deliver_later
    end
  end

  def log_publication
    ActivityLog.create!(user: @user, action: 'published_post', target: @post)
  end
end

# Usage in controller:
def publish
  if PostPublisher.new(@post, current_user).call
    redirect_to @post, notice: 'Post published!'
  else
    redirect_to @post, alert: 'Could not publish post.'
  end
end
```

### Concerns vs Service Objects

**Concerns** (for shared behavior across models/controllers):

```ruby
# app/models/concerns/publishable.rb
module Publishable
  extend ActiveSupport::Concern

  included do
    scope :published, -> { where(published: true) }
    scope :draft, -> { where(published: false) }
  end

  def publish!
    update!(published: true, published_at: Time.current)
  end
end

# Usage:
class Post < ApplicationRecord
  include Publishable
end
```

**Service Objects** (for complex operations):

```ruby
# Use when operation involves multiple models, external APIs,
# or complex business logic that doesn't belong in a model
```

---

## Controllers

### Standard RESTful Controller Pattern

```ruby
class PostsController < ApplicationController
  before_action :authenticate_user!, except: [:index, :show]
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authorize_post, only: [:edit, :update, :destroy]

  # GET /posts
  def index
    @posts = Post.includes(:user).published.page(params[:page])
  end

  # GET /posts/:id
  def show
    @comments = @post.comments.includes(:user).recent
  end

  # GET /posts/new
  def new
    @post = current_user.posts.build
  end

  # POST /posts
  def create
    @post = current_user.posts.build(post_params)

    if @post.save
      redirect_to @post, notice: 'Post was successfully created.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  # GET /posts/:id/edit
  def edit
  end

  # PATCH/PUT /posts/:id
  def update
    if @post.update(post_params)
      redirect_to @post, notice: 'Post was successfully updated.'
    else
      render :edit, status: :unprocessable_entity
    end
  end

  # DELETE /posts/:id
  def destroy
    @post.destroy
    redirect_to posts_url, notice: 'Post was successfully destroyed.'
  end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def authorize_post
    redirect_to root_path, alert: 'Not authorized' unless @post.user == current_user
  end

  def post_params
    params.require(:post).permit(:title, :body, :published)
  end
end
```

### API Controller Pattern (JSON)

```ruby
class Api::V1::PostsController < ApplicationController
  skip_before_action :verify_authenticity_token
  before_action :authenticate_api_user!
  before_action :set_post, only: [:show, :update, :destroy]

  # GET /api/v1/posts
  def index
    @posts = Post.published.includes(:user)
    render json: @posts, include: :user
  end

  # GET /api/v1/posts/:id
  def show
    render json: @post, include: [:user, :comments]
  end

  # POST /api/v1/posts
  def create
    @post = current_user.posts.build(post_params)

    if @post.save
      render json: @post, status: :created, location: api_v1_post_url(@post)
    else
      render json: { errors: @post.errors }, status: :unprocessable_entity
    end
  end

  # PATCH/PUT /api/v1/posts/:id
  def update
    if @post.update(post_params)
      render json: @post
    else
      render json: { errors: @post.errors }, status: :unprocessable_entity
    end
  end

  # DELETE /api/v1/posts/:id
  def destroy
    @post.destroy
    head :no_content
  end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def post_params
    params.require(:post).permit(:title, :body, :published)
  end
end
```

---

## Models

### Standard Model Pattern

```ruby
class Post < ApplicationRecord
  # Concerns (first)
  include Publishable

  # Associations (second)
  belongs_to :user
  has_many :comments, dependent: :destroy
  has_many :tags, through: :post_tags
  has_one_attached :cover_image

  # Validations (third)
  validates :title, presence: true, length: { maximum: 200 }
  validates :body, presence: true
  validates :user, presence: true

  # Scopes (fourth)
  scope :published, -> { where(published: true) }
  scope :recent, -> { order(created_at: :desc) }
  scope :by_user, ->(user) { where(user: user) }

  # Callbacks (use sparingly - prefer service objects)
  before_save :generate_slug, if: :title_changed?
  after_create_commit :notify_followers

  # Class methods
  def self.search(query)
    where('title ILIKE ? OR body ILIKE ?', "%#{query}%", "%#{query}%")
  end

  # Instance methods
  def published?
    published && published_at.present?
  end

  def word_count
    body.split.size
  end

  private

  def generate_slug
    self.slug = title.parameterize
  end

  def notify_followers
    PostNotificationJob.perform_later(id)
  end
end
```

### Associations

```ruby
# One-to-many
class User < ApplicationRecord
  has_many :posts, dependent: :destroy
end

class Post < ApplicationRecord
  belongs_to :user
end

# Many-to-many (through join model - preferred)
class Post < ApplicationRecord
  has_many :post_tags
  has_many :tags, through: :post_tags
end

class Tag < ApplicationRecord
  has_many :post_tags
  has_many :posts, through: :post_tags
end

class PostTag < ApplicationRecord
  belongs_to :post
  belongs_to :tag
end

# One-to-one
class User < ApplicationRecord
  has_one :profile, dependent: :destroy
end

class Profile < ApplicationRecord
  belongs_to :user
end

# Polymorphic associations
class Comment < ApplicationRecord
  belongs_to :commentable, polymorphic: true
end

class Post < ApplicationRecord
  has_many :comments, as: :commentable
end

class Video < ApplicationRecord
  has_many :comments, as: :commentable
end
```

---

## Routing

### RESTful Routes (Preferred)

```ruby
# config/routes.rb
Rails.application.routes.draw do
  # Standard resourceful routes
  resources :posts
  # Generates: index, show, new, create, edit, update, destroy

  # Limit actions
  resources :posts, only: [:index, :show]
  resources :posts, except: [:destroy]

  # Nested resources (keep shallow)
  resources :posts do
    resources :comments, shallow: true
  end
  # Generates:
  # /posts/:post_id/comments (index, create)
  # /comments/:id (show, edit, update, destroy)

  # Custom member/collection actions
  resources :posts do
    member do
      post :publish      # POST /posts/:id/publish
      delete :unpublish  # DELETE /posts/:id/unpublish
    end

    collection do
      get :archived      # GET /posts/archived
      get :search        # GET /posts/search
    end
  end

  # API routes
  namespace :api do
    namespace :v1 do
      resources :posts, only: [:index, :show, :create, :update, :destroy]
    end
  end

  # Root route
  root 'posts#index'
end
```

---

## Database & Migrations

### Migration Best Practices

```ruby
# Good migration - with index and null constraint
class CreatePosts < ActiveRecord::Migration[7.1]
  def change
    create_table :posts do |t|
      t.references :user, null: false, foreign_key: true, index: true
      t.string :title, null: false
      t.text :body
      t.boolean :published, default: false, null: false
      t.datetime :published_at
      t.string :slug, index: { unique: true }

      t.timestamps
    end

    add_index :posts, [:user_id, :created_at]
    add_index :posts, :published
  end
end

# Adding columns
class AddViewsCountToPosts < ActiveRecord::Migration[7.1]
  def change
    add_column :posts, :views_count, :integer, default: 0, null: false
  end
end

# Removing columns (reversible)
class RemoveBodyFromPosts < ActiveRecord::Migration[7.1]
  def change
    remove_column :posts, :body, :text
  end
end

# Data migration (separate from schema changes)
class BackfillPostSlugs < ActiveRecord::Migration[7.1]
  def up
    Post.where(slug: nil).find_each do |post|
      post.update_column(:slug, post.title.parameterize)
    end
  end

  def down
    # Optionally define rollback
  end
end
```

---

## Testing

### Model Tests (RSpec)

```ruby
# spec/models/post_spec.rb
require 'rails_helper'

RSpec.describe Post, type: :model do
  describe 'associations' do
    it { should belong_to(:user) }
    it { should have_many(:comments) }
  end

  describe 'validations' do
    it { should validate_presence_of(:title) }
    it { should validate_presence_of(:body) }
    it { should validate_length_of(:title).is_at_most(200) }
  end

  describe 'scopes' do
    it 'returns published posts' do
      published = create(:post, published: true)
      draft = create(:post, published: false)

      expect(Post.published).to include(published)
      expect(Post.published).not_to include(draft)
    end
  end

  describe '#word_count' do
    it 'returns the number of words in body' do
      post = build(:post, body: 'This is a test post')
      expect(post.word_count).to eq(5)
    end
  end
end
```

### Controller Tests (RSpec)

```ruby
# spec/controllers/posts_controller_spec.rb
require 'rails_helper'

RSpec.describe PostsController, type: :controller do
  let(:user) { create(:user) }
  let(:post) { create(:post, user: user) }

  describe 'GET #index' do
    it 'returns a success response' do
      get :index
      expect(response).to be_successful
    end
  end

  describe 'POST #create' do
    context 'with valid params' do
      it 'creates a new Post' do
        sign_in user
        expect {
          post :create, params: { post: attributes_for(:post) }
        }.to change(Post, :count).by(1)
      end
    end

    context 'with invalid params' do
      it 'does not create a new Post' do
        sign_in user
        expect {
          post :create, params: { post: { title: '' } }
        }.not_to change(Post, :count)
      end
    end
  end
end
```

---

## Resources

For detailed information on specific topics, see:

- [Routing & Controllers](resources/routing-and-controllers.md) - RESTful patterns, strong params, filters
- [Database Patterns](resources/database-patterns.md) - Schema design, indexes, migrations, ActiveRecord
- [Services & Repositories](resources/services-and-repositories.md) - When and how to extract logic
- [Testing Guide](resources/testing-guide.md) - Rails testing with Minitest, fixtures, controller tests
- [Webhook Implementation](resources/webhook-implementation.md) - GitHub webhooks, PR-to-issue routing, structured context
- [Async & Errors](resources/async-and-errors.md) - Background jobs, error handling
- [Configuration](resources/configuration.md) - Environment configuration, secrets
- [Complete Examples](resources/complete-examples.md) - Full implementation examples

---

## Common Patterns This Project Uses

Review your existing codebase to understand project-specific patterns:

- `app/models/user.rb` - Authentication and user model patterns
- `app/controllers/application_controller.rb` - Base controller setup
- Existing controllers in `app/controllers/` - Follow established patterns
- `db/schema.rb` - Database structure and conventions used

---

**Last Updated**: 2025-01-12
