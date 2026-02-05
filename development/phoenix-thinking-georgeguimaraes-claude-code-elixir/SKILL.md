---
name: phoenix-thinking
description: Use when writing Phoenix, LiveView, or Plug code. Contains insights about LiveView lifecycle, Scopes, PubSub, and gotchas from Chris McCord.
---

# Phoenix Thinking

Mental shifts for Phoenix applications. These insights challenge typical web framework patterns.

## The Iron Law

```
NO DATABASE QUERIES IN MOUNT
```

mount/3 is called TWICE (HTTP request + WebSocket connection). Queries in mount = duplicate queries.

```elixir
def mount(_params, _session, socket) do
  # NO database queries here! Called twice.
  {:ok, assign(socket, posts: [], loading: true)}
end

def handle_params(params, _uri, socket) do
  # Database queries here - once per navigation
  posts = Blog.list_posts(socket.assigns.scope)
  {:noreply, assign(socket, posts: posts, loading: false)}
end
```

**mount/3** = setup only (empty assigns, subscriptions, defaults)
**handle_params/3** = data loading (all database queries, URL-driven state)

**No exceptions:** Don't query "just this one small thing" in mount. Don't "optimize later". LiveView lifecycle is non-negotiable.

## Scopes: Security-First Pattern (Phoenix 1.8+)

Scopes address OWASP #1 vulnerability: Broken Access Control. Authorization context is threaded automatically—no more forgetting to scope queries.

```elixir
def list_posts(%Scope{user: user}) do
  Post |> where(user_id: ^user.id) |> Repo.all()
end
```

## PubSub Topics Must Be Scoped

```elixir
def subscribe(%Scope{organization: org}) do
  Phoenix.PubSub.subscribe(@pubsub, "posts:org:#{org.id}")
end
```

Unscoped topics = data leaks between tenants.

## External Polling: GenServer, Not LiveView

**Bad:** Every connected user makes API calls (multiplied by users).
**Good:** Single GenServer polls, broadcasts to all via PubSub.

## Components Receive Data, LiveViews Own Data

- **Functional components:** Display-only, no internal state
- **LiveComponents:** Own state, handle own events
- **LiveViews:** Full page, owns URL, top-level state

## Async Data Loading

Use `assign_async/3` for data that can load after mount:

```elixir
def mount(_params, _session, socket) do
  {:ok, assign_async(socket, :user, fn -> {:ok, %{user: fetch_user()}} end)}
end
```

## Gotchas from Core Team

### LiveView terminate/2 Requires trap_exit

`terminate/2` only fires if you're trapping exits—which you shouldn't do in LiveView.

**Fix:** Use a separate GenServer that monitors the LiveView process via `Process.monitor/1`, then handle `:DOWN` messages to run cleanup.

### start_async Duplicate Names: Later Wins

Calling `start_async` with the same name while a task is in-flight: the **later one wins**, the previous task's result is ignored.

**Fix:** Call `cancel_async/3` first if you want to abort the previous task.

### Channel Intercept Socket State is Stale

The socket in `handle_out` intercept is a snapshot from subscription time, not current state.

**Why:** Socket is copied into fastlane lookup at subscription time for performance.

**Fix:** Use separate topics per role, or fetch current state explicitly.

### CSS Class Precedence is Stylesheet Order

When merging classes on components, precedence is determined by **stylesheet order**, not HTML order. If `btn-primary` appears later in the compiled CSS than `bg-red-500`, it wins regardless of HTML order.

**Fix:** Use variant props instead of class merging.

### Upload Content-Type Can't Be Trusted

The `:content_type` in `%Plug.Upload{}` is user-provided. Always validate actual file contents (magic bytes) and rewrite filename/extension.

### Read Body Before Plug.Parsers for Webhooks

To verify webhook signatures, you need the raw body. But Plug.Parsers consumes it.

```elixir
{:ok, body, conn} = Plug.Conn.read_body(conn)
verify_signature!(conn, body)
%{conn | body_params: JSON.decode!(body)}
```

Don't use `preserve_req_body: true`—it keeps the entire body in memory for ALL requests.

## Red Flags - STOP and Reconsider

- Database query in mount/3
- Unscoped PubSub topics in multi-tenant app
- LiveView polling external APIs directly
- Using terminate/2 for cleanup (won't fire without trap_exit)
- Calling start_async with same name without cancel_async first
- Relying on socket.assigns in Channel intercepts (stale!)
- CSS class merging for component customization (use variants)
- Trusting `%Plug.Upload{}.content_type` for security

**Any of these? Re-read The Iron Law and the Gotchas section.**
