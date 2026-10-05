---
name: mac-build-validator
description: Mac Build Validator subagent — validates iOS/macOS builds via SSH to a remote Mac, runs xcodebuild and reports pass/fail
---

# Mac Build Validator Agent Skill

You validate that iOS/macOS build scripts succeed on the remote Mac build machine.
You run via SSH to the Mac — no local macOS toolchain is required.

---

## Base Rules

You are running in Claude Code directly — there is no Docker container. Your
working directory is the global workspace (the root containing all repos).

**Terminal commands:** Single uninterrupted line, no backslash continuations.

---

## Configuration

`mac_build` lives **per iOS target**, inside each iOS leaf's
`agent-build.yaml`, not in the root `agent.yaml`. This lets different iOS
sub-projects (e.g. `mobile.ios` vs. `tablet.ios`) point at different
remote Macs.

For each iOS target you are validating this session:

1. Resolve the target's leaf `agent-build.yaml` via the root `agent.yaml`
   `repos:` entry — following `build:` for a leaf repo, or
   `build:` → `projects[subproject].build` for a mono-repo sub-project.
2. Read `mac_build.host` and `mac_build.workspace` from that leaf file.
3. If `mac_build.host` is empty or missing for that target, record a SKIP
   for that target only (other targets in the same session may still run).
   If every target is SKIP, write a SKIP report overall and stop.

## Step 1: Identify What to Build

Read all task files in `.workflow/tasks/` that belong to the current feature
(match by Source Item or the feature name passed in your prompt).

Collect every task file that contains a `## Manual Steps Required` section
where the described command mentions iOS, macOS, Xcode, xcrun, xcworkspace,
build-ios, or Swift binding generation.

If none exist, write `.workflow/reports/<feature>-mac-build.md` with verdict
`SKIP — no iOS manual steps found` and stop.

## Step 2: For Each iOS Target — rsync + Build

Process each affected iOS target in sequence. For each target, use the
`mac_build.host` / `mac_build.workspace` values from *that target's* leaf
`agent-build.yaml` — do not cache them across targets; a single session
may involve multiple Macs.

The worktree path for each target is its worktree on disk:
- Leaf repo: `<global_workspace>/<repo>/.workflow/worktrees/<feature-name>`
- Mono-repo sub-project: `<global_workspace>/<parent>/<subproject>/.workflow/worktrees/<feature-name>`
(Single-repo mode is unchanged: `<workflow.worktrees_dir>/<feature-name>`.)

### 2a. rsync the worktree to the Mac

```
rsync -avz --delete --exclude='.git' <worktree-path>/ <mac_build.host>:<mac_build.workspace>/<feature>/<repo-name>/
```

### 2b. Detect project type via SSH

SSH to the Mac and check what's present in the rsynced directory:

```bash
ssh <mac_build.host> "ls <mac_build.workspace>/<feature>/<repo-name>/"
```

Project type priority (check in this order):

| Condition | Type |
|-----------|------|
| `build-ios.sh` exists | **Script** — run the script |
| `Podfile` exists | **CocoaPods** — run `pod install`, then build xcworkspace |
| `*.xcworkspace` exists (no Podfile) | **Workspace** — build xcworkspace directly |
| `*.xcodeproj` exists | **Project** — build xcodeproj |

### 2c. CocoaPods install (if Podfile present)

```bash
ssh <mac_build.host> "cd <mac_build.workspace>/<feature>/<repo-name> && pod install 2>&1"
```

If `pod install` fails, record the failure and skip the xcodebuild step for this repo.

### 2d. Run build check

**Script type:**
```bash
ssh <mac_build.host> "cd <mac_build.workspace>/<feature>/<repo-name> && bash build-ios.sh 2>&1 | tail -60"
```

**CocoaPods / Workspace type:**
First, discover the available schemes:
```bash
ssh <mac_build.host> "cd <mac_build.workspace>/<feature>/<repo-name> && xcodebuild -list -workspace *.xcworkspace 2>&1 | grep -A 20 'Schemes:'"
```
Pick the first non-test scheme. Then build:
```bash
ssh <mac_build.host> "cd <mac_build.workspace>/<feature>/<repo-name> && xcodebuild build -workspace *.xcworkspace -scheme <scheme> -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO 2>&1 | tail -60"
```

**Project type:**
```bash
ssh <mac_build.host> "cd <mac_build.workspace>/<feature>/<repo-name> && xcodebuild build -project *.xcodeproj -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO 2>&1 | tail -60"
```

Capture: exit code, last 60 lines of output.

### 2e. Cleanup

Regardless of pass/fail:
```bash
ssh <mac_build.host> "rm -rf <mac_build.workspace>/<feature>/<repo-name>"
```

## Step 3: Write Report

Write `.workflow/reports/<feature>-mac-build.md`:

```markdown
# Mac Build Report: <feature-name>

**Date**: <today>
**Mac Host**: <mac_build.host>
**Overall Verdict**: PASS | FAIL

## Results

| Repo | Project Type | Verdict | Notes |
|------|-------------|---------|-------|

## Build Output (failures only)

### <repo-name>
<last 60 lines of failed build output>
```

## Step 4: Return Verdict

- **PASS** (all repos succeeded): state `Mac Build Validator: PASS` and the
  report path.

- **FAIL** (any repo failed): state `Mac Build Validator: FAIL`. Do NOT create
  rework tasks yourself — report the findings verbatim to the Coordinator.
