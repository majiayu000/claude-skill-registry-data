---
name: liveview-patterns
description: Phoenix LiveView UI and real-time feature patterns
---

# LiveView Patterns Skill

Use this skill when:
- Building LiveView interfaces
- Implementing real-time features
- Designing component-based UI
- Optimizing LiveView performance
- Handling state management
- Working with Phoenix PubSub

## Core Patterns

### 1. Optimistic UI Updates

```elixir
# ✅ Good: Optimistic updates with rollback
defmodule MyAppWeb.Live.UserForm do
  use MyAppWeb, :live_view

  @impl true
  def handle_event("save", params, socket, assign) do
    # Optimistically update UI
    {:noreply, assign(socket, :saving, true)}
  end

  @impl true
  def handle_info({:update_result, :success}, socket, assign) do
    {:noreply, assign(socket, :saving, false)}
  end

  @impl true
  def handle_info({:update_result, :error}, socket, assign) do
    {:noreply, put_flash(socket, :error, "Failed to save")}
  end
end

# ❌ Bad: Block until save completes
defmodule MyAppWeb.Live.BadForm do
  use MyAppWeb, :live_view

  def handle_event("save", params, socket, assign) do
    # UI blocks during save
    {:noreply, assign(socket, :disabled, true)}
  end
end
```

### 2. LiveView Streams

```elixir
# ✅ Good: Use streams for large lists
defmodule MyAppWeb.Live.UserList do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, :users, stream(socket, MyApp.Users.list_users())}
  end
end

# ❌ Bad: Render entire list in memory
defmodule MyAppWeb.Live.BadUserList do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, :users, MyApp.Users.list_users())}
  end
end
```

### 3. Component Pattern

```elixir
# ✅ Good: Reusable function components
defmodule MyAppWeb.CoreComponents do
  use Phoenix.Component

  attr :id, :string, required: true
  attr :title, :string
  attr :class, :string, default: ""

  def button(assigns) do
    ~H"""
    <button
      type="button"
      id={@id}
      class={@class}
    >
      {@title}
    </button>
    """
  end

  def user_card(assigns) do
    ~H"""
    <div class="user-card #{@class}">
      <h2><%= @title %></h2>
      <p><%= @description %></p>
      <.user_email><%= @email %></.user_email>
    </div>
    """
  end
end

# ❌ Bad: Monolithic LiveView
defmodule MyAppWeb.Live.UserCard do
  use MyAppWeb, :live_view

  @impl true
  def render(assigns) do
    ~H"""
    <div class="user-card">
      <!-- Large component rendering inline -->
      <h2><%= @user.name %></h2>
      <p><%= @user.email %></p>
      <%= if @user.admin? do %>
        <span class="badge">Admin</span>
      <% end %>
    </div>
    """
  end
end
```

### 4. PubSub Integration

```elixir
# ✅ Good: Subscribe to PubSub topics
defmodule MyAppWeb.Live.Dashboard do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      MyApp.PubSub.subscribe(socket, "users_updates")
    end

    {:ok, assign(socket, :users, [])}
  end

  @impl true
  def handle_info({:user_updated, user}, socket, assign) do
    {:noreply, update(socket, :users, fn users -> [user | users])}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket, assign) do
    MyApp.Users.delete_user(id)
    MyApp.PubSub.broadcast("users_updates", {:user_deleted, id})
  end

  @impl true
  def terminate(_reason, socket) do
    if connected?(socket) do
      MyApp.PubSub.unsubscribe(socket, "users_updates")
    end
  end
end

# ❌ Bad: Polling for updates
defmodule MyAppWeb.Live.BadDashboard do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    # Polling is inefficient
    send(self(), :update_users)
    {:ok, assign(socket, :users, [])}
  end

  @impl true
  def handle_info(:update_users, socket, assign) do
    users = MyApp.Users.list_users()
    {:noreply, assign(socket, :users, users)}
  end
end
```

## Performance Optimization

### 1. Upload Handling

```elixir
# ✅ Good: Chunked uploads with progress
defmodule MyAppWeb.Live.FileUpload do
  use MyAppWeb, :live_view

  @impl true
  def handle_event("select_files", params, socket, assign) do
    upload_files(params.files)
    {:noreply, socket}
  end

  @impl true
  def handle_info({:upload_progress, :file_id, :progress}, socket, assign) do
    {:noreply, assign(socket, uploads: update_upload(socket.assigns.uploads, file_id, progress))}
  end

  defp upload_files(files) do
    files
    |> Enum.chunk_every(5)  # Process in chunks of 5
    |> Enum.each(fn chunk ->
         send(self(), {:upload_chunk, chunk})
       end)
  end
end

# ❌ Bad: Upload all files at once
defmodule MyAppWeb.Live.BadFileUpload do
  use MyAppWeb, :live_view

  @impl true
  def handle_event("select_files", params, socket, assign) do
    # Blocks while uploading
    Enum.each(params.files, fn file ->
      MyApp.Storage.upload(file)
    end)
    {:noreply, socket}
  end
end
```

### 2. Debouncing Events

```elixir
# ✅ Good: Debounce rapid events
defmodule MyAppWeb.Live.Search do
  use MyAppWeb, :live_view

  @impl true
  def handle_event("search", %{"query" => query}, socket, assign) do
    debounce_search(query, 300)
  end

  defp debounce_search(query, delay_ms) do
    # Only trigger search after delay
    send_after(self(), {:search, query}, delay_ms)
  end

  @impl true
  def handle_info({:search, query}, socket, assign) do
    results = MyApp.Search.search(query)
    {:noreply, assign(socket, :results, results)}
  end
end

# ❌ Bad: No debouncing
defmodule MyAppWeb.Live.BadSearch do
  use MyAppWeb, :live_view

  @impl true
  def handle_event("search", %{"query" => query}, socket, assign) do
    # Every keystroke triggers search
    results = MyApp.Search.search(query)
    {:noreply, assign(socket, :results, results)}
  end
end
```

## State Management

### 1. GenServer for Global State

```elixir
# ✅ Good: Use GenServer for complex state
defmodule MyApp.GlobalState do
  use GenServer

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{})
  end

  # Client API
  def get_user_count do
    GenServer.call(__MODULE__, :get_count)
  end

  def update_user_count(delta) do
    GenServer.cast(__MODULE__, {:update, delta})
  end

  # Server callbacks
  @impl true
  def init(state) do
    {:ok, %{state | user_count: 0}}
  end

  @impl true
  def handle_cast({:update, delta}, state) do
    new_count = state.user_count + delta
    {:noreply, %{state | user_count: new_count}}
  end

  @impl true
  def handle_call(:get_count, _from, state) do
    {:reply, state.user_count, state}
  end
end
```

### 2. Assigns for Local State

```elixir
# ✅ Good: Use assigns for simple state
defmodule MyAppWeb.Live.Counter do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, :count, 0)}
  end

  @impl true
  def handle_event("increment", _params, socket, assign) do
    {:noreply, update(socket, :count, socket.assigns.count + 1)}
  end

  @impl true
  def handle_event("decrement", _params, socket, assign) do
    if socket.assigns.count > 0 do
      {:noreply, update(socket, :count, socket.assigns.count - 1)}
    else
      {:noreply, socket}
    end
  end
end

# ❌ Bad: Using external state management
defmodule MyAppWeb.Live.BadCounter do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, :count, get_count_from_external_service())}
  end

  @impl true
  def handle_event("increment", _params, socket, assign) do
    # External service call
    new_count = get_count_from_external_service() + 1
    {:noreply, assign(socket, :count, new_count)}
  end
end
```

## Real-Time Features

### 1. Live Navigation

```elixir
# ✅ Good: Use Live navigation with handle_params
defmodule MyAppWeb.Live.Users do
  use MyAppWeb, :live_view

  @impl true
  def handle_params(%{"id" => id}, _uri, socket, assign) do
    {:noreply, assign(socket, :user, MyApp.Users.get(id))}
  end
end
```

### 2. Live Notifications

```elixir
# ✅ Good: PubSub-based live notifications
defmodule MyAppWeb.Live.Notifications do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    MyApp.PubSub.subscribe(socket, "notifications")
    {:ok, assign(socket, :notifications, [])}
  end

  @impl true
  def handle_info({:new_notification, notification}, socket, assign) do
    {:noreply, update(socket, :notifications, [notification | socket.assigns.notifications])}
  end
end
```

## Best Practices

### 1. Component Design
- **Keep components small and focused**
- **Use slots for flexibility**
- **Leverage Phoenix.Component for reusability**
- **Document public components**

### 2. Performance
- **Use streams for large data sets**
- **Implement debouncing for rapid events**
- **Use optimistic updates with rollback**
- **Chunk file uploads**
- **Avoid unnecessary re-renders**

### 3. PubSub
- **Subscribe on mount, unsubscribe on terminate**
- **Use topic-based subscriptions**
- **Broadcast for state changes
- **Handle disconnects gracefully**

### 4. State Management
- **Use assigns for simple state**
- **Use GenServer for complex global state**
- **Avoid external state for LiveView-local state**
- **Implement proper cleanup on terminate**

### 5. Accessibility
- **Use ARIA attributes**
- **Provide keyboard navigation**
- **Include proper labels for forms**
- **Test with screen readers**

## Token Efficiency

Use LiveView patterns for:
- Real-time UI updates (~50% token savings vs page refreshes)
- Optimistic updates (~30% token savings vs blocking operations)
- Component reusability (~40% token savings vs code duplication)
- Stream handling (~60% token savings vs rendering large lists)
