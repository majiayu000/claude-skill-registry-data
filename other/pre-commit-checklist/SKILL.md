---
name: pre-commit-checklist
description: Implement automated pre-commit quality checks including linting, formatting, type checking, tests, security scans, and commit message validation. Use when.
---

# Pre-Commit Security and Quality Checklist

Implement comprehensive automated pre-commit quality checks that validate code before it enters version control. Prevent defects, security issues, and policy violations by catching problems at commit time through linting, formatting, type checking, unit tests, security scans, and commit message validation.

## When to Use This Skill

Use this skill when you need to:

- Establish quality gates before code enters version control
- Prevent committing secrets or sensitive data
- Enforce code style and formatting standards
- Run fast unit tests before each commit
- Validate commit message conventions
- Detect common security issues early
- Ensure type safety before commits
- Maintain consistent code quality across team
- Reduce CI/CD pipeline failures
- Implement shift-left security practices

**Trigger phrases**: "pre-commit hooks", "git hooks", "commit validation", "prevent secrets", "enforce formatting", "lint on commit", "husky setup", "pre-commit framework"

## What This Skill Does

### Core Capabilities

- **Git Hook Setup**: Install and configure pre-commit hooks
- **Code Formatting**: Automatic formatting enforcement
- **Linting**: Style and quality validation
- **Type Checking**: Static type verification
- **Unit Testing**: Fast smoke tests before commit
- **Security Scanning**: Detect secrets and vulnerabilities
- **Commit Message Validation**: Enforce conventions
- **File Size Checks**: Prevent large file commits
- **Merge Conflict Detection**: Catch unresolved conflicts

### Language Support

| Language | Formatting | Linting | Type Check | Security |
|----------|------------|---------|------------|----------|
| Python | Black, autopep8 | Flake8, pylint | mypy, pyright | bandit |
| JavaScript | Prettier | ESLint | TypeScript | eslint-security |
| Java | google-java-format | Checkstyle | - | SpotBugs |
| C# | dotnet format | StyleCop | - | Security Code Scan |
| Go | gofmt | golint | staticcheck | gosec |
| C/C++ | clang-format | clang-tidy | - | cppcheck |

## Prerequisites

- Git repository initialized
- Package manager for target language(s)
- Bash or PowerShell (for hook scripts)
- Development environment with command-line access

## Instructions

### Step 1: Choose Pre-Commit Framework

#### Option A: Pre-commit Framework (Recommended for Multi-language)

```bash
# Install pre-commit (Python-based but supports all languages)
pip install pre-commit

# Verify installation
pre-commit --version

# Create .pre-commit-config.yaml in repository root
pre-commit sample-config > .pre-commit-config.yaml

# Install hooks
pre-commit install

# Test on all files (optional)
pre-commit run --all-files
```

**Advantages**:
- Multi-language support
- Large plugin ecosystem
- Automatic tool installation
- Easy configuration
- Active community

#### Option B: Husky (JavaScript/TypeScript Projects)

```bash
# Install husky
npm install --save-dev husky

# Initialize husky
npx husky-init && npm install

# Add pre-commit hook
npx husky add .husky/pre-commit "npm test"

# Make executable
chmod +x .husky/pre-commit
```

#### Option C: Manual Git Hooks

```bash
# Navigate to git hooks directory
cd .git/hooks

# Create pre-commit hook
cat > pre-commit << 'EOF'
#!/bin/bash
echo "Running pre-commit checks..."

# Run linting
if ! npm run lint; then
    echo "Linting failed. Commit aborted."
    exit 1
fi

# Run tests
if ! npm test; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

echo "All checks passed!"
exit 0
EOF

# Make executable
chmod +x pre-commit
```

### Step 2: Configure Language-Specific Checks

#### Python - Comprehensive Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # Code Formatting
  - repo: https://github.com/psf/black
    rev: 23.10.1
    hooks:
      - id: black
        language_version: python3.11
        args: ['--line-length=88']

  # Import Sorting
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ['--profile', 'black']

  # Linting
  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203']
        additional_dependencies: [flake8-docstrings]

  # Type Checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.1
    hooks:
      - id: mypy
        args: ['--ignore-missing-imports', '--strict']
        additional_dependencies: [types-all]

  # Security Scanning
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', 'src/', '-ll']

  # Secret Detection
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  # General Checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: check-json
      - id: pretty-format-json
        args: ['--autofix']

  # Testing (fast smoke tests only)
  - repo: local
    hooks:
      - id: pytest-quick
        name: pytest-quick
        entry: pytest tests/quick/ -x --tb=short
        language: system
        pass_filenames: false
        always_run: true
```

#### JavaScript/TypeScript - Using Husky + lint-staged

```json
// package.json
{
  "scripts": {
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "test:quick": "jest --testPathPattern=quick --bail",
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "jest --findRelatedTests --bail"
    ],
    "*.{json,md,yml}": [
      "prettier --write"
    ]
  },
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged && npm run type-check"
    }
  },
  "devDependencies": {
    "husky": "^8.0.3",
    "lint-staged": "^15.0.2",
    "eslint": "^8.52.0",
    "prettier": "^3.0.3",
    "typescript": "^5.2.2",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "eslint-plugin-security": "^1.7.1"
  }
}
```

**ESLint Configuration** (.eslintrc.json):

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:security/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint", "security"],
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "security/detect-object-injection": "warn"
  }
}
```

#### Java - Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # Google Java Format
  - repo: https://github.com/google/google-java-format
    rev: v1.18.1
    hooks:
      - id: google-java-format

  # SpotBugs (Security)
  - repo: local
    hooks:
      - id: spotbugs
        name: SpotBugs Security Check
        entry: mvn spotbugs:check
        language: system
        pass_filenames: false
        files: \.java$

  # Quick Unit Tests
  - repo: local
    hooks:
      - id: maven-test-quick
        name: Maven Quick Tests
        entry: mvn test -Dtest=*QuickTest
        language: system
        pass_filenames: false
```

#### Go - Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # gofmt
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-imports
      - id: go-lint
      - id: go-vet
      - id: go-staticcheck

  # Security - gosec
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-sec

  # Quick tests
  - repo: local
    hooks:
      - id: go-test-quick
        name: Go Quick Tests
        entry: go test -short ./...
        language: system
        pass_filenames: false
```

#### C# - Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # dotnet format
  - repo: local
    hooks:
      - id: dotnet-format
        name: dotnet format
        entry: dotnet format --verify-no-changes
        language: system
        files: \.(cs|vb)$
        pass_filenames: false

  # Security Analysis
  - repo: local
    hooks:
      - id: security-scan
        name: .NET Security Scan
        entry: dotnet list package --vulnerable
        language: system
        pass_filenames: false

  # Quick Unit Tests
  - repo: local
    hooks:
      - id: dotnet-test-quick
        name: Quick Unit Tests
        entry: dotnet test --filter "Category=Quick"
        language: system
        pass_filenames: false
```

#### C/C++ - Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # clang-format
  - repo: https://github.com/pre-commit/mirrors-clang-format
    rev: v17.0.4
    hooks:
      - id: clang-format
        args: ['-i']

  # cppcheck
  - repo: local
    hooks:
      - id: cppcheck
        name: cppcheck
        entry: cppcheck
        args: ['--enable=all', '--error-exitcode=1', '--inline-suppr']
        language: system
        files: \.(c|cpp|cc|cxx|h|hpp)$

  # clang-tidy
  - repo: local
    hooks:
      - id: clang-tidy
        name: clang-tidy
        entry: clang-tidy
        args: ['--fix', '--format-style=file']
        language: system
        files: \.(c|cpp|cc|cxx)$
```

### Step 3: Implement Secret Detection

**Prevent accidental credential commits:**

#### Using detect-secrets (Recommended)

```bash
# Install
pip install detect-secrets

# Generate baseline (initial scan)
detect-secrets scan > .secrets.baseline

# Add to pre-commit config
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json
```

**Workflow**:
1. Initial scan creates baseline of existing "secrets" (false positives)
2. Pre-commit hook compares new changes against baseline
3. New secrets are blocked
4. Update baseline when adding legitimate patterns

**Update baseline** when adding legitimate patterns:

```bash
# Audit and update baseline
detect-secrets audit .secrets.baseline

# Mark false positives
# Press 'y' for true positives, 'n' for false positives

# Regenerate baseline
detect-secrets scan --baseline .secrets.baseline
```

**Common Secret Patterns to Detect**:

```regex
# API Keys
api[_-]?key.*["\'][a-zA-Z0-9]{32,}["\']

# AWS Keys
AKIA[0-9A-Z]{16}

# Private Keys
-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----

# Passwords
password.*["\'][^"\']{8,}["\']

# Tokens
(access|auth|bearer)[_-]?token.*["\'][a-zA-Z0-9\-_]{20,}["\']

# Database URLs with credentials
(postgres|mysql|mongodb):\/\/[^:]+:[^@]+@
```

### Step 4: Configure Commit Message Validation

#### Conventional Commits Standard

**Format**: `<type>(<scope>): <subject>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```
feat(auth): add OAuth2 authentication
fix(api): resolve null pointer exception in user endpoint
docs(readme): update installation instructions
test(user): add unit tests for user service
```

#### Using commitlint

```bash
# Install commitlint
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Create configuration
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js

# Install commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

**commitlint.config.js** (custom rules):

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'test',
        'chore',
        'revert'
      ]
    ],
    'subject-case': [2, 'never', ['upper-case']],
    'subject-max-length': [2, 'always', 100],
    'body-max-line-length': [2, 'always', 200]
  }
};
```

#### Using Pre-commit Framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: []
```

**Install commit-msg hook**:

```bash
pre-commit install --hook-type commit-msg
```

### Step 5: Configure Fast Unit Tests

**Run quick smoke tests before committing:**

#### Python - Pytest Configuration

```ini
# pytest.ini
[pytest]
markers =
    quick: marks tests as quick (deselect with '-m "not quick"')
    slow: marks tests as slow

# Run only quick tests in pre-commit
addopts = -m quick --tb=short -x
```

**Mark tests**:

```python
import pytest

@pytest.mark.quick
def test_user_creation():
    """Quick test: user creation works."""
    user = User("test@example.com")
    assert user.email == "test@example.com"

@pytest.mark.slow
def test_database_migration():
    """Slow test: full database migration."""
    # This test takes 30 seconds, skip in pre-commit
    migrate_database()
    assert check_migration_complete()
```

#### JavaScript - Jest Configuration

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:quick": "jest --testPathPattern=quick --bail --maxWorkers=2",
    "test:slow": "jest tests/slow/"
  }
}
```

### Step 6: Configure File Size and Type Checks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      # File size check (max 1MB)
      - id: check-added-large-files
        args: ['--maxkb=1000']

      # Prevent committing to main/master
      - id: no-commit-to-branch
        args: ['--branch', 'main', '--branch', 'master']

      # Check for merge conflicts
      - id: check-merge-conflict

      # Check file encoding
      - id: check-case-conflict
      - id: mixed-line-ending
        args: ['--fix=lf']

      # Prevent committing private keys
      - id: detect-private-key

      # YAML validation
      - id: check-yaml
        args: ['--safe']

      # JSON validation
      - id: check-json

      # Trailing whitespace
      - id: trailing-whitespace
        args: ['--markdown-linebreak-ext=md']

      # End of file fixer
      - id: end-of-file-fixer

      # Check Python syntax
      - id: check-ast

      # Check for debugger statements
      - id: debug-statements
```

### Step 7: Complete Multi-Language Configuration

```yaml
# .pre-commit-config.yaml
# Comprehensive pre-commit configuration for multi-language project

default_language_version:
  python: python3.11
  node: 18.18.0

repos:
  # ===== General Checks =====
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: detect-private-key
      - id: no-commit-to-branch
        args: ['--branch', 'main']

  # ===== Secret Detection =====
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json

  # ===== Python =====
  - repo: https://github.com/psf/black
    rev: 23.10.1
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ['--profile', 'black']

  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.1
    hooks:
      - id: mypy
        args: ['--ignore-missing-imports']

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-ll']

  # ===== JavaScript/TypeScript =====
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.52.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]
        args: ['--fix']

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.3
    hooks:
      - id: prettier

  # ===== Commit Message =====
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]

  # ===== Local Hooks (Tests) =====
  - repo: local
    hooks:
      # Python quick tests
      - id: pytest-quick
        name: Python Quick Tests
        entry: pytest -m quick --tb=short -x
        language: system
        pass_filenames: false
        types: [python]

      # TypeScript type check
      - id: tsc
        name: TypeScript Type Check
        entry: npx tsc --noEmit
        language: system
        types: [ts, tsx]
        pass_filenames: false
```

### Step 8: Team Adoption and CI/CD Integration

#### Team Onboarding

**README.md Addition**:

```markdown
## Development Setup

### Pre-commit Hooks

This project uses automated pre-commit hooks to ensure code quality and security.

**Installation** (one-time setup):

```bash
# Install pre-commit framework
pip install pre-commit

# Install hooks for this repository
pre-commit install
pre-commit install --hook-type commit-msg

# Test installation (optional)
pre-commit run --all-files
```

**What Gets Checked**:
- Code formatting (Black, Prettier, etc.)
- Linting (Flake8, ESLint, etc.)
- Type checking (mypy, TypeScript)
- Security scanning (bandit, secret detection)
- Quick unit tests
- Commit message format
- File size limits
- Merge conflict detection

**Bypassing Hooks** (use sparingly):
```bash
# Skip all pre-commit hooks (NOT RECOMMENDED)
git commit --no-verify -m "message"
```

**Troubleshooting**:
```bash
# Update hooks to latest versions
pre-commit autoupdate

# Clear cache if hooks fail unexpectedly
pre-commit clean

# Run specific hook manually
pre-commit run <hook-id> --all-files
```
```

#### CI/CD Pipeline Integration

**GitHub Actions**:

```yaml
# .github/workflows/quality-checks.yml
name: Quality Checks

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install pre-commit
        run: pip install pre-commit

      - name: Run pre-commit on all files
        run: pre-commit run --all-files
```

## Common Pitfalls and Solutions

### Pitfall 1: Hooks Too Slow

**Problem**: Pre-commit takes >30 seconds, frustrating developers.

**Solution**:
- Run only quick tests (< 5 seconds total)
- Use `lint-staged` to check only changed files
- Offload comprehensive checks to CI/CD
- Parallelize independent checks

### Pitfall 2: False Positives Block Commits

**Problem**: Legitimate code flagged incorrectly.

**Solution**:
- Tune linting rules to reduce noise
- Add exclusions for generated code
- Update secret detection baseline

```yaml
# Exclude generated files
- id: flake8
  exclude: ^(migrations/|generated/|.*_pb2\.py$)
```

### Pitfall 3: Developers Bypassing Hooks

**Problem**: Team uses `--no-verify` frequently.

**Solution**:
- Investigate why hooks are being bypassed
- Fix underlying issues (speed, false positives)
- Enforce checks in CI/CD (safety net)
- Educate team on importance

### Pitfall 4: Hooks Not Installed

**Problem**: New team members forget to install hooks.

**Solution**:
- Add setup to onboarding documentation
- Include in README prominently
- Add installation check to CI/CD
- Use `husky` which auto-installs for JavaScript projects

## Quality Checklist

- [ ] Pre-commit framework installed and configured
- [ ] Code formatting automated for all languages
- [ ] Linting enforced with appropriate rules
- [ ] Type checking enabled (TypeScript, Python, etc.)
- [ ] Secret detection preventing credential leaks
- [ ] Quick unit tests running (<10 seconds)
- [ ] Commit message validation enforcing conventions
- [ ] File size and type checks preventing inappropriate commits
- [ ] Team trained on pre-commit workflow
- [ ] CI/CD pipeline enforces same checks
- [ ] Documentation updated with setup instructions
- [ ] Performance optimized (total time <30 seconds)
- [ ] False positive rate acceptable (<5%)
- [ ] Bypass rate monitored and low (<10%)

## Related Skills

- `dependency-security-audit` - Dependency vulnerability scanning
- `code-commit-workflow` - Git commit best practices
- `security-review` - Deep security audit
- `code-quality` - Code quality assessment

## Additional Resources

### Pre-commit Frameworks
- [Pre-commit Framework](https://pre-commit.com/) - Multi-language framework
- [Husky](https://typicode.github.io/husky/) - JavaScript/TypeScript
- [Lefthook](https://github.com/evilmartians/lefthook) - Fast Git hooks manager

### Commit Message Standards
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Commitlint](https://commitlint.js.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)

### Secret Detection
- [detect-secrets](https://github.com/Yelp/detect-secrets)
- [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- [git-secrets](https://github.com/awslabs/git-secrets)
- [Gitleaks](https://github.com/gitleaks/gitleaks)

### Code Quality Tools
- [Black](https://black.readthedocs.io/) - Python formatter
- [ESLint](https://eslint.org/) - JavaScript linter
- [Prettier](https://prettier.io/) - Universal formatter
- [Checkstyle](https://checkstyle.org/) - Java style checker

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: Git Hooks Best Practices, Pre-commit Framework, Husky, Conventional Commits


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
