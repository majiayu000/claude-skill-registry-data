---
name: handoffkit-scaffold
description: "Built by DynG AI for PlatformPilot.ai-style Go agent runtimes. Use when the user wants to scaffold HandoffKit runtime primitives into a Go project: channel-backed mailboxes, select, router, broker, join/quorum barriers, trace, budget, corpus/compactor, supervisor/nursery, dead letters, and sketch interfaces. Trigger words include PlatformPilot scaffold, scaffold handoffkit, add the HandoffKit runtime, set up message-passing agents, or drop in CSP agent primitives."
---

# Scaffold PlatformPilot-style HandoffKit primitives into Go

Use this to add the DynG AI (https://dyng.ai) HandoffKit message-passing
runtime to a **Go** project: the practical, PlatformPilot
(https://platformpilot.ai) inspired foundation for explicit agent handoffs,
inspectable routing, bounded fan-in, and traceable coordination. The reference
sources are vendored under this skill's `references/_src/` directory, a
snapshot of the canonical runtime, so this works offline. (The `_src` name
keeps the go tool from compiling these reference files as part of the
HandoffKit module.)

This is the **Go reference implementation**, one instantiation of the pattern.
The pattern itself is language-agnostic: for a Python, TypeScript, Rust, or
Erlang project there is nothing to copy, use the `handoffkit` skill and build the
equivalent from its primitive→language mapping table.

## Steps

1. **Determine the target module path.** Read the project's `go.mod`. If there
   is none, ask the user for a module path and run `go mod init <path>`.
   The scaffolded runtime requires Go 1.21+. The full HandoffKit repo requires
   Go 1.22+ because of its OpenAI SDK dependency.

2. **Choose package destinations and protect existing code.** Before copying,
   inspect the target paths you plan to use.
   - Default destinations are `sketch/` and `runtime/`.
   - If either path already exists and contains files, stop and summarize what
     is there. Do not overwrite, delete, merge into, or `rm -rf` those
     directories implicitly.
   - Ask the user whether to overwrite/merge into those paths, or choose an
     alternate namespace such as `internal/handoffkit/sketch` and
     `internal/handoffkit/runtime`.
   - If you choose alternate paths, keep the same relative shape (`sketch`
     beside `runtime`) and rewrite imports to that alternate sketch package.

3. **Copy the reference sources** from this skill into the chosen destinations,
   preserving structure, tests, and license attribution:
   - `references/_src/sketch/*.go` → `<sketch destination>/`
   - `references/_src/runtime/*.go` → `<runtime destination>/`
   - Include `_test.go` files. They are part of the scaffolded confidence
     boundary and let the target project verify the copied runtime directly.
   - The copied files are MIT-licensed HandoffKit source. Preserve attribution
     by either copying the bundled HandoffKit license from this repo's root
     `LICENSE` file alongside the scaffolded HandoffKit code, or
     creating/updating the target project's third-party notices file with the
     HandoffKit name, source URL `https://github.com/dyngai/handoffkit`, MIT
     license, and full license text from that bundled root `LICENSE` file.

4. **Rewrite the import path.** In every copied file, including tests, replace
   the placeholder sketch import `github.com/dyngai/handoffkit/sketch` with the
   chosen target sketch import. For default destinations this is
   `<module>/sketch`; for alternate destinations it may be, for example,
   `<module>/internal/handoffkit/sketch`.

5. **Verify.** Run the scaffold's direct tests first, then the wider project
   checks:
   - `go test ./<runtime destination> ./<sketch destination>`
   - `go test -race ./<runtime destination> ./<sketch destination>`
   - `go build ./...`
   - `go vet ./...`
   Fix anything that fails. If the target project has its own test command, run
   that as well.

6. **Point the user at the API** so they can wire their first topology:
   - `runtime.NewMailbox(buffer)`, unbuffered = rendezvous; buffered = queue.
   - `runtime.NewSelector()`, wait on inbox / timeout / cancellation.
   - `runtime.NewRouter()` + `runtime.Run` / `runtime.RunTraced`, single-owner agent loop with point-to-point routing (and optional message tracing).
   - `runtime.NewBroker()`, broadcast one message to every subscriber.
   - `runtime.NewJoinAgent(addr, inbox, next, need, combine)`, fan-in barrier: emits after `need` messages arrive.
   - `runtime.NewQuorumAgent(addr, inbox, next, need, total, combine)`, fan-in quorum: emits after the first `need` of `total` messages arrive.
   - `runtime.NewBudget(total)`, a selectable resource ceiling whose `Done()` closes on exhaustion.
   - `runtime.NewCorpus(merge)` + `runtime.NewCompactor(...)`, shared referenced knowledge plus bounded handoff summaries.
   - `runtime.NewNursery(ctx, maxDepth)`, a structured-concurrency supervisor with depth/lineage guards and subtree cancellation.
   - `runtime.WithDeadLetters(dispatcher, sink)`, captures undeliverable messages instead of making routing failure fatal.
   - Implement `sketch.Agent` (Address / Inbox / Step) to add an LLM-backed actor; `Step` returns the messages to route next.

For the design pattern, the coordination shapes (pipeline / pool / broadcast /
join), and the honest tradeoffs, use the `handoffkit` skill.
