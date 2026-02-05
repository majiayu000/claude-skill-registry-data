---
name: ungit
description: Fetch code from GitHub repositories as LLM-friendly context. Use when needing to reference, analyze, or understand code from a GitHub repo/directory/file.
---

Use the `ungit` command with the `--prompt` flag to fetch code from GitHub in a format optimized for LLM context.

## Usage

```
ungit -p [options] <source>
```

**Source formats:**

- `user/repo` - entire repository
- `user/repo/path` - specific directory or file
- `user/repo@branch` - specific branch
- GitHub URLs (HTTPS, SSH, or tree URLs)

**Options:**

- `-p, --prompt` - Output as XML-formatted text (required for LLM context)
- `-i, --include GLOB` - Only include files matching pattern (repeatable)
- `-e, --exclude GLOB` - Exclude files matching pattern (repeatable)

## Output Format

The command outputs XML-formatted content:

- `<directory_structure>` - tree view of fetched files
- `<files>` - file contents wrapped in `<file path="...">` tags

## Examples

```bash
# Fetch a specific directory
ungit -p facebook/react/packages/react

# Fetch from a branch
ungit -p vercel/next.js/examples@canary

# Filter: Only TypeScript files
ungit -p -i "*.ts" -i "*.tsx" user/repo/src

# Filter: Exclude tests and config files
ungit -p -e "*.test.*" -e "*.config.*" user/repo

# Filter: Combine filters
ungit -p -i "*.py" -e "*_test.py" user/repo/src
```

## Notes

- Binary files show `[binary file]` placeholder
- Files >100KB show `[file too large]` placeholder
- Output goes to stdout for piping/capturing
