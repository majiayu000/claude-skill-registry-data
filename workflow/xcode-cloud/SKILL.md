---
name: xcode-cloud
description: Xcode Cloud CI/CD configuration, workflows, custom scripts, testing, deployment, and optimization. Use when setting up or troubleshooting Xcode Cloud pipelines.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion]
---

# Xcode Cloud CI/CD

Guides configuration and optimization of Xcode Cloud workflows including build automation, testing, TestFlight distribution, App Store deployment, and custom scripts.

## When This Skill Activates

Use this skill when the user:
- Asks to "set up Xcode Cloud" or "configure CI/CD"
- Mentions "Xcode Cloud workflows" or "build pipelines"
- Wants to automate TestFlight or App Store distribution
- Needs custom build scripts (`ci_scripts/`)
- Has Xcode Cloud build failures or signing issues
- Wants to optimize build times or compute hours
- Asks about test plans in CI/CD
- Mentions "cloud signing" or "managed certificates"
- Wants to compare Xcode Cloud with other CI/CD (GitHub Actions, Bitrise)

## Pre-Configuration Checks

### 1. Project Detection

- [ ] Check for existing Xcode project
- [ ] Determine project type (app, framework, multi-platform)
- [ ] Check for existing CI/CD configuration
- [ ] Verify source control setup (Git required)

```
Glob: **/*.xcodeproj, **/*.xcworkspace, **/ci_scripts/*.sh
Grep: "CI" or "xcodebuild" or "ci_post_clone"
```

### 2. Existing CI/CD Detection

Search for other CI/CD configurations:

```
Glob: **/.github/workflows/*.yml, **/bitrise.yml, **/.circleci/config.yml, **/fastlane/Fastfile
```

If found, ask user:
- Replace with Xcode Cloud?
- Run alongside existing CI/CD?

### 3. Signing Requirements

```
Glob: **/*.entitlements, **/*.xcodeproj/project.pbxproj
Grep: "CODE_SIGN_STYLE" or "PROVISIONING_PROFILE" or "DEVELOPMENT_TEAM"
```

## Configuration Questions

Ask user via AskUserQuestion:

1. **What do you want to automate?**
   - Build + Test on every PR
   - TestFlight distribution on merge to main
   - App Store submission on tag
   - All of the above

2. **What triggers should start builds?**
   - Push to branch (specify branch pattern)
   - Pull request (opened/updated)
   - Tag creation (version tags)
   - Schedule (nightly/weekly)

3. **What tests should run?**
   - Unit tests only
   - Unit + UI tests
   - Unit + UI + performance tests
   - No tests (build only)

4. **What platforms do you target?**
   - iOS only
   - iOS + macOS
   - iOS + watchOS
   - All Apple platforms

## Workflow Configuration

### Workflows are configured in Xcode

Unlike other CI/CD systems, Xcode Cloud workflows are configured in Xcode's UI or via the App Store Connect API — not YAML files. However, custom scripts provide programmatic control.

### Workflow Components

1. **Start Conditions** — What triggers the workflow
2. **Environment** — Xcode version, macOS version
3. **Build Actions** — Build, test, analyze, archive
4. **Post-Actions** — TestFlight, App Store, notifications

### Custom Scripts (ci_scripts/)

The primary way to customize Xcode Cloud behavior:

```
ci_scripts/
├── ci_post_clone.sh         # After repo clone (install deps)
├── ci_pre_xcodebuild.sh     # Before build starts
└── ci_post_xcodebuild.sh    # After build completes
```

**Execution order:**
1. `ci_post_clone.sh` — Install tools, resolve dependencies
2. `ci_pre_xcodebuild.sh` — Pre-build setup, code generation
3. Build/Test/Archive runs
4. `ci_post_xcodebuild.sh` — Post-build actions, notifications

## Generation Process

### Step 1: Create ci_scripts Directory

```bash
mkdir -p ci_scripts
```

### Step 2: ci_post_clone.sh

Install dependencies and tools after repository clone.

### Step 3: ci_pre_xcodebuild.sh

Pre-build code generation, environment setup.

### Step 4: ci_post_xcodebuild.sh

Post-build notifications, artifact uploads.

### Step 5: Xcode Workflow Setup Guide

Provide step-by-step instructions for configuring the workflow in Xcode.

## Key Environment Variables

Xcode Cloud provides these automatically:

| Variable | Description |
|----------|-------------|
| `CI` | Always `TRUE` in Xcode Cloud |
| `CI_XCODEBUILD_ACTION` | `build`, `test`, `archive` |
| `CI_WORKFLOW` | Workflow name |
| `CI_BRANCH` | Branch being built |
| `CI_TAG` | Tag being built (if triggered by tag) |
| `CI_COMMIT` | Full commit SHA |
| `CI_BUILD_NUMBER` | Auto-incrementing build number |
| `CI_PRODUCT` | Product name |
| `CI_XCODE_PROJECT` | Project file path |
| `CI_XCODE_SCHEME` | Scheme being built |
| `CI_DERIVED_DATA_PATH` | Derived data location |
| `CI_ARCHIVE_PATH` | Archive output path |
| `CI_RESULT_BUNDLE_PATH` | Test result bundle path |
| `CI_PULL_REQUEST_NUMBER` | PR number (if PR trigger) |

## Output Format

### Files Created

```
project/
├── ci_scripts/
│   ├── ci_post_clone.sh       # Dependency installation
│   ├── ci_pre_xcodebuild.sh   # Pre-build setup
│   └── ci_post_xcodebuild.sh  # Post-build actions
```

### Xcode Configuration Steps

1. Open project in Xcode
2. Product → Xcode Cloud → Create Workflow
3. Configure start conditions, environment, actions
4. Set up TestFlight/App Store post-actions

## Pricing Tiers

| Tier | Hours/Month | Cost |
|------|-------------|------|
| Free | 25 | $0 |
| Tier 1 | 100 | ~$15/mo (via Apple Developer subscription) |
| Tier 2 | 250 | ~$50/mo |
| Tier 3 | 1,000 | ~$200/mo |
| Enterprise | 10,000 | ~$4,000/mo |

## References

- **workflow-patterns.md** — Workflow configuration, start conditions, actions
- **scripts-reference.md** — Complete ci_scripts/ patterns and environment variables
- **testing-patterns.md** — Test plans, parallel testing, UI tests in CI
- **deployment-patterns.md** — TestFlight, App Store, notarization
- **troubleshooting.md** — Common errors, signing, SPM, timeouts
- **optimization.md** — Build time, compute hours, caching
- [Xcode Cloud Documentation](https://developer.apple.com/documentation/xcode/xcode-cloud)
- [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
