---
name: npm-publishing
description: Prepare npm bootstrap and trusted publishing commands for a human.
---

# npm publishing bootstrap

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/npm-publishing/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Prepare the local package. Leave public registry writes and trusted-publisher mutations to the
human. Read every applicable `AGENTS.md` from the repository root through the
package. Repository-local policy and the consumer wrapper own the package path and name, npm scope,
GitHub repository, release workflow, build commands, and whether a laptop may publish.

## Prepare the package

- Resolve the absolute repository root, the package directory relative to that root, the exact npm
  package name, `owner/repository`, and the release workflow filename. The workflow value is the
  case-sensitive filename under `.github/workflows`, not a path. Leave no placeholders in the final
  commands.
- Confirm npm 11.15 or newer, account-level two-factor authentication, and write access to the
  package or scope.
- On the default branch, the workflow must grant `id-token: write`, use a supported runner, install
  an npm version that can trusted-publish, and publish this package.
- When the package does not exist in the registry, create the smallest useful stub in its intended
  directory. Follow neighboring packages for metadata, source, exports, types, license, README,
  build output, and workspace registration.
- Do not replace an existing module with a stub. Do not publish a version already in the registry.
- Build the package, then inspect the payload with
  `npm publish <package-directory> --access public --dry-run`. Stop if it includes secrets,
  environment files, source maps, unrelated workspace files, or a missing runtime or type
  entrypoint. The dry run must include `prepublishOnly`. A pack-only check misses that script.
- If the package already exists, have the human run `npm trust list <package-name>` before any
  mutation. Omit the initial publish command. If trust already exists, report it and omit trust
  creation. Do not revoke or replace it.

## Hand off the mutations

- Do not run a real `npm publish` or a mutating `npm trust` subcommand.
- Say that the first command creates an externally visible, effectively irreversible package
  version, and the second grants the named workflow publish authority.
- Include the publish command only when bootstrapping a package that does not exist. An existing
  package with an empty trust list goes straight to trust setup.
- Tell the human to append a current one-time password after each final `--otp=` and not to share
  or record it. Warn that `--otp=` can expose the OTP in shell history and process arguments, and
  to follow local secret-handling policy.
- Give the applicable commands with resolved values, in this order:

```sh
cd /absolute/repository/root
npm publish ./relative/package-directory --access public --otp=
npm trust github @scope/package \
  --repo owner/repository \
  --file release.yml \
  --allow-publish \
  --yes \
  --otp=
```

- The `cd` target is the directory from which the relative publish path resolves.
- If local policy prohibits publishing from this machine, say so and name the approved environment.
  Keep the same command order.
- Ask the human to confirm the payload, package name, repository, workflow filename, and publish
  permission immediately before running the commands.
- Afterward, have the human verify any newly published version and run `npm trust list` again.
- Do not retry an authorization or registry failure blindly. Do not fall back to a long-lived npm
  token without explicit direction.

Consumer wrapper owns: package path and name, npm scope, GitHub repository, release workflow, build
commands, and whether a laptop may publish.
