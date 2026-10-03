---
name: bootstrap
tags: [setup, scaffolding, agents-md, context-drift]
description: Interactive agent-flow setup for a repository. Scans the repo read-only, proposes AGENTS.md (root + per module), DOCS_INDEX.md and CONTEXT_MANIFEST.json with a confidence marker on every claim, calibrates protected paths and risk boundaries with the user, and writes each file only after the human approves it. Use when setting up agent-flow, when context files are missing, or when migrating from Root_AGENT.md. Also use whenever the user wants an AGENTS.md (or CLAUDE.md/GEMINI.md) written for a repo that doesn't have one, says their coding agents keep getting confused about the codebase, asks to "onboard" or "document" a repo for AI agents, or wants to set protected paths / risk boundaries — even if they don't say "agent-flow" or "bootstrap" by name.
compatibility: Requires git and Node 20+; runs through `npx @drix10/agent-flow`, so no package.json or node_modules is needed (any language). Pi gets the bootstrap_scan/bootstrap_write tools; other harnesses use `npx @drix10/agent-flow scan`/`template`/`schema` plus normal file edits with the user's approval.
---

# Bootstrap

You propose. The human decides. Every claim you write carries a confidence marker, and every risk boundary is a question to the human, never an assumption.

Why this matters: a context file with confident wrong claims makes agents *worse* than having no context at all (FM-01). Fewer true claims beat many plausible ones.

## Phase 1: Reconnaissance (read-only)

1. Call `bootstrap_scan` (outside Pi: `npx @drix10/agent-flow scan --json`). Every field it returns was read from a file, so those are `[HIGH CONFIDENCE]`. That covers: languages, package managers, test frameworks, commands (from `package.json` scripts, the `Makefile`, CI workflow `run:` steps and `build.sh`/`test.sh` scripts), CI files, existing context files, docs, default branch, and recent commits. A command shown as `…/<name>.py (12 files: …)` stands for that many sibling commands in CI.
2. **Secrets gate.** If `secretSuspects` is not empty, stop and show the paths and kinds (never the values). Context files are sent to model providers.
   - A tracked `.env` or key file must be removed from git and **rotated** before bootstrap continues. No exceptions.
   - Anything else (a hardcoded password in a compose file, a sample key): ask the human, and act on the answer. *Fakes or local-only values* → add the path to `secret_scan.ignore_paths`. *Real, or unsure* → stop until it's moved out and rotated. *Continue but keep it flagged* → leave it out of `ignore_paths`; the pre-commit hook keeps warning on it, and say so in Local traps.
3. **Existing context.** If `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules` or `.github/copilot-instructions.md` exist, read them first. They are the user's own rules. You merge into them; you never replace them. If you find `Root_AGENT.md` or `Per-app_AGENT.md` (agent-flow ≤1.0.x), offer to move them to `AGENTS.md`. No harness loads the old names automatically.
   Their rules bind you during bootstrap too. A repo that says "no code change without a plan entry" or "one theme per commit" means bootstrap touches context files and agent-flow wiring only; anything else you'd change (a build script, CI) becomes a recommendation for the human, not an edit.
4. Read the entry points and 2–3 representative modules so you can describe them from the code itself. Anything you describe without reading gets `[INFERRED]`.

## Phase 2: Proposal (interactive, nothing written)

Why `AGENTS.md`: Pi, Codex, Cursor, Copilot, Windsurf and most agents load `AGENTS.md` automatically — it's a [shared, Linux-Foundation-stewarded convention](https://agents.md), not something specific to this project. Claude Code loads `CLAUDE.md`, which can import it with one line (`@AGENTS.md`). Gemini CLI loads it when `context.fileName` includes `AGENTS.md`. One source of truth, every harness.

Templates ship with agent-flow; print them instead of searching the disk: `npx @drix10/agent-flow template` lists them, `npx @drix10/agent-flow template AGENTS.md` prints one.

Show the root `AGENTS.md` (template: `AGENTS.md`) as a proposal, one section at a time:

```
Repository map
  src/api/      HTTP handlers (Express)          [HIGH CONFIDENCE — read src/api/index.ts]
  src/billing/  Stripe integration               [HIGH CONFIDENCE — read src/billing/charge.ts]
  scripts/      deploy helpers                   [INFERRED — names only]

Commands
  npm test          [HIGH CONFIDENCE — package.json#scripts.test]
  npm run typecheck [HIGH CONFIDENCE — package.json#scripts.typecheck]
```

Rules for the proposal:
- **Keep it short.** Aim for under 150 lines at the root. Agents pay for every line on every task.
- **No directory-tree dumps.** They go stale on the first rename. Describe what each module is *for*.
- **Paths go in `backticks`.** `/doctor` checks every backticked path against the filesystem, so a wrong path gets caught. For a path you mention on purpose even though it no longer exists (history, a warning), add `<!-- agent-flow:ignore-refs -->` on that line.
- **Only real commands.** Only commands that exist in `package.json`, the `Makefile`, or CI.

Ask: *"What here is wrong or missing? What do new people always get wrong in this repo?"* Their answer to the second question gives you the **Local traps**, the most valuable part of the file.

For monorepos: propose `<package>/AGENTS.md` for each package that has its own rules (template: `module-AGENTS.md`). Skip packages that have nothing specific to say.

## Phase 3: Risk calibration (interactive)

Ask these one at a time. Never pre-fill the answers.

1. **Protected paths.** "Which paths must agents never modify?" These are usually migrations, lockfiles, CI, security modules, and vendored code. They go into `protected_paths`, and the guard and pre-commit hook enforce them (directories included: `rm`, `mv` and whole-tree git rewrites that reach them are refused). Also ask which files an agent must never read (credentials, key material beyond `.env*`, which is always denied): those go into `deny_read`. Never invent either list; the human owns it.
2. **Critical paths.** "Where are money, auth, contracts or PII?" These become `risk_boundaries` with `risk_level: critical`. Changes there get high-reasoning review, a draft PR, and human approval.
3. **Low-risk paths.** "What is safe for mechanical edits?" (docs, tests, generated code). These become `risk_level: low`.
4. **Auto-merge.** "Should low-risk changes that pass QA auto-merge?" Recommend **no** until the pipeline has shipped about 10 clean PRs in this repo. This sets `pipeline.auto_merge_low_risk`.
5. **Gates.** "Which commands prove a change works?" Offer the scan's commands (CI is the best source: it's what already guards `main`). These become `gates`, which the pipeline runs itself and judges by exit code. For each, settle:
   - **Where it can run.** A gate that needs a Linux toolchain or a POSIX filesystem (chmod tests, `fsync`, `/proc`) gets `"os": ["linux"]`; on other machines it's reported as skipped, never as a pass, and CI judges it. On Windows, string gates run in Git Bash.
   - **How long it takes.** Set `timeout_seconds` above the slowest honest run (default 600).
   - **Fast ones for the stop gate.** Lint, typecheck and unit tests can be `on_stop: true`; full builds can't.
   Prefer one gate per CI job over one per file. A loop in a string command is fine: `for t in a b; do python3 tests/$t.py || exit 1; done`.
6. **Models (only if there are critical areas).** "Should critical changes be reviewed by a stronger model than routine ones?" This sets `pipeline.models.high_reasoning` (and `pipeline.models.fast` for everything else), spelled the way their harness does (`opus` and `sonnet` on Claude Code). Left unset, a critical review runs on the same model as any other, and `status` and `run` say so. If they don't know, leave it unset; don't guess a model name.

Patterns match with globs from the repo root: `*` stays inside one directory level only when it has a `/` before it (`src/*.ts`); `*.md` and `**/*.md` match at any depth, and `docs/` covers everything under it. When a diff matches several boundaries, the highest level wins, so a `low` test folder inside a `critical` tree stays critical. A context file that sits in a critical tree (`kernel/AGENTS.md` under `kernel/**`) makes its edits critical too: say so, and let the human choose.

Show the resulting `risk_boundaries`, `protected_paths` and `gates` back to the human and get a yes.

## Phase 4: Write (one confirmation per file)

Call `bootstrap_write` once per file. It shows the human a confirmation dialog, refuses paths outside the repo, refuses an invalid manifest, and refuses secret-shaped content. It will not overwrite an existing file unless you pass `overwrite: true`, and it asks again when you do. On an overwrite it keeps the file's line endings, BOM and (for the manifest) indentation, saves the old file under `.agent-flow/backups/`, tells the human how many existing lines the new content removes, and refuses a manifest that drops any `protected_paths` / `risk_boundaries` entry or top-level key the current one has. Read the current file and carry everything over.

1. `AGENTS.md`, plus one `AGENTS.md` per module.
2. `CLAUDE.md` containing `@AGENTS.md`, if the user uses Claude Code (template: `CLAUDE.md`). If a `CLAUDE.md` already exists, propose adding the import line to it.
3. `DOCS_INDEX.md` (template: `DOCS_INDEX.md`).
4. `CONTEXT_MANIFEST.json`. You write the keys the human decided: `protected_paths`, `deny_read`, `secret_scan`, `risk_boundaries`, `gates`, `pipeline`, plus `version: "2"`, `repo` and `default_branch` from the scan (`npx @drix10/agent-flow schema manifest` is the contract). Don't build `context_files` by hand: write the context files first, then run `npx @drix10/agent-flow manifest sync` to preview and `… manifest sync --yes` to fill `context_files` from them. It records every path the prose names (and warns about named paths that don't exist), counts the confidence markers, and never touches the keys above. With no manifest yet, `npx @drix10/agent-flow init --yes` writes a starter you then edit. Don't leave any `{{PLACEHOLDER}}` in any file. `/doctor` fails on them.

Outside Pi, show each file's full content and write it only after the human says yes.

## Phase 5: Harness wiring

Suggest these; the human runs them:

- Pi: nothing more. The guard and tools are active once the package is installed.
- Claude Code / Codex / Gemini / Cursor / Copilot / Windsurf: `npx @drix10/agent-flow install --harness <name>`. It copies the skills and the reviewer subagent and never overwrites your edits. In a repo without `node_modules/@drix10/agent-flow` (Python, Go, C++…) it also copies a ~0.5 MB runtime to `.agent-flow-runtime/` for the guard hook; that folder gets committed so the hook works for everyone who clones. No `package.json` is added. `.agent-flow/` (audit log, gate logs) stays local through `.git/info/exclude`.
- Everyone: `npx @drix10/agent-flow hook install` for the pre-commit gate (protected paths, secrets, broken context references).
- `protected_paths` bind local agents through the guard and the pre-commit hook. A pull request pushed from elsewhere is only stopped by the host, so offer `npx @drix10/agent-flow codeowners --yes`: it appends a `CODEOWNERS` line per protected path, owner taken from `origin` (`--owner @team` to override). The file is harmless on its own; GitHub just asks the owner for review. Do not push the human toward "Require review from Code Owners" unless there's a team: alone, it blocks their own PRs until they allow admin bypass. `doctor` says plainly (one note, not a warning) whether GitHub enforces it when a logged-in `gh` can tell, and stays silent otherwise. Never ask the human for a token for this.
- CI: add `doctor` and `audit-risk --fail-on-new` as steps (see `README.md`). Without Node in the project, call the committed runtime: `node .agent-flow-runtime/bin/agent-flow.js doctor` (CI images have Node; `actions/setup-node` if not).
- First baseline: after the human reviews `npx @drix10/agent-flow audit-risk`, `npx @drix10/agent-flow baseline accept --all --yes`.

## Phase 6: Verify

1. Run `/doctor` (`stale_detect`). It has to be healthy before you say you're done. If it isn't, fix what it reports; don't explain it away.
2. Run `npx @drix10/agent-flow gates run`. A gate that fails here fails every future pipeline round, so sort each failure before you finish:
   - *Exit 2 / "could not run"*: a missing tool or a wrong path. Fix the command.
   - *Needs another platform* (Linux-only build, chmod tests on a Windows filesystem): add `"os"` to that gate, re-run, and confirm it reports as skipped.
   - *A real failure on the default branch*: tell the human. Leave the gate as it is; it is telling the truth.
   Never edit the repo's code or build scripts to make a gate pass during bootstrap.
3. `npx @drix10/agent-flow guard --check` (Claude Code) confirms the hook is wired.

## Edge cases

| Situation | Action |
|---|---|
| Empty repo | Write a minimal `AGENTS.md` with `[NEEDS VERIFICATION]` on everything. No manifest refs yet. |
| No tests | Say so plainly in `AGENTS.md`. The pipeline's QA step will report `no_commands_defined` until tests exist. |
| No CI | Propose the CI steps above. Don't write CI files yourself (bootstrap only writes context files). |
| Huge repo (`truncated: true`) | Bootstrap the top-level modules the user names, not everything. |
| Existing agent-flow ≤1.0 files | Offer the migration in Phase 1.3. |
| The user won't answer the risk questions | Write nothing to `protected_paths` or `risk_boundaries`. The classifier falls back to path heuristics and says so. |
| No `package.json` (Python, Go, C++…) | Normal. Use `npx @drix10/agent-flow …`; `install` vendors the hook's runtime. Never add a `package.json` to make agent-flow work. |
| CI is the only place the full build passes | Gate it with `"os": ["linux"]` (or the CI platform) and say in Local traps where it does run. |
| Context files changed after the manifest was written | `npx @drix10/agent-flow manifest sync --yes`, then `/doctor`. |
