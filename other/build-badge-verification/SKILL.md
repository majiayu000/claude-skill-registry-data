---
name: build-badge-verification
description: Use when you need to validate that a repository's automated build and publish pipeline is functioning correctly on a release or target branch, particularly when assessing the reliability of release artifacts or the health of a CI/CD workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - GitHub Actions
  - SIRIUS
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
---

# build-badge-verification

## Summary

Verify that a GitHub Actions build and publish workflow executes successfully on a specified branch by inspecting the workflow configuration, triggering execution, monitoring logs, and confirming the build status badge displays a passing result. This skill ensures release artifacts are being built and published correctly in continuous integration pipelines.

## When to use

Apply this skill when you need to validate that a repository's automated build and publish pipeline is functioning correctly on a release or target branch, particularly when assessing the reliability of release artifacts or the health of a CI/CD workflow. Use this when a status badge exists in the repository README and you need to confirm the reported status reflects actual workflow execution.

## When NOT to use

- The repository does not use GitHub Actions or has no automated build workflow configured.
- The workflow is not intended to publish artifacts (e.g., it is a test-only or linting workflow).
- The build status badge URL is not accessible or the badge is not present in the repository README.

## Inputs

- GitHub repository URL
- Target branch name (e.g., 'release-4-pre')
- Workflow configuration file path (e.g., .github/workflows/distribute.yaml)
- Repository README file

## Outputs

- Workflow execution logs
- Workflow run status ('passed' or 'failed')
- Build status badge verification result
- Confirmation of artifact publication status

## How to apply

First, locate the target repository and identify the release or target branch (e.g., 'release-4-pre' for SIRIUS). Next, examine the workflow configuration file (typically .github/workflows/distribute.yaml) to understand the build and publish pipeline's trigger conditions and steps. Then trigger the workflow by either creating a release tag or pushing to the specified branch, depending on the configured triggers. Monitor the GitHub Actions run in the repository's Actions tab, reviewing logs for any errors or warnings until completion. Finally, verify the workflow run status displays 'passed' and confirm that the build status badge in the README (e.g., via the badge URL badge.svg?branch=release-4-pre) reflects a passing status, typically indicated by 'passing' or 'success' label and green coloring.

## Related tools

- **GitHub Actions** (CI/CD platform that executes the build and publish workflow on configured triggers (tag creation or branch push); provides the Actions tab UI and workflow logs for monitoring execution and verifying status.) — https://github.com/sirius-ms/sirius
- **SIRIUS** (The target software framework being built and published by the workflow; understanding its structure and build requirements informs interpretation of workflow logs and artifact validation.) — https://github.com/sirius-ms/sirius

## Evaluation signals

- Workflow run completes without timeout or cancellation; status field in Actions tab shows 'passed' or 'success'.
- Build status badge URL (e.g., badge.svg?branch=release-4-pre) renders with green background and 'passing' or 'success' label text.
- Workflow logs show no ERROR or FATAL level messages; all build steps execute in expected order without skipping.
- Artifact artifacts (e.g., release binaries or packages) are present in the GitHub Releases section corresponding to the trigger event (tag or branch push).
- Badge status remains consistent across multiple page refreshes and matches the most recent workflow run timestamp in the Actions tab.

## Limitations

- Badge status may be cached by browsers or CDNs; refresh with cache-busting (e.g., Ctrl+Shift+R) to see the latest status.
- Workflow may succeed but artifact publication may fail silently if the publish step does not properly report errors; inspect the full workflow logs, not just the final status badge.
- The workflow trigger conditions (e.g., 'run on release tag creation' vs. 'run on branch push') must match your test scenario; pushing to a branch will not trigger a tag-only workflow.
- Repository permissions and branch protection rules may prevent manual workflow triggering; verify you have write access and no required reviews block the push.
- Build status badge reflects the specified branch only (as indicated by the ?branch=release-4-pre query parameter); other branches may have different statuses.

## Evidence

- [other] Workflow configuration insight: "Examine the distribute.yaml workflow file in the .github/workflows directory to understand the build and publish pipeline."
- [other] Workflow execution monitoring: "Monitor the GitHub Actions run until completion, tracking logs for any failures or warnings."
- [other] Status verification on badge: "Inspect the repository README to confirm the build badge displays a passing status (typically indicated by 'passing' or 'success' label and green coloring)."
- [readme] Build and Publish workflow badge in README: "[![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml)"
- [other] Workflow trigger and execution context: "Trigger the 'Build and Publish' workflow by creating a release tag or pushing to the release branch, depending on the workflow trigger conditions specified in distribute.yaml."
