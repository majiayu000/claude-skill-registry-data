---
name: elixir-phoenix
description: Elixir and Phoenix development guidelines with critical language-specific gotchas. Use when writing Elixir code, Phoenix applications, or Mix tasks. Prevents common mistakes with list access, variable rebinding, struct access, and OTP patterns that cause subtle bugs or compilation errors.
---

# Elixir/Phoenix Guidelines

## Critical Elixir Gotchas

### List Access

Lists do NOT support index-based access syntax. Never use `list[i]`.

```elixir
# ❌ INVALID - will not compile
mylist = ["blue", "green"]
mylist[0]

# ✅ CORRECT
Enum.at(mylist, 0)
```

### Block Expression Rebinding

Variables are immutable but can be rebound. Block expressions (`if`, `case`, `cond`) must bind results externally:

```elixir
# ❌ INVALID - rebinding inside block has no effect outside
if connected?(socket) do
  socket = assign(socket, :val, val)
end

# ✅ CORRECT - bind the block result
socket =
  if connected?(socket) do
    assign(socket, :val, val)
  end
```

### Struct Access

Never use map access syntax on structs—they don't implement Access behaviour:

```elixir
# ❌ INVALID
changeset[:field]

# ✅ CORRECT
Ecto.Changeset.get_field(changeset, :field)
my_struct.field
```

### Module Nesting

Never nest multiple modules in the same file—causes cyclic dependencies and compilation errors.

## Naming Conventions

- Predicate functions: end with `?`, not `is_` prefix
  - `valid?` not `is_valid`
  - Reserve `is_thing` for guards only
- Avoid `String.to_atom/1` on user input (memory leak risk)

## OTP Patterns

Primitives like `DynamicSupervisor` and `Registry` require names in child specs:

```elixir
# In supervision tree
{DynamicSupervisor, name: MyApp.MyDynamicSup}

# Then use the name
DynamicSupervisor.start_child(MyApp.MyDynamicSup, child_spec)
```

## Concurrency

Use `Task.async_stream/3` for concurrent enumeration with back-pressure:

```elixir
collection
|> Task.async_stream(&process/1, timeout: :infinity)
|> Enum.to_list()
```

## Date/Time

Use standard library (`Time`, `Date`, `DateTime`, `Calendar`). Only add `date_time_parser` for parsing if needed.

## Mix Guidelines

- Read task docs first: `mix help task_name`
- Debug test failures: `mix test test/my_test.exs` or `mix test --failed`
- Avoid `mix deps.clean --all` unless absolutely necessary
