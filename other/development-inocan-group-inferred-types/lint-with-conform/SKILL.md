---
name: lint-with-conform
description: Run formatters on files based on the user's conform neovim configuration. Supports multiple languages including JavaScript, TypeScript, Python, Go, Nix, Lua, and more. Use this when the user asks to format, lint, or clean up code files.
---

# Lint with Conform

This skill runs formatters on files according to the conform neovim setup in `~/workspace/nvim-config`.

## Formatter Configuration

Based on the user's conform setup, the following formatters should be used:

- **CSS**: prettierd
- **HTML/Django Templates**: djlint (for htmldjango), prettierd (for html)
- **GraphQL**: prettierd
- **JavaScript/JSX**: prettierd
- **JSON**: prettierd
- **Lua**: stylua
- **Markdown**: prettierd
- **Nix**: nixfmt
- **Python**: isort, then black (run in sequence)
- **Shell scripts**: shfmt
- **Svelte**: prettierd
- **Sass**: prettierd
- **TypeScript/TSX**: prettierd
- **Vue**: prettierd
- **YAML**: prettierd
- **Go**: gofumpt
- **Go templates**: gofumpt
- **Terraform**: terraform_fmt

## Instructions

When asked to lint or format files:

1. **Determine file type**: Check the file extension or content to determine the language
2. **Select formatter**: Use the appropriate formatter(s) from the configuration above
3. **Run formatter**: Execute the formatter command with appropriate flags
4. **Show results**: Display any errors or changes made

### Common Formatter Commands

- **prettierd**: `prettierd <file>` (prints formatted output to stdout)
- **nixfmt**: `nixfmt <file>` (formats file in place)
- **stylua**: `stylua <file>` (formats file in place)
- **black**: `black <file>` (formats file in place)
- **isort**: `isort <file>` (sorts imports in place)
- **shfmt**: `shfmt -w <file>` (formats file in place)
- **gofumpt**: `gofumpt -w <file>` (formats file in place)
- **terraform_fmt**: `terraform fmt <file>` (formats file in place)
- **djlint**: `djlint --reformat <file>` (formats file in place)

### For Python files

Run both formatters in sequence:
```bash
isort <file> && black <file>
```

### Handling Multiple Files

When multiple files are provided, process them according to their file types and run the appropriate formatter for each.

### Error Handling

- If a formatter is not installed, inform the user which tool is missing
- If formatting fails, show the error message and suggest fixes
- Skip files in `node_modules` directories (per user's config)

## Examples

### Format a single JavaScript file
```bash
prettierd src/components/Button.jsx
```

### Format a Python file
```bash
isort main.py && black main.py
```

### Format a Nix file
```bash
nixfmt flake.nix
```

## Notes

- The user's setup disables `eslint_d` as it's not available
- Files in `node_modules` should be skipped
- For files with formatters that modify in place, ensure to read the file first to preserve content if formatting fails
