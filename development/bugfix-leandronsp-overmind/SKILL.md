---
name: bugfix
description: "Bug hunter. Reproduces bugs with failing tests (RED), then fixes with TDD. Accepts a prompt, issue URL, or bug description. Use when: bugfix, fix bug, debug, broken, regression, failing, doesn't work, fix this."
---

# Bugfix

Bug hunter. Reproduces the bug with a failing test, then fixes it with strict TDD. Focused and surgical.

## Usage

- `/bugfix` — asks what's broken
- `/bugfix <prompt>` — fix from description
- `/bugfix <url>` — fix from GitHub issue
- `/bugfix <path>` — fix from bug report file

## Workflow

### Phase 1: Understand the Bug

**No arguments:** Ask: "What's broken? Describe the bug, paste an issue URL, or point me to a report."

**Wait for the user's response.**

**Prompt:** Use as bug description.

**URL:** Fetch: `gh issue view <number> --json title,body --jq '.title + "\n\n" + .body'`

**File path:** Read the file.

Restate the bug:

> My understanding: {what's broken, when it happens, expected vs actual behavior}
>
> Is that right? Anything else I should know?

**Wait.** Confirm understanding before proceeding.

### Phase 2: Scout the Bug

Explore the codebase to understand the area where the bug lives:

- Read the relevant source files
- Read existing tests for that area
- Trace the data/control flow where the bug occurs
- Check git log for recent changes that might have introduced it

Report findings:

> Here's what I found:
>
> - **Where it happens:** {file(s), function(s), line(s)}
> - **Root cause hypothesis:** {what I think is wrong and why}
> - **Existing test coverage:** {what's tested, what's missing}
> - **Recent changes:** {any suspicious recent commits, or "nothing recent"}
>
> Does this match what you're seeing?

**Wait.** The user may have more context.

### Phase 3: Reproduce with a Failing Test

**This is the most important phase. Do not skip. Do not rush.**

Write a test that **fails right now** because of the bug. This test proves the bug exists.

Rules:
- It must fail for the **right reason** (the actual bug, not a setup error)
- It must be **minimal** — test only the broken behavior
- It must describe the **expected** behavior
- Name it clearly: `test "description of correct behavior that is currently broken"`
- Use `assert_receive` with monitors for async assertions, never `Process.sleep`

> Reproduction test:
>
> ```elixir
> {test_code}
> ```
>
> This proves: {what broken behavior it captures}
> Expected: {what should happen}
> Actual: {what happens now}
>
> Write it?

**Wait.** The user may adjust the test.

Write the test. Run it. **Confirm RED.**

```bash
mix test test/path/to/test_file.exs:LINE
```

> RED — {error message or assertion failure}

**If the test passes unexpectedly:** The test doesn't reproduce the bug. Investigate. Ask the user for help if stuck after 3 attempts.

### Phase 4: Fix (GREEN)

Write the **minimum code** to make the failing test pass. No more.

- Don't refactor unrelated code
- Don't add features
- Don't fix other bugs you find (note them for later)
- Stay surgical

Run tests. **Confirm GREEN.**

```bash
mix test test/path/to/test_file.exs:LINE
```

> GREEN — Bug fix verified.

### Phase 5: Check for Collateral

Run the full suite:

```bash
mix test
mix dialyzer
```

If other tests break: the fix introduced a regression. Adjust the fix.

> Full suite: {pass/fail}. {details if any breakage}

### Phase 6: Refactor (if needed)

Only if the fix is ugly or the area needs cleanup:
- Clean up, run tests, confirm GREEN
- Keep it minimal — this is a bugfix, not a rewrite

### Phase 7: Commit

Stage only the changed files. Commit with:

```
fix(<scope>): <what was fixed>
```

No Co-Authored-By. No AI mentions.

---

## Multiple Bugs

If the input describes multiple bugs:

1. List them
2. Ask the user which to tackle first
3. Fix one at a time, full cycle each
4. Commit each fix separately

---

## Iron Rules

1. **No fix without a failing test.** The test must prove the bug exists before you touch production code
2. **Persist on RED.** If you can't reproduce it in a test, dig deeper. Don't skip to the fix
3. **Minimum fix.** Smallest change that makes the test pass. No scope creep
4. **Run full suite.** `mix test && mix dialyzer`
5. **One bug at a time.** Don't batch
6. **Ask when stuck.** If you can't reproduce after 3 attempts, ask the user for more context
7. **Note but don't fix** other bugs you discover along the way
