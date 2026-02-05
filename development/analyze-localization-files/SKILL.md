---
name: analyze_localization_files
description: Analyze differences between English master i18n file and target language files using the project's check-i18n tool. Builds task manifests with missing keys and English values for translation work.
allowed-tools: Bash, Read
---

# Analyze Localization Files

Analyze the differences between the English master i18n file and all target language files using the project's existing `check-i18n` tool to build translation task manifests.

## Inputs

None - this skill uses the project's existing `pnpm run check-i18n` script.

## Output

Return a dictionary mapping language code to task manifest:

```json
{
  "ar-SA": {
    "file_path": "src/assets/i18n/ar-SA.json",
    "language_code": "ar-SA",
    "language_name": "Arabic (Saudi Arabia)",
    "missing_keys": [
      ["about.trademarks", "All product names, logos, and brands are property of their respective owners..."]
    ],
    "extra_keys": [],
    "total_missing": 1
  },
  "bn-BD": {
    "file_path": "src/assets/i18n/bn-BD.json",
    "language_code": "bn-BD",
    "language_name": "Bengali (Bangladesh)",
    "missing_keys": [
      ["about.trademarks", "All product names, logos, and brands..."],
      ["admin.groups.viewMembersTooltip", "View and manage group members"],
      ["admin.webhooks.addDialog.secret", "HMAC Secret"],
      ["admin.webhooks.addDialog.secretHint", "HMAC secret for signing payloads (auto-generated if empty)"],
      ["admin.webhooks.addDialog.secretPlaceholder", "Leave empty to auto-generate"]
    ],
    "extra_keys": [],
    "total_missing": 5
  }
}
```

## Process

### Step 1: Run check-i18n Script

Execute the project's i18n validation script:

```bash
pnpm run check-i18n
```

This script:
- Compares all language files against `en-US.json`
- Reports missing keys in each language file
- Reports extra keys (keys in target but not in master)
- Automatically sorts JSON files
- Creates backups in `/tmp`

### Step 2: Parse Script Output

The script output follows this pattern:

```
=== Comparing src/assets/i18n/en-US.json with src/assets/i18n/ar-SA.json ===

Keys present in src/assets/i18n/en-US.json but missing in src/assets/i18n/ar-SA.json:
about.trademarks

No keys missing in src/assets/i18n/en-US.json
Backup and sorted files saved to /tmp/...

=== Comparing src/assets/i18n/en-US.json with src/assets/i18n/bn-BD.json ===

Keys present in src/assets/i18n/en-US.json but missing in src/assets/i18n/bn-BD.json:
about.trademarks
admin.groups.viewMembersTooltip
admin.webhooks.addDialog.secret
admin.webhooks.addDialog.secretHint
admin.webhooks.addDialog.secretPlaceholder

No keys missing in src/assets/i18n/en-US.json
...
```

**Parsing logic:**

1. **Identify language sections**: Look for pattern `=== Comparing ... with src/assets/i18n/XX-YY.json ===`
2. **Extract language code**: Parse `XX-YY` from the file path (e.g., `ar-SA`, `bn-BD`, `zh-CN`)
3. **Extract missing keys**: Collect lines between "Keys present in en-US.json but missing in..." and the next section marker or "No keys missing"
4. **Detect extra keys**: If output shows "Keys present in [target] but missing in en-US.json", collect those keys

### Step 3: Read English Values

Load and parse `src/assets/i18n/en-US.json` to retrieve the English values for each missing key.

**Key lookup logic:**

For a dot-notation key like `admin.webhooks.addDialog.secret`:
1. Split by `.` to get path: `["admin", "webhooks", "addDialog", "secret"]`
2. Traverse the JSON object following the path
3. Return the leaf value

### Step 4: Map Language Codes to Names

Use this mapping for `language_name`:

| Code | Language Name |
|------|---------------|
| ar-SA | Arabic (Saudi Arabia) |
| bn-BD | Bengali (Bangladesh) |
| de-DE | German (Germany) |
| es-ES | Spanish (Spain) |
| fr-FR | French (France) |
| he-IL | Hebrew (Israel) |
| hi-IN | Hindi (India) |
| id-ID | Indonesian (Indonesia) |
| ja-JP | Japanese (Japan) |
| ko-KR | Korean (South Korea) |
| pt-BR | Portuguese (Brazil) |
| ru-RU | Russian (Russia) |
| th-TH | Thai (Thailand) |
| ur-PK | Urdu (Pakistan) |
| zh-CN | Chinese (Simplified, China) |

### Step 5: Build Task Manifests

For each language, construct the task manifest:

```json
{
  "file_path": "src/assets/i18n/XX-YY.json",
  "language_code": "XX-YY",
  "language_name": "Language Name",
  "missing_keys": [
    ["key.path", "English value"],
    ["another.key", "Another English value"]
  ],
  "extra_keys": ["obsolete.key1", "obsolete.key2"],
  "total_missing": 2
}
```

## Output Format Details

### Task Manifest Fields

| Field | Type | Description |
|-------|------|-------------|
| `file_path` | string | Full path to the language file |
| `language_code` | string | ISO language-country code (e.g., `es-ES`) |
| `language_name` | string | Human-readable language name with region |
| `missing_keys` | array | List of `[key, english_value]` tuples |
| `extra_keys` | array | List of key strings present in target but not in master |
| `total_missing` | number | Count of missing keys |

### missing_keys Entry

Each entry is a tuple (2-element array):
- Element 0: Dot-notation key path (string)
- Element 1: English value from en-US.json (string)

```json
["admin.webhooks.addDialog.secret", "HMAC Secret"]
```

## Example Output

```json
{
  "ar-SA": {
    "file_path": "src/assets/i18n/ar-SA.json",
    "language_code": "ar-SA",
    "language_name": "Arabic (Saudi Arabia)",
    "missing_keys": [
      ["about.trademarks", "All product names, logos, and brands are property of their respective owners. All company, product, and service names used in this application are for identification purposes only. Use of these names, logos, and brands does not imply endorsement."]
    ],
    "extra_keys": [],
    "total_missing": 1
  },
  "de-DE": {
    "file_path": "src/assets/i18n/de-DE.json",
    "language_code": "de-DE",
    "language_name": "German (Germany)",
    "missing_keys": [],
    "extra_keys": [],
    "total_missing": 0
  },
  "fr-FR": {
    "file_path": "src/assets/i18n/fr-FR.json",
    "language_code": "fr-FR",
    "language_name": "French (France)",
    "missing_keys": [
      ["admin.webhooks.addDialog.secret", "HMAC Secret"],
      ["admin.webhooks.addDialog.secretHint", "HMAC secret for signing payloads (auto-generated if empty)"]
    ],
    "extra_keys": [],
    "total_missing": 2
  }
}
```

## Notes

1. **Script side effects**: The `check-i18n` script automatically sorts JSON files and creates backups in `/tmp`. This is expected behavior.

2. **Empty results**: Languages with no missing keys will have `missing_keys: []` and `total_missing: 0`.

3. **Extra keys**: These indicate potentially obsolete translations that exist in the target file but not in the English master.

4. **Key value lookup**: If a key path doesn't exist in en-US.json (shouldn't happen), use an empty string or note the error.

5. **Nested keys**: The English value lookup must handle deeply nested objects. A key like `a.b.c.d.e` requires traversing 5 levels.

6. **Template variables**: English values may contain template variables like `{{name}}` or `{{count}}`. These should be preserved exactly in the output.
