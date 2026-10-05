---
type: Skill
name: mcp-ai-wpoos-updates
description: "Operational guide for the three recurring NV oOS maintenance tracks: (1) Docs & Release Catch-Up — plan-first per-version docs, changelog, and version-bump passes; (2) Model Catalog & Config Updates — the monthly model-config refresh across the catalog and its derived files; (3) PR Deferred-Item Sweep — review merged/closed PRs for deferred work and file GitHub issues for what is still incomplete. Use when asked to 'catch up docs', 'update the model configs', or 'review the week's PRs for deferred work'."
license: Proprietary. See LICENSE.txt
metadata:
  plugin: mcp-ai-wpoos
  plugin-version: "1.1.91"
  plugin-version-tested: "1.1.91"
  last-updated: "2026-10-01"
---

# NV oOS Updates — Docs Catch-Up, Model Catalog & PR Deferred-Item Sweeps

Playbook for the three recurring update tracks in this repo, distilled from the

executed catch-up plans (`docs/project/plans/v1.1.58-docs-catch-up.md` through
`v1.1.83-post-docs-catch-up.md`), the model-catalog process docs (July 2026 and
September 2026 runs), and the executed 2026-09-17 PR deferred-item sweep
(issues #6646–#6655). The workflows implement industry standards — Keep a
Changelog, SemVer commit separation, and deprecation-driven LLM model lifecycle
management — adapted to this repo's conventions.

## When to use this skill

**Track A — Docs & Release Catch-Up:**
- "Catch up docs/release notes for vX.Y.Z" / "do the same exercise for this version"
- A window of PRs merged on `alpha-working` has no release-note coverage
- Version bump + changelog + agent-context sweep for a new release

**Track B — Model Catalog & Config Updates:**
- "Update model configs" / "refresh the model catalog" / "new model lineup"
- Provider deprecations, price changes, new default models
- The monthly model-update exercise

**Track C — PR Deferred-Item Sweep:**
- "Review all the PRs for the past week to find deferred issues"
- "Add deferred/incomplete items to the issues list"
- A PR window has follow-up notes that were never re-tracked

Tracks A and B can run in the same window: Track B's catalog changes always get
a changelog mention, folded into Track A's release surfaces. Track C runs
weekly (or on demand), independent of any release.

---

## Track A — Docs & Release Catch-Up

### A0. Orientation (before touching anything)

1. **Check `git log` first** — another agent may have already executed parts of
   the window. Compare against the latest executed plan's execution log.
2. **Read `docs/project/plans/docs-catch-up-open-items.md` FIRST** — it holds
   every standing open item (OI-1 `@since` reconciliation, OI-2 Docker count
   re-derivation, OI-3 test-suite cross-ref, OI-4 wave residuals). Parked items
   stay parked; new finds get *recorded* there, never fixed in-pass.
1. **Read the template plans** — the latest executed plan (`v1.1.91-docs-catch-up.md`,
   with `v1.1.90-docs-catch-up.md` as the previous pass) plus the
   `v1.1.83-post-docs-catch-up.md` post-window precedent (executed when PRs
   merged after the catch-up but before the next version bump) and
   `v1.1.58`/`v1.1.59` for the original structure.
4. **Identify the PR window** — everything merged on `alpha-working` after the
   previous catch-up merge. Classify every PR: production-touching (file + change
   table), test-only, docs-only, build-only, closed-unmerged docs PRs.
5. **Create the plan** `docs/project/plans/[VERSION]-docs-catch-up.md` if none
   exists — or `[VERSION]-post-docs-catch-up.md` when a catch-up already merged
   for the current version and a new PR window landed on the same line (the
   v1.1.83 post pass is the precedent: extend the current-release changelog
   section in place, re-derive the count delta, and sweep the previous pass's
   "unchanged" claims — they can be falsified by post-window merges). Use the
   v1.1.83 structure:
   1. Context — PR table + scope rules
   2. Work items (P0–P3 + Verify-only)
   3. Execution log (stamped when run)
   4. Commit breakdown
   5. Validation
   6. Open items — point at the standing tracker, add only new items
6. **Read every PR description in the window.** `@since` tags that don't match
   the shipping version go to OI-1 as a new group (recorded, **not** fixed).
   Residual test-suite findings from PR notes go to OI-4 (hand to the test-suite
   workstream, not the docs pass).

### A1. Work items by priority

| Priority | Scope | Files |
|---|---|---|
| **P0** Release-note surfaces (user-facing) | Changelog, wp.org readme, repo readme, quick reference, doc index, reviewer notes | `CHANGELOG.md`, `readme.txt`, `README.md`, `docs/QUICK_REFERENCE.md`, `docs/DOCUMENTATION_INDEX.md`, `docs/project/FOR_REVIEWERS.md` |
| **P1** Agent context files | Subsystem context stamps + notes, agent configs, skill copies | `.context/tool-registry.md`, `.context/security-checklist.md`, `.context/testing.md`, `.context/rest-api.md`, `CLAUDE.md`, `MAINTAINER_MAP.md`, `.bmad/README.md`, all three `mcp-ai-wpoos-plugin` SKILL.md copies, `.agents/skills/mcp-ai-wpoos-test-suite/SKILL.md` |
| **P2** Operational & feature docs | Inventory stamps, open-items tracker, this plan | `docs/project/ADDON_INVENTORY.md`, `docs/reference/tools/tool-reference.md`, `docs/project/plans/docs-catch-up-open-items.md`, `docs/developer/testing-docs/TEST-SUITE-REMAINING-FIXES-PLAN.md`, the plan doc itself |
| **P3** Version bump (mechanical) | Version headers + constants only | `mcp-ai-wpoos.php`, `includes/bootstrap/constants.php`, `addons/pro/mcp-ai-wpoos-pro.php`, `package.json` — **never** `package-lock.json` |
| Verify-only | Confirm no change; list in the plan | Skill counts, tool counts, addon/toolkit counts, proposals index, Docs Hub changelog |

### A2. Scope rules (non-negotiable)

- **Historical per-version entries stay untouched.** Old CHANGELOG/README blocks
  (`[1.1.XX]` and earlier) are history and are never rewritten.
- **Tool counts use `~`** with the live-registry caveat; counts change only when
  tools are added/removed (delta-derived — OI-2's live re-derivation is parked).
- **Sub-projects keep their own tracks:** Media Worker v3.x, Docs Hub 0.4.x,
  standalone plugins (nvoos-content-graph 1.0.x, -ai 1.0.x, -ai-platform 2.0.x).
- **Parked items stay parked:** OI-1 `@since` reconciliation and OI-2 Docker
  count derivation are user-deferred — record, never re-attempt.
- **Exclude unrelated working-tree noise** (vendor/, other agents' untracked
  work, backup dirs) from every commit.
- **README keeps the last 12 releases in full.** The `## 📜 Release History`
  section holds exactly the 12 most recent releases. Each new release adds a
  new `### vX.Y.Z — Date` + `#### Title` entry at the top of that section; the
  oldest entry is demoted to a one-line row in the `### 📋 Previous Releases`
  table (newest first). Full per-release detail lives in `CHANGELOG.md` only —
  the README never grows past 12 detailed entries, and the Overview keeps a
  single current-release "What's New at a Glance" block. (Adopted 2026-09-22
  to stop the README's duplicated changelog blocks from growing unboundedly.)
- **Anchor hygiene:** headings must not carry VS16 (U+FE0F) emoji — GitHub's
  slugger strips the base emoji but keeps the invisible VS16, producing broken
  `#...` anchors (e.g. `### ⚠️ Warranty` resolves to `#️-warranty--safe-use`).
  Use the no-VS16 form (`⚠`, `⚙`, `🗨`, `🛡`) and keep TOC links as the plain
  `#-slug` form; never add manual `<a id="...">` anchors.
- **Provider-count figure tracks model-catalog chat providers only.**
  Media-generation providers (Sora, Veo, Runway, Higgsfield, …) are **not**
  counted in the "N providers" versioning line — that figure follows the
  model catalog (`WP_MCP_AI_Model_Config::get_all_provider_slugs()`), and media
  providers live outside the catalog. When a media-provider PR lands, verify
  the catalog is untouched and keep the provider count unchanged (the v1.1.86
  Higgsfield pass is the precedent).
- **Dual-layer tool PRs count the plugin registry only.** When a PR registers
  the same tools in `includes/class-wp-mcp-ai-tool-registry.php` **and** adds
  framework-agnostic wrappers under `lib/core/src/Tool/` via
  `includes/bootstrap/oos-bridge.php`, the base/Pro count delta is the
  **registry** registration count — `lib/core` keeps its own registry and its
  tools are never counted in the base/Pro totals (the v1.1.86 Higgsfield
  pass: +4 base, not +8).
- **Release-sync PRs are build-classified.** "Merge alpha-working into main
  (squashed)" PRs are tree-identical to `alpha-working` — classify them
  build/release-only (no production file table); their only real effect is
  dropping already-stale build ZIPs (the v1.1.86 pass's #6770 is the
  precedent).
- **The stale-ZIP set follows the full build set, not just the wp.org root.**
  When a release ships, remove the whole previous-version artifact set — root
  `build/` ZIPs + `.sha256` pairs **plus** `build/optional-components/` and
  `build/toolkit-addons/` (the v1.1.85 pass's "30 files" shape — 9 + 2 + 19 —
  repeated by the v1.1.87 pass for the 1.1.85 set).
- **An introducing PR may pre-stage the readme.txt release entry.** A feature
  PR can add a `= X.Y.Z - Unreleased =` changelog paragraph before the
  catch-up runs (the v1.1.87 window's #6780 did) — the catch-up converts it
  into the dated release entry and extends it with the rest of the window;
  never keep two entries for the same version.
- **Sub-project window PRs are flagged-not-edited even when they carry their
  own changelog surfaces.** PRs that update `plugins/nvoos-content-graph`'s
  own CHANGELOG.md/readme.txt/.pot (the v1.1.87 window's #6782/#6783) keep
  their own version track (1.0.8) — the catch-up notes them in the plan and
  the changelog's sub-project paragraph but edits nothing under `plugins/`.
- **Wrong-version `@since` groups with unusual tags record like any other OI-1
  group.** The v1.1.87 window shipped `@since 2.12.0` ×139 (outbound-booking
  toolkit + Upwork files) — record the group with its counts and locations;
  parked reconciliation (OI-1) still applies, no in-pass fixes.
- **A PR merged between the previous plan's window map and its catch-up merge
  belongs to the new window when the previous changelog never covered it.**
  The tree diff alone misses such PRs (they sit inside the previous catch-up's
  tree). Cross-check the previous changelog for the PR number during
  orientation — the v1.1.88 window's #6787 (gateway express bump) merged
  24 min before the #6788 catch-up and was absent from the 1.1.87 changelog.
- **A PR may explicitly defer its own changelog entry to the catch-up.** The
  v1.1.88 window's #6792 (decision-model Phase A) carried a "CHANGELOG entry
  at merge time (v1.1.88+ window)" note — grep PR bodies for
  changelog/release-note deferrals during orientation; the catch-up owns the
  entry.
- **Addon sub-projects with their own version tracks may update `ADDON_INVENTORY.md`
  in-window** (the v1.1.88 window's #6797 set the saas-controller row to 0.3.0)
  — the pass refreshes only the header stamp, and the addon's versioning goes
  in the changelog's sub-project paragraph, not a new inventory row.
- **In-window skill updates are not proof the skills are current.** The v1.1.88
  window updated `design-crm` (#6790) and `design-elementor-mcp-connection`
  (#6799) in place, yet #6793 then reverted the URL canonical form #6790 had
  just documented, the bundled `design-crm` copy was two windows behind the
  Zed copy, and the elementor skill's security rules still claimed inline
  secrets were plaintext after #6798 encrypted them. After mapping the window,
  diff each updated skill against the code it documents and `diff -q` the
  Zed/bundled pairs — the catch-up owns the reconciliation.
- **A PR may pre-stage a `## [Unreleased]` CHANGELOG section, not just a
  readme.txt entry.** The v1.1.89 window's #6809 added an `[Unreleased]`
  block (the Google Classroom content) at the top of `CHANGELOG.md` before the
  catch-up ran — the catch-up converts it into the dated release section and
  extends it with the rest of the window; never keep two entries for the same
  version (the same rule as the readme.txt pre-staging).
- **Verify addon rows in `ADDON_INVENTORY.md` against the addon's own version
  constant.** The v1.1.89 window's #6810 updated the Design System row
  in-window but wrote **0.2.0** while the addon's header + `NVOOS_DESIGN_SYSTEM_VERSION`
  + PR body say **0.3.0** (the proposals README even said "v0.2.0 → v0.3.0").
  The catch-up corrects a factually wrong in-window row version in-pass (the
  "refreshes only the header stamp" rule assumes the row was right).
- **Addon-level wrong-version `@since` waves record like any other OI-1 group.**
  #6810 shipped 33 × `@since 0.2.0` across the renamed/new
  `addons/nvoos-design-system/` files while the addon shipped **0.3.0** (2
  files correctly tagged 0.3.0) — the addon-version convention (SaaS Controller
  precedent) requires tags to match the shipped addon version. Record the
  group with its counts; parked reconciliation applies.
- **Tools registered by standalone addons via `wp_mcp_ai_register_tools` are
  described in the changelog but never counted in base/Pro totals.** The
  v1.1.89 window's 8 `nds_*` email tools (Design System addon) join the same
  registry the algorave/embedded/graphify/page-agent addon tools use — the
  base/Pro count lines track plugin + `addons/pro` registrations only (the
  algorave "9 tools" entry is the precedent: described, not counted).
- **Folder/file `@since` conventions override the wrong-version rule.** The new
  `includes/google/` Classroom files carry `@since 1.0.0` ×71 like their
  Calendar siblings (which already had 31), and the Pro remote-site files'
  `@since 1.0.0` additions follow each file's dominant pre-existing tag —
  local convention, not a new OI-1 group.
- **Track B: the migration-trigger line now covers per-provider settings keys.**
  #6805 extended `WP_MCP_AI_Model_Catalog_Migration` to rewrite
  `deepseek_model`/`default_gemini_model`/`anthropic_model`/`kimi_model`
  alongside `default_model` — the rewrite still only runs on a catalog
  version bump, so a migration-behavior change without a bump is dormant until
  the next one.
- **The plugin skill keeps a companion `RELEASE-NOTES.md` and must stay under
  the Zed 100KB skill-size limit.** #6822 moved the per-version release-note
  tail out of `mcp-ai-wpoos-plugin/SKILL.md` (103KB → 46KB) into a companion
  `RELEASE-NOTES.md` — **future version notes append to RELEASE-NOTES.md, not
  SKILL.md**. When a structural change like this lands on the Zed copy, sync
  the base bundled copy byte-identical (SKILL.md + companion) — stamp-only is
  not enough; the CG AI platform bundled copy is a deliberately trimmed
  variant and keeps stamp-only treatment.
- **In-window tool-reference edits may update the header note without the
  count line.** #6824 added the RF-DETR entries + the "+2 Pro in v1.1.90"
  note but left the main count line at ~1,299/~1,646 — the catch-up
  reconciles the count line (and the Last Updated stamp) in-pass.
- **An introducing PR may complete the A5 skill-count bookkeeping itself.**
  #6820 (the dependabot-loop skill) bumped 60 → 61 in `AGENTS.md` §1,
  `.github/copilot-instructions.md`, and the `README.md` repo map in-window —
  the catch-up verifies (grep for the old count) rather than assuming the
  fold-in is owed.

### A3. Commit structure (mirror v1.1.58–v1.1.83)

Separate commits, in this order:

1. `chore: bump version to [VERSION]` — version headers, constants, Pro addon,
   `package.json`.
2. `docs: add [VERSION] changelog and release notes` — `CHANGELOG.md`,
   `README.md`, `readme.txt`, `docs/QUICK_REFERENCE.md`,
   `docs/DOCUMENTATION_INDEX.md`, `docs/project/FOR_REVIEWERS.md`.
3. `docs: update agent context for [VERSION] changes` — `.context/*`, `CLAUDE.md`,
   `MAINTAINER_MAP.md`, affected `.agents/skills/*`.
4. `docs: reconcile [VERSION] reference surfaces` — `ADDON_INVENTORY.md`,
   proposals index, addon READMEs, tool-reference header, the plan doc itself.
5. **Optional:** `docs: reconcile remaining [VERSION] tool counts` — only when
   counts changed; grep for stale counts (e.g. `~265`, `~1,508`) and skip
   historical per-version blocks, plans, and proposals.

### A4. Housekeeping (when requested)

- Remove stale build ZIPs: delete all `build/**/*[OLD_VERSION]*` (ZIPs **and**
  `.sha256` files). Commit: `chore: remove stale [OLD_VERSION] build ZIPs [skip ci]`.

### A5. New coding-time skill bookkeeping (when a skill is added)

Per `AGENTS.md` §6, when adding a skill under `.agents/skills/[slug]/`:

- Update the skill count (e.g. 53 → 54) in `AGENTS.md` §1 (inventory row + the
  coding-time-vs-runtime paragraph), `.github/copilot-instructions.md`
  (multi-agent-awareness bullet + repo-tree comment), and the `README.md` repo
  map row. (The 2026-09-07 `mcp-ai-wpoos-wporg-submission` skill is the
  example — wp.org submission/PCP/screenshot playbook; see that skill for
  the submission track itself.)
- **The introducing PR may skip the count bookkeeping — fold it into the
  release.** Feature PRs sometimes add a new skill without the `AGENTS.md` §1 /
  `.github/copilot-instructions.md` / `README.md` repo-map count updates (the
  v1.1.86 pass: #6761 added `design-elementor-mcp-connection` without them).
  During orientation, diff the introducing PR's file list against the count
  surfaces; the catch-up pass owns the fold-in and states it in the
  changelog's Versioning line (never post-hoc edit an executed release entry).
- **Leave historical per-version count lines untouched** — old release entries
  keep the counts they shipped with.

### A6. Validation

- `php -l` on every bumped PHP file; JSON-parse `package.json`.
- `git grep` sweeps for the old version string and stale counts — remaining hits
  must be intentional history only (`@since` docblocks, per-version blocks,
  plans, archive).
- Verify every claim in the plan (file paths, counts, versions) against the
  actual PRs before marking executed.
- Re-run the README anchor check: every `](#...)` target must resolve under
  github-slugger rules (emoji stripped, spaces → hyphens, `&` → `--`), and the
  Release History section must hold exactly the last 12 releases.

### A7. Branch + PR (required)

- **Do NOT commit directly to `alpha-working`.**
- `git checkout -b chore/[VERSION]-docs-catch-up`, commit there, reset local
  `alpha-working` to `origin/alpha-working`, push the branch.
- Open a PR against `alpha-working` with Summary / What's in / Validation /
  Notes structure, listing deferred open items explicitly.

---

## Track B — Model Catalog & Config Updates

### B0. Orientation

- **Read** `docs/reference/models/model-update-process-2026-07.md` (13-phase
  checklist, 24-file map) and `docs/reference/models/keeping-the-model-catalog-up-to-date.md`
  (catalog architecture, loader, migration).
- **Check `git log` on the catalog + derived files first** — another agent or a
  drift-fix commit may have already landed part of the window
  (`git log --oneline -10 -- includes/data/model-catalog.json`).
- **Verify the previous run's process-doc claims against the actual files.**
  The previous run's "This Month's Changes" section is a plan of record, **not**
  proof the values are in the files — a later drift-fix commit can revert a
  documented fix (the July 2026 run: the doc said Claude Opus 4.5/4.6/4.7 input
  was fixed $15 → $5, but the cost calculator still shipped $15; the catalog
  also shipped `deepseek-v4-flash` input 10× too low at $0.014/1M). Diff each
  claim against the JSON + cost tables before trusting it.
- **Scope boundary (as established by the July 2026 run):** edit only
  `includes/` + `addons/pro/` + `tests/` + `assets/examples/` + the two model
  docs. `lib/core/` (`Infrastructure/Token/TokenBudgetManager.php`,
  `Infrastructure/Cost/CostCalculator.php`, `Infrastructure/Provider/KimiClient.php`,
  `Tool/CountTokensTool.php`, `Tool/GenerateGeminiImageTool.php`,
  `Tool/EditGeminiImageTool.php`), `lib/wordpress-adapter/src/Tool/RunGeminiManagedAgentTool.php`,
  and the sub-project `plugins/nvoos-content-graph-ai/` (its own mirrored
  `src/Model/model-catalog.json`, `ModelCatalogMigration.php`, and
  `Analytics/UsageTracker.php`) mirror model data but keep their own tracks —
  **flag them in the PR notes, do not edit**.
- **Windows shell:** `sh` mangles double-quoted `php -r` one-liners. Always use
  single quotes around the PHP code:
  `php -r 'json_decode(file_get_contents("includes/data/model-catalog.json"), true); echo json_last_error_msg();'`
- **Single source of truth:** `includes/data/model-catalog.json` — a
  `version` + `updated_at` + `models[]` array. Entry keys are the JSON's actual
  field names: `model_name`, `provider`, `tpm_limit`/`rpm_limit`/`tpd_limit`/
  `rpd_limit`, `context_window`, `max_output_tokens`, `tier`,
  `supports_streaming`/`supports_function_calling`/`supports_vision`,
  `cost_per_1k_input_tokens`/`cost_per_1k_output_tokens`, `fallback_model`,
  `status`, `sunset_date`, `notes`.
- **Migration trigger:** `WP_MCP_AI_Model_Catalog_Migration` runs once per
  catalog `version` bump and rewrites stored references (`wp_mcp_ai_model_configs`
  option, assistant `_wp_mcp_ai_model` meta, `wp_mcp_ai_settings.default_model`
  plus the per-provider keys `deepseek_model`/`default_gemini_model`/
  `anthropic_model`/`kimi_model` since #6805).
  **Always bump `version` + `updated_at` when editing the JSON.**
- **Discovery is suggestion-only:** the daily `wp_mcp_ai_model_catalog_discovery`
  cron writes diffs to the Suggestions panel — they are **never** auto-applied.

### B1. The 13-phase checklist (run monthly, or on provider model changes)

1. **Research (web).** Check each major provider for new/deprecated models:
   OpenAI deprecations page (`developers.openai.com/api/docs/deprecations`),
   Anthropic model overview (`platform.claude.com/docs/en/about-claude/models/overview`),
   Google Gemini models blog (`blog.google`), DeepSeek pricing
   (`api-docs.deepseek.com/quick_start/pricing`). Search patterns:
   `"[Provider] API models deprecated discontinued [MONTH] [YEAR]"`.
   Tactics learned in the September 2026 run:
   - **Fire searches sequentially, not in parallel** — the search API
     rate-limits the second call of a parallel batch, forcing retries.
   - **Cross-check every model against ≥2 sources** and prefer the provider's
     own docs/changelog over aggregator trackers; trackers disagree (one claimed
     Gemini 2.5 was dead when Google listed "no shutdown date announced").
   - Useful 2026 trackers found: felloai.com's discontinued-models list,
     digitalapplied.com's monthly release tracker, OpenRouter per-model pages
     (pricing + context windows), and the providers' changelog pages.
   - **Log pricing with source + date** as you go (e.g. "Gemini 3.8 Flash
     $0.75/$3.75 intro through 2026-12-31, then $1.50/$7.50 — ai.google.dev
     changelog"). Intro/promo pricing is common — record the expiry so the next
     run knows to re-check it (DeepSeek V4-Pro promo, GPT-5.6 Sol promo,
     Gemini Flash intro rates).
2. **Catalog JSON.** Add new models with full metadata; mark deprecated models
   `status: deprecated` + `sunset_date` + `fallback_model` successor; bump
   `version`/`updated_at`; validate: `php -r "json_decode(file_get_contents('includes/data/model-catalog.json'), true); echo json_last_error_msg();"`.
   Editing tactics:
   - Edit **surgically per provider section** with `edit_file` (version bump,
     then one batch per provider), and validate the JSON + dump the changed
     entries after each batch — a whole-file rewrite loses the hand-formatting.
   - **`model_name` is unique only per provider.** `deepseek-coder` exists under
     both `deepseek` (API, removed) and `ollama` (local tag, kept). When removing
     an ID, target the full entry block including its `"provider"` field, then
     verify with a one-liner that prints provider + status for every remaining
     occurrence.
   - Removal checklist: sunset passed → remove + migration-map entry;
     retired-without-successor → keep deprecated until the provider documents one.
     Keep `gpt-4.1`, `gpt-4o`, `gpt-4o-mini`, `gpt-4.1-mini`, `gpt-4.1-nano`
     ACTIVE (pinned-ID tests).
   - One-line verification pattern used this run:
     `php -r '$d = json_decode(file_get_contents("includes/data/model-catalog.json"), true); $names = array_column($d["models"], "model_name"); foreach ([...ids...] as $n) { echo $n, ": ", in_array($n, $names, true) ? "PRESENT" : "MISSING", "\n"; }'`
3. **Migration map** — `includes/class-wp-mcp-ai-model-catalog-migration.php`
   `get_legacy_id_map()`: add legacy-ID → successor entries. **Rule:** target
   must exist in the catalog; a removed ID without a documented successor is
   not auto-rewritten.
4. **Settings defaults** — `includes/admin/class-wp-mcp-ai-admin-settings-base.php`
   `get_default_settings()` keys: `default_model`, `default_gemini_model`,
   `nvidia_model`, `cloudflare_model`, `high_token_fallback_model`,
   `openai_realtime_model`, `gemini_live_model`, `gemini_image_model`,
   `openai_image_model`. Also `includes/admin/class-wp-mcp-ai-admin-settings.php`
   (`get_default_model()` fallback + hardcoded dropdown fallback).
   **Defaults live in more than one layer** — when changing one, sweep the rest
   (this is the #6255 three-layer lesson applied to models): the settings-base
   default, the section field `'default'`/`'options'` (`section-kimi.php`,
   `section-providers.php`), the runtime fallback in consuming code (provider
   clients' `DEFAULT_MODEL` consts, tool `DEFAULT_MODEL` consts like
   `class-wp-mcp-ai-tool-generate-openai-image.php`, sanitize fallbacks), and
   the tests that pin each layer.
5. **Model selector** — `includes/class-wp-mcp-ai-model-selector.php`:
   `get_default_light_model()`, `get_default_advanced_model()`,
   `check_tpm_and_suggest_fallback()`, `get_high_capacity_fallback_model()`.
6. **Language model router** — `includes/class-wp-mcp-ai-language-model-router.php`:
   draft + verification tier maps (17 providers) + fallback defaults.
7. **Provider clients** — `includes/class-wp-mcp-ai-anthropic-client.php`
   (`list_models()` static list, `resolve_model()`, `test_connection()`) and
   `includes/class-wp-mcp-ai-gemini-live-client.php` (`DEFAULT_MODEL`).
8. **Token budget service** — `includes/services/class-wp-mcp-ai-token-budget-service.php`:
   `$model_limits`, `$default_tpm_limits`, `$model_max_output_tokens`,
   `get_higher_limit_models()`, `resolve_tiktoken_encoding()`.
9. **Cost tables** — `includes/class-wp-mcp-ai-cost-calculator.php` (per 1M
   tokens) and `includes/class-wp-mcp-ai-usage-tracker.php`
   `get_fallback_pricing()` (per 1K). Add new models, drop retired ones, remove
   expired promotional pricing (e.g. DeepSeek V4-Pro promo).
10. **Admin UI placeholders** — bulk `sed` over
    `includes/admin/class-wp-mcp-ai-admin-profession-settings.php`,
    `-admin-team-settings.php`, `sections/class-wp-mcp-ai-section-orchestration.php`,
    `includes/cli/class-wp-mcp-ai-cli-assistant-command.php`,
    `includes/class-wp-mcp-ai-model-rate-limits-cct.php`,
    `includes/class-wp-mcp-ai-token-tracking-database.php`. Also
    `includes/admin/class-wp-mcp-ai-admin-ajax-handlers.php` (test-connection
    defaults) and `includes/class-wp-mcp-ai-default-assistants.php` (pre-built
    assistant `model` values).
11. **Pro tool files** — `grep -rn "gpt-4o\|gemini-1.5\|claude-3-haiku\|claude-3-5-sonnet" addons/pro/includes/tools/`:
    fix `get_model()`/`get_research_model()` fallbacks, schema `enum` arrays,
    docblocks, `get_definition()` enums.
12. **Example files** — `assets/examples/model-config-capability-filtering.php`,
    `addons/pro/includes/metaboxes/class-wp-mcp-ai-media-template-metabox-operation.php`.
13. **Validate** — JSON validity (above), `php -l` on every changed PHP file,
    `git --no-pager diff --stat` review. Then the Docker test loop below and the
    test-drift sweep in B1b.

    **Docker test loop (learned in the September 2026 run):**

    1. The `oos-wp` container bind-mounts **one** worktree. Check which one:
       `docker inspect oos-wp --format '{{json .Mounts}}'` — if the mounted path
       isn't the worktree you're editing, `docker exec oos-wp phpunit` tests the
       wrong code. Use the cross-worktree one-off runner instead (details in the
       `mcp-ai-wpoos-test-suite` skill, "Cross-worktree runs"):
       - Build a **Linux** vendor into a named volume — the Windows-host vendor/
         breaks inside Linux (`Class "PHPUnit\TextUI\Application" not found`):
         `docker run --rm -v <worktree>:/app:ro -v <name>-vendor:/app/vendor composer:2 sh -c 'cd /app && composer install --no-interaction --prefer-dist --no-progress'`
       - Run tests in one invocation (catches cross-suite interference):
         `docker run --rm -e WP_CORE_DIR=/var/www/html -e WP_DB_HOST=db -e WP_DB_NAME=wordpress_test -e WP_DB_USER=wordpress -e WP_DB_PASSWORD=wordpress -v oos-wp_wp_core:/var/www/html -v <worktree>:/var/www/html/wp-content/plugins/mcp-ai-wpoos -v <name>-vendor:/var/www/html/wp-content/plugins/mcp-ai-wpoos/vendor --network oos-wp_default wordpress:6.9-php8.2-apache sh -c 'cd /var/www/html/wp-content/plugins/mcp-ai-wpoos && php -d memory_limit=1G vendor/bin/phpunit <files> --no-coverage'`
       - **Never two concurrent phpunit runs** — they share the `wordpress_test` DB.
       - Clean up afterwards: `docker volume rm <name>-vendor`, remove temp
         worktrees with `git worktree remove` — never stage the artifacts.
    2. **phpcs gate counts ERRORS only** (warnings don't fail CI). Run it in the
       same one-off style with `php:8.2-cli` (that image has no git): mount the
       worktree at `/app` + the vendor volume at `/app/vendor`, then
       `php vendor/bin/phpcs --standard=phpcs.xml.dist --error-severity=1 --warning-severity=1 --report=summary <changed files>`.
       To compare against HEAD, use `git worktree add ../tmp HEAD` and run phpcs
       inside that worktree — checking files copied outside the tree skews
       path-based rules. Some test files carry pre-existing docblock errors; only
       fix what your change introduces (net-error-count must not grow).
    3. **phpcbf first, then re-test.** New array keys break WPCS array alignment
       (`=>` column). Run `php vendor/bin/phpcbf --standard=phpcs.xml.dist --error-severity=1 --warning-severity=1`
       over the changed files — it edits them in place — then **re-run the PHPUnit
       batch** (phpcbf touches code, so the pre-phpcbf test run is no longer proof).
    4. **Batch-edit gotcha:** large `edit_file` batches can mangle overlapping
       regions (this run deleted a test function's signature by accident). After
       every multi-edit batch: `php -l` each file, re-read the edited regions, and
       keep new PHP assertions float-safe (`assertEqualsWithDelta`, not
       `assertEquals`, for cost math — 0.42 !== 0.42000000000000004).

    Run the model suites: `tests/test-model-catalog.php`,
    `tests/test-model-config.php`, `tests/test-model-selector.php`,
    `tests/test-token-budget-manager.php`, `tests/test-model-rate-limits-cct.php`,
    `tests/test-model-pricing-checker.php`, `tests/test-model-discovery-service.php`
    — plus every drift file from B1b in the same invocation.

### B1b. Test drift files & file surface beyond the process-doc map

The July 2026 process doc's 24-file map misses several files the September 2026
run had to touch. Grep for the IDs you changed across `tests/`,
`addons/pro/tests/`, and `tests/js/`, then update:

| File | What it pins |
|---|---|
| `tests/test-model-catalog.php` | Dropdown keys (mirror the admin Providers dropdowns), user-pinned ACTIVE ids, removed-ids-absent list |
| `tests/test-model-config.php` | `get_models_by_provider()` per provider (e.g. deepseek list after removals) |
| `tests/test-cost-calculator.php` | Exact per-model price assertions (per 1M) |
| `tests/test-deepseek-client.php` | `MODELS_WITHOUT_TOOL_CALLING`, `get_model()` settings round-trip, `build_payload` model ids |
| `tests/test-kimi-client.php` | `DEFAULT_MODEL`, `MODELS_WITH_TOOL_CALLING`, context windows |
| `tests/test-kimi-integration.php` | Sanitize-to-default fallback (section default) |
| `tests/test-admin-settings.php` | `default_gemini_model`, `openai_image_model` |
| `tests/test-onboarding-wizard.php` | Per-provider fallback map |
| `tests/test-image-tool-settings.php` + `tests/test-openai-image-tool.php` | Image tool `DEFAULT_MODEL` const + schema fallback |
| `tests/test-model-rate-limits-cct.php` | Image-model presence/absence assertions |
| `addons/pro/tests/test-oos-composition-service.php` | Seeded `_wp_mcp_ai_model` ids |

Files the 24-file map misses (all touched in the September 2026 run):

- `includes/services/class-wp-mcp-ai-model-service.php` — per-provider dropdown
  lists (watch for duplicate-key mislabels, e.g. `gemini-2.5-flash` reassigned)
- `includes/admin/sections/class-wp-mcp-ai-section-providers.php` — provider
  fallback dropdowns + default-model descriptions
- `includes/admin/sections/class-wp-mcp-ai-section-kimi.php` — Kimi dropdown,
  sanitize fallback; **dropdown defaults must exist in the catalog** (the file
  referenced `kimi-k2.7-code` which the catalog lacked)
- `includes/class-wp-mcp-ai-deepseek-client.php` — `MODELS_WITHOUT_TOOL_CALLING`,
  `MODEL_CONTEXT_WINDOWS`, docblocks
- `includes/class-wp-mcp-ai-kimi-client.php` — `DEFAULT_MODEL`, tool-calling
  lists, context map
- `includes/admin/class-wp-mcp-ai-onboarding-wizard.php` — provider fallback map
- `includes/admin/class-wp-mcp-ai-provider-diagnostics.php` — test-connection
  fallback ids per provider
- `includes/services/class-wp-mcp-ai-gemini-managed-agent-service.php` —
  `DEFAULT_MODEL` (+ docblock `@type` example)
- `includes/tools/class-wp-mcp-ai-tool-run-gemini-managed-agent.php` — schema
  default + runtime fallback
- `includes/tools/class-wp-mcp-ai-tool-deep-research.php` — per-provider fallback
  ids in the resolver + class docblock
- `includes/tools/class-wp-mcp-ai-tool-discover-new-models.php` — known-Anthropic
  static list
- `includes/tools/class-wp-mcp-ai-tool-generate-openai-image.php` —
  `DEFAULT_MODEL` const + per-model pricing tables
- `includes/cli/class-wp-mcp-ai-cli-chat-command.php` — docblock examples
- `addons/pro/includes/admin/class-wp-mcp-ai-ext-cog-settings.php` — vision-model
  dropdown + allowed-models list
- `addons/pro/includes/tools/orchestration/class-wp-mcp-ai-blueprint-installer.php` —
  provider fallback map
- `addons/pro/includes/tools/extended-cognition/class-wp-mcp-ai-tool-ext-cog-analyze-sensory-input.php` —
  schema `enum`
- The 9 pro research tools (`addons/pro/includes/tools/{research,places,quiz-management,eca-management,orchestration}/`) —
  identical `deepseek-chat` fallback pattern; grep `deepseek-chat\|gemini-3.5-flash\|claude-mythos-preview`
  and fix in one sweep

### B2. Hard rules & invariants (do not break)

- The catalog JSON is the single source of truth — never hand-edit a derived
  file without a matching catalog entry.
- `model_name` is unique only per provider — always remove/edit entries by their
  full block (including `provider`), never by name match alone.
- `status` ∈ `active` | `deprecated` | `legacy`; only `active` entries appear in
  fallback dropdowns.
- Migration-map targets must exist in the catalog.
- `tpd_limit`/`rpd_limit` of `0` means "no limit" — keep the keys present.
- **Units are per 1K in the catalog JSON and usage tracker, per 1M in the cost
  calculator.** After editing, dump the values with a one-liner — the September
  2026 run found real drifts this way: catalog `deepseek-v4-flash` 10× too low,
  usage-tracker `gemini-2.5-flash` 10× too low, cost-calculator Opus inputs 3×
  too high. Trust the provider's current pricing page over any previous doc.
- **Provider-enable invariant (PR #6255):** fresh installs disable cloud
  providers by default; `WP_MCP_AI_Model_Config::get_available_providers()` lists
  only enabled + credentialed providers. New providers must respect it.
- **User-pinned defaults must stay active** — `tests/test-model-catalog.php`
  asserts `gpt-4o` (and the other gpt-4.1 family ids) stay ACTIVE (users pin
  their IDs as fallback targets). Do not flip pinned/fallback-referenced IDs to
  inactive without a migration mapping.
- **Dropdown defaults must exist in the catalog** — if a section/file references
  an ID the catalog lacks (e.g. `kimi-k2.7-code` before this run), either add the
  ID to the catalog or change the default; don't leave the mismatch.
- Cost calculator and usage tracker use different units (per 1M vs per 1K) —
  do not cross-copy values.
- Never auto-apply discovery suggestions.
- If a change is security-adjacent (URLs, credential resolution), re-read
  `.context/security-checklist.md` before touching provider clients.

### B3. Release integration & run documentation

- Catalog changes always get a changelog mention (see v1.1.69 "model catalog
  fixes — #6274" and v1.1.40 "July 2026 model catalog").
- If the update ships in a release window, run it through Track A's P0 surfaces
  and the P3 version bump; a standalone monthly catalog refresh can ship as its
  own branch + PR without a full version bump (record it for the next catch-up).
- **Record the run in the model docs** (the September 2026 run did this): append
  a "This Month's Changes" section to
  `docs/reference/models/model-update-process-2026-07.md` (new models, status
  changes, default changes, pricing fixes, migration-map changes) and bump the
  "Last reviewed" line in
  `docs/reference/models/keeping-the-model-catalog-up-to-date.md`. If the real
  derived-file count outgrows the "~24 files" description, update that too.

---

## Track C — PR Deferred-Item Sweep (weekly review → issues list)

Reviews a window of merged/closed PRs for work the PRs explicitly deferred
("follow-up", "out of scope", "parked", "next cluster") and files GitHub issues
for what is still incomplete and untracked. Executed once for 2026-09-10 →
2026-09-17 and back one week (2026-09-03 → 2026-09-10): filed #6646–#6655,
closed-as-complete #6389.

### C0. Orientation

- **Use the `gh` CLI, not the GitHub API MCP tools** — the MCP GitHub tools
  fail with "Authentication Failed: Bad credentials" in this environment while
  `gh pr/issue` works. `gh auth status` confirms the token.
- Check `git log --all` first (direct commits from closed PRs, e.g. #6614's
  release commit, only show with `--all`).
- The sweep files issues; it never fixes code.
- Scope = the requested window (default: last 7 days) **plus one window back**
  when asked — port-wave PRs defer work that lands a week later.

### C1. Harvest

1. Dump the window's PRs (bounded windows use `updated:START..END`):
   ```
   gh pr list --repo nvdigitalsolutions/mcp-ai-wpoos --state all --limit 200 \
     --search "updated:>=YYYY-MM-DD" \
     --json number,title,body,state,mergedAt \
     --jq '.[] | "=== #" + (.number|tostring) + " [" + .state + "] " + .title + "\n" + (.body // "") + "\n"' \
     > /tmp/pr_bodies.txt
   ```
   (`/tmp` persists between terminal calls in this environment — one dump per
   window, then grep it repeatedly.)
2. Grep for deferral language (case-insensitive, always `-B 3` for context):
   ```
   grep -n -i -B 3 "defer|follow-up|followup|todo|out of scope|not addressed|future work|future pr|later pr|next pr|remaining work|parked|postponed|known limitation|left for|tracked in|issue candidate" /tmp/pr_bodies.txt
   ```
3. Read every matched section in full — a bare keyword hit is not a deferred
   item (e.g. "JS display toggles now defer to the stylesheet").
4. Separately list CLOSED-without-merge PRs (`grep "\[CLOSED\]"`) — their
   content never landed, so their plans/fixes may exist nowhere else.

### C2. Triage each candidate

- **Resolved by a later PR?** Verify with `gh pr view` / `git log --all --grep`
  (#6587's Stripe-424 follow-up → done by #6589; #6555's lib/core mirrors →
  done by #6608).
- **Tracked already?** Check the three in-repo trackers plus the issue list:
  `docs/project/ecosystem-port-tracker.md` (a cluster row ending "Remaining:
  —" means the wave completed), `docs/project/plans/docs-catch-up-open-items.md`
  (OI-1…OI-5), `docs/legal/COMPLIANCE-CHECKLIST.md` (legal ops), and
  `gh issue list --state open`. Tracked ⇒ no new issue.
- **Byte-identical quirks are NOT bugs to file.** The port policy pins upstream
  quirks as-is (unkeyed `$arguments['blueprint']` read, dead `ok` key). Only
  file *latent bugs* explicitly flagged "follow-up issue candidate" in PR
  bodies or the tracker.
- **Closed plan-only PRs lose their content** — recover the plan from the PR
  body when filing (issue #6654 recovered #6519 this way).
- **Verify every claim before filing**: `git tag --sort=-creatordate` for
  missing release tags, grep root `CHANGELOG.md`/`README.md` for stale version
  stamps, `ls build/` for ZIPs, grep `plugins/` for missing port files.

### C3. File the issues

- One issue per deferred item. Labels: `status:needs-triage` + area labels
  (`area:pro`, `area:core`, `area:tools`, `area:docs`, `area:frontend`,
  `area:ci-cd`, `area:integrations`) + `bug`/`proposal` when apt.
- Body structure that survived review:
  1. `## Source` — PR number/title + the exact deferred quote.
  2. `## Still incomplete` — verified evidence, **with the verification date**.
  3. `## Suggested scope` — a concrete follow-up plan.
  For multi-part deferrals add `## Status of each deferred item` marking what
  later PRs completed (see issue #6649's structure).
- Write bodies to `/tmp/issueN.md` with a **quoted** heredoc (`<<'EOF'`) so
  backticks/`$` stay literal under `sh`, then:
  ```
  gh issue create --repo nvdigitalsolutions/mcp-ai-wpoos --title "..." \
    --body-file /tmp/issueN.md --label "area:pro,status:needs-triage"
  ```
- Housekeeping: close stale-but-complete issues found during the sweep, with a
  closing comment referencing the completing PRs (#6389 closed after #6447 /
  #6448 landed both of its items).

### C4. Report back

Summarize in three tables: (1) filed issues with numbers, (2) already-tracked
(no action), (3) verified-resolved (no action). Offer the same sweep for the
previous window — the user will usually want it back-dated.

### Known deferral hotspots (where this repo parks work)

| Hotspot | What to expect |
|---|---|
| Ecosystem-port PRs | "Deferred (tracker-documented)" = in-wave, usually completed by a later sub-cluster — confirm the tracker row before filing |
| Docs catch-up PRs | OI-1/OI-2 parked ⇒ already issues #5968/#5967; new OI groups are *recorded in the open-items tracker, not fixed* — file an issue only when a new OI has no GitHub issue (OI-5 → #6651) |
| Release/sub-project PRs | Root docs + tags deferred to "next catch-up" and silently dropped when the PR is closed unmerged (#6614 → #6646) |
| Dependency-bump PRs | Cross-major bumps deferred "to a separate PR" (AI SDK v5) — almost never re-tracked (#6592 → #6647) |
| Legal/compliance PRs | Out-of-repo ops deferred into `docs/legal/COMPLIANCE-CHECKLIST.md` — a static checklist nobody revisits; file an umbrella issue (#6507/#6607 → #6655) |

---

## Industry-standards grounding (why the workflow looks like this)

- **Keep a Changelog** (`keepachangelog.com`): a curated, chronological list of
  notable changes for humans — never raw commit-log diffs. This is why Track A
  reads PR descriptions and classifies production vs test/docs/build PRs before
  writing the changelog.
- **SemVer discipline**: mechanical version bumps are a separate commit from
  content commits, and `package-lock.json` is never hand-edited — reproducible
  release hygiene.
- **LLM model lifecycle management** (UiPath AI Trust Layer lifecycle;
  valuestreamai 2026 lifecycle guide): deprecation target dates set at
  registration time, sunset-driven migration of stored references, a single
  registry source of truth, and provider suggestions that are never
  auto-applied. The repo's `status`/`sunset_date`/`fallback_model` fields and
  the version-gated migration routine already implement this — Track B just
  enforces it end-to-end across the ~45 derived + test-drift files.

## Shared guardrails (both tracks)

- `git log` first; another agent may own part of the scope.
- **Verify previous runs' documented claims against the actual files** — docs
  are plans of record, not proof; drift-fix commits can revert documented
  changes (see B0).
- Read the per-folder `README.md` before editing `includes/<folder>/` files.
- Every claim (paths, counts, versions) is verified against the actual PRs.
- Never commit to `alpha-working` directly; branch + PR; exclude unrelated
  working-tree noise from commits.
- **README anchor links**: after any `README.md` edit that touches headings or
  the TOC, run `python3 bin/validate-readme-anchors.py` (also enforced by the
  `link-check.yml` CI job). TOC links use GitHub's visible slug form: emoji
  headings keep the leading hyphen (`## 🧩 Overview` → `#-overview`), `&`
  becomes a double hyphen (`#-warranty--safe-use`), and hyphens are never
  collapsed or trimmed. Headings whose emoji carries a variation selector or
  ZWJ (`🛡️`, `🧑‍💻`) only resolve via GitHub's hidden fallback anchors —
  always link the visible form the validator computes.

## References

- Plan templates: `docs/project/plans/v1.1.58-docs-catch-up.md`,
  `docs/project/plans/v1.1.59-docs-catch-up.md`,
  `docs/project/plans/v1.1.83-docs-catch-up.md`,
  `docs/project/plans/v1.1.83-post-docs-catch-up.md`,
  `docs/project/plans/v1.1.84-docs-catch-up.md`,
  `docs/project/plans/v1.1.85-docs-catch-up.md`,
  `docs/project/plans/v1.1.86-docs-catch-up.md`,
  `docs/project/plans/v1.1.87-docs-catch-up.md`,
  `docs/project/plans/v1.1.88-docs-catch-up.md`,
  `docs/project/plans/v1.1.89-docs-catch-up.md`,
  `docs/project/plans/v1.1.90-docs-catch-up.md`,
  `docs/project/plans/v1.1.91-docs-catch-up.md` (latest executed — the v1.1.91
  pass over PRs #6825, #6827–#6836: the FlowHub MCP-mode connection proxy
  binding (#6836, pre-staged [Unreleased] CHANGELOG block converted), the
  MCP App OAuth discovery chain per MCP spec (#6835), the OAuth redirect
  allowlists (#6831/#6832), the orchestration CCT physical-table gate +
  DB output guard (#6827), the security-events display + double-render
  fixes (#6829/#6830), the RF-DETR presets/manifest repair (#6828), the
  nodemailer 10.x + fast-uri advisory patches (#6833/#6834), the RF-DETR
  CG Pro ecosystem port (#6825), five skill reconciliations (plugin ×3 +
  elementor ×2 + dependabot-loop + test-suite patterns 54/55 +
  ecosystem-port + updates), the stale 1.1.89 build-set removal (30
  files), and an unchanged tool count)

Preceding windows:
  `docs/project/plans/v1.1.89-docs-catch-up.md` (the v1.1.89
  pass over PRs #6802 + #6804–#6810: the Google Classroom ECA integration
  (proposal 046, 12 flag-gated Pro tools + base foundation + new webhook
  route), the Design System addon rename + token-driven email module
  (proposal 047/048, 8 addon-provided nds tools, 0.1.0 → 0.3.0), the Upwork
  MCP connection mode (#6804), the vision/remote/EZuite live-site fixes
  (#6805), the MCP legacy-dialect handshake cache (#6802), the CodeQL closure
  + dependency advisory patches (#6807/#6806), the coverage-manifest repair
  (#6808), three skill reconciliations (design-elementor-mcp-connection
  bundled sync + stamps, design-email-marketing bundled sync, design-crm MCP
  mode), the in-window ADDON_INVENTORY version correction (0.2.0 → 0.3.0),
  the stale 1.1.87 build-set removal (30 files), and +12 Pro tool-count)
- Standing open items: `docs/project/plans/docs-catch-up-open-items.md`
- Executed PR deferred-item sweep (2026-09-17): issues #6646–#6655; closed
  #6389 as complete
- Model process: `docs/reference/models/model-update-process-2026-07.md`,
  `docs/reference/models/keeping-the-model-catalog-up-to-date.md`
- Cross-worktree Docker test runner + phpcs details:
  `.agents/skills/mcp-ai-wpoos-test-suite/SKILL.md`
- File-update checklist when adding skills/context: `AGENTS.md` §6
