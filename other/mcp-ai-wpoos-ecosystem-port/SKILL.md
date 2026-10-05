---
name: mcp-ai-wpoos-ecosystem-port
description: Operational guide for the base+pro → Content Graph ecosystem port loop — porting Pro addon files byte-identical into plugins/nvoos-content-graph-pro cluster-by-cluster (transform rules, byte-identity verifier, standalone-only wiring, dual-matrix validation, tracker updates, PR + self-merge). Use when the user asks to "continue the loop", "do the next cluster", "port <toolkit> to CG Pro", or resumes a Wave E/F port session.
---

# Ecosystem Port Loop — Base+Pro → Content Graph Pro Addon

Operational playbook for the additive **base+pro → Content Graph ecosystem
port** (decision D5, Waves E/F). Each cluster ports base Pro addon files
byte-identical into the standalone `plugins/nvoos-content-graph-pro` addon,
wires standalone-only tool/module registration, validates both test matrices,
then self-merges after the two `PHPUnit Pro Addon` CI checks pass. Distilled
from the Wave F2 toolkit clusters (CRM through comic-creation, ending at
#6508) and the Wave F3 RF-DETR cluster (#6825, sub-cluster 1 complete).

## Canonical references (read before starting a wave)

- **Plan**: `docs/project/plans/base-pro-ecosystem-port-plan.md` (wave slicing,
  D8-compat rules, ownership boundaries).
- **State**: `docs/project/ecosystem-port-tracker.md` (per-cluster landed
  entries + the "Remaining:" tail — the source of truth for what's next).
- **Porting rules**: `plugins/nvoos-content-graph-pro/README.md` (§Porting
  rules) and the per-folder READMEs.
- **Test env**: `.agents/skills/mcp-ai-wpoos-test-suite/SKILL.md` ("Pro addon
  dual-matrix runs" + cross-worktree one-off runner).
- **Monolith registration map**: `addons/pro/mcp-ai-wpoos-pro.php` →
  `wp_mcp_ai_pro_register_tools()` — the authoritative per-toolkit tool maps
  (gated on `enable_*_toolkit` settings).

## The loop (per cluster)

1. **Pick the next slice** from the tracker's "Remaining:" tail (usually:
   data layer → tool batch(es) → admin slice → blueprint/extras).
2. **Fresh branch** from `origin/alpha-working` — only after the previous
   cluster's PR is MERGED (the next slice edits the same init/tests):
   `git fetch origin alpha-working && git switch -c feat/ecosystem-port-<slug>
   origin/alpha-working`. Never `git checkout alpha-working` (other worktrees
   own it). Stage explicit paths only — never `git add -A`, never `vendor/`.
3. **Port byte-identical** with the documented transforms (below).
4. **Wire standalone-only registration** (below) — tool filter, ecosystem
   registration, registry module, entry autoloader probe.
5. **Write characterization tests** — derive every asserted constant from the
   ported source first (see test-suite skill pattern 41: `mcp_ai_comic_char`,
   not `mcp_ai_comic_character`).
6. **Verify**: `php -l` the new files; PHPCS
   (`--standard=plugins/nvoos-content-graph-pro/phpcs.xml.dist`; phpcbf for
   array alignment; exit 0 required); the byte-identity verifier (below);
   then local dual-matrix Docker runs (filter first, then full).
7. **Update the tracker**: append the sub-cluster entry before the row's
   "Remaining:" tail and rewrite the tail (remove landed slices).
8. **Commit → push → PR to `alpha-working`** with the standard body
   (what landed, documented deviations, standalone-only wiring, validation).
9. **Merge after both `PHPUnit Pro Addon/test` checks pass** (monolith +
   standalone). The PHP Linting workflow (WPCS 3.0 + PHP Compatibility) is
   repo-wide and takes 20–30 min — local PHPCS on the changed files is the
   substantive gate; watch with `gh pr checks <n> --repo
   nvdigitalsolutions/mcp-ai-wpoos`.
10. **Start the next cluster** from the merged `origin/alpha-working`.

## Port transforms (byte-identity rules)

Every ported file keeps the body byte-identical with exactly these documented
deviations:

- Prepend a port-note header: source path, "Kept byte-identical", ownership
  boundary ("the base Pro addon owns the class in monolith installs — the
  addon boots nothing when `WP_MCP_AI_PRO_PATH` is defined"), and the
  documented deviations list.
- Add `declare(strict_types=1);` after the header.
- Text domain: `mcp-ai-wpoos-pro` → `nvoos-content-graph-pro` (for base-owned
  D8-compat copies the source domain is `mcp-ai-wpoos` — swap to
  `nvoos-content-graph-pro` either way).
- `WP_MCP_AI_PRO_PATH . 'includes/` → `NVOOS_CONTENT_GRAPH_PRO_PATH . 'src/`
  (and `_URL` / `_VERSION` swaps).
- Source directories differ per ownership: Pro-owned files come from
  `addons/pro/includes/`; base-owned D8-compat copies (tool interface, traits,
  `WP_MCP_AI_Logger`, image base, etc.) come from `includes/`.
- **Interface copies track the base file.** When the base
  `includes/interfaces/interface-wp-mcp-ai-tool.php` gains a new optional
  interface (e.g. `WP_MCP_AI_Tool_Data_Contract_Interface`,
  `WP_MCP_AI_Tool_Usage_Guidance_Interface`), port it into the CG copy
  `src/interfaces/interface-wp-mcp-ai-tool.php` in the SAME relative position
  BEFORE any CG tool implements it — a CG class implementing an undefined
  interface is a compile-time fatal in standalone mode (the monorepo root
  classmap masks it in monolith runs). Precedent: #6740 ported
  `Usage_Guidance` (interface first, then the member-mirror classes) and
  synced the copy's stale Data_Contract docblock example with the base.
- Allowed seams (only where the source requires base-owned files):
  `defined( 'WP_MCP_AI_PATH' )` guards, `file_exists`-gated requires resolving
  to the addon's `src/` copies, `class_exists` re-checks with the byte-identical
  degrade error. Never change behavior beyond the documented seam.

## Byte-identity verifier

Write a one-shot `bin/verify-<cluster>.php` that RECONSTRUCTS the expected
ported body instead of reversing the destination (the port script has already
replaced the source's own docblock header with the port-note header, so the
raw source can never diff cleanly):

1. Expected side: take the source file, strip its OWN docblock header (cut at
the FIRST closing comment marker — the same cut the port script makes), then
apply the same transforms the port script applies (path swap, text-domain
swap).
2. Actual side: take the destination, strip the port-note header (its first
closing comment marker closes the port header), strip the added
`declare(strict_types=1);` line.
3. Normalize both: collapse 3+ newline runs to `\n\n`, ltrim leading
newlines, then `rtrim`-compare.

Traps: never write `*/` inside a verifier's own docblock/comment (it closes
the comment early — parse error); cutting the DESTINATION at the port
header's end must not cut the source's own docblock on the EXPECTED side (use
the source cut on the source, the port cut on the destination). Use
**per-pair source path + source domain** (Logger: `includes/` + `mcp-ai-wpoos`;
CPTs/tools: `addons/pro/includes/` + `mcp-ai-wpoos-pro`). Delete the verifier
after use — only `bin/port-cluster.sh` is committed; per-cluster verifiers are
scratch.

## Standalone-only wiring pattern

The base tree ships many inits that NOTHING loads monolith; standalone needs
new wiring (documented as a deviation every time):

- **Slim init** `src/tools/<toolkit>/init.php`: full-body
  `! defined( 'WP_MCP_AI_PATH' )` runtime guard whenever the base init declares
  the same global helper functions (compile-time fatal otherwise); CPT
  requires; deferred admin/research-add/consolidate requires file-gated until
  those slices land; the byte-identical CPT init hook priority + enqueue
  helper.
- **Tool filter**: `wp_mcp_ai_pro_register_<toolkit>_tools( $tools )` on
  `wp_mcp_ai_pro_tools` — mirrors the monolith's inline map (subset/inert
  standalone), empty maps that fill as tool batches land.
- **Ecosystem registration**: `wp_mcp_ai_pro_register_<toolkit>_ecosystem_tools()`
  — register each tool into the graph `ToolRegistry` via
  `WP_MCP_AI_Pro_Tool_Adapter` and wrap into the nvoos/core registry via the
  AI addon's `GraphToolAdapter` (duplicate slugs non-fatal).
- **Registry module**: standalone-only `toolkit_<name>` module in
  `WP_MCP_AI_Pro_Module_Registry::define_modules()` (files guard on the init;
  "the base tree ships the init but nothing loads it" comment). Update
  `tests/test-module-registry.php` `$expected` — count the list yourself, do
  not trust handoff ordinals.
- **Entry autoloader**: add the `src/tools/<toolkit>/` (+ `examples/`,
  `harmonization/` …) subtree probe in `nvoos-content-graph-pro.php`.
- Tree-only files (not in the monolith map — CC extras, import-blueprint
  tools) are standalone-only registrations (CRM CC-extras precedent).

## Validation & test conventions

- Serving-source assertions: monolith asserts `includes/<file>`; standalone
  accepts `nvoos-content-graph-pro/src/<file>` OR `includes/<file>` for
  base-owned D8 copies (the monorepo root classmap may serve base symbols in
  the test matrix — real standalone installs have no root vendor).
- **Capability variance is per-tool, not per-batch**: before writing the
  surfaces test, `grep get_required_capability` across the whole batch — law-firm
  batches shipped `manage_options` on 1–3 tools per batch (billing-trust ×3,
  document-drafter) while the rest carry `edit_posts`. Assert a capability map,
  not a uniform string.
- **Gate-test choice**: pick a tool whose `execute()` is `edit_posts`-gated AND
  has a `missing_required` first gate after the availability check — grep
  `missing_required` across the batch first. Some tools compute with defaults
  (no missing-required gate: damages-calculator), and a `manage_options`-gated
  tool returns `wp_mcp_ai_forbidden` before any argument gate. Verify the gate
  ORDER (some tools require the calculator BEFORE the argument gate — that's
  fine; deterministic either way).
- Hook assertions on init wiring are first-loader-gated where earlier suites
  require the init in-process.
- **Admin-slice in-init wiring can't be asserted standalone**: the standalone
  test matrix boots with `is_admin()` false, so an init's `is_admin()`-gated
  admin block never fires there. Assert gate targets via `assertFileExists` and
  wire pages directly via their own `::init()` calls (PM/calendar precedent).
  Probe the actual state with a scratch test when unsure (`is_admin()`,
  `function_exists( 'wp_mcp_ai_is_base_version' )`).
- Local matrix parity: standalone ~1 skip, monolith skips every
  standalone-gated test (hundreds — not failures).
- Per-matrix commands + Docker one-off runner: see the test-suite skill.

## Common pitfalls

- **Resuming mid-cluster**: verify the worktree against the handoff before
  trusting it (`git status` + `ls` the target dir) — a reset worktree keeps
  the branch but drops uncommitted ports. Re-porting from scratch is cheap
  (port scripts re-read the source); just redo port → verify → wire → test.
- **Port scripts echo success on failed writes**: `file_put_contents` into a
  missing directory only warns and the script still prints "ported:". Create
  the destination subdir FIRST (`mkdir`), and always follow the script with
  `php -l` + `ls` on the new files.
- **Constant drift**: assert source constants, not guesses (comic character
  slug is `mcp_ai_comic_char`).
- **Module ordinals**: count from the registry test list.
- **Double-declaration hazards**: never copy a symbol the root classmap
  serves; use D8-compat copies only for `includes/tools/` (classmap-excluded)
  symbols.
- **Seam needles must be the FULL require expression**
  (`require_once WP_MCP_AI_PATH . 'includes/...php';`), never just the
  filename: a partial needle silently misses, the leftover path swap then
  leaves a BARE addon-path `require_once`, and the root classmap's base copy
  + the addon copy double-declare mid-suite (site-creator/docgen precedent —
  surfaced as "Cannot declare trait X … already in use" in the standalone
  matrix).
- **No-autoload seams for non-self-contained D8 copies**: when a base-owned
  copy itself references `WP_MCP_AI_PATH` (e.g. self-hosted-ocr-client), a
  plain `class_exists()` seam lets the monorepo root classmap win the
  autoload race and fatals on the undefined constant. Use
  `if ( ! defined( 'WP_MCP_AI_PATH' ) && ! class_exists( 'X', false ) )`
  (no autoload) — and replace only the FIRST occurrence (the seam): inner
  execute-time `class_exists` availability checks stay byte-identical.
- **Re-porting wipes post-steps**: port scripts re-read the source, so
  phpcbf whitespace fixes, header notes, and domain patches are lost on
  every re-run — keep those post-steps scripted (php -r batch) and re-apply
  after each re-port.
- **`phpcbf` exit 1** = fixed files (not an error); re-run phpcs for exit 0.
  Do NOT chain `phpcbf && phpcs` and read the combined exit code — run phpcs
  alone to verify exit 0.
- **Transient Docker slowness**: a filtered matrix run can hang mid-suite and
  hit a 600 s timeout; retry with `timeout_ms` 900000 before investigating.
- **Trackers are huge**: edit only the row tail (append sub-cluster entry +
  rewrite "Remaining:"), never the historical entries.
- **Guidance-sweep drift (~957 files, tracked as #6741).** The v1.1.83 Tool
  Description Engineering sweep added `get_usage_guidance()` to the addon
  trees but was never ported to the CG mirrors — ~957 files under
  `src/tools/` whose `addons/pro/includes/tools/` counterpart carries
  `WP_MCP_AI_Tool_Usage_Guidance_Interface`. Lint-invisible (the CG phpcs
  standard lacks the `WPMCPAI.Tools.ToolDescriptionGuidance` sniff; the root
  sniff is warning-severity), so CI stays green. When a guidance-port cluster
  is picked up, port the guidance block (text domain swapped per the
  transforms above) + add the interface to the class declaration; the member
  mirrors (PR #6740) are the precedent. Measurement:

  ```bash
  for f in $(find plugins/nvoos-content-graph-pro/src/tools -name "*.php" -not -name "init.php"); do
    grep -q "Usage_Guidance" "$f" && continue
    addon="addons/pro/includes/tools/${f#plugins/nvoos-content-graph-pro/src/tools/}"
    [ -f "$addon" ] && grep -q "Usage_Guidance" "$addon" && echo "$f"
  done
  ```
