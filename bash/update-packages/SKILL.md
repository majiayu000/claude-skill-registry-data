---
name: update-packages
description: Use when reviewing a Dependabot PR, judging whether a dependency major or upgrade is actually safe, driving a large manual dependency upgrade Dependabot won't do well, or checking for tool versions pinned in shell scripts that Dependabot cannot see.
---

# update-packages

## Overview

Dependabot already opens routine version-bump PRs (Actions, Docker, uv/Python,
Terraform, submodules). This skill is the **advisory complement** to it — the
judgment layer Dependabot lacks. It is **not** a routine bumper; never use it to
re-do what Dependabot already does on its own schedule.

## When to use

- A Dependabot PR is open and you need to decide whether to merge it.
- A major-version bump needs a safety call before trusting it.
- A large upgrade Dependabot handles poorly (big provider jumps, lockfile
  churn) needs a human-reviewed `plan`/`diff`.
- You suspect a tool version is pinned somewhere Dependabot can't read.

**Don't** use it to bump things on a schedule, or to override a clean Dependabot
PR with manual edits.

## The three jobs

### 1. Judge a Dependabot PR
Green CI is necessary, not sufficient. For a **major**, read the upstream
changelog for breaking changes and confirm the release *actually* does what its
notes claim.

> Cautionary example: a `dokploy` provider `0.4.0` release was assumed to fix a
> redeploy bug; checking the actual release contents disproved it. Verify the
> fix exists in the diff, don't trust the version label or the PR title.

### 2. Drive large manual upgrades
For jumps Dependabot won't sequence well (e.g. a `linode/linode` provider
`3.4.0 → 3.14.x`), do it by hand and gate on a reviewed `terraform plan` diff —
confirm the plan shows only intended changes, no surprise resource replacement.

### 3. Track shell-pinned tool versions
Dependabot can't see versions hard-coded in shell scripts. Scan
`dotfile-utils/scripts/install_*.sh` for pins (e.g.
`CHEZMOI_VERSION="v2.70.5"`), check upstream releases, and propose bumps.
Scripts that resolve "latest" at runtime (e.g. `install_bw_cli.sh`) have nothing
to track — skip them.

## Quick reference

| Situation | Action |
|-----------|--------|
| Dependabot minor/patch, green CI | Low risk — merge |
| Dependabot major | Read changelog; confirm fix is real before merging |
| Provider/module multi-version jump | Manual; gate on reviewed `terraform plan` diff |
| Tool pinned in `install_*.sh` | Check upstream; propose bump manually |
| Script resolves latest at runtime | Nothing to track |

## Common mistakes

- **Trusting the version label.** A release tagged as fixing X may not. Read the
  diff.
- **Merging a major on green CI alone.** CI proves it builds, not that the
  breaking changes are handled.
- **Forgetting shell pins.** They drift silently because no bot watches them.
