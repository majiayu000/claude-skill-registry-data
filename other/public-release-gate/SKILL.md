---
name: public-release-gate
description: Review a public repository release across version and tag consistency, final build artifacts, archives, secrets and internal material, third-party licenses, production response headers, and GitHub Release attachments. Use when the user asks to publish, create a tag or Release, verify a launch, or run the complete public-release gate, adapting checks to the project's configuration.
---

# Public Release Gate

Treat a Release as a separate deliverable. Repository commit checks do not
constitute a Release review; inspect the source, final artifacts, release page,
and deployment state together. The sibling `public-repo-git-gate` skill owns
the public-content and branch gates for commit, push, and PR operations. Do not
repeat this skill's artifact checks for an ordinary commit.

This skill is a manual review workflow. A passing script or CI job alone does
not prove every Release condition. Reuse the project's existing automated
checks first, then manually verify final artifacts, the hosting platform, and
production. Mark the gate as passed only when the required evidence exists.

Keep the review read-only by default. Creating a tag or GitHub Release,
uploading attachments, changing production configuration, or deploying each
requires explicit user authorization. Passing this gate does not authorize
any of those actions.

## Inputs and output

Before starting, identify the repository root, target version and tag, final
artifact paths, third-party resource inventory, production URL, and
project-specific configuration.

Return a structured record containing at least:

```text
Release gate: PASS | BLOCKED | FAILED
Repository:
Version / tag:
Build and artifacts:
Publicity and sensitive-data scan:
Third-party notices:
Deployment and response headers:
Release page and attachments:
Evidence:
Skipped checks / residual risks:
```

`PASS` means that all required evidence was checked. `BLOCKED` means that an
external state, permission, or user decision is missing. `FAILED` means that
the review found a problem. Neither non-passing state permits creating a tag,
GitHub Release, or continuing deployment.

## Workflow

1. Identify repository visibility, technology stack, build commands, artifact
   directories, version sources, third-party resources, and deployment entry
   points.
2. Check that `package.json` and lockfiles, or the project's version files,
   agree with the README, CHANGELOG, Release Notes, and tag.
3. Build the final artifacts from a clean state. Scan both the artifact
   directories and final archives; do not scan only the source tree.
4. Check for secrets, personal or customer data, internal business or legal
   material, private model or service configuration, and files that do not need
   to be public.
5. For vendored code, models, WASM, fonts, and media, verify the source,
   version or commit, license, redistribution terms, and SHA-256 individually.
   The license inventory must match the final resources.
6. After deployment, check HTTPS, HTTP status, key static entry points, CSP,
   HSTS, X-Frame-Options, and other project-required response headers.
7. Before creating a GitHub Release, verify the tag, Release page, and every
   attachment. Attachments must come from scanned final artifacts; calculate
   and record their SHA-256 values.
8. When database migrations, edge functions, or external configuration are
   involved, confirm production state separately. Passing CI does not prove
   that a production migration ran.

## Reuse project checks

Prefer the project's existing `release:check`. If none exists, create
`release-gate.config.json` in the project root with at least:

```json
{
  "versionFiles": ["package.json"],
  "artifactPaths": ["dist"],
  "vendoredPaths": [],
  "noticeFiles": ["THIRD_PARTY_NOTICES.md"],
  "requireDeploymentChecklist": true,
  "deploymentChecklist": "docs/release-checklist.md",
  "production": {
    "requiredHeaders": [],
    "forbiddenHeaderValues": [],
    "paths": ["/"]
  }
}
```

This is a cross-project convention example, not a universal validation
schema. The project's own `release:check` must validate its actual fields and
paths.

Keep project-specific details in the configuration, such as Supabase
migrations, a Vercel production URL, Piper resources, and required headers.
Do not copy one project's assumptions into another.

Prefer to provide these commands or equivalent entry points:

```text
npm run verify          # Source, tests, and build
npm run release:check   # Release metadata, artifacts, licenses, and deployment checks
```

When no automated entry point exists, perform the same checks manually and
record the evidence in the PR or Release Notes. Stop the release on any failed
check; do not create the Release first and explain afterward.

## Failure, blocking, and recovery

1. If you find a secret, personal data, internal material, a missing license,
   or an artifact mismatch, stop the release and record the exact path,
   attachment, or check item.
2. If the production URL, GitHub Release permission, deployment state, or
   external configuration is unavailable, mark the gate `BLOCKED`. Do not use
   a successful local build as a substitute for external evidence.
3. After a fix, rerun the failed check and recheck affected versions, artifact
   hashes, and attachments. Do not reuse an old `PASS` record unchanged.
4. Treat exposed secrets or personal data as a security incident, rotate the
   credentials, and retain an incident record. Merely deleting a file or
   rewriting history does not prove that the risk is gone.

## Platform boundaries

Version, build, artifact, and license checks apply across languages and build
systems, but use the commands defined by the project. GitHub Release, HTTP
header, and production-deployment checks depend on the relevant hosting
platform. Do not describe an untested platform CLI, Preview environment, or
local server result as production verification.

## Trigger phrases

Treat the following requests as full triggers:

- "Check this Release against the complete public-repository gate."
- "Can this tag be released?"
- "Review the final installer/archive and GitHub Release."
- "Verify this version after launch."

An ordinary request to "check a commit" covers only the commit/PR gate. When
the user mentions a Release, tag, installer, store package, deployment, or
launch, use this skill's complete workflow.
