---
name: github-gist
description: Create GitHub gists quickly from files, code snippets, or text content. Use when the user wants to share code via GitHub gists or export content to gist format.
license: MIT
metadata:
  author: Kenny Gatdula
  version: "1.0.0"
  tags: github, gist, export, sharing, utility, universal
  compatibility: Any agentskills.io-compatible agent
---

# GitHub Gist Creation

Create GitHub gists quickly from files, code snippets, or text content. This skill simplifies the process of sharing code and conversations via GitHub gists.

## Features

- Create private or public gists
- Support for single or multiple files
- Custom descriptions and filenames
- Automatic browser opening to view created gist
- GitHub Enterprise support via `--host` option
- GitHub CLI integration

## Prerequisites

- GitHub CLI (`gh`) must be installed and authenticated
- Run `gh auth login` if not already authenticated

## Usage

### Basic Examples

Create a private gist from a file:
```bash
gist.sh path/to/file.js
```

Create a public gist from a file:
```bash
gist.sh --public path/to/file.js
```

Create a gist with a custom description:
```bash
gist.sh --desc "My awesome code snippet" file.js
```

Create a gist from multiple files:
```bash
gist.sh file1.js file2.md file3.txt
```

Create a gist with stdin:
```bash
echo "console.log('hello')" | gist.sh --filename "hello.js"
```

### Advanced Usage

Combine options:
```bash
gist.sh --public --desc "React component example" component.jsx
```

Specify custom filename (when using stdin):
```bash
cat script.sh | gist.sh --filename "deploy.sh" --desc "Deployment script"
```

Don't open browser automatically:
```bash
gist.sh --no-browser file.js
```

Use with GitHub Enterprise:
```bash
gist.sh --host github.mycompany.com file.js
```

Or set the `GH_HOST` environment variable:
```bash
GH_HOST=github.mycompany.com gist.sh file.js
```

## Script Arguments

- `--public` - Create a public gist (default is private)
- `--desc "description"` - Add a description to the gist
- `--filename "name"` - Specify filename when using stdin
- `--no-browser` - Don't open the gist in browser after creation
- `--host "hostname"` - GitHub Enterprise host (or set `GH_HOST` env var)
- Any other arguments are treated as file paths

## Compatibility

This skill works with any agent that supports the agentskills.io format:
- ✅ OpenCode
- ✅ Claude Code
- ✅ Cursor
- ✅ VS Code with agentskills support
- ✅ Any agentskills.io-compatible agent

## How It Works

The skill uses the GitHub CLI (`gh gist create`) to create gists. It automatically:
1. Checks if you're authenticated with GitHub
2. Parses your arguments to build the appropriate `gh` command
3. Creates the gist with your specified options
4. Opens the gist in your browser (unless `--no-browser` is specified)

## Common Use Cases

**Share a code file:**
```bash
gist.sh src/components/Button.tsx
```

**Quick snippet sharing:**
```bash
echo "SELECT * FROM users WHERE active = true;" | gist.sh --filename "query.sql" --public
```

**Export multiple related files:**
```bash
gist.sh --desc "API documentation" api.md examples.js tests.js
```

**Agent Integration:**
Works in any agent that can execute shell scripts and supports agentskills.io.

## Tips

- Use `--public` sparingly - private gists are safer for sensitive code
- Add meaningful descriptions to make gists easier to find later
- You can edit or delete gists later via `gh gist edit` or `gh gist delete`
- View all your gists with `gh gist list`

## Troubleshooting

**"gh: command not found"**
- Install GitHub CLI: https://cli.github.com/

**"authentication required"**
- Run `gh auth login` and follow the prompts

**"failed to create gist"**
- Check that the file paths are correct
- Ensure you have an internet connection
- Verify GitHub CLI is properly authenticated

## See Also

- GitHub CLI documentation: https://cli.github.com/manual/gh_gist_create
- Managing gists: `gh gist list`, `gh gist edit`, `gh gist delete`
- Agent Skills specification: https://agentskills.io
