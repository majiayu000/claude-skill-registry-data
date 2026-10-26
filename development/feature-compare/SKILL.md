---
name: feature-compare
description: Build a feature-parity table across N products of any kind (tools, frameworks, libraries, apps, services, platforms), grounded in each product's best-available source of truth (DeepWiki for open-source repos, official docs otherwise). Use whenever the user asks to compare, diff, benchmark feature sets, or "who supports what" across two or more products, even if they only say "compare X, Y, Z" or "does X have what Y has". Output is the parity table only, plus a one-line sources footer.
---

# feature-compare

Goal: an accurate N-product × M-feature parity table. Accuracy comes from asking each product's best source of truth, not from memory. Training knowledge is stale and products ship weekly, so every cell must come from a retrieved source or be marked unverified.

## Phase 0: Source plan (confirm once)

For each product, pick sources in priority order:

- **Open-source, public GitHub repo** → (1) DeepWiki `ask_wiki_question` on `owner/repo`; (2) official docs. DeepWiki goes first because answers are direct, token-cheap and backed by code. It can lag the repo, so docs are the staleness check (Phase 2).
- **Closed-source / no repo** → official docs (WebSearch + WebFetch, latest version/changelog).
- If the user didn't give a repo or docs URL, find it with WebSearch. If DeepWiki has no index for a repo, fall back to docs and say so in the footer.

Show a compact plan table (product | repo/docs | source order) and ask the user to confirm or correct in one message. Proceed on confirmation. DeepWiki is deferred: load only `mcp__DeepWiki__ask_wiki_question` via ToolSearch (`select:`). Use ask only, never `read_wiki_structure` / `read_wiki_contents`: they dump large pages into context, while ask returns a direct, code-backed answer for far fewer tokens.

## Phase 1: Feature extraction → union U

Per product, extract its user-facing feature list:
- DeepWiki: ask "List all user-facing features/capabilities of this project, grouped by area." One broad ask first, then follow-up asks per area ("anything else under <area>?") until answers stop adding features.
- Docs: fetch the docs index/nav, plus feature, settings, CLI-reference and changelog pages.

Then build U = union of all lists. Be smart about it:
- Merge synonyms and renamed concepts ("hooks" / "lifecycle events"); keep one neutral name.
- Feature = something a user can use or configure. Drop internal implementation details and marketing fluff.
- Split a feature if products differ in behavior inside it; merge if it's just naming.
- Group into categories (e.g. Tools, Extensibility, Permissions, Sessions, Integrations) so the table scans well.
- Scale to the products: usually 20–80 rows. If U balloons, merge near-duplicates rather than truncating.

## Phase 2: Verify every (product × feature)

For each product, check every feature in U:
- DeepWiki products: ask per feature (batch tightly related features in one question if M is large). Request: yes / partial / no, plus the file or symbol that proves it.
- Docs products: search the docs for the feature; absence after a real search = ❌, not-found-but-unsure = ❓.
- **Staleness check:** for every DeepWiki ❌ or 🟡, and for any fast-moving area, cross-check the latest docs, README or changelog. On conflict, trust the newer source and note it (e.g. "new in docs").
- Never guess. If the sources can't settle it, mark ❓.

## Phase 3: Gap discovery (expand U)

Phase 1 can miss features, so ask each product what U doesn't cover. Per product, pass the actual list:
- DeepWiki: ask "Apart from these features: [<U, as a real list>], what other user-facing features exist in this project?"
- Docs products: scan the docs nav, settings and changelog for anything not matching a row in U.

Merge genuinely new features into U (same synonym/granularity rules as Phase 1). Then backfill: run Phase 2 for the new rows against **all** products, because a feature found in one product still needs a verdict for the others. Repeat the gap ask only for products where the previous round found something new; stop when a round adds nothing (cap at 3 rounds).

## Parallelism

Default: one subagent per product, for Phases 1–3 (main thread builds U between phases and hands the full U to each Phase 2/3 agent, and merges new rows after Phase 3). Each agent returns, per feature: `status`, `note`, `source`. Keep agent outputs structured and short.
Only if the user explicitly asks, upgrade to per-feature (or per-feature-batch) subagents.

## Output

Return the table only, then one sources footer. No preamble, no commentary, no recap of steps.

- Rows = features (grouped under category rows), columns = products.
- Cell = status + note of at most ~5 words, e.g. `✅ built-in`, `🟡 via plugin`, `❌`, `❓ docs unclear`.
- Statuses: ✅ yes · 🟡 partial/needs extension · ❌ no · ❓ unverified.
- Footer: one line per product listing sources used (DeepWiki repo / docs URLs / fallbacks / date checked), then the legend.
