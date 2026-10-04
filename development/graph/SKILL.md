---
name: graph
description: Use when the user wants to build, refresh, or visualize the repo's knowledge graph — code structure plus the committed wiki/ — via graphify. Produces an interactive graph + a GRAPH_REPORT.md of God Nodes, surprising connections, and suggested questions. Trigger on "/graph", "build the knowledge graph", "graph the repo", "map the codebase", "refresh the graph", "visualize the second brain".
---

# Knowledge Graph (graphify)

Build a map of how this AIOS actually fits together — which code files and which wiki notes depend on, reference, and cluster with each other — so you can see the structure instead of guessing it. Powered by **graphify** (a knowledge-graph builder), scoped hard to what's safe to graph.

## When to run
- The user asks to see how the repo / second brain hangs together ("map the codebase", "graph the repo").
- After meaningful structural change — new skills, tools, SOPs, or a `/wiki` loop that added entries — to refresh the picture.
- As a thinking aid before a refactor, an audit, or a `/weekly` review: *what's load-bearing, what's orphaned, what's surprisingly connected.*
- Before exploring with `/graph-query` (this builds/refreshes the graph it queries).

## The output (always this shape)
graphify writes everything to **`graphify-out/`** (git-ignored — a derived artifact, never committed):
```
## Knowledge graph — <date>
**Built from** — code (local AST) + committed wiki/. Excluded: raw/, .tmp/, .env, secrets.
**Artifacts** — graphify-out/graph.html (interactive) · graph.json · GRAPH_REPORT.md

**God Nodes** — the most-connected hubs (what everything leans on):
1. <node> — <why it's central, in a phrase>
2. … 3. …
**Surprising Connections** — edges you wouldn't expect (cross-domain links worth a look):
- <A> ↔ <B> — <what the link is>
**Suggested Questions** — what the graph invites you to ask next:
- <question> → run `/graph-query "<question>"`
```
Every edge carries graphify's honesty label — **EXTRACTED** (read directly), **INFERRED** (reasoned), or **AMBIGUOUS** — so claims about the graph cite their basis (cite-don't-invent).

## Process
1. **Ensure graphify is installed.** Run `python tools/graphify_setup.py check`. If missing, offer to install (`uv tool install graphifyy`, fallback `pipx install graphifyy` / `pip install graphifyy`, then `graphify install --platform claude`). No account or signup is needed. **Gate:** don't proceed until `graphify --version` resolves.
2. **Set the build scope — code + committed `wiki/` ONLY.** This is the hard line:
   - **Include:** source code (Python in `tools/`, etc.) and the committed `wiki/`.
   - **EXCLUDE always:** `raw/` (may hold raw PHI/PII/financials before de-identification), `.tmp/`, `.env`, `graphify-out/`, and any sensitive/secret path. **Never** point graphify's document extraction at `raw/`.
   - Why this is safe: code is parsed locally by tree-sitter AST (no LLM, nothing leaves the machine); document extraction is limited to `wiki/`, which is already de-identified and non-confidential per the wiki admission policy. graphify also auto-skips sensitive files during detection — but scope, not that fallback, is your guardrail.
3. **Build the graph.**
   - **Full build (code + wiki):** the heavy document pass runs through graphify's own pipeline using the host IDE session — invoke `/graphify .` (graphify's global skill), having confirmed scope. Non-code text in `wiki/` is extracted by *this* session; graphify does not call any third party or read `ANTHROPIC_API_KEY` in-IDE.
   - **Code-only refresh (no LLM, fast):** run `graphify update <path>` — re-extracts the code AST deterministically, no model call. Prefer this when only code changed.
   - **Gate:** confirm `graphify-out/graph.json` and `GRAPH_REPORT.md` were written before reporting.
4. **Surface the highlights.** Read `graphify-out/GRAPH_REPORT.md` and summarize into the output shape above — God Nodes, Surprising Connections, Suggested Questions — keeping the EXTRACTED/INFERRED/AMBIGUOUS labels. Point the user at `graphify-out/graph.html` for the interactive view.
5. **Offer the next move.** Propose `/graph-query "<question>"` to explore (shortest paths, neighbors, communities), and — if the user wants it standing — `graphify hook install` for auto-rebuild on commit (a Cadence touch) or `--watch` for continuous rebuild while working.

## Autonomy
**L2 — drafts/refreshes the graph; the human reads it.** Building is reversible and lands only in git-ignored `graphify-out/`, so it's safe to run on request. A **code-only `graphify update`** (deterministic, no LLM, no document pass) can run at **L3** — e.g. via the commit hook — once trusted. Never commit `graphify-out/`; never widen scope beyond code + `wiki/` without explicit approval.

## Guardrails (from CLAUDE.md)
- **Never extract `raw/`** (or `.env`, `.tmp/`, secrets) — `raw/` can hold pre-de-identified PHI/PII/financials. Document extraction is limited to the committed, de-identified `wiki/`. (Guardrails #1, #2, #7)
- **`graphify-out/` is git-ignored** — a derived artifact. No secrets, confidential figures, or sensitive data enter git via the graph.
- **Cite, don't invent.** Carry graphify's honesty audit trail (EXTRACTED / INFERRED / AMBIGUOUS) into any claim about the graph. (Guardrail #6)
- Code AST is parsed locally; the wiki document pass uses this host session only — no third-party call, no `ANTHROPIC_API_KEY` read.
