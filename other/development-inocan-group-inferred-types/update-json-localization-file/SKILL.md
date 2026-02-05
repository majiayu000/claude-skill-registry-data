---
name: update_json_localization_file
description: Update a JSON localization file with additions and deletions while preserving formatting. Use when modifying i18n translation files or syncing localization keys.
allowed-tools: Read, Write, Bash
---

# Update JSON Localization File

Safely update a JSON localization file by adding, updating, or removing keys while preserving proper formatting.

## Inputs

- **file_path**: Path to the JSON file to update
- **additions**: Dictionary of `{key: value}` pairs to add or update
- **deletions**: List of keys to remove
- **preserve_formatting**: Boolean (default: `true`) - maintain existing key order vs. sort alphabetically

## Output

Return a summary object:

```json
{
  "file_path": "src/assets/i18n/es-ES.json",
  "keys_added": 5,
  "keys_updated": 3,
  "keys_deleted": 2,
  "total_keys": 450
}
```

## Process

### Step 1: Read Current File

Read the existing file content. If the file doesn't exist, start with an empty object `{}`.

```
file_path: src/assets/i18n/es-ES.json
```

Handle errors gracefully:
- File not found → Create new file
- Permission denied → Report error
- Invalid JSON → Report error with line number if possible

### Step 2: Parse JSON

Parse the JSON content while preserving structure:
- Maintain nested object hierarchy
- Track existing keys for add vs. update distinction

### Step 3: Apply Deletions

For each key in the deletions list:
- Support dot notation for nested keys: `"about.title"` → delete `json.about.title`
- If key doesn't exist, skip silently (idempotent)
- If deleting a key leaves an empty parent object, keep the empty object

```
deletions: ["obsolete.key1", "deprecated.feature"]
```

**Deletion logic for nested keys:**

```
Key: "about.opensource.paragraph3"

Before:
{
  "about": {
    "opensource": {
      "paragraph1": "...",
      "paragraph2": "...",
      "paragraph3": "..."
    }
  }
}

After:
{
  "about": {
    "opensource": {
      "paragraph1": "...",
      "paragraph2": "..."
    }
  }
}
```

### Step 4: Apply Additions

For each key-value pair in additions:
- Support dot notation: `"about.newKey"` → `json.about.newKey = value`
- If key exists: update value, count as "updated"
- If key is new: add it, count as "added"
- Create intermediate objects as needed for nested keys

```
additions: {
  "about.title": "Acerca de TMI",
  "newSection.newKey": "New Value"
}
```

**Addition logic for nested keys:**

```
Key: "newSection.subSection.key"
Value: "Hello"

Before:
{
  "existingKey": "..."
}

After:
{
  "existingKey": "...",
  "newSection": {
    "subSection": {
      "key": "Hello"
    }
  }
}
```

### Step 5: Sort Keys (Optional)

If `preserve_formatting` is `false`, sort all keys alphabetically at each level of nesting.

**Sorting rules:**
- Case-sensitive alphabetical sort
- Sort recursively at every nesting level
- Numbers sort before letters in ASCII order

If `preserve_formatting` is `true`:
- Keep existing keys in their original order
- Add new keys at the end of their respective objects (or in sorted position among new keys)

### Step 6: Write File

Write the updated JSON back to the file with proper formatting.

**Formatting requirements:**
- 2-space indentation
- UTF-8 encoding
- Final newline at end of file
- No trailing whitespace on lines
- Unix line endings (`\n`)

**Safe write process:**

1. Create backup: `{file_path}.bak`
2. Write to temporary file: `{file_path}.tmp`
3. Rename temporary file to target (atomic operation)
4. Preserve original file permissions

```bash
# Conceptual process
cp file.json file.json.bak
write_json > file.json.tmp
mv file.json.tmp file.json
```

## Error Handling

### File Errors

| Error | Behavior |
|-------|----------|
| File not found | Create new file with additions only |
| Permission denied | Return error, do not modify |
| Disk full | Return error, backup preserved |
| Invalid JSON | Return error with details |

### Key Errors

| Error | Behavior |
|-------|----------|
| Delete non-existent key | Skip silently (idempotent) |
| Invalid key format | Return error |
| Key collision (add + delete same) | Delete wins, then add |

## Examples

### Add New Translations

```
Input:
  file_path: "src/assets/i18n/es-ES.json"
  additions: {
    "common.save": "Guardar",
    "common.cancel": "Cancelar",
    "errors.network": "Error de red"
  }
  deletions: []

Output:
  {
    "file_path": "src/assets/i18n/es-ES.json",
    "keys_added": 3,
    "keys_updated": 0,
    "keys_deleted": 0,
    "total_keys": 453
  }
```

### Update Existing Translation

```
Input:
  file_path: "src/assets/i18n/fr-FR.json"
  additions: {
    "common.save": "Sauvegarder"
  }
  deletions: []

Output:
  {
    "file_path": "src/assets/i18n/fr-FR.json",
    "keys_added": 0,
    "keys_updated": 1,
    "keys_deleted": 0,
    "total_keys": 450
  }
```

### Remove Obsolete Keys

```
Input:
  file_path: "src/assets/i18n/de-DE.json"
  additions: {}
  deletions: ["deprecated.oldFeature", "legacy.button"]

Output:
  {
    "file_path": "src/assets/i18n/de-DE.json",
    "keys_added": 0,
    "keys_updated": 0,
    "keys_deleted": 2,
    "total_keys": 448
  }
```

### Mixed Operations

```
Input:
  file_path: "src/assets/i18n/ja-JP.json"
  additions: {
    "new.feature.title": "新機能",
    "common.ok": "はい"
  }
  deletions: ["old.feature.title"]

Output:
  {
    "file_path": "src/assets/i18n/ja-JP.json",
    "keys_added": 1,
    "keys_updated": 1,
    "keys_deleted": 1,
    "total_keys": 450
  }
```

### Create New File

```
Input:
  file_path: "src/assets/i18n/new-LANG.json"
  additions: {
    "app.title": "Application Title",
    "app.description": "Description"
  }
  deletions: []

Output:
  {
    "file_path": "src/assets/i18n/new-LANG.json",
    "keys_added": 2,
    "keys_updated": 0,
    "keys_deleted": 0,
    "total_keys": 2
  }
```

## Implementation Notes

1. **Atomic writes**: Always use temp file + rename to prevent corruption on failure.

2. **Backup retention**: Keep only the most recent `.bak` file. Consider timestamped backups for critical operations.

3. **Key counting**: For nested structures, count leaf keys only (keys with string values, not object parents).

4. **Dot notation edge cases**:
   - Key contains literal dot: Not supported (use nested structure)
   - Empty key segment: Invalid (`"a..b"`)
   - Leading/trailing dots: Invalid (`".key"`, `"key."`)

5. **Concurrent access**: This operation is not atomic across multiple callers. Use external locking if needed.

6. **Large files**: For files over 1MB, consider streaming JSON parser. Standard i18n files are typically under 100KB.

7. **Validation**: After writing, optionally re-read and parse the file to verify it's valid JSON.
