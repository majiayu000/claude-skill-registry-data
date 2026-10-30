---
name: optimize-agent-usage
description: Reduce or diagnose agent usage of tokens, credits, and context without weakening task quality or safety. Use only when the user explicitly asks to save credits, tokens, or usage limits in the current agent host; optimize Skills, instruction files such as AGENTS.md or CLAUDE.md, MCP, or context loading; explain unusually high usage; or design a lower-consumption workflow. Do not use for ordinary coding, software performance work, or generic cost questions.
---

# Optimize Agent Usage

Reduce total agent consumption while preserving the requested outcome,
authorization boundaries, safety checks, and completion evidence.

Defaults you may adapt, saying so: the Optimization Order sequence where no check depends on it, and report layout. Every other rule here and in the references this skill loads binds.

## Load Policy

- For a conceptual explanation or a narrow current-product fact, use this file
  and the current host's official documentation only. Do not inspect a
  repository or load the audit reference unless the request needs it.
- For an audit, design change, or implementation involving Skills, instruction
  files, MCP, context, history, tools, validation, or reporting, read
  `references/context-audit.md` before changing files.
- Add another Axiom skill only when the requested implementation crosses into
  that skill's distinct owner: an AGENTS instruction system, traceable Git
  state, or a persistent system change. Usage analysis alone needs only this
  skill.

## Measurement Boundary

- Use exact token, credit, cache, reasoning, or tool metrics only when the host
  exposes them for the scoped run. Axiom cannot recover hidden usage data.
- Otherwise label UTF-8 bytes, words, lines, reference counts, tool calls, and
  route-chain sizes as proxies or estimates.
- Do not claim a percentage saving without a repeatable before/after workload
  and equivalent quality acceptance.
- Fetch the current host's official documentation only when a volatile host
  fact affects the decision. Never place current prices, plan limits, or model
  quotas in always-loaded instructions.

## Non-Negotiable Boundaries

- Define the required quality, safety, authorization, rollback, and evidence
  bar before optimizing. Lower resource use counts only when that bar still
  passes.
- Do not remove required tests, rollback checks, secret handling, destructive
  safeguards, or outcome-owning evidence to reduce context or calls.
- Do not automatically change the model, reasoning effort, execution mode, or
  host configuration. Offer a bounded comparison only when the user requests
  usage optimization and the host supports the choice.
- Preserve unrelated work. Do not reset, stash, clean, stage, commit, push,
  deploy, install tools, change user Skills, or mutate remote state without
  separate authorization.
- Do not add telemetry, background work, automatic updates, or network checks.

## Optimization Order

1. Bound the target workflows and representative requests.
2. Measure always-loaded and common-path context before rare worst cases.
3. Inventory metadata and route edges before reading bodies.
4. Read only candidate owners, then remove duplication or route detail behind
   one directly discoverable on-demand reference.
5. Reduce repeated tool calls, checks, updates, and reports only where the
   next decision does not depend on each intermediate result.
6. Re-run the same routing, authorization, safety, and outcome scenarios.
7. Stop when further reduction would trade away required quality or evidence.

Prefer precise trigger descriptions, one canonical owner per rule,
phase-specific references, bounded retries, conclusive stopping conditions,
and concise evidence-led reporting. Keep ordinary no-match work outside Axiom.

## Report

Lead with the implemented or recommended outcome. Include affected files or
surfaces, comparable before/after measurements, validation results, and real
unverified gaps. Omit repeated rationale, routine successful details, and exact
usage claims the host did not expose.
