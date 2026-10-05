---
name: programming-golang
description: >-
  Guides Go work under the Go standard: starting from the module's recorded gates, placing tests by the boundary they
  touch, and judging error forms, interface placement, goroutine ownership, and context use.
when_to_use: >-
  Use when writing, changing, or reviewing Go code in a module, before the first test of the change.
compatibility: Requires a Go module with the Go toolchain on the path.
---

# Go Programming

Every Go rule is owned by [Go Standards](../../../repo-governance/development/quality/stacks/golang-standards.md).
[Test-Driven Development](../../../repo-governance/development/tdd-policy.md) and
[Test Boundaries and Gates](../../../repo-governance/development/quality-gates.md) govern tests and gates,
[Red, Green, Refactor](../../../repo-governance/workflows/quality/red-green-refactor.md) runs each cycle, and
[Developing Applications](../developing-applications/SKILL.md) carries the judgement on layers, errors, logs, and input
that holds in every language. This skill adds only the procedure and judgement of applying them in Go. Where a sentence
here seems to state a rule, the standard decides.

## Start From What the Module Records

Read the module's `go` directive, its committed linter configuration, and the recorded choices for assertions and
integration selection. Run the standard's gates, then the unit run with the race detector, on the untouched tree. A gate
already failing is handled under
[Preexisting Error Resolution](../../../repo-governance/principles/root-cause-orientation.md).

## Place a Test by What It Touches

`t.TempDir`, `t.Setenv`, a real listener, and a child process each reach a boundary the unit layer excludes, so a test
using one belongs to the integration selection. To keep a decision under unit test, pass in the content, an `io.Reader`,
an `fs.FS`, or the setting's value.

In a table-driven test, name each row for the behaviour it proves, so a failure names it too. A row for a new behaviour
is a new cycle: add it, watch it fail, then change the code.

## Choose the Form of an Error

Ask what the nearest caller will do with the failure. If it only reports or passes it on, wrap it with context and give
it no identity. Only when a caller must test for the condition, or read details from it, does the error take one of the
exported forms the standard lists. An exported sentinel or type joins the package's Public Contract, so exporting one
"in case" commits the package to it. When a `panic` seems tempting, ask whether any caller could handle the failure; if
one could, it is a returned error.

## Declare the Interface Where It Is Used

Declare an interface in the package that consumes it, sized to the methods that consumer calls, and let the
implementation return its concrete type. An interface sitting beside its only implementation "for testing" usually
belongs with the caller, which is also where Hexagonal Architecture puts a port.

## Give Every Goroutine an Owner

Before starting a goroutine, name who waits for it and what tells it to stop. One nobody waits for leaks on the first
error path; one with no stop signal outlives its request.

- Pass the caller's `context.Context` down through every call that may wait, rather than starting a fresh one.
- Use a channel to hand over a value or signal completion, and a mutex to guard state several goroutines read.
- The race detector sees only races that ran, so a test for concurrent code drives the goroutines it starts to
  completion.

## Before Handing Off

- the standard's gates report nothing, and the unit run passed with the race detector;
- every returned error is handled or returned, never discarded;
- every goroutine added has an owner and a stop signal;
- randomness that protects anything comes from `crypto/rand`; and
- each recorded red failed on an assertion, never on a build error or a panicking stub.
