---
name: code-audit-expert
description: Critically audit refactorings and design decisions against the real codebase, verify claims vs code, score only relevant quality axes, and write evidence-based tech reports. Use after refactors, when reviewing agent-reported work, or when asking for architecture / ISP / DRY / token-cost / reliability feedback. For builtin MCP tool audits, prefer critique-builtin-tool or lean-builtin-tool-auditor instead.
---

# Code Audit Expert

Audit completed work against the codebase. Prefer skepticism over praise. Every claim needs a file/line or a measured number.

## Scope routing

- **Builtin MCP tools** (schema, hints, Tool Design Manifesto): use `critique-builtin-tool` or `lean-builtin-tool-auditor`.
- **This skill**: architecture fit, claim verification, DRY/ISP, token/cost impact, side effects after refactors or feature work (TS/React, Rust, shared libs).

## Workflow

1. **Gather context** — Changed files, PR notes, agent summary. Treat summaries as claims, not facts.
2. **Verify against code** — Open the actual implementations. Build a claim→evidence table (see template §2). Mark invents, mismatches, and unstated gaps.
3. **Analyze only what applies** — Interface fit (ISP), duplication/abstraction (DRY), cost (tokens/caching), reliability/side effects. Skip irrelevant axes.
4. **Report** — Follow [reporting-template.md](references/reporting-template.md). Write under `.libragent/work/` (e.g. `.libragent/work/code_audit_report.md`). Do not invent paths.

## Hard rules

- **No fabricated metrics.** Do not invent token savings, coverage %, speedups, or “100% tests” unless you measured them in this session. Prefer qualitative statements or cite the command/output.
- **Score only relevant axes.** Irrelevant rows = `N/A` with one-line reason. Never force a 5/5 for flavor.
- **Cite evidence.** Prefer `path:line` or short quoted snippets. Star ratings without citations are invalid.
- **Surface risks.** Side effects, regressions, and remaining debt go in the report even when the change is otherwise good.
- **Language.** Skill instructions are English. Match the user’s language for the written report (Korean user → Korean report is fine).

## Critique checklist (inline)

Use when scoring; omit items that do not apply.

- [ ] Claims in the agent/PR summary match the code
- [ ] Public contracts (schemas, APIs, tool responses) stay coherent for consumers
- [ ] Shared logic is extracted once (not copy-pasted) without over-abstraction
- [ ] Hot paths / LLM context avoid redundant payload echo
- [ ] Error handling and limits (size caps, LCS bounds, etc.) are explicit
- [ ] Tests cover the new contract fields and failure modes that matter
- [ ] Feature-flag / build-variant behavior is consistent where dual builds exist

## Consumer / dependency check

When changing a core type or service (example: `BaseAIService` / `src/lib/ai-service/base-service.ts`), inspect call sites for correct type narrowing and broken assumptions—not only the edited file.
