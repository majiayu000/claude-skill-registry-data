---
name: dep-vuln-update
description: Use when dependencies in a repo have known vulnerabilities and need updating, including when the dep-vuln hook reports advisories at commit or merge request time, when the user asks to fix vulns, patch CVEs or GHSAs, run an audit fix, or bump vulnerable packages. Covers scanning tracked lockfiles with osv-scanner, choosing the smallest version that clears each advisory, overrides for transitive deps, verifying with the repo's own tests, and committing per repo.
---

# Dependency vulnerability update

Clear known advisories with the smallest change that removes them, prove the repo still builds and passes, and leave a commit the user can read.

## How it is triggered

Directly, when the user asks to fix vulnerable dependencies, or through the opt-in commit gate. `./install.sh --with-dep-vuln-gate` copies `scripts/scan.py` to `~/.claude/hooks/dep-vuln-scan.py` and wires it as a `PreToolUse` hook on Bash that runs whenever a command contains `git commit`, `gh pr create`, `glab mr create`, or `merge_request.create`. It scans only lockfiles tracked by git in that repo, so `.claude/worktrees`, `node_modules` and other clones are skipped. Results are cached per lockfile content per UTC day, and the hook reports a given lockfile state at most once per session per gate (commit, merge request). It never blocks the command.

Requires [osv-scanner](https://google.github.io/osv-scanner/installation/) on PATH. The scan sends package names and versions to the OSV.dev API.

When the hook output lands in context: finish the commit or MR the user asked for, then tell them in one line how many advisories and how many are fixable, and ask whether to fix now. Do not start without a yes.

## Workflow

1. **Scan.** `python3 -I <this skill's directory>/scripts/scan.py --repo <root> --no-cache` gives one line per package with the version that clears all its advisories. `--detail` lists each advisory, `--json` gives the raw findings. Exit 1 means something fixable remains.
2. **Isolate.** In a shared main checkout, ask before editing whether to work in a fresh worktree. Use a branch named `deps/vuln-YYYY-MM-DD`.
3. **Triage.** Fix in this order: CRITICAL and HIGH with a fix, then the rest with a fix. Skip `no fix yet`. Anything marked `MAJOR BUMP` goes on a list for the user and is not applied without their call. Dev-only tooling (docs sites, test runners) still gets fixed when the bump is minor, since it is cheap.
4. **Fix, smallest first.**
   - Direct dependency: raise it to the `clears at` version, or the lowest version in the same major that satisfies it. Keep the existing range style (`^`, `~`, pinned).
   - Transitive dependency: first try updating the parent within its range (`pnpm update <parent>`, `npm update <parent>`, `uv lock --upgrade-package <pkg>`, `cargo update -p <pkg>`). If the parent's range blocks it, add an override scoped to the vulnerable package.
   - Never run a blanket `update --latest` or regenerate the whole lockfile.
5. **Verify.** Run the repo's own install, typecheck, lint, test and build commands (read `package.json` scripts, `Makefile`, `pyproject.toml`, CI config to find them). Then rerun the scan with `--no-cache` and confirm the targeted advisories are gone. A fix that does not clear the advisory, or breaks a test, is reverted and reported, not committed.
6. **Commit.** One commit per repo. Subject `deps: clear N advisories (pkg@from -> to, ...)`, body lists each GHSA/CVE id cleared. Push and open an MR only when the user says so.
7. **Report.** Short table: cleared, reverted (with the failing command), major bumps waiting on the user, no fix available.

## Per-ecosystem commands

| Ecosystem | Bump a direct dep | Refresh a transitive dep | Override |
|---|---|---|---|
| pnpm | `pnpm add <pkg>@<ver>` (`-D` if dev, `--filter` in workspaces) | `pnpm update <pkg> --depth Infinity` | `pnpm.overrides` in root `package.json` (or `overrides` in `pnpm-workspace.yaml` on pnpm 10+) |
| npm | `npm install <pkg>@<ver>` | `npm update <pkg>` | `overrides` in `package.json` |
| yarn | `yarn add <pkg>@<ver>` | `yarn up -R <pkg>` (berry) | `resolutions` in `package.json` |
| uv | edit `pyproject.toml`, `uv lock` | `uv lock --upgrade-package <pkg>` | `[tool.uv] constraint-dependencies` |
| poetry | `poetry add <pkg>@^<ver>` | `poetry update <pkg>` | pin it as a direct dependency |
| requirements.txt | edit the pin | regenerate with the repo's own tool (pip-compile, uv pip compile) if one is used | add an explicit pin |
| cargo | edit `Cargo.toml` | `cargo update -p <pkg> --precise <ver>` | `[patch]` only as a last resort |
| bundler | `bundle update <gem> --conservative` | same | pin in `Gemfile` |

For npm lockfiles, `osv-scanner fix --strategy=in-place -L package-lock.json` can compute a minimal in-place upgrade; review its diff like any other change.

## Waiving an advisory

When the user decides an advisory does not apply, add its id to `~/.claude/state/dep-vuln-ignore.json`:

```json
{"ids": ["GHSA-xxxx-xxxx-xxxx"], "repos": {"/abs/path/to/repo": ["GHSA-yyyy-yyyy-yyyy"]}}
```

`ids` applies everywhere, `repos` to one repo root. A repo's own `osv-scanner.toml` is also honored by osv-scanner. Only waive on the user's word.
