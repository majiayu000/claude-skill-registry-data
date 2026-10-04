---
name: go-troubleshooting
description: "Systematic troubleshooting and debugging for Golang programs. Covers panics, deadlocks, race conditions, and performance issues."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:50:00 GMT
---

## Troubleshooting Methodology

1. **Read the Error** — Go error messages and stack traces are precise. Identify the file and line number.
2. **Reproduce** — Create a minimal, deterministic test case that fails.
3. **Isolate** — Strip away unrelated code until only the bug remains.
4. **Hypothesize** — Form one explanation for the bug and test it.
5. **Measure** — Use tools (`pprof`, `-race`) to confirm your hypothesis.
6. **Fix Root Cause** — Avoid "band-aid" fixes. Ensure you understand *why* the fix works.

## Decision Tree: What are you seeing?

| Symptom | Action |
| --- | --- |
| **Build won't compile** | `go build ./...` and check type/import errors. |
| **Logic bug** | Write a failing test; check error handling and nil pointers. |
| **Random crashes / Panics** | Check stack trace; run with `GOTRACEBACK=all`. |
| **Race conditions** | Run tests with `go test -race ./...`. |
| **Program hangs** | Capture goroutine profile: `curl .../debug/pprof/goroutine?debug=2`. |
| **High CPU/Memory** | Use `pprof` CPU or heap profiling. |

## Common Go Bugs

- **Nil Pointer Dereference**: Accessing a field/method on a nil pointer.
- **Interface Nil Gotcha**: A typed nil pointer inside an interface is NOT nil.
- **Concurrent Map Access**: Writing to a map from multiple goroutines without a lock.
- **Goroutine Leak**: Spawning goroutines that never exit.
- **Variable Shadowing**: Accidental redeclaration of a variable in a nested scope (e.g., `err := ...`).

## Debugging Tools

- **`go test -race`**: Detects data races.
- **`delve` (dlv)**: Full-featured debugger for setting breakpoints and inspecting state.
- **`pprof`**: Profiling CPU, memory, and blocking operations.
- **`GODEBUG`**: Environment variables for tracing GC (`gctrace=1`) or the scheduler (`schedtrace=1000`).

## Anti-patterns in Debugging

- ❌ **Guessing fixes** — "Maybe adding a nil check here helps."
- ❌ **treating symptoms** — Fixing a crash without understanding the invalid state that caused it.
- ❌ **Multiple changes at once** — You won't know which one fixed the issue (or broke something else).
- ❌ **Ignoring `-race` output** — Races are undefined behavior; fix every single one.
- ❌ **Leaving `fmt.Println`** — Use a structured logger (`slog`) for persistent diagnostics.
