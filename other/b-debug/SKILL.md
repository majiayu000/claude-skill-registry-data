---
name: b-debug
description: >
  Systematic hypothesis-driven diagnosis for runtime bugs, errors, broken
  behavior, slow paths, memory issues, and stack traces. Confirms root
  cause and produces a handoff with the exact runnable repro command,
  observable to flip, and confirmed causal mechanism, without editing
  product code. When the issue is not yet a confirmed product bug, it
  hands off cleanly instead of guessing. Unlike b-test, b-debug owns
  runtime behavior failures, not test-mechanic issues such as wrong
  assertions, mocks, or fixtures. Routing signals: bug, broken, stack
  trace, "not working", runtime error, regression, product regression,
  product bug, diagnose. Delegated: runs only in the `b-debugger`
  subagent; the main session never executes it itself.
metadata:
  phase: Decide
  execution_mode: subagent
  agent: b-debugger
---

<!-- Generated from skills/registry.yaml and skills/b-debug/prompt.md. Edit those sources, not this file. -->

# b-debug

Confirm the real cause of broken runtime behavior, then produce an evidence-backed handoff for the fix. Do not edit product code.

## Delegation boundary

`b-debug` runs only in the `b-debugger` subagent.

- Main session: reading this file prepares the handoff; it never authorizes running the steps below yourself. Gather the parent-owned evidence and confirm the effective `b-debugger.md` (project `.pi/agents/` over the Pi agent directory's `agents/`) is readable and its parsed frontmatter `tools` value, normalized to a list (comma-separated scalar or YAML sequence), is explicit, non-empty, and contains neither `edit` nor `write` (a missing, blank, or null `tools` grants them), then call `subagent` with agent `b-debugger` and a bounded task naming `b-debug`. Do not do this skill's work with your own tools, even for a quick, small, or single-lookup request. If the subagent is unavailable or fails, or its result notes an unknown agent type or `general-purpose` fallback (discard that result), report the gap and ask the user; never fall back to self-execution. Evaluate the returned result before any user-facing or worktree action.
- `b-debugger` child: execute the steps below read-only, return this skill's Output format to the main session, and do not delegate again.

## When to use

- The user reports a runtime bug, broken behavior, error, stack trace, race, memory issue, or slowdown.
- A failing test likely exposes a real product bug.

## When NOT to use

- The problem is only a test assertion, mock, fixture, or setup issue -> use **b-test**.
- The task is external docs/API lookup only -> use **b-research**.
- New scoped frontend/UI work -> use **b-frontend**; a clear non-UI change -> use **b-implement**; an unclear change -> use **b-plan**.

## Tool guidance

- `read` - inspect repository context and the main session's supplied reproduction evidence only when it materially affects the diagnosis.
- Read-only shell commands - inspect logs, diffs, and diagnostics; do not run mutating commands or state-changing probes.
- Native MCP tools - use only named read-only tools permitted to this subagent; report an unavailable or denied evidence gap to the main session.
- `codegraph` - per the kernel CodeGraph rule, trace entry-to-failure call paths in an indexed project; report an absent-index gap to the main session.
- `context7` - versioned dependency/API behavior only when a library suspect remains after local evidence.
- `firecrawl_developer_search` - upstream issue/PR history for a named dependency suspect remaining after local evidence; limit ≤5; query only the public package name, version, and public error text. Never send repository paths, code, private stack frames, internal URLs, or secrets; report that gap instead.
- Use only the reproduction and diagnosis evidence supplied in the current task; report missing historical context rather than assuming it.

## Steps

1. Establish a feedback loop from the main session's supplied failing test, CLI reproduction, HTTP/browser trace, replay, diagnostic output, or baseline measurement. The read-only child may run read-only diagnostic commands but does not create mutating probes.
2. Capture exact symptom, expected versus actual behavior, repro rate, determinism, and environment. Use read for repository context only when it materially affects the diagnosis.
3. Rank suspects from stack traces, diagnostics, recent changes, config, data shape, call paths, and the feedback loop.
4. Trace the call path from entry to failure with CodeGraph when an index is available; otherwise report the gap to the main session. Use Context7 only for versioned dependency suspects, and `firecrawl_developer_search` only for that suspect's upstream issue history.
5. Confirm the root cause before handing it off. If the supplied evidence cannot prove it, report the exact additional reproduction or diagnostic artifact the main session must collect rather than creating a probe.
6. When the cause is confirmed, produce a diagnosis handoff that names the next skill: **b-frontend** for a UI fix, **b-implement** for a clear non-UI fix, **b-test** for a test-only correction, or **b-plan** when scope remains unclear. Include the exact runnable repro command, the observable that must flip, and the confirmed causal mechanism. When it is unconfirmed, report the evidence gap and exact artifact needed instead of a confirmed diagnosis handoff.
7. Stop without editing product code. For performance work, include the baseline measurement in the handoff; the main session changes product code and reruns the same measurement.
8. If the issue is not yet a confirmed bug, say whether the next step belongs in **b-plan**, **b-research**, or **b-test**.

## Output format

For a confirmed cause: symptom, confirmed root cause, and evidence. Include the diagnosis handoff: target skill, exact runnable repro command, observable to flip, confirmed causal mechanism, and baseline measurement for performance work.

For an unconfirmed cause or bug: symptom, evidence inspected, remaining uncertainty, the exact additional reproduction or diagnostic artifact needed, and the next skill if known. Mark root cause and causal mechanism unconfirmed; do not invent a runnable repro command. Do not include a product fix in either case.

## Rules

- Do not patch speculatively or edit product code.
- Do not bundle redesign or cleanup.
- Use only named read-only MCP tools granted to this subagent; report any unavailable or denied evidence gap to the main session.
- If no trustworthy feedback loop can be built, report what you tried and what artifact/access is needed instead of guessing. Do not run mutating commands or probes that change system state.
