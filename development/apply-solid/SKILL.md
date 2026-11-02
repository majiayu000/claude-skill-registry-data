---
name: apply-solid
description: Use when a class or module violates SOLID — an edit forces unrelated edits, a dependency needs a mock everywhere, an abstraction leaks — and you must apply the five principles at the class level.
---

# Apply SOLID

The five principles applied at the class and module level (Clean Architecture). The layer-level rules —
dependencies point inward, boundaries at axes of change — are in
[enforce-dependency-rule](../enforce-dependency-rule/SKILL.md). Object-design rules in
[apply-design-principles](../apply-design-principles/SKILL.md).

## The five

1. **Single Responsibility** — a module has one reason to change, which means one *actor* it serves.
   Two actors (e.g. the billing team and the ops team) that share a class will fight over it.
2. **Open/Closed** — open for extension, closed for modification. Protect the high-level, stable
   components by pointing dependencies away from them; add behaviour by adding code, not editing the core.
3. **Liskov Substitution** — a subtype must be usable wherever its base type is, including the base's
   contract (preconditions not stronger, postconditions not weaker). LSP is about *behaviour*, not shape:
   a Square that breaks Rectangle's setters fails LSP even though it inherits.
4. **Interface Segregation** — depend only on what you use. A fat interface forces every client to
   recompile and re-mock for methods it never calls; split by client.
5. **Dependency Inversion** — depend on abstractions, not concretions. The abstraction is owned by the
   high-level policy; the detail (DB, web, framework) implements it and points inward.

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null | head -20
grep -rn "mock\|Mock\|stub" --include="*.ts" --include="*.rs" --include="*.go" --include="*.py" . 2>/dev/null | head -20
```

Find the violation, not the abstraction: a class that changed for two unrelated tickets (SRP), a change
that forced edits to a stable core (OCP), a subtype that throws "not supported" (LSP), an interface with
methods most clients leave empty (ISP), a policy module importing a vendor SDK directly (DIP).

## 2. Apply the smallest fix

- SRP: extract the second actor's responsibility into its own class/module.
- OCP: add a seam (a function parameter, a registry, an interface) so the new case is an addition.
- LSP: fix the contract, or drop the inheritance and use composition (see
  [apply-design-principles](../apply-design-principles/SKILL.md)).
- ISP: split the interface by client; a client depends only on the slice it uses.
- DIP: move the abstraction up into the policy and have the detail import it.

## 3. State the exception

SOLID is a means to a maintainable boundary, not a purity test. If a principle's ceremony outweighs the
churn it prevents in this codebase, say which and why.

## Verify

The edit that used to touch two unrelated places now touches one; a new case landed as an addition, not
a modification; the mock that was needed everywhere now appears once at the seam. State the principle
violated and the fix in the note.

## When to deviate

- Small, single-actor modules where a full abstraction is premature.
- Framework or library code whose contract is fixed by the vendor.
