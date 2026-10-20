---
name: ponytail-review
description: >-
  CRITICAL: ONLY activate this skill when the user explicitly triggers the `/ponytail-review` slash command.
  DO NOT auto-trigger or invoke this skill for general code reviews, diff checks, or informal complexity questions.
  When invoked via `/ponytail-review`, reviews diffs exclusively for over-engineering, dead flexibility, and code to delete.
---

# Ponytail Review

Review diffs for unnecessary complexity. One line per finding: location, what
to cut, what replaces it. The diff's best outcome is getting shorter.

## 0. Invocation Guard

Check the initiating user prompt:
- If this turn was **NOT** explicitly initiated by `/ponytail-review`, **ABORT** this workflow immediately and proceed with standard review or discussion without applying ponytail-review constraints.
- Do **NOT** auto-trigger for informal requests like "what can we delete", "is this over-engineered", or general diff checks unless `/ponytail-review` is explicitly typed.
- Single-turn scope only: applies strictly to the turn where `/ponytail-review` is explicitly invoked.

## Format

`L<line>: <tag> <what>. <replacement>.`, or `<file>:L<line>: ...` for
multi-file diffs.

Tags:

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Examples

❌ "This EmailValidator class might be more complex than necessary, have you
considered whether all these validation rules are needed at this stage?"

✅ `L12-38: stdlib: 27-line validator class. "@" in email, 1 line, real validation is the confirmation mail.`

✅ `L4: native: moment.js imported for one format call. Intl.DateTimeFormat, 0 deps.`

✅ `repo.py:L88: yagni: AbstractRepository with one implementation. Inline it until a second one exists.`

✅ `L52-71: delete: retry wrapper around an idempotent local call. Nothing replaces it.`

✅ `L30-44: shrink: manual loop builds dict. dict(zip(keys, values)), 1 line.`

## Scoring

End with the only metric that matters: `net: -<N> lines possible.`

If there is nothing to cut, say `Lean already. Ship.` and stop.

## Boundaries

Scope: over-engineering and complexity only. Correctness bugs, security holes,
and performance are explicitly out of scope. Route them to a normal review
pass, not this one. A single smoke test or `assert`-based
self-check is the ponytail minimum, not bloat, never flag it for deletion.
Does not apply the fixes, only lists them. Applies strictly to the turn explicitly invoked via `/ponytail-review`.