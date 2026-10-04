---
name: mine-rs-documentation
description: Use this skill when writing or updating mine-rs documentation, README, roadmap, backlog, AGENTS.md, architecture docs, product scope, Spanish technical docs, conceptual examples, or consistency across project docs.
---

# mine-rs documentation skill

Use this skill for documentation, roadmap, README, AGENTS.md, backlog and architecture writing tasks.

## Source of truth

For documentation changes, inspect the relevant files:

1. `README.md`
2. `AGENTS.md`
3. `docs/backlog.md`
4. `docs/references/vision.md`
5. `docs/references/product-scope.md`
6. `docs/references/domain-capabilities.md`
7. `docs/references/architecture.md`
8. `docs/references/repository-strategy.md`
9. `docs/references/python-sdk-design.md`
10. `docs/references/agentic-layer.md`
11. `docs/references/roadmap.md`
12. `docs/references/temporal-backlog.md`

## Writing conventions

- Write primary project documentation in Spanish.
- Use clear, professional and practical language.
- Distinguish current state, target architecture and future roadmap.
- Mark non-implemented API examples as conceptual.
- Keep `docs/backlog.md` as operational backlog.
- Keep `docs/references/repository-strategy.md` as the source of truth for repo/crate/package decisions.
- Avoid claiming that planned features already exist.

## Documentation procedure

1. Determine whether the change is product, architecture, domain, Python SDK, agentic layer or roadmap.
2. Update the most specific document first.
3. Update README if discoverability changes.
4. Update AGENTS.md if future agent behavior should change.
5. Keep terminology consistent across docs.
6. Check links after edits.
7. Keep examples short and label conceptual examples.

## Preferred terminology

- "SDK" for the reusable library surface.
- "Rust core" for deterministic compute.
- "Python SDK" or `python/miners` for user-facing Python.
- "`mine-tools`" for deterministic tool contracts.
- "`python/mine-agents`" for Python-first agentic orchestration.
- "Capa agentica" for agents, VFS, task tools, subagents and verifiers.

## Gotchas

- Do not turn the project into a GUI-first product in docs.
- Do not blur SDK responsibilities with agent responsibilities.
- Do not duplicate roadmap details if the backlog already owns ticket-level execution.
- Do not remove the monorepo decision unless explicitly asked to reevaluate it.
