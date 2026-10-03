---
name: ls-github-actions-builder
description: Guide GitHub Actions workflow authoring. Use for CI, release, scheduled
  jobs, permissions, caching, matrices, artifacts, and secure workflow design.
metadata:
  version: '1.0'
---

# GitHub Actions

Use this skill when authoring or reviewing GitHub Actions workflows.

## Workflow

1. Inspect existing triggers, permissions, concurrency, secrets, environments, and repository rules before editing.
2. Define the smallest job permissions, cache key/restore strategy, artifact retention, and validation needed for the change.
3. Resolve every third-party action release to its full 40-character commit SHA. Keep the human-readable release tag only as an adjacent comment; never use a mutable `@vN`, branch, or tag as the executable ref.
4. Verify the owner, release tag, and commit provenance before accepting a new or updated SHA. Advance pins only through the repository's controlled dependency-update or reviewed maintenance process.
5. Validate YAML, changed workflow paths, and representative local or CI commands before relying on automation.

## Immutable action references

```yaml
# actions/checkout v4.2.2
uses: actions/checkout@<verified-40-character-commit-sha>
```

- The SHA is the executed supply-chain boundary. A major-version tag such as `@v4` is a mutable Git ref and is not a safe default for credential-bearing CI.
- Do not copy a SHA from an unverified issue, example, or third-party workflow. Resolve the intended official release, review its provenance, and record the release tag in the comment.
- Treat third-party action pin changes as dependency updates: review the diff and release notes, run the workflow's relevant validation, and retain the review evidence.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source classification: `official-docs-reference`
- This is a LocalSetup-native skill written from project workflow requirements and public/official documentation routing.
