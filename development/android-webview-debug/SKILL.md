---
name: android-webview-debug
version: "1.0.0"
user-invocable: true
description: "Unified WebView remote debugging toggle for Android projects. `android-webview-debug-enable` sets all `setWebContentsDebuggingEnabled` calls to `true` and records modified locations with their original content; `android-webview-debug-revert` restores from the record, listing any mismatched entries at the end for manual confirmation. Triggers: 「开启 WebView 调试」「恢复 WebView 调试」 / android-webview-debug-enable, android-webview-debug-revert. Suitable for Android projects that need to uniformly enable or restore WebView debugging."
---

# Android WebView Debug Toggle

## Triggers

- 「开启 WebView 调试」 / **android-webview-debug-enable**: Change all `setWebContentsDebuggingEnabled` calls in the project to `true`, and **record** modified locations with their original content for later revert.
- 「恢复 WebView 调试」 / **android-webview-debug-revert**: **Restore** previously modified locations from the record; entries that don't match the record are **not auto-reverted** — they are listed at the end for user confirmation.

## State File Convention

- **Path**: `.android-webview-debug-state.json` in the project/workspace **root directory**.
- **Creation timing**: Only created or overwritten when **android-webview-debug-enable** runs; revert only reads (can be deleted or archived after restore is complete).
- **Format**:

```json
{
  "version": 1,
  "createdAt": "ISO8601",
  "projectRoot": "/absolute/path/to/project",
  "entries": [
    {
      "file": "app/src/main/java/.../CoreWebView.kt",
      "line": 42,
      "original": "setWebContentsDebuggingEnabled(AppContext.isDebug())",
      "replaced": "setWebContentsDebuggingEnabled(true)"
    }
  ]
}
```

- **Note**: Only entries **actually changed in this enable session** are recorded (calls already set to `true` are not included). Recommend adding `.android-webview-debug-state.json` to `.gitignore` to avoid accidental commits.

---

## android-webview-debug-enable Flow

1. **Search**: Use grep or codebase search to find all `setWebContentsDebuggingEnabled` occurrences (including commented lines), list all locations.
2. **Classify**: Mark each location as "already true", "conditional or other expression", or "commented out".
3. **Optional confirmation**: If user input is needed, present 1–2 quick choices (e.g., "Change all to true?" "Also modify commented-out calls?"). User can answer briefly like "1A 2B".
4. **Existing state**: If `.android-webview-debug-state.json` already exists in the project root, first prompt: "An enable record already exists. Overwrite and continue?" Wait for user confirmation before overwriting.
5. **Write state file**: **Before making any code replacements**, generate `entries` for items about to be changed and write `.android-webview-debug-state.json` (path: project root).
6. **Execute replacements**: Change "conditional or other expression" calls to `setWebContentsDebuggingEnabled(true)`. **Do not modify commented-out calls by default**, unless the user explicitly says "also change commented ones" or "uncomment them".
7. **Summary**: Briefly list modified files and entry count.

---

## android-webview-debug-revert Flow

1. **Read state file**: Read `.android-webview-debug-state.json` from the project root. If not found, prompt: "No enable record found, cannot revert" and exit.
2. **Iterate entries**:
   - For each entry: read the corresponding file/line and compare with `replaced` (or check if it contains `setWebContentsDebuggingEnabled(true)`).
   - **Match**: Replace the line with `original` (restore pre-modification content).
   - **Mismatch**: Do not auto-revert; add to the "mismatched" list (record file, line, current line summary).
3. **Complete all restorable items first**: Only apply replacements for entries where the current line matches the record.
4. **Final prompt and manual confirmation**: If there are mismatched entries, output the list at the end: "The following N entries don't match the enable record (may have been manually modified). Confirm whether to restore per the record or skip." Restore or skip each entry based on user choice.
5. **Summary**: Report number of restored entries; if all restored, prompt: "You can now delete .android-webview-debug-state.json or add it to .gitignore."

---

## Default Rules

- **enable**: **Does not modify** commented-out `setWebContentsDebuggingEnabled` calls by default; user can override with a single phrase (e.g., "also change commented ones").
- **revert**: Only restores entries recorded in the state file; mismatched entries are **not auto-reverted** — always listed at the end for manual confirmation.
- **State file**: Only one copy in the project root; enable overwrites, revert only reads.

---

## Verification Checklist

- After **enable**: All non-commented `setWebContentsDebuggingEnabled` calls in the project should be `true`, and `.android-webview-debug-state.json` should exist in the root with `entries` matching this session's modifications.
- After **revert**: Restored lines should match the `original` in the state file; mismatched entries should be listed and processed per user confirmation.
