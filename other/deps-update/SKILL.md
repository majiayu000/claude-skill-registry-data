---
name: ha:deps-update
description: Bump outdated HA requirements — inventory, snapshot changelogs, update, fix breaks, split reviewable PRs (dependency bumps ALWAYS a separate PR). Use to upgrade/bump manifest `requirements` or core/test requirements when versions fall behind. NOT for pip install failures (/ha:investigate).
effort: high
argument-hint: "[--scope patch|minor|major|all] [--pkg <name>...] [--pr-per major|area|none] [--dry-run]"
---

# Dependency Update (Freshness)

Inventory → update → fix breaks → grouped PRs. This is the only MUTATING
deps skill: it edits `manifest.json` `requirements`, the generated
`requirements*.txt`, and source. Security scanning stays in
`/ha:deps-audit`; the vet ledger stays in `/ha:deps-vet`.

## Usage

```
/ha:deps-update                         # inventory + interactive scope pick
/ha:deps-update --scope patch           # bundle all patch bumps (one PR per lib)
/ha:deps-update --pkg aiohttp           # one package (+ every manifest using it)
/ha:deps-update --dry-run               # inventory only, no changes
```

## Iron Laws

1. **Dependency bumps are ALWAYS a separate/preliminary PR (PR1) ★TOP** —
   a bump never rides along with a bug fix or feature. "Please split the
   bug fix and the dependency bump into two PRs." (edenhaus,
   https://github.com/home-assistant/core/pull/165959#discussion_r2959065055).
   One library per PR. **Carve-out (C2)**: a *brand-new* library ships in
   the SAME PR as the code that first uses it (the dependency exception
   inverts for new libs — docs/framework-dev-laws.md C2). Existing-library
   version bumps never get this exception
2. **Requirements are EXACT pins — every bump is a `manifest.json` edit** —
   integration deps are `pkg==1.2.3` in `manifest.json` `requirements`;
   there is no semver range to "update within". Edit the pin, then
   regenerate (`python3 -m script.gen_requirements_all`). Never hand-edit
   `requirements_all.txt`/`requirements_test_all.txt`/`package_constraints.txt`
   — they are generated (see `${CLAUDE_SKILL_DIR}/references/update-mechanics.md`)
3. **NEVER introduce a pre-release or git/URL requirement (P11)** — manifest
   requirements must be CI-published, tagged, exact-pinned PyPI releases; no
   `==1.2.3rc1`/`.dev`/`a`/`b` and no `git+`/`https://…tar.gz`. Fix upstream,
   cut a release, then bump
4. **ALWAYS snapshot the changelog delta BEFORE updating** — capture the
   GitHub releases page or the PyPI JSON (`https://pypi.org/pypi/<pkg>/json`),
   then delta against the new version. Never update blind
5. **NEVER claim an update is safe without verification** — run `/ha:verify`
   (`ruff` + `mypy` + `hassfest` + `pytest`). "Type-checks" ≠ "works"
6. **ALWAYS move a shared package together across every manifest** —
   HA enforces ONE version per PyPI package across all integrations
   (`gen_requirements_all`/hassfest fail on divergence). Bumping `aiohttp`
   in one manifest means every `manifest.json` requiring it moves in the
   SAME commit (see `${CLAUDE_SKILL_DIR}/references/coupled-groups.md`)
7. **NEVER commit a partial bump** — the `manifest.json` edit(s) + the
   regenerated `requirements_all.txt`/`requirements_test_all.txt`/
   `package_constraints.txt` land in ONE commit
8. **HAND OFF security to `/ha:deps-audit`** — run it on the requirements
   diff before any PR; don't reimplement audit rules
9. **`pip list --outdated` "outdated" output is normal** — it means "deps
   are behind", not failure. Capture with `|| true`

## Workflow

### Phase 0: Discover

Detect the target (see `${CLAUDE_SKILL_DIR}/references/update-mechanics.md`
"Target detection"): HA core checkout (`homeassistant/__init__.py` + `script/`),
custom integration (`custom_components/*/manifest.json`), or ha-frontend
(`package.json` with `"name": "home-assistant-frontend"` — frontend uses the
Yarn path, unchanged). Read every in-scope `manifest.json` `requirements`,
plus core `requirements.txt`/`pyproject.toml` and `requirements_test.txt`.
Create scratch dir `.claude/deps-update/{YYYY-MM-DD}/`.

### Phase 1: Inventory

`pip list --outdated --format json || true` for what's installed, cross-checked
against each pinned `manifest.json` requirement via the PyPI JSON
(`https://pypi.org/pypi/<pkg>/json` → `info.version`). Classify each package
patch/minor/major by semver delta pinned→latest. Map every package to the set
of manifests that pin it (shared-package fan-out). Write `inventory.md` to
scratch. Render grouped table: Patch / Minor / Major / Pre-release-only
(skip — P11) / Git-or-URL (manual, forbidden — P11). `--dry-run` stops here.

### Phase 2: Scope (AskUserQuestion)

Present groups with counts and risk. Default recommendation: "Patches (N)
— low risk, one PR each". `--scope`/`--pkg` flags skip the prompt. When a
package is pinned by ≥2 manifests, force every one of them into the same
step (Iron Law 6) even under a narrower scope.

### Phase 3: Per-Package Update Loop

For each selected package, one library at a time (PR1 = one bump per PR):

1. Snapshot the current changelog (GitHub releases page or PyPI JSON
   release notes) → `scratch/before/`
2. Update — edit the `==` pin in EVERY `manifest.json` that requires the
   package to the same new version, then regenerate:
   `python3 -m script.gen_requirements_all` (core checkout). For a custom
   integration there is no generator — edit the single `manifest.json`
3. `git diff` on `manifest.json` + `requirements_all.txt` +
   `requirements_test_all.txt` + `package_constraints.txt` → the REAL
   `{pkg, old, new}` set (the generator resolves transitive/constraint
   shifts the inventory never listed)
4. Changelog delta: fetch the GitHub releases page for the tag range, or the
   PyPI JSON release entries diffed against the snapshot — keep the relevant
   hunk. Empty → PyPI "Release history" fallback → compare-URL note (see
   `${CLAUDE_SKILL_DIR}/references/changelog-sources.md`)
5. Write `scratch/{pkg}-{old}-{new}.md`
6. `python3 -m script.hassfest --requirements` (validates the pins,
   constraint consistency, and that no pre-release/git ref slipped in)

### Phase 4: Verify

Run `/ha:verify`. On failure → Phase 5; else Phase 6.

### Phase 5: Breaking-Change Fixes

Read the changelog deltas for "breaking"/"removed"/"deprecated" + the
`mypy`/`pytest` errors. Fix source (apply the sibling-file check). A
user-visible break also needs the PR3 treatment (breaking-change section,
migration, deprecation period). Re-verify.

### Phase 6: Security Handoff

Run `/ha:deps-audit` on the working requirements diff (its Mode B default).
BLOCK findings → surface and offer `/ha:deps-vet <pkg> <ver>` for accepted
risks. Never skip this before a PR. (Escape hatch for the install-time gate:
`HA_SKIP_DEPS_AUDIT=1` — for local iteration only, never in a PR.)

### Phase 7: Group, Commit, PR

Apply the splitting strategy (`${CLAUDE_SKILL_DIR}/references/pr-strategy.md`):
one library per PR (PR1), every manifest sharing that package moves in the
same PR, a brand-new library rides with its first consumer (C2). PR bodies
cite the changelog excerpt, the
`https://github.com/<owner>/<repo>/compare/v<old>...v<new>` link,
verification result, and the deps-audit risk band. Stage `manifest.json` +
regenerated requirements together.

## Integration

```text
/ha:deps-update (mutating) → /ha:deps-audit (security, Mode B)
        │                            │ BLOCK → /ha:deps-vet (ledger)
        └→ /ha:verify (gate) → one-bump-per-PR commits / PRs (PR1)
```

## References

- `${CLAUDE_SKILL_DIR}/references/update-mechanics.md` — pip outdated + PyPI JSON, exact-pin edits, gen_requirements_all, the requirements diff
- `${CLAUDE_SKILL_DIR}/references/changelog-sources.md` — GitHub releases, PyPI JSON, fallbacks
- `${CLAUDE_SKILL_DIR}/references/coupled-groups.md` — one-version-per-package rule + edge cases
- `${CLAUDE_SKILL_DIR}/references/pr-strategy.md` — PR1 splitting, area buckets, PR template, scratch layout
