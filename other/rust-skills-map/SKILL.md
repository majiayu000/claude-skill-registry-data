---
name: rust-skills-map
description: The router for this skill set — which Rust skill covers which decision, how they relate, and which one to reach for from where you are.
disable-model-invocation: true
---

# Rust Skills Map

This map contains no guidance of its own: every sentence in it either names a
skill or explains how to choose between two of them. What it settles is the
choice — which skill owns the decision in front of you, and which neighbour it
is not. It runs only when the user invokes it, as `/rust-skills-map`: a map
you consult on purpose, not one the model reaches for mid-task.

## How to use this map

Pick the row in the decision table matching the decision in front of you, run
that skill, and come back here only if the skill hands you off. Skills invoke
each other in prose, so following a handoff means typing the named skill —
every handoff in this set is a directly typeable `/skill-name`.

## The four buckets, one line each

- `rust/` — language craft: how the code should be shaped.
- `workflow/` — process: testing, review, and repo setup.
- `porting/` — migration from another language.
- `misc/` — occasional: CI, hooks, and dependency audits.

## The decision table

| You are asking | Skill | Not to be confused with |
|---|---|---|
| Does this read like Rust? | `/idiomatic-rust` | `/type-driven-design` — that one changes the model, this one changes the expression |
| Is this `clone` necessary? | `/ownership-not-clone` | `/idiomatic-rust` — expression shape, not ownership structure |
| What should this return on failure? | `/rust-errors` | `/rust-api-design` — whether the error type is a breaking change |
| Can this state exist at all? | `/type-driven-design` | `/rust-errors` — invalid states versus runtime failures |
| Should this be `pub`, generic, or `dyn`? | `/rust-api-design` | `/idiomatic-rust` — public surface versus internal shape |
| Is this safe to `.await` here? | `/async-rust` | `/ownership-not-clone` — the across-`.await` rule only |
| Is this `unsafe` block sound? | `/unsafe-rust` | `/rust-code-review` — soundness versus review process |
| Why is this slow, and what should I change? | `/rust-performance` | `/async-rust` — executor stalls and blocking work are the runtime question, not the throughput one |
| Which concurrency model fits this work? | `/rust-concurrency` | `/async-rust` — tasks and executors; this row is threads, locks, and atomics |
| How should this code report what it is doing? | `/rust-observability` | `/rust-errors` — what the error carries, not how it gets logged |
| What has to be written down about this API? | `/rust-docs` | `/rust-api-design` — whether the item is public at all, not how it documents |
| Does this change deserve a test, and which kind? | `/rust-testing` | `/rust-code-review` — designing the test versus judging its absence |
| How do I move this code into Rust without losing behaviour? | `/port-to-rust` | `/rust-testing` — the harness mechanism, not what the harness has to prove |
| What does this Python construct become in Rust? | `/port-from-python` | `/port-to-rust` — the process and the contract, not the construct |
| What does this TypeScript or JavaScript construct become in Rust? | `/port-from-typescript` | `/port-to-rust` — the process and the contract, not the construct |
| What does this Go construct become in Rust? | `/port-from-go` | `/async-rust` — the runtime rules, not the goroutine-to-task mapping |
| What does this Java construct become in Rust? | `/port-from-java` | `/type-driven-design` — the enum rules, not the hierarchy mapping |
| What does this C++ construct become in Rust? | `/port-from-cpp` | `/ownership-not-clone` — the sharing rules, not the smart-pointer mapping |
| What does this C construct become in Rust? | `/port-from-c` | `/port-from-cpp` — RAII, templates, and the STL are the other skill |
| Is this diff ready to merge? | `/rust-code-review` | every craft skill — review routes to them, it does not restate them |
| How should this repo be configured? | `/setup-rust-skills` | `/setup-rust-ci`, `/setup-rust-pre-commit` — the workflow and the hook; this one writes the lint configuration and the recorded posture |
| The repo needs CI that runs what the skills run locally | `/setup-rust-ci` | `/setup-rust-pre-commit` — that one is the commit-time convenience, this one the push-time gate |
| Contributors keep pushing unformatted code | `/setup-rust-pre-commit` | `/setup-rust-ci` — that one is the public gate, this one the local hook |
| An advisory fired, a licence question came up, or the tree grew duplicates | `/rust-supply-chain` | `/rust-code-review` — that one reviews the code, this one the dependencies |
| Should this be a macro, and is this one written well? | `/rust-macros` | `/idiomatic-rust` — the derives that already exist, before writing one |
| How should this type cross a wire format? | `/rust-serde` | `/type-driven-design` — what the validated type is, not how it deserializes |
| How should this Rust code be called from another language? | `/rust-ffi` | `/port-from-c` — moving off C, not designing a boundary to keep |

## The four flows, one line each

The full route for each — the situation, the ordered skills, and the handoff
signal that moves between them — is in `FLOWS.md`.

- **Starting fresh in a Rust repo:** `/setup-rust-skills` to configure and
  record posture, then the craft skills as the code demands them,
  `/rust-testing` and `/rust-docs` alongside, and `/rust-code-review`
  before merge.
- **Reviewing someone else's code:** `/rust-code-review` first — it dispatches
  to the craft skills itself; a craft skill directly only when the review
  already named it and the depth is wanted.
- **Porting from another language:** `/port-to-rust` for the end
  state, the parity contract, the seam, and the phase sequence, then
  `/port-from-python` for a Python source, `/port-from-typescript`
  for a TypeScript or JavaScript one, `/port-from-go` for a Go one,
  `/port-from-java` for a Java one, `/port-from-cpp` for a C++ one,
  or `/port-from-c` for a C one, for the construct mapping and the
  boundary, `/rust-testing` for the differential harness, the craft
  skills, `/rust-code-review` before merge, and `/rust-ffi` at the end
  for the case where the port leaves a permanent boundary rather than
  replacing the source outright — the end-state decision in `/port-to-rust`
  is what tells you whether it applies.
- **Making working code production-ready:** `/rust-performance` when a
  measurement says it is too slow, `/rust-concurrency` when the work needs
  to happen in parallel, `/rust-observability` so a failure in production
  is diagnosable, `/rust-serde` where the crate has a wire format,
  before the code is depended on by anything the crate does not control,
  and `/rust-docs` before the crate is published.

## Keeping this map honest

When a skill is added, renamed, or removed from the set, this map is updated
in the same change — a router that names a skill nobody can run is worse than
no router.

## No verification step, and why

This skill makes no claim a machine can settle — it routes between skills, and
there is no code to run a check against — which is the exemption the
verification rule for this set allows, and no `cargo` command is invented to
satisfy the pattern.
