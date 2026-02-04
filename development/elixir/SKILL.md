---
name: elixir
description: Elixir programming
---

# Elixir Expertise

Comprehensive guidance on Elixir language, Phoenix framework, Ecto database
patterns, Ash framework, and OTP behaviors.

## Critical Code Style Guidelines

### Running Elixir Code and Testing

**ALWAYS use a scratch test file for testing code snippets - NEVER create new
files, use `mix run`, or use `iex` for quick tests:**

```elixir
# ✅ CORRECT - Use test/scratch_test.exs for all test scripts
# Create/update test/scratch_test.exs with your test code, then run:
mix test test/scratch_test.exs

# ❌ INCORRECT - Don't create new test files
mix test test/some_new_test.exs  # Creates clutter

# ❌ INCORRECT - Don't use mix run for testing
mix run scratch.exs  # Use test framework instead

# ❌ INCORRECT - Don't use iex for complex multi-line tests
iex -S mix  # Hard to iterate on multi-line code
```

**Scratch Test File Setup:**

1. **Create `test/scratch_test.exs`** (if it doesn't exist)
2. **Add to `.gitignore`**:
   ```
   # Scratch test file
   test/scratch_test.exs
   ```
3. **Use for all test scripts**:

   ```elixir
   # test/scratch_test.exs
   defmodule ScratchTest do
     use ExUnit.Case

     # Testing user creation
     test "create user" do
       alias MyApp.Accounts

       params = %{
         email: "test@example.com",
         name: "Test User"
       }

       case Accounts.create_user(params) do
         {:ok, user} ->
           IO.inspect(user, label: "Created user")
           assert user.email == "test@example.com"
         {:error, changeset} ->
           IO.inspect(changeset.errors, label: "Errors")
           flunk("User creation failed")
       end
     end
   end
   ```

4. **Run with**: `mix test test/scratch_test.exs`

**Benefits of scratch test file approach:**

- **Single file to manage**: Always know where test code lives
- **Git-ignored**: Never accidentally commit test code
- **Easy iteration**: Edit and re-run without file management
- **Test framework benefits**: Proper test isolation, helpers, and formatting
- **Database cleanup**: Automatic sandbox rollback between tests
- **Better output**: Clear pass/fail with detailed error messages
- **No cleanup needed**: Just overwrite for next test

**🚨 CRITICAL: This is the ONLY way to run test code**

- **NEVER use `iex -S mix`** - always use the scratch test file instead
- **NEVER use `mix run`** - always use the scratch test file instead
- **NEVER create temporary files** - always use the scratch test file instead
- For literally any code testing, exploration, or experimentation, use
  `test/scratch_test.exs` and run with `mix test test/scratch_test.exs`

### Pipe Operator Usage

**Use the pipe operator correctly based on the number of function calls:**

**Single Function Call - No Pipe:**

```elixir
# ✅ CORRECT - Direct function call for single operation
Enum.map(list, & &1 * 2)

# ❌ INCORRECT - Unnecessary pipe for single function
list
|> Enum.map(& &1 * 2)
```

**Multiple Function Calls - Use Pipe:**

```elixir
# ✅ CORRECT - Pipe chain for multiple operations
list
|> Enum.map(& &1 * 2)
|> Enum.filter(& rem(&1, 2) == 0)
|> Enum.sum()

# ❌ INCORRECT - Mixing direct calls with pipes
Enum.map(list, & &1 * 2)
|> Enum.filter(& rem(&1, 2) == 0)
```

## Phoenix/LiveView Guidelines

### LiveView Component Best Practices

**ALWAYS create a public wrapper function for LiveView components to enable
compile-time validation:**

```elixir
# ✅ CORRECT - Public wrapper function with attrs
defmodule MyAppWeb.Components.UserCard do
  use MyAppWeb, :live_component

  attr :user, :map, required: true
  attr :show_email, :boolean, default: false
  attr :class, :string, default: ""

  def user_card(assigns) do
    ~H"""
    <.live_component
      module={__MODULE__}
      id={"user-card-#{@user.id}"}
      user={@user}
      show_email={@show_email}
      class={@class}
    />
    """
  end

  # Component implementation
  def render(assigns) do
    ~H"""
    <div class={"user-card #{@class}"}>
      <h3><%= @user.name %></h3>
      <%= if @show_email do %>
        <p><%= @user.email %></p>
      <% end %>
    </div>
    """
  end
end

# Usage in parent component/view
<.user_card user={@current_user} show_email={true} />
```

**Why This Pattern:**

- **Compile-time validation**: Attrs are checked at compile time
- **Better IDE support**: Autocomplete and documentation for component props
- **Clear API**: Public function defines the component's interface
- **Type safety**: Can specify types and requirements for each attribute

**Component Wrapper Rules:**

1. **Always** define a public function that wraps `<.live_component>`
2. **Always** use `attr` declarations for all component props
3. **Always** mark required attributes with `required: true`
4. **Always** provide default values for optional attributes

## Ash Framework Guidelines

### Migrations with Ash

**ALWAYS use `mix ash.codegen` for creating migrations when working with Ash:**

```elixir
# ✅ CORRECT - Use ash.codegen for Ash resource migrations
mix ash.codegen initial_migration
mix ash.codegen add_users
mix ash.codegen update_products

# ❌ INCORRECT - Don't use ecto.gen.migration directly for Ash resources
mix ecto.gen.migration add_users  # Wrong for Ash projects!
```

**Why use `mix ash.codegen` for migrations:**

- **Automatic schema generation**: Creates migrations based on your Ash
  resources
- **Consistency**: Ensures migrations match your resource definitions
- **Relationships**: Properly handles associations and references
- **Constraints**: Includes all Ash-defined validations and constraints
- **Policies**: Considers security policies in migration structure

**Ash migration workflow:**

1. Define or update your Ash resources
2. Run `mix ash.codegen <migration_name>` to generate migration
3. Review the generated migration for accuracy
4. Run `mix ecto.migrate` to apply the migration

## Testing Guidelines

### Mimic Mocking Best Practices

**ALWAYS use `expect` instead of `stub` when mocking with Mimic:**

```elixir
# ✅ CORRECT - Use expect (will fail if not called)
expect(MyModule, :function_name, fn args ->
  {:ok, "response"}
end)

# ❌ INCORRECT - Don't use stub (allows unused mocks)
stub(MyModule, :function_name, fn args ->
  {:ok, "response"}
end)
```

**Why `expect` is preferred:**

- **Ensures mocks are actually needed**: Test fails if mock isn't called
- **Prevents dead mocks**: Avoids unused mocks that hide missing test coverage
- **Better test reliability**: Guarantees the mocked interaction actually
  happens
- **Cleaner test maintenance**: Unused mocks are automatically detected

### Test Setup Best Practices

**Only call the action under test - use generators for everything else:**

```elixir
# ✅ CORRECT - Use generators for setup, only call action under test
test "create guild with valid params" do
  # Setup using generators
  user = generate(user_generator())

  # Only action under test
  {:ok, guild} = Guilds.create_guild(user, %{name: "Test Guild"})

  assert guild.name == "Test Guild"
  assert guild.owner_id == user.id
end

# ❌ INCORRECT - Multiple actions called in test
test "create guild with valid params" do
  # Don't call multiple actions
  {:ok, user} = Users.create_user(%{name: "Test User"})  # Wrong!
  {:ok, guild} = Guilds.create_guild(user, %{name: "Test Guild"})

  assert guild.name == "Test Guild"
end
```

**Key Testing Principles:**

- **One action per test**: Each test should call exactly one action
- **Generators for setup**: Use `generate()` for all test data setup
- **No cascading actions**: Don't test multiple actions in sequence
- **Isolated testing**: Each test should be independent

## Elixir Language Fundamentals

### Pattern Matching

- Elixir's most powerful feature
- Use for destructuring, control flow, and function clauses
- Prefer pattern matching over conditionals when possible

### OTP Behaviors

- **GenServer**: State management and synchronous/asynchronous calls
- **GenStage**: Producer-consumer pipelines with backpressure
- **Supervisor**: Process supervision and fault tolerance
- **Application**: Application lifecycle and configuration

### Process Communication

- Message passing with `send` and `receive`
- Process linking and monitoring
- Task and Task.Supervisor for async work

## Ecto Patterns

### Schema Definitions

- Use embedded schemas for value objects
- Leverage changesets for validation
- Cast params before validation

### Query Composition

- Build queries incrementally with pipe operators
- Use named bindings for readability in complex queries
- Prefer Ecto.Query macros over raw SQL when possible

### Changesets

- Always use changesets for data validation
- Separate casting from validation
- Use custom validators for complex business rules

## Phoenix Conventions

### Context Boundaries

- Contexts define API boundaries
- Keep contexts focused on single responsibilities
- Don't expose Ecto queries/changesets outside contexts

### LiveView Patterns

- Mount for initial state setup
- Handle events for user interactions
- Use assigns for reactive updates
- Leverage PubSub for real-time updates

### Router Organization

- Group related routes under scopes
- Use pipelines for common middleware
- Leverage plug for request transformation

## Performance Considerations

### Process Usage

- Spawn processes for concurrent work
- Use Task for simple async operations
- Supervise long-running processes

### Memory Management

- Be aware of process memory isolation
- Use ETS for shared state when appropriate
- Monitor process mailbox sizes

### Database Optimization

- Use database indices appropriately
- Batch database operations when possible
- Leverage Ecto's preload for associations
