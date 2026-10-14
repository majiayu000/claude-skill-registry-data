---
name: craft-oracle
description: Gates that exit 0 or 1. Choosing the commands, and promoting judgment into them.
---

# Skill: Craft Oracle

> "An adversary without an oracle is a critic."

## The Standard

- **An oracle is a command**, not an opinion. It exits 0 or 1.
- **The harness runs it.** Never a judge. A model reporting its own gate result has voided the gate.
- **Prefer the project's own script.** `composer test`, `pnpm test`, `make test`. Re-specifying the
  raw invocation duplicates a definition that will drift.
- **Judgment is not permanently judgment.** A judgment that recurs identically becomes an oracle.

## Choosing Them

Every stack has tests, types, and lint that exit 0 or 1. Start there.

```yaml
# panel.yml
gates:
  - name: tests
    command: composer test
  - name: types
    command: vendor/bin/phpstan analyse
  - name: architecture
    command: vendor/bin/pest --testsuite=arch
  # polyglot repos scope by directory
  - { name: web-types, workdir: apps/web, command: pnpm tsc --noEmit }
```

Split by cost, not by category:

| Cadence | What runs | Why |
|---|---|---|
| Every loop | tests, types, lint | Cheap, catches most |
| At approval | mutation, full acceptance | Expensive, run once |

## Promotion

The system gets cheaper here, or it does not get cheaper at all.

Round one, a judge argues that a module near IO must not be imported by a module far from it.
Judgment: correct, expensive, and it will recur on every review forever.

Round five, it is a forbidden-import check. It costs an exit code.

**The tell that something is ready to promote:** you have written the same finding three times, in
the same words.

Record candidates in the verdict's `### Promote` section. Promotion is authored work like any
other — a judge cannot write the check, and it should not arrive as a surprise commit.

## A Green Gate Can Be Empty

Passing is not covering. Two ways a gate exits 0 while certifying nothing:

| Failure | Tell |
|---|---|
| the inputs dodge the failure mode | the data was chosen by whoever wrote the code |
| the harness passes vacuously | zero cases executed, still exit 0 |

A charter demanding exact money, tested only on values binary floating point happens to represent
exactly, has a gate certifying the author's choice of examples.

**Audit a gate by breaking the code on purpose.** If it stays green, it was never a gate.

## The Coverage Rule

**Panel is worth exactly what its oracles are worth.** A task with four independent gates gets a
real adversary. A task with none gets taste ping-pong wearing a protocol.

Before convening a panel, ask what would catch this mechanically. If the honest answer is *nothing*,
either build an oracle first or do not convene.

## The Anti-Patterns

| Don't | Do | Why |
|---|---|---|
| Judge reports "tests pass" | Harness reads the exit code | Voids the gate entirely |
| Enumerate an open set in a lint | Narrow scope until it closes | Unbounded vocabularies produce false positives |
| One gate for everything | Name them separately | You cannot tell what failed |
| Re-specify a project script | `composer test` | Duplication drifts |
| Gate on a metric nobody agreed | Gate on a command everyone runs | A gate nobody trusts gets overridden |

## Real-World Examples

See [examples.md](examples.md).
