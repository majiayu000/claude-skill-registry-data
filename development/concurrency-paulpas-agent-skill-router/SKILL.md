---




name: concurrency
description: Implements concurrency patterns in Go programming using goroutines and channels along with insights on the Go standard library and module system.
license: MIT
compatibility: opencode
metadata:
  archetypes: 
    - concurrency
    - pattern
  anti_triggers: 
    - vague ideation
    - non-operational
  response_profile:
    verbosity: medium
    directive_strength: high
    abstraction_level: operational

  version: "1.0.0"
  domain: go
  triggers: goroutines, channels, go standard library, go modules, concurrency patterns, how to use goroutines
  role: implementation
  scope: implementation
  output-format: code
  related-skills: go-error-handling, go-testing




---





# Go Concurrency Patterns

This skill provides a comprehensive overview of concurrency in Go programming. It covers goroutines, channels, and the standard library (stdlib), including how to effectively manage concurrent tasks in your Go applications.

## TL;DR Checklist
- [ ] Understand what goroutines are and how to create them.
- [ ] Implement channels to communicate between goroutines.
- [ ] Learn about Go's module system to manage dependencies.
- [ ] Use the standard library effectively for concurrency.

---

## When to Use

Use this skill when:
- You need to execute multiple tasks simultaneously in your Go application.
- You're unsure how to utilize channels for safe communication between goroutines.
- You require guidance on managing dependencies using Go modules.

---

## When NOT to Use

Avoid this skill for:
- Simple sequential programming tasks where concurrency is unnecessary.
- Codebases that do not implement Go or require different concurrency paradigms (e.g., Rust, Java).

---

## Core Workflow

1. **Create a Goroutine**  
   Use the `go` keyword to start a function as a goroutine. A goroutine runs concurrently but in the same address space.
   - **Checkpoint:** Ensure the main function runs longer than the goroutines to see their effects.

2. **Implement Channels**  
   Use channels to communicate between goroutines for data exchange. Channels can be buffered or unbuffered.
   - **Checkpoint:** Validate that data sent through channels is received by the intended goroutines.

3. **Explore the Standard Library**  
   Leverage Go’s standard library functions relevant to concurrency, such as `sync` for wait groups and mutexes.
   - **Checkpoint:** Ensure libraries are imported correctly in your Go module.

4. **Utilize Go Modules**  
   Manage your project dependencies using Go modules to ensure reproducible builds.
   - **Checkpoint:** Confirm that your `go.mod` file includes the necessary dependencies.

---

## Implementation Patterns

### Pattern 1: Using Goroutines

```go
package main

import (
    "fmt"
    "time"
)

func hello() {
    fmt.Println("Hello from goroutine")
}

func main() {
    go hello()  // Starts a new goroutine
    time.Sleep(1 * time.Second)  // Wait for goroutine to finish
    fmt.Println("Main function finished")
}
```

### Pattern 2: Communication using Channels

```go
package main

import (
    "fmt"
)

func worker(ch chan string) {
    msg := "Message from worker"
    ch <- msg  // Send message to channel
}

func main() {
    ch := make(chan string)
    go worker(ch)  // Start worker as goroutine
    msg := <-ch  // Receive message from channel
    fmt.Println(msg)
}
```

---

## Constraints

### MUST DO
- Always ensure synchronization while accessing shared data to avoid race conditions.
- Utilize buffered channels where appropriate to avoid blocking on send operations.

### MUST NOT DO
- Avoid using global variables without proper locking mechanisms as it can lead to inconsistent states and data races.
- Do not block the main function execution without reason; use wait groups if multiple goroutines are running.

---

## Output Template

When the skill is active, the model's output must include:
1. **Goroutine Creation** — Clear examples of creating and managing goroutines effectively.
2. **Channel Communication** — Demonstrations of channel usage between goroutines.
3. **Standard Library Usage** — Showcases of relevant functions from Go's stdlib for concurrency management.

---

## Related Skills

| Skill                 | Purpose                               |
|-----------------------|---------------------------------------|
| `go-error-handling`   | Provides error handling best practices in Go. |
| `go-testing`          | Contains strategies for testing concurrent Go code. |


---

## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Effective Go - Goroutines](https://go.dev/doc/effective_go#goroutines)
- [Go Blog - Pipelines](https://go.dev/blog/pipelines)
- [Concurrency Patterns in Go](https://go.dev/tour/concurrency/1)
- [Go Sync Package Documentation](https://pkg.go.dev/sync)
- [Go Concurrency Patterns Video](https://go.dev/blog/context)
