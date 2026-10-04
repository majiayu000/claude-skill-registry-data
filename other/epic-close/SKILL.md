---
name: epic-close
description: >
  Close out a completed EPIC / sprint end-to-end: author a fact-verified meta-post
  announcing what shipped, archive the EPIC's handovers, snapshot orchestrator memory,
  gate the integration→main merge on CI-green + explicit human go, drive the version
  bump (merge-commit conventions that auto-sync classifies), and verify the release
  reached the registry/PyPI. Use when the user says "close out EPIC <n>", "wrap up the
  sprint", "ship the meta shift", "/epic-close", or asks to finalize an integration
  branch that is ready to merge to main. Generalizes the EPIC 1002 (Yggdrasil II)
  close-out. This skill orchestrates — it authors founder docs directly (superadmin)
  and delegates code/regen to workers; it NEVER merges to main without the human gate.
version: 1.0.0
argument-hint: "<EPIC number or name, e.g. 1002 / Yggdrasil II>"
---

# epic-close

Deterministic close-out procedure for a completed EPIC or sprint. It turns "the work is
done on the integration branch" into "released on main, announced, archived, and
snapshotted" — with the one mandated human gate (the merge to main) preserved.

This skill is **orchestrator-facing**. It assumes the `/gaia-orchestrator` persona:
founder docs (`root *.md`, `founder/`) are authored directly under superadmin mode; code,
schema, and regen (`src/`, `scripts/`, `registry/`, `docs/js/`, `docs/**/*.html`,
`.github/`) are delegated to workers. It never pushes to `main` directly and never merges
the integration PR without an explicit founder go on CI-green.

## Preconditions (verify before starting)

1. The EPIC's feature work is fully merged into the integration branch (`dev/<sprint>`).
   No open child PRs targeting it that belong to this EPIC (sprint-completeness: no
   follow-ups carrying the sprint's own remainder — see CLAUDE.md § Sprint Completeness).
2. The integration PR (`dev/<sprint>` → `main`) exists and is MERGEABLE. If ancestry is
   severed (e.g. after a history rewrite), repair it by **merging** `origin/main` into the
   integration branch first (never rebase — see ORCHESTRATOR.md branch-strategy invariant).
3. The live source of truth (`META.md` / `CONTEXT.md`) already reflects the ratified
   change — the meta-post *documents* what shipped, it does not decide it.

## The six steps (run in order)

### 1 — Author the announcement meta-post (show, don't tell)

Announce what the EPIC shipped as a fact-verified meta report. **Every claim must be
checked against live data**, not asserted from memory or a handover.

- **Prefer a verification workflow** for anything with numbers. A fan-out →
  synthesize → verify pipeline with an **opus synthesizer** produces publishable stats
  without hand-rework: parallel readers pull the live counts (`registry/gaia.json`
  `skills` key; TM grade distribution; named-skill totals), a synthesizer drafts the
  report, and a verify pass re-derives every number against the registry before it lands.
  Author the workflow inline (do not require the user to opt into `ultracode` for a
  routine close-out unless they ask for that scale).
- **Show, don't tell.** Work at least one concrete example end-to-end (a real skill the
  change reclassifies; a real skill an old gate would have blocked). Before/after tables
  beat prose assertions.
- **Publish via the contract**, never hand-edit HTML:
  ```bash
  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python scripts/add_post.py report \
    "<Title>" "<Queue summary.>" \
    --source docs/meta/YYYY-MM-<slug>.md \
    --author "<byline>" --label "<Label>" --date YYYY-MM-DD
  ```
  The renderer writes `docs/meta/reports/YYYY-MM-DD-<slug>.html`, prepends `posts.json`,
  and patches `docs/index.html` (queue + hero) and `docs/meta.html` (cards).
- **Verify after publish:** scan the source for banned vocabulary (`CONTEXT.md`); the
  report HTML's embedded LaTeX `<style>` carries hex colors but the hex CI guard
  (`check_hex_colors.py`) scans only `docs/**/*.js` + `docs/**/*.css` — HTML `<style>` is
  out of scope, so report HTML is safe (all prior reports share the template hex and pass
  CI). Confirm the title renders in the generated HTML.
- **Byline:** default author is `Gaia Research` unless the user requests a founder byline.
  Never invent a byline; if the EPIC is founder-authored, use the founder's stated name +
  role and preserve the approved commit/author identity.

### 2 — Archive the EPIC's handovers

- Move completed handovers/specs/roadmaps into `founder/handovers/archive/` (keep any
  explicitly-exempt forward-looking docs live — e.g. a vision doc for the next EPIC).
- Write/extend the archive `README.md` with a dated **sprint-done marker** cataloging
  what was archived and what stayed live.
- Reconcile `founder/CLAUDE.md`'s Key References table so no row points at a moved file.
- Write a standalone `EPIC<n>_CLOSEOUT_YYYY-MM-DD.md` in the archive: what shipped, the
  close-out actions, the release version, and pointers back to the MEMORY snapshot.

### 3 — Snapshot orchestrator memory

Invoke `/memory-snapshot` (or write directly, additive-only) to prepend a dated
`## State Snapshot` block to `founder/MEMORY.md`: headline, TLDR, what changed, branch
SHAs, issues/PRs, routing, lessons, open questions, token cost. Preserve every prior
snapshot verbatim.

### 4 — CI green + HUMAN GATE (hard stop)

- Push the integration branch; wait for checks. Distinguish **regressions** from
  **pre-existing baseline reds** (a red that predates the EPIC and is untouched by it is
  not a merge blocker — document it, don't chase it, unless asked). Merge on the green
  gate that the EPIC's changes actually exercise (Test / Build / Smoke).
- **STOP.** The integration→main merge is the ONLY mandated hard human gate. Do NOT
  merge without the founder's explicit go on CI-green. This is non-negotiable and
  survives every "all auto" instruction.

### 5 — Version bump via the merge commit

- The merge-to-main IS the release trigger; auto-sync classifies the bump from the HEAD
  merge-commit message. **The merge commit message MUST carry the right conventional
  token:** `feat!:` or a `BREAKING CHANGE:` footer → **major**; `feat:` → minor; `fix:` /
  `chore:` → patch. A meta shift is breaking → major. A plain merge commit ships the
  wrong version.
- **Never squash an EPIC integration PR** (destroys child-commit topology — founder/
  CLAUDE.md § EPIC branching). Use a merge commit.
- Author the `CHANGELOG.md` entry for the release version.
- The three manifests (`pyproject.toml`, `packages/cli-npm/package.json`, `registry/gaia.json`) stay
  in lockstep via the pre-commit hook; `registry/gaia.json` is Class P (gitignored) — do
  NOT hand-commit it. Class-S regen (`docs/graph/*`) belongs in CI or a clean Linux
  worktree, not a Windows hand-curation (regen there flips CRLF EOL as noise).

### 6 — Post-merge verify

- Release CD reached the target version.
- PyPI received the new CLI wheel. For `vX.Y.0` (minor/major) the "Bundle fresh registry
  snapshot" step injects the fresh registry into the wheel; verify
  `unzip -l dist/*.whl | grep data/registry`.
- The EPIC's issues are closed; `main` is healthy.
- **Proof-of-work:** post one comment on the governing EPIC issue — what shipped, key
  decisions (especially registry-semantics/policy changes), merged PR/commit refs.
- **Token spend:** log input/output by model + date to the EPIC comment and
  `founder/COST.md` per the token-spend-logging directive.

## Hard boundaries (survive any "all auto" instruction)

- **Never push to `main`.** All work lands via the integration PR through the human gate.
- **Never merge the integration PR without the explicit human go on CI-green** (step 4).
- **Never hand-edit generated HTML** (`add_post.py` owns it) or **timeline arrays** (CLI
  only) or **`registry/gaia.json`** (Class P, gitignored).
- **Author founder docs directly (superadmin); delegate code/regen to workers.**
- Respect branch-scope, redaction exemptions, Class P/S, and the Programmatic-First
  policy throughout.

## Why this skill exists

The EPIC 1002 (Yggdrasil II) close-out ran this exact sequence — verified meta-post,
founder archive, memory snapshot, CI-green human gate, `feat!:` major bump, post-merge
verify. Capturing it as a skill removes the variance the next EPIC would otherwise
rediscover: the merge-commit token that drives the version, the human gate that must not
be automated away, the "show don't tell" bar on the announcement, and the hex-guard /
Class-P / regen footguns that make the mechanical steps safe.
