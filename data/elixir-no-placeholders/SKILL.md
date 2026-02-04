---
name: elixir-no-placeholders
description: PROHIBITS placeholder code, default values that mask missing data, and silent failures. Enforces fail-fast with loud errors. Use when implementing ANY function or data structure.
---

# Elixir No Placeholders: Fail Loud, Fail Fast

## THE IRON LAW

**NEVER create placeholder code or provide defaults where there shouldn't be any.**

Silent failures are debugging nightmares. Loud failures save hours of troubleshooting.

**FAIL LOUD. FAIL FAST. FAIL OBVIOUSLY.**

## ABSOLUTE PROHIBITIONS

You are **NEVER** allowed to:

### 1. Create Placeholder Code

```elixir
# BAD: Placeholder implementations
def process_payment(_user_id, _amount) do
  # TODO: Implement this
  {:ok, %{}} # WRONG! Silent success with empty data
end

def send_email(_to, _subject, _body) do
  :ok  # WRONG! Pretends to work but does nothing
end

def validate_user(_attrs) do
  {:ok, attrs}  # WRONG! Bypasses validation
end

# GOOD: Explicit not implemented
def process_payment(_user_id, _amount) do
  raise "process_payment/2 not yet implemented"
end

# OR use @impl with proper error
@impl true
def handle_call({:process_payment, user_id, amount}, _from, state) do
  {:stop, {:error, :not_implemented}, state}
end
```

### 2. Provide Default Values That Hide Missing Data

```elixir
# BAD: Default values masking missing required data
defmodule User do
  schema "users" do
    field :email, :string, default: "unknown@example.com"  # WRONG!
    field :name, :string, default: "Unknown User"          # WRONG!
    field :role, :string, default: "user"                  # Maybe OK if truly optional
  end
end

# GOOD: No defaults for required fields
defmodule User do
  schema "users" do
    field :email, :string  # Required - no default
    field :name, :string   # Required - no default
    field :role, :string, default: "user"  # OK - has sensible default meaning
  end

  def changeset(user, attrs) do
    user
    |> cast(attrs, [:email, :name, :role])
    |> validate_required([:email, :name])  # Explicit requirements
  end
end
```

### 3. Silent Fallbacks in Pattern Matching

```elixir
# BAD: Catch-all that hides problems
def handle_result({:ok, data}), do: process(data)
def handle_result({:error, reason}), do: log_error(reason)
def handle_result(_anything_else), do: :ok  # WRONG! Silent success

# GOOD: Explicit handling, crash on unexpected
def handle_result({:ok, data}), do: process(data)
def handle_result({:error, reason}), do: {:error, reason}
# No catch-all - crashes loudly if unexpected input

# OR explicit error if you must handle it
def handle_result(unexpected) do
  raise ArgumentError, "Expected {:ok, data} or {:error, reason}, got: #{inspect(unexpected)}"
end
```

### 4. Empty Data Structures as Fallbacks

```elixir
# BAD: Return empty instead of error
def get_user_posts(user_id) do
  case Repo.get(User, user_id) do
    nil -> []  # WRONG! Silent "no posts" vs "user doesn't exist"
    user -> Repo.preload(user, :posts).posts
  end
end

# GOOD: Explicit error for missing user
def get_user_posts(user_id) do
  user = Repo.get!(User, user_id)  # Crashes if user missing
  Repo.preload(user, :posts).posts
end

# OR return proper error tuple
def get_user_posts(user_id) do
  case Repo.get(User, user_id) do
    nil -> {:error, :user_not_found}
    user -> {:ok, Repo.preload(user, :posts).posts}
  end
end
```

### 5. Try/Rescue That Silences Errors

```elixir
# BAD: Catch and return default
def parse_date(date_string) do
  try do
    Date.from_iso8601!(date_string)
  rescue
    _ -> ~D[2000-01-01]  # WRONG! Why this date? Masks parsing errors
  end
end

# GOOD: Let it crash or return error
def parse_date(date_string) do
  Date.from_iso8601!(date_string)  # Crashes with clear error
end

# OR return explicit error
def parse_date(date_string) do
  case Date.from_iso8601(date_string) do
    {:ok, date} -> {:ok, date}
    {:error, reason} -> {:error, {:invalid_date, reason}}
  end
end
```

### 6. Map.get/3 With Default for Required Keys

```elixir
# BAD: Default hides missing required keys
def create_user(attrs) do
  email = Map.get(attrs, :email, "unknown@example.com")  # WRONG!
  name = Map.get(attrs, :name, "Unknown")                # WRONG!
  User.changeset(%User{}, %{email: email, name: name})
end

# GOOD: Let it crash if key missing
def create_user(attrs) do
  # Will raise KeyError if :email or :name missing - GOOD!
  %{email: email, name: name} = attrs
  User.changeset(%User{}, %{email: email, name: name})
end

# OR explicit error
def create_user(attrs) do
  with {:ok, email} <- Map.fetch(attrs, :email),
       {:ok, name} <- Map.fetch(attrs, :name) do
    User.changeset(%User{}, %{email: email, name: name})
  else
    :error -> {:error, :missing_required_fields}
  end
end
```

### 7. Config With Silent Fallbacks

```elixir
# BAD: Default config hides missing env vars
def api_key do
  System.get_env("API_KEY") || "default_key_12345"  # WRONG!
end

def database_url do
  System.get_env("DATABASE_URL") || "localhost"  # WRONG!
end

# GOOD: Crash if required env var missing
def api_key do
  System.fetch_env!("API_KEY")  # Crashes if missing
end

def database_url do
  System.get_env("DATABASE_URL") ||
    raise "DATABASE_URL environment variable is required"
end
```

## WHEN DEFAULTS ARE ACCEPTABLE

Defaults are OK when they have **semantic meaning**, not just placeholders:

### Acceptable Defaults

```elixir
# OK: Default has actual business meaning
defmodule Post do
  schema "posts" do
    field :status, :string, default: "draft"        # OK: New posts are drafts
    field :published, :boolean, default: false      # OK: Unpublished by default
    field :view_count, :integer, default: 0         # OK: No views initially
    field :featured, :boolean, default: false       # OK: Not featured by default
  end
end

# OK: Optional fields with sensible defaults
def create_user(email, name, opts \\ []) do
  role = Keyword.get(opts, :role, "user")          # OK: "user" is sensible default
  locale = Keyword.get(opts, :locale, "en")        # OK: "en" is sensible default
  %User{email: email, name: name, role: role, locale: locale}
end

# OK: Pagination defaults
def list_users(opts \\ []) do
  page = Keyword.get(opts, :page, 1)               # OK: Page 1 is sensible start
  per_page = Keyword.get(opts, :per_page, 20)      # OK: 20 is sensible page size

  User
  |> limit(^per_page)
  |> offset(^((page - 1) * per_page))
  |> Repo.all()
end
```

### Unacceptable Defaults (Placeholders)

```elixir
# WRONG: Default hides missing required data
field :email, :string, default: "unknown@example.com"     # User email is required!
field :stripe_customer_id, :string, default: "cus_xxxxx"  # Payment ID required!
field :api_token, :string, default: "token123"            # Security credential!

# WRONG: Default bypasses validation
def validate_amount(amount) do
  amount || 0  # If amount is nil, use 0 - WRONG!
end

# WRONG: Default hides configuration errors
api_endpoint = System.get_env("API_ENDPOINT") || "http://localhost"  # Production will break!
```

## DETECTION CHECKLIST

Before writing ANY default value, ask:

1. **Is this data actually optional?** → If no, don't provide default
2. **Does this default have semantic meaning?** → If no, don't provide default
3. **Would I rather know immediately if this is missing?** → If yes, don't provide default
4. **Could this default hide a bug?** → If yes, don't provide default
5. **Is this a configuration value?** → If yes, crash if missing

**If in doubt, NO DEFAULT. Let it crash.**

## FAIL LOUD PATTERNS

### Pattern 1: Let It Crash

```elixir
# Prefer this
def process_order(order_id) do
  order = Repo.get!(Order, order_id)  # ! version crashes if not found
  Repo.preload(order, :items)
end

# Over this
def process_order(order_id) do
  case Repo.get(Order, order_id) do
    nil -> %Order{}  # WRONG! Fake order with no data
    order -> Repo.preload(order, :items)
  end
end
```

### Pattern 2: Explicit Errors

```elixir
# When you need to handle missing data
def find_user(id) do
  case Repo.get(User, id) do
    nil -> {:error, :user_not_found}       # Explicit error
    user -> {:ok, user}                     # Explicit success
  end
end

# Not this
def find_user(id) do
  Repo.get(User, id) || %User{}  # WRONG! Fake user
end
```

### Pattern 3: Required Keys

```elixir
# Use pattern matching to enforce required keys
def create_notification(%{user_id: user_id, message: message} = attrs) do
  # Will crash with clear error if user_id or message missing
  %Notification{user_id: user_id, message: message}
end

# Not this
def create_notification(attrs) do
  user_id = attrs[:user_id] || 1       # WRONG! Who is user 1?
  message = attrs[:message] || "N/A"   # WRONG! Useless notification
  %Notification{user_id: user_id, message: message}
end
```

### Pattern 4: Config Required

```elixir
# In config/runtime.exs
config :my_app, MyApp.Mailer,
  adapter: Swoosh.Adapters.Sendgrid,
  api_key: System.fetch_env!("SENDGRID_API_KEY")  # Crashes if missing

# Not this
config :my_app, MyApp.Mailer,
  adapter: Swoosh.Adapters.Sendgrid,
  api_key: System.get_env("SENDGRID_API_KEY") || "default"  # WRONG!
```

## DEBUGGING BENEFITS

**With placeholders and defaults:**
```
User registration succeeds ✓
Email notification "sent" ✓
Database shows: user.email = "unknown@example.com"
Customer: "I never received my confirmation email!"
Developer: "Oh, the email was actually 'unknown@example.com' all along..."
Debugging time: 2 hours to trace through logs
```

**Without placeholders (fail loud):**
```
User registration fails ✗
Error: "Required key :email not found in params"
Developer: "Email field is missing from the form"
Debugging time: 2 minutes to add email field
```

## EXAMPLES FROM REAL DEBUGGING NIGHTMARES

### Example 1: Silent Payment Failure

```elixir
# BAD: Silent failure with placeholder
def charge_customer(amount) do
  stripe_customer_id = get_stripe_id() || "cus_placeholder"  # WRONG!

  case Stripe.charge(stripe_customer_id, amount) do
    {:ok, charge} -> {:ok, charge}
    {:error, _} -> {:ok, %{id: "ch_placeholder", status: "succeeded"}}  # WRONG!
  end
end

# Result: Database shows successful charge, customer never charged, debugging takes days

# GOOD: Fail loud
def charge_customer(amount) do
  stripe_customer_id = get_stripe_id!()  # Crashes if missing

  case Stripe.charge(stripe_customer_id, amount) do
    {:ok, charge} -> {:ok, charge}
    {:error, reason} -> {:error, reason}  # Explicit error
  end
end

# Result: Error appears immediately, fix in 5 minutes
```

### Example 2: Default Hiding Configuration Error

```elixir
# BAD: Default hides missing config
defmodule MyApp.EmailClient do
  def send(to, subject, body) do
    api_key = System.get_env("EMAIL_API_KEY") || "test_key_123"  # WRONG!
    # Works in development, fails silently in production
    ThirdPartyMailer.send(api_key, to, subject, body)
  end
end

# GOOD: Crash early
defmodule MyApp.EmailClient do
  def send(to, subject, body) do
    api_key = System.fetch_env!("EMAIL_API_KEY")  # Crashes at startup
    ThirdPartyMailer.send(api_key, to, subject, body)
  end
end
```

### Example 3: Empty List Hiding Database Issue

```elixir
# BAD: Empty list hides query error
def user_orders(user_id) do
  try do
    Repo.all(from o in Order, where: o.user_id == ^user_id)
  rescue
    _ -> []  # WRONG! Query error looks like "no orders"
  end
end

# GOOD: Let database errors surface
def user_orders(user_id) do
  Repo.all(from o in Order, where: o.user_id == ^user_id)
  # If query fails, error is obvious and immediate
end
```

## RATIONALIZATIONS THAT ARE WRONG

### "I'll add a TODO and fix it later"
**WRONG.** TODOs with placeholder code never get fixed. Write raise "not implemented" instead.

### "This is just for development/testing"
**WRONG.** Development placeholders leak to production. Be explicit from the start.

### "I need something to make the tests pass"
**WRONG.** Tests passing with placeholder data proves nothing. Write proper fixtures.

### "The default value is harmless"
**WRONG.** Default values mask bugs. There's no such thing as a harmless default for required data.

### "It's easier to provide a default than handle the error"
**WRONG.** Easier now = debugging nightmare later. Fail loud, fix fast.

### "This makes the API more flexible"
**WRONG.** Required data that's "optional" isn't flexibility, it's ambiguity.

## THE RULE

**Required data should be required. Missing data should crash.**

**If it's optional, document WHY and what the default MEANS.**

**Placeholders are lies. Defaults without meaning are bugs waiting to happen.**

## ENFORCEMENT CHECKLIST

Before providing ANY default value:

- [ ] Is this data truly optional in the business domain?
- [ ] Does this default have clear semantic meaning?
- [ ] Have I documented what this default represents?
- [ ] Would failing loudly here save debugging time?
- [ ] Could this default hide a bug or misconfiguration?

**If you can't clearly explain WHY a default exists and WHAT it means, DON'T USE IT.**

## REMEMBER

> "Silent failures waste hours. Loud failures save hours."

> "A crash in development prevents a bug in production."

> "Defaults should have meaning, not just placeholders to avoid errors."

> "If data is required, make it required. If it's missing, crash."

**FAIL LOUD. FAIL FAST. FAIL OBVIOUSLY.**
