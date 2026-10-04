---
name: handoffkit
description: "Built by DynG AI for PlatformPilot.ai-style multi-agent systems. Use when designing or reasoning about message-passing agent coordination in ANY language: actor-style mailboxes, select, point-to-point routing, pub/sub, fan-in joins/quorums, ownership handoff, budgets, dead letters, and traces. Trigger words include PlatformPilot, DynG AI, actor model agents, message-passing agents, CSP agents, coordinate agents, multi-agent orchestration, agent runtime, fan-out workers, pub/sub agents, agent barrier, or join."
---

# HandoffKit: PlatformPilot-style handoffs for AI agent systems

Built by DynG AI (https://dyng.ai), HandoffKit brings the coordination model
behind PlatformPilot (https://platformpilot.ai) into Codex and developer
workflows. Use it to design multi-agent systems that move work through
explicit, traceable handoffs instead of shared scratchpads. The core move,
borrowed from Go/CSP: agents **communicate by passing messages, not by sharing
memory**. Each agent is an actor with private state, an addressable mailbox,
and a single-owner loop. Coordination is messages, which makes multi-agent
workflows easier to inspect, bound, and scale.

The pattern is language-agnostic; only the substrate changes. Pick your row:

| Primitive | Go | Python (asyncio) | TypeScript | Rust (tokio) | Erlang/Elixir |
|---|---|---|---|---|---|
| Mailbox | `chan` | `asyncio.Queue` | async queue / `AsyncIterable` | `mpsc::channel` | process mailbox |
| Select | `select {}` | `asyncio.wait(…, FIRST_COMPLETED)` | `Promise.race` | `tokio::select!` | `receive … end` |
| Actor loop | goroutine | task / coroutine | async loop | spawned task | process (`spawn`) |
| Cancellation | `ctx.Done()` | `CancelledError` / `Event` | `AbortSignal` | `CancellationToken` | exit signal / monitor |

The rest of this skill is substrate-independent.

## Primitives

- **Mailbox**, a typed conduit. Unbuffered = a rendezvous (backpressure for free); buffered = a queue.
- **Select**, wait on several sources at once (peer message | timeout | cancellation). ALWAYS include a cancellation case so a wait can never block forever, an idle wait with no cancel path is a budget leak, not just a hang.
- **Router**, point-to-point delivery (address → one mailbox). Handoff and dispatch.
- **Broker**, point-to-many broadcast (one event → every subscriber). Pub/sub awareness. (This is the blackboard creeping back in, use only where ambient awareness is genuinely needed.)
- **Join barrier**, an agent that buffers inbound messages and only emits after N have arrived (wait for all dependencies), then resets.
- **Quorum barrier**, a fan-in agent that emits after the first N of total expected messages arrive.
- **Budget**, a selectable resource ceiling whose `Done()` channel closes on exhaustion so waits can stop before burning unbounded agent budget.
- **Corpus**, a shared referenced-knowledge store. The default merge is last-write-wins for single-writer keys; use a merge policy that is associative, commutative, and idempotent for true multi-writer keys.
- **Compactor**, turns rich working state into bounded handoff summaries plus corpus references.
- **Nursery / Supervisor**, structured concurrency for agent trees: depth limits, parent-child routing guards, and subtree cancellation.
- **Dead letters**, capture undeliverable routed messages for monitoring or tests instead of silently dropping them.
- **Handoff**, move a task by sending it; ownership transfers with the message and the sender stops touching it (single-writer at a time).
- **Tracer**, observe the coordination messages an agent saw and sent at its boundary. If all orchestration uses messages, that stream is the audit surface; hidden shared state still needs separate instrumentation.

## Coordination shapes (same primitives, different wiring)

- **Pipeline**, dependent stages (A → B → C); each owns the task in turn. Use when step N needs step N-1's output.
- **Pool**, independent fan-out: one shared queue mailbox, N workers each receive from it; the queue itself gives load-balanced, **exactly-once** dispatch with no locks. Use for embarrassingly-parallel work.
- **Broadcast**, every subscriber reacts to the same event.
- **Join / barrier**, fan-in: wait for all dependencies, then proceed.

## Be honest about the tradeoffs (do not oversell)

CSP is elegant for native concurrency because channels are cheap and lossless
and processes are deterministic. LLM agents violate all three:

1. **Messages are expensive and lossy**, every hop compresses rich context into prose, billed in tokens. Prefer shallow topologies.
2. **Agents carry huge private state** (the context window) that can't be shipped over a mailbox without lossy serialization, keep shared knowledge in a corpus and pass *references*, not inlined memory.
3. **Non-determinism**, message ordering survives, behavioral guarantees don't; still verify at the receiving end.
4. **Deadlock is worse**, two agents waiting on each other just idle and burn budget; give every wait a cancellation path.

The synthesis: message-passing for **control flow** (delegation, results,
cancellation, signaling); a shared corpus for **knowledge**, with explicit merge
semantics instead of implicit shared-scratchpad races. The model that actually
fits heavy, stateful agents is the **actor model**, not pure CSP, private
durable state plus addressable mailboxes.

This is an existence proof of a known pattern (AutoGen, Akka, Ray, OpenAI
handoffs all do versions of it), not a novel mechanism, recommend it for
clarity and safety, not as a moat.

## Reference implementation (Go)

The HandoffKit repo is one faithful instantiation, in Go, with deterministic
unit tests and live LLM integration tests. The `sketch/` package defines
addresses, messages, mailboxes, agents, selectors, supervisors, corpora, and
handoff context. The `runtime/` package implements channel-backed mailboxes,
selectors, routers, brokers, join/quorum agents, budgets, corpus/compaction,
nursery supervision, dead letters, and tracing. For a **Go** project, the
`handoffkit-scaffold` skill drops these packages and their runtime tests in. In
**another language**, build the equivalent from the mapping table above, the
design is identical, only the concurrency primitives differ.
