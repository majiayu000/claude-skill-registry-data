---
name: review-go
description: Use when reviewing, debugging, or giving feedback on Go code in this repo (exercises/part2, website/tools, or any *.go file) or when asked for a "code review", "review this Go", "revisa este código Go", or "crítica de código". Reviews for correctness, idiomatic Go, error handling, resource cleanup, concurrency, performance, and security, and always ends with a test-thinking pass (what a test would catch). For exercises/part2, prefer the go-exercise-reviewer skill which knows the module-mode quirk; this skill covers general Go anywhere in the repo.
---

# Go Code Review

You review Go code like the strictest reviewer and the meanest test-designer
combined. You think about what could break and whether the code would survive
a test that actually checks it. You do not stop at "it compiles."

## Steps

1. **Read the code first** — read every file in scope in full before judging.
   Understand what it is *for* (grep for callers/uses) before reviewing how.
2. **Verify it builds and is formatted** — from the package dir run
   `go vet ./...`, `go build ./...` (or `gofmt -l .`), and fix anything
   mechanical before going deeper. In this repo, stdlib exercises without a
   `go.mod` need `GO111MODULE=off` (the parent `.git` confuses module mode);
   that "cannot find main module" error is expected, not a code bug.
3. **Review the dimensions below**.
4. **Test-thinking pass** — for each concern, name the test that would catch it.
5. **Report** in the output format at the bottom.

## Review dimensions

1. **Correctness** — does it do what it claims? Right protocol/algorithm,
   right boundaries, right ordering, right error semantics. Check off-by-one,
   empty-input, and single-element cases explicitly.
2. **Error handling** — every error checked and handled meaningfully. No
   swallowed errors (`_`), no bare `panic` on recoverable input, errors
   wrapped with context (`fmt.Errorf("...: %w", err)`), `defer` on close that
   still surfaces errors where it matters.
3. **Resource management** — every `net.Conn`, `net.Listener`, `http.Response`
   body, `io.Reader`, file, and goroutine cleaned up. `defer r.Body.Close()`
   present and correct. No leaked listeners, unclosed sockets, or files.
4. **Concurrency** — goroutines must be stoppable; channels closed exactly
   once; `sync.WaitGroup` correct; no busy-loops without backoff; shared state
   under mutex or confined; contexts respected (`context.WithTimeout`,
   `SetDeadline`). Watch for data races and double-close.
5. **Idiomatic Go** — `io.Copy` over manual loops, `net.JoinHostPort` over
   `fmt.Sprintf("%s:%d", ...)`, `bufio.Scanner` with error check, `errors.Is`
   for unwrapping, `strconv` over hand-rolled parsing, table-driven tests.
6. **Performance** — allocations in hot loops, `strings.Builder` over string
   concatenation in loops, `sync.Pool` only when justified, avoid premature
   optimization (note it as a nit, not a blocker, unless measurable).
7. **Security** — no hardcoded secrets or keys, no shell injection (use
   `exec` with args, never `sh -c` on concatenated input), bounds-checked
   reads, no unbounded memory growth from untrusted input, TLS used where the
   context demands it, `net/http` timeouts set on server and client.

## Test-thinking checklist (the superpower)

For every concern ask: *if I wrote a test, what would it break?*

- **Edge inputs** — empty, oversized, truncated, malformed, maximum-length.
- **Races** — concurrent access, shared state, read/write from two goroutines
  on one connection.
- **Timeouts/hangs** — does a slow or silent peer block forever?
- **Leaks** — goroutines that outlive their scope, unclosed resources.
- **Panics** — does malformed input crash or return a clean error?
- **Flakiness** — fixed ports vs ephemeral `:0`; would a timed test be flaky?

## Output format

- **Verdict** — build/vet/gofmt result, then pass/fail per dimension
  (correctness, errors, resources, concurrency, idiom, performance, security).
- **Issues** prioritized:
  - **Critical** — broken build, wrong behavior, race, leak, security hole.
  - **Important** — missing cleanup, swallowed error, correctness gap.
  - **Style** — naming, formatting, idiom nits.
  Each with `file:line`, the problem, and the fix as a code snippet.
- **Test plan** — the 3-6 tests you would write and exactly which bug each
  would expose.
- When asked to fix, apply edits with the Edit tool, then re-run the verify
  commands and confirm the code is clean before reporting done.
