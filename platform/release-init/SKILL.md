---
name: release-init
description: Detect project type and generate a tailored project-level /release skill. Run once per project to set up releasing.
tags: [release, init, scaffold, meta]
---

# Release Init

## Protocol

### 1. Check for existing project skill

Look for `.claude/skills/release/SKILL.md` in the repo root.

If it exists, ask:
> Project release skill already exists. Overwrite with fresh detection? (y/n)

Stop if user declines.

### 2. Detect project type

Scan the working directory. First match wins:

| Marker | Type |
|---|---|
| `ProjectSettings/ProjectSettings.asset` (search recursively) | `unity` |
| `package.json` + `src-tauri/` directory | `tauri` |
| `package.json` | `node` |
| `*.xcodeproj` or `*.xcworkspace` (in root) | `ios-native` |
| `build.gradle` or `build.gradle.kts` (in root) | `android-native` |
| None of the above | `generic` |

### 3. Discover version files and current values

Read current version values from the detected files:

**unity:**
- Find `ProjectSettings/ProjectSettings.asset` (may be nested, e.g. `ProjectName/ProjectSettings/`)
- Read: `bundleVersion` (display version), `AndroidBundleVersionCode`, `buildNumber.iPhone`
- Report all three values

**tauri:**
- `package.json` → `version`
- `src-tauri/tauri.conf.json` → `version`
- `src-tauri/Cargo.toml` → `version`

**node:**
- `package.json` → `version`

**ios-native:**
- Find `Info.plist` → `CFBundleShortVersionString`, `CFBundleVersion`

**android-native:**
- `build.gradle` or `build.gradle.kts` → `versionName`, `versionCode`

**generic:**
- Ask user: "Where does your version live? (file path and field name)"

### 4. Detect platforms and recommend tagging approach

Determine if multi-platform based on project type and evidence:

| Type | Signal | Recommendation |
|---|---|---|
| `unity` | Has both Android + iOS build settings in ProjectSettings | Multi-platform: `android`, `ios` |
| `unity` | Only one platform target | Single platform, no platform tags |
| `tauri` | Desktop app | Single artifact, no platform tags |
| `node` | Web app / server | Single deploy, no platform tags |
| `ios-native` | iOS only | Single platform, no platform tags |
| `android-native` | Android only | Single platform, no platform tags |

Present the recommendation WITH reasoning.

Wait for confirmation. User may correct platforms (e.g., "also shipping to Steam") or remove some.

### 5. Handle greenfield / untracked repos

Check `git tag -l "v*"`:

- **Tags exist** — note the latest tag, continue.
- **No tags exist** — ask:
  > No version tags found in git. Is this a first release, or has this project shipped before without tags?

  - **First release** — suggest starting at `1.0.0` (user can override).
  - **Previously shipped** — ask for current live versions:
    > What are the current live versions? (e.g., "Android 4.0.5 build 41, iOS 1.2.9 build 12")

    Create a baseline tag on the current commit so future releases have a reference point. For multi-platform, also create platform baseline tags.

### 6. Present full summary for confirmation

Show everything in one block:

```
Project type: unity
Version files:
  - PuzzleSnake/ProjectSettings/ProjectSettings.asset
    - bundleVersion (display version): 4.0.5
    - AndroidBundleVersionCode: 40
    - buildNumber.iPhone: 1

Platforms: android, ios
Tagging: v{version} + v{version}-android, v{version}-ios

Qualification: clean git, on master

Git baseline: v4.0.5 (to be created)

Generate .claude/skills/release/SKILL.md with these settings?
```

Wait for user approval.

### 7. Generate the project-level skill

Read `assets/template.md` (sibling to this SKILL.md) and fill all `{{placeholders}}` per the map in step 8 below, then write to `.claude/skills/release/SKILL.md`.

### 8. Fill the template

Replace all `{{placeholders}}` with detected values:

- `{{project_type}}` — detected type
- `{{version_files_list}}` — bullet list of file paths and field names with current values
- `{{platforms_or_none}}` — comma-separated platform list, or `none (single-platform)`
- `{{main_branch}}` — from `git branch --show-current` or detect default
- `{{bump_instructions}}` — project-specific Edit instructions for each version file. Format: one Edit call per file showing the old version string and new version string. Example:
  ```
  Edit `package.json`: change `"version": "1.2.3"` → `"version": "{new_version}"`
  Edit `src-tauri/tauri.conf.json`: change `"version": "1.2.3"` → `"version": "{new_version}"`
  ```
- `{{version_file_paths}}` — space-separated paths for `git add`
- `{{platform_build_number_instructions}}` — how to read each platform's build number. Format: one read instruction per platform file. Example:
  ```
  Read `ProjectSettings/ProjectSettings.asset` → `AndroidBundleVersionCode` for android; `buildNumber.iPhone` for ios.
  ```
- Remove the `{{#if platforms}}...{{/if}}` block entirely if single-platform

The generated skill should be clean markdown with no template syntax remaining.

### 9. Commit

```bash
git add .claude/skills/release/SKILL.md
git commit -m "chore: add project release skill"
```

### 10. Report

> Project release skill generated at `.claude/skills/release/SKILL.md`.
> From now on, just run `/release`.

Then offer to push this commit: **"Push now? (y / skip)"** — push only on yes, skip by default if silent.

## Rules

- Push only on explicit confirmation — offer after the commit, never force, never unannounced.
- Always confirm detection results before generating.
- Surface ambiguous detection with the candidate interpretations before proceeding.
- Verify all `{{placeholders}}` are replaced before writing the file.
