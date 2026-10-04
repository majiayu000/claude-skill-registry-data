---
name: deploy-anywhere
description: >
  Deploy with unified build/test/deploy intent across providers using
  .agent-loom/deploy.yml and per-provider adapters. Load when the user
  asks to deploy, ship to preview, release to production, or run a
  provider-agnostic deploy flow. Also triggers on "deploy anywhere",
  "deploy to Vercel", "deploy with GitHub Actions", "preview deploy",
  or "ship this". Runs preflight before any deploy — stops on missing
  secrets. Pairs with ci-cd-and-automation for pipeline design. Ships
  vercel and github-actions adapters; extensible adapter interface.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: nikolareljin/ci-orchestrator, universal-deploy/universal-deploy, vercel/examples
  resources:
    references:
      - DEPLOY-SCHEMA.md
      - adapters/vercel.md
      - adapters/github-actions.md
      - examples.md
    scripts:
      - preflight.py
---
# Deploy Anywhere

One deploy intent — read or scaffold `.agent-loom/deploy.yml`, detect provider, **preflight** secrets, run adapter steps, return URL + rollback command.

## Hard Rules

Run `scripts/preflight.py` before any deploy — **no partial deploys** on missing config/secrets.
Secrets by name only in files — never write credential values to repo.
Shipped adapters: `vercel`, `github-actions` — see `references/adapters/`.
Run `test_cmd` from config when present before build.
Emit deployment summary: target, URL/status, rollback command.

---

## Workflow

### Step 1 — Read or scaffold config

Load `.agent-loom/deploy.yml` per `DEPLOY-SCHEMA.md`. If missing, scaffold from repo signals (`vercel.json`, `.github/workflows/`) and confirm with user.

### Step 2 — Detect target

Config `targets[]` first; else repo signals; else ask.

### Step 3 — Preflight

```bash
python3 .agents/skills/deploy-anywhere/scripts/preflight.py
```

On fail: list missing items exactly; **stop**.

### Step 4 — Test + build

Run `test_cmd` then `build_cmd` from config.

### Step 5 — Run adapter

Load `references/adapters/<provider>.md`. Execute documented CLI sequence.

### Step 6 — Summarize

```markdown
## Deploy summary
Target: [provider] ([preview|prod])
URL: [url or run link]
Rollback: [command]
```

---

## Gotchas

- Vercel prebuilt flow requires `vercel build` before `vercel deploy --prebuilt`.
- Local `gh workflow run` needs `gh` auth — not the same as CI token.
- Multiple targets deploy sequentially — confirm order with user.

---

## Output Format

See Step 6 summary template.

---

## Examples

Teaser: deploy.yml with vercel target → preflight OK → build → deploy URL returned.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Skip preflight — I'll add secrets later" | Half-configured deploys fail opaquely. |
| "Embed token in deploy.yml for now" | Secrets in repo leak — names only. |
| "Skip tests this once" | test_cmd exists for a reason. |
| "One adapter fits all" | Use the adapter file — don't improvise CLI. |
| "Rollback is optional" | Always emit rollback command. |

## Verification

- [ ] preflight.py passed
- [ ] test_cmd run when configured
- [ ] Adapter steps from reference file
- [ ] Rollback command in summary

## Red Flags

- Deploy attempted after preflight fail
- Secret value written to yaml
- Unknown provider without adapter file

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 3 family)

## Impact Report

```
Deploy: [provider] | Preflight: [pass/fail] | URL: [url or n/a]
```
