---
name: coding-assistant
description: "AI-powered coding assistant for code generation, explanation, debugging, and refactoring. Supports 50+ programming languages."
triggers:
  - "help me code"
  - "写代码"
  - "debug python"
  - "explain code"
  - "refactor code"
---

# Coding Assistant

AI-powered coding assistant for all your programming needs.

## Features

- 💻 **Code Generation** — Generate code from description
- 📖 **Code Explanation** — Understand any code
- 🐛 **Debugging** — Find and fix bugs
- ♻️ **Refactoring** — Improve code quality
- 📚 **Documentation** — Generate docs/comments
- ✅ **Code Review** — AI-powered review

## Supported Languages

Python, JavaScript, TypeScript, Go, Rust, Java, C++, C#, Ruby, PHP, Swift, Kotlin, Scala, R, MATLAB, Julia, Lua, Perl, Haskell, Elixir, Clojure, F#, OCaml, Dart, SQL, Shell, and 30+ more.

## Usage

### Generate Code

```bash
# Generate function
hermes code generate \
  --prompt "function to calculate fibonacci" \
  --language python

# Generate from spec
hermes code generate --spec api-spec.yaml --language typescript
```

### Debug Code

```bash
# Debug file
hermes code debug --file main.py

# Debug function
hermes code debug --function "broken_function" --file main.py
```

### Explain Code

```bash
# Explain file
hermes code explain --file complex_module.py

# Explain specific section
hermes code explain --lines "10-50" --file main.py
```

### Refactor

```bash
# Improve code
hermes code refactor --file main.py --target performance

# Convert language
hermes code convert --from python --to javascript --file script.py
```

### Generate Tests

```bash
hermes code test --file main.py --framework pytest
```

## Examples

### API Development
```
hermes code generate \
  --prompt "REST API for user management with CRUD operations" \
  --language python \
  --framework fastapi
```

### Data Processing
```
hermes code generate \
  --prompt "pandas code to clean and merge datasets" \
  --language python
```

### DevOps Script
```
hermes code generate \
  --prompt "bash script to deploy docker container" \
  --language shell
```

## Configuration

```yaml
# coding-assistant.yml
defaults:
  language: python
  style: pep8
  comments: true
  
generation:
  max_tokens: 2000
  temperature: 0.7
  
debug:
  explain_fixes: true
  include_tests: true
```

## Pitfalls

1. **Context Window** — Large files may exceed limits
2. **Framework Knowledge** — May not know all frameworks
3. **Best Practices** — Verify generated code for security