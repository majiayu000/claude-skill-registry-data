---
name: setup-bootstrap
description: One-time repo setup that detects tech stack, audits the codebase, pulls coding guidelines, and generates a project-specific AGENTS.md plus a CLAUDE.md shim
type: skill
user-invocable: false
---

# MTK Setup Bootstrap — Prepare Repository for AI-Assisted Development

## MTK File Resolution

Resolve MTK skill/reference/script paths per `.claude/references/mtk-file-resolution.md` unless the router already stated `MTK_ROOT=<path>` this session; `AGENTS.md`, `CLAUDE.md`, `.claude/tech-stack`, `.claude/rules/`, `tasks/`, `docs/`, `.mtk/` stay project-relative.

**Companion files:** several steps defer detail to `.claude/references/*.md`. If a companion cannot be resolved at read time, stop that step and report the missing path — do not reconstruct its content from memory.

---

You detect the tech stack, audit the codebase, and generate a tailored `AGENTS.md` — the canonical constitution every harness reads — plus the `CLAUDE.md` shim that imports it. The implementation and review agents use them as their source of truth.

## Modes

- **`--preview`** — run detection, scan and interview, then show the proposed AGENTS.md + shim + rules diff and confirm via `AskUserQuestion` before writing anything.
- **`--non-interactive`** — skip the STEP 2.5 interview.
- **`--no-verify-commands`** — skip STEP 3.5a's command verification: nothing is executed, and the Tech Stack section gets no `<!-- verified: ... -->` stamp and no `[UNVERIFIED]` annotations. The STEP 5 report says `Command verification: skipped via --no-verify-commands`.

The flags combine.

## Generation Constraints

Compliance with constitution rules degrades as the instruction count grows, and generated constitutions that list everything perform worst. So:

1. **Root AGENTS.md: target 60–80 lines, hard cap 120.** Detail goes to `.claude/rules/` or a hook. The `CLAUDE.md` shim is ~20 lines with no rule text.
2. **Trigger-action rules with the reason attached** (`When X, do Y — because Z`). Write prohibitions only for constraints the codebase actually enforces (the counter-example gate in STEP 3 decides). No `IMPORTANT:` / `YOU MUST` markers: they cause over-triggering.
3. **Mechanize what you can.** A rule a hook or the `settings.json` deny list enforces is not repeated in AGENTS.md.
4. **No aspirational rules, no list-of-everything.** Every rule comes from an observed pattern or failure in this codebase; omit what the model can read from the code.

## File Preservation Policy (non-destructive contract — read before writing anything)

Bootstrap is **additive and merge-only. It NEVER deletes a file it did not generate**, and never runs `git rm`, `rm`, or a "replace/fresh-generate" sweep over pre-existing files — even if a wrapper, runner or `--non-interactive` caller asks for "replace mode." There is no replace mode.

- **Only MTK-owned files may be overwritten in place.** MTK-owned means carrying the `<!-- mtk-setup` provenance stamp, OR one of MTK's known generated paths: root `CLAUDE.md`, `.claude/rules/*` in the standard set, `.claude/references/*`, `.claude/tech-stack`, `.claude/settings.json`, `.claude/detected-tools.json`, `.claude/mtk-version.json`, `CODE_INDEX.md`, `pre-commit-review-list.md`. Overwrite means rewrite the body — never `git rm`. **Exception:** `architecture-principles.md`, `product.md` and `decisions.md` are never overwritten once present; a re-run routes changes through `.claude/references/regen-diff-contract.md`.
- **Everything else is preserved untouched.** Never delete: nested/per-package `CLAUDE.md` at any non-root path (**even when the repo is NOT a monorepo**), `.claude/CLAUDE.md`, custom `.claude/commands/*`, custom `.claude/rules/*` outside MTK's standard set, team-added `.claude/references/*`, lockfiles, source files, or any AI-assistant config the team adopted.
- **Superseding a prior MTK file must be loud.** Remove it explicitly AND list it under "Retired prior MTK files" in the STEP 5 report. If unsure a file is MTK-owned, treat it as hand-authored.
- **Stage only your declared output** — `git add` specific generated paths, never `git add -A` / `git add .`.
- **Scratch stays out of the tree.** No `run-report.md` / `review.md` in the repo; operator scratch goes outside the working tree or is git-ignored.

## STEP 0: Detect Tech Stack

```bash
bash scripts/setup-detect.sh --json
```

Read `stacks`, `primary_candidate`, `package_manager`, `react_native.detected` / `react_native.expo`, `go_detected` and `multiple_lockfiles` (STEP 4.5 reuses this output). Markers: `*.sln`/`*.slnx`/`*.csproj` → `dotnet`; `pyproject.toml`/`setup.py`/`requirements.txt`/`Pipfile` → `python`; `package.json`/`tsconfig.json` without `*.csproj` → `typescript`.

- More than one stack → ask via `AskUserQuestion` (header "Tech stack", one option per detected stack) which is primary. Record the rest as **secondary stacks**: `setup-audit` STEP 2.6 writes them to `detected-tools.json` `secondary_stacks`, STEP 2 runs their naming/testing recipes, STEP 3.6 folds in their references.
- Empty → stop: go is not yet supported (`go_detected`), otherwise add a `tech-stack-{name}/` skill or open an issue.

Write the primary stack as a single word: `echo "dotnet" > .claude/tech-stack`.

- `.claude/tech-stack` is a **file**: never put it in a `mkdir -p` list.
- Run `mkdir`, `rm -rf` and `echo >` as separate Bash calls: conservative permission modes reject a chain containing `rm -rf`, which aborts the whole chain.

**Polyglot repos.** `.claude/tech-stack` holds the primary stack; subprojects override it with a nested `.claude/tech-stack` (closest wins) or a root `.claude/tech-stack.map` of `<glob> <stack>` lines (`web/*  typescript`). Both resolve through `scripts/resolve-tech-stack.sh`. Add a map only for a genuinely polyglot repo. Repo-wide generators use the primary stack.

Then load `.claude/skills/tech-stack-{stack}/SKILL.md` — the source of build commands, scan recipes and reference paths for the rest of the run.

**Prerequisites:** run `bash hooks/check-prerequisites.sh` and carry its warnings into the STEP 5 report; they never block.

**TypeScript only:** the `.claude/tech-stack-pm` write, the multiple-lockfiles warning and the React Native/Expo feed live in `.claude/references/bootstrap-supporting-files.md`. Read it now and follow it.

## STEP 1: Pull External Standards

### Coding Guidelines

If the stack skill's `## Coding Style Reference` names a remote source, fetch it at the **pinned SHA** and verify its sha256. **Never fetch from `main`.** The pin is bumped only by `/mtk-setup --update-guidelines`, so every bootstrap is reproducible.

For `dotnet`:
```bash
bash scripts/update-guidelines.sh --fetch CodingStyle.md --out .claude/references/dotnet/coding-guidelines.md
```

The script reads the pin (repo-local `.claude/mtk-version.json` block first, else the toolkit manifest), fetches `<sha>/CodingStyle.md`, and moves it into place only after the sha256 matches. On a failed fetch or a mismatch it exits 1 and leaves the target untouched. If the file is then absent, tell the engineer to place it manually. Never fall back to an unpinned fetch.

For `python` / `typescript`: a reference whose first frontmatter block contains `status:[[:space:]]*placeholder` is skipped — not copied, not cited. When the team removes that line, the next bootstrap ships it.

### Architecture Principles

If `.claude/references/architecture-principles.md` exists, leave it alone. Otherwise generate it from the STEP 2 findings with the `/mtk-setup --audit` template, including the repomap evidence pass (setup-audit STEP 0.5) and the mandatory `## Provenance` section (setup-audit STEP 3.5). If you cannot run those inline, delegate to `setup-audit` rather than produce an unevidenced document.

## STEP 1.5: Scan Ledger (resumable)

Persist progress with `scripts/workflow-artifact.sh` so a compaction or crash resumes instead of re-scanning.

- **At skill start:** `bash scripts/workflow-artifact.sh list`. For an incomplete `setup-bootstrap` artifact updated < 24h ago, ask via `AskUserQuestion`: "Resume from <current_step>" (skip every STEP with a `step_completed` event, reload its `outputs`/`summary`), "Start fresh" (`abandon <old-uuid> --reason engineer-choice`, then `init`), or "Cancel". An artifact ≥ 24h old is abandoned automatically (`--reason stale-24h`) with `⚠️ Abandoned stale setup-bootstrap run (> 24h old) — starting fresh.`
- **Start:** `UUID=$(bash scripts/workflow-artifact.sh init setup-bootstrap --goal "<one-line goal>")`.
- **After each STEP:**
  ```bash
  bash scripts/workflow-artifact.sh event "$UUID" step_completed \
    --data '{"step":"STEP 2","outputs":["<files>"],"summary":"<one concrete sentence>"}'
  bash scripts/workflow-artifact.sh set "$UUID" current_step="STEP 2"
  ```
  Summaries are concrete ("scanned 214 files, 3 inconsistencies").
- **End of STEP 5:** `bash scripts/workflow-artifact.sh set "$UUID" status=completed`.

For repos with >1000 tracked source files, process the scan categories one at a time: write each category's findings into its `step_completed` event and keep only a 1–2 sentence summary in context.

## STEP 2: Audit the Codebase

Run the stack skill's `## Scan Recipes` in order: Project Structure, Patterns In Use, Data Layer, Infrastructure, Naming Conventions, Testing Patterns, Configuration. Then:

```bash
git log --oneline -20
git branch -a | awk 'NR<=20'
find . -name "pull_request_template*"
```

For each secondary stack, also run its categories 5 (Naming) and 6 (Testing) so `conventions.md` covers it.

## STEP 2.5: Post-Scan Interview (skip if `--non-interactive` and no persisted answers)

The questions, adaptive-ambiguity protocol, answer routing and `setup-answers.json` schema live in `.claude/references/bootstrap-interview.md`. Read it now and follow it.

- **Answers file exists, interactive:** show a compact summary, ask only empty/new keys, offer "revise a previous answer".
- **`--non-interactive` + file:** reuse silently; print `ℹ️ Reusing persisted interview answers from .claude/setup-answers.json (--non-interactive).`
- **`--non-interactive`, no file:** skip and print `⚠️ Interview skipped. AGENTS.md will be auto-detected only — consider running without --non-interactive for better team-specific rules.`

## STEP 2.7: Ingest Existing AI-Assistant Configs

Existing Cursor/Copilot/Windsurf/Cline/Gemini configs or a prior CLAUDE.md are interview-grade input to STEP 3: read-only and evidence-anchored. Detection list, anchors and dedup/conflict rules: `.claude/references/config-ingestion.md`. Read it now and follow it. Report `Ingested AI configs: [paths, or "none found"]` in STEP 5.

## STEP 3: Generate AGENTS.md + CLAUDE.md shim + Rules Files

`AGENTS.md` holds the rules; `CLAUDE.md` imports it; `.claude/rules/*.md` hold topic detail, path-scoped; `.claude/references/` are read on demand and never duplicated; hooks and the deny list carry what is mechanically enforceable.

### Which path

- **Neither AGENTS.md nor CLAUDE.md:** write `AGENTS.md` from the template, the shim from its second block, and the rules files.
- **Hand-curated AGENTS.md (no `<!-- mtk-setup` stamp):** preserve it untouched and report it under "Preserved hand-authored files". Write the shim only if `CLAUDE.md` is absent; if both exist, leave both and name the pair in STEP 5.
- **MTK-owned constitution (stamped AGENTS.md, or any existing CLAUDE.md) → merge mode (default):**
  0. Stamped `AGENTS.md`, no `CLAUDE.md`: write the shim, leave `AGENTS.md`; report `shim written; AGENTS.md preserved`.
  1. Read the existing constitution and check for `.claude/rules/`.
  2. **Inversion migration.** A constitution-shaped `CLAUDE.md` (has `## Critical Rules`) with no `^@AGENTS\.md` line and no hand-curated `AGENTS.md` predates the inversion. **Propose** moving its body to `AGENTS.md` and replacing it with the shim, as a regen-diff proposal per `.claude/references/regen-diff-contract.md`. Never rewrite either file without approval; under `--non-interactive` it defers to NEEDS REVIEW.
  3. **Monolithic (>200 lines, full rule sections):** extract sections into `.claude/rules/` and replace the body with the lean template, preserving project-specific content (through the proposal above when the body is still in `CLAUDE.md`).
  4. **Lean constitution + existing rules:** classify and resolve each regenerated file per `regen-diff-contract.md` §2 (classification against the `.claude/.mtk-cache/` ancestor), §3/§3a (per-hunk proposals; no ancestor → additive-only), §4 (cache) and §6 (gate not skippable, non-interactive defers, never deletes). Report per-file RESULT values in STEP 5.

### Root AGENTS.md

Reproduce the first block of `.claude/references/root-agents-md-template.md`, filling placeholders from the scan and interview. End it with the mandatory footer (needed by `--audit` re-runs and compliance audits):

```html
<!-- mtk-setup: v{MANIFEST_VERSION}
     coding-guidelines: moberghr/coding-guidelines@{MANIFEST_SHA}
     generated: {ISO8601_UTC_NOW} -->
```

`{MANIFEST_VERSION}` and `{MANIFEST_SHA}` come from `.claude/manifest.json` (`{MANIFEST_SHA}` is the SHA STEP 1 fetched at); `{ISO8601_UTC_NOW}` is `date -u +%Y-%m-%dT%H:%M:%SZ`.

### CLAUDE.md shim

The template's second block: heading, the import, one plain-text pointer for a harness that reads the file literally, and the `## Claude Code only` notes. **Emit `@AGENTS.md` as a bare line**, never in backticks or a fence — wrapped, the import is inert. Claude Code's default `claude-md-or-agents-md` mode reads `CLAUDE.md` and ignores `AGENTS.md`, so the bare import is the only path to the constitution; `claude-md-and-agents-md` loads both and de-duplicates. Rule text in the shim is duplicated in one mode and lost in the other.

### .claude/rules/ files

Generate only files relevant to the project, 30–80 lines each: `security.md`, `architecture.md`, `coding-style.md` (project overrides only, never a copy of the guidelines), `testing.md`, `data-layer.md`, `performance.md`, `infrastructure.md`, `git-workflow.md`, `project-specific.md`.

**Every rule file opens with `paths:` frontmatter.** Without it the file loads into every request (measured: 30KB, ~7.5k tokens per turn, in one repo with 7 unfrontmattered files).

```yaml
---
paths:
  - "src/Handlers/**"
  - "src/Services/**"
---
```

Derive the globs from the directories the rule's own sections cite. A rule with no defensible glob folds into `AGENTS.md` or is dropped. `"**"` is allowed only with a comment saying why. A rule whose globs match nothing in the repo is dropped.

### Rules for Generation

- **Counter-example gate — run before emitting any absolute rule.** Before writing any rule containing `NEVER`, `ALWAYS`, `all`, `every` or `must`, grep for counter-examples. If ANY exist, soften to `Prefer X`, note the exception count/location, and tag `[CONVENTION]`, not `[ENFORCED]`. Absolute language and `[ENFORCED]` are for zero-counter-example, build-gated or tool-enforced rules.
- Every rule carries a section number (§X.Y) for reviewers to cite, and cites code from this codebase where possible.
- Flag conflicts: "⚠️ Guideline says X, but codebase does Y. Standardize on: [recommendation]".
- Point at `.claude/references/` files instead of copying them.
- **Live references over restated facts.** Versions, dependency lists and package-manager choice are pointed at (`see \`package.json\``), not restated; build/test command lines stay inline. `@`-import only files of ≤~50 lines — never a manifest or lockfile.
- **Cache-stable ordering:** invariants (Critical Rules, Standards Reference, Tech Stack commands) first; volatile state (project profile, monorepo layout) last, so the prompt prefix stays cacheable.

## STEP 3.5a: Verify Generated References

Before writing (or previewing), verify every concrete path, project and file claim in `AGENTS.md`, `architecture-principles.md`, every `.claude/rules/*.md` and (monorepo) every per-package `CLAUDE.md`:

```bash
bash scripts/verify-references.sh AGENTS.md \
  .claude/references/architecture-principles.md .claude/rules/*.md
# (monorepo) also pass each per-package CLAUDE.md
```

It checks backtick-spanned path claims, `.csproj` existence, framework versions and solution membership against disk, printing `STALE …` lines (exit 3) or exiting 0. On stale output: remove or correct the claim; drop a framework version no project file uses; note a stale solution entry but never edit the `.sln`. Re-run after any deletion or rename this session. Disk (`test -d` / `test -f`) is the source of truth — never solution membership, manifests or lockfiles — as of writing time, not scan time.

**Claim-level grounding (mandatory):** after writing each generated doc, run `bash scripts/verify-claims.sh <file>` and apply `.claude/references/audit-grounding.md`: rule tags `[ENFORCED]/[CONVENTION]/[ASPIRATIONAL]`, the `<!-- mtk-stamp -->` footer, zero-hit downgrades, transient-state and terminology flags, and the paste-ready weak-claims report.

### Command verification

Unless `--no-verify-commands`, verify the exact build/test/format commands before writing the Tech Stack section. Command assembly, the `verify-commands.sh` call and outcome handling — including the branch for a missing verifier or non-JSON output — live in `.claude/references/command-verification.md`. Read it now and follow it. Report `N verified, N unverified, N skipped` (or the skip reason) in STEP 5.

## STEP 3.5b: Preview Gate (if `--preview`)

With `--preview`, write nothing yet: the plan table and the `AskUserQuestion` confirmation live in `.claude/references/preview-gate.md`. Read it now and follow it.

**Unconditional:** compute the lines/tokens table and enforce the ceilings in every mode. AGENTS.md over 120 lines → print "Generated AGENTS.md exceeds 120 lines — move <section> to .claude/rules/<name>.md" and abort. A shim over ~20 lines, or holding rule text, aborts the same way.

## STEP 3.5c: Secret Scan Gate (always)

Before **any** write of a generated file, stage it and scan it, in every mode:

```bash
TMP=$(mktemp)
# write content to $TMP, then:
bash scripts/secret-scan.sh "$TMP" || { echo "secret-scan blocked write of <filename>"; rm -f "$TMP"; exit 1; }
mv "$TMP" "<target-path>"
```

On a non-zero exit: print the offending `<file>:<line>: <pattern>` lines, abort the whole bootstrap, and point the engineer at the audit output or guidelines for the leak. `MTK_SECRET_SCAN_SKIP=1` bypasses the scan for a confirmed false positive only; log the bypass prominently in STEP 5.

## STEP 3.5d: Instruction Load Check

After `AGENTS.md`, the shim and the rules are written, run `bash scripts/check-instruction-load.sh`. Fix every finding before writing the PR; exit 2 or a missing script → report "instruction load not checked" in STEP 5.

## STEP 3.6: Prune Stack Reference Files Against Detected Tools

The pruning procedure (`detected` union, per-file `tools:` intersection, override path, cache TTL) lives in `.claude/references/bootstrap-supporting-files.md`. Read it now and follow it.

## STEP 3.8: Product Context Artifacts

Follow `.claude/references/product-context.md` to generate:

- **`.claude/references/product.md`** (≤40 lines) — purpose, users, key flows, non-goals, from the STEP 2 README/docs scan and `setup-answers.json` → `answers.product_purpose`.
- **`.claude/references/decisions.md`** — ADR-lite, append-only, seeded from detectable history and interview rationale.

An existing file is preserved untouched and reported as preserved. Both writes pass the STEP 3.5c gate. After writing `product.md`, run `bash scripts/verify-claims.sh .claude/references/product.md` with the one-retry loop (fix the anchor, or delete only a self-generated line that failed); it is generated after STEP 3.5a, so it is checked here. Report surviving downgrades and one line per file (`generated` / `preserved (existing)`) in STEP 5.

## STEP 4: Set Up Supporting Files & Directories

### .claude/rules/

`mkdir -p .claude/rules` (never with `.claude/tech-stack` in the list). Then confirm every rule file has frontmatter — a missing block is how a repo ends up with every rule always-on:

```bash
for f in .claude/rules/*.md; do
  head -1 "$f" | grep -q '^---$' || echo "BOOTSTRAP BUG: $f has no auto-attach frontmatter"
done
```

### Settings Merge

Merge `.claude/references/settings-baseline.md` (`### allow`, `### deny`, `### ask`, `### settings`) first, then the stack skill's `## Settings Additions`. `### allow` → `permissions.allow`, `### deny` → `permissions.deny`, `### ask` → `permissions.ask`; `### settings` bullets (`key: value`) are top-level keys, merged only when absent so an existing value always wins. There is no top-level `allowedTools` key; never write one.

- **No `.claude/settings.json`:** create it from the baseline plus stack additions over `{}`. Never copy the toolkit's own `settings.json`.
- **Never write an MTK hook command into the target's `.claude/settings.json`.** `$CLAUDE_PLUGIN_ROOT` is defined only for hooks a plugin declares in its own `hooks/hooks.json`; in a project settings file it expands to empty and the hook runs as `bash /hooks/<name>`, failing on every call, silently (measured: 4,552 `bash: /hooks/format-on-edit.sh: No such file or directory` failures across 7 repos). Bare `hooks/...` and `$CLAUDE_PROJECT_DIR/hooks/...` dangle in plugin-cache installs. The plugin wires MTK's hooks itself; bootstrap writes only the opt-in marker (`.claude/tech-stack`). `scripts/validate-toolkit.sh` fails on a stack skill whose Settings Additions lists an MTK hook.
- **Existing `.claude/settings.json`:** if it carries legacy `permissions.allowedTools`, first run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/migrate-settings-permissions.sh" .claude/settings.json` (and on `.claude/settings.local.json` if it has the key). It activates only narrow build/test/format/lint rules; list the broad leftovers (interpreters, package managers, `curl`, bare `Write`/`Edit`) under **Needs review** — they were never in effect. Then union `allow`/`deny`/`ask` with the existing lists, no duplicates. **Strip** any existing `hooks.*` entry pointing at an MTK hook (`$CLAUDE_PLUGIN_ROOT/hooks/`, `$CLAUDE_PROJECT_DIR/hooks/` or bare `hooks/` with an MTK hook basename): the first form fails on every call, the others fire twice beside the plugin's copy. Leave non-MTK hooks untouched.
- **Write refused by the permission layer:** write the merged content to `.claude/settings.json.mtk-proposed` and add a **Needs review** line: "review the diff, then `mv .claude/settings.json.mtk-proposed .claude/settings.json`". Never skip the merge silently or retry the refused write verbatim.

### Reference File Customization

Substitute the shared references' "match existing" placeholders with scan findings — only when the scan found exactly ONE tool in a category; with several or none, leave the generic text. The per-stack substitution tables live in `.claude/references/bootstrap-customization.md`. Read it now and apply them. Never remove sections for tools not yet in use.

### Supporting files, hooks, ignore files, tooling & cross-agent mirrors

The git pre-commit hook, CI staleness gate, skills/agents checklist, `pre-commit-review-list.md` selection, `tasks/`, the learnings seed, `.mtkignore`, `.claudeignore`, analyzer configuration, the .NET companion plugin, recommended tooling, the `.claude/mtk-version.json` stamp and cross-agent mirrors live in `.claude/references/bootstrap-supporting-files.md`. Read it now and follow it.

These bind without the read:
- Never overwrite an existing git pre-commit hook (other than MTK's own shim or a legacy MTK symlink), `.mtkignore`, `.claudeignore` or `pre-commit-review-list.md` — skip and report.
- Keep `tasks/lessons.md` tracked; `.mtkignore` and `.claudeignore` are committed.
- Recommended tooling and the .NET companion plugin are surfaced, never installed.
- Cross-agent mirrors need an explicit ask — never orphan a tool a team adopted.
- The version stamp goes to `.claude/mtk-version.json` only — never a slim `.claude/manifest.json`.

## STEP 4.5: Monorepo — Per-Package CLAUDE.md (conditional)

Reuse STEP 0's `setup-detect.sh --json` (re-run if it fell out of context): `monorepo.is_monorepo`, `ambiguous`, `packages`, `packages_skipped`.

- **`is_monorepo` true:** generate per-package files below.
- **false, not ambiguous:** skip. Any existing nested `CLAUDE.md` is hand-authored: leave it and list it under "Preserved hand-authored files". Not generating per-package files is never a reason to delete existing ones.
- **false, ambiguous:** ask via `AskUserQuestion` (header "Repo layout"): "Yes — generate per-package CLAUDE.md files" / "No — single project".

`monorepo.packages` is already resolved and capped at 20; when `packages_skipped` > 0, print "Skipped N packages — generate per-package CLAUDE.md manually for any that need special context." The per-package template, its rules (15–30 line local delta, 5-line stub for trivial packages, never overwrite, never repeat root rules) and the root **Monorepo Layout** block live in `.claude/references/monorepo-bootstrap.md`. Read it now and follow it; the layout block goes in root `AGENTS.md` (inside the 120-line cap), not the shim.

## STEP 4.8: Seed Template Cache (for future re-runs)

The snapshot spec (files, layout, copy, retention) lives in `.claude/references/bootstrap-template-cache.md`. Read it now and follow it.

## STEP 4.9: Rebuild References Index

`bash scripts/build-references-index.sh` regenerates the gitignored `.claude/references.index` used to auto-select references by file pattern.

## STEP 4.95: Seed CODE_INDEX.md

Seed a root `CODE_INDEX.md` from `.claude/references/code-index-template.md` unless it exists (consumed by `prior-work-check` via `scripts/query-code-index.sh`). **Never ship the template's placeholder rows.** Populate from the audit's actual capabilities — each `path:Symbol` must resolve (`test -f` / `git ls-files`) — or write an explicitly empty index ("No capabilities indexed yet — add a row when a capability lands").

## STEP 5: Verify & Report

Emit the report from `.claude/references/bootstrap-report.md` verbatim — earlier steps route their report lines into it and `verify-claims.sh` consumes it.

## Bootstrap invariants

- **Default to merge mode** when a constitution exists — don't ask overwrite/merge/abort.
- **Count AGENTS.md lines before finishing** (target 60–80, cap 120); the shim stays ~20 lines with no rules.
- **Per-package / nested CLAUDE.md files are never overwritten OR deleted** at any non-root path, monorepo or not.
- `.claude/tech-stack` is written before completion is reported — every skill reads it.
- The generated files are meant to be committed.
