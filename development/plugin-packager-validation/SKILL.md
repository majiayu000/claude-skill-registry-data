---
name: plugin-packager-validation
description: Plugin validation errors and fixes
---

# Validation Error Reference

| Error | Fix |
|-------|-----|
| Invalid path | Add `./` prefix |
| Script not executable | `chmod +x <script>` |
| Invalid JSON | Run `jq . .claude-plugin/plugin.json` |
| Missing field | Add `name` and `version` |
| Component not found | Verify path exists |

## Debug Commands

```bash
# Validate JSON
jq . .claude-plugin/plugin.json

# List all components
find . -type d \( -name agents -o -name commands -o -name skills -o -name hooks \) -exec ls {} \;

# Check hook scripts
find hooks -type f -exec file {} \;
```

## Full Schema Reference

```json
{
  "name": "REQUIRED",
  "version": "REQUIRED (semver)",
  "description": "optional",
  "author": {"name": "", "email": "", "url": ""},
  "commands": "./commands/ OR [array]",
  "agents": "./agents/ OR [array]",
  "skills": "./skills/ OR [array]",
  "hooks": "./hooks/hooks.json OR [array] OR {inline}"
}
```

## Rules

1. All paths relative, starting with `./`
2. Only plugin.json in `.claude-plugin/`
3. Components at plugin root
4. Arrays for multiple paths
