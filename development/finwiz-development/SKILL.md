---
name: finwiz-development
description: "General development standards for FinWiz including dependency management, code quality, file organization, version control, and documentation practices. Use when setting up projects, managing dependencies, or establishing development workflows."
allowed-tools: ["Read", "Edit", "Bash"]
---

# FinWiz Development Standards

General development standards and best practices for maintaining high-quality code in the FinWiz project.

## Dependency Management

### Adding Dependencies

- **Use latest stable versions** of all libraries
- **Leverage Context7 MCP server** to verify compatibility before adding
- **Justify each dependency** with clear business or technical value
- **Prefer well-maintained libraries** with active communities
- **Document version constraints** in `pyproject.toml` or `requirements.txt`

### Maintenance

- **Remove unused dependencies** regularly
- **Use lock files** (`uv.lock`) for consistent installations
- **Update dependencies** systematically with testing
- **Monitor security advisories** for dependencies

```bash
# Check for unused dependencies
uv sync --group dev
uv run pip-check

# Update dependencies safely
uv sync --upgrade
make test  # Verify nothing breaks
```

## Code Quality Standards

### File Management

- **Never create duplicate files** with suffixes like `_fixed`, `_clean`, `_backup`
- **Work iteratively** on existing files
- **Maintain clean directory structures**
- **Use consistent naming conventions** across the project
- **Avoid temporary files** in version control
- **Organize code logically** by feature or domain

### Code Style

- **Follow language-specific conventions** (Python PEP 8, TypeScript standards)
- **Use meaningful variable and function names**
- **Keep functions small** and focused on single responsibilities
- **Implement proper error handling** and logging
- **Include relevant documentation links** in code comments

```python
# ✅ GOOD: Clear, descriptive names
def calculate_sharpe_ratio(returns: list[float], risk_free_rate: float) -> float:
    """Calculate Sharpe ratio with proper error handling."""
    if not returns:
        raise ValueError("Returns list cannot be empty")
    
    # Implementation with clear logic...
    return sharpe_ratio

# ❌ BAD: Unclear names, no error handling
def calc(r, rf):
    return (sum(r)/len(r) - rf) / (sum([(x-sum(r)/len(r))**2 for x in r])/len(r))**0.5
```

## Version Control Standards

### Commit Messages

Use **conventional commit format**:

```
type(scope): description

feat(auth): add JWT token validation
fix(api): resolve timeout issue in stock data fetch
docs(readme): update installation instructions
refactor(scoring): extract risk calculation to separate module
test(portfolio): add unit tests for rebalancing logic
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Branching Strategy

- **Feature branches** for new development: `feature/user-authentication`
- **Bug fix branches**: `fix/portfolio-calculation-error`
- **Keep main/master stable** and deployable
- **Delete merged branches** to keep repository clean

### Workflow

```bash
# Start new feature
git checkout main
git pull origin main
git checkout -b feature/new-feature

# Work with frequent commits
git add .
git commit -m "feat(feature): implement core logic"

# Clean up before merge
git rebase -i main  # Interactive rebase to clean history

# Create pull request for review
gh pr create --title "feat: implement new feature" --body "Description..."
```

### Repository Management

- **Use `.gitignore`** to exclude build artifacts and secrets
- **Never commit secrets**, API keys, or passwords
- **Keep repository size manageable** (use Git LFS for large files)
- **Review commits** for sensitive information
- **Use signed commits** when possible

```bash
# Check for secrets before commit
git diff --cached | grep -i "api_key\|password\|secret"

# Sign commits
git config --global user.signingkey YOUR_GPG_KEY
git config --global commit.gpgsign true
```

## Documentation Standards

### Code Documentation

- **Maintain comprehensive README** covering setup, usage, deployment
- **Keep documentation close to code** (docstrings, inline comments)
- **Document API endpoints** and data structures
- **Include setup and deployment instructions**
- **Reference official sources** through MCP servers when available

### Documentation Updates

- **Update docs when upgrading dependencies**
- **Document breaking changes** in CHANGELOG.md
- **Use inline comments** for complex business logic
- **Keep examples current** and tested

```python
def analyze_portfolio(holdings: list[Holding]) -> PortfolioAnalysis:
    """
    Analyze portfolio holdings and generate recommendations.
    
    This function performs comprehensive analysis including:
    - Risk assessment using modern portfolio theory
    - Performance attribution analysis
    - Rebalancing recommendations
    
    Args:
        holdings: List of portfolio holdings with current allocations
        
    Returns:
        PortfolioAnalysis with recommendations and risk metrics
        
    Raises:
        ValidationError: If holdings data is invalid
        APIError: If external data sources are unavailable
        
    Example:
        >>> holdings = [Holding(ticker="AAPL", weight=0.3)]
        >>> analysis = analyze_portfolio(holdings)
        >>> print(analysis.recommendation)
        'REBALANCE'
    """
```

## Quality Assurance

### Testing Requirements

- **Write tests for new functionality**
- **Run tests before committing** changes
- **Maintain high test coverage** (>80% for critical modules)
- **Use appropriate test types** (unit, integration, end-to-end)

### Code Review Process

- **All changes require review** via pull requests
- **Review for**: correctness, performance, security, maintainability
- **Use automated checks**: linting, formatting, type checking
- **Document review decisions** in PR comments

### Continuous Integration

```bash
# Pre-commit checks
make lint      # Linting and formatting
make mypy      # Type checking
make test      # Unit tests
make check     # All quality checks

# CI pipeline should run
make check-all  # Complete validation suite
```

## Configuration Management

### Environment Configuration

- **Use environment variables** for configuration
- **Provide `.env.example`** with required variables
- **Document all configuration options**
- **Use different configs** for dev/staging/production

### Project Configuration

- **Keep configuration files** at appropriate levels
- **Use `pyproject.toml`** for Python project configuration
- **Document configuration changes** in commit messages
- **Validate configuration** on startup

## Performance and Security

### Performance

- **Profile code** for performance bottlenecks
- **Use appropriate data structures** and algorithms
- **Cache expensive operations** when appropriate
- **Monitor resource usage** in production

### Security

- **Never commit secrets** to version control
- **Use secure coding practices**
- **Validate all inputs** from external sources
- **Keep dependencies updated** for security patches
- **Use HTTPS** for all external communications

## Development Workflow

### Daily Workflow

1. **Pull latest changes** from main branch
2. **Create feature branch** for new work
3. **Write tests first** (TDD approach)
4. **Implement functionality** with proper error handling
5. **Run quality checks** before committing
6. **Commit with descriptive messages**
7. **Create pull request** for review
8. **Address review feedback**
9. **Merge and delete branch**

### Project Setup

```bash
# Clone and setup
git clone <repository>
cd finwiz
uv sync --group dev

# Verify setup
make check
make test

# Start development
git checkout -b feature/my-feature
```

Remember: **Quality over speed**. It's better to write maintainable, well-tested code than to rush and create technical debt.