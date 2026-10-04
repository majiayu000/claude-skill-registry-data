---
name: srp
description: >-
  v1.0.11 — Use whenever writing or editing Python (or other) code: enforce
  single-responsibility functions and methods. Apply on every coding task,
  including small scripts and new files from scratch.
---

# Single responsibility

Write code as single-responsibility functions/methods.

Before the first source write, identify the raw-command parser, the operation
owner(s) for the current capability, and the public dispatcher. Implement that
separation in the initial working slice. Do not first draft a complete operation
in the entrypoint and plan to extract it after testing or in a later commit.
A helper that only formats output, converts one token, or records history does
not extract the operation that computes or mutates the value.

Before each commit, read the public entrypoint itself and locate its call to
the raw-command parser and its calls to the current operation owners. Move any
remaining raw-string manipulation, aggregate calculation, state mutation or
state-dependent validation into its responsible helper before committing.
Adding a later helper elsewhere in the file does not repair work still left
in the entrypoint. Simple state reads and format guards retain the narrow
allowances below; this check does not require pass-through wrappers.


- **Parsing lives in its own helper(s).** Every `strip()`, `split()`,
  `startswith()`, `partition()`, slice, or regex on the raw command belongs
  there, and one parse helper covers **every** command variant — never parse
  most commands in the helper and one special case (`bye`, `period`) inline.
- **Core logic lives in its own helper(s).** Arithmetic, state updates, and
  business conversions, and domain validation belong to helpers, which may
  return a one-line formatted result. For a bank, checking whether an amount
  is negative is part of the deposit/withdraw/transfer operation: do that in
  its operation helper, after dispatch. `int()` / `float()` of an
  already-split token is not a business conversion.
- **State-dependent validation is operation logic.** Resource existence,
  uniqueness, available balance, and other domain constraints belong inside
  the helper that owns the operation. Do not check them in the entrypoint
  before calling the helper; dispatch may check only command/argument shape
  and the format guards below.
- **The public entrypoint stays thin: parse → call helpers → return/format.**
  It hands the raw command to the parse helper in a single call before it
  branches on anything, then dispatches only on what the helper returned. It
  never takes the raw string apart, never increments or updates state, and
  never builds a computed result literal (`f"hello={name}"`) — that string
  belongs to the helper that owns the value.
- **A converted token is passed on, never worked on.** `helper(int(token))` is
  thin; so is `value = int(token); helper(value)` when the local value is passed
  unchanged. Arithmetic or state-dependent work on that value in the entrypoint
  is core logic and belongs in
  the helper: no offset or other arithmetic on it
  (`index = int(token) - 1`), no comparison against current state to validate
  it, and above all no assignment into state
  (`_total = int(token)`). Hand the raw converted value over
  (`helper(int(token))`) and let the helper apply the offset, check its domain range,
  and store the result — a command that replaces state needs its own helper
  exactly like one that increments it.
- **These belong in the entrypoint or a core helper, not a new function:**
  if/elif dispatch, raises for an unknown operation or extra/missing
  arguments, and simple input-shape or format guards on an already-parsed
  value (for example, a clock hour outside 0..23),
  `helper(int(token))`, and a one-line format or read of existing state
  (`str(state)`, `f"value={state}"`, `state if operation == "get" else
  helper(...)`). Do not require `get` to go through a helper. A format guard
  checks whether input is representable, not whether the operation accepts it:
  a narrower business interval within a valid format range belongs in the
  operation helper. Do not reject an operation's disallowed hours or other
  domain values in the entrypoint under the format-guard allowance.
  Successful numeric conversion only establishes that the token can be
  represented. Whether that value is acceptable to an operation, including
  finite-only, sign, or magnitude rules, is domain validation in the
  operation helper. Pass the converted value there unchanged.
- **Each command owns its own helper, amount, and label.** Do not collapse two
  commands into one parameterized helper by computing the difference in the
  entrypoint. Branching on the parsed command to call `_deposit(...)` or
  `_withdraw(...)` is ordinary dispatch; choosing `+1`/`-1` or `up`/`down`
  in the entrypoint as arguments to one shared helper is core work:

  ```python
  amount = 1 if operation == "inc" else -1          # arithmetic mapping, and
  prefix = "up" if operation == "inc" else "down"   # label, both left in
  result = _change_counter(amount, prefix)          # the entrypoint
  ```

  Instead `_increment()` returns `f"up={_counter}"`, `_decrement()` returns
  `f"down={_counter}"`, and the entrypoint only dispatches:
  `result = _increment() if operation == "inc" else _decrement()`. Two helpers
  sharing a private one-line updater are fine.
- Do not leave parsing and core logic mixed in one monolithic function body.
- Before committing, inspect each entrypoint comparison or raise involving a
  parsed value. Command shape and universal format validity may stay there;
  choosing a result category or rejecting a narrower operation-specific
  range belongs in the operation helper. A helper that only formats a category
  already chosen by the entrypoint has not extracted that core logic.
- Logging prints are a separate skill; they never merge responsibilities.
  When a logging skill applies, the entry `print(...)` is still the first
  statement and the parse-helper call comes after it — printing is not
  parsing, so both rules hold.

## Establish responsibilities in the current slice

The first capability already needs a parse helper, its operation helper(s), and
an entrypoint that delegates to them. A single command, a short function, or a
simple greeting/conversion does not exempt raw-command parsing or computed
output from these boundaries. When fixing an existing program, inspect its
entrypoint too: extract existing mixed parsing and core work as part of the
current repair, preserving the public signature and earlier behavior. Do not
leave the original command monolithic while giving only new commands helpers,
or defer the extraction to a later capability or final cleanup.

## Reduce churn while modifying code

Before editing, identify the requested behavior, its current owner, and the
callers and checks that depend on it. Change that owner and its necessary
integration points; preserve working behavior outside the request.

- Keep existing names, signatures, file locations, and conventions when they
  still fit. Avoid unrelated renaming, reordering, formatting, or rewriting
  working functions merely to make the new code look uniform.
- Extend the existing parsing and dispatch path for a new command variant.
  Do not add a parallel parser or copy a working operation into a second
  implementation that will drift from the original.
- When a function acquires a second responsibility, extract that responsibility
  and update its callers. A local extraction may touch several files; prefer
  that justified change over a tiny patch that leaves mixed responsibilities,
  duplicated logic, or another special case.
- Add helpers for a clear responsibility or actual reuse. Avoid speculative
  frameworks, pass-through layers, and broad reorganizations for hypothetical
  future requirements. Simple functions may share a small private helper.
- Check changed behavior and representative earlier behavior through the public
  entrypoint. Update expectations only for behavior the request intentionally
  changes; preserve the remaining contracts and state on failed operations.
- Review the diff before committing. Each changed block should serve the
  requested behavior, its necessary extraction, or its checks/documentation.
  Remove unrelated edits and explain any broader refactor that is necessary.
  Diff size alone is not proof of churn: judge whether the edits were needed
  and whether the resulting responsibilities remain clear.

### Start simple, then grow through edits

For a new program, implement only the current requested capability as a small
working slice: one parsing path, the operation helpers it needs, and a thin
public entrypoint. Avoid scaffolding later capabilities. Follow the selected
commits skill or the request's stage order when either defines the next slice;
this section does not create a separate commit policy.

At each subsequent change:

1. Run the current slice through its public entrypoint and identify the helper
   that owns the behavior being extended or revised.
2. Edit that helper or add a focused operation helper through the existing
   parsing/dispatch path. Keep each function's purpose clear; split a newly
   mixed responsibility locally instead of rebuilding the program around it.
3. Exercise the new behavior and retained earlier behavior before advancing.
   If a requirement changes an earlier rule, replace only the affected
   expectations and keep the remaining regression examples.
4. Inspect the working code and diff now, rather than deferring simplicity to
   a final rewrite. Remove dead branches and obsolete helpers created by this
   change; keep helpers that still serve earlier capabilities. Avoid needless
   one-line wrappers and abstractions whose only purpose is a possible later
   stage.

Repeat this cycle as the program grows. Prefer a clear, cohesive helper over
arbitrary function-size limits, and preserve existing interfaces unless the
request changes them. A simple final file does not justify building every
capability up front or repeatedly replacing earlier working implementations.
