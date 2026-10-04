---
name: frontend-quality-workflow
description: Run and fix the frontend static-quality lane — formatting, ESLint, TypeScript, markdownlint, jscpd duplication, and rust-code-analysis metrics — through the profile's make target map, raise-only and with no suppressions. Use when the user asks to format code, run lint, fix ESLint/TypeScript/markdown failures, resolve duplication, or lower complexity metrics before committing or finishing a change.
---

# Frontend Quality Workflow Skill

## Profile keys consumed

- `make.format`, `make.lint`, `make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`, `make.lint_metrics`, `make.lint_deps`
- `quality.eslint_errors`, `quality.eslint_warnings`, `quality.tsc_errors`, `quality.markdownlint_errors`, `quality.jscpd_clones`, `quality.depcruise_violations`, `quality.metrics_enforced`

## Context (Input)

- Code, doc, or config changes exist in the working directory.
- You need formatting + the static lint lane green before a commit, review, or PR.
- Profile loaded from `.claude/react-sdlc.yml` (run `/fe-sdlc-setup` if missing).

This is the static-quality lane that the full suite's preflight and lint groups route into. When run under `/fe-sdlc-finish-pr`, the `ci-fixer` agent drives this loop to green; invoked directly, follow the same steps yourself. For the whole CI flow (lint **plus** tests, mutation, and prod-side lanes) use [ci-workflow](../ci-workflow/SKILL.md).

## Task (Function)

Drive the static-quality lane to a clean exit: run the **mutating formatter first**, then every read-only lint gate, fixing each failure at the root cause.

**Required order** — the formatter rewrites files, so it must run alone before any verification, never in parallel with a read-only gate:

```bash # profile-example
make format   # mutating preflight: Prettier + qlty fmt
make lint     # read-only aggregate: eslint, tsc, markdownlint, jscpd, rca-metrics, dependency-cruiser
```

The target mapped by `make.format` runs the project's Prettier pass (invoked through the project package manager, `framework.package_manager`) followed by `qlty fmt`. The target mapped by `make.lint` is the aggregate that fans out to the individually mapped sub-targets below.

**Success Criteria**: the target mapped by `make.lint` exits `0` after `make.format` has run. Treat exit status as the contract.

**Degrade rule (capability absent)**: if `make.lint` is `null` in the profile (a library/app that ships no aggregate lint target), run the individually mapped sub-targets instead, in order — `make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`, `make.lint_metrics`, `make.lint_deps` — skipping any `null` entry with an explicit capability-absent note. Common skips across divergent repos:

- `SKIPPED: make.lint_dup` when `make.lint_dup` is `null` (a repo that ships no jscpd duplication gate).
- `SKIPPED: make.lint_metrics` when `make.lint_metrics` is `null` (a repo that ships no rust-code-analysis metrics gate).
- `make.lint_eslint` may resolve to a different target name per repo (e.g. an ESLint target wired under `lint-next`); `make.format` may resolve to a check-only variant (`format-check`); `make.lint_deps` may resolve to a dependency-cruiser target under a different name. Always use the mapped target, never the bare tool name.

**Qlty bootstrap (tooling absent)**: if the `make.format` run fails only because the `qlty` CLI is missing, install it once, put it on `PATH`, and re-run — do not skip the formatter or stage repo Qlty config. Prefer a binary preinstalled by the host image; otherwise download the release artifact for the host platform and verify its published checksum before extracting — never fetch-and-execute a remote install script:

```bash # profile-example
command -v qlty >/dev/null || {
  target="x86_64-unknown-linux-gnu" \
    && release="https://github.com/qltysh/qlty/releases/latest/download" \
    && dir="$(mktemp -d)" \
    && curl -fsSL -o "$dir/qlty-$target.tar.xz" "$release/qlty-$target.tar.xz" \
    && curl -fsSL -o "$dir/qlty-$target.tar.xz.sha256" "$release/qlty-$target.tar.xz.sha256" \
    && (cd "$dir" && sha256sum --check "qlty-$target.tar.xz.sha256") \
    && mkdir -p "$HOME/.qlty/bin" \
    && tar -xJf "$dir/qlty-$target.tar.xz" -C "$HOME/.qlty/bin" \
      --strip-components=1 "qlty-$target/qlty"
  rc=$?
  [ -n "${dir:-}" ] && rm -rf "$dir"
  [ "$rc" -eq 0 ] || exit "$rc"   # fail loudly here, not with a later "qlty: not found"
}
export PATH="$HOME/.qlty/bin:$PATH"
```

Substitute `target` for the host platform (e.g. `aarch64-apple-darwin`, whose `shasum -a 256 -c` replaces `sha256sum --check`). Do not run `qlty init` or stage `.qlty/qlty.toml` unless the task explicitly asks for repository Qlty configuration.

## Individual Checks

Each logical gate maps to one profile target. Run the smallest failing check while fixing, then the aggregate before finishing.

| Gate                | Profile target      | What it enforces                                             |
| ------------------- | ------------------- | ------------------------------------------------------------ |
| Formatter           | `make.format`       | Prettier + `qlty fmt` (mutating preflight, runs first)       |
| ESLint              | `make.lint_eslint`  | Lint rules incl. the no-suppression / convention gates       |
| TypeScript          | `make.lint_tsc`     | `tsc` type-check; zero type errors                           |
| Markdown            | `make.lint_md`      | markdownlint over docs and skill/agent frontmatter           |
| Duplication (jscpd) | `make.lint_dup`     | Copy/paste DRY gate (clone mass over the source root)        |
| Metrics (rca)       | `make.lint_metrics` | rust-code-analysis complexity/size/Halstead hard-fail policy |
| Dependencies        | `make.lint_deps`    | dependency-cruiser layer/import-boundary rules               |

Dependency-cruiser is part of the `make.lint` aggregate but its findings route to [architecture](../architecture/SKILL.md), not this lane.

## Execution Steps

### Step 1: Format

Run the target mapped by `make.format` first (always through `make` — the targets wrap the containerized toolchain and the project-package-manager-managed dependencies; never invoke Prettier, `qlty`, ESLint, `tsc`, markdownlint, jscpd, or rust-code-analysis directly on the host). Inspect the files it rewrote.

### Step 2: Lint

Run the target mapped by `make.lint` (or, under the degrade rule, each non-`null` sub-target in order).

- **Success** (exit `0`): lane clean → done.
- **Failure**: identify the failing gate from the grouped output → Step 3.

### Step 3: Fix at the Root Cause

Re-run only the smallest failing check while iterating, and fix the code — never the bar:

| Failing gate        | Re-run via          | Fix                                                                                         | Companion Skill                                            |
| ------------------- | ------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Formatting drift    | `make.format`       | Let the formatter rewrite; commit the formatted result                                      | -                                                          |
| ESLint              | `make.lint_eslint`  | Fix the reported rule at source (no `eslint-disable`)                                       | [code-organization](../code-organization/SKILL.md)         |
| TypeScript          | `make.lint_tsc`     | Make the type contract honest; avoid `any` (no `@ts-ignore`)                                | -                                                          |
| Markdown            | `make.lint_md`      | Fix headings, fences, list/line structure; keep skill frontmatter to `name` + `description` | -                                                          |
| Duplication (jscpd) | `make.lint_dup`     | Deduplicate — extract a shared style fragment, constant, or factory                         | [complexity-management](../complexity-management/SKILL.md) |
| Metrics (rca)       | `make.lint_metrics` | Split dense functions/files; extract helpers; replace branch chains with lookup maps        | [complexity-management](../complexity-management/SKILL.md) |
| Dependencies        | `make.lint_deps`    | Fix the layer/import-boundary violation                                                     | [architecture](../architecture/SKILL.md)                   |

**Refactoring during fixes**: if a failure reveals a structural issue (wrong directory, vague name, a component or hook in the wrong module, hardcoded config), consult [code-organization](../code-organization/SKILL.md) before patching.

### Step 4: Re-run

Re-run the failing check, then the aggregate `make.lint`. Repeat Steps 2-4 until it exits `0`. Run `make.format` again only if a fix touched formatting.

## Fix Rules

- Prefer code changes over disabling rules — fix the root cause, never silence it.
- Keep TypeScript types honest; avoid `any` unless an external boundary genuinely requires it.
- Keep markdown skill/agent frontmatter to `name` and `description` only.
- Split complex components, hooks, and helpers instead of lowering the metrics policy.
- Re-run the failing check after each focused fix; do not batch unrelated fixes blind.

## Line Length Disclosure

Before presenting changes, check changed text files for lines longer than 100 characters. If any exist, tell the user each `path:line` and the measured character count. Treat this as disclosure, not failure, unless a project gate (markdownlint, ESLint `max-len`, or the rca size policy) actually fails on it.

## Constraints (Parameters)

**Thresholds come from `quality.*` in the profile — NEVER decrease them.** This lane's gates are fixed-`0` ceilings plus the boolean metrics switch; a profile may never raise a ceiling above `0` nor flip the metrics gate off (raise-only rule). The authoritative policy for the metrics gate is `config/metrics-policy.json`.

| Profile key                                         | Shipped default | Direction               |
| --------------------------------------------------- | --------------- | ----------------------- |
| `quality.eslint_errors` / `quality.eslint_warnings` | 0               | ceiling (fixed)         |
| `quality.tsc_errors`                                | 0               | ceiling (fixed)         |
| `quality.markdownlint_errors`                       | 0               | ceiling (fixed)         |
| `quality.jscpd_clones`                              | 0               | ceiling (fixed)         |
| `quality.depcruise_violations`                      | 0               | ceiling (fixed)         |
| `quality.metrics_enforced`                          | true            | bool (must stay `true`) |

**DO NOT**:

- Lower a `quality.*` ceiling or relax `eslint.config.mjs`, `.jscpd.json`, `config/metrics-policy.json`, or the dependency-cruiser config to make violations disappear.
- Skip a failing gate or commit while a mapped lint target fails.
- Run the underlying tools outside the mapped `make` targets (they wrap the containerized toolchain and the project-package-manager-managed dependencies).
- Add any suppression/ignore directive — `eslint-disable`, `// @ts-ignore`, `// @ts-nocheck`, `prettier-ignore`, `markdownlint-disable`, `editorconfig-checker-disable`, or a jscpd/dependency-cruiser ignore comment — to silence a failure. Fix the code or the type contract instead.

If a rule genuinely cannot apply because of an external constraint, raise it with the user before silencing anything; never silence to land a change.

## Format (Output)

**Required final state**: `make.format` has run, and the target mapped by `make.lint` (or, under the degrade rule, every non-`null` mapped sub-target, skipping capability-absent gates with a note) exits `0`.

## Verification Checklist

- [ ] `make.format` ran first (mutating preflight) and its rewrites were inspected.
- [ ] `make.lint` aggregate (or every non-`null` sub-target) passed: ESLint, TypeScript, markdown, jscpd, rust-code-analysis metrics, dependency-cruiser.
- [ ] Exit status `0`; zero ESLint errors/warnings, zero `tsc` errors, zero markdown errors, zero jscpd clones, zero dependency-cruiser violations.
- [ ] No `quality.*` ceiling decreased and `quality.metrics_enforced` still `true`.
- [ ] No suppression/ignore directive added anywhere.
- [ ] Any line over 100 characters in a changed file disclosed as `path:line` + count.

## Rollback

If the aggregate's parallel grouping causes issues (interleaved failures, resource contention):

1. Run the mutating preflight on its own first (`make.format`), then re-run the read-only `make.lint` aggregate.
2. Otherwise run the mapped sub-targets individually in the degrade order: `make.lint_eslint`, `make.lint_tsc`, `make.lint_md`, `make.lint_dup`, `make.lint_metrics`, `make.lint_deps` — skipping capability-absent gates with a note — to isolate the failing one.

## Related Skills

- [ci-workflow](../ci-workflow/SKILL.md) - Run the full suite (this lane plus tests, mutation, and prod-side lanes)
- [complexity-management](../complexity-management/SKILL.md) - Reduce complexity and resolve duplication when jscpd or rust-code-analysis fails
- [code-organization](../code-organization/SKILL.md) - Fix structural/naming issues, misplaced components/hooks, or hardcoded config a failure reveals
- [architecture](../architecture/SKILL.md) - Resolve dependency-cruiser layer/import-boundary violations
- [quality-standards](../quality-standards/SKILL.md) - Overview of all protected thresholds
