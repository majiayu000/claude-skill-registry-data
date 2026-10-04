---
name: resolve-plugins
description: "Curate Claude Code skill / MCP / hook picks against live upstream sources and pin them in .claude/settings.json. Adding a process harness (a paired skill set) is an ordinary pick this door handles. Reads stack from docs/techstack.md, workflow signal from docs/overview.md + existing pins, then live-queries six source pools, dedupes, scores trust tier, presents diff vs pinned, writes settings.json. Standalone refresh path; also run as gated tier-2 curation by /super-bootstrap:setup. Solo dev workflow. Requires `docs/techstack.md` (seeded by `/super-bootstrap:harness-bootstrap`)."
tags: [plugins, curation, mcp, skills, settings, meta]
---

# Resolve Plugins — Curate & Pin

Curate Claude Code skill / MCP / hook picks against live upstream sources and write them to `.claude/settings.json`. Designed for two callers: standalone refresh (`/super-bootstrap:resolve-plugins`) and gated tier-2 curation (run by `/super-bootstrap:setup` once seed docs are substantive).

## When to Use

Caller: standalone refresh (`/super-bootstrap:resolve-plugins`) or gated tier-2 curation (run by `/super-bootstrap:setup` once seed docs are substantive). Same execution path.

---

## Phase 1: Read inputs (or fail loud)

Read inputs from files: `docs/techstack.md`, `docs/overview.md`, `.claude/settings.json` — caller passes no state.

### Required input

`docs/techstack.md` — drives stack-matched picks. Read § Runtime, § Framework, § Key Dependencies.

If missing → fail loud:

> No `docs/techstack.md` found. `/super-bootstrap:resolve-plugins` reads stack signal from harness-seeded docs. Run `/super-bootstrap:harness-bootstrap` first to seed the harness, then re-run `/super-bootstrap:resolve-plugins` if you want a standalone refresh.

Don't silently scan manifests — manifest detection is harness's job. Doing it here would duplicate logic.

### Workflow-tools signal (priority order)

1. **Existing `.claude/settings.json` pinned MCPs** — Notion MCP pinned → docs-heavy workflow. Linear MCP pinned → ticket-driven. Slack MCP pinned → team comm. Etc. Strong signal — user already explicitly enabled the tool.
2. **`<!-- harness-meta -->` block in `docs/overview.md`** — structured `external-tools:` record (seeded `[github]` by the runway, updated manually or via the entry skill). Parse the YAML `external-tools:` list. Strong signal — committed in the docs, not inferred. Robust to prose drift.
3. **Keyword scan of `docs/overview.md` prose** — phrases like "Notion docs", "Linear tickets", "Slack standup". Weak signal, brittle, but cheap. Fallback only when (1) and (2) absent (e.g. legacy harness-bootstrapped repos predating the meta block).
4. **Prompt user once** with the external-tools MCQ below if none of (1)–(3) yields signal:

   > External tools in your workflow? GitHub-only / Notion / Linear / Jira / Slack / Trello / ClickUp / other (multi-select).

### Optional input

`docs/overview.md` — § User, § Current State for additional workflow signal. Skip silently if missing (rare on a harness-bootstrapped repo).

---

## Phase 2: Live-query source pool

**Non-skippable, runs every invocation.** Stable project ≠ stable upstream. Marketplaces add picks, deprecate picks, change licenses, between any two runs. The only way to detect that drift is to actually query.

Issue WebFetch / Bash queries against each source. **GitHub-only pool — sites without backing repos can't surface trust signals (stars / recency / license).** Run queries in parallel where the harness allows.

- **Anthropic plugin marketplace** — `gh api repos/anthropics/claude-plugins-official/contents/plugins` — Anthropic-vetted picks (🛡 tier).
- **MCP official registry** — `gh api repos/modelcontextprotocol/registry/contents` (or query the registry API directly) — official MCP discovery service. Indexes both steering-group reference impls AND community-published servers. Primary source for MCP picks. Picks authored under `modelcontextprotocol/*` org auto-tier as 🛡 vetted.
- **everything-claude-code (affaan-m / ECC)** — `gh api repos/affaan-m/everything-claude-code/contents` — harness component bundle (skills + agents + rules + hooks + MCP configs). Strongest source for **language-specific rules** (TS / Python / Go / etc.).
- **awesome-claude-skills (ComposioHQ)** — `gh api repos/ComposioHQ/awesome-claude-skills/contents/README.md` (or WebFetch) — actively-curated category index with a "production ready" bar. Strongest source for **workflow / external-tools** picks (Composio SaaS workflow skills covering Notion / Slack / Jira / Linear / CRM).
- **VoltAgent/awesome-agent-skills** — `gh api repos/VoltAgent/awesome-agent-skills/contents` — skills from official dev teams (Anthropic, Vercel, Stripe, Cloudflare, Sentry, Hugging Face, Figma) + community. Cross-reference for cross-team picks the Claude-only catalogs miss.
- **Fast-path — `claude-code-setup` recommender.** If the `claude-code-setup` plugin is installed locally, invoke `/claude-code-setup:claude-automation-recommender` and treat its report as **candidate input** — its rows enter Phase 3 dedupe + trust + earn-right gate like any other source; this skill is the sole author of the final pin set. Adds one signal the GitHub pools lack: hook candidates from a live repo-config scan (Prettier / ESLint / `.env` present). Subagent rows fall outside settings.json scope — route them to `/super-bootstrap:log` as a GAP.

**Partial failure handling.** Single source unreachable (404 / rate limit / network) → note inline, continue with the others. Never skip the whole step.

**Total failure handling.** All sources unreachable → fail loud, don't write a stale-pin diff. Report and let user retry.

### Language-LSP pre-filter

`claude-plugins-official` ships per-language LSP plugins (`python-lsp`, `rust-lsp`, `go-lsp`, `ruby-lsp`, `swift-lsp`, `php-lsp`, `kotlin-lsp`, `lua-lsp`, `java-lsp`, `csharp-lsp`, `typescript-lsp`, etc.). For a single-language project, all but one are guaranteed stack-mismatches — running Phase 2.5 README parse on each is wasted cycles (10+ fetches per run on Node/TS repos).

Pre-filter rule: after Phase 2 returns the source pool, partition `*-lsp` plugins by name → language mapping. Drop any whose language ≠ techstack.md § Runtime / § Framework / § Key Dependencies match. Surface dropped count inline so user sees they exist:

```
Pre-filtered: 10 language-LSP plugins (stack-mismatch w/ {detected-language}) — type `expand prefilter` to list.
```

Default collapsed. Multi-language repos (monorepos w/ Python + TS, etc.) keep both matching LSPs.

Skipped plugins do **not** enter Phase 2.5 README parse, Phase 3 dedupe/trust/gate, or Phase 4 rejection collapse — they're filtered above all of those. Distinct from Phase 3 earn-right rejections (collapsed under `Rejected (earn-right)`); the pre-filter line surfaces separately so the source-rejection accounting stays accurate.

Apply the pre-filter only to the `*-lsp` pattern from `claude-plugins-official`; extending to another pattern requires an equally precise name → stack-attribute mapping first — false-positive skip is silent harm.

---

## Phase 2.5: README parse → cached digest

For each candidate Phase 2 emitted, fetch the upstream README once (WebFetch / `gh api`, same mechanic as Phase 2) — the fetch stays here, on the gateway. Reducing the fetched bodies to a structured digest is mechanical extraction; dispatch it. The thinking runs in the `plugin-digest` subagent (`agents/plugin-digest.md`, `model: haiku`); this phase is the dispatch shell. Phase 3 (gate) and Phase 5 (install plan) consume the same digest — single parse, two callers.

Digest fields (agent's job — see `agents/plugin-digest.md` for the full field spec):

- `hard_paths_shipped` — hooks declared (which event + file glob), slash commands shipped, frontmatter `agents:` / `related-skills:` delegations, MCP server config presence.
- `manual_install_steps` — ordered imperative steps lifted from `## Installation` / `## Setup` / `## Quick Start` headings (e.g. `brew install graphify`, `pnpm add -D <pkg>`, `chmod +x .claude/hooks/<name>.sh`).
- `user_invoke_trigger` — one-sentence "user types /name when ___" hypothesis for any slash command shipped (empty if none).
- `multi_component` — boolean. Flags Phase 5 to plan an atomic multi-step install (e.g. binary + MCP + hook + skill in one bundle).

**Dispatch:** `Agent` tool, `subagent_type: "plugin-digest"`, prompt = every fetched README/manifest body from this run, each tagged with its candidate name (batch over loop — one dispatch for the whole batch, never one per candidate). Relay the returned per-candidate digests into the Phase 2.5 cache verbatim; the gateway does not re-derive fields the agent already extracted.

**Why Haiku is safe here:** the agent only extracts — it never scores trust or decides admission. Phase 3's trust-tier scoring and earn-right gate already judge the digest downstream, so a lossy extraction gets caught before it reaches `settings.json`. Never build a verification stage just for this; ride the judge stage that already exists.

If README absent or fetch fails for one candidate: warn inline before dispatch, mark that candidate `unresolved` in the batch (the agent surfaces `unresolved` too if a supplied body is empty). Don't halt the whole batch on a single missing README.

Cache lifetime: per `/super-bootstrap:resolve-plugins` invocation. Discarded at end. Re-runs re-fetch (README content drifts between runs) and re-dispatch.

---

## Phase 3: Dedupe + trust signals + filter

### Filter to matched picks only

Drop generic / spray suggestions. Match against stack signals (Phase 1 § Required input) AND product/workflow signals (Phase 1 § Workflow-tools signal). A Notion MCP isn't "off-stack" if Phase 1 surfaced docs-heavy workflow.

### Dedupe by canonical name across sources

Same skill / MCP often appears in multiple sources (e.g. `react-expert` in Anthropic + ECC + VoltAgent with different versions / licenses / recency). Sources are peers, not ranked — never silently default to one. Process:

- Group hits by canonical plugin name (case-insensitive, ignore source suffix)
- Pick the **primary row** by highest composite signal: stars × recency × license-clean. Tie-break by Anthropic-vetted if present.
- Collapse other variants into a single `also in: <source-A> · <source-B>` line under the primary row, with provenance: stars / last-commit / license per alternate.
- User can expand alternates at present-batch step if the primary's trust signal looks weaker than an alternate's.

### Trust signal lookup per pick

For any plugin NOT from `claude-plugins-official` or `modelcontextprotocol/*`, fetch (via WebFetch or `gh api`):

- Repo URL + GitHub stars
- Last-commit recency (e.g. "3d ago", "14mo ago")
- License (or "no license" — flag as ⚠)
- Permissions exercised (read-only? shell? network? auto-exec hook?)

Hooks are elevated risk: auto-exec on every tool call (PreToolUse / PostToolUse / UserPromptSubmit). Always tag hooks: `⚠ HOOK = auto-executes. Audit source before accept.`

### Trust tiers

- `🛡 vetted` — authored under `anthropics/*` or `modelcontextprotocol/*` org (Anthropic-audited or MCP steering-group authored, license-clean, slower to land sharp picks).
- `★ popular` — outside the vetted orgs above, ≥1k stars + commit ≤90d ago + license clean
- `🆕 fresh` — recent activity (≤30d) but lower stars / smaller pool
- `⚠ unaudited` — no license, archived, last-commit >12mo, or stars <100

### Earn-right gate

For each candidate that survived dedupe + trust scoring, name one hard invocation path that exists in **this project** (use Phase 2.5 digest's `hard_paths_shipped` as primary signal):

- [ ] hook (which event? which file glob?)
- [ ] slash command (concrete user-trigger context — "user types /name when ___")
- [ ] pipeline delegation (which existing skill calls it by name?)
- [ ] frontmatter `agents:` / `related-skills:` bundle (which orchestrator pulls it?)
- [ ] committed-stack — plugin name or primary keyword matches an entry committed in `docs/techstack.md` § Runtime / § Framework / § Key Dependencies. Covers passive runtime integrations (LSPs, type checkers, debuggers, formatters) that ship no hook/slash/bundle but earn their slot because Claude Code uses them when reading matched files.
- [ ] none — only CLAUDE.md prescription / description match

#### Decision rules

- **≥1 of hook / slash / delegation / bundle** → admit. Tag the path: `[hook]`, `[slash]`, `[delegation]`, `[bundle]`.
- **Only committed-stack** → admit when trust tier is `🛡 vetted` (Anthropic-vetted or MCP steering-group). Tag `[committed-stack: <matched-term>]`. For community tiers (`★ / 🆕 / ⚠`), surface for user confirm before admit — keyword-spoof risk on unvetted sources. Tag becomes `[committed-stack: <matched-term> · user-confirmed]` on accept.
- **Only the last box** → reject by default. Description-match autopilot orphan.
- **User override** → admit on single-line justification; tag becomes `[override: <reason>]`. Surfaces in Phase 6 report only.

#### Mass-rejection collapsing

If many candidates from the same source reject for the same reason, collapse to one batch line — e.g. `Rejected 42 candidates from VoltAgent/awesome-agent-skills (description-match-only)`. Default collapsed; user types `expand rejected` to expand.

---

## Phase 4: Diff vs pinned, present batch

### Pre-resolve pin (core)

`/super-bootstrap:harness-bootstrap` Phase 2a pins this before curation runs.

**Core pin** — locked when harness-active:

- `super-bootstrap@super-bootstrap` — requires `super-bootstrap` entry in `extraKnownMarketplaces` (source: `github` / `RockyHong/super-bootstrap`).

A process harness a repo adds on its own is an ordinary adaptive pick — proposable, droppable, trust-signals re-fetched like any other.

**Harness-active marker:** `docs/work/` directory exists in the repo. Detect with one Glob.

Core pin:

- **Harness-active + pinned + present** → keep silently, do not surface in batch.
- **Harness-active + pin absent** (user manually removed; or fresh harness call hadn't reached Phase 2a yet) → **propose re-pin** as a locked core dep, short message: "core dep missing, re-pinning so CLAUDE.md triggers resolve." User can decline only with explicit override; flag what breaks (every `/super-bootstrap:*` door in CLAUDE.md dangles, and the committed `commit-channel.sh` routes workers to a command that doesn't resolve).
- **Not harness-active** (no `docs/work/` folder — standalone curation on a non-harness repo) → no core lock applies. The core dep, if present, is treated as a regular adaptive pick the user may drop.
- Locked pick: never propose drop, never re-fetch trust signals (super-bootstrap locked as the harness's own door set — the runway it installed names it).

### Adaptive picks

If `.claude/settings.json` already has pinned picks, diff the new curation against the pinned set. **Re-fetch trust signals on every pinned pick** (not just new ones) — license can change, last-commit can age, repo can be archived.

- **Pinned + still recommended + trust block unchanged** → keep silently, mark `✓ pinned`
- **Pinned + still recommended + trust block moved** (license / last-commit / archive status changed) → re-show that pick's trust block, ask user to re-confirm
- **New pick recommended** (upstream added it; or stack signal changed) → propose as **add**
- **Pinned but no longer recommended** (deprecated upstream; license changed; stack changed) → propose as **drop** with reason
- **Pinned but source missing** — `enabledPlugins` entry exists with no resolvable source (not in `extraKnownMarketplaces`, not Anthropic-vetted). **Live-query source pool first** to find the plugin's real marketplace; if found, propose **resolve** (add marketplace to `extraKnownMarketplaces`) with trust block; if not found in any source, propose **drop** (orphan, can't reproduce on a fresh machine).

### Batch presentation format

Render using §batch-presentation in `assets/formats.md`.

Path tag column (`[hook]` / `[slash]` / `[delegation]` / `[bundle]` / `[committed-stack: <term>]` / `[override: <reason>]`) shows the hard invocation path Phase 3 admitted the pick on — surfaces "why this one earned its slot" at a glance.

An LSP pick's row carries two rider notes: (a) the language-server **binary** is a separate install — state its install command (npm / rustup / go / dotnet per language) beside the pick; a pinned plugin without the binary reads as installed while the `LSP` tool returns no-server-configured. (b) coverage is typed symbols only — string literals, comments, config and markdown stay grep-and-verify.

`Rejected (earn-right): {R} candidates collapsed` line renders only when Phase 3 produced rejections. Default collapsed; user types `expand rejected` to expand into per-source breakdown.

`also in:` line collapses dedupe alternates from Phase 3. User can ask to expand if primary's signal looks weaker than an alternate.

**Catalog stays chat — never popup.** Per-row trust blocks + per-pick toggles + alternate expand don't fit popup option/description shape. Final approve gesture stays chat too — splitting from catalog adds friction.

---

## Phase 5: Apply approved → settings.json + atomic install + verify + commit

Source of truth: project-scope intent, committed, travels with repo to fresh clones and machines. Device install (`claude plugin install`) is optional convenience layered on top.

Each accepted candidate executes as an **atomic unit** — settings write + per-component install + per-component verify. Atomic boundary is per-candidate: one candidate failing verify halts only its own steps; sibling candidates continue independently.

### Phase 5.1: Install plan

For each accepted candidate, expand the Phase 2.5 digest into ordered install steps and render the plan before execution. Render using §install-plan in `assets/formats.md`.

Steps execute sequentially within a candidate. Multiple candidates may install in parallel.

### Phase 5.2: Settings.json write

- Add accepted picks to `enabledPlugins`. Drop rejected picks. **When harness-active (`docs/work/` exists), never drop the core pin** (`super-bootstrap@super-bootstrap`) — see Phase 4 § Pre-resolve pin.
- For any plugin NOT from `claude-plugins-official`, ensure its source is in `extraKnownMarketplaces` so fresh clones / machines can resolve.
- Example shape:
  ```json
  {
    "enabledPlugins": {
      "graphify@claude-plugins-official": true,
      "caveman@caveman": true
    },
    "extraKnownMarketplaces": {
      "caveman": { "source": { "source": "github", "repo": "JuliusBrussee/caveman" } }
    }
  }
  ```
- One-line transparency: "Pinning plugins per-project in `.claude/settings.json` so fresh clones and machines reproduce this toolset."
- Cloud line, printed to the user once after the transparency line: "Cloud sessions ignore this pin — add `claude plugin install <plugin>@<marketplace>` per pick to the cloud environment's Setup script, preceded by `claude plugin marketplace add <owner/repo>` for each pick outside `claude-plugins-official`: https://github.com/RockyHong/super-bootstrap#cloud-sessions"

Pin all accepted picks in `.claude/settings.json` — fresh clones and machines resolve from there. Device install alone doesn't travel.

### Phase 5.3: Verify per component

For each install step: log to user → execute → run mechanical verify command. Never claim "done ✓" without an observable check. Render using §verify-table in `assets/formats.md`. `bash -n` catches syntax pre-runtime. `jq -e` is structural — exits non-zero on missing keys, not substring match. `command -v` is POSIX-portable.

### Phase 5.4: Halt-or-rollback on verify fail

If any step fails verify:

1. Halt remaining steps for **this candidate only**. Sibling candidates continue.
2. Surface failure: which step (component type + name), the verify command + observed output, candidate's progress so far.
3. Offer three resolutions:
   - **Rollback** — best-effort undo of already-applied steps. Some manual installs (e.g. `brew install`) aren't rollback-able — surface that.
   - **Pause** — leave partial state, surface summary, user fixes manually then re-runs `/super-bootstrap:resolve-plugins`.
   - **Drop** — accept candidate didn't install, drop from accepted set, revert its settings.json edit.

Never silently skip. Never claim "done" with half-installed state.

### Phase 5.5: Commit only fully-installed candidates

`/super-bootstrap:commit` handoff. Restrict commit to candidates where every Phase 5.3 verify exited 0. Half-installed candidates excluded; user resolves before re-running.

If delta non-empty → invoke `/super-bootstrap:commit` to stage `.claude/settings.json` (and `.mcp.json` / `.claude/hooks/` / `.claude/skills/` if written by atomic install) with message `chore: refresh plugin picks` (or `chore: pin plugin picks` on first run with empty `enabledPlugins`).

If delta empty (every row `✓ pinned` and trust blocks unchanged) → report `✓ all pinned picks current` and skip commit.

---

## Phase 6: Report

After Phase 5 completes, render using §report-block in `assets/formats.md`.

