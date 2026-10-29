---
name: release-bump
description: |
  Move the Unity Catalog or Delta Lake docs to a new upstream release: rewrite
  every pin with `just bump-uc` / `just bump-delta`, triage the scripts CI runs
  against it, then review the claims the release can change (support state,
  known issues, "the server has no X") and open one PR with a claims table.
  Use when the user wants to bump, upgrade, or move the docs to a new Unity
  Catalog or Delta release, update the release pins, or check the docs against
  a new release.
argument-hint: '<unitycatalog|delta> <X.Y.Z>'
---

# Bump a release and review its claims

A bump has two halves. The pin rewrite is mechanical. The release review
re-reads the sentences that describe what the release does and doesn't do.
[`docs/design/docs-versioning.md`](../../../docs/design/docs-versioning.md) is
the source of truth for both: its *Tooling* section for the pin rules, and
*Release review* for the procedure, the evergreen rules, and the
release-sensitive pages. Read it first. This skill sequences it and doesn't
restate it.

Aim for fewer release-dependent sentences, not just correct ones. When a claim
has to change, check whether it belongs only in R01 and the page can drop it.

## 1. Bump

On a branch (`chore/bump-<project>-X.Y.Z`), not `main`:

```bash
just bump-uc X.Y.Z        # or: just bump-delta X.Y.Z
uv run docsnip check
```

`just bump-uc` also re-renders the generated environments (`envs/<name>/env.toml`,
`uc-aws` today) with the pinned Trestle, because their recipe and image
`Dockerfile` carry the release: commit the re-render with the bump. The
Trestle workflow fails a PR whose render differs from a fresh one.

For Unity Catalog, the companion pins in `content/unitycatalog/release.yml`
(client, Spark connector, delta-spark, PySpark, Iceberg) follow the release
upstream, and the bump doesn't move them all. Look up each one at the new tag
(`build.sbt`, the client's release), edit the manifest, then run
`uv run docsnip versions --fix`. For Delta, `deltalake` and `duckdb` move the
same way.

## 2. Run the scripts

Run the lanes the release touches: `just test`, plus `just test-services`,
`test-spark`, `test-jvm`, or `test-rust` for the pins that moved. Internal package
proxies lag new releases by about a week, so a fresh pin may only resolve in CI.
Say so, push, and treat CI as the first real run.

A failing script is a behavior that changed. Fix the script and the page
prose together. An assert that pinned a known issue and now fails means the
issue is fixed: that's a step 4 change, not a bug.

## 3. Find what changed upstream

Compare the old tag with the new one before reading any page, so the review
checks against evidence instead of memory:

- Unity Catalog: `git diff vOLD vNEW -- api/` in an upstream checkout (or the
  GitHub compare view), plus the release notes. List new endpoints, securable
  types, `TableType` values, privileges, and removed or deprecated surface.
- Delta: the release notes, new table features, and engine-side changes for
  the pinned `deltalake` and DuckDB `delta` extension.

Keep it as a short "what's new" list. It goes in the PR description.

## 4. Review the claims

Follow *After a bump* in the design doc, steps 3–5. Start from what the pin
reaches: `uv run docsnip query impact pin:<project>/release` (or
`pin:<project>/<key>` for a companion pin) lists the environments, scripts,
claims, and pages. Work through those and the release-sensitive pages table,
then grep the rest of `content/<project>/` for
absence wording and check each hit against the step 3 list.

Record each claim you checked:

| Page | Claim | Verdict | Evidence |
| --- | --- | --- | --- |
| E03 | The server has no groups | holds | no group endpoints in `api/all.yaml` at `blob/vNEW` |

Verdicts are `holds`, `changed`, or `unsure`. Mark a claim `unsure` when the
evidence doesn't settle it. Leave it for a reviewer, and don't guess.

## 5. Fix

- Edit claims that changed. Where a page restated an absence that R01 already
  lists and the page's task doesn't need it, cut the restatement. R01 is
  private, so never link it.
- Update R01's known issues as the design doc describes (*Fixed in* note,
  **Affects** column).
- `uv run docsnip compat --fix` if a script's claims changed.
- A page that gains a new release-sensitive claim joins the design doc's
  table in the same commit.

Don't change `status:`. A `ready` page whose claims changed needs a new review
approval, so list it in the PR description.

## 6. Commit and open the PR

Commit in logical pieces. The pin bump and its generated output go in
`chore(<project>): bump to X.Y.Z`. Each claim fix is a
`docs(<project>): …`. Then:

```bash
uv run docsnip check && uv run ruff check . && uv run ruff format --check . && uv run ty check
```

The PR description carries the "what's new" list, the claims table, any
`unsure` rows called out for reviewers, and the `ready` pages that need
re-approval.
