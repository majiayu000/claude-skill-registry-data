---
name: opencode-repo-setup-skill
description: >-
  Interactive per-repo setup — opt-in MCP servers (project opencode.json wins),
  optional CodeGraph init, AGENTS.md rule blocks, built-in agent model pins
  (project or global scope), token-cost report. Triggers: set up mcp for this
  repo, repo setup, per-project enable, pin agent models, configure project
  opencode.
license: Apache-2.0
compatibility: opencode
metadata:
  harness: "opencode"
category: OpenCode Meta
---

## What I do

I am the **interactive frontend for per-project MCP enablement**. The global deploy ships most MCP servers disabled (zero always-on schema cost); this skill is how a specific repo opts in. I run in the primary session of the TARGET project (not the configurator repo):

1. **Detect** — scan the repo for setup signals
2. **Ask** — present a question-tool menu of opt-in servers + extras
3. **Write** — merge-write ONLY the delta into `<repo>/opencode.json` (Global-scope model pins instead target `~/.config/opencode/opencode.json`, backup-then-merge)
4. **Init** — optionally run `codegraph init -i`
5. **Report** — enabled set, estimated token cost, revert instructions

I never edit the global `~/.config/opencode/opencode.json` — sole exception: the agent model-pin extra when the user explicitly chooses Global scope (backup-then-merge, Step 3). Opencode merges project config over global with **project wins** semantics, so a one-key delta is all that's needed.

## When to use me

- User says "set up MCP for this repo", "enable Jira/Atlassian here", "project-level opencode setup"
- A marker rule fired (user AGENTS.md may say: if a repo's AGENTS.md mentions Jira/MCP needs, offer this skill)
- First session in a repo that carries its own `.opencode/` — offer to review/extend it

## Step 1 — Detect

Cheap, read-only scans (no network):

| Signal | Check | Suggests |
|--------|-------|----------|
| Existing project config | `<repo>/opencode.json` exists | Idempotent mode: show current overrides, offer to extend |
| CodeGraph index | `<repo>/.codegraph/` exists | codegraph already enabled locally; no action |
| Jira usage | AGENTS.md/README mentions Jira keys (`PROJ-123`), JIRA env vars, `atlassian` refs | offer `atlassian` enable |
| GitHub-centric | `.github/`, `gh` in scripts | gh CLI usually suffices; no MCP needed |
| Docs-heavy | `.docx`/`.pptx`/`.pdf` in repo | offer markitdown/docling packs |
| Frontend | `package.json` with next/react | offer next-devtools |
| Python | `pyproject.toml` | nothing MCP-specific by default |
| GitHub repo | `.github/` or GitHub remote present AND `.github/ISSUE_TEMPLATE/` absent | offer issue-template scaffold (Step 2 extras) |

Report findings in one table, then go to Step 2.

## Step 2 — Ask (question tool)

> Harness binding (§Portability contract): OpenCode — `question` tool. Claude Code — `AskUserQuestion`. Other/none — print the menu in a plain reply and wait; non-interactive → skip extras, apply defaults.

One multi-select question + one yes/no per extra. Options are built from the detection table — only show servers with a detected signal plus the general opt-in list:

**MCP enables** (any of):
- `atlassian` — Jira/Confluence tools (~5–6.5k tok/session when enabled; see caveats below)
- markitdown / docling / chrome-devtools / next-devtools / playwright / alpha-vantage / nanobanana — via global `--enable-pack` if not already enabled (alpha-vantage needs `ALPHA_VANTAGE_API_KEY`; nanobanana needs `GEMINI_API_KEY`)

**Extras**:
- "Initialize CodeGraph index? (`codegraph init -i`)" — only if `.codegraph/` absent and repo is code-heavy; on accept, also append the CodeGraph rule block (below) to `<repo>/AGENTS.md`
- "Append the LSP rule block to AGENTS.md?" — offer when a built-in LSP server matches the repo language (TS/JS → `typescript`+`eslint`; Python → `pyright`)
- "Scaffold a minimal project AGENTS.md?" — repo rules only; NO MCP prose (that belongs to config + this skill)
- "Scaffold GitHub issue templates? (bug report + feature request forms + chooser config)" — offer when the detection table signals a GitHub repo without `.github/ISSUE_TEMPLATE/`; copies `bug_report.yml`, `feature_request.yml`, `config.yml` from the installed `ticketing-skill/templates/` dir into `<repo>/.github/ISSUE_TEMPLATE/`. Create-if-absent ONLY — an existing file is skipped and reported, never overwritten. Source templates dir absent (per-skill install without `ticketing-skill`) → skip the offer with a note (mirrors the CodeGraph soft-skip). These are git-tracked repo files — they never touch `opencode.json`.
- "Pin built-in agent models?" — group multi-select: hidden maintenance (`title`, `summary`, `compaction` — they inherit the session model and run constantly, the cheapest cost trim) / subagents (`explore`, `general`) / all five / no. Never offer `build`/`plan` (session-selected models). Declined → skip silently.

**Model-pin intake** (only when the pin extra is accepted) — two more questions:

1. Per chosen group, one free-form `provider/model[#variant]` input (the question tool's own-answer field). Validate: must contain `/`; reject otherwise and re-ask. NEVER hardcode or suggest model IDs — the skill ships no model inventory (see Governance); the user supplies current values.
2. "Where should the pins live?" — **Project** `<repo>/opencode.json` (recommended: versioned with the repo, project-wins merge, other repos unaffected) / **Global** `~/.config/opencode/opencode.json` (all projects). Global is this skill's ONLY sanctioned global write — backup-then-merge per Step 3, never silent.

## Step 3 — Write (merge-write, delta-only)

Target: `<repo>/opencode.json` (Global-scope model pins: `~/.config/opencode/opencode.json`). Create if absent; **never clobber existing keys** — deep-merge at the top level manually (read file, add only the chosen `mcp.servers.<server>` entries). Keep the file comment-free JSON.

Typical delta (FULL entry — mandatory):

```json
{
  "mcp": {
    "servers": {
      "atlassian": {
        "type": "local",
        "command": ["npx", "-y", "mcp-remote", "https://mcp.atlassian.com/v1/mcp"],
        "disabled": false
      }
    }
  }
}
```

Agent model-pin delta (model-pin extra accepted):

```json
{
  "agents": {
    "title": { "model": "provider/model" }
  }
}
```

Rules:
- **Full entries only**: v2 replaces `mcp.servers.<name>` **atomically** across config layers — a bare `{"disabled": false}` stub erases the global transport and yields an inert server. Copy `type`/`command`/`environment` from the global `~/.config/opencode/opencode.json` definition and set `disabled: false` (Atlassian OAuth flows via `mcp-remote`; see caveats)
- **Model-only agent entries are safe** (the atomicity rule does NOT apply): v2 merges agent definitions across config layers — scalars replace, permission rules append — so `agents.explore.model` preserves the global entry's permissions. Valid IDs: `explore`, `general`, `title`, `summary`, `compaction`. Never write `build`/`plan` pins.
- **Global target** (model pins with Global scope): back up first — `cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.bak-$(date +%Y%m%d_%H%M%S)` — then run the same merge procedure against the global file. This backup is mandatory and MUST be reported in Step 5. Absent global file → skip the backup (nothing to preserve) and create the file fresh with the merged result.
- If the file exists, preserve every other key verbatim (byte-stable elsewhere; pretty-print 2-space)
- Never write `disabled: true` to disable something globally enabled — the project layer is for opting IN

Merge procedure (MANDATORY when `<repo>/opencode.json` already exists — never Write-overwrite):

1. Read + validate the existing file: `jq . opencode.json` (if invalid JSON, STOP and show the user; do not guess)
2. Merge the delta with jq `*` deep-merge, existing file as base:

   ```bash
   jq -s '.[0] * .[1]' opencode.json delta.json > opencode.json.new && mv opencode.json.new opencode.json
   ```

   No `jq`? Same deep-merge (existing base, delta wins) with Node:

   ```bash
   node -e "
   const fs = require('fs');
   const base = JSON.parse(fs.readFileSync('opencode.json', 'utf8'));
   const delta = JSON.parse(fs.readFileSync('delta.json', 'utf8'));
   const isObj = (v) => v && typeof v === 'object' && !Array.isArray(v);
   const merge = (b, d) => { for (const k of Object.keys(d)) b[k] = (isObj(b[k]) && isObj(d[k])) ? merge(b[k], d[k]) : d[k]; return b; };
   fs.writeFileSync('opencode.json.new', JSON.stringify(merge(base, delta), null, 2) + '\n');
   " && mv opencode.json.new opencode.json
   ```

   (`delta.json` = the chosen blob — `{"mcp":{...}}` for server enables, `{"agents":{...}}` for model pins; `*` merges recursively, existing non-conflicting keys survive, delta wins on conflicts — which is exactly the chosen-enable set; type-conflicting keys replace, matching jq)
3. Diff-check: `git diff opencode.json` (or plain diff vs a pre-made backup) must show ONLY the added `mcp.*` / `agents.*` keys (whichever the accepted extras produced). For a Global-scope pin write, diff against the `.bak-<timestamp>` file instead of git.
4. No jq available? Read the file, hand-merge the `mcp` / `agents` keys into the parsed object, and Write the full merged result — never emit a file missing previously-present keys

Also in Step 1 detection: ALWAYS `cat <repo>/opencode.json` when present and show its current keys to the user before Step 2, so the menu reflects what is already enabled.

## Step 4 — Init (CodeGraph only)

If accepted and `.codegraph/` absent: run `codegraph init -i` in the repo root. If `codegraph` is not installed or the repo is non-code/very large, soft-skip with a note. In headless/CI: skip silently unless explicitly requested.

CodeGraph setup reference (merged from the former `codegraph-setup-skill`):

```bash
npx @colbymchenry/codegraph init -i          # init + index (5-60s; creates .codegraph/)
echo ".codegraph/" >> .gitignore             # index is local-only — never commit it
npx @colbymchenry/codegraph status           # verify: backend native (preferred) or wasm
npx @colbymchenry/codegraph sync             # incremental sync (watcher auto-syncs, 2s debounce)
npx @colbymchenry/codegraph index --force    # full re-index after major structural changes
npx @colbymchenry/codegraph uninit --force   # remove CodeGraph from the project
```

- **Prereqs:** Node.js v18+, no API keys (100% local). 19+ languages (TS/JS/Python/Go/Rust/Java/C#/…).
- **Post-setup:** the file watcher auto-syncs; MCP tools (`codegraph_search`, `codegraph_callers`/`callees`, `codegraph_impact`, `codegraph_files`, …) are available to all agents whenever `.codegraph/` exists. `codegraph_explore`/`codegraph_context` are for explore agents (flood primary context otherwise).

Troubleshooting:

- **"Backend: wasm" (5–10x slower)** — install native build tools (`sudo apt install build-essential python3 make`; macOS: `xcode-select --install`; Windows: WSL, or VS Build Tools then `npm rebuild better-sqlite3`), then `npm rebuild better-sqlite3`. Also fixes **"database is locked"**.
- **Missing symbols after edits** — wait 2–3s for the watcher, or run `sync` manually.
- **Large repos slow to index** — add `exclude` globs (`node_modules/**`, `dist/**`, `build/**`, `vendor/**`, `*.min.js`, `*.generated.*`) to `.codegraph/config.json`.

## Rule blocks (project AGENTS.md)

Per-tool routing rules live at PROJECT level, not user level — this skill appends them on acceptance. Append = add the block verbatim under an `## OpenCode Rule Blocks` heading (create file/heading if absent); skip if the block's marker comment already exists anywhere in the file.

**CodeGraph** (marker `<!-- opencode:codegraph -->`) — append on init accept:

> The `codegraph_*` tools are the interface (`status` → `search`/`callers`/`callees`/`impact`/`node`/`files`). Never call `read_mcp_resource`/`list_mcp_resources` — runtime-denied (upstream tool-list bug). Main session: lightweight lookups only — never `codegraph_explore`/`codegraph_context` (flood context; spawn an explore agent).

**LSP** (marker `<!-- opencode:lsp -->`) — append on offer accept:

> On reviews with >10-file or shared-module changes where `opencode.json` has no `lsp` key and a built-in server matches: append a one-line LSP-enable recommendation (TS/JS/Next.js → `typescript`+`eslint`; Python → `pyright`). Recommend only — never auto-edit `opencode.json`.

**Jira templates** (marker `<!-- opencode:jira-templates -->`) — offer appended when the repo is Jira-centric (detection table's Jira signal) and accepted:

> Jira ticket descriptions follow the type templates — Bug: Problem description / Steps to reproduce / Expected vs Actual / Environment / Logs / References (mirrors the canonical GitHub bug body). Story: "As a… I want… so that…" + acceptance-criteria checklist. Task: Context / Acceptance Criteria / Scope. Run the intake from `ticketing-skill` first (classify → collect required fields → validate → preview); never leave a Jira description empty.

> GitHub repos get real form files via the issue-template scaffold above; Jira has no repo-file equivalent, so this rule block is the agent-side application path.

## Step 5 — Report

State exactly:

- **Enabled here**: list (e.g. `atlassian`) — takes effect on NEXT session start (opencode reads config at startup; no lazy-start mid-session)
- **Estimated per-session cost**: atlassian ~5–6.5k tok; codegraph ~1.2k + zai-web-search ~0.35k (both already default-on, GIT-336)
- **Rule blocks appended**: CodeGraph / LSP / Jira templates / none
- **Files written**: `.github/ISSUE_TEMPLATE/{bug_report.yml,feature_request.yml,config.yml}` (per file actually written; none if all already existed) + appended AGENTS.md blocks
- **Agent model pins written** (when the extra was accepted): `<id>.model = <value>` per pin + the scope (project `<repo>/opencode.json` / global), each effective on NEXT session start; global writes also report the `.bak-<timestamp>` backup path. Note: pinning the hidden agents (`title`, `summary`, `compaction`) does NOT make them selectable — they stay maintenance-only; pins are a cost/quality knob.
- **Revert**: delete the added `mcp.<server>` keys and `agents.<id>` entries (or the whole file if we created it); remove appended AGENTS.md blocks
- **Global untouched**: `~/.config/opencode/opencode.json` unchanged; other repos unaffected — EXCEPT a Global-scope model-pin write, which reports the exact keys added to the global file and its backup path

## Atlassian caveats (read before enabling)

- **First use opens a browser OAuth flow** (mcp-remote → mcp.atlassian.com). Fine on desktop; **fails headless/CI**.
- Headless fallback = skip MCP, use REST: token at id.atlassian.com/manage-profile/security/api-tokens; REST pattern + cloudId discovery per `ticketing-skill` §MCP Availability Guard.
- Delegation pattern: even when enabled, route bulk Jira calls through a subagent to keep tool output out of the primary context (schemas are paid regardless of who calls).

## Governance

| Aspect | Source of truth |
|--------|----------------|
| Server inventory + default enable states | `deploy/opencode.json` `mcp` block of the configurator repo |
| Config layering (project wins) | opencode docs — config merge semantics |
| Builtin agent IDs + agent-definition merge semantics (`model` pin safety) | opencode v2 agents docs — https://opencode.ai/v2/docs/agents |
| CodeGraph init | CodeGraph server's own MCP instructions + this skill's Step 4 / Rule blocks |

This skill deliberately contains no server versions, no model IDs, and no token costs beyond the estimates above — refresh from the configurator repo's README MCP table when drifting. Doc citations (Atlassian REST constants, the opencode v2 agents docs) are references, not inventory.
