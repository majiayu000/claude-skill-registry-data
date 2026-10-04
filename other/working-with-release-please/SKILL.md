---
name: working-with-release-please
description: "Use when working with release-please (Google's release automation, a.k.a. Release Please) — the tool that reads Conventional Commits on your default branch, opens/maintains a \"release PR\" that bumps the version and updates CHANGELOG.md, and on merge tags the release + creates the GitHub Release. Covers config (release-please-config.json + .release-please-manifest.json), manifest/monorepo mode with per-path components, the full set of release-type strategies (node, python, simple, go, rust, ruby, php, java, terraform-module, …), the release-please-action@v5 GitHub Actions wiring (permissions, outputs release_created/releases_created, gating downstream publish jobs), and cookbooks for shipping an npm package, a pip/PyPI package, and a VS Code extension. Bundles the upstream README, docs/, and JSON schemas fetched at a pinned tag, plus hand-written integration/automation/troubleshooting guides. Invoke for any release-please config field, version-bump/changelog/release question, \"set up automated releases\", \"why didn't a release PR appear\", or monorepo release setup. For raw gh/REST release commands use working-with-github; for general CI/workflow YAML use working-with-github-actions; for Conventional Commits authoring tooling (commitizen) see joe-stack-preferences."
metadata:
  last_updated: "2026-06-16"
---

# working-with-release-please

[release-please](https://github.com/googleapis/release-please) automates releases from [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). It does **not** run on a timer or on every push the way semantic-release does — instead it keeps a **release PR** open and up to date: every commit to your default branch is parsed, the pending version + changelog are recalculated, and the PR is amended. When you merge that PR, release-please tags the commit and creates the GitHub Release. That's the whole model.

## Two things that trip everyone up — read these first

1. **The action is `@v5`.** Almost every tutorial and many Google docs still show `googleapis/release-please-action@v4` (or `@v3`). v5.0.0 is current. Pin `@v4` only if you have a specific reason.
2. **release-please does versioning + CHANGELOG + GitHub release/tag — and nothing else.** It does **not** run `npm publish`, `twine upload`, or `vsce publish`. Publishing is always a **separate, follow-on CI job** gated on the action's output (`release_created` for a root component, `releases_created` for manifest mode). Every cookbook below follows this two-job shape.

## When to use

- Setting release-please up in a new or existing repo (single package or monorepo).
- Writing/debugging `release-please-config.json` or `.release-please-manifest.json`.
- Wiring `release-please-action` into GitHub Actions and gating a publish job.
- "Why didn't a release PR appear?" / "Why is the first PR my entire git history?" / "Why didn't my publish workflow trigger?"
- Shipping an npm package, a PyPI package, or a VS Code extension on merge.

## Quick reference — route to the right file

| You want to… | Read |
| --- | --- |
| **Set up release-please** (new repo *and* existing repo bootstrap) | [`references/guides/integration.md`](references/guides/integration.md) |
| Understand **changelogs + GitHub releases** (commit→bump→CHANGELOG→tag lifecycle) | [`references/guides/changelogs-and-github.md`](references/guides/changelogs-and-github.md) |
| **Set up GitHub Actions** automation (action@v5, permissions, outputs, gating) | [`references/guides/github-actions.md`](references/guides/github-actions.md) |
| Monorepo, linked-versions, plugins, separate-PRs, prereleases | [`references/guides/advanced.md`](references/guides/advanced.md) |
| Debug a stuck/missing release PR or publish | [`references/guides/troubleshooting.md`](references/guides/troubleshooting.md) |
| **Cookbook: npm package** | [`references/guides/cookbook/npm-package.md`](references/guides/cookbook/npm-package.md) |
| **Cookbook: pip / PyPI package** | [`references/guides/cookbook/pip-package.md`](references/guides/cookbook/pip-package.md) |
| **Cookbook: VS Code extension** | [`references/guides/cookbook/vscode-extension.md`](references/guides/cookbook/vscode-extension.md) |
| Every config field (authoritative JSON Schema) | [`references/schemas/config.json`](references/schemas/config.json) · [`references/schemas/manifest.json`](references/schemas/manifest.json) |
| Upstream config/customization docs | [`references/docs/customizing.md`](references/docs/customizing.md) |
| Manifest (monorepo) mode upstream docs | [`references/docs/manifest-releaser.md`](references/docs/manifest-releaser.md) |
| CLI usage (running release-please locally) | [`references/docs/cli.md`](references/docs/cli.md) |
| How it decides versions (design) | [`references/docs/design.md`](references/docs/design.md) |
| Upstream troubleshooting | [`references/docs/troubleshooting.md`](references/docs/troubleshooting.md) |
| Java specifics | [`references/docs/java.md`](references/docs/java.md) · [`references/docs/java-releases.md`](references/docs/java-releases.md) |
| Core README / Action README | [`references/release-please-README.md`](references/release-please-README.md) · [`references/release-please-action-README.md`](references/release-please-action-README.md) |

## Supported `release-type` strategies

`dart`, `elixir`, `expo`, `go`, `helm`, `java`, `krm-blueprint`, `maven`, `node`, `ocaml`, `php`, `python`, `ruby`, `rust`, `sfdx`, `simple`, `terraform-module`.

Pick the one matching your ecosystem so release-please knows which version files to bump and how to format the changelog. `simple` just maintains a `version.txt` + CHANGELOG (handy for anything not in the list). VS Code extensions use `node` (the manifest is `package.json`).

## Reference freshness

`references/docs/`, `references/schemas/`, and the two READMEs are fetched **verbatim at a pinned git tag** by [`scripts/update_docs.js`](scripts/update_docs.js) (run via `make update-working-with-release-please`). The pin lives in [`PINNED_VERSION`](PINNED_VERSION) (release-please 17.9.0, action 5.0.0). To refresh to a newer release, bump `PINNED_VERSION` and re-run. `references/guides/**` is hand-written and never overwritten.
