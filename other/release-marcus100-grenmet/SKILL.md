---
name: release
description: "Drives the release pipeline dev → staging → main → tagged release with CI gating, arming staging auto-merge automatically and stopping for the owner before main and production. Use when promoting dev to staging, or when the user asks to release, promote or ship to production."
allowed-tools: Bash(pnpm *), Bash(turbo run *), Bash(gh *), Bash(git *), Bash(curl *)
---

## Release Promotion

Follow `docs/operations/release-runbook.md`. Local dev integration, direct dev
push, staging PR creation/update and merging after all applicable checks pass
have standing user authorization. Monitor the resulting staging deployment.
Main merges and production publication/deployment need separate authorization.
Never bypass protection, hooks, or failing checks.

**1. Pre-flight**
Integrate completed task branches into local `dev` and validate the combined
result before pushing `dev` directly. Do not push feature branches or open
feature-to-dev PRs unless requested. See `AGENTS.md` → Git and GitHub Workflow.

Confirm the latest `dev` CI run is green (`gh run list --branch dev --limit 3`);
if not, triage it first. Run `pnpm check:ci` and `pnpm type-check`, then the
`/pre-merge` checklist. Report findings. Stop and ask if anything is red.

**2. dev → staging**
Create or reuse the promotion PR (`gh pr create --base staging --head dev`).
Review its complete diff for authorized, finished work. Keep the PR body's
recap current: changed, gates, outcome and friction per `/commit` step 7. Verify
`dev` still matches the reviewed head, then arm auto-merge without another
confirmation: `gh pr merge <num> --auto --merge --match-head-commit <sha>`.
GitHub merges once the staging ruleset's required checks pass; `CI Success` and
`Build Web Apps` aggregate every API and web job (see
`docs/operations/release-runbook.md`). If dev advances, review the new head and
re-arm on it.
On failure, diagnose and fix locally within scope, validate and push dev again.
Monitor `pipeline-staging.yml` and verify its deployed SHA still equals staging
head. Then smoke-test what the promotion changed:
- `curl -fsS https://api.staging.barrels.gd/api/v1/utils/health-check/`
- `pnpm ui:screenshots --url https://<app>.staging.barrels.gd --path /` for each
  web app in the promoted diff (hosts in `docs/ports.md`); read the PNGs and
  treat console errors as defects. Aborted `_rsc` prefetches are not.
- Probe new public API routes with `curl`; staging has no `/docs` page.
- Pages behind sign-in: use Claude in Chrome if connected, otherwise list the
  exact pages for the owner (`docs/agents/tool-usage.md`).
Report readiness for authenticated acceptance or actionable failure;
do not claim acceptance from CI alone. Stay quiet while status is unchanged.

**3. staging → main**
After staging acceptance, create/update a PR with `--base main --head staging`.
Obtain separate authorization before merging. Remind the user: merging to main
builds nothing extra and does not deploy prod.

**4. Release**
Determine the next `vN.M` tag from `gh release list --limit 3`. Draft release
notes from the PRs/commits promoted. Show the exact
`gh release create vN.M --target main --title "vN.M" --notes "…"` command and
stop — the user publishes. After publish, watch `pipeline-prod.yml`; note that
a queued deploy job usually means the self-hosted production runner is offline.

**5. Verify**
`curl -fsS https://api.barrels.gd/api/v1/utils/health-check/` and report status.
List the canonical app domains from `docs/deployment.md#canonical-app-domains`
for the user to spot-check.

**Output style:** one short status line per gate as you pass it. At each human
gate, say exactly what to click/run and nothing else.
