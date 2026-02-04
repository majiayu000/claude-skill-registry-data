---
name: phoenix-context-creator
description: Create complete Phoenix contexts following best practices including bounded contexts, proper API design, and comprehensive testing. Use when designing new features or refactoring code into contexts.
allowed-tools: Bash, Read, Edit, Write
---

# Phoenix Context Creator

This skill guides the creation of well-designed Phoenix contexts following bounded context principles and Phoenix best practices.

## When to Use

- Creating new business domains
- Organizing related functionality
- Refactoring code into contexts
- Designing API boundaries
- Building feature modules

## What is a Context?

A context is a module that groups related functionality and provides a public API for that domain. Contexts enforce boundaries between different parts of your application.

**Examples:**
- `Accounts` - User management, authentication
- `Catalog` - Products, categories, inventory
- `Sales` - Orders, shopping cart, checkout
- `CMS` - Blog posts, pages, comments
- `Notifications` - Emails, SMS, push notifications

## Context Design Principles

### 1. Bounded Context
Each context should have clear responsibilities:

```elixir
# Good: Focused contexts
Accounts.create_user()
Catalog.list_products()
Sales.place_order()

# Bad: Mixed responsibilities
Users.create_user()
Users.list_products()  # Products don't belong here
Users.send_email()     # Email sending doesn't belong here
```

### 2. Public API Only
Contexts expose intentional APIs, hide implementation:

```elixir
# Good: Clear, intention-revealing API
defmodule MyApp.Accounts do
  def list_users, do: Repo.all(User)
  def get_user!(id), do: Repo.get!(User, id)
  def create_user(attrs), do: %User{} |> User.changeset(attrs) |> Repo.insert()
end

# Bad: Exposing internal details
defmodule MyApp.Accounts do
  # Don't expose User schema directly
  def user_schema, do: User

  # Don't expose changesets
  def user_changeset(attrs), do: User.changeset(%User{}, attrs)
end
```

### 3. No Cross-Context Dependencies
Contexts should not directly reference other contexts' schemas:

```elixir
# Bad: Post directly references User schema
defmodule Blog.Post do
  schema "posts" do
    belongs_to :user, Accounts.User  # Direct schema reference
  end
end

# Good: Use IDs to reference across contexts
defmodule Blog.Post do
  schema "posts" do
    field :user_id, :id  # Just store the ID
  end
end

# Then in Blog context, delegate user lookups to Accounts
defmodule Blog do
  def get_post_with_author!(id) do
    post = get_post!(id)
    author = Accounts.get_user!(post.user_id)
    %{post | author: author}
  end
end
```

## Creating a New Context

### Step 1: Plan the Domain

**Questions to answer:**
1. What is the primary responsibility?
2. What are the main entities?
3. What operations will be needed?
4. How does it interact with other contexts?

**Example: Building a Blog**
- Primary responsibility: Content management
- Entities: Post, Comment, Tag
- Operations: CRUD posts, publish/unpublish, add comments
- Interactions: Needs user data from Accounts context

### Step 2: Generate the Context

```bash
# Generate context with primary schema
mix phx.gen.context Blog Post posts \
  title:string \
  body:text \
  published:boolean \
  user_id:references:users \
  slug:string:unique
```

Generates:
- Context: `lib/my_app/blog.ex`
- Schema: `lib/my_app/blog/post.ex`
- Migration: `priv/repo/migrations/*_create_posts.exs`
- Tests: `test/my_app/blog_test.exs`

### Step 3: Design the Public API

**Start with CRUD:**
```elixir
defmodule MyApp.Blog do
  alias MyApp.Blog.Post

  # List operations
  def list_posts
  def list_published_posts

  # Get operations
  def get_post!(id)
  def get_post_by_slug(slug)

  # Create/Update/Delete
  def create_post(attrs)
  def update_post(post, attrs)
  def delete_post(post)

  # Domain-specific operations
  def publish_post(post)
  def unpublish_post(post)
  def increment_view_count(post)
end
```

**Add business logic:**
```elixir
def publish_post(%Post{} = post) do
  post
  |> Post.publish_changeset()
  |> Repo.update()
end

def list_posts_by_user(user_id) do
  Post
  |> where(user_id: ^user_id)
  |> order_by([desc: :inserted_at])
  |> Repo.all()
end
```

### Step 4: Enhance the Schema

```elixir
defmodule MyApp.Blog.Post do
  use Ecto.Schema
  import Ecto.Changeset

  schema "posts" do
    field :title, :string
    field :body, :text
    field :published, :boolean, default: false
    field :slug, :string
    field :view_count, :integer, default: 0
    field :user_id, :id

    timestamps()
  end

  # Creation changeset
  def changeset(post, attrs) do
    post
    |> cast(attrs, [:title, :body, :user_id])
    |> validate_required([:title, :body, :user_id])
    |> validate_length(:title, min: 3, max: 100)
    |> generate_slug()
    |> unique_constraint(:slug)
  end

  # Publishing changeset
  def publish_changeset(post) do
    change(post, published: true, published_at: DateTime.utc_now())
  end

  defp generate_slug(changeset) do
    case get_change(changeset, :title) do
      nil -> changeset
      title -> put_change(changeset, :slug, Slug.slugify(title))
    end
  end
end
```

### Step 5: Add Additional Schemas

```bash
# Add comments to blog context
mix phx.gen.context Blog Comment comments \
  body:text \
  post_id:references:posts \
  user_id:references:users \
  --merge-with-existing-context
```

### Step 6: Write Comprehensive Tests

```elixir
defmodule MyApp.BlogTest do
  use MyApp.DataCase

  alias MyApp.Blog

  describe "posts" do
    test "list_posts/0 returns all posts" do
      post = fixture(:post)
      assert Blog.list_posts() == [post]
    end

    test "get_post!/1 returns the post with given id" do
      post = fixture(:post)
      assert Blog.get_post!(post.id) == post
    end

    test "create_post/1 with valid data creates a post" do
      attrs = %{title: "Title", body: "Body", user_id: 1}
      assert {:ok, %Post{} = post} = Blog.create_post(attrs)
      assert post.title == "Title"
    end

    test "publish_post/1 marks post as published" do
      post = fixture(:post)
      assert {:ok, %Post{} = published} = Blog.publish_post(post)
      assert published.published == true
    end
  end
end
```

## Context Interaction Patterns

### Pattern 1: ID References (Recommended)
```elixir
# Blog context references users by ID only
defmodule MyApp.Blog do
  def create_post(user_id, attrs) do
    attrs
    |> Map.put(:user_id, user_id)
    |> create_post()
  end

  # When you need user data, delegate to Accounts
  def get_post_with_author(post_id) do
    post = get_post!(post_id)
    author = MyApp.Accounts.get_user!(post.user_id)
    Map.put(post, :author, author)
  end
end
```

### Pattern 2: Data Transfer Objects
```elixir
# Blog context accepts struct from Accounts
defmodule MyApp.Blog do
  def create_post_for_user(%Accounts.User{id: user_id}, attrs) do
    create_post(Map.put(attrs, :user_id, user_id))
  end
end
```

### Pattern 3: Event-Based Communication
```elixir
# Publish events when something important happens
defmodule MyApp.Blog do
  def publish_post(post) do
    with {:ok, post} <- do_publish(post) do
      Phoenix.PubSub.broadcast(
        MyApp.PubSub,
        "posts",
        {:post_published, post}
      )
      {:ok, post}
    end
  end
end

# Other contexts subscribe to events
defmodule MyApp.Notifications do
  def handle_info({:post_published, post}, state) do
    send_notifications(post)
    {:noreply, state}
  end
end
```

## Common Context Patterns

### Accounts Context
```elixir
defmodule MyApp.Accounts do
  # User management
  def list_users
  def get_user!(id)
  def create_user(attrs)
  def update_user(user, attrs)
  def delete_user(user)

  # Authentication
  def authenticate(email, password)
  def change_password(user, password)

  # Authorization
  def assign_role(user, role)
  def has_permission?(user, permission)
end
```

### Catalog Context (E-commerce)
```elixir
defmodule MyApp.Catalog do
  # Products
  def list_products
  def get_product!(id)
  def create_product(attrs)

  # Categories
  def list_categories
  def get_category_products(category_id)

  # Search
  def search_products(query)
  def filter_products(filters)

  # Inventory
  def check_availability(product_id, quantity)
  def reserve_stock(product_id, quantity)
end
```

### Sales Context (E-commerce)
```elixir
defmodule MyApp.Sales do
  # Cart
  def get_cart(user_id)
  def add_to_cart(user_id, product_id, quantity)
  def update_cart_item(cart_item, quantity)

  # Orders
  def create_order(user_id, cart_id)
  def get_order!(id)
  def cancel_order(order)

  # Checkout
  def calculate_total(cart)
  def apply_discount(cart, code)
  def process_payment(order, payment_details)
end
```

## Anti-Patterns to Avoid

### 1. God Contexts
```elixir
# Bad: Kitchen sink context
defmodule MyApp.Core do
  def create_user(attrs)
  def create_product(attrs)
  def send_email(attrs)
  def process_payment(attrs)
end

# Good: Focused contexts
MyApp.Accounts.create_user(attrs)
MyApp.Catalog.create_product(attrs)
MyApp.Notifications.send_email(attrs)
MyApp.Billing.process_payment(attrs)
```

### 2. Direct Schema Access
```elixir
# Bad: Controllers accessing schemas directly
def index(conn, _params) do
  users = Repo.all(User)  # Don't do this!
  render(conn, "index.html", users: users)
end

# Good: Use context API
def index(conn, _params) do
  users = Accounts.list_users()
  render(conn, "index.html", users: users)
end
```

### 3. Context Coupling
```elixir
# Bad: Blog directly importing Accounts
defmodule MyApp.Blog do
  alias MyApp.Accounts.User

  def create_post_with_user(attrs) do
    user = Repo.get!(User, attrs.user_id)  # Direct coupling
    # ...
  end
end

# Good: Use IDs and delegate
defmodule MyApp.Blog do
  def create_post(attrs) do
    # Just verify user exists via ID
    unless Accounts.user_exists?(attrs.user_id) do
      {:error, :user_not_found}
    else
      # Create post
    end
  end
end
```

## Context Organization

```
lib/my_app/
├── accounts/
│   ├── user.ex
│   ├── session.ex
│   └── role.ex
├── accounts.ex          # Public API
├── blog/
│   ├── post.ex
│   ├── comment.ex
│   └── tag.ex
├── blog.ex              # Public API
└── catalog/
    ├── product.ex
    ├── category.ex
    └── variant.ex
```

## Testing Contexts

```elixir
defmodule MyApp.BlogTest do
  use MyApp.DataCase

  alias MyApp.Blog

  # Test context API, not internal functions
  describe "list_posts/0" do
    test "returns all posts" do
      # Setup
      post1 = fixture(:post)
      post2 = fixture(:post)

      # Execute
      posts = Blog.list_posts()

      # Assert
      assert length(posts) == 2
      assert post1 in posts
      assert post2 in posts
    end
  end

  describe "create_post/1" do
    test "with valid data" do
      attrs = %{title: "Title", body: "Body", user_id: 1}
      assert {:ok, post} = Blog.create_post(attrs)
      assert post.title == "Title"
    end

    test "with invalid data" do
      assert {:error, changeset} = Blog.create_post(%{})
      assert %{title: ["can't be blank"]} = errors_on(changeset)
    end
  end
end
```

## Migration Strategy

### Adding to Existing Codebase

1. **Identify Boundaries** - Group related functionality
2. **Create Context** - Start with one clear boundary
3. **Move Schemas** - Relocate related schemas
4. **Extract Functions** - Pull functions into context
5. **Update References** - Update controllers/views
6. **Write Tests** - Ensure nothing broke
7. **Repeat** - Continue with other boundaries

### Refactoring Example

**Before:**
```elixir
# Everything in one place
defmodule MyAppWeb.UserController do
  def index(conn, _params) do
    users = Repo.all(User)
    render(conn, "index.html", users: users)
  end
end
```

**After:**
```elixir
# Context layer
defmodule MyApp.Accounts do
  def list_users, do: Repo.all(User)
end

# Controller uses context
defmodule MyAppWeb.UserController do
  def index(conn, _params) do
    users = Accounts.list_users()
    render(conn, "index.html", users: users)
  end
end
```
