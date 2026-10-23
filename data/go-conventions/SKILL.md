---
name: go-conventions
description: "Use when writing or reviewing Go: concurrency, errors, context, defensive correctness, database access, tests, layout and idioms, standard-library security."
---

# go-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Go code. **Special status**:
unlike the frontend blocks (vue-nuxt-vuetify, react-nextjs), there is no in-house production experience
behind this file yet: the content comes from deterministic tooling (golangci-lint, staticcheck, govet)
and published style and practice guides, not from real review feedback. To be treated as a solid base to be
confronted with the first real Go project, not as proven doctrine.

## When
As soon as Go code is written or modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task touches.** One file per section under `references/`; a section read is a
section that has to be applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Concurrency and goroutines | a goroutine, channel, lock or wait group is written | [`01-concurrency.md`](./references/01-concurrency.md) |
| 2 | Error handling | a function can fail, an error is wrapped, logged or shown | [`02-errors.md`](./references/02-errors.md) |
| 3 | Context | a context is created, passed, stored or cancelled | [`03-context.md`](./references/03-context.md) |
| 4 | Other correctness | a response body, a `defer`, an `err` shadow, a slice at an API edge, an exit call | [`04-correctness.md`](./references/04-correctness.md) |
| 5 | Defensive correctness | an interface return, a map, an `append`, a numeric conversion or comparison, a zero value | [`05-safety.md`](./references/05-safety.md) |
| 6 | database/sql | a query, a transaction, a pool or a migration appears | [`06-database.md`](./references/06-database.md) |
| 7 | Tests | a test is written or reviewed | [`07-tests.md`](./references/07-tests.md) |
| 8 | Layout and idioms | a package, an interface, a module path or a version-dependent idiom | [`08-layout-and-idioms.md`](./references/08-layout-and-idioms.md) |
| 9 | Security with the standard library | untrusted input reaches SQL, a process, a template, a path, a random value or a server | [`09-security-stdlib.md`](./references/09-security-stdlib.md) |

## Output / checkpoint
Code compliant with the sections read, and `golangci-lint run` (default config: errcheck, govet,
staticcheck, gosimple, ineffassign, unused, plus `contextcheck`/`bodyclose`/`noctx` if enabled) with no
new finding introduced by the diff. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Don't enable `shadow` (govet) by default: noisy, only if the project
explicitly wants it. The agent does not design a database schema (§6.8). This block hasn't been confronted
with a real production Go project in house yet: if a rule here diverges from a real observed need, fix this
block rather than treating it as settled.

## Origin
Provenance, source versions and the dogfood record in [`references/origin.md`](./references/origin.md).
