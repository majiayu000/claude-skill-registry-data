---
name: dependabot
description: Configure Dependabot coverage, grouping, cooldowns, and trusted automation.
---

# Dependabot policy

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/dependabot/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Read every applicable `AGENTS.md`, then the repository's dependency, CI, release,
and branch-protection docs. The consumer wrapper owns the accepted cooldown, package roots,
first-party publishers, manual-update exceptions, runner policy, required checks, and secret source.

## Cover the dependency graph

- Inventory tracked manifests, lockfiles, Dockerfiles, workflow actions, infrastructure roots, and
  any companion dependency bot. Add one Dependabot update entry per supported ecosystem and
  manifest root. Do not create a second owner for a dependency already assigned elsewhere.
- Schedule version checks daily. Set `cooldown.default-days` to the consumer's release delay, or
  seven days when local policy does not choose another value. Cooldown applies to version updates,
  not security updates.
- Set `open-pull-requests-limit: 5` on every update entry. The limit is per entry and covers
  version updates only. Use a lower value only when a serialized repair or manual validation path
  requires it.
- Keep security updates enabled and immediate. Do not add an age gate that delays vulnerability
  fixes.

## Group package families

Group packages that share one compatibility family or release train. Do not group by version type.
Use manifests, peer dependencies, lockfiles, and upstream release practice to decide what moves
together.

```yaml
cooldown:
  default-days: 2
  exclude: ['@acme/*', 'acme-cli']
groups:
  first-party:
    patterns: ['@acme/*', 'acme-cli']
  oxc:
    patterns: ['oxlint', 'oxfmt', 'oxlint-tsgolint']
  vitest:
    patterns: ['vitest', '@vitest/*', '@vitejs/*']
  react:
    patterns: ['react', 'react-dom']
  react-security:
    applies-to: 'security-updates'
    patterns: ['react', 'react-dom']
  react-email:
    patterns: ['react-email', '@react-email/*']
```

- Name each group for the package, toolchain, framework, or verified release family. Prefer a narrow
  namespace or prefix wildcard such as `@vitest/*` when that wildcard is one family. Put more
  specific families before broader ones.
- Do not add generic groups such as `other-minor-and-patch`, `minor-and-patch`,
  `security-minor-and-patch`, or `security-updates`. Do not use `patterns: ['*']` to force every
  update into a group. Narrow family wildcards are expected. Leave unrelated packages ungrouped.
- Omit `update-types` so a family receives major, minor, and patch updates. Major updates stay
  human-reviewed. Leaving majors out of the group splits the release train.
- Groups default to `applies-to: version-updates`. When the same family is also safe to upgrade
  together for security fixes, add a separate group such as `react-security` with the same patterns
  and `applies-to: security-updates`. Do not combine unrelated vulnerability fixes into one group.
- Keep verified first-party packages in a `first-party` group. For a namespace the owner wholly
  controls, use its scoped wildcard, such as `@acme/*`. List unscoped packages by exact name.
- Keep first-party patterns in `cooldown.exclude` so those updates have zero-day eligibility, while
  third-party packages keep the release delay. A grouped pull request is auto-mergeable only when
  every included update is eligible.

## Exempt verified first-party releases

- Use `cooldown.exclude` only for first-party packages whose owning repository and default-branch
  release workflow have been verified.
- That workflow must publish the package with OIDC, `id-token: write`, and no long-lived registry
  token.
- Use a namespace wildcard only when the owner controls the whole namespace and intends future
  packages to inherit the exemption. Otherwise use exact package names.
- Keep the consumer-owned registry, documentation, cooldown exclusions, and `first-party` group in
  sync.

## Preserve the trust boundary

- Use a trusted default-branch `pull_request_target` workflow only for metadata inspection and the
  minimal auto-merge mutation.
- Revalidate the live pull request, Dependabot identity, default base, same-repository
  `dependabot/` head, and immutable base and head SHAs.
- Do not check out or execute pull-request code in that privileged workflow. Pin external actions
  per local policy.
- Auto-merge only a verified semver patch, or a stable minor whose old and new majors are both at
  least 1. Majors, pre-1.0 minors, prereleases, downgrades, malformed or inconsistent metadata, and
  consumer-declared manual ecosystems need a human.
- Enable platform auto-merge. Do not auto-approve. Required checks and branch rules remain the gate.
- Store `DEPENDABOT_AUTOMERGE_TOKEN` as a Dependabot secret, not only as an Actions secret. Grant
  only the Contents and Pull requests access needed to enable or disable auto-merge. Fail an
  eligible mutation visibly when the token is missing or underprivileged.
- A Dependabot-triggered workflow cannot assume ordinary Actions secrets or trusted OIDC access.
  Copy only the narrow credentials mandatory tests need into Dependabot secret scope.
- For cloud, deployment, production, or other privileged checks, keep credential-free validation
  running and mark the trusted portion skipped or not applicable for Dependabot. A required fan-in
  job must distinguish that intentional state from an unexpected missing credential.

## Validate and roll out

- Parse the YAML. Run the repository's workflow checker and policy tests.
- Inspect the diff for uncovered manifests, overlapping groups, broad exemptions, secret exposure,
  and pull-request code crossing a privileged boundary.
- Verify repository settings for dependency security updates and auto-merge.
- After the configuration reaches the default branch, read Dependabot logs for every configured
  root. Check a representative patch, minor, major, security update, manual update, and
  missing-secret path.

Consumer wrapper owns: cooldown, package roots, first-party publishers, manual-update exceptions,
runner policy, required checks, and secret source.
