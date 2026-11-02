---
name: promote-release
description: Use when deploying — promoting develop to stage (stg) or stage to main (prd) by fast-forward of a verified SHA, with the ancestry invariant, approval gates and deploy-status preconditions.
---

# Promote Release

Promotion moves a verified SHA forward: `stage := develop@<sha>`, then `main := stage@<sha>`. It is a
fast-forward, never a merge or squash. Contract: [branch-promotion](../_shared/branch-promotion.md); full
commands: [promotion-recipes](./promotion-recipes.md).

## 1. Audit (change nothing)

```bash
git fetch origin --prune --tags
git rev-parse origin/develop origin/stage origin/main          # the three SHAs, printed
git merge-base --is-ancestor origin/main origin/stage \
  && git merge-base --is-ancestor origin/stage origin/develop  # both must exit 0
ls .github/workflows/promote.yml 2>/dev/null                    # is the promotion workflow present?
for b in stage main; do gh run list --branch "$b" --json status,conclusion,databaseId,workflowName --limit 10; done
# latest deployment status of a SHA on an environment (a deployment has no state; its statuses do)
dep_state() { local id; id=$(gh api "repos/{owner}/{repo}/deployments?environment=$1&sha=$2" --jq '.[0].id // empty')
  [ -n "$id" ] && [ "$id" != null ] && gh api "repos/{owner}/{repo}/deployments/$id/statuses" --jq '.[0].state' || echo none; }
dep_state dev "$(git rev-parse origin/develop)"     # must print success before promoting to stg
```

Read the three SHAs and the invariant. A run that is still `queued` or `in_progress` on the target
environment blocks a promotion — never start two releases for the same env at once. The deployment lookup
proves the source SHA deployed green on the previous environment before it moves forward.

## 2. Decide

- `origin/develop == origin/stage == origin/main` → nothing to promote; report it, stop.
- `origin/stage..origin/develop` is non-empty and the invariant holds → fast-forward possible → promote
  (steps 3 to 6).
- The invariant is broken → stop and go to the repair recipe (contract rule "repair a broken chain by content") first.
- `main` holds content `develop` lacks (a hotfix) and `stage == main` → hotfix, not promotion (contract rule "hotfix").

## 3. Detect the track

- `promote.yml` present → dispatch it:
  ```bash
  gh workflow run promote.yml -f target=stg
  ```
  The workflow runs the preflight (and `e2e` for stg), waits on `promote-stg`, pushes the SHA, starts the
  stg deploy and waits for it. Do the same for `prd` with `-f target=prd` once stg is green. `dev` must have
  deployed the SHA first: `gh workflow run deploy.yml --ref develop`.
- No workflow yet → manual fast-forward push of the verified SHA with the same checks (steps 4 to 7), and
  recommend [set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md) (infra) or
  [set-up-delivery-pipeline](../../infra/set-up-delivery-pipeline/SKILL.md) (apps) to add `promote.yml`, so
  promotion is one dispatch instead of hand-run git.

## 4. Promote to stg

```bash
SHA=$(git rev-parse origin/develop)
git log --oneline origin/stage..$SHA          # the changelog — show it, then approve
git push origin "$SHA:refs/heads/stage"       # fast-forward only; never --force
```

On a manual run, confirm the SHA deployed green on `dev` first (the deployment lookup in step 1). The
workflow's preflight does this for you. With the fleet pipeline a push deploys nothing; in a repo without `promote.yml`, start
the deploy by hand: `gh workflow run infra.yml --ref stage -f environment=stg -f mode=apply`.

## 5. Wait

Wait for the target pipeline run for that SHA to complete **and** succeed, and the smoke test to pass. A
run waiting at an approval is **not done** — do not treat it as finished. A stale run waiting at an
approval blocks every later run of that environment: reject superseded pending deployments instead of
approving a days-old plan:

```bash
gh api "repos/{owner}/{repo}/actions/runs/<id>/pending_deployments" --jq '.[].environment | {id, name}'
gh api -X POST "repos/{owner}/{repo}/actions/runs/<id>/pending_deployments" \
  -F 'environment_ids[]=<env-id>' -f state=rejected -f comment="superseded by $SHA"
```

## 6. Promote to prd

Same, from `stage`, with the stg deployment of that SHA as the precondition:

```bash
SHA=$(git rev-parse origin/stage)
dep_state stg "$SHA"                           # must print success (helper from step 1)
git log --oneline origin/main..$SHA
git push origin "$SHA:refs/heads/main"
```

Then start the prd deploy (`gh workflow run infra.yml --ref main -f environment=prd -f mode=apply`) and wait
(step 5) for that run.

## 7. Verify

```bash
git rev-parse origin/develop origin/stage origin/main           # after a full release: all three equal
git merge-base --is-ancestor origin/main origin/stage \
  && git merge-base --is-ancestor origin/stage origin/develop
git rev-list --count origin/stage..origin/main                  # expect 0
git rev-list --count origin/main..origin/stage                  # expect 0 after a full release
dep_state prd "$(git rev-parse origin/main)"     # success
```

If the release merge reported failure but `main` moved, do not push anything blindly: verify the branch
SHA and that a pipeline run exists for it.

## References

- [../_shared/branch-promotion.md](../_shared/branch-promotion.md): the contract: its rules,
  enforcement and deviations.
- [promotion-recipes.md](./promotion-recipes.md): full commands — ff promotion, hotfix, back-merge,
  reconcile, revert-on-main, stale locks, release scope.
- [../../infra/set-up-terraform-pipeline/SKILL.md](../../infra/set-up-terraform-pipeline/SKILL.md),
  [../../infra/set-up-delivery-pipeline/SKILL.md](../../infra/set-up-delivery-pipeline/SKILL.md): the
  workflows that carry out promotion.
