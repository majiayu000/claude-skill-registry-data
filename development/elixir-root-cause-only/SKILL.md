---
name: elixir-root-cause-only
description: MANDATORY systematic debugging - trace to root cause before proposing fixes. NO random changes, NO symptom fixes, NO "try this". Use when debugging ANY error or issue.
---

# Elixir Root Cause Only: No Random Fixes

## THE IRON LAW

**NEVER fix symptoms. ALWAYS trace to the root cause.**

No guessing. No "try this". No random changes. No symptom fixes.

**TRACE. UNDERSTAND. FIX. VERIFY.**

## ABSOLUTE PROHIBITIONS

You are **NEVER** allowed to:

1. **Propose random fixes**
   - "Try adding this import"
   - "Maybe change this to that"
   - "Let's see if this works"
   - "Could you try restarting the server?"

2. **Fix where error appears**
   - Error appears in module A
   - Root cause is in module B
   - Don't just patch module A

3. **Make multiple changes at once**
   - Change A + B + C together
   - Now you don't know which one fixed it
   - Make ONE change, verify, repeat

4. **Skip understanding**
   - "I don't know why, but this fixes it"
   - If you don't know why, it's not fixed
   - Understanding is mandatory

5. **Accept "works on my machine"**
   - Reproducibility is required
   - Environmental differences matter
   - Document exact reproduction steps

## THE 4-PHASE DEBUGGING PROCESS

### Phase 1: REPRODUCE

**Objective:** Get consistent, repeatable reproduction.

```bash
# Required steps:
1. Identify exact steps to trigger the issue
2. Run those steps
3. Confirm issue appears
4. Document steps precisely
5. Verify it reproduces every time
```

**Output required:**
```markdown
## Reproduction Steps

1. Run `mix test test/my_app/accounts_test.exs:42`
2. Error appears: "undefined function User.changeset/2"
3. Reproduces 100% of the time
4. Environment: Elixir 1.15.7, OTP 26
```

**CHECKPOINT: Cannot proceed to Phase 2 until you have consistent reproduction.**

### Phase 2: TRACE

**Objective:** Follow the error back to its origin.

```bash
# Tracing questions:
1. What function fails?
2. What called that function?
3. What called THAT function?
4. Where did the bad data/state originate?
5. What's the first point where things went wrong?
```

**Tracing tools:**
```elixir
# 1. Add IO.inspect to see data flow
def create_user(attrs) do
  attrs
  |> IO.inspect(label: "Input attrs")
  |> User.changeset(%User{})
  |> IO.inspect(label: "Changeset")
  |> Repo.insert()
end

# 2. Use IEx.pry for interactive debugging
def create_user(attrs) do
  require IEx; IEx.pry()
  # Execution pauses here
  User.changeset(%User{}, attrs)
  |> Repo.insert()
end

# 3. Check the stack trace completely
** (UndefinedFunctionError) function User.changeset/2 is undefined
    (my_app 0.1.0) lib/my_app/accounts/user.ex:42: User.changeset/2
    (my_app 0.1.0) lib/my_app/accounts.ex:15: MyApp.Accounts.create_user/1
    test/my_app/accounts_test.exs:25: (test)
```

**Output required:**
```markdown
## Root Cause Trace

Error appears: lib/my_app/accounts.ex:15
Called from: test/my_app/accounts_test.exs:25
Root cause: lib/my_app/accounts/user.ex:42
Reason: User.changeset/2 is not defined (should be User.changeset/1)
```

**CHECKPOINT: Cannot proceed to Phase 3 until root cause is identified.**

### Phase 3: FIX

**Objective:** Fix the root cause, not the symptom.

```elixir
# BAD: Fix where error appears
# In accounts.ex
def create_user(attrs) do
  # Catch the error and work around it
  try do
    User.changeset(%User{}, attrs)
  rescue
    UndefinedFunctionError ->
      User.new_changeset(%User{}, attrs)  # Symptom fix!
  end
end

# GOOD: Fix the root cause
# In user.ex - fix the actual function definition
defmodule MyApp.Accounts.User do
  def changeset(user \\ %User{}, attrs) do  # ← Fixed arity
    user
    |> cast(attrs, [:name, :email])
    |> validate_required([:name, :email])
  end
end
```

**Output required:**
```markdown
## Fix Applied

Location: lib/my_app/accounts/user.ex:42
Change: Modified `changeset/2` to `changeset/1` with default parameter
Reason: Function was being called with 2 args but only defined with 1
```

**CHECKPOINT: Fix must address root cause, not symptom.**

### Phase 4: VERIFY

**Objective:** Prove the fix works and didn't break anything else.

```bash
# Required verification:
1. Run the failing test/command
2. Confirm it now passes
3. Run full test suite
4. Confirm no regressions
5. Document verification
```

**Output required:**
```markdown
## Verification

$ mix test test/my_app/accounts_test.exs:42
.
1 test, 0 failures ✓

$ mix test
..........
10 tests, 0 failures ✓

Root cause fixed, no regressions.
```

**CHECKPOINT: Cannot claim complete until verified.**

## EXAMPLES OF ROOT CAUSE TRACING

### Example 1: Dialyzer Type Error

**Error:**
```
lib/my_app/billing.ex:42:pattern_can_never_match
Pattern {:ok, amount} can never match type {:error, :invalid}
```

**WRONG approach (symptom fix):**
```elixir
# Just add to dialyzer.ignore
```

**RIGHT approach (root cause):**

**Phase 1 - Reproduce:**
```bash
$ mix dialyzer
# Error appears consistently
```

**Phase 2 - Trace:**
```elixir
# lib/my_app/billing.ex:42
def process_payment(user_id, amount) do
  case validate_amount(amount) do
    {:ok, amount} -> charge(user_id, amount)  # Line 42
    {:error, reason} -> {:error, reason}
  end
end

# Trace back to validate_amount/1
def validate_amount(amount) when amount > 0 do
  {:ok, amount}
end
def validate_amount(_amount) do
  {:error, :invalid}  # This is the only return value!
end
```

**Root cause:** `validate_amount/1` ALWAYS returns `{:error, :invalid}` for non-positive amounts, so the `{:ok, amount}` pattern can never match for the error case.

**Phase 3 - Fix:**
```elixir
# Fix the logic - validate_amount should return {:ok, amount} for valid amounts
def validate_amount(amount) when amount > 0 do
  {:ok, amount}
end
def validate_amount(_amount) do
  {:error, :invalid_amount}
end

# Or fix the pattern match to handle the actual return type
def process_payment(user_id, amount) do
  case validate_amount(amount) do
    {:ok, valid_amount} -> charge(user_id, valid_amount)
    {:error, :invalid_amount} -> {:error, :invalid_amount}
  end
end
```

**Phase 4 - Verify:**
```bash
$ mix dialyzer
Total errors: 0, Skipped: 0
done (passed successfully)
```

### Example 2: Test Failure

**Error:**
```
test create_user with valid attrs (MyApp.AccountsTest)
** (KeyError) key :email not found
```

**WRONG approach (symptom fix):**
```elixir
# Just add a default email
test "create_user with valid attrs" do
  attrs = Map.put(%{name: "Alice"}, :email, "default@example.com")
  # ...
end
```

**RIGHT approach (root cause):**

**Phase 1 - Reproduce:**
```bash
$ mix test test/my_app/accounts_test.exs:42
** (KeyError) key :email not found
```

**Phase 2 - Trace:**
```elixir
# Test code
test "create_user with valid attrs" do
  attrs = %{name: "Alice"}  # Missing :email
  assert {:ok, user} = Accounts.create_user(attrs)  # Fails here
end

# Trace to create_user
def create_user(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert()
end

# Trace to changeset
def changeset(user, attrs) do
  user
  |> cast(attrs, [:name, :email])
  |> validate_required([:name, :email])  # Requires :email!
  |> validate_format(:email, ~r/@/)      # Accesses attrs.email
end
```

**Root cause:** Test fixture doesn't include required :email field. The schema validation requires :email, but test attrs don't provide it.

**Phase 3 - Fix:**
```elixir
# Fix the test to provide required data
test "create_user with valid attrs" do
  attrs = %{name: "Alice", email: "alice@example.com"}
  assert {:ok, user} = Accounts.create_user(attrs)
  assert user.name == "Alice"
  assert user.email == "alice@example.com"
end

# OR if email shouldn't be required, fix the schema
def changeset(user, attrs) do
  user
  |> cast(attrs, [:name, :email])
  |> validate_required([:name])  # Email is optional
end
```

**Phase 4 - Verify:**
```bash
$ mix test test/my_app/accounts_test.exs:42
.
1 test, 0 failures
```

### Example 3: N+1 Query Issue

**Symptom:**
```
GET /users - 342ms (slow!)
```

**WRONG approach (symptom fix):**
```elixir
# Just add a cache
def list_users do
  Cachex.get_or_store(:users, fn ->
    Repo.all(User)
  end)
end
```

**RIGHT approach (root cause):**

**Phase 1 - Reproduce:**
```bash
# Enable query logging
config :logger, level: :debug

$ curl localhost:4000/users
# Logs show:
SELECT * FROM users
SELECT * FROM posts WHERE user_id = 1
SELECT * FROM posts WHERE user_id = 2
SELECT * FROM posts WHERE user_id = 3
# ... 100 queries total for 100 users
```

**Phase 2 - Trace:**
```elixir
# Controller
def index(conn, _params) do
  users = Accounts.list_users()
  render(conn, "index.html", users: users)
end

# View template
<%= for user <- @users do %>
  <div>
    <%= user.name %>
    Posts: <%= length(user.posts) %>  # ← N+1 trigger!
  </div>
<% end %>

# Context
def list_users do
  Repo.all(User)  # Doesn't preload posts
end
```

**Root cause:** View accesses `user.posts` which triggers a separate query for each user. The context doesn't preload the association.

**Phase 3 - Fix:**
```elixir
# Fix: Preload in the context
def list_users do
  User
  |> Repo.all()
  |> Repo.preload(:posts)
end
```

**Phase 4 - Verify:**
```bash
$ curl localhost:4000/users
# Logs show:
SELECT * FROM users
SELECT * FROM posts WHERE user_id IN (1, 2, 3, ..., 100)
# 2 queries instead of 101!

# Response time: 342ms → 45ms
```

## DEBUGGING TOOLS

### IEx.pry - Interactive debugging
```elixir
def create_user(attrs) do
  require IEx; IEx.pry()
  # Execution pauses, you can inspect:
  # > attrs
  # > User.__struct__()
  # > continue to proceed
  User.changeset(%User{}, attrs)
end
```

### IO.inspect - Data inspection
```elixir
def create_user(attrs) do
  attrs
  |> IO.inspect(label: "Raw attrs")
  |> Map.put(:inserted_at, DateTime.utc_now())
  |> IO.inspect(label: "With timestamp")
  |> User.changeset(%User{})
  |> IO.inspect(label: "Changeset")
end
```

### Logger - Production debugging
```elixir
require Logger

def create_user(attrs) do
  Logger.debug("Creating user with attrs: #{inspect(attrs)}")

  case User.changeset(%User{}, attrs) |> Repo.insert() do
    {:ok, user} ->
      Logger.info("User created: #{user.id}")
      {:ok, user}
    {:error, changeset} ->
      Logger.error("Failed to create user: #{inspect(changeset.errors)}")
      {:error, changeset}
  end
end
```

### Observer - System monitoring
```bash
# Start Observer GUI
iex -S mix
iex> :observer.start()

# Shows:
# - Process tree
# - Memory usage
# - Message queues
# - ETS tables
```

### Recon - Production tracing
```elixir
# Find slow processes
:recon.proc_window(:memory, 3, 1000)

# Trace function calls
:recon_trace.calls({MyApp.Accounts, :create_user, :return_trace}, 10)
```

## RATIONALIZATIONS THAT ARE WRONG

### "Let's just try this and see if it works"
**WRONG.** Random changes waste time. Trace to root cause first.

### "I'm 90% sure this is the fix"
**WRONG.** 90% sure = 10% broken. Get to 100% by tracing.

### "We can debug in production"
**WRONG.** Debug in development where you have full tools and can break things.

### "The error message is unclear"
**WRONG.** Error messages are precise. Read them completely and carefully.

### "It's probably a race condition"
**WRONG.** "Probably" means you haven't traced. Race conditions are reproducible with the right tools.

### "Let's change multiple things to be safe"
**WRONG.** Change ONE thing, verify, repeat. Multiple changes = confusion.

## BANNED PHRASES

❌ "Try this"
❌ "Maybe this will work"
❌ "Let's see if"
❌ "Could you try"
❌ "I think the issue is"
❌ "Just restart it"
❌ "Clear the cache"
❌ "It works on my machine"
❌ "I'm not sure why, but"
❌ "This is a Heisenbug"

**Instead:** Trace, understand, fix with certainty.

## SYSTEMATIC DEBUGGING CHECKLIST

Before proposing any fix:

- [ ] I can reproduce the issue consistently
- [ ] I have the exact error message
- [ ] I've read the entire stack trace
- [ ] I've traced from error to root cause
- [ ] I understand WHY the error occurs
- [ ] I know the FIRST place things went wrong
- [ ] My fix addresses the root cause (not symptom)
- [ ] I've verified the fix works
- [ ] I've verified no regressions
- [ ] I can explain the root cause clearly

**If you can't check ALL boxes, keep tracing.**

## THE RULE

**No fix without understanding.**

**No changes without tracing.**

**Root cause only. Always.**

## REMEMBER

> "The error appears where the problem is detected, not where it originates."

> "Symptoms are visible. Root causes must be traced."

> "Random fixes might work by accident. Understanding works on purpose."

**TRACE. UNDERSTAND. FIX. VERIFY.**
