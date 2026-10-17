---
name: agentic-coding
category: Engineering & code
blurb: Gets reliable work out of coding agents — tight specs, fast feedback loops, and guardrails so automated coding helps instead of creating chaos.
example: Help me spec a small feature so a coding agent can build it safely.
---
# Agentic Coding

Coding agents multiply output — and chaos, if undirected. The skill is making them **reliable**: clear specs, tight feedback loops, and deterministic guardrails so you're not just hoping the model behaves.

## Claude Code building blocks (from the guide)
- **Hooks** (lifecycle: PreToolUse, PostToolUse, etc.): intercept, validate, format, and log agent actions. Use them as deterministic guardrails — block edits to protected paths, auto-run formatters, run tests after every edit, deny secrets. Don't rely on the model's goodwill; wire the policy.
- **Sub-agents:** delegate bounded tasks to focused agents; keep each one's context narrow; orchestrate planner -> worker -> reviewer patterns.
- **MCP tools:** extend the agent with external tools/data via Model Context Protocol servers — prefer typed, narrowly-scoped tools over broad ones.
- **Events & payloads:** know what each hook/event carries so your automation is precise, not guesswork.

## Disciplines for reliable agentic coding
- **Spec first, small vertical slices.** Review diffs — never rubber-stamp.
- **Tight feedback in the loop:** tests + linters wired into hooks so the agent gets automatic signal.
- **Context hygiene:** give the agent only what it needs. Pull files into a workspace (the `town-github-coding-workflow` VFS pattern) rather than dumping the whole repo.
- **Guardrails:** protected paths, no secrets, **no Docker** (house rule), staging-first.
- **Human-in-the-loop on irreversible actions; autonomous on safe, reversible ones.**

## His multi-agent patterns
LocalForge (Planner -> Writer -> Reviewer -> Tester), reliable-engineering-agent (disciplined agent), guardian-agent (Guardian Mesh security), autocoder/argent (local GGUF + **WASM sandbox** for untrusted execution). The disciplines above are exactly what make these dependable.

## Tie-ins
`senior-fullstack-engineer` (the craft the agent must uphold) · `town-github-coding-workflow` (VFS -> branch -> atomic commit -> PR) · `phased-delivery` (plan before the agent builds) · `security-zero-knowledge` (sandbox untrusted agent execution — the argent WASM model).

## Anti-patterns to refuse
- Letting the agent run unbounded; rubber-stamping diffs; no automated tests in the loop; dumping whole repos into context; agents with broad write access and zero guardrails.