---
name: system-design
description: Design and review of the structure of a system with SOLID, design patterns, contracts and an invariant catalogue. Use for a design choice, a module boundary, a refactor plan or a design review.
---

# System design

This skill gives one method to design a system, to review a design, and to plan a refactor. It combines four
sources: the SOLID principles, the design-pattern catalogue, the code-smell and refactoring catalogue, and
production lessons that real rebuilds paid for. The references hold the detail and the source links.

Write every result in ASD-STE100 (output style `shark:asd-ste100`): outcome first, label each statement
**observed**, **inferred** or **assumed**, give full file paths, and write Markdown files (never published pages).

## When to use

- You design a new feature, a module, a service, or a boundary between services.
- You review a design document, a spec, or a diff for structure (not for style).
- You plan a refactor or a rebuild that replaces code.
- You write a round contract before parallel lanes start (the operator skill, `shark:operator`).
- A change is difficult: one fix needs edits in many files, or a fix in one place breaks another place.

Do not use it for a one-line local fix. Do not add a pattern to code that has no named force for it.

## Inputs to read first

1. The project's `AGENTS.md` (or `CLAUDE.md`): `## Invariants`, `## Architecture rules`, `## Docs layout`.
   If a section is missing, ask the user one time and suggest that they add it to `AGENTS.md`.
2. The spec or the request, and the code that it touches. Make sure that each design term names a real structure
   in the code before you build on it. A term that maps to a different structure gives a design with a hidden gap.
3. For a rebuild: the branch that runs in production. Its deleted rules are part of the input
   (see step 6 and `shark:port-audit`).

## Workflow

### 1. State the forces and the invariants

Write down what pushes on the design: what changes often, what must never change, the load, the latency budget,
the cost budget, the failure modes, and who owns each decision. List each invariant as one testable sentence
(for example: "a tenant reads only its own rows"; "money is an integer in minor units"). Put a number on each
force that you can measure. Most of the analysis belongs here, before code. A design with the math written first
makes the code fast to write.

### 2. Choose the boundaries and the dependency direction

- Split by reason to change (SRP), not by technical layer alone.
- Make dependencies point inward: presentation and infrastructure depend on application; application depends on
  ports; ports depend on the domain; the domain depends on nothing outside the standard library and shared value
  types. Adapters implement ports (DIP; ports and adapters).
- Other modules call a module only through its facade. Write the allowed calls between modules as a table, and
  make a tool check it (import contracts, dependency rules).
- Put each invariant in **one place** that every path must pass: the data layer for isolation, one value type for
  money, one router for permissions, one unit of work for write + event + job.

### 3. Pick patterns only for a named force

For each pattern that you add, write: the force it answers, the pattern, and the cost it adds. If you cannot name
the force, do not add the pattern. Prefer the simplest structure that holds the invariants. See
[references/patterns.md](references/patterns.md) for the 22 patterns, with "use when" and "watch out".

### 4. Write the contract

Before any parallel work, write one contract with:

- each shared name (type, event, field, route, setting, table) and its **one owner file**;
- each data shape in native types (Money, date, enum, integer), and the place where text is made from it;
- every writer and every reader of each new or changed event or field;
- the invariants and the owner decisions to keep;
- each rule to delete, with its callers and its new owner;
- the cross-service contracts, pinned by version or hash, with both sides named.

A lane that needs a shared decision that the contract does not give stops and reports. It does not decide alone.

### 5. Check against the smells

Read the design or the diff against [references/smells-and-refactorings.md](references/smells-and-refactorings.md)
and [references/production-lessons.md](references/production-lessons.md). For each finding, give the smell, the
file and line, and the refactoring that removes it.

### 6. Plan the refactor as safe steps with tests

- Pin the current behaviour with tests first (characterisation tests; rule-tagged tests for business rules).
- One step = one refactoring = one commit that passes the gate. Never mix a refactor with a behaviour change
  (`shark:commit-blocks`).
- Use expand/contract for every shared shape: add the new, move the callers, remove the old.
- A rebuild loses rules. Before the new code replaces the old code, audit the deleting commits against the
  production branch (`shark:port-audit`).
- After a rebuild, delete the old path. Do not keep it alive behind a switch or a frozen byte-for-byte test. The
  version history and the rollback of a release are the safety. Count progress by what you removed.

### 7. Define how it is measured

- Measure a baseline before you add complexity (a cache, a new index, embeddings, a second model, a queue).
  Keep the change only if the measurement shows a gain on the named force.
- Compare old and new by measurement on the same inputs, not by a parallel run of the old path.
- Name the signals: latency, traffic, errors, saturation, and cost. Cost must price cache reads and cache writes;
  if it does not, the reported spend is only an upper bound.
- Judge a speed change by its effect on accuracy first. A speed lever may overlap, cache or reuse work; it may not
  drop or degrade a result that later steps depend on.

## Design review checklist

Use the expanded form, with examples in two stacks, in
[references/review-checklist.md](references/review-checklist.md).

**Boundaries and dependencies**
1. Each module has one reason to change.
2. Dependencies point inward; the domain imports no framework, database or network code.
3. Other modules call only the facade; a tool checks the import contracts.
4. Adapters are built in one wiring place and injected; no module builds another module's adapter.
5. Presentation and infrastructure never import each other.

**State and data**
6. State, events and messages keep native types; text is made only at the presentation edge.
7. No code parses display text back into data.
8. Money is an integer in minor units (or a decimal type); each rounding call names its mode.
9. Keys are unique and sortable (for example time-ordered UUIDs); no shared sequences across services.
10. One typed reader per external result shape, with a contract test against the real writer.

**Rules and invariants**
11. Each business rule lives in one place; no copy in a second call site.
12. Per-customer or per-tenant behaviour is configuration or spec, not a branch on a name in shared code or prompts.
13. Each invariant is enforced at one point that every path passes (data layer, value type, router).
14. Tenant isolation is enforced at the data layer, not only in application filters.
15. Routes deny by default: authentication, then membership, then one named permission.

**Consistency and failure**
16. A write, its event and its job enqueue commit in one unit of work (transactional outbox).
17. Each retried or external call carries an idempotency key; a repeat returns the first result.
18. Reads have no side effects.
19. SQL is safe for the connection pooler (no session state in transaction pooling mode).
20. Timeouts, retries and budgets are explicit for each external call.

**Change and contracts**
21. Schema changes are expand/contract; data changes run as backfill jobs, not in migrations.
22. Contracts between services are pinned (version or hash) and changed byte-identical on both sides.
23. A rebuild has a port audit and deletes the old path; no switch keeps both alive.

**Measurement**
24. A baseline exists before the added complexity, and the change shows a measured gain.
25. Logs, metrics and traces name the unit of work, the tenant and the request; cost includes cache reads/writes.

## References

- [references/solid.md](references/solid.md): the five principles, with original sources, symptoms and checks.
- [references/patterns.md](references/patterns.md): the 22 design patterns in three groups.
- [references/smells-and-refactorings.md](references/smells-and-refactorings.md): smell groups and the
  refactorings that fix them.
- [references/production-lessons.md](references/production-lessons.md): production rules, each with the failure
  it prevents and how to check it.
- [references/review-checklist.md](references/review-checklist.md): the expanded checklist with examples.

## Related kit parts

- Agents: `shark:architect` (design review), `shark:code-writer` (design check before code),
  `shark:lead-engineer` (merge against the contract).
- Skills: `shark:port-audit` (rules that a rewrite lost), `shark:commit-blocks` (one refactoring per commit),
  `shark:operator` (when to write the round contract).
