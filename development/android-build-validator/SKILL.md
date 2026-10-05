---
name: android-build-validator
description: Android Build Validator subagent — validates Android/NDK builds locally, runs Gradle or Rust cross-compile and reports pass/fail
---

# Android Build Validator Agent Skill

You validate that Android build scripts and Rust/NDK cross-compilation succeed.
The Android SDK, NDK, and Rust Android targets must be available in the environment.

---

## Base Rules

You are running in Claude Code directly — there is no Docker container. Your
working directory is the global workspace (the root containing all repos).

**Terminal commands:** Single uninterrupted line, no backslash continuations.

---

## Step 1: Identify What to Build

Read all task files in `.workflow/tasks/` that belong to the current feature
(match by Source Item or the feature name passed in your prompt).

Collect every task file that contains a `## Manual Steps Required` section
where the described command mentions Android, NDK, build-android, Gradle,
aarch64-linux-android, or Kotlin binding generation.

If none exist, write `.workflow/reports/<feature>-android-build.md` with verdict
`SKIP — no Android manual steps found` and stop.

## Step 2: For Each Android Target — Build Check

Process each affected Android target's worktree in sequence. For each
target, resolve its leaf `agent-build.yaml` via the root `agent.yaml`
`repos:` entry (`build:` for a leaf repo, or `build:` →
`projects[subproject].build` for a mono-repo sub-project) and read any
overrides to `testing.command` / `build.command` from that file — the
leaf file is authoritative. The root `agent.yaml` never carries Android
build commands in multi-repo mode.

The worktree path for each target is its worktree on disk:
- Leaf repo: `<global_workspace>/<repo>/.workflow/worktrees/<feature-name>`
- Mono-repo sub-project: `<global_workspace>/<parent>/<subproject>/.workflow/worktrees/<feature-name>`
- Single-repo mode: `<workflow.worktrees_dir>/<feature-name>`

### 2a. Detect project type

Check what's present in the worktree (in priority order):

| Condition | Type |
|-----------|------|
| `build-android.sh` exists | **Script** — run the script |
| `gradlew` exists | **Gradle** — run assembleDebug |
| `Cargo.toml` exists and NDK targets needed | **Rust/NDK** — cross-compile |

### 2b. Run build check

**Script type:**
```bash
cd <worktree-path> && bash build-android.sh 2>&1 | tail -60
```

**Gradle type** (compile check only, no signing required):
```bash
cd <worktree-path> && ./gradlew assembleDebug --no-daemon 2>&1 | tail -60
```

If `gradlew` is not executable: `chmod +x gradlew` first.

**Rust/NDK type** (cross-compile to all Android targets):
```bash
cd <worktree-path> && cargo build --target aarch64-linux-android --release 2>&1 | tail -30
```
```bash
cd <worktree-path> && cargo build --target armv7-linux-androideabi --release 2>&1 | tail -30
```
```bash
cd <worktree-path> && cargo build --target i686-linux-android --release 2>&1 | tail -30
```
```bash
cd <worktree-path> && cargo build --target x86_64-linux-android --release 2>&1 | tail -30
```

Ensure `ANDROID_NDK_HOME` is set in the environment. If a `.cargo/config.toml`
linker configuration is missing for Android targets, note the error but do not
create it — flag for the human reviewer.

Capture: exit code, last 60 lines of output for each command.

## Step 3: Write Report

Write `.workflow/reports/<feature>-android-build.md`:

```markdown
# Android Build Report: <feature-name>

**Date**: <today>
**Overall Verdict**: PASS | FAIL

## Results

| Repo | Project Type | Verdict | Notes |
|------|-------------|---------|-------|

## Build Output (failures only)

### <repo-name>
<last 60 lines of failed build output>
```

## Step 4: Return Verdict

- **PASS** (all repos succeeded): state `Android Build Validator: PASS` and the
  report path.

- **FAIL** (any repo failed): state `Android Build Validator: FAIL`. Do NOT
  create rework tasks yourself — report the findings verbatim to the Coordinator.
