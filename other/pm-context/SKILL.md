---
name: pm-context
description: "Manage per-task document links and inject context into sessions. Manual invocation only — do NOT auto-trigger."
argument-hint: "get [KEY] | add <KEY> <URL> [LABEL] | remove <KEY> <MATCH> | annotate <KEY> [LABEL] [--regen-triggers] | list | manage"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, WebFetch
disable-model-invocation: true
---

Manage per-task document links. **Project-scoped**: stored per task at `<git-root>/.agents/tasks/<KEY>/links.md`, where the git root is `git rev-parse --show-toplevel`. Refuse outside a git repo. There is no pm-context-owned active-task pointer — an agent's **current Task** is derived from its validated session-bound plan, while `pm-roadmap.ts current-task` remains a launcher/dashboard projection only.

`.agents/tasks/` is **gitignored** (task links may carry internal URLs); the gitignore line is ensured by the pm-roadmap store, not by this skill. **All writes to `links.md` go through the pm-roadmap CLI → ops (lock + CAS) — never hand-edit the markdown.** pm-context's job is the fetch + trigger/summary extraction; it then persists the result via `links <KEY> add|remove`.

CLI setup (one block; capture the git root, install once):

```bash
repo_root="$(git rev-parse --show-toplevel)" || { echo "pm-context needs a git repo"; exit 1; }
(cd $HOME/.config/ai/skills/pm-roadmap && [[ -d node_modules ]] || npm install)
pm() { PM_ROOT="$repo_root" $HOME/.config/ai/skills/pm-roadmap/node_modules/.bin/tsx $HOME/.config/ai/skills/pm-roadmap/pm-roadmap.ts "$@"; }
```

Arguments: $ARGUMENTS

## System — the pm-* loop

One of four skills in a single project-management system. **This skill owns *context*** (a task's external links).

```
(pm-context · context)  ┐
(retro · memory)         ├──▶  (design · plan)
(pm-roadmap · backlog)  ┘
```
`pm-context`→links · `retro`→memory(per-task decisions) · `pm-roadmap`→backlog(items) · `design`→plan(reads all three). Each fact in the smallest file enforcing its invariant; views derived. A task owns its dir `<git-root>/.agents/tasks/<KEY>/`: `links.md` (this skill), `memory.md` (**retro** is the primary writer; the `manage` GUI is the other), `backlog.md`/`closed.md`/`task.md` (pm-roadmap). All are written through the pm-roadmap CLI → ops.

> In the subcommands below, `tasks/<KEY>/links.md` is the link file under `<git-root>/.agents/tasks/<KEY>/`. Resolve the git root once per invocation; refuse outside a repo.

> Every subcommand taking a KEY (`get`/`add`/`remove`/`annotate`) validates it against `^[A-Z0-9_-]+$` **before any filesystem access** — reject with the expected pattern. A lowercase or path-bearing KEY (`../foo`) must never resolve `tasks/<KEY>/links.md`, on read paths as well as writes. (The CLI re-validates the KEY too.)

## Subcommands

### get [KEY]

Inject a task's links — including TRIGGERS and Summary — into the current session so Claude can decide which documents to fetch.

1. Resolve KEY:
   - If KEY argument provided, use it
   - Else run `resolve-session` with the exact tool/id from the injected session-routing block, take its validated plan `id`, and call `pm get <id>` to read the owning Task `key`
   - If the session is unbound or `pm get` finds no linked open item, report "no Task is linked to this session-bound plan. Select/bind a linked plan or pass a KEY." and stop; never consult the main launcher

   ```bash
   PM_SESSION_TOOL="<injected session tool>" PM_SESSION_ID="<exact injected session id>" node "$HOME/.config/ai/lib/worktree.mjs" resolve-session --root "$repo_root" --tool "<injected session tool>"
   ```
2. Read `tasks/<KEY>/links.md`. If not found, run `list` and report missing key.
3. Output a header line followed by the file content verbatim:

   ```
   ## <KEY> — Task Context

   For each link below: if any TRIGGER matches the current task, fetch the URL with the appropriate tool (MCP/WebFetch). The Summary is a hint, not a substitute.

   <file content>
   ```

### add <KEY> <URL> [LABEL]

Add a single link to a task without starting the GUI, then auto-fetch its Summary and suggest Triggers.

1. If LABEL is omitted, auto-detect from URL pattern:
   - `jira.` → Jira, `wiki.`/`confluence` → Wiki, `/pull/\d+` → PR
   - `figma.com` → Figma, `github.com`/`oss.` → GitHub
   - `slack.com` → Slack, `notion.` → Notion, default → Link
2. Ensure the task exists — `pm task create <KEY> --title "<title>"` if it does not (`links add` refuses a non-existent task). Never hand-create the dir/file.
3. Read `tasks/<KEY>/links.md` (read-only). Reject if the URL is already present, or if LABEL collides with an existing label (case-insensitive). On label collision, suggest a numeric suffix (`Wiki-2`) and ask the user via interactive question prompt to confirm/override.
4. **Fetch** the URL using the appropriate tool (see Fetch Routing). The response takes one of two forms:

   **Path 1 — inline response (small pages):** parse the returned content directly, then proceed to step 5.

   **Path 2 — file-saved response (large pages, token limit exceeded):** the tool reports `Output has been saved to <path>`. Do **NOT** read the file in full. Run a grep-based identifier sweep on the saved file:
   - camelCase fields: `grep -oE '\b[a-z][a-zA-Z]+[A-Z][a-zA-Z]+\b' <path> | sort | uniq -c | sort -rn | head -40`
   - snake_case fields/endpoints: `grep -oE '\b[a-z]+_[a-z_]+\b' <path> | sort | uniq -c | sort -rn | head -40`
   - JIRA/issue IDs: `grep -oE '[A-Z]{2,}-[0-9]+' <path> | sort -u`
   - Experiment/feature IDs: `grep -oE '[A-Z]+-[A-Z]+-[0-9]+-[A-Z]+' <path> | sort -u` (adjust regex to your team's ID format)
   - API path tokens: `grep -oE '/[a-z][a-z_]{3,}(_[a-z]+){1,}' <path> | sort -u`
   
   Then `Read <path> limit:80` for title, TOC, and opening section. If a specific section is needed for Summary, use `Read <path> offset:N limit:M` selectively — never read the whole file.

5. **Extract** Summary and Triggers from whichever source step 4 produced (inline content or grep+selective-read output):
   - **Summary**: one-line description (page title + brief context, ≤120 chars)
   - **Triggers**: 5-13 keywords/short phrases, comma-separated, prioritized in this order:
     1. **Code identifiers (highest priority)** — API endpoints (snake_case route segments verbatim from the document), data field names (camelCase fields verbatim), enum values (UPPER_SNAKE constants), JIRA/issue IDs (e.g. `PROJ-1234`, `REPO-567`), experiment/feature IDs (project-specific format), component/module names verbatim from the document
     2. **Domain-specific proper nouns** — project codenames verbatim from the document, domain abbreviations or category labels unique to your team (verbatim), specific feature labels that are unique to this codebase
     3. **Concept terms (last resort)** — only when the document lacks identifiers; use distinctive phrases, never generic words like "block", "slot", "page"
     
     The goal is grep-ability during code work. A trigger like a unique camelCase field name matches a code edit instantly; a generic noun phrase matches noisily across many files. Always prefer identifiers actually present in the document body. **Never invent triggers from outside the source — when in doubt, leave Triggers shorter.**

   On fetch failure (network, permission, 404): Summary `(fetch 실패)`, Triggers empty.

6. Persist the entry through the CLI (single write path — lock + CAS via ops; never hand-edit `links.md`):

   ```bash
   pm links <KEY> add "<LABEL>" --url "<URL>" --triggers "<comma-separated keywords>" --summary "<one-line summary>"
   ```

   Omit `--triggers` on fetch failure (leave empty) and pass `--summary "(fetch 실패)"`. The op upserts by label. The user can refine Triggers later via `manage` (GUI) — auto-extracted values are a starting point.
7. Read `tasks/<KEY>/links.md` back and output its content verbatim.

### remove <KEY> <MATCH>

Remove an entry from a task by label or URL substring match.

1. Read `tasks/<KEY>/links.md`. If missing, report and stop.
2. Find entries whose Label or URL contains MATCH (case-insensitive; top-level Link entries only).
3. If no matches, report and stop. If multiple, list them and interactively prompt the user to clarify so MATCH names exactly one.
4. Remove via the CLI (the op drops every link whose label or URL contains MATCH — pass a specific MATCH): `pm links <KEY> remove "<MATCH>"`.
5. Read `tasks/<KEY>/links.md` back and output its content verbatim.

### annotate <KEY> [LABEL] [--regen-triggers]

Re-fetch the Summary for one or all entries. Triggers behavior depends on current state:

- **Triggers empty** → auto-extract from page content (same prompt as `add`)
- **Triggers populated** → preserved (user authored them)
- **`--regen-triggers` flag** → force re-extraction even when populated (overrides user edits)

1. Read `tasks/<KEY>/links.md`. If missing, report and stop.
2. Determine target entries:
   - If LABEL provided, target only that entry (case-insensitive match; top-level Link entries only). Error if not found.
   - Else target all top-level Link entries.
3. For each target, fetch URL via Fetch Routing using the same two-path logic as `add` (Path 1 inline / Path 2 file-saved with grep sweep — see `add` step 4). Then compute the fields to persist:
   - **Summary**: the fresh one-line summary (or `(fetch 실패)` on failure) — always replaced.
   - **Triggers**: if currently empty OR `--regen-triggers` is set → auto-extracted keywords (5-13, same priority rules as `add` — code identifiers first, concept terms last); else → the existing Triggers verbatim.
   - Label/URL are never changed.
4. Persist each via the CLI (upsert by label — re-supply the unchanged URL and the resolved Triggers so they are preserved): `pm links <KEY> add "<LABEL>" --url "<existing URL>" --triggers "<resolved>" --summary "<fresh>"`. Then read `tasks/<KEY>/links.md` back and output it verbatim.

### current task (no `set`/`unset`)

There is no pm-context active-task pointer. The **current Task is the Task linked to the validated session-bound plan**. `get` with no KEY resolves the session plan id and then uses `pm get <id>`; standalone, stale, terminal, or unbound session states require an explicit KEY. `pm current-task` is reserved for launcher/dashboard projection and is not an agent-session fallback.

### list

List all task keys, marking the current one.

1. List keys (each task dir holding a `links.md`):
   ```bash
   for d in "$repo_root"/.agents/tasks/*/; do [ -f "$d/links.md" ] && basename "$d"; done
   ```
2. Resolve the active key with the same `resolve-session` → `pm get <plan-id>` flow as
   `get [KEY]`; an unbound session has no active marker.
3. Output one key per line; prefix the current key with `* `.
4. If empty, report no tasks.

### manage

Open the web GUI for full link management (Label, URL, Triggers, Summary).

1. Install dependencies if needed (subshell — do not change the working dir, the git root must stay resolvable):
   ```bash
   (cd $HOME/.config/ai/skills/pm-context && [[ -d node_modules ]] || npm install)
   ```
2. Check port:
   ```bash
   lsof -ti:8484 2>/dev/null
   ```
   If non-empty, kill stale process first:
   ```bash
   kill $(lsof -ti:8484 2>/dev/null) 2>/dev/null; sleep 1
   ```
   Conversely: if your own background server later exits with SIGTERM, a newer `manage` launch replaced it — do not relaunch reflexively; check the port first (a live listener means the replacement is already serving).
3. Start server in background. **Capture the git root BEFORE `cd`** and pass it as `TASK_CONTEXT_ROOT` (cd-ing first would make the server resolve the skill's own repo, not the project). One block — shell vars do not persist across calls:
   ```bash
   repo_root="$(git rev-parse --show-toplevel)" || { echo "pm-context needs a git repo"; exit 1; }
   cd $HOME/.config/ai/skills/pm-context && TASK_CONTEXT_ROOT="$repo_root" ./node_modules/.bin/tsx server.ts
   ```
   Use `run_in_background: true`.
4. Wait 2 seconds for server startup, then open browser:
   ```bash
   sleep 2 && { command -v xdg-open >/dev/null && xdg-open http://localhost:8484 || open http://localhost:8484; }
   ```
5. Prompt interactively:
   > 브라우저에서 작업이 끝나면 알려주세요.
6. When user confirms, kill server:
   ```bash
   kill $(lsof -ti:8484 2>/dev/null) 2>/dev/null
   ```
7. Reconcile: for each task, walk entries with empty Summary OR empty Triggers and run the `annotate <KEY>` flow. Per `annotate` rules, only empty fields are filled — populated Triggers stay intact.

## Fetch Routing

Pick the fetch tool by host and page type, in priority order:

1. **Authenticated / internal hosts** → the matching MCP server, per the internal routing table already loaded in context.
2. **SPA / client-rendered pages** → the `spa-fetch` skill, run headless — **bundled with pm-skills, but its Playwright browser needs a one-time setup** (`cd $HOME/.config/ai/skills/spa-fetch && npm install && npx playwright install`). Applies when the page body is rendered by JS so `WebFetch` returns only title/nav chrome with no field or endpoint identifiers — typical of Swagger UI (`/docs`, `/swagger`), Notion (`notion.so`), and Figma (`figma.com`) URLs.
   - **If `spa-fetch`'s Playwright browser is set up** (the script below runs), route here up front for those known patterns, or whenever a `WebFetch` summary degrades to a bare page title:
     ```bash
     [ -f $HOME/.config/ai/skills/spa-fetch/spa-fetch.js ] && node $HOME/.config/ai/skills/spa-fetch/spa-fetch.js <URL>; echo "EXIT:$?"
     ```
     - `EXIT:0` → parse stdout through the same Path 1 / Path 2 logic as `add` step 4.
     - `EXIT:10` (login required) / `EXIT:11` (bot wall) → the host needs an interactive browser session; do NOT drive login inside a batch add/annotate. Set Summary `(fetch 실패)`, leave Triggers empty, and tell the user to run `/spa-fetch <URL>` once to establish the session, then re-`annotate`.
     - `EXIT:1` → treat as fetch failure.
   - **If `spa-fetch`'s Playwright browser is not yet set up** → skip gracefully: fall back to `WebFetch` (#3); if that degrades to a bare title, set Summary `(fetch 실패)` and leave Triggers empty. (To enable richer SPA fetching, run the one-time setup above — see README.)
3. **Everything else** → `WebFetch`.

On fetch failure, use `(fetch 실패)` as the Summary. Never block the add/annotate flow on a single fetch failure.

## File Format

`<git-root>/.agents/tasks/<KEY>/links.md` is the single source of truth for a task's links (project-scoped).

A task's context has **two parts**: external **Links** (`links.md`, this skill) and per-task **Memory** (`memory.md`, retro-owned — decisions / things to remember). Both are this task's "context"; a `/pm-roadmap` backlog item belongs to the task by its directory (`tasks/<KEY>/backlog.md`), so it inherits this context. `links.md` holds **only links** — memory is its own file (no `## Memory` section here; the legacy in-file section is folded out once by `pm migrate`).

```markdown
# <KEY> — Links

- **<Label>**
  - URL: https://example.com/page
  - Triggers: keyword1, keyword2, keyword3
  - Summary: one-line description
```

**Field rules:**
- `Label`: required, **case-insensitive unique** within file (the CLI upserts by case-folded label), max 80 char, used as the block id / join key — free of `*` and newlines (the CLI rejects those)
- `URL`: required, must match `https?://` (the CLI rejects non-http), **unique within file** (the CLI rejects a URL already linked under another label)
- `Triggers`: optional, comma-separated keyword list (5-13 recommended — see `add` step 5)
- `Summary`: optional, single-line
- **Memory** lives in `.agents/tasks/<KEY>/memory.md` (`- **<title>**` / `Note:` / `Date:`), written by /retro (primary, via `pm memory add`) and the `manage` GUI; surfaced in `pm next` prompts and item context. It is **not** part of `links.md`.

**Parser:**
- Top-level `- **Label**` opens a link entry
- Sub-bullet `  - Key: Value` populates a field (Key is case-insensitive, value is trimmed)
- Unknown sub-bullet keys are ignored (forward compatibility)
- Sub-bullets without a parent are ignored
- The `add`/`remove`/`annotate` subcommands (including the `manage` reconcile pass, which reuses `annotate`) match **link entries only**, and **all of their writes go through `pm links <KEY> add|remove`** (lock + CAS via ops) — never a direct markdown edit. Memory is a separate file with its own writers (/retro, GUI).

## Current task (no pm-context pointer)

For agent flows, the current Task is **derived** from the validated session-bound plan when that plan is linked to an open Item: resolve the session read-only, then use `pm get <plan-id>`. The launcher/dashboard may continue to project its checkout-local selection through `pm current-task` and `GET /api/roadmap`; that explicit UI exemption stores no separate Task or Item navigation selection.

## Rules

- All Bash commands are pre-authorized via `allowed-tools` frontmatter — no user confirmation needed
- **Never hand-edit `tasks/<KEY>/links.md` — every write goes through `pm links <KEY> add|remove` (lock + CAS via ops).** That is the single write path; the GUI `manage` is the other writer (also via ops)
- The web GUI in `manage` writes the full schema (Label/URL/Triggers/Summary). The skill's `add` auto-extracts both Summary and Triggers from page content; the user can refine Triggers in the GUI afterward
- `annotate` overwrites Summary unconditionally. Triggers are auto-extracted only when empty; populated Triggers are preserved unless `--regen-triggers` is passed
- Task keys: uppercase alphanumeric, underscores, hyphens (`^[A-Z0-9_-]+$`) — enforced at every entry surface (skill subcommands, the CLI/ops, server API endpoints, GUI forms) before filesystem access
- On fetch failure, write `(fetch 실패)` as the Summary — never skip the entry
- Label/URL uniqueness is enforced by the `links add` CLI → ops (case-insensitive label upsert, unique URL per task — throws on a cross-label URL dup) and pre-checked by the skill's `add` (suggests a `Wiki-2` suffix on collision). The GUI `manage` is a full-state editor (links + memory written together via `ops.updateTaskLinks`); there is no per-link HTTP 409 in the new model
