---
name: otp-patterns
description: Implements OTP design patterns including GenServer, Supervisor, and Application behaviors.
---

# OTP Patterns Skill

Use this skill when implementing OTP behaviors and patterns in Elixir.

## When to Use

- Creating new GenServers or Supervisors
- Designing supervision trees
- Implementing process-based features

## GenServer Pattern

### Basic GenServer

```elixir
defmodule Cache.Worker do
  use GenServer

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  def get(key), do: GenServer.call(__MODULE__, {:get, key})
  def put(key, value), do: GenServer.cast(__MODULE__, {:put, key, value})

  # Server Callbacks
  @impl true
  def init(opts), do: {:ok, %{cache: %{}, opts: opts}}

  @impl true
  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state.cache, key), state}
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    {:noreply, put_in(state.cache[key], value)}
  end
end
```

### Named Processes

```elixir
# ✅ Good - Named process
{Cache.Worker, name: {:via, Registry, {MyRegistry, :worker}}

# ✅ Good - Module name
{Cache.Worker, name: Cache.Worker}

# ❌ Bad - PID dependencies
pid = Process.whereis(:some_process)
```

## Supervisor Pattern

### One-For-One

```elixir
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      MyApp.Repo,
      {Registry, keys: :unique, name: MyApp.Registry},
      {MyApp.WorkerSupervisor, []},
      MyAppWeb.Endpoint
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

### Dynamic Supervisor

```elixir
defmodule DynamicSupervisor do
  def start_link(init_arg, opts \\ []) do
    DynamicSupervisor.start_link(__MODULE__, init_arg, opts)
  end

  @impl true
  def init(init_arg, opts) do
    DynamicSupervisor.init(init_arg, opts)
  end
end
```

## Common Anti-Patterns

### Blocking GenServer Callbacks

```elixir
# ❌ Bad - Blocks entire GenServer
@impl true
def handle_call(:slow_operation, _from, state) do
  result = HTTPoison.get!("https://api.example.com")
  {:reply, result, state}
end

# ✅ Good - Use Task for async
@impl true
def handle_call(:slow_operation, from, state) do
  Task.start(fn ->
    result = HTTPoison.get!("https://api.example.com")
    GenServer.reply(from, result)
  end)
  {:noreply, state}
end
```

### Overusing Shared State via ETS

```elixir
# ❌ Bad - Breaks immutability
ETS.update(:cache, :key, value)

# ✅ Good - Use GenServer for stateful operations
GenServer.call(__MODULE__, {:update, new_value})
```

## Tools to Use

- Use `:observer.start()` to visualize processes
- Use `:erlang.system_info(:process_count)` to check process count
- Use `Process.info(pid)` for process details

## Best Practices

- Clear separation between client API and server callbacks
- Use named processes for long-running services
- Avoid blocking handle_call callbacks
- Use handle_cast for fire-and-forget operations
- Document restart strategies and fault boundaries
- Separate OTP processes from business logic functions
