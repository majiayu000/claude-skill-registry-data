---
name: dependabot-sweep
description: Use when the user wants to fix, address, clear, or resolve open Dependabot security/vulnerability alerts for a repository, end to end. Fetches open alerts via the gh CLI, fixes them per ecosystem (pnpm/npm overrides + lockfile regen, cargo update, pip/go/bundler), verifies with audit and frozen-lockfile installs, then branches → commits → pushes → opens a PR, and squash-merges once CI is green — escalating only when a fix carries breaking-change risk or can't be resolved. Trigger on "/dependabot-sweep", "address the dependabot alerts", "fix the security vulnerabilities", "clear the dependabot alerts", "handle the dependency vulnerabilities", "sweep dependabot".
when_to_use: "Use when the user wants open Dependabot alerts fixed end-to-end. Triggers on: '/dependabot-sweep', 'fix the dependabot alerts', 'address security vulnerabilities', 'clear dependency alerts', 'sweep dependabot'."
effort: high
---

# Dependabot Sweep

Resolve open Dependabot alerts end to end: **fetch → triage → fix per ecosystem → verify → branch → commit → push → PR → merge.** Built to run with minimal intervention.

**Announce at start:** "I'm using the dependabot-sweep skill to clear open Dependabot alerts."

**This is a workflow skill.** It invokes the `gh` CLI, the repo's package managers (`pnpm` / `npm` / `cargo` / `pip` / `go` / `bundler`), `git`, and may hand the final merge to the `merge-pr` skill.

---

## Autonomy contract

Running this skill **is** the user's consent for the whole workflow — fetch through merge — with no confirmation prompts. Do not ask "should I push / open a PR / merge?". Proceed.

**Stop and surface a concise summary only when an Escalate condition is hit:**

- A required fix is a **SemVer-major bump of a direct dependency** (real breaking-change risk).
- Lockfile regeneration would pull **major bumps of packages unrelated to the alert** (churn well beyond the targeted package and its subtree). A large *minor/patch* refresh of a stale lockfile is fine — note it, don't stop.
- **No patched version exists**, or the only remaining vulnerable copy is an **upstream-pinned / build-only transitive** with no reachable fix → document it and recommend dismissing that specific alert; fix everything else and continue.
- The ecosystem **audit still reports the vulnerability** after the fix.
- **CI fails** and the documented quick-fixes don't resolve it after one attempt.
- A **merge conflict** with the base branch that isn't a trivial lockfile re-resolution.
- A manifest uses an **ecosystem with no playbook** here.

When you escalate, do the fixable work first, then present only the decision the user actually needs to make.

---

## Step 1 — Fetch open alerts

Resolve the repo, then list every open alert grouped by manifest:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh api "repos/$REPO/dependabot/alerts" --paginate \
  -q '.[] | select(.state=="open")
      | [.number, .security_advisory.severity, .dependency.package.ecosystem,
         .dependency.package.name, .dependency.manifest_path, .dependency.scope,
         .security_vulnerability.vulnerable_version_range,
         .security_vulnerability.first_patched_version.identifier] | @tsv' \
  | sort -t$'\t' -k5 | column -t -s$'\t'
```

If there are **zero** open alerts, report that and stop. Otherwise build a per-manifest work list. The `first_patched_version` is your target; the `vulnerable_version_range` tells you whether a copy still in the tree is affected.

## Step 2 — Branch

Work off a fresh branch from the default branch — **never on main**:

```bash
git checkout -b fix/dependabot-security-alerts   # reuse if it already exists
```

## Step 3 — Fix per ecosystem

For each manifest, prefer the **smallest change that lands a patched version**:

- **Direct dependency** (named in the manifest): raise its version range to `>= patched`.
- **Transitive dependency** (scope/dep not in the manifest): use the ecosystem's override/pin mechanism.
- Then **regenerate the lockfile** (lockfile-only — no need to write `node_modules`/build).

See the **Ecosystem playbooks** below.

## Step 4 — Verify

- Run the ecosystem **audit** at moderate+ and confirm "No known vulnerabilities found".
- Run a **frozen-lockfile install** to prove the lockfile is internally consistent (this is what CI runs).
- If a build/test is cheap, run it; otherwise rely on CI.

## Step 5 — Commit

Conventional commit, specific `git add` (no `-A`):

```
fix(deps): resolve Dependabot security alerts
```

Body: per-manifest list of what changed with the alert numbers, plus any alert **deliberately left unfixed and why**. End with:

```
Co-Authored-By: Claude <current model name> <noreply@anthropic.com>
```

Use the name of whichever model is actually running this session (e.g. "Claude Fable 5") — never hardcode a specific model name here, since it will go stale as new models ship.

## Step 6 — Push + open PR

```bash
git push -u origin fix/dependabot-security-alerts
gh pr create --title "fix(deps): resolve Dependabot security alerts" --body "<template below>"
```

## Step 7 — Merge (autonomous)

```bash
PR=$(gh pr view --json number -q .number)
gh pr checks "$PR" --watch
```

- **CI green** → squash-merge and clean up: `gh pr merge "$PR" --squash --delete-branch` (or invoke the `merge-pr` skill). Dependabot closes the alerts automatically once the fix lands on the default branch.
- **CI red** → attempt the documented quick fixes once; if still failing, **escalate**.

Final report: alert numbers cleared, anything intentionally deferred, and the merge result.

---

## Ecosystem playbooks

### pnpm / npm

- **Direct dep** → bump its range in `package.json` to `>= patched`.
- **Transitive dep** → add/raise an entry in `pnpm.overrides` (pnpm) or `overrides` (npm), e.g. `"qs": ">=6.15.2"`.
- **Regenerate without installing**: `pnpm install --lockfile-only` (npm: `npm install --package-lock-only`).
- **Workspaces**: overrides MUST live in the **workspace-root** `package.json`. A nested package's `pnpm.overrides` is *ignored* in the workspace context (pnpm prints a warning) — put workspace overrides at the root.
- **Standalone lockfiles**: a sub-project with its **own committed lockfile** (e.g. a docs/website site built separately on its own CI job) is installed with `--ignore-workspace`. Regenerate it from inside that directory:
  ```bash
  cd <subdir> && pnpm install --lockfile-only --ignore-workspace
  ```
  and put that project's overrides in **its own** `package.json`. A repo can have BOTH a root workspace lockfile and one or more standalone lockfiles pinning the **same** package at different versions — Dependabot lists each `manifest_path` separately, so **fix every manifest the alerts name.**
- A standalone lockfile whose specifiers no longer match its `package.json` (e.g. lock pins `next@16.2.3` while `package.json` says `^16.2.7`) is **stale and was failing `--frozen-lockfile`** — regenerating it produces a large but correct diff. Note the churn; don't treat it as suspicious.
- **Verify**: `pnpm audit --audit-level=moderate` (append `--ignore-workspace` when auditing a standalone project) and `pnpm install --frozen-lockfile`.

### cargo (Rust)

- `cargo update -p <pkg>@<current> --precise <patched>` from the crate dir (the one with `Cargo.toml` + `Cargo.lock`).
- **Multiple copies in the tree**: the same crate can appear at several versions; the advisory range may cover more than one. Use `cargo tree -i <pkg>@<ver>` to see who pulls each.
- **Runtime vs build-only**: a copy reachable *only* through `[build-dependencies]` is compile-time (codegen, perfect-hash generators, etc.), never shipped in the binary, and usually not runtime-exploitable. If such a copy is **pinned by an upstream crate** (e.g. a framework's own toolchain) with no reachable patch, **document it and recommend dismissing that alert** rather than forking upstream. Fix the runtime-relevant copy and move on.

### pip / Python

- `requirements.txt`: bump the pin to `>= patched`. Poetry: `poetry update <pkg>`. uv: `uv lock --upgrade-package <pkg>`. Regenerate the lock, then `pip-audit` / `uv pip audit` to verify.

### go

- `go get <pkg>@<patched> && go mod tidy`. Verify with `govulncheck ./...` if available.

### bundler (Ruby)

- `bundle update --conservative <gem>` to bump only the vulnerable gem. Verify with `bundle audit`.

> Any other ecosystem: apply the same pattern — **direct bump or transitive override → regenerate lockfile → audit**.

---

## PR body template

```markdown
Resolves the open Dependabot alerts.

## Changes

| Manifest | Fix | Alerts |
|---|---|---|
| `<path>` | `<pkg> X → Y` (direct / override) | #NN, #NN |

## Notes
- <intentional lockfile churn, if any, and why>
- <any alert deliberately left, with the reason and a dismissal recommendation>

## Verification
- `<audit cmd>`: No known vulnerabilities found (moderate+)
- `<frozen-lockfile install>`: passes
- <build/test result or "relying on CI">

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Notes

- This sweeps **all** open alerts in one PR by default — don't ask which ones.
- Keep `git add` scoped to the manifests and lockfiles you changed.
- Don't use `--no-verify`; let hooks run.
- If the repo already has an open Dependabot-fix PR/branch, update it instead of opening a duplicate.
