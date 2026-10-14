---
name: ground-mechanism
description: Code or model. What must be deterministic, and what must be judged.
---

# Skill: Mechanism

> "The model decides. Code enforces. Never the reverse."

## The Standard

- **Model decides, code enforces**: if a model's output *is* the enforcement, there is no enforcement.
- **Never let a model report its own oracle result**: run the command in code, read the exit code in code.
- **One answer means code**: a single correct answer is computable. A space of acceptable answers is judgment.
- **Replay means code**: billing, audit, security, migrations. A model is not reproducible across versions, and versions change underneath you.

## The Check

Ask yourself:
- One correct answer, or a space of acceptable ones?
- Must this replay identically?
- Is the input space enumerable? A model choosing between four known branches is an expensive, non-deterministic switch statement.
- If this is wrong, will anyone notice?

Silent wrongness with a wide blast radius is code, or a model behind a gate.

## The Surface

Frequency × ambiguity. Not a binary.

|                     | Low ambiguity                     | High ambiguity                       |
|---------------------|-----------------------------------|--------------------------------------|
| **High frequency**  | Code. The economics compound.     | Model — and promote aggressively.    |
| **Low frequency**   | Either. Don't over-engineer.      | Model. Encoding never pays back.     |

## The Migration

The line moves. Both ways.

- **Promote** judgment → code when it recurs identically. It gets cheaper forever.
- **Demote** code → judgment when rules accrete special cases faster than they generalize. A rule set growing one clause per incident is a classifier fighting to be born.

## The Sandwich

The practical shape:

```
code    deterministic preparation, constrained input
  model   the judgment, and only the judgment
code    deterministic validation of the output
```

Widen the middle only where The Check says judgment is genuinely required.

## Before Delegation

Mechanism decides the executor **kind**. `ground-delegation` decides the executor **context**.

Ask this one first. If the answer is code, there is nobody to delegate to.

## The Anti-Patterns

| Don't                              | Do                            | Why                                  |
|------------------------------------|-------------------------------|--------------------------------------|
| Model doing arithmetic or format   | Code                          | Slower, costlier, sometimes wrong    |
| Model routing over known branches  | A switch                      | Non-deterministic control flow       |
| Model reporting its own test result| Harness reads the exit code   | Voids the gate entirely              |
| Regex over natural language        | Model                         | Open sets do not enumerate           |
| Rule engine encoding taste         | Model                         | Expert systems died of this          |

## Real-World Examples

See [examples.md](examples.md).
