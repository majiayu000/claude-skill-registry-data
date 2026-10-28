---
name: lat-md
description: Use for explicit lat.md requests to install or configure its CLI, author linked project knowledge, validate or retrieve sections and references, or build and publish its knowledge UI. Not for generic Markdown, code-graph analysis, or persistent agent memory.
---

# lat.md

## Establish scope and CLI contract

Treat the current user request as the action boundary. Inspect the selected project's instructions and existing knowledge workflow before changing anything. Public documentation and local read-only inspection are safe; do not expand a retrieval request into setup, indexing, integration, or publishing.

The observed installation is global mise `npm:lat.md` 0.13.1. Do not reinstall by default. Read `lat --version`, `lat --help`, and the relevant `lat <command> --help`; installed help owns available commands, arguments, and flags. The observed command set includes `locate`, `section`, `refs`, `check`, `expand`, `paths`, `ui`, `search`, `reindex`, `gen`, `init`, and `mcp`, with global `--dir`. Do not assume online documentation matches the installed version or invent flags. For an explicit installation or upgrade, follow current official instructions and the user's runtime-management convention.

## Author and retrieve knowledge

Source Markdown is authoritative. Reuse the project's established `lat.md/` organization; author explanatory headings and sections, connect them with `[[links]]`, and use documented `// @lat:` code annotations for backlinks. Resolve actual section or symbol targets rather than guessing addresses. Consult the syntax and concepts references for exact annotation and addressing rules.

Choose the smallest relevant command:

- `locate`: find exact or fuzzy section names.
- `section`: retrieve section content and its references.
- `refs`: inspect incoming Markdown/code references.
- `expand`: resolve links into context.
- `check`: validate links, structure, and code references after authoring.
- `paths`: discover configured paths before editing configuration.
- `search`: retrieve natural-language matches when authorized for the configured backend.

Separate authored project knowledge from Graft's code-symbol/call graph and from persistent agent memory. None replaces or silently updates another.

## Control setup and data exposure

Never run `lat init` automatically in an unrelated repository: it creates knowledge structure and alters coding-agent files. Inspect the codified project workflow, identify affected files, and obtain consent for that scope before initialization. Do not configure MCP, generate/apply agent integrations, or publish by default.

Inspect backend/configuration before search or `reindex`; indexing may process private content. Obtain explicit consent before uploads or remote persistence. Never print credentials, and never promise embeddings or search remain local/private without evidence.

## Preview, build, and publish

Use installed UI help to distinguish local preview from local builds and external deployment. Static output is read-only and has no search; server output supports search. Inspect the actual generated local artifact before claiming a build works. A local artifact is not evidence of publication. Confirm exact destination, visibility, and content scope before external publishing, login, or upload; report the actual result and distinguish documented capabilities from observed behavior and unverified claims.

Before browser use, load available `agent-browser` and `agent-browser-policy` skills plus the installed CLI's bundled core instructions. If unavailable, use the active harness's documented owned browser tools; fail closed if none exist. Never guess selectors, authentication, APIs, or remote-saving actions.

## Official references

- [Quick start](https://www.lat.md/quick-start)
- [Commands](https://www.lat.md/docs/commands)
- [Syntax primer](https://www.lat.md/docs/syntax-primer)
- [Concepts](https://www.lat.md/docs/concepts)
- [UI and publishing](https://www.lat.md/docs/ui)
