---
name: ls-firebase-hosting-basics
description: Guide Firebase Hosting setup and deploy basics. Use for Firebase static
  hosting configuration, deploy previews, rewrites, headers, redirects, and CLI validation.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: adapted-import
    source_url: https://github.com/firebase/agent-skills
    source_path: skills/firebase-hosting-basics/SKILL.md
    source_commit: 538130c39402a40d9c2586ede87def5914641a33
    source_ref: main
    source_sha256: 70587dd26053712d9e7e1e9461ce4856455f9bee4cd4cae60d4c89b2f4e17624
    license: Apache-2.0
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Firebase Hosting

Use this skill when working on Firebase Hosting tasks.

## Workflow

- Inspect `firebase.json`, `.firebaserc`, project aliases, framework output directories, and CI deploy commands.
- Validate rewrites, redirects, headers, cleanUrls, trailingSlash, and cache-control behavior before deploy.
- Use Firebase CLI commands in dry-run or preview-oriented modes when possible and keep project IDs out of source.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source: `https://github.com/firebase/agent-skills`
- Ref: `main` at `538130c39402a40d9c2586ede87def5914641a33`
- Source path: `skills/firebase-hosting-basics/SKILL.md`
- License classification: `Apache-2.0`
- Source SHA-256: `70587dd26053712d9e7e1e9461ce4856455f9bee4cd4cae60d4c89b2f4e17624`
