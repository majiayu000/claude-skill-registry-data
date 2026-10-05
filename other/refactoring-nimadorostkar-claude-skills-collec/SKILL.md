---
name: refactoring
description: Use when improving the structure of code without changing its behavior. Covers safe refactoring sequences, characterization tests, and knowing when to stop.
metadata:
  category: development
  version: 1.0.0
  tags: [refactoring, code-quality, technical-debt, testing]
---

# Refactoring

## Purpose

Change the structure of code while provably preserving behavior. The defining constraint is that behavior does not change — if it does, it is a rewrite, and it needs different scrutiny.

## When to Use

- Before adding a feature to code that resists the change.
- When a module has become hard to test.
- To pay down a specific, identified cost — not to satisfy an aesthetic.
- After a bug reveals a structural cause.

## Capabilities

- Characterization tests to pin down existing behavior, including its bugs.
- Standard sequences: extract function, extract class, inline, replace conditional with polymorphism, introduce parameter object.
- Dependency breaking: seams, adapters, and inversion for untestable code.
- Incremental strangling of legacy paths behind a stable interface.

## Inputs

- The module to change and the reason for changing it.
- The existing test suite, and an honest assessment of its coverage.
- The feature or fix that motivated the refactor, if any.

## Outputs

- Restructured code with identical observable behavior.
- Tests that passed before and after, unchanged.
- A commit sequence where each commit is independently green.

## Workflow

1. **Justify it** — Name the concrete cost the current structure imposes. "It's ugly" is not a cost. "Every new payment method requires editing five files" is.
2. **Pin the behavior** — If tests do not cover the code, write characterization tests first: call the code, record what it actually does, assert that. Bugs included.
3. **Refactor in small steps** — One mechanical transformation per commit. Run the tests after each.
4. **Do not mix in behavior changes** — A refactoring commit and a feature commit must be separate. Reviewers cannot verify both at once.
5. **Stop when the motivating change is easy** — Refactoring is preparation, not a destination.

## Best Practices

- Make the change easy, then make the easy change. In that order, in separate commits.
- Never refactor on a branch that is not fully covered by tests you trust.
- If the tests need to change, you are not refactoring. Say so.
- Extract until each function does one thing at one level of abstraction, and no further.
- Delete dead code aggressively; version control remembers it for you.
- Resist wholesale rewrites. The existing code encodes years of edge cases you have not thought of.

## Examples

**Breaking a dependency to make code testable:**

```python
# Before: untestable — reaches out to the network and the clock.
def send_expiry_warnings():
    for user in db.query("SELECT * FROM users WHERE expires_at < now() + interval '7 days'"):
        smtp.send(user.email, render("expiry_warning", user=user))

# After: dependencies are seams. Behavior is unchanged.
def find_expiring_users(db, now, window=timedelta(days=7)):
    return db.users_expiring_before(now + window)

def send_expiry_warnings(db, mailer, now):
    for user in find_expiring_users(db, now):
        mailer.send(user.email, render("expiry_warning", user=user))
```

The test can now supply a fake `db`, a fake `mailer`, and a fixed `now` — without a network, a database, or a sleep.

## Notes

- Characterization tests will encode existing bugs. That is intentional: fix them in a separate, clearly labeled commit so the fix is reviewable.
- Automated refactorings in an IDE (rename, extract method) are safer than hand edits. Prefer them.
- A refactor that touches a hundred files is not small steps, whatever the commit message says. Split by module.
