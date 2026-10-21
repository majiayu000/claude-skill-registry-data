---
name: code-browser
owner: baseline
description: The primary tool for code-navigation questions in ANY language (frontend or backend) — walk the structural graph from an entry point (page, route, handler, command, `main`) down through imports to the IO boundary (network call, query, file read). Use this skill, in preference to the Explore agent or global grep, whenever the user asks "where does X come from?", "what API/data populates Y?", "what renders or wraps the Z panel?", "which file for feature F?", "how is this wired up?", or any code-navigation question mapping a UI element, route, or feature concept to source files. Also reverse queries ("what uses /api/foo?", "who consumes this service?"). Keyword search routinely picks up unrelated flows sharing a domain word and produces wrong answers; the walk follows the actual graph. The JS/TS `walk.mjs`/`discover.mjs` are an optional accelerator, not required — the walk is language-agnostic.
---

# Code Browser

A natural code-traversal skill. Answers "where does this come from?" by walking from the entry point downward, not by string-searching for the name.

It is the **primary** path for code-navigation questions in any language (CLAUDE.md Article X.5): the universal walk is the first attempt; reach for the `Explore` agent or `grep` only when the repo has no resolvable structure or the walk dead-ends. Pure full-text search and direct type/util definition lookups stay with `grep` — they are not navigation.

## When this skill exists

The user-visible label of a thing (a third-party integration's icon, a "Refresh" button, a panel header) is rarely the right keyword to grep for. The same word often appears in unrelated flows — e.g., grepping a vendor's product name can land on an unrelated documents API while the icon itself is rendered by a generic integrations registry that fetches a different endpoint. The reliable path is always top-down: start at the page, follow imports, stop at the network boundary. This skill encodes that walk and supplies a fast helper so it costs essentially nothing.

## The universal walk

This works on any codebase, regardless of framework:

1. **Locate the entry point** for the user-visible thing. For web: the page/route file. For a single-page app, the screen component. The user's question almost always names the page directly or implicitly (e.g. "the loan-application page").
2. **Read the entry point and follow imports downward.** Note components rendered (JSX, route children), data hooks called (`useFoo()`), and service/API helpers invoked.
3. **Stop at a network/IO boundary**: a `fetch`/`axios`/SDK call, a SQL query, a file read. The URL or query you find there is the answer.
4. **Verify**: open the leaf file once with `Read` and confirm the URL/symbol is still what the cache claims.

If at any point you find yourself globally grepping for the user-visible label, stop — you've left the walk.

## Optional accelerator (JS/TS only): `walk.mjs`

The universal walk above is the primary path and works on any language. For **JS/TS** codebases this skill has been initialized in (i.e. `conventions.json` exists alongside this file), an **optional accelerator** does the walk deterministically in milliseconds and returns the entire reachable graph as JSON with flat indexes — no per-step LLM round trips. On other languages (Python, Go, Rust, …) `walk.mjs`/`discover.mjs` do not apply — do the universal walk by hand with `Read`; that is the primary mechanism, not a fallback.

```bash
node .claude/skills/code-browser/walk.mjs --page <entry-file-path>
```

Output shape (truncated; values are illustrative placeholders — the actual symbols and paths come from the repo being walked):
```json
{
  "entry": "src/app/<route>/page.tsx",
  "summary": { "filesVisited": 120, "hooks": 18, "services": 14, "apiCalls": 22, "components": 95 },
  "indexes": {
    "byHook":      { "useGetWidgets": { "file": "src/context/widgets/hook.ts" } },
    "byService":   {
      "getWidgets":     { "file": "src/services/widgets/get-widgets.ts", "isDefault": true,  "apiCalls": [{"method":"GET","url":"/api/v1/widgets"}] },
      "getWidgetById":  { "file": "src/services/widgets/get-widgets.ts", "isDefault": false, "apiCalls": [{"method":"GET","url":"/api/v1/widgets/:param"}] },
      "listGadgets":    { "file": "src/services/gadgets/list-gadgets.ts", "isDefault": true,  "apiCalls": [{"method":"GET","url":"/api/v1/gadgets?..."}] }
    },
    "byApiCall":   { "GET /api/v1/widgets": "src/services/widgets/get-widgets.ts" },
    "byComponent": { "WidgetPanel": "src/components/dashboard/widget-panel.tsx" }
  },
  "tree": { /* nested file -> children, with rendersComponents, usesHooks, apiCalls per node */ }
}
```

**Reading the output efficiently** — for big trees (the output can run to hundreds of KB), don't read the whole JSON into context. The shape is intentional: `entry`, `summary`, and `indexes` come first and are small. Use `Read` with a small `limit` (~200 lines) to get just the head; that's almost always enough. Only fall back to reading the `tree` section if a question requires "which component renders this hook" or similar parent/child information that the flat indexes don't answer.

**How to use the output:**
- Scan `indexes.byHook` / `byService` / `byComponent` for symbols that match the user's question (substring or fuzzy). The flat indexes exist so you don't have to recurse the tree manually.
- **`byService` is keyed by exported function, not by file.** A single service file can export many functions, each with its own URL — for example `getWidgets` and `getWidgetById` may both live in `get-widgets.ts` but hit different endpoints. Match the question's topic to the **function name** in `byService` and use that function's URL. Do not assume the file's default-export URL applies to all functions in the file.
- The page's `tree` node lists `importedAs: [...]` showing which specific functions it actually imports — consult that to confirm which `byService` entry applies.
- Walk the `tree` when you need parent/child relationships — e.g., "which component wraps X" or "which component renders X". `byComponent` tells you where a component is *defined*; the tree tells you who *renders* it.
- For reverse queries ("what page uses /api/foo?"), walk the relevant page(s) and check their `byApiCall` index — or walk from each candidate page and inspect.

## Walker vs LLM: who does what

The walker is deterministic — fast, free, gives you complete facts about the import graph and reachable URLs/components. You're the navigator — read what the user is actually asking and decide which facts matter. Best results come from mixing them.

**The walker handles** (facts):
- Listing every URL, component, and hook reachable from a page
- Mapping a function/hook/component name to its defining file (`byHook`, `byService`, `byComponent`)
- Confirming a literal still exists at a path
- Route-path → page-file resolution (Next.js: a route like `home/c/[channelId]/p/[pid]/dashboard` maps deterministically to `src/app/.../dashboard/page.tsx`)

**You handle** (judgment):
- Picking among multiple candidates the walker surfaces — match the question's wording to function/component names
- UI-element references ("the icon", "the panel on the right", "the documents list") — read the JSX of relevant components to see what's actually rendered where
- Vague questions — ask back, or pick the most central candidate with reasoning
- Cross-cutting concerns (analytics, error tracking, side effects) — not modeled by the walker
- Genuine ambiguity — when two URLs or two components both reach the page and both fit the question, name both and give your best guess with reasoning
- **Choosing whether to use the walker at all** — direct concept-to-file lookups (see Example 4 below) don't need it

**Strategic mix**: walker narrows the search space (e.g. 86 URLs → 5 task-related ones), you pick the right one by reading question intent against function/component names, walker confirms with one `Read`.

## Caching and freshness

Results are cached at `cache/trees/<hash>.json` per entry file. On reuse the walker compares every visited file's `mtime` against the cache build time; if any descendant is newer, the cache is rebuilt automatically.

**Always verify the leaf — but only confirm, don't substitute.** A cached path is a hypothesis. Before quoting a URL or service to the user, do one `Read` on the leaf service file that `byApiCall` names — confirm the URL literal is present. **If the service file contains multiple functions with multiple different URLs, do NOT switch to a different URL just because its function name sounds more relevant to the question.** The `byApiCall` entry already resolved which specific call the page reaches; your only job is to confirm that URL literal still exists in the file. For example: if `byApiCall` says `GET /api/v1/<resource-a>/:param` and the leaf file also contains a sibling function calling `/api/v1/<resource-b>`, do not substitute — the page reaches `<resource-a>` and that is the answer, even if `<resource-b>` sounds closer to the question topic.

If the walker fails or returns a partial tree (e.g., dynamic imports, conditional renders the walker can't see, unusual export patterns), fall back to the procedural walk: open the entry file by hand, read what it renders, recurse. The walker is an accelerator, not a contract.

## Adapting to a new codebase

`conventions.json` records *where each layer lives* in this specific repo. If it's missing, or if the repo has been refactored, regenerate it:

```bash
node .claude/skills/code-browser/discover.mjs
```

`discover.mjs` reads `tsconfig.json` for path aliases, samples `package.json` for the framework, finds layer directories under `src/`, and detects the API URL prefix by sampling service files. It writes both `conventions.json` (consumed by `walk.mjs`) and `conventions.md` (a human-readable summary you can read for context).

The universal walk works without `conventions.json` — it's only required for the fast path. If conventions don't exist and the repo doesn't follow common conventions you can infer, just do the walk manually with `Read`.

## What this skill is not for

- **Writing/editing code**: this is a *read* skill. Don't use it to refactor.
- **Finding type definitions / utility implementations**: those live in skipped dirs (`src/types/`, `src/utils/`). Grep is fine there — the keyword-as-name correspondence is usually direct.
- **Pure full-text search**: for "find every file containing string X", use `grep` directly. Use this skill when the question is about *structure or wiring* — what data drives a UI element, what wraps a component, where a feature's code lives — rather than substring matching.

## The single most common mistake: name-similarity over walker truth

When `byApiCall` shows several URLs and one of them *sounds* like the question's topic, that is **not** how you pick. The right URL is the one that the **specific page's subtree** reaches — not the one whose name best matches the keyword. The walker already filtered for "reachable from this page". Trust that.

Concretely:
- If the question is about a page whose subject is "X" and `byApiCall` has both an `/api/.../X` endpoint and a sibling `/api/.../Y` endpoint, do **not** pick `/X` because the page is about X. The walker already filtered for reachable calls from this page — if `/Y` is the one in the tree, that is the answer. Pages routinely call APIs whose name is unrelated, opposite, or more general than the page's purpose (a "manage Xs" screen may fetch a related entity to compare or assign; two screens often reuse the same generic endpoint).
- If the question asks about a domain term and `byApiCall` has both a general-sounding URL (`.../get_all_things`) and a more specific-sounding URL (`.../get_user_things`), do **not** substitute the more "intuitive" one. Report exactly the URL the walker found for this page's subtree, even if it sounds generic.
- If the question's topic word matches two URLs in the index, prefer the one whose `:param` path-shape matches what a real call from this page would look like. When in doubt, walk the tree from the page node to confirm which leaf the call actually reaches.

A distinct but related failure mode: substituting an endpoint that is entirely **absent** from the page's `byApiCall`. `byApiCall` is exhaustive — every URL statically reachable from the page's import chain is listed there. If an endpoint does not appear in `byApiCall`, the page does not call it. Do not add endpoints sourced from Grep results, prior knowledge, or intuition about what the page "should" call. For example: if `byApiCall` for a page lists only the "all items" endpoint, do not report a hypothetical "user-scoped items" endpoint even if it sounds more user-specific — it is not in the tree, so this page does not reach it. The walker's list is the ground truth; anything outside it is speculation.

If you find yourself reasoning "the URL contains the same word as the question, so it must be the answer", stop. Re-read `byApiCall` for this page only.

## Worked examples

These show how the walker + LLM judgment combine across different question shapes. The skill exists for all of them, not just data-flow traces.

> The examples below use generic concepts (notifications, search, cart, etc.). Substitute the equivalent file paths and component names from `conventions.md` for the actual codebase you are working in. The walk shape is the same regardless.

### Example 1 — Data trace ("where does the data come from?")

**Question**: *"Where does the notifications list come from on the inbox page?"*

1. Identify page → resolve "inbox" against the framework's routing convention (e.g. `src/app/inbox/page.tsx` for Next.js app-dir, `pages/inbox.tsx` for pages-dir).
2. `node walk.mjs --page <file>` → tree + indexes.
3. Scan `byService` for `notification` → a handful of candidates with URLs attached. Match "notifications list" to e.g. `getUserNotifications` (not `markNotificationRead`, `subscribeNotifications`, etc. — function names disambiguate).
4. `Read` the leaf service file → confirm the URL literal.
5. **Answer**: `GET /api/v1/notifications` at the leaf service path.

### Example 2 — Component to modify for a UI feature

**Question**: *"We need to add a download-CSV button to the report panel on the analytics dashboard."*

This is a *component-tree* question — the user wants the file to edit, not the API to call. API tracing alone won't help; the answer is a React component.

1. Identify page → the analytics dashboard's page file.
2. Walk it.
3. Scan `byComponent` for terms from the question (`ReportPanel`, `Report`, `Export`). The page's subtree typically renders a layout component, which in turn renders the named panel.
4. Follow the `tree` downward from the page to find where the report panel + its UI actually lives.
5. **Answer**: the component file containing the panel's JSX, e.g. `src/components/analytics/report-panel/index.tsx`. That's the file to edit.

### Example 3 — Find the wrapper / parent component

**Question**: *"Show me the wrapper for the search results list."*

1. Identify page → the search page.
2. Walk it.
3. Search `byComponent` for `SearchResultsList`. The wrapper file is named with a `wrappers/` or `containers/` convention if the project uses one.
4. Confirm via the `tree` that the page's content component loads the wrapper (chain: page → `SearchContent` → `SearchResultsListWrapper` → inner list).
5. **Answer**: the wrapper file path, e.g. `src/components/search/wrappers/search-results-list.tsx`.

### Example 4 — Direct concept-to-file lookup (no walk needed)

**Question**: *"Show me the reducer for the cart state."*

This is a *structural* lookup — the answer is derivable from convention alone. Walking is overkill and slow.

1. Read `conventions.md`: contexts/state live under a convention path like `src/context/<feature>/` or `src/store/<feature>/`, and each feature directory typically contains files like `reducer.ts`, `actions.ts`, `hook.ts`, `types.ts`.
2. "Cart" → the cart feature directory.
3. Reducer → `reducer.ts`.
4. **Skip the walker.** Use `Glob` or just confirm the path with one `Read`.
5. **Answer**: e.g. `src/context/cart/reducer.ts`.

Use this pattern whenever the question names a feature **and** a kind of file (`reducer`, `types`, `mutations`, `hook`, `context`, `service`). Those map deterministically to convention paths — no traversal needed.

### How to decide which example pattern applies

| The question is about… | Use… |
|---|---|
| Data shown on a page (lists, fields, status) | Example 1 — page → walker → `byService`/`byApiCall` |
| Adding/modifying a UI feature on a page | Example 2 — page → walker → `byComponent` + `tree` |
| What wraps / contains a component | Example 3 — `byComponent` + `tree` parent navigation |
| A specific *kind* of file (reducer, types, hook) for a named feature | Example 4 — conventions + `Glob`, skip the walker |

When in doubt, lean on the walker — even if it ends up being unnecessary, it costs ~300ms and gives you grounded facts. Reaching for `grep` should be a last resort, not a first instinct.

## Failure modes to watch for

- **Dynamic imports / lazy loading**: the walker follows static `import` statements. Components loaded via `React.lazy(() => import(...))` may need manual follow-up.
- **Renamed re-exports** (`export { Foo as Bar } from "..."`): the regex parser sees the new name but may not perfectly track the original. Verify with one Read at the leaf.
- **Server vs. client boundary** (Next.js): a server component may pass data to a client component which then uses a hook. Walk follows the import chain across this boundary.
- **Stale conventions**: if `discover.mjs` was run before a refactor, the layers may have moved. Re-run it.

In all of these, the universal walk by hand is the safety net.
