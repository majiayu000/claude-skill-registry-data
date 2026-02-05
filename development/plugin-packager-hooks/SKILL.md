---
name: plugin-packager-hooks
description: Handle hook scripts and paths for plugin packaging
---

# Hook Script Handling

## Make Executable

```bash
chmod +x hooks/golang/scripts/*.sh
chmod +x hooks/security/scripts/*.py
```

## Dynamic Path Resolution

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths:

```json
{
  "script": "${CLAUDE_PLUGIN_ROOT}/hooks/golang/scripts/go-fmt.sh"
}
```

## Validate All Scripts

```bash
find hooks -type f \( -name "*.sh" -o -name "*.py" \) ! -perm -u+x
```

## Multiple hooks.json Handling

### Option 1: Array Reference (Recommended)

```json
{
  "hooks": [
    "./hooks/golang/hooks.json",
    "./hooks/security/hooks.json"
  ]
}
```

### Option 2: Inline Merged

Combine all hook definitions into single inline object in plugin.json.
