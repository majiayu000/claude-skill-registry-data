---
name: elixir-no-shortcuts
description: BLOCKS shortcuts like modifying dialyzer.ignore or .credo.exs excludes. Enforces fixing actual problems. Use when encountering ANY error, warning, or quality tool complaint.
---

# Elixir No Shortcuts: Fix the Real Problem

## THE IRON LAW

**NEVER suppress errors. ALWAYS fix the root cause.**

## ABSOLUTE PROHIBITIONS

You are **NEVER** allowed to:

1. **Add to dialyzer.ignore**
   - Not for "unknown function" errors
   - Not for "pattern can never match" warnings
   - Not for "no local return" issues
   - Not even "temporarily"

2. **Modify .credo.exs to disable checks**
   - Not adding to `disabled:` list
   - Not adding to `excluded_paths:`
   - Not using inline `# credo:disable-for-this-file`
   - Not raising complexity limits

3. **Suppress compiler warnings**
   - Not with `@compile {:no_warn_undefined, Module}`
   - Not with `# noqa` style comments
   - Not by removing `--warnings-as-errors`

4. **Modify .gitignore to hide problems**
   - Not to hide accidentally created files
   - Not to ignore build artifacts in wrong places
   - Fix the process that created them

5. **Comment out failing tests**
   - Not "just for now"
   - Not "until we figure it out"
   - Fix the test or fix the code

6. **Skip quality checks**
   - Not removing from pre-commit hook
   - Not skipping with `--no-verify`
   - Not disabling in CI/CD

## INSTEAD: FIX THE ACTUAL PROBLEM

### Dialyzer Errors

**When Dialyzer complains:**

```elixir
# BAD: Adding to dialyzer.ignore
# dialyzer.ignore
lib/my_app/accounts.ex:42:pattern_can_never_match

# GOOD: Fix with proper @spec
defmodule MyApp.Accounts do
  @spec get_user(integer()) :: {:ok, User.t()} | {:error, :not_found}
  def get_user(id) do
    case Repo.get(User, id) do
      nil -> {:error, :not_found}
      user -> {:ok, user}
    end
  end
end
```

**Common Dialyzer fixes:**

1. **Unknown function** - Add @spec or import the module
2. **Pattern can never match** - Fix the actual pattern mismatch
3. **No local return** - Add error handling paths
4. **Invalid type specification** - Correct the @spec to match reality

**Process:**
1. Read the full Dialyzer error (don't just scan it)
2. Understand what Dialyzer is telling you
3. Add @spec that matches what the function actually does
4. If function behavior is wrong, fix the function
5. Run `mix dialyzer` again to verify

### Credo Warnings

**When Credo complains:**

```elixir
# BAD: Adding to .credo.exs
{Credo.Check.Refactor.CyclomaticComplexity, max_complexity: 20}

# GOOD: Refactor to reduce complexity
# Before: Complex conditional logic
def process(data, opts) do
  if opts[:validate] and opts[:transform] and not opts[:skip] do
    # ... 50 lines of nested logic
  end
end

# After: Extract functions
def process(data, opts) do
  data
  |> maybe_validate(opts)
  |> maybe_transform(opts)
  |> finalize()
end

defp maybe_validate(data, %{validate: true}), do: validate(data)
defp maybe_validate(data, _opts), do: data
```

**Common Credo fixes:**

1. **High complexity** - Extract functions, use pipelines
2. **Long functions** - Break into smaller, focused functions
3. **Nesting too deep** - Use early returns, with statements, or guard clauses
4. **Modules too long** - Split into multiple focused modules
5. **Design anti-patterns** - Refactor following Elixir idioms

**Process:**
1. Read WHY Credo is warning
2. Understand the code smell it detected
3. Refactor to eliminate the smell
4. Run `mix credo --strict` to verify

### Compiler Warnings

**When compiler warns:**

```elixir
# BAD: Suppressing warning
@compile {:no_warn_undefined, SomeModule}

# GOOD: Fix the actual issue
# If function doesn't exist - implement it
# If module doesn't exist - add dependency
# If typo - fix the typo
```

### Test Failures

**When tests fail:**

```elixir
# BAD: Commenting out test
# test "user can login" do
#   # This is broken, will fix later
# end

# GOOD: Fix the test or the code
test "user can login" do
  user = fixture(:user)
  assert {:ok, session} = Accounts.authenticate(user.email, "password")
  assert session.user_id == user.id
end
```

## DETECTION CHECKLIST

**Before making ANY file modification, ask:**

1. **Am I about to modify a `.ignore` file?** → STOP
2. **Am I about to add to an `excluded:` or `disabled:` list?** → STOP
3. **Am I about to comment out code to make errors go away?** → STOP
4. **Am I about to skip a quality check?** → STOP
5. **Am I about to suppress a warning?** → STOP

**If ANY answer is YES → Use this skill to fix the real problem.**

## BANNED PHRASES

If you're about to say ANY of these phrases, **STOP IMMEDIATELY** and use this skill:

❌ "This is a minor warning"
❌ "This will be implemented later"
❌ "It's not related to MY changes"
❌ "These warnings are safe to ignore"
❌ "I'll add a TODO and come back to it"
❌ "This is a false positive"
❌ "The code works fine, the tool is being pedantic"
❌ "Adding to ignore is just for this one case"
❌ "This function is too complex to refactor right now"
❌ "Let's just disable this check for now"

**Instead:** Fix the actual problem. Now. While context is fresh.

## THE DEBUGGING PROCESS

When you encounter an error:

### Step 1: READ THE ERROR COMPLETELY
- Don't scan - read every word
- Note the file, line, and exact message
- Understand what tool is complaining and why

### Step 2: UNDERSTAND THE ROOT CAUSE
- Why is this happening?
- What is the code actually doing vs. what it should do?
- What does the tool want me to fix?

### Step 3: FIX THE CODE
- Add missing @spec annotations
- Refactor complex functions
- Fix pattern matching
- Add error handling
- Implement missing functions

### Step 4: VERIFY THE FIX
- Run the tool again
- See the error is GONE (not suppressed)
- All tests still pass

## RATIONALIZATIONS THAT ARE WRONG

### "This is a false positive from the tool"
**WRONG.** The tool is almost always right. If you think it's wrong, you've misunderstood either:
- What your code does
- What the tool is checking
- The Elixir/Erlang semantics

### "I'll fix this later, just need to move forward"
**WRONG.** "Later" never comes. Fix it now while context is fresh.

### "The code works fine, Dialyzer is just being pedantic"
**WRONG.** Dialyzer found a type inconsistency. Your code might work NOW, but it's brittle and will break when circumstances change.

### "This function is too complex to refactor right now"
**WRONG.** If it's too complex to refactor, it's too complex to maintain. Refactor it now or suffer forever.

### "Adding to ignore is just for this one case"
**WRONG.** Once you start ignoring, you never stop. The ignore file grows and grows. Fix. The. Code.

### "The test is flaky, I'll just comment it out"
**WRONG.** Flaky tests indicate real problems (race conditions, improper setup/teardown, environmental dependencies). Fix the flakiness.

### "This is minor warning"
**WRONG.** No warning is minor. Every warning is the compiler/tool trying to tell you something important. "Minor" warnings become major bugs in production.

### "This will be implemented later"
**WRONG.** This is TODO hell. Either implement it NOW or don't write the code at all. Placeholder implementations with "TODO: implement later" never get implemented - they become permanent technical debt.

### "It's not related to MY changes"
**WRONG.** You touched the code, you own it. The warning appeared on your watch - fix it. "Not my problem" attitude leads to rotting codebases. Leave the code better than you found it.

### "These warnings are safe to ignore"
**WRONG.** There is no such thing as a "safe to ignore" warning. If a warning was truly safe to ignore, the tool wouldn't emit it. Every warning has a reason - understand it and fix the code.

## CONSEQUENCES OF TAKING SHORTCUTS

**If you suppress instead of fix:**

1. **Technical debt accumulates** - Future you will hate past you
2. **Real bugs hide** - The error was trying to tell you something
3. **Code quality degrades** - Broken windows theory in action
4. **Team velocity slows** - Every shortcut makes next feature harder
5. **Production failures increase** - Suppressed warnings become runtime errors

**The 5 minutes "saved" by adding to ignore costs 5 hours in debugging later.**

## ENFORCEMENT

**Before modifying ANY of these files, you MUST use this skill:**

- `dialyzer.ignore`
- `.credo.exs` (specifically `disabled:` or `excluded_paths:` sections)
- Any file containing quality check configuration
- `.gitignore` (when hiding problems vs. proper ignore patterns)
- Test files (when commenting out failing tests)

**If you find yourself typing "add to ignore", STOP and fix the real issue.**

## EXAMPLES OF PROPER FIXES

### Example 1: Dialyzer Unknown Function

```elixir
# Error: Function MyApp.Repo.get/2 is undefined or private

# BAD: Add to dialyzer.ignore
# GOOD: Add proper typing
defmodule MyApp.Accounts do
  alias MyApp.Repo
  alias MyApp.Accounts.User

  @spec get_user(integer()) :: User.t() | nil
  def get_user(id) do
    Repo.get(User, id)
  end
end
```

### Example 2: Credo Complexity Warning

```elixir
# Warning: Cyclomatic complexity is 15 (max is 9)

# BAD: Raise max_complexity to 20
# GOOD: Refactor into pipeline
def process_order(order, user, opts) do
  order
  |> validate_order()
  |> check_inventory()
  |> apply_discounts(user)
  |> calculate_shipping(opts)
  |> finalize_order()
end
```

### Example 3: Pattern Match Warning

```elixir
# Warning: Pattern can never match

# BAD: Add to dialyzer.ignore
# GOOD: Fix the pattern
# Before:
def handle_result({:ok, data}), do: process(data)
def handle_result(:ok), do: :ok  # This can never match!

# After:
def handle_result({:ok, data}), do: process(data)
def handle_result({:error, reason}), do: {:error, reason}
```

## THE RULE

**If a quality tool complains, it's trying to help you write better code.**

**Listen to it. Fix the code. Don't silence the messenger.**

## REMEMBER

> "Every time you add to an ignore file, a production bug gets its wings."

> "Technical debt isn't free - you pay interest every single day."

> "Fix the code, not the tooling."

> "Minor warnings become major bugs. 'Later' means never. 'Not my changes' means rotting codebase."

> "You touched it, you own it. Leave the code better than you found it."
