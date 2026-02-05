---
name: vscode-extension
# prettier-ignore
description: Use when developing VS Code extensions including TextMate grammars, language configuration, and extension manifest
---

# VS Code Extension Development

## Quick Start

```json
// package.json
{
  "name": "my-language",
  "contributes": {
    "languages": [{
      "id": "mylang",
      "extensions": [".ml"],
      "configuration": "./language-configuration.json"
    }],
    "grammars": [{
      "language": "mylang",
      "scopeName": "source.mylang",
      "path": "./syntaxes/mylang.tmLanguage.json"
    }]
  }
}
```

## Core Components

- **package.json**: Extension manifest with `contributes` for languages, grammars, commands
- **language-configuration.json**: Brackets, comments, auto-closing pairs, folding
- **TextMate Grammar**: Syntax highlighting via regex patterns and scopes
- **Language Server**: Advanced features (LSP) for completions, diagnostics

## TextMate Grammar Structure

```json
{
  "scopeName": "source.mylang",
  "patterns": [{ "include": "#expression" }],
  "repository": {
    "expression": {
      "patterns": [
        { "include": "#keywords" },
        { "include": "#strings" }
      ]
    },
    "keywords": {
      "match": "\\b(if|else|while)\\b",
      "name": "keyword.control.mylang"
    }
  }
}
```

## Key Scope Naming

- `keyword.control` - Control flow (if, else, for)
- `keyword.operator` - Operators (+, -, =)
- `string.quoted` - String literals
- `comment.line` / `comment.block` - Comments
- `entity.name.function` - Function names
- `variable` - Variables
- `constant.numeric` - Numbers

## Reference Files

- [references/textmate.md](references/textmate.md) - TextMate grammar patterns
- [references/language-config.md](references/language-config.md) - Language configuration
- [references/publishing.md](references/publishing.md) - Publishing to marketplace
