---
name: plugin-security-release-targets
description: Given a Mattermost priority/severity level and a plugin repository, resolve the target plugin release-X.Y branches by cross-referencing the platform release policy with the plugin versions declared in each platform Makefile, plus any plugin release branches not yet wired into the platform. Returns only branches that exist on the plugin's origin.
allowed-tools: Read, Bash(git ls-remote:*), Bash(git show:*), Bash(git clone:*), Bash(rg:*), Bash(gh api:*)
---

# Resolve target plugin release branches for a severity

You take a priority/severity level and a plugin identifier, then return the set of
plugin `release-X.Y` branches that a fix at that level must be cherry-picked onto.
The resolution works by: (1) delegating to `/cursor-automations:security-release-targets`
to get the set of active platform `release-X.Y` branches, then (2) looking up the
plugin version shipped in each platform release's Makefile, then (3) adding any plugin
release branches not yet referenced by the platform Makefile (newer than the highest
Makefile-resolved version), and finally (4) filtering to branches that exist on the
plugin's remote.

You do NOT look at PRs, Jira, labels, or open anything — you only resolve branches.
Ticket handling, gating, and cherry-pick execution live in the caller.

## Inputs

- `<PRIORITY>`: one of `Critical` | `High` | `Medium` | `Low`. Optional — if omitted, defaults to `Critical` (which resolves to all `ACTIVE ∪ ESR` platform versions, giving the broadest coverage).
  - Treat `Highest` as Critical-tier and `Lowest` as Low-tier.
  - If the value is unrecognised, return an empty result and report the unsupported priority.
- `<PLUGIN_REPO>`: the `owner/repo` of the plugin (e.g. `mattermost/mattermost-plugin-jira`).
- `<MAKEFILE_NAME>`: the artifact name as it appears in the platform Makefile (e.g. `mattermost-plugin-jira`). Used to grep for the bundled version.

## Step 1: Resolve platform release branches via `security-release-targets`

Invoke the `/cursor-automations:security-release-targets` skill with `<PRIORITY>` (or `Critical` if priority was omitted). That skill:

1. Parses the Mattermost release policy (reads `docs/main/product-overview/release-policy.mdx` from the `mattermost/mattermost` repo loaded in the workspace context)
2. Maps the priority to candidate platform versions (`ACTIVE ∪ ESR` for Critical/High/Medium; `{UPCOMING} ∪ ESR` for Low)
3. Filters to branches that exist on origin

Take its output — a deduped list of platform `release-X.Y` branches — as `PLATFORM_BRANCHES`.

If `PLATFORM_BRANCHES` is empty, return an empty list immediately.

## Step 2: Look up the plugin version in each platform release Makefile

The `mattermost/mattermost` repo must be available. If it's not yet cloned locally, clone it to a temporary location first:

```bash
git clone https://github.com/mattermost/mattermost.git /tmp/mattermost-repo
```

Reuse the cloned repo if it already exists at that path; otherwise, delete it after use to avoid disk bloat. Then use that path for subsequent `git show` commands. For each platform branch `release-X.Y` in `PLATFORM_BRANCHES`:

1. Read the Makefile directly from git (change to the repo directory if cloned):

   ```bash
   cd /path/to/mattermost && git show "origin/release-X.Y:server/Makefile" | rg -o '<MAKEFILE_NAME>-v[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?' | grep -v fips | sort -Vu | tail -1
   ```

2. Parse the semver from the match: `vMAJOR.MINOR.PATCH`. Keep only `MAJOR.MINOR` for branch resolution.

3. Track the highest `MAJOR.MINOR` across all platform branches — call this `MAX_MAKEFILE`. This will be used in Step 3 to identify plugin branches not yet wired into the platform.

If the branch does not exist on origin or the plugin is not found in the Makefile, skip that platform version.

## Step 3: Include plugin release branches not yet wired into the platform

A plugin may cut a `release-X.Y` branch before the `mattermost/mattermost` Makefile is updated to reference it — for example, when the plugin release is ahead of the next platform release cycle. To avoid missing cherry-pick targets:

1. Enumerate all plugin release branches from the remote:

   ```bash
   git ls-remote --heads https://github.com/<PLUGIN_REPO>.git 'release-*'
   ```

   Filter to the `release-X.Y` pattern; parse `X` and `Y` as integers.

2. Use `MAX_MAKEFILE` from Step 2. Any plugin branch with a version **strictly greater than** `MAX_MAKEFILE` is not yet wired into the platform — include it unconditionally.

Merge these branches into the candidate set from Step 2.

## Step 4: Map to plugin release branches and filter to what exists

1. Map each resolved plugin version `vX.Y` (major.minor) to the branch name `release-X.Y` on the plugin repository.

2. Deduplicate: multiple platform releases may ship the same plugin version, and a branch added in Step 3 may overlap with a Makefile-resolved branch. Keep only one copy of each branch name.

3. Verify that branches actually exist on the plugin's remote. Branches added in Step 3 already exist by definition; for Makefile-resolved branches, re-verify they still exist (the branch may have been deleted or renamed since the Makefile was written). For each candidate branch, run:

   ```bash
   git ls-remote --heads https://github.com/<PLUGIN_REPO>.git release-X.Y
   ```

   Alternatively, if you are already in a checkout of the plugin:

   ```bash
   git ls-remote --heads origin release-X.Y
   ```

   If the command returns empty, exclude that branch from the final result.

## Output

Return the deduped list of existing plugin `release-X.Y` target branches, in ascending order. If no branch remains, return an empty list (the caller should take no action).
