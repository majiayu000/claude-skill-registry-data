---
name: openai-assistants-legacy-security
description: Review a legacy OpenAI Assistants API integration for unsafe thread and run reuse, attachment scope failures, hosted tool exposure, and migration risk to newer interfaces.
last_reviewed: 2026-04-27
---

# OpenAI Assistants Legacy Security

## First Principle

**A thread is a conversation context with memory. If a thread is reused across users or tasks, that memory is shared — and any injection from one use affects every future use of the same thread.**

The OpenAI Assistants API manages state through threads. A thread accumulates messages, tool call results, and file references across runs. If threads are reused across users, unrelated tasks, or trust domains — either by accident (thread ID reuse in a session store) or by design (a "shared assistant" pattern) — earlier interactions become context that shapes later responses. An attacker who can influence an early interaction in a shared thread has persistent influence over every future interaction in that thread. The thread is a memory surface, and memory is an attack surface.

Read the base [tool-use-execution-security/SKILL.md](../tool-use-execution-security/SKILL.md) first for the shared control model. This skill addresses inherited integrations that have not yet migrated to newer interfaces.

## Framework Focus

- Assistants, threads, runs, and message attachments
- Hosted tools, function calling, and file-backed workflows
- Thread reuse, run orchestration, and assistant-level instructions

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Assistant instructions, thread history, file attachments, tool arguments, and run outputs are all validated before they drive application logic or downstream systems. |
| **Scope** | Assistants, threads, files, and tools are scoped per user and per task. Cross-user thread reuse is not permitted. |
| **Isolate** | A poisoned run, thread, or attachment cannot leak across assistants, users, or later runs within the same thread. |
| **Enforce** | Attachment authorization, strict tool validation, thread isolation, and migration-safe wrappers are deterministic code controls — not defaults trusted from the API. |

## OA.1 Legacy Assistant Tool and File Exposure Review

**The legacy-specific risk:** The Assistants API allows attaching tools (code interpreter, file search, custom functions) at the assistant definition level. An assistant defined with broad tool access applies that access to every user who interacts with it — regardless of whether that user's context warrants those capabilities.

### Check

- Is each assistant definition scoped to the minimum required tools and file access for its intended workflow — or does it have broad tool access configured "for flexibility"?
- Are file attachments authorized per user and per thread before they are made available to a run?
- Are there assistants with mutating tool access (write, delete, external API calls) used for workflows that only require read-only retrieval?

### Action

- **Inventory every assistant definition.** For each assistant, record: enabled tools, attached files and their sensitivity, intended user population, and intended task scope. Compare actual configuration against intended scope. Any discrepancy is a finding.
- **Per-thread file authorization.** Before creating a run, verify that every file attached to the thread is authorized for the user who initiated this interaction. Do not rely on assistant-level file attachment as a user-authorization check — a file attached to an assistant is available to all users of that assistant.
- **Separate read-only from action-enabled assistants.** An assistant that only needs to retrieve and answer should not have `code_interpreter`, external function calling, or file write capabilities enabled. Define separate assistant configurations for retrieval-only and action-enabled workflows.
- **Treat tool outputs and file content as untrusted.** When the assistant API returns tool output or file content as part of a run result, validate it before using it in application logic — the same way you would validate any untrusted external content.

### Failure Modes

- An assistant configured for HR queries has `code_interpreter` enabled from an earlier phase of development. A user exploits this to run arbitrary Python code through the assistant.
- A file containing internal business logic was attached to the assistant for testing and never removed. All users of the assistant can reference that file in their queries.
- A run's function call output contains a crafted payload that the application passes directly to a database query builder without validation.

## OA.2 Thread, Run, and Attachment Isolation

**The legacy-specific risk:** Thread IDs are persistent identifiers stored by the application. If the application reuses threads across sessions, users, or tasks — due to caching, session management bugs, or intentional design — the thread's accumulated context becomes shared state.

### Check

- Is each thread bound to a single user and a single workflow scope — or can threads be reused across users, across sessions, or across unrelated task contexts?
- Can run outputs from one run carry hidden approvals, unsafe tool state, or attacker-injected instructions into subsequent runs within the same thread?
- Is there a migration plan that eliminates legacy thread-reuse patterns before successor integrations inherit them?

### Action

- **One thread per user per session.** Create a new thread at the start of each user session. Do not reuse thread IDs across users or across distinct task workflows. Treat thread IDs as session secrets — store them with the same access controls as session tokens.
- **Validate function call outputs before acting on them.** Every function call result returned by the Assistants API must be validated by the application before it is used in downstream logic. The API's function call result is model-produced text shaped like a function return value — it is not a trusted response from the function itself.
- **Migration audit.** Document every legacy assumption about threads, runs, and attachments in the current integration. For each one, identify whether that assumption propagates into the successor interface (Responses API or equivalent). Legacy assumptions that persist unnoticed in a migration are the most common source of inherited vulnerabilities.

### Minimum Deliverable Per Review

- [ ] Assistant inventory: tools enabled, files attached, intended user population, and authorized task scope
- [ ] Thread lifecycle: creation policy (one per user per session), storage, access control, and expiry
- [ ] File authorization path: per-user, per-thread verification before run creation
- [ ] Function call output validation path before downstream use
- [ ] Migration blockers: legacy assumptions that must be eliminated before decommissioning this integration

## Quick Win

**Audit thread reuse in your session management.** Search your codebase for where thread IDs are stored and retrieved. If a thread ID can be associated with more than one user — through session inheritance, caching, or shared-assistant patterns — you have a cross-user context leakage vulnerability. Fixing this does not require migration; it requires a one-thread-per-user-session policy enforced in the session management layer.

## References

- Shared tool-use control model → [tool-use-execution-security/SKILL.md](../tool-use-execution-security/SKILL.md)
- Attachment and observability leakage controls → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Framework notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
