---
name: pnpm-version-bumper
description: Systematically bump package versions in pnpm monorepos by analyzing pnpm-lock.yaml, walking dependency trees, and finding the optimal parent package to upgrade. Use when the user asks to bump a package to meet a specific version requirement (e.g., "bump tmp to >=0.2.4", "upgrade package X to meet requirement Y", or "resolve version conflict for package Z"). Handles transitive dependencies and suggests overrides when needed.
---

# pnpm Version Bumper

## Overview

Systematically resolve package version conflicts in pnpm monorepos by analyzing the lockfile, walking the dependency tree, and finding the optimal parent package to upgrade. When walking the tree doesn't work, suggest pnpm overrides as a last resort.

## Quick Start

For a request like "Bump tmp to >=0.2.4":
1. Check pnpm-lock.yaml for all installed versions (don't rely on `pnpm why` alone)
2. Identify which versions don't meet the requirement
3. Walk up the dependency tree from problem version to workspace package
4. Find a parent package that can be upgraded to solve the problem
5. Update package.json, run `pnpm install`, and verify

## Core Workflow

Execute these steps in order, reporting progress at each step for transparency.

### 1. Install Dependencies and Identify Versions

Run `pnpm install` to ensure lockfile is up to date.

Use `grep -n "<package>@" pnpm-lock.yaml` to extract all installed versions from pnpm-lock.yaml. Do NOT rely on `pnpm why` alone as it can be misleading and may not show all versions.

**Report to user:** "Found X versions of <package> in pnpm-lock.yaml: [list versions with line numbers]"

### 2. Identify Problem Versions

For each version found, check if it satisfies the requirement. Consider semver rules:
- `>=X.Y.Z`: Version must be greater than or equal to X.Y.Z
- `^X.Y.Z`: Compatible with X.Y.Z (same major version for X>0, same minor for 0.Y.Z)
- `~X.Y.Z`: Approximately equivalent to X.Y.Z (same minor version)

For complex semver ranges, read `references/semver-guide.md` for detailed rules.

**Report to user:** "<package>@<version> [meets/does not meet] requirement <requirement>"

If all versions meet requirement, inform user and stop - no work needed.

### 3. Analyze Dependency Tree

For each problematic version, run `pnpm why -r <package>@<version>` to show the full dependency chain from workspace package down to the problem package.

**Report to user:** "Dependency chain for <package>@<version>:"

Show the full output from pnpm why, then summarize the chain:
"<workspace-package> → <parent-package>@<version> → <grandparent>@<version> → ... → <problem-package>@<version>"

### 4. Walk Up the Tree

Starting from the direct parent of the problem package, examine each package in the chain to see if upgrading it would solve the problem.

For each parent package in the chain:

**a. Check parent's current requirement:**
- Run `npm view <parent-package>@<current-version> dependencies | grep <package>`
- Extract the semver range requirement
- **Report:** "<parent-package>@<current-version> requires <package>: <semver-range>"

**b. Check if parent can be upgraded:**
- Find what the grandparent requires: `npm view <grandparent>@<version> dependencies | grep <parent>`
- List available versions: `npm view <parent-package> versions --json`
- Filter to versions within grandparent's allowed range
- Identify the latest acceptable version
- **Report:** "Latest version of <parent-package> within allowed range: <version>"

**c. Check if upgrading solves the problem:**
- Run `npm view <parent-package>@<newer-version> dependencies`
- Check if it uses a different/newer version of the problem package
- Verify the new version meets the requirement
- **Report:** "<parent-package>@<newer-version> uses <package>@<version>" (and state whether it meets requirement)

**d. If solution found:**
- **Report:** "Solution found! Upgrading <parent-package> from <old-version> to <new-version> will resolve the issue."
- Find which workspace package depends on this parent
- Update that workspace package's package.json to require the new version
- Run `pnpm install`
- Proceed to verification (step 5)
- Stop - problem solved

**e. If no solution at this level:**
- **Report:** "No solution found by upgrading <parent-package>, checking next parent in chain..."
- Continue to the next parent up the chain

### 5. Verify Resolution

After making changes, run these verification steps and report each result:

**a.** Run `pnpm why -r <package>@<old-version>` - should return empty
- **Report:** "✓ <package>@<old-version> no longer in dependency tree"

**b.** Run `grep "<package>@<old-version>" pnpm-lock.yaml` - should return empty
- **Report:** "✓ <package>@<old-version> not found in pnpm-lock.yaml"

**c.** Run `grep "<package>@" pnpm-lock.yaml` - confirm only acceptable versions remain
- **Report:** "✓ Only <package>@<version> remains (meets requirement <requirement>)"

**d.** Run `pnpm why -r <package>` - show final dependency tree
- **Report:** "Final dependency tree:" [show full output]

**Final summary:** "Successfully bumped <package> by upgrading <parent-package> from <old-version> to <new-version>. All versions now meet requirement <requirement>."

**Verification Failed?** It's common that there will be other branch of the dependency tree still using the old version. If so, return to step 4 and continue walking up the tree to find another parent to upgrade.

### 6. Handle Edge Cases

If walking up the tree exhausted all parents without finding a solution:

**a. Check if problem package is a direct dependency:**
- Look at the workspace package's package.json
- If it's a direct dependency: Can update it directly in package.json
- If it's a peer dependency: Consider if breaking change is acceptable
- **Report findings and recommend action**

**b. If no parent can be upgraded (all are already at latest versions):**
- Read `references/overrides-guide.md` for detailed guidance
- Explain that pnpm overrides are the last resort
- Suggest specific override syntax: `"<parent>><package>": "<version>"`
- **Explain risks:**
  - May introduce breaking changes if package API changed
  - Bypasses normal dependency resolution
  - Requires manual maintenance and testing
- **Report:** "No parent can be upgraded. Recommend using pnpm override: [show exact syntax]. This requires thorough testing."
- Ask user for confirmation before proceeding with override

**c. If upgrade would require breaking changes:**
- Report clearly: "Upgrading <package> to meet requirement would require upgrading <parent> to version X.0.0, which is a major version change that may break compatibility."
- Explain what the breaking change entails (if apparent from version jump)
- Ask user: "Would you like to proceed with this major version upgrade, or explore alternatives like overrides?"

## Decision Tree

```
User requests: "Bump <package> to meet <requirement>"
│
├─ Step 1: Find all versions in pnpm-lock.yaml
│  └─ Report versions found
│
├─ Step 2: Check which versions don't meet requirement
│  ├─ All versions OK? → Stop, inform user
│  └─ Some versions fail? → Continue
│
├─ Step 3: Get dependency tree for problem versions
│  └─ Report chain: workspace → ... → problem package
│
├─ Step 4: Walk up tree, check each parent
│  ├─ Can parent be upgraded to fix? → YES
│  │  ├─ Update workspace package.json
│  │  ├─ Run pnpm install
│  │  └─ Go to Step 5 (Verify)
│  │
│  └─ Can't be upgraded? → Continue to next parent
│      ├─ More parents to check? → Loop to next parent
│      └─ No more parents? → Go to Step 6 (Edge Cases)
│
├─ Step 5: Verify solution worked
│  ├─ Old version gone?
│  ├─ Only good versions remain?
│  ├─ Verify success? -> YES
│  │  └─ Report success to user
│  └─ Verification failed? → NO
|     └─ Return to Step 4
│
└─ Step 6: Handle edge cases
   ├─ Direct dependency? → Update directly
   ├─ Need override? → Suggest with risks, ask confirmation
   └─ Breaking change required? → Explain, ask user how to proceed
```

## Bundled References

This skill includes two reference files that are loaded only when needed:

### references/semver-guide.md
Load when you need to:
- Understand complex semver range syntax
- Manually check if a version satisfies a requirement
- Explain why a version doesn't meet a requirement
- Handle special cases with 0.x versions

### references/overrides-guide.md
Load when:
- Walking up the tree found no solution
- User asks about forcing a specific package version
- You need to explain pnpm overrides syntax and risks
- Recommending overrides as last resort

## Best Practices

1. **Always check pnpm-lock.yaml directly** - `pnpm why` can be misleading
2. **Report progress at each step** - User should see what you're discovering
3. **Try walking the tree first** - Overrides are last resort
4. **Be specific with overrides** - Use `parent>package` syntax when possible
5. **Explain risks clearly** - Breaking changes, testing requirements, maintenance burden
6. **Verify thoroughly** - Check lockfile, dependency tree, and test if possible
