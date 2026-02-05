---
name: elixir-verification-gate
description: MANDATORY verification before claiming anything works. Run actual commands, read actual output, provide evidence. Use when claiming tests pass, build succeeds, or code works.
---

# Elixir Verification Gate: Evidence or It Didn't Happen

## THE IRON LAW

**NEVER claim something works without running it and reading the output.**

Not "should work". Not "looks correct". Not "I think it passes".

**RUN IT. READ IT. PROVE IT.**

## ABSOLUTE REQUIREMENT

Before claiming ANY of the following, you MUST provide evidence:

### 1. "Tests pass"
**MUST run:** `mix test`
**MUST read:** Actual test output showing "X tests, 0 failures"
**MUST provide:** Exact output or test count

```bash
# Required evidence
$ mix test
..........

Finished in 0.3 seconds (0.1s async, 0.2s sync)
10 tests, 0 failures

# This is evidence ✓
```

### 2. "Code compiles"
**MUST run:** `mix compile --warnings-as-errors`
**MUST read:** Output showing "Compiled" or error messages
**MUST provide:** Confirmation of zero warnings

```bash
# Required evidence
$ mix compile --warnings-as-errors
Compiling 5 files (.ex)
Generated my_app app

# This is evidence ✓
```

### 3. "Code is formatted"
**MUST run:** `mix format --check-formatted`
**MUST read:** Output or lack thereof
**MUST provide:** Confirmation no files would be formatted

```bash
# Required evidence
$ mix format --check-formatted
# (no output means all files formatted)

# This is evidence ✓
```

### 4. "Credo passes"
**MUST run:** `mix credo --strict`
**MUST read:** Analysis results
**MUST provide:** Confirmation of "no issues found"

```bash
# Required evidence
$ mix credo --strict
Checking 42 source files...

Please report incorrect results: https://github.com/rrrene/credo/issues

Analysis took 0.3 seconds (0.2s to load, 0.1s running 100 checks on 42 files)
17 mods/funs, found no issues.

# This is evidence ✓
```

### 5. "Dialyzer passes"
**MUST run:** `mix dialyzer`
**MUST read:** Type checking results
**MUST provide:** "done (passed successfully)" message

```bash
# Required evidence
$ mix dialyzer
...
Total errors: 0, Skipped: 0, Unnecessary Skips: 0
done (passed successfully)

# This is evidence ✓
```

### 6. "Migration runs successfully"
**MUST run:** `mix ecto.migrate`
**MUST read:** Migration execution output
**MUST provide:** Confirmation migration completed

```bash
# Required evidence
$ mix ecto.migrate

15:42:13.456 [info] == Running 20231201150000 MyApp.Repo.Migrations.CreateUsers.change/0 forward

15:42:13.458 [info] create table users

15:42:13.478 [info] == Migrated 20231201150000 in 0.0s

# This is evidence ✓
```

### 7. "Function works correctly"
**MUST run:** Test that exercises the function
**MUST read:** Test output showing it passes
**MUST provide:** Example usage or test code

```elixir
# Required evidence
test "create_user/1 with valid attrs creates user" do
  attrs = %{name: "Alice", email: "alice@example.com"}
  assert {:ok, %User{} = user} = Accounts.create_user(attrs)
  assert user.name == "Alice"
  assert user.email == "alice@example.com"
end

# ✓ Test passes with actual run
```

### 8. "Issue is fixed"
**MUST run:** The command that revealed the issue
**MUST read:** Output showing issue no longer appears
**MUST provide:** Before/after comparison

```bash
# Required evidence - BEFORE
$ mix dialyzer
lib/my_app.ex:42:pattern_can_never_match
Total errors: 1

# Applied fix...

# Required evidence - AFTER
$ mix dialyzer
Total errors: 0, Skipped: 0, Unnecessary Skips: 0
done (passed successfully)

# This is evidence ✓
```

## BANNED PHRASES (Without Evidence)

These phrases are **BANNED** unless accompanied by actual command output:

❌ "The tests should pass"
❌ "This should compile"
❌ "I believe this works"
❌ "This looks correct"
❌ "The code appears to be working"
❌ "I think this fixes it"
❌ "This ought to work"
❌ "Assuming the tests pass"
❌ "If you run the tests, they'll pass"
❌ "The build will succeed"

**Instead, RUN THE COMMAND and report actual results.**

## VERIFICATION CHECKLIST

Before claiming you're done with ANY task:

- [ ] I ran the relevant commands (not just wrote code)
- [ ] I read the actual output (not assumed it worked)
- [ ] I saw success messages with my own eyes
- [ ] I can quote the exact output
- [ ] All tests actually pass (I ran them)
- [ ] Code actually compiles (I compiled it)
- [ ] No warnings exist (I checked)
- [ ] Quality checks actually pass (I ran them)

**If you can't check ALL boxes with evidence, you're not done.**

## EXAMPLES OF PROPER VERIFICATION

### Example 1: Claiming Tests Pass

**WRONG:**
```
I've implemented the create_user function. The tests should pass now.
```

**RIGHT:**
```
I've implemented the create_user function. Running tests:

$ mix test test/my_app/accounts_test.exs
..........

Finished in 0.2 seconds (0.1s async, 0.1s sync)
10 tests, 0 failures

✓ All tests pass.
```

### Example 2: Claiming Code Compiles

**WRONG:**
```
I've fixed the compilation error. It should compile now.
```

**RIGHT:**
```
I've fixed the compilation error. Compiling:

$ mix compile --warnings-as-errors
Compiling 1 file (.ex)
Generated my_app app

✓ Compiles with zero warnings.
```

### Example 3: Claiming Dialyzer Is Happy

**WRONG:**
```
I added the @spec. Dialyzer won't complain anymore.
```

**RIGHT:**
```
I added the @spec. Running Dialyzer:

$ mix dialyzer
Finding suitable PLTs
Checking PLT...
...
Total errors: 0, Skipped: 0, Unnecessary Skips: 0
done (passed successfully)

✓ Dialyzer passes with zero errors.
```

### Example 4: Claiming Migration Works

**WRONG:**
```
The migration is ready and should run fine.
```

**RIGHT:**
```
Running the migration:

$ mix ecto.migrate

15:42:13.456 [info] == Running 20231201150000 MyApp.Repo.Migrations.CreateUsers.change/0 forward
15:42:13.458 [info] create table users
15:42:13.478 [info] == Migrated 20231201150000 in 0.0s

✓ Migration executed successfully.
```

## WHEN VERIFICATION FAILS

If you run a command and it fails:

### DO NOT:
- Claim it works anyway
- Say "it should work, not sure why it's failing"
- Move on to other tasks
- Assume the failure is environmental

### INSTEAD:
1. **Read the error message completely**
2. **Understand what failed and why**
3. **Fix the actual problem**
4. **Run the command again**
5. **Verify it now passes**
6. **Provide evidence of success**

## VERIFICATION WORKFLOW

**For EVERY change you make:**

### 1. Make the change
```elixir
# Edit code
def create_user(attrs) do
  # ... implementation
end
```

### 2. Run the relevant test
```bash
$ mix test test/my_app/accounts_test.exs:42
.

Finished in 0.1 seconds
1 test, 0 failures
```

### 3. Run full test suite
```bash
$ mix test
..........

Finished in 0.3 seconds
10 tests, 0 failures
```

### 4. Run quality checks
```bash
$ mix format --check-formatted
$ mix credo --strict
$ mix dialyzer
```

### 5. Report results
```
✓ Tests pass (10/10)
✓ Code formatted
✓ Credo: no issues
✓ Dialyzer: 0 errors
```

**Only THEN can you claim the task is complete.**

## INTEGRATION WITH OTHER SKILLS

This skill works with:

- **elixir-tdd-enforcement** - Verify tests fail (RED), verify tests pass (GREEN)
- **elixir-no-shortcuts** - Verify error is gone (not suppressed)
- **elixir-root-cause-only** - Verify root cause is fixed (not symptom)

**Example TDD verification:**
```
1. Write test → RUN → See it fail ← VERIFICATION
2. Implement → RUN → See it pass ← VERIFICATION
3. Refactor → RUN → See it still passes ← VERIFICATION
```

## SPECIAL CASES

### "I can't run tests because..."
**STOP.** Fix the environment so you CAN run tests. Testing is non-negotiable.

### "The tests are flaky"
**STOP.** Fix the flakiness before proceeding. Flaky tests = broken tests.

### "Dialyzer takes too long"
**Run it anyway.** Cache the PLT. Use `mix dialyzer --incremental`. No shortcuts.

### "I'm just writing documentation"
**Still verify.** Run `mix docs` and confirm it generates without warnings.

### "It's just a comment change"
**Still verify.** Run `mix format --check-formatted` and ensure formatting is maintained.

## RATIONALIZATIONS THAT ARE WRONG

### "I don't need to run it, the code is obviously correct"
**WRONG.** Code is never obviously correct. Computers are precise. Run it.

### "I ran it locally yesterday, still works"
**WRONG.** Run it NOW, in THIS context, with THESE changes.

### "The CI will catch it"
**WRONG.** Catch it locally BEFORE pushing. CI is last resort, not primary check.

### "I'm confident this works"
**WRONG.** Confidence without evidence is just hope. RUN. THE. COMMAND.

### "Trust me, I know what I'm doing"
**WRONG.** Trust, but verify. Actually, just verify. Evidence > trust.

## CONSEQUENCES OF SKIPPING VERIFICATION

**If you claim something works without running it:**

1. **It probably doesn't work** - Murphy's Law applies
2. **You waste everyone's time** - Including your own
3. **Bugs reach production** - Because they weren't caught locally
4. **Team velocity drops** - Time spent debugging "working" code
5. **You lose credibility** - Claims without evidence are meaningless

**The 30 seconds "saved" by not running tests costs 30 minutes debugging later.**

## THE RULE

**Evidence or it didn't happen.**

**If you didn't run it, you don't know if it works.**

**If you can't quote the output, you didn't run it.**

## OUTPUT TEMPLATE

When verifying, use this template:

```markdown
## Verification Results

### Tests
$ mix test
[paste actual output]
✓ 10 tests, 0 failures

### Compilation
$ mix compile --warnings-as-errors
[paste actual output]
✓ Zero warnings

### Credo
$ mix credo --strict
[paste actual output]
✓ No issues found

### Dialyzer
$ mix dialyzer
[paste actual output]
✓ 0 errors

## Conclusion
All verification steps passed. Task complete.
```

## REMEMBER

> "Code doesn't work until you run it and prove it works."

> "Assumptions are the mother of all failures."

> "If you can't quote the output, you didn't verify it."

**RUN. READ. REPORT. Every. Single. Time.**
