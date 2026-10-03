---
name: phoenix
description: Build Phoenix/Elixir apps — APIs, LiveView, Ecto, Channels, OTP patterns, Oban jobs.
when_to_use: Reach for this when the project is an Elixir Phoenix app (mix.exs with :phoenix, lib/*_web). This is the Elixir web-framework skill; for Phoenix/Elixir *tests* use exunit. For Ruby web apps use rails instead.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "mix.exs"
  - "lib/**/*_web/**/*.ex"
  - "lib/**/*.ex"
---

# Phoenix Framework Skill - Quick Reference

**Version**: 1.0.0 | **Last Updated**: 2025-10-22 | **Agent**: backend-developer

Quick reference for Phoenix and Elixir development patterns. For comprehensive documentation, see REFERENCE.md.

---

## Table of Contents

1. [Phoenix API Development](#phoenix-api-development)
2. [OTP Patterns](#otp-patterns)
3. [Phoenix LiveView](#phoenix-liveview)
4. [Ecto Database Operations](#ecto-database-operations)
5. [Phoenix Channels](#phoenix-channels)
6. [Background Jobs (Oban)](#background-jobs-oban)
7. [Production Deployment](#production-deployment)
8. [Testing with ExUnit](#testing-with-exunit)
9. [Security Best Practices](#security-best-practices)
10. [Performance Optimization](#performance-optimization)

---

## Phoenix API Development

### RESTful Controller Pattern

```elixir
defmodule MyAppWeb.PostController do
  use MyAppWeb, :controller
  alias MyApp.Blog
  alias MyApp.Blog.Post

  # List all posts
  def index(conn, _params) do
    posts = Blog.list_posts()
    render(conn, "index.json", posts: posts)
  end

  # Show single post
  def show(conn, %{"id" => id}) do
    post = Blog.get_post!(id)
    render(conn, "show.json", post: post)
  end

  # Create post
  def create(conn, %{"post" => post_params}) do
    case Blog.create_post(post_params) do
      {:ok, post} ->
        conn
        |> put_status(:created)
        |> render("show.json", post: post)
      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> render("error.json", changeset: changeset)
    end
  end

  # Update post
  def update(conn, %{"id" => id, "post" => post_params}) do
    post = Blog.get_post!(id)
    case Blog.update_post(post, post_params) do
      {:ok, updated_post} ->
        render(conn, "show.json", post: updated_post)
      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> render("error.json", changeset: changeset)
    end
  end

  # Delete post
  def delete(conn, %{"id" => id}) do
    post = Blog.get_post!(id)
    {:ok, _post} = Blog.delete_post(post)
    send_resp(conn, :no_content, "")
  end
end
```

### Phoenix Context Pattern

```elixir
defmodule MyApp.Blog do
  @moduledoc """
  The Blog context - business logic for blog operations
  """

  alias MyApp.Repo
  alias MyApp.Blog.Post
  import Ecto.Query

  # List all posts with associations preloaded
  def list_posts do
    Post
    |> preload(:author)
    |> order_by(desc: :inserted_at)
    |> Repo.all()
  end

  # Get single post with error handling
  def get_post!(id) do
    Post
    |> preload(:author)
    |> Repo.get!(id)
  end

  # Create post with validation
  def create_post(attrs) do
    %Post{}
    |> Post.changeset(attrs)
    |> Repo.insert()
  end

  # Update post
  def update_post(%Post{} = post, attrs) do
    post
    |> Post.changeset(attrs)
    |> Repo.update()
  end

  # Delete post
  def delete_post(%Post{} = post) do
    Repo.delete(post)
  end
end
```

### Routing with Pipelines

```elixir
# router.ex
defmodule MyAppWeb.Router do
  use MyAppWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  pipeline :authenticated do
    plug MyAppWeb.Auth.Pipeline
  end

  scope "/api", MyAppWeb do
    pipe_through :api

    # Public routes
    post "/login", AuthController, :login
    post "/register", AuthController, :register

    # Authenticated routes
    pipe_through :authenticated
    resources "/posts", PostController
    resources "/comments", CommentController
  end
end
```

---

## OTP Patterns

### GenServer Pattern

```elixir
defmodule MyApp.Cache do
  use GenServer

  # Client API
  def start_link(opts \\\\ []) do
    GenServer.start_link(__MODULE__, %{}, opts)
  end

  def get(server, key) do
    GenServer.call(server, {:get, key})
  end

  def put(server, key, value) do
    GenServer.cast(server, {:put, key, value})
  end

  # Server Callbacks
  @impl true
  def init(_state) do
    {:ok, %{}}
  end

  @impl true
  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key), state}
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    {:noreply, Map.put(state, key, value)}
  end

  @impl true
  def handle_info(:cleanup, state) do
    # Periodic cleanup
    {:noreply, %{}}
  end
end
```

### Supervisor Tree

```elixir
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Database connection pool
      MyApp.Repo,
      # PubSub for real-time features
      {Phoenix.PubSub, name: MyApp.PubSub},
      # Phoenix Endpoint
      MyAppWeb.Endpoint,
      # Custom GenServer
      {MyApp.Cache, name: MyApp.Cache},
      # Task Supervisor for async tasks
      {Task.Supervisor, name: MyApp.TaskSupervisor},
      # Oban for background jobs
      {Oban, Application.fetch_env!(:my_app, Oban)}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

### Task for Async Operations

```elixir
# Fire and forget
Task.start(fn -> send_notification(user) end)

# Supervised task
Task.Supervisor.start_child(MyApp.TaskSupervisor, fn ->
  process_large_file(file_path)
end)

# Task with await
task = Task.async(fn -> fetch_external_data() end)
result = Task.await(task, 5000) # 5 second timeout
```

---

## Phoenix LiveView

### Basic LiveView Component

```elixir
defmodule MyAppWeb.DashboardLive do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      # Subscribe to real-time updates
      Phoenix.PubSub.subscribe(MyApp.PubSub, "metrics:updates")
      # Schedule periodic refresh
      :timer.send_interval(30_000, self(), :refresh)
    end

    {:ok, assign(socket, :metrics, get_metrics())}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="dashboard">
      <h1>Dashboard</h1>
      <.metrics_display metrics={@metrics} />
      <button phx-click="refresh">Refresh</button>
    </div>
    """
  end

  @impl true
  def handle_event("refresh", _params, socket) do
    {:noreply, assign(socket, :metrics, get_metrics())}
  end

  @impl true
  def handle_info({:metric_update, new_metrics}, socket) do
    {:noreply, assign(socket, :metrics, new_metrics)}
  end

  @impl true
  def handle_info(:refresh, socket) do
    {:noreply, assign(socket, :metrics, get_metrics())}
  end

  defp get_metrics do
    # Fetch metrics from database or cache
  end
end
```

### LiveView Form with Validation

```elixir
defmodule MyAppWeb.UserLive.Form do
  use MyAppWeb, :live_view
  alias MyApp.Accounts
  alias MyApp.Accounts.User

  @impl true
  def mount(_params, _session, socket) do
    changeset = Accounts.change_user(%User{})
    {:ok, assign(socket, changeset: changeset)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <.form
      for={@changeset}
      phx-change="validate"
      phx-submit="save"
    >
      <.input field={@changeset[:name]} label="Name" />
      <.input field={@changeset[:email]} label="Email" type="email" />
      <.button>Save</.button>
    </.form>
    """
  end

  @impl true
  def handle_event("validate", %{"user" => user_params}, socket) do
    changeset =
      %User{}
      |> Accounts.change_user(user_params)
      |> Map.put(:action, :validate)

    {:noreply, assign(socket, changeset: changeset)}
  end

  @impl true
  def handle_event("save", %{"user" => user_params}, socket) do
    case Accounts.create_user(user_params) do
      {:ok, user} ->
        {:noreply,
         socket
         |> put_flash(:info, "User created successfully")
         |> redirect(to: ~p"/users/#{user}")}

      {:error, changeset} ->
        {:noreply, assign(socket, changeset: changeset)}
    end
  end
end
```

### LiveView Streams for Performance

```elixir
defmodule MyAppWeb.PostsLive do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok,
     socket
     |> stream(:posts, MyApp.Blog.list_posts())}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div id="posts" phx-update="stream">
      <div :for={{id, post} <- @streams.posts} id={id}>
        <%= post.title %>
      </div>
    </div>
    """
  end

  @impl true
  def handle_info({:new_post, post}, socket) do
    {:noreply, stream_insert(socket, :posts, post, at: 0)}
  end
end
```

---

## Ecto Database Operations

### Ecto Schema

```elixir
defmodule MyApp.Blog.Post do
  use Ecto.Schema
  import Ecto.Changeset

  schema "posts" do
    field :title, :string
    field :body, :text
    field :published, :boolean, default: false
    field :views, :integer, default: 0

    belongs_to :author, MyApp.Accounts.User
    has_many :comments, MyApp.Blog.Comment

    timestamps()
  end

  def changeset(post, attrs) do
    post
    |> cast(attrs, [:title, :body, :published, :author_id])
    |> validate_required([:title, :body, :author_id])
    |> validate_length(:title, min: 3, max: 255)
    |> validate_length(:body, min: 10)
    |> foreign_key_constraint(:author_id)
  end
end
```

### Query Optimization (N+1 Prevention)

```elixir
# ❌ Bad: N+1 query problem
def list_posts_bad do
  posts = Repo.all(Post)
  # Each access to post.author triggers a separate query
  Enum.map(posts, fn post ->
    %{title: post.title, author: post.author.name}
  end)
end

# ✅ Good: Preload association
def list_posts_good do
  Post
  |> preload(:author)
  |> Repo.all()
  |> Enum.map(fn post ->
    %{title: post.title, author: post.author.name}
  end)
end

# ✅ Better: Join with select for specific fields
def list_posts_optimized do
  from p in Post,
    join: a in assoc(p, :author),
    select: %{title: p.title, author_name: a.name}
  |> Repo.all()
end
```

### Advanced Queries

```elixir
# Pagination
def list_posts_paginated(page, per_page \\\\ 20) do
  from(p in Post,
    order_by: [desc: p.inserted_at],
    limit: ^per_page,
    offset: ^((page - 1) * per_page)
  )
  |> Repo.all()
end

# Search
def search_posts(query_string) do
  search_term = "%#{query_string}%"

  from(p in Post,
    where: ilike(p.title, ^search_term) or ilike(p.body, ^search_term)
  )
  |> Repo.all()
end

# Aggregation
def post_stats do
  from(p in Post,
    select: %{
      total: count(p.id),
      published: count(p.id, :distinct) |> filter(where: p.published),
      avg_views: avg(p.views)
    }
  )
  |> Repo.one()
end
```

### Migrations

```elixir
defmodule MyApp.Repo.Migrations.CreatePosts do
  use Ecto.Migration

  def change do
    create table(:posts) do
      add :title, :string, null: false
      add :body, :text, null: false
      add :published, :boolean, default: false
      add :views, :integer, default: 0
      add :author_id, references(:users, on_delete: :delete_all), null: false

      timestamps()
    end

    create index(:posts, [:author_id])
    create index(:posts, [:published])
    create index(:posts, [:inserted_at])
  end
end
```

---

## Phoenix Channels

### Channel Definition

```elixir
defmodule MyAppWeb.RoomChannel do
  use MyAppWeb, :channel
  alias MyApp.Chat

  @impl true
  def join("room:" <> room_id, _params, socket) do
    if authorized?(socket, room_id) do
      send(self(), :after_join)
      {:ok, socket}
    else
      {:error, %{reason: "unauthorized"}}
    end
  end

  @impl true
  def handle_in("new_msg", %{"body" => body}, socket) do
    message = Chat.create_message(%{
      room_id: socket.assigns.room_id,
      user_id: socket.assigns.user_id,
      body: body
    })

    broadcast!(socket, "new_msg", %{
      id: message.id,
      body: message.body,
      user: message.user.name
    })

    {:noreply, socket}
  end

  @impl true
  def handle_info(:after_join, socket) do
    messages = Chat.list_recent_messages(socket.assigns.room_id, 50)
    push(socket, "messages", %{messages: messages})
    {:noreply, socket}
  end

  defp authorized?(socket, room_id) do
    # Check if user can access room
    socket.assigns[:user_id] != nil
  end
end
```

### Phoenix Presence

```elixir
defmodule MyAppWeb.Presence do
  use Phoenix.Presence,
    otp_app: :my_app,
    pubsub_server: MyApp.PubSub
end

# Track user in channel
def handle_info(:after_join, socket) do
  {:ok, _} = Presence.track(socket, socket.assigns.user_id, %{
    online_at: System.system_time(:second)
  })

  push(socket, "presence_state", Presence.list(socket))
  {:noreply, socket}
end
```

---

## Background Jobs (Oban)

### Oban Worker

```elixir
defmodule MyApp.Workers.EmailWorker do
  use Oban.Worker,
    queue: :emails,
    max_attempts: 3,
    priority: 1

  @impl Oban.Worker
  def perform(%Oban.Job{args: %{"user_id" => user_id, "type" => type}}) do
    user = MyApp.Accounts.get_user!(user_id)

    case type do
      "welcome" -> MyApp.Mailer.send_welcome_email(user)
      "reset_password" -> MyApp.Mailer.send_password_reset(user)
      _ -> {:error, "unknown email type"}
    end
  end
end
```

### Scheduling Jobs

```elixir
# Immediate job
%{user_id: user.id, type: "welcome"}
|> MyApp.Workers.EmailWorker.new()
|> Oban.insert()

# Delayed job (1 hour)
%{user_id: user.id, type: "reminder"}
|> MyApp.Workers.EmailWorker.new(schedule_in: 3600)
|> Oban.insert()

# Scheduled at specific time
%{user_id: user.id, type: "newsletter"}
|> MyApp.Workers.EmailWorker.new(scheduled_at: ~U[2025-12-25 09:00:00Z])
|> Oban.insert()

# Unique job (prevent duplicates)
%{user_id: user.id, type: "daily_summary"}
|> MyApp.Workers.EmailWorker.new(
  unique: [period: 86400, fields: [:user_id, :type]]
)
|> Oban.insert()
```

### Cron Jobs

```elixir
# config/config.exs
config :my_app, Oban,
  repo: MyApp.Repo,
  queues: [default: 10, emails: 20, reports: 5],
  plugins: [
    {Oban.Plugins.Cron,
     crontab: [
       {"0 2 * * *", MyApp.Workers.DailyReportWorker},
       {"*/15 * * * *", MyApp.Workers.CacheWarmerWorker},
       {"0 0 * * 0", MyApp.Workers.WeeklyDigestWorker}
     ]}
  ]
```

---

## Production Deployment

### Runtime Configuration

```elixir
# config/runtime.exs
import Config

if config_env() == :prod do
  database_url = System.get_env("DATABASE_URL") ||
    raise "DATABASE_URL not set"

  config :my_app, MyApp.Repo,
    url: database_url,
    pool_size: String.to_integer(System.get_env("POOL_SIZE") || "10"),
    ssl: true

  config :my_app, MyAppWeb.Endpoint,
    url: [host: System.get_env("PHX_HOST"), port: 443],
    http: [port: String.to_integer(System.get_env("PORT") || "4000")],
    secret_key_base: System.get_env("SECRET_KEY_BASE")
end
```

### Health Checks

```elixir
defmodule MyAppWeb.HealthController do
  use MyAppWeb, :controller

  def check(conn, _params) do
    checks = %{
      database: database_healthy?(),
      cache: cache_healthy?(),
      oban: oban_healthy?()
    }

    status = if Enum.all?(Map.values(checks), & &1), do: 200, else: 503

    conn
    |> put_status(status)
    |> json(checks)
  end

  defp database_healthy? do
    case MyApp.Repo.query("SELECT 1") do
      {:ok, _} -> true
      _ -> false
    end
  end

  defp cache_healthy? do
    # Check Redis or ETS cache
    true
  end

  defp oban_healthy? do
    # Check Oban queues
    true
  end
end
```

### Telemetry Instrumentation

```elixir
defmodule MyApp.Telemetry do
  use Supervisor
  import Telemetry.Metrics

  def start_link(arg) do
    Supervisor.start_link(__MODULE__, arg, name: __MODULE__)
  end

  def init(_arg) do
    children = [
      {:telemetry_poller, measurements: periodic_measurements(), period: 10_000}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end

  def metrics do
    [
      # Phoenix Metrics
      summary("phoenix.endpoint.stop.duration",
        unit: {:native, :millisecond}
      ),
      summary("phoenix.router_dispatch.stop.duration",
        tags: [:route],
        unit: {:native, :millisecond}
      ),

      # Database Metrics
      summary("my_app.repo.query.total_time",
        unit: {:native, :millisecond}
      ),
      summary("my_app.repo.query.queue_time",
        unit: {:native, :millisecond}
      ),

      # VM Metrics
      summary("vm.memory.total", unit: {:byte, :megabyte}),
      summary("vm.total_run_queue_lengths.total"),
      summary("vm.total_run_queue_lengths.cpu"),
      summary("vm.total_run_queue_lengths.io")
    ]
  end

  defp periodic_measurements do
    []
  end
end
```

---

## Testing with ExUnit

### Context Testing

```elixir
defmodule MyApp.BlogTest do
  use MyApp.DataCase
  alias MyApp.Blog

  describe "posts" do
    test "list_posts/0 returns all posts" do
      post = post_fixture()
      assert Blog.list_posts() == [post]
    end

    test "get_post!/1 returns the post with given id" do
      post = post_fixture()
      assert Blog.get_post!(post.id) == post
    end

    test "create_post/1 with valid data creates a post" do
      attrs = %{title: "Title", body: "Body", author_id: author_fixture().id}
      assert {:ok, %Post{} = post} = Blog.create_post(attrs)
      assert post.title == "Title"
    end

    test "create_post/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Blog.create_post(%{})
    end
  end

  defp post_fixture(attrs \\\\ %{}) do
    {:ok, post} =
      attrs
      |> Enum.into(%{
        title: "some title",
        body: "some body",
        author_id: author_fixture().id
      })
      |> Blog.create_post()

    post
  end
end
```

### Controller Testing

```elixir
defmodule MyAppWeb.PostControllerTest do
  use MyAppWeb.ConnCase
  alias MyApp.Blog

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all posts", %{conn: conn} do
      conn = get(conn, ~p"/api/posts")
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create post" do
    test "renders post when data is valid", %{conn: conn} do
      attrs = %{title: "Title", body: "Body", author_id: author_fixture().id}
      conn = post(conn, ~p"/api/posts", post: attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, ~p"/api/posts/#{id}")
      assert %{"id" => ^id, "title" => "Title"} = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/api/posts", post: %{})
      assert json_response(conn, 422)["errors"] != %{}
    end
  end
end
```

### LiveView Testing

```elixir
defmodule MyAppWeb.DashboardLiveTest do
  use MyAppWeb.ConnCase
  import Phoenix.LiveViewTest

  test "displays dashboard metrics", %{conn: conn} do
    {:ok, view, html} = live(conn, ~p"/dashboard")
    assert html =~ "Dashboard"
    assert render(view) =~ "metrics"
  end

  test "refreshes metrics on button click", %{conn: conn} do
    {:ok, view, _html} = live(conn, ~p"/dashboard")
    assert view |> element("button", "Refresh") |> render_click()
    assert render(view) =~ "metrics"
  end

  test "receives real-time updates", %{conn: conn} do
    {:ok, view, _html} = live(conn, ~p"/dashboard")

    # Broadcast update
    Phoenix.PubSub.broadcast(MyApp.PubSub, "metrics:updates", {:metric_update, %{}})

    assert render(view) =~ "metrics"
  end
end
```

---

## Security Best Practices

### SQL Injection Prevention

```elixir
# ❌ NEVER use string interpolation in queries
def get_user_bad(email) do
  Repo.query("SELECT * FROM users WHERE email = '#{email}'")
end

# ✅ ALWAYS use Ecto parameterization
def get_user_good(email) do
  from(u in User, where: u.email == ^email)
  |> Repo.one()
end
```

### Input Validation

```elixir
def changeset(user, attrs) do
  user
  |> cast(attrs, [:email, :password])
  |> validate_required([:email, :password])
  |> validate_format(:email, ~r/@/)
  |> validate_length(:password, min: 8)
  |> validate_confirmation(:password)
  |> unique_constraint(:email)
  |> hash_password()
end
```

### Authentication with phx.gen.auth

```bash
mix phx.gen.auth Accounts User users
```

---

## Performance Optimization

### Query Optimization Checklist

- ✅ Preload associations to prevent N+1 queries
- ✅ Use `select` to fetch only required fields
- ✅ Add database indexes for frequently queried columns
- ✅ Use `join` instead of `preload` for aggregations
- ✅ Implement pagination for large result sets
- ✅ Use `Repo.stream` for processing large datasets

### LiveView Performance

```elixir
# Use streams for large lists
socket |> stream(:posts, posts)

# Mark non-reactive assigns as temporary
socket |> assign(:large_data, value) |> assign(:temp_assigns, [:large_data])

# Optimize rendering with targeted updates
socket |> push_event("update_chart", %{data: chart_data})
```

### Caching with ETS

```elixir
defmodule MyApp.Cache do
  def get(key) do
    case :ets.lookup(:my_cache, key) do
      [{^key, value}] -> {:ok, value}
      [] -> :error
    end
  end

  def put(key, value, ttl \\\\ 3600) do
    :ets.insert(:my_cache, {key, value})
    schedule_expiry(key, ttl)
  end
end
```

---

## Quick Reference Cheatsheet

### Mix Commands

```bash
mix phx.new my_app                    # Create new Phoenix project
mix phx.server                        # Start development server
mix ecto.create                       # Create database
mix ecto.migrate                      # Run migrations
mix ecto.rollback                     # Rollback last migration
mix phx.gen.context Blog Post posts   # Generate context + schema
mix phx.gen.live Blog Post posts      # Generate LiveView CRUD
mix test                              # Run tests
mix test --cover                      # Run tests with coverage
mix format                            # Format code
mix deps.get                          # Install dependencies
```

### IEx Helpers

```elixir
iex -S mix phx.server                 # Start server with IEx
h Module                              # View module documentation
recompile                             # Recompile changed files
MyApp.Repo.all(User)                  # Query database
```

---

**For More Details**: See [REFERENCE.md](REFERENCE.md) for comprehensive guides, advanced patterns, and production optimization strategies.
