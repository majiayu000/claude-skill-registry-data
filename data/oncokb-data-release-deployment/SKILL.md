---
name: oncokb-data-release-deployment
description: Update the knowledgesystems-k8s-deployment yamls for an OncoKB data release. Use when rolling a data release out to the public site, demo, trimmed public API, or MSK prod.
---

## Scope

Covers only the deployment-repo edits in the `Release and Deployment` half of [`DATA_RELEASE_ISSUE_TEMPLATE`](https://github.com/oncokb/oncokb/blob/master/DATA_RELEASE_ISSUE_TEMPLATE): pointing each cluster's deployment at the new image tag and the new versioned database.

Two actions in that checklist are the user's, never yours:

- Creating and importing the versioned database on each RDS instance.
- Syncing and restarting the workloads in ArgoCD.

You stop and hand off at both. The staging pipeline, the GitHub releases, and the oncokb-data branch merges happen before this skill runs.

## Repository

All edits land in `knowledgesystems/knowledgesystems-k8s-deployment`. Locate the clone before editing; do not guess the path. Manifests live under `argocd/aws/<account>/clusters/<cluster>/apps/`.

## Deployment targets

| Target | File | Changes |
| --- | --- | --- |
| www.oncokb.org core | `argocd/aws/175678591974/clusters/oncokb-research/apps/oncokb-main/oncokb_core.yaml` | `image: mskcc/oncokb:<tag>` and the `-Djdbc.url` database name |
| www.oncokb.org frontend | `argocd/aws/175678591974/clusters/oncokb-research/apps/oncokb-main/oncokb_public.yaml` | `image: mskcc/oncokb-public:<tag>` |
| transcript API | `argocd/aws/175678591974/clusters/oncokb-research/apps/oncokb-main/oncokb_transcript.yaml` | `image: mskcc/oncokb-transcript:<tag>`, only when the transcript service itself was released |
| demo.oncokb.org | `argocd/aws/175678591974/clusters/oncokb-research/apps/public-access-apis/oncokb_core_demo.yaml` | `image: mskcc/oncokb:<tag>-no-frontend` |
| public.api.oncokb.org | `argocd/aws/175678591974/clusters/oncokb-research/apps/public-access-apis/oncokb_core_public.yaml` | `image: mskcc/oncokb:<tag>-no-frontend` |
| www.oncokb.aws.mskcc.org | `argocd/aws/084637913395/clusters/oncokb-production/apps/oncokb-core/oncokb_core_cbx.yaml` | `image: mskcc/oncokb:<tag>` and the `-Djdbc.url` database name |

Demo and the trimmed public API read from the fixed databases `oncokb_core_demo` and `oncokb_core_public`, so their `-Djdbc.url` stays as written; the user imports the new data into those names in place. Only `oncokb_core.yaml` and `oncokb_core_cbx.yaml` carry a versioned database name (`oncokb_core_vX_Y`) that has to move.

The transcript database name in `oncokb_transcript.yaml` (`SPRING_DATASOURCE_URL`) is unversioned; a transcript data refresh is an import plus a restart, not a yaml edit.

Leave every beta, staging, curation, preview, and germline manifest alone. They carry their own tags and are not part of a data release.

## Workflow

1. Collect the release inputs.
   - Ask one grouped question for: data version (`X.Y`), versioned core database name (`oncokb_core_vX_Y`), `mskcc/oncokb` tag, `mskcc/oncokb-public` tag, whether the transcript service was re-released and at what tag, and which of the six targets are in scope this release.
   - Derive nothing you were not told. The core tag and the data version are unrelated numbers.
   - Completion criterion: every in-scope target has a confirmed tag and database name.

2. Verify the images exist.
   - For each tag, confirm it is published: `curl -fsS https://hub.docker.com/v2/repositories/mskcc/<repo>/tags/<tag> > /dev/null`.
   - Check the `-no-frontend` variant separately; it is built by its own workflow and can lag the enterprise image.
   - If a tag is missing, stop and report which one. The GitHub release build is either still running or failed.
   - Completion criterion: every tag you are about to write resolves on Docker Hub.

3. Stop for the database import.
   - Report the exact work the user must do first, per in-scope target: which RDS instance, which dump from the merged `oncokb-data` `RELEASE/v<version>` folder, and which database name it lands in.
   - Name the versioned databases that must be created (`oncokb_core_vX_Y` on the public RDS and on the MSK prod RDS) and the fixed databases that are imported in place (`oncokb_core_demo`, `oncokb_core_public`).
   - Wait for the user to confirm the imports are done. Do not edit any yaml before that confirmation: a merged manifest pointing at a database that does not exist takes the site down on the next sync.
   - Completion criterion: the user has confirmed, target by target, that the data is loaded.

4. Edit the manifests.
   - Read each file first and change only the `image:` line and, where the table says so, the database name inside `-Djdbc.url`.
   - Preserve the rest of the URL query string exactly.
   - Show the full diff and have the user confirm it before any push.
   - Completion criterion: `git diff` touches only in-scope files and only those lines.

5. Open the pull request.
   - Branch from an up-to-date `master`, for example `deploy/oncokb-data-v<version>`.
   - Never push to `master` in this repository; if the user wants a direct commit they run it themselves.
   - Use `oncokb-make-pull-request` for the PR itself. Title the change after the data release and list each target with its old and new tag in the body.
   - Completion criterion: PR URL reported.

6. Stop for the sync and restart.
   - Tell the user the remaining work is theirs: merge the PR, sync the affected ArgoCD applications, and restart `oncokb-core` so it recaches.
   - Give them the verification step: `curl -s https://www.oncokb.org/api/v1/info` should report the new `dataVersion` and `dataVersionDate`, and the same check against `demo.oncokb.org`, `public.api.oncokb.org`, and the MSK prod host for the targets that were in scope.
   - Completion criterion: the user has the merge, sync, restart, and verification steps in one message, with nothing left implied.

## Quality bar

- Report the two hand-offs as hard stops, not as suggestions, and wait for an explicit confirmation at each.
- Write only tags the user gave you and Docker Hub confirmed.
- One PR per data release, covering every in-scope target, so the rollout is a single revert if it goes wrong.
- If a target's current tag already matches the requested tag, say so and leave the file untouched rather than producing an empty commit.
