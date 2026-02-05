---
name: installing-git-hooks
description: Use when setting up git pre-commit and pre-push hooks - provides simple shell script approach and pre-commit framework method, both calling justfile commands for DRY principle
---

# Installing Git Hooks

## Purpose

Enforce quality checks automatically:
- **Pre-commit:** format, lint, typecheck
- **Pre-push:** test

Hooks call justfile commands (DRY).

## Quick Setup

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e
echo "Running pre-commit checks..."
just format
just lint
just typecheck
echo "✅ Pre-commit checks passed"
EOF
chmod +x .git/hooks/pre-commit

cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
set -e
echo "Running pre-push checks..."
just test
echo "✅ Pre-push checks passed"
EOF
chmod +x .git/hooks/pre-push
```

## Justfile Integration

```just
# Install git hooks
hooks:
    @echo "Installing git hooks..."
    @cat > .git/hooks/pre-commit << 'EOF'\n#!/bin/bash\nset -e\necho "Running pre-commit checks..."\njust format\njust lint\njust typecheck\necho "✅ Pre-commit checks passed"\nEOF
    @chmod +x .git/hooks/pre-commit
    @cat > .git/hooks/pre-push << 'EOF'\n#!/bin/bash\nset -e\necho "Running pre-push checks..."\njust test\necho "✅ Pre-push checks passed"\nEOF
    @chmod +x .git/hooks/pre-push
    @echo "✅ Git hooks installed"

hooks-remove:
    rm -f .git/hooks/pre-commit .git/hooks/pre-push
    @echo "✅ Git hooks removed"
```

## Pre-commit Framework

For teams or complex setups:

**`.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: local
    hooks:
      - id: format
        name: Format code
        entry: just format
        language: system
        pass_filenames: false

      - id: lint
        name: Lint code
        entry: just lint
        language: system
        pass_filenames: false

      - id: typecheck
        name: Type check
        entry: just typecheck
        language: system
        pass_filenames: false

      - id: test
        name: Run tests
        entry: just test
        language: system
        pass_filenames: false
        stages: [push]
```

**Install:**
```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```

## Python with venv

```bash
#!/bin/bash
set -e
source .venv/bin/activate
just format
just lint
just typecheck
```

## Polyglot Projects

```bash
#!/bin/bash
set -e

if git diff --cached --name-only | grep -q "^api/"; then
    cd api && just format && just lint && just typecheck
fi

if git diff --cached --name-only | grep -q "^web/"; then
    cd web && just format && just lint && just typecheck
fi
```

## Best Practices

- **Fast:** Format/lint/typecheck in seconds
- **Fail fast:** Use `set -e` to exit on first error
- **Match CI:** Hooks should match CI checks
- **Document:** Include setup in README/onboarding

## Skipping (Use Sparingly)

```bash
git commit --no-verify -m "message"  # Skip pre-commit
git push --no-verify                 # Skip pre-push
```

## Troubleshooting

**Hook not running:**
```bash
ls -la .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
head -1 .git/hooks/pre-commit  # Verify shebang
```

**Just not found:**
```bash
#!/bin/bash
export PATH="$HOME/.cargo/bin:$PATH"
set -e
just format
```

**Venv issues:**
```bash
#!/bin/bash
set -e
source .venv/bin/activate
just format
```
