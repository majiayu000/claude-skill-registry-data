---
name: rails
description: "Expert skill for Ruby on Rails web development across Rails 7.2, 8.0, and 8.1. Covers ActiveRecord (associations, scopes, callbacks, migrations, query interface), Action Pack (controllers, routing, strong parameters), Action View (templates, partials, helpers, form builders), Active Job, Action Cable, Turbo/Hotwire (Drive, Frames, Streams, Stimulus), Active Storage, Action Mailer, and testing. WHEN: \"Rails\", \"Ruby on Rails\", \"ActiveRecord\", \"Active Record\", \"Action Pack\", \"Action View\", \"Active Job\", \"Action Cable\", \"Action Mailer\", \"Turbo\", \"Hotwire\", \"Stimulus\", \"Turbo Frames\", \"Turbo Streams\", \"Active Storage\", \"has_many\", \"belongs_to\", \"has_one_attached\", \"before_action\", \"strong parameters\", \"form_with\", \"turbo_frame_tag\", \"turbo_stream\", \"broadcast_to\", \"perform_later\", \"deliver_later\", \"rails new\", \"rails generate\", \"Solid Queue\", \"Solid Cache\", \"Solid Cable\", \"Kamal\", \"Propshaft\", \"importmap\"."
license: MIT
---

# Ruby on Rails

This skill covers Ruby on Rails web development across Rails 7.2, 8.0 (current LTS-equivalent), and 8.1 (current stable). Rails is a full-stack, batteries-included web framework built on the Model-View-Controller pattern, emphasizing convention over configuration and developer happiness. It runs on Ruby 3.2+ and is served by Puma behind an optional reverse proxy.

## How to Approach Tasks

1. **Classify** the request:
   - **Architecture** -- Load `references/architecture.md` for ActiveRecord internals, Rack middleware stack, routing engine, Action Cable, Turbo/Hotwire, Active Storage, engines
   - **Best practices** -- Load `references/best-practices.md` for API mode, authentication, background jobs, deployment, performance, testing, security, common gems, project conventions
   - **Troubleshooting** -- Load `references/diagnostics.md` for common errors, N+1 detection, query debugging, Kamal deployment issues, Action Cable debugging
   - **Version-specific** -- Read the matching version reference (see Version-specific guidance below)

2. **Identify version** -- Determine the Rails version from the `Gemfile`, `Gemfile.lock`, `config/application.rb` (`config.load_defaults`), or explicit mention. Default to Rails 8.1 for new projects.

3. **Load context** -- Read the relevant reference file before answering.

4. **Analyze** -- Apply Rails-specific reasoning. Consider ActiveRecord query efficiency, callback lifecycle, middleware ordering, Turbo/Hotwire integration, and convention compliance.

5. **Recommend** -- Provide concrete Ruby code examples with explanations. Always qualify trade-offs.

6. **Verify** -- Suggest validation steps: `rails test`, `bundle exec rspec`, `rails routes`, `rails db:migrate:status`, checking N+1 queries.

## Core Architecture

### ActiveRecord (ORM)

ActiveRecord implements the Active Record pattern: each model class maps to a database table, each instance to a row. It sits atop Arel (the SQL AST) and exposes a chainable query interface.

```ruby
class Article < ApplicationRecord
  # Associations
  belongs_to :author, class_name: "User"
  has_many   :comments, dependent: :destroy
  has_many   :tags, through: :article_tags
  has_one_attached :cover_image

  # Scopes (chainable query fragments)
  scope :published, -> { where(published: true) }
  scope :recent,    -> { order(created_at: :desc) }
  scope :by_author, ->(user) { where(author: user) }

  # Validations
  validates :title, presence: true, length: { maximum: 255 }
  validates :status, inclusion: { in: %w[draft published archived] }

  # Callbacks
  before_validation :normalize_title
  after_commit :sync_to_search_index, on: [:create, :update]

  # Enum
  enum :status, { draft: 0, published: 1, archived: 2 }, prefix: true

  private

  def normalize_title
    self.title = title&.strip
  end
end
```

**Callback lifecycle (create):**
`before_validation` -> `after_validation` -> `before_save` -> `around_save` -> `before_create` -> `around_create` -> `after_create` -> `after_save` -> `after_commit`

Use `after_commit` for side effects (emails, jobs, external APIs) to ensure the transaction has committed.

**Query interface:**

```ruby
# Chainable -- returns ActiveRecord::Relation
Article.published.recent.by_author(user).limit(10)
Article.where(status: :published).where("created_at > ?", 1.week.ago)
Article.joins(:comments).where(comments: { approved: true })

# Eager loading (prevent N+1)
Article.includes(:author, :tags)       # preload or eager_load (Rails decides)
Article.eager_load(:comments)          # LEFT OUTER JOIN
Article.preload(:comments, :author)    # separate queries

# Strict loading (N+1 detection)
Article.strict_loading.first.comments  # raises StrictLoadingViolationError
```

### Action Pack (Controllers & Routing)

```ruby
class ArticlesController < ApplicationController
  before_action :authenticate_user!
  before_action :set_article, only: [:show, :edit, :update, :destroy]

  def index
    @articles = Article.published.includes(:author).page(params[:page])
  end

  def create
    @article = current_user.articles.build(article_params)
    if @article.save
      redirect_to @article, notice: "Article created."
    else
      render :new, status: :unprocessable_entity
    end
  end

  def destroy
    @article.destroy!
    redirect_to articles_path, status: :see_other  # 303 for Turbo
  end

  private

  def set_article
    @article = Article.find(params[:id])
  end

  def article_params
    params.require(:article).permit(:title, :body, :status, tag_ids: [])
  end
end
```

**Routing:**

```ruby
Rails.application.routes.draw do
  root "home#index"
  resources :articles do
    resources :comments, only: [:create, :destroy]
    member { post :publish }
    collection { get :search }
  end
  namespace :api do
    namespace :v1 do
      resources :users
    end
  end
end
```

### Action View (Templates & Partials)

```erb
<%# app/views/articles/_article.html.erb %>
<%# locals: (article:, compact: false) %>  <%# strict locals (8.0 default) %>
<article class="card">
  <h2><%= link_to article.title, article %></h2>
  <p class="byline">By <%= article.author.name %></p>
  <%= render article.comments unless compact %>
</article>
```

**form_with:**

```erb
<%= form_with model: @article do |f| %>
  <%= f.text_field :title, required: true %>
  <%= f.text_area :body %>
  <%= f.select :status, Article.statuses.keys.map { |s| [s.humanize, s] } %>
  <%= f.file_field :cover_image, direct_upload: true %>
  <%= f.submit %>
<% end %>
```

### Active Job

```ruby
class ProcessPaymentJob < ApplicationJob
  queue_as :critical
  retry_on Stripe::RateLimitError, wait: :polynomially_longer, attempts: 5
  discard_on ActiveJob::DeserializationError

  def perform(order_id)
    order = Order.find(order_id)
    PaymentService.new(order).process!
  end
end

# Enqueue
ProcessPaymentJob.perform_later(order.id)
ProcessPaymentJob.set(wait: 5.minutes).perform_later(order.id)
```

### Action Cable (WebSockets)

```ruby
class ChatChannel < ApplicationCable::Channel
  def subscribed
    room = Room.find(params[:room_id])
    stream_for room
  end

  def speak(data)
    room = Room.find(params[:room_id])
    room.messages.create!(content: data["message"], user: current_user)
  end
end
```

### Turbo/Hotwire

Hotwire (HTML Over the Wire) is Rails' default front-end paradigm from Rails 7+. It sends HTML instead of JSON.

**Turbo Drive** -- Intercepts link clicks and form submissions, replaces `<body>` only (SPA-like navigation without JavaScript).

**Turbo Frames** -- Scope navigation to a portion of the page:

```erb
<%= turbo_frame_tag "new-article" do %>
  <%= link_to "New Article", new_article_path %>
<% end %>
```

**Turbo Streams** -- Update multiple DOM elements simultaneously:

```ruby
# From model (broadcast over Action Cable)
class Message < ApplicationRecord
  after_create_commit  -> { broadcast_append_to room }
  after_update_commit  -> { broadcast_replace_to room }
  after_destroy_commit -> { broadcast_remove_to room }
end
```

```erb
<%# Subscribe in view %>
<%= turbo_stream_from @room %>
```

**Stimulus** -- Modest JavaScript framework connecting HTML attributes to controller classes:

```javascript
import { Controller } from "@hotwired/stimulus"
export default class extends Controller {
  static targets = ["input", "counter"]
  static values  = { max: { type: Number, default: 280 } }

  update() {
    const remaining = this.maxValue - this.inputTarget.value.length
    this.counterTarget.textContent = `${remaining} remaining`
  }
}
```

### Active Storage

```ruby
class User < ApplicationRecord
  has_one_attached  :avatar
  has_many_attached :documents
end

# Variants (image processing)
image_tag user.avatar.variant(resize_to_limit: [150, 150])

# Direct uploads (browser uploads directly to S3/GCS)
f.file_field :avatar, direct_upload: true
```

### Action Mailer

```ruby
class OrderMailer < ApplicationMailer
  def confirmation
    @order = params[:order]
    mail(to: @order.user.email, subject: "Order ##{@order.number} Confirmed")
  end
end

# Deliver
OrderMailer.with(order: @order).confirmation.deliver_later
```

### Testing

Rails ships with Minitest; RSpec is the most popular alternative.

```ruby
# Minitest
class ArticleTest < ActiveSupport::TestCase
  test "requires title" do
    article = Article.new(title: "")
    assert_not article.valid?
    assert_includes article.errors[:title], "can't be blank"
  end
end

# RSpec
RSpec.describe Article, type: :model do
  it { is_expected.to validate_presence_of(:title) }
  it { is_expected.to have_many(:comments).dependent(:destroy) }
end
```

## Version-specific guidance

Read the matching reference when the question involves features introduced in a specific Rails release:

| Version | Status | Reference | What's version-specific |
|---|---|---|---|
| Rails 7.2 | Security only (EOL Aug 2026) | `references/versions/7.2.md` | Dev containers, health check endpoint, YJIT default, Brakeman default, PWA support |
| Rails 8.0 | Security fixes (until Nov 2026) | `references/versions/8.0.md` | Solid trilogy (Queue/Cache/Cable), Kamal 2, authentication generator, Propshaft, Thruster, strict locals |
| Rails 8.1 | Current stable (Oct 2025) | `references/versions/8.1.md` | Active Job Continuations, structured event reporting, enhanced rate limiting, deprecated associations, local CI |

**For new projects:** Use Rails 8.1 with Ruby 3.4.

**Migration path:** Always upgrade one minor version at a time: 7.2 -> 8.0 -> 8.1. Fix all deprecation warnings before each upgrade.

## Ruby Version Requirements

| Rails | Minimum Ruby | Recommended |
|---|---|---|
| 7.2.x | 3.1.0 | 3.4.x |
| 8.0.x | 3.2.0 | 3.4.x |
| 8.1.x | 3.2.0 | 3.4.x |

## Key Patterns Quick Reference

| Pattern | When to Use |
|---|---|
| Service objects | Complex business logic spanning multiple models |
| Form objects | Multi-model forms, complex validation |
| Query objects | Reusable complex ActiveRecord queries |
| Concerns | Cross-cutting model/controller behavior (use sparingly) |
| Presenters | View-specific formatting logic |
| ViewComponent | Testable, encapsulated view objects (gem by GitHub) |

## Cross-Version Feature Matrix

| Feature | 7.2 | 8.0 | 8.1 |
|---|---|---|---|
| Turbo/Hotwire | Yes | Yes | Yes |
| Solid Queue | Gem only | Default | Default |
| Solid Cache | Gem only | Default | Default |
| Solid Cable | Gem only | Default | Default |
| Kamal | Manual | Default | Default + registry-free |
| Propshaft | Opt-in | Default | Default |
| Authentication generator | No | Yes | Yes |
| Active Job Continuations | No | No | Yes |
| Strict locals (default) | Opt-in | Default | Default |
| YJIT auto-enabled | Yes (3.3+) | Yes | Yes |

## Reference Files

Load these for deep knowledge on specific topics:

- `references/architecture.md` -- ActiveRecord internals (associations, query interface, Arel, callbacks lifecycle), Rack middleware stack, routing engine, Action Cable, Turbo/Hotwire (Drive, Frames, Streams, Stimulus), Active Storage, engines. **Load when:** architecture questions, ORM patterns, middleware customization, WebSocket setup, Turbo integration.
- `references/best-practices.md` -- API mode (jbuilder, Blueprinter, Alba), authentication (Devise, Rails 8 generator, JWT), background jobs (Solid Queue vs Sidekiq), deployment (Kamal 2, Docker), performance (N+1/Bullet, caching, counter_cache), testing (RSpec, FactoryBot, system tests), security, common gems, project conventions. **Load when:** "how should I", best approach, gem selection, deployment, performance optimization, testing strategy.
- `references/diagnostics.md` -- Common errors (RecordNotFound, migration issues, routing errors, asset pipeline), N+1 detection, query debugging, Kamal deployment troubleshooting, Action Cable debugging. **Load when:** troubleshooting errors, debugging queries, deployment failures, WebSocket issues.
