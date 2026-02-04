---
name: dev-swarm-npm-publish
description: Publish JavaScript/TypeScript packages to the npm registry with consistent metadata, versioning, and release checks. Use when preparing or executing an npm release.
---

# AI Builder - NPM Publish

This skill provides a repeatable process for publishing packages to the npm registry with proper metadata, versioning, and safeguards.

## When to Use This Skill

- You need to publish a new or updated npm package
- You want a standard preflight checklist for npm releases
- You need guidance on npm CLI steps and package metadata

## Your Roles in This Skill

- **DevOps Engineer**: Ensure release process, tags, and automation readiness
- **Backend Developer (Engineer)**: Validate package structure and metadata correctness
- **Technical Writer**: Verify README and release notes expectations

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role, and Role-XYZ if have more roles}, I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.

## Instructions

Follow these steps in order:

### Step 1: Confirm prerequisites and access

- Verify required tools are installed and versions are visible.
- Ensure npm account access works from the CLI.
- If missing prerequisites, stop and resolve before continuing.

### Step 2: Validate package metadata and repository links

- Confirm `package.json` includes required fields and correct naming.
- Ensure repository, homepage, and issues metadata point to the correct GitHub URLs.
- Ensure README exists and meets the minimum content expectation.

### Step 3: Control published files

- Use the `files` field or `.npmignore` to exclude non-release content.
- Double-check the package tarball content before publishing.

### Step 4: Apply semantic versioning

- Choose patch/minor/major based on the change impact.
- Use `npm version` to update metadata and create the git tag.
- Ensure the branch matches the expected release branch.

### Step 5: Publish to npm

- Run a dry run with `npm pack`.
- Publish with correct access flags (especially for scoped packages).
- Verify the published package is visible on npm.

### Step 6: Post-publish management

- Add owners or deprecate as needed.
- Handle unpublish within the allowed window if necessary.

## Expected Output

- A published npm package with correct metadata, version, and README content
- A clear audit trail via git tags and release notes
- Confidence the package content matches the intended release

## Key Principles

- Prefer scoped packages when possible
- Never publish secrets
- Always validate metadata and README before release
- Use dry runs to verify package contents

## Common Issues

- 403 errors from version conflicts or missing access flags
- 402 errors for scoped packages published without `--access public`

## References

- For detailed commands, checks, and error handling, see `references/npm-publish.md`
