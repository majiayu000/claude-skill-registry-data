---
name: prism-syntax
# prettier-ignore
description: Use when adding syntax highlighting for custom languages to Prism.js, used by Docusaurus and many documentation sites
---

# Prism.js Syntax Highlighting

## Quick Start

```javascript
Prism.languages.mylang = {
  'comment': /\/\/.*/,
  'string': /"(?:\\.|[^"\\])*"/,
  'keyword': /\b(?:if|else|while|for|return)\b/,
  'number': /\b\d+(?:\.\d+)?\b/,
  'operator': /[+\-*/%=<>!&|]+/,
  'punctuation': /[{}[\];(),.:]/
};
```

## Token Types (CSS Classes)

- `comment` - Comments
- `string` - String literals
- `keyword` - Language keywords
- `number` - Numeric literals
- `operator` - Operators
- `punctuation` - Punctuation marks
- `function` - Function names
- `class-name` - Type/class names
- `property` - Object properties
- `boolean` - true/false
- `builtin` - Built-in functions

## Pattern Techniques

```javascript
{
  // Lookbehind for context
  'function': {
    pattern: /(\bfunction\s+)\w+/,
    lookbehind: true
  },
  // Nested grammar
  'interpolation': {
    pattern: /\$\{[^}]+\}/,
    inside: {
      'variable': /\$\{|\}/,
      'expression': { pattern: /[\s\S]+/, inside: Prism.languages.javascript }
    }
  },
  // Greedy matching
  'string': { pattern: /"(?:\\.|[^"\\])*"/, greedy: true }
}
```

## Docusaurus Integration

```javascript
// docusaurus.config.js
module.exports = {
  themeConfig: {
    prism: {
      additionalLanguages: ['mylang'],
      theme: require('prism-react-renderer').themes.github,
    }
  }
};

// Create src/prism/prism-mylang.js and import in src/theme/prism-include-languages.js
```

## Reference Files

- [references/tokens.md](references/tokens.md) - Complete token reference
- [references/patterns.md](references/patterns.md) - Advanced pattern techniques
- [references/docusaurus.md](references/docusaurus.md) - Docusaurus integration
