---
name: ci-cd-and-automation
description: >
  Design and implement CI/CD pipelines and automation — fast checks on every PR,
  safe releases, and repeatable workflows. Load when setting up GitHub Actions
  (or similar), adding pre-merge gates, automating releases, or the user asks
  "add CI", "set up workflows", "automate checks", "CD pipeline". Not for
  one-off local scripts (use task-specific tooling).
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: addyosmani/agent-skills ci-cd-and-automation (11/12, 2026-05-29)
  resources:
    references:
      - examples.md
---

# CI/CD and Automation

You create a pipeline that is **fast, deterministic, and protective**: it runs the right checks automatically, fails loudly, and makes shipping boring.

## Hard Rules

- Prefer **fast PR checks** (minutes) over heavy pipelines that nobody trusts.
- Fail on **lint/test/typecheck/build** before merge; keep steps deterministic.
- Never store secrets in repo; use platform secret stores and least privilege.
- Make workflows **cache-aware** and **concurrency-safe** (cancel superseded runs).
- Add automation only when it has a clear owner and a failure mode plan.

---

## Workflow

### Step 1 — Define lifecycle and artifacts

Write:
- Target events: PR, main push, tag, manual dispatch
- Required gates: lint, unit, integration, build, security scan (if available)
- Release artifact: npm package, container, binary, docs site, or “none”

### Step 2 — Choose the minimum viable pipeline

Start with:
- **PR workflow**: checkout → setup runtime → install deps → cache → lint/typecheck → tests → build
- **Main workflow**: re-run critical checks + publish artifact (optional)

### Step 3 — Make it reliable

- Pin runtime versions (Node/Python/etc.)
- Use lockfiles
- Cache dependencies
- Add concurrency cancellation on PR branches
- Split slow suites into separate jobs only when needed

### Step 4 — Secrets and permissions

- Use env vars from secret store
- Minimize token permissions (read-only unless publishing)
- Avoid broad “write-all” permissions on default branch workflows

### Step 5 — Add automation hooks (only if they pay rent)

Examples:
- Auto-label PRs
- Run formatter on changed files (if you accept auto-fixes)
- Generate changelog on release tag

### Step 6 — Verification

- Trigger PR workflow on a small change; ensure duration is acceptable
- Confirm failing checks block merge (branch protection)
- Confirm secrets are not echoed in logs

---

## When NOT to use

- Tiny repos where CI cost exceeds value (prototype stage) unless the user explicitly wants it
- Complex deployment platforms without access (require infra context first)

---

## Gotchas

- “Green CI” that doesn’t match local commands becomes ignored.
- Unpinned runtimes cause flakey builds over time.
- Missing branch protections makes CI advisory-only.
- Long pipelines encourage skipping checks; keep PR path fast.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We don’t need CI yet" | CI is cheapest when the repo is small; add the PR gates early. |
| "Let’s add every check" | Overbuilt CI becomes slow and ignored; start minimal and expand on evidence. |
| "Caching is premature optimization" | Without caching, CI becomes slow and gets bypassed. |
| "We’ll add branch protection later" | CI without enforcement is a suggestion, not a gate. |
| "We can just use a PAT" | PATs are high-risk; use least-privilege tokens and secret stores. |

---

## Output Format

```markdown
## CI/CD plan — [repo]

Events: [PR/main/tag/manual]
Jobs: [list]
Runtime pinned: [yes/no]
Caching: [what]
Secrets: [needed + where stored]
Protections: [branch protections summary]
Verification: [how to prove it works]
```

---

## Examples

<examples>
  <example>
    <input>“Add CI to a TypeScript repo.”</input>
    <output>
Create `.github/workflows/ci.yml` with node-version pinned, npm cache, `npm ci`, `npm run lint`, `npm test`, `npm run build`, concurrency cancel. Add branch protection requiring the workflow.
    </output>
  </example>
</examples>

---

## Verification

- [ ] PR checks run on a sample PR and complete in an acceptable time
- [ ] Lint/tests/build are deterministic and match documented local commands
- [ ] Caching is enabled where appropriate
- [ ] Secrets are stored in the platform secret store (not repo)
- [ ] Branch protections enforce required checks (or explicitly deferred)

---

## Red Flags

- CI commands diverge from local lint/test/build scripts
- Runtimes and action versions left unpinned
- Branch protection missing — CI is advisory only
- Secrets committed or inlined in workflow YAML

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Repo: [name] | Workflows: N | Gates: [list]
Runtime pinned: [yes/no] | Cache: [yes/no]
Protections: [enforced/deferred]
```
