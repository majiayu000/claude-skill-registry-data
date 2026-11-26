---
name: setup-refresh
description: Refresh generated setup artifacts (principles, conventions, detected tools, AGENTS.md, configs, indexes) against codebase drift — proposes diffs for engineer-edited files instead of overwriting.
type: skill
user-invocable: false
---

# MTK Setup Refresh — Detect Drift, Regenerate Scoped, Propose Diffs

## MTK File Resolution

Resolve MTK skill/reference/script paths per `.claude/references/mtk-file-resolution.md` unless the router already stated `MTK_ROOT=<path>` this session; `CLAUDE.md`, `.claude/tech-stack`, `.claude/rules/`, `tasks/`, `docs/`, `.mtk/` stay project-relative.

---

This skill re-runs setup's generators on an already-bootstrapped repo. It never re-audits blind: it consults `scripts/setup-refresh-plan.sh` for a per-artifact staleness verdict, regenerates only what drifted, and — critically — never silently overwrites a file an engineer has hand-edited. Engineer-edited files go through the diff-proposal contract in `.claude/references/regen-diff-contract.md`, the same contract `setup-audit` and `setup-bootstrap` use for their own re-run merges. `--check` (## Check Mode) is the read-only inverse: it treats the docs as normative and reports where the *code* has drifted from them, writing nothing outside `.claude/.mtk-cache/`.

## File Preservation Policy

This skill inherits the File Preservation Policy defined in `.claude/skills/setup-bootstrap/SKILL.md` (`## File Preservation Policy`) wholesale — read it before writing anything. In short: only MTK-owned files may be overwritten in place, everything else (nested CLAUDE.md, custom rules, custom references, lockfiles, source) is preserved untouched, and superseding a prior MTK-owned file must be reported loudly, never silent. Refresh must not weaken this contract in any way — it has strictly more ways to go wrong than bootstrap (drift scoping, cached ancestors, diff proposals), and every one of them defaults to preserving what's on disk.

## STEP 0: Preconditions

Require a prior bootstrap:

```bash
test -f .claude/tech-stack || MISSING_TECH_STACK=1
test -f .claude/mtk-version.json || MISSING_VERSION=1
```

If either file is missing, stop immediately and tell the engineer:

> "This repo has not been bootstrapped yet (`.claude/tech-stack` and/or `.claude/mtk-version.json` missing). Run `/mtk-setup` (full bootstrap) first, then `/mtk-setup --refresh` on future re-runs."

Do not attempt a partial refresh, and do not fall back to generating these files yourself — that is bootstrap's job, not refresh's.

Otherwise, resolve the active stack as usual: `bash scripts/resolve-tech-stack.sh "$PWD"` (polyglot-aware — subproject `.claude/tech-stack` → root `.claude/tech-stack.map` glob → root file), then load `.claude/skills/tech-stack-{stack}/SKILL.md`. Its `## Scan Recipes` section is the input STEP 3 uses when a full re-audit is required. In a polyglot repo, run the scan recipes per declared subtree rather than once against the root stack.

## Check Mode (`--check`)

Read-only: no doc, source file or `tasks/todo.md` is written without approval, and nothing outside `.claude/.mtk-cache/`. Run STEP 0's preconditions, then:

1. **Staleness gate.** `bash scripts/setup-refresh-plan.sh --check`. Print the table verbatim and keep the exit code: `0` fresh, `1` stale, `2` usage/setup error (report it and stop).
2. **Claim regrade.** For each stamped doc (`architecture-principles.md`, `conventions.md` carrying `<!-- mtk-stamp`), copy it to a temp dir and run `bash scripts/verify-claims.sh <temp copy>`. The script rewrites its input, so it never runs on the on-disk doc, and the copy is never written back. Check each exit code: a nonzero exit is an engine failure, not a clean result. Stop with "verification engine failed for `<doc>` (exit N)" and do not read that doc's `weak-claims-*.json`, which may be stale. Otherwise read `.claude/.mtk-cache/weak-claims-<doc-basename-slug>.json` (an out-of-repo input falls back to its basename) and take its `weak` array.
3. **Drift pairing.** `bash scripts/audit-drift-check.sh <doc> --json` is read-only. Attach each `drift` entry whose `cited_anchor` matches a weak claim's anchor as that item's changed paths.
4. **Grade** each `weak` entry by its *original* tag (the `text` field, before the downgrade), per S1.15: `[EXTRACTED]`/`[ENFORCED]` → **blocking**; `[INFERRED:N]` with N ≥ 0.7 → **flag**; `[INFERRED:N]` with N < 0.7, or `[AMBIGUOUS]` → **note**. Each item quotes the principle line, the failed anchor (or "claim carries no evidence anchor"), and the changed paths (or "no drift-check match — anchor may be a symbol"). It ends with a one-line direction for the human, never a diff or a rewritten rule. Report nothing that is not a `weak` entry: an impression with no failing claim is not an item, and an empty `weak` array after exit 0 is a clean `0/0/0`.
5. **Report.** Write `.claude/.mtk-cache/check-report.md` (per doc: stamp SHA vs HEAD, then blocking → flags → notes) and print `| doc | blocking | flags | notes |`. Outcome: fresh only when the plan exited 0 and there are no blocking items.
6. **Todo append, interactive only.** Offer via `AskUserQuestion` to append the blocking items to `tasks/todo.md`. In a non-interactive run, never ask and never append; say "todo-append skipped: non-interactive run". The report file keeps the items.

## STEP 1: Staleness Plan

Run the plan script and read its structured output — this is the sole source of truth for what has drifted:

```bash
bash scripts/setup-refresh-plan.sh --json
```

Parse each artifact row (the script emits full paths: `.claude/references/architecture-principles.md`, `.claude/references/conventions.md`, `CLAUDE.md`, `.claude/detected-tools.json`, `AGENTS.md`, `path-references`, `permissions-baseline`, and the informational `.claude/setup-answers.json` row) for its `status` (`fresh` / `stale` / `missing` / `unstamped` / `unknown` / `present` / `absent`) and `reason`. STEP 3 scopes its regeneration entirely from this plan — do not re-derive staleness by re-reading the codebase from scratch. If the plan script itself fails or is not found, stop and report the failure; do not silently degrade to a full re-audit as a workaround.

## STEP 2: Dry-Run Gate

If `--dry-run` was passed:

1. Re-run `bash scripts/setup-refresh-plan.sh` **without** `--json` and print the resulting plan table verbatim — every row, no reformatting or summarizing away entries (the table format exists only in the default output mode).
2. Follow it with one paragraph describing what a full refresh would do, per stale/missing row (e.g., "`architecture-principles.md` is stale — 4 claims touch changed files under `src/Api/`; a refresh would re-read those files plus their containing modules, regenerate the affected sections, and propose any resulting diff against your on-disk copy per the regen-diff-contract before writing anything").
3. Stop. Write nothing — no docs, no cache entries, no stamps, no `.claude/detected-tools.json` updates.

## STEP 3: Scoped Regeneration

For each artifact the plan marked `stale`, `missing`, or `unstamped`, apply the matching procedure below (`unstamped` docs route to the full-re-audit path — there is no stamp to scope by). Skip rows marked `fresh` or `unknown` — leave those files exactly as they are. The informational `setup-answers.json` row never drives regeneration; STEP 5 handles it.

**Temp-path mandate:** STEP 3 never writes a regenerated doc to its on-disk path. Every regenerated doc goes to a temp path (e.g. `/tmp/mtk-refresh/<file>`); only STEP 4 — the diff-proposal contract — may touch the on-disk copy. The two exceptions are the deterministic artifacts explicitly listed below (AGENTS.md/tool configs/indexes), whose generators carry their own marker-refusal guards.

### `architecture-principles.md` / `conventions.md`

1. Get the stale-claim scoping input from the same drift source the plan consulted: `bash scripts/audit-drift-check.sh <doc> --json` — its `drift` array pairs each changed path with the claim anchor it touches.
2. Compute the **full** changed-file set yourself (the drift check reports only the changed ∩ cited intersection, which systematically undercounts churn): read the doc's `audited-against:` stamp, then `git diff --name-only <stamp>..HEAD`. Count tracked source files for the active stack (`git ls-files` filtered to stack extensions) as the denominator.
3. **Full re-audit** (re-run `setup-audit`'s STEP 0.5 through STEP 3.7 for this doc, in full) only when: the doc's stamp is missing or unreadable, **or** the full `git diff` changed set from item 2 exceeds ~30% of tracked source files. In that case, treat this as equivalent to a fresh `/mtk-setup --audit` for this one document.
4. **Scoped regeneration** (the default path): re-read only the changed files reported by the drift check, plus the directories/modules that contain them. Re-derive only the principle/convention lines whose evidence anchors point into that changed set. Every other section is carried over **verbatim, byte-for-byte** from the current on-disk doc — do not reword, re-flow, or "improve" untouched sections. This keeps prompt-cache prefixes stable and keeps the diff STEP 4 has to reason about small and honest.
5. Either way, the regenerated doc is written to the temp path, never in place. Run `setup-audit` STEP 3.5 (Provenance section) against the temp copy so `fresh` is complete before classification. Stamping and verify-claims happen in STEP 5, against the on-disk doc **after** STEP 4 has resolved the proposals — the engineer-approved state is what gets stamped and verified, not the unreviewed template.

### `.claude/detected-tools.json`

Re-run `setup-audit` STEP 2.6 (tool detection) only — do not re-run the full scan recipes. Write the result to a temp path first; STEP 4 diffs it against the on-disk copy before deciding whether to overwrite (this file is machine-generated and deterministic, but a manual edit is still possible and must not be clobbered silently).

### Reference pruning

Re-run `setup-bootstrap` STEP 3.6 (prune stack reference files against detected tools) against the freshly regenerated `detected-tools.json`. This may newly ship a reference file that was previously pruned (a tool got detected). **Refresh-time pruning affects only which files would be *newly shipped* — it never deletes or proposes deleting an on-disk reference file.** "Prune" is a ship-time filter, not an operation on existing files (File Preservation Policy).

### `AGENTS.md` + tool configs + indexes

**Branch on the row's `reason`, not just its status.** Row 5 of `setup-refresh-plan.sh` reports three distinct `AGENTS.md` provenances, and only one of them is a generator's to reconcile. Read the reason string and pick exactly one branch:

**(1) Footer-version drift on an mtk-stamped AGENTS.md** — reason names the footer and the installed version (e.g. `AGENTS.md footer stamped v7.29.0, installed v7.30.0`). This AGENTS.md is the canonical constitution written by `setup-bootstrap` from `.claude/references/root-agents-md-template.md`: it is **authored, never regenerated**. Do **not** run `generate-agents-md.sh` for this row — against a canonical AGENTS.md it exits 0 *without writing*, so a 0 here means "declined", not "regenerated". Instead, treat AGENTS.md exactly as `CLAUDE.md` and `.claude/rules/*.md` are treated below: compute the fresh template content as `setup-bootstrap` would, write it to a temp path, and hand it to STEP 4 so `.claude/references/regen-diff-contract.md` classifies it against the cached ancestor and proposes the MTK delta hunk-by-hunk. Under `--non-interactive`, unresolved hunks land under **Needs review** — never auto-applied, never force-merged.

**(2) Legacy generator-marked AGENTS.md** — reason mentions the auto-generated marker or `regenerated content differs from on-disk AGENTS.md`. This file really is generator output, so keep the deterministic path (no `--force`):

```bash
bash scripts/generate-agents-md.sh
```

**(3) Hand-curated AGENTS.md (`unknown`)** — no footer stamp and no auto-generated marker. Leave it untouched, list it under "Preserved hand-authored files", and report it as a Needs review item if the plan flagged it. The generator is never invoked against it.

Tool configs and derived indexes are unaffected by the branch above and run whenever `AGENTS.md` or `path-references` is `stale`/`missing`:

```bash
bash scripts/generate-tool-configs.sh --all
bash scripts/refresh-derived.sh references
```

`generate-tool-configs.sh` may write in place because it carries its own preservation guard: it refuses to overwrite any output file that lacks its auto-generated marker. **A marker-less config (GEMINI.md, `.windsurfrules`, …) is hand-curated — leave it alone, list it under "Preserved hand-authored files", and note it as a Needs review item if the plan flagged it.** Never pass `--force` to reconcile a staleness row; a row that cannot be reconciled without `--force` means the file is not MTK's to regenerate. `refresh-derived.sh` is idempotent and silent on no-op, so running it at the end of this step regardless of the trigger is safe and keeps `.claude/references.index` in sync with whatever STEP 3 just touched.

### `.claude/settings.json` permission keys

Runs on every refresh, regardless of the plan (like `refresh-derived.sh`). Earlier bootstraps wrote stack allow lists under `permissions.allowedTools`, a key Claude Code does not read (its permission lists are `permissions.allow` / `deny` / `ask`), so those entries never applied. Activate the narrow ones:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/migrate-settings-permissions.sh" .claude/settings.json .claude/settings.local.json
```

The script is idempotent: a file without the bad key, or a missing file, is left byte-for-byte untouched. It moves only an explicit allow-list of narrow build/test/format/lint rules into `permissions.allow`, printing each one; every broad entry (interpreters, package managers, `curl`, bare `Write`/`Edit`) stays inert under `allowedTools`. Report each activated entry under `Updated`, each left-inert entry under `Needs review` (the engineer decides whether to grant it — it was never in effect), and each untouched file under `Preserved (untouched)`.

### `permissions-baseline` (`.claude/settings.json` deny/ask rules)

When the plan marks `permissions-baseline` `stale`, the repo's `.claude/settings.json` lacks deny/ask rules from `.claude/references/settings-baseline.md` — every repo bootstrapped before 8.1.0 lacks all of them, and those deny rules are what now keep secret files (`.env`, keys, keystores, `.npmrc`, SSH keys) out of context since `read-guard.sh` was retired. List them, and build the merged candidate at a temp path (never in place):

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/settings-baseline.sh" --missing .claude/settings.json
bash "${CLAUDE_PLUGIN_ROOT}/scripts/settings-baseline.sh" --merge .claude/settings.json --out /tmp/mtk-refresh/settings.json
```

The merge is `hooks/merge-settings.sh`'s union: every existing key and rule stays, only the missing baseline rules are added. Hand the temp copy to STEP 4 as `fresh`. `.claude/settings.json` is protected and engineer-owned, so it is always proposed, never overwritten: show the missing rules as one hunk per list (`permissions.deny`, `permissions.ask`) and any missing baseline settings keys (`settings\t<key>: <value>` lines, e.g. `autoCompactWindow`) as their own `settings` hunk via `AskUserQuestion`, write the approved ones with `--merge` (without `--out`), and report them under `Updated`. A declined hunk is listed under `Preserved (untouched)` with "engineer kept the current rules"; under `--non-interactive` nothing is written and every missing rule lands under **Needs review**. A row marked `unknown` (helper missing, invalid JSON) is reported as is — never hand-edit the file to work around it.

### `CLAUDE.md` and `.claude/rules/*`

Never rewritten in place, regardless of staleness reason (version-drift footer or stale dependency mentions). Compute the fresh template content as `setup-bootstrap` would, then hand it to STEP 4 — CLAUDE.md and every `.claude/rules/*.md` file always go through the diff-proposal contract, never a direct `Write`.

### Retired generated indexes

Runs on every refresh, regardless of the plan. Older MTK versions generated a rule index and a keyword-trigger index that nothing reads any more. `.claude/rules/INDEX.md` is the costly one: it has no `paths:` frontmatter, so Claude Code loads it into every session. Find the candidates:

```bash
for f in .claude/rules/INDEX.md .claude/rules/triggers.index .claude/triggers.index; do
  [ -f "$f" ] && awk 'NR<=5' "$f" | grep -qiE 'generated by `?scripts/build-(rule-index|triggers-index)\.sh' && echo "$f"
done
```

Only a file whose header names one of those two generators is a candidate. A file at the same path without that header is hand-authored: list it under "Preserved hand-authored files" and leave it alone. **Propose each deletion. Never delete without the engineer's approval.** This is the File Preservation Policy's loud-retirement case, and the regen-diff-contract never deletes by itself. Ask once per file via `AskUserQuestion`, naming the path and its generator header and giving the reason (generated, no consumer, and for `INDEX.md` an always-on load). On approval, run `git rm -q <file>` if the file is tracked and `rm <file>` if it is not, then list it under "Retired prior MTK files". On a decline, list it under `Preserved (untouched)` with the reason "engineer kept it". Under `--non-interactive`, delete nothing and list each candidate under **Needs review**. Under `--dry-run`, STEP 2 has already stopped, so name the candidates in its paragraph instead.

## STEP 4: Engineer-Edited Files

For every file STEP 3 regenerated or would regenerate (`architecture-principles.md`, `conventions.md`, `CLAUDE.md`, each `.claude/rules/*.md`, `.claude/detected-tools.json`, `.claude/settings.json` when STEP 3 proposed baseline rules, and `AGENTS.md` when STEP 3 routed it here via the footer-drift branch), resolve `ancestor` / `current` / `fresh` and apply `.claude/references/regen-diff-contract.md` exactly as written there — do not re-derive or restate its classification, diff-proposal, or cache-update rules here. In short: files unchanged since the last generation overwrite cleanly; files an engineer edited get their MTK delta proposed hunk-by-hunk via `AskUserQuestion`, never force-merged; hunks that no longer apply cleanly land under **Needs review** with the conflicting region quoted; protected files (`manifest.protected`) that this run has no business touching are reported `SKIP`.

Run this step for every candidate file even if STEP 3 judged the underlying content unchanged — the contract's own `current == ancestor` check is what decides "safe to overwrite," and that decision belongs to the contract, not to this step.

When applying resolved content to `.claude/references/architecture-principles.md`, write via a temp file promoted through the shrink guard (S3.16), same as `setup-audit`:

```bash
. hooks/lib/shrink-guard.sh
mtk_guarded_write .claude/references/architecture-principles.md "$tmp"
```

## STEP 5: Grounding

For every doc whose on-disk copy STEP 4 actually changed (wholesale stock overwrite or applied hunks):

1. **Sync Impact stamp.** Refresh the `<!-- mtk-stamp -->` block with the three re-run fields, computed by diffing the regenerated doc against its previous on-disk version **before** writing:
   ```
   <!-- mtk-stamp
   audited-against: <sha>
   audited-at: <ISO8601>
   mtk-version: <version>
   previous-stamp: <previous audited-against sha, or "none">
   sections-changed: <comma-separated H2 titles, or "none">
   claims-delta: +<added> ~<modified> -<removed>
   -->
   ```
2. **Verify-claims retry loop.** Run `bash scripts/verify-claims.sh <doc>`. Read `.claude/.mtk-cache/weak-claims-<doc>.json`. For each downgraded claim, make exactly **one** re-derivation attempt: re-locate correct evidence (fix the anchor — right path, right glob, right symbol), or, if it truly cannot be evidenced, delete the claim line — **but only if the line is byte-identical to the `fresh` template's version** (i.e., this run generated it). A line the engineer authored or modified is never deleted by the retry loop: leave the downgraded tag in place and let the engineer decide. Every deleted line must be itemized in the STEP 6 report. Rewrite the doc and run `verify-claims.sh` once more. Downgrades that survive the second pass are accepted and reported in STEP 6 — never loop a third time, and never re-upgrade a tag without a resolving anchor.
3. **Load `.claude/setup-answers.json`.** If present, treat its contents as authoritative human input. Any rule or claim sourced from it must keep the evidence-anchor convention (`Evidence: engineer interview — .claude/setup-answers.json (hard_nevers)`), which always resolves for `verify-claims.sh` (it checks the path exists before content-grep) — engineer-stated rules are therefore never auto-downgraded by the verify pass. Regeneration must not drop or reword a rule sourced from this file. If a fresh scan finding contradicts an interview answer, do not silently pick a side — emit a **Needs review** item citing both the answer and the contradicting finding.

## STEP 6: Report

First bump the repo's version stamp, so session-start and `mtk-doctor` stop pointing at a refresh that just ran — but only when this run left **no** `Needs review` item and no declined MTK hunk; otherwise report `stamp left at <old>: <N> item(s) still need review` and do not run it, so the nudge stays until the engineer resolves them. Skip it in check mode, which writes nothing outside `.claude/.mtk-cache/`. The script never lowers a newer stamp:

```bash
bash "$MTK_ROOT/scripts/stamp-version.sh" --manifest "$MTK_ROOT/.claude/manifest.json"
```

Put its one line (`stamp 7.24.0 -> 9.4.2`, or `stamp already …`) in the report. On exit 2, report the reason; do not hand-edit `.claude/mtk-version.json`.

Then print a summary with four counts — `Updated`, `Created`, `Preserved (untouched)`, `Needs review` — followed by an itemized list of every needs-review item.

**A count of `Updated` is a claim that a file on disk changed — never infer it from a generator's exit code.** A generator that exits 0 may have declined to write: `generate-agents-md.sh` prints `AGENTS.md is already the canonical constitution (CLAUDE.md is absent or a shim importing it) — nothing to regenerate.` and exits 0 without touching the file. That stdout note is the signal — when you see it, report the file under **Preserved (untouched)** as "generator declined — AGENTS.md is the canonical constitution", never under `Updated`. The same applies to any run whose diff is empty: a file whose bytes did not change belongs under `Preserved (untouched)` with the reason "no change", not under `Updated`. Confirm a change before counting it (e.g. `git status --porcelain <file>`); an exit-0 no-op reported as a regeneration is a false completion claim.

Apply the same preservation reporting rules as `setup-bootstrap` STEP 5: list every preserved hand-authored file (or "none found"), and if any MTK-owned file was retired this run, list it explicitly under a "Retired prior MTK files" heading — never let a retirement pass silently.

```
✅ MTK SETUP REFRESH COMPLETE

Plan:      [N] fresh, [N] stale, [N] missing, [N] unstamped/unknown

Updated:            [N]
  [file — RESULT from regen-diff-contract, e.g. "architecture-principles.md — scoped regen, 3 sections re-derived"]
Created:            [N]
  [file — e.g. "conventions.md — was missing"]
Preserved (untouched): [N]
  [file — reason, e.g. "CLAUDE.md — PROPOSED (2 hunks: 2 applied, 0 skipped)" or "conventions.md — fresh, no drift"]
  [file — e.g. "AGENTS.md — generator declined (canonical constitution), nothing written"]
Needs review:       [N]
  [file — hunk description and quoted conflicting region, per regen-diff-contract]

Preserved hand-authored files (untouched):
  [nested CLAUDE.md, custom rules/references outside the standard set — or "none found"]
Retired prior MTK files (explicitly removed this run):
  [MTK-owned files this run superseded — or "none"]

Next steps:
  1. Resolve each Needs review item — the conflicting region is quoted above
  2. Re-run `/mtk-setup --check` to confirm the plan is now clean
```

## Verification

- `bash scripts/setup-refresh-plan.sh --json` ran and its output drove every scoping decision in STEP 3 (no ad-hoc staleness judgment).
- No file outside the plan's `stale`/`missing` artifacts (or the derived AGENTS.md/tool-config/index set, the `allowedTools` key move in `.claude/settings*.json`, or an engineer-approved retired index) was modified; no non-MTK file was modified or deleted.
- Every doc rewritten in STEP 3/4 carries a refreshed `<!-- mtk-stamp -->` with `previous-stamp` / `sections-changed` / `claims-delta` populated.
- `scripts/verify-claims.sh` ran per refreshed doc, including the one-retry loop where downgrades occurred.
- Every engineer-edited file — including an `AGENTS.md` row flagged for footer-version drift — went through `.claude/references/regen-diff-contract.md`, not `generate-agents-md.sh`: no direct `Write` to `CLAUDE.md` or any `.claude/rules/*.md`, no `git merge-file --union`, and no exit-0 generator no-op reported as `Updated`.
- Each retired generated index (`.claude/rules/INDEX.md`, `.claude/rules/triggers.index`, `.claude/triggers.index` carrying a `build-rule-index`/`build-triggers-index` header) was deleted only after the engineer approved it and is listed under "Retired prior MTK files"; under `--non-interactive` none was deleted.
- `scripts/stamp-version.sh` bumped `.claude/mtk-version.json` only when nothing was left under Needs review (never in check mode), and the STEP 6 report was printed with its line, all four counts and an itemized needs-review list (or explicit "none").
- Check mode: `verify-claims.sh` ran only on temp copies with every exit code checked; every item cites a `weak` entry; nothing outside `.claude/.mtk-cache/` was written, and `tasks/todo.md` only after interactive approval.
