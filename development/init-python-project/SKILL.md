---
name: init-python-project
description: Initialize a complete Python project with standard structure, pyproject.toml, testing framework, and documentation. Use when starting a new Python project.
---

# Initialize Python Project

Create a complete, production-ready Python project with standard structure, configuration files, testing framework, and documentation.

## When to Use This Skill

Use this skill when you need to:

- Start a new Python project from scratch
- Establish standard project structure
- Set up development environment with best practices
- Initialize testing framework and CI/CD
- Create documentation templates
- Configure linting, formatting, and type checking

**Trigger phrases**: "init python project", "new python project", "create python project", "python boilerplate", "python project setup", "python starter"

## What This Skill Does

### Project Structure Created

```
project_name/
├── .venv/                  # Virtual environment
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # Entry point
│   └── core/              # Core modules
│       ├── __init__.py
│       └── utils/
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── run_all_tests.py   # Master test runner
│   ├── common.py          # Shared test utilities
│   ├── test_config.py     # Test configuration
│   └── test_main.py       # Example tests
├── docs/                   # Documentation
│   └── DEVLOG.md          # Development log
├── .gitignore             # Git ignore rules
├── .github/               # GitHub workflows
│   └── workflows/
│       └── ci.yml
├── CHANGELOG.md           # Version history
├── README.md              # Project documentation
├── pyproject.toml         # Project configuration
└── requirements.txt       # Dependencies
```

## Instructions

### Step 1: Gather Project Requirements

Before initialization, define:

```
Project Details:
- Name: [project_name]
- Description: [one-line summary]
- Type: [CLI tool / Web API / Library / Data Science]
- Author: [name and email]

Dependencies:
- Core: [pandas, requests, etc.]
- Dev: [pytest, black, mypy]

Features:
- [Key capability 1]
- [Key capability 2]
```

### Step 2: Create Directory Structure

```bash
# Create project root
mkdir project_name && cd project_name

# Create directories
mkdir -p src/core/utils
mkdir -p tests
mkdir -p docs
mkdir -p .github/workflows

# Create __init__.py files
touch src/__init__.py
touch src/core/__init__.py
touch src/core/utils/__init__.py
touch tests/__init__.py
```

### Step 3: Create pyproject.toml

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
authors = [{name = "Your Name", email = "your.email@example.com"}]
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
keywords = ["python", "tool"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    # Add core dependencies here
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=22.0",
    "flake8>=4.0",
    "mypy>=0.950",
    "isort>=5.10",
    "pre-commit>=2.20"
]

[project.scripts]
project-name = "src.main:main"

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88
known_first_party = ["src"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --cov=src --cov-report=html --cov-report=term"
filterwarnings = [
    "ignore::DeprecationWarning"
]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError"
]
```

### Step 4: Create Main Entry Point

```python
# src/main.py
"""
Project Name - Main Entry Point

Description of what this project does.

Authors:
    - Your Name (your.email@example.com)
"""
import sys
from typing import Optional


def main(args: Optional[list] = None) -> int:
    """
    Main entry point for the application.

    Parameters:
        args: Command-line arguments (defaults to sys.argv)

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    if args is None:
        args = sys.argv[1:]

    print("Project Name v0.1.0")
    print("=" * 50)
    print("Project initialized successfully!")
    print("\nNext steps:")
    print("1. Implement core functionality in src/core/")
    print("2. Add tests in tests/")
    print("3. Update documentation")
    print("4. Run 'python tests/run_all_tests.py' to verify")

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### Step 5: Create Test Framework

```python
# tests/run_all_tests.py
"""
Master test runner for Project Name.

Authors:
    - Your Name (your.email@example.com)
"""
import sys
import unittest
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main():
    """Run all test suites and report results."""
    print("=" * 100)
    print(" " * 20 + "PROJECT NAME - FULL TEST SUITES RUNNER")
    print("─" * 100)
    print(f"Test execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print()
    print("=" * 100)
    print(" " * 30 + "TEST EXECUTION SUMMARY")
    print("─" * 100)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("─" * 100)

    if result.wasSuccessful():
        print("FINAL TESTS STATUS: ✅  All tests passed")
    else:
        print("FINAL TESTS STATUS: ❌  Some tests failed")

    print("=" * 100)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
```

```python
# tests/test_main.py
"""Tests for main module."""
import unittest
from src.main import main


class TestMain(unittest.TestCase):
    """Test cases for main entry point."""

    def test_main_returns_zero(self):
        """Test that main returns 0 on success."""
        result = main([])
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
```

### Step 6: Create Documentation

```markdown
# README.md

# Project Name - v0.1.0

## What's New
- Initial release

## Overview
Brief description of the project purpose.

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation

### Prerequisites
- Python 3.9+
- pip

### Setup
```bash
git clone <repository-url>
cd project-name
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Usage
```bash
python src/main.py
```

## Development

### Running Tests
```bash
pytest
python tests/run_all_tests.py
```

### Code Quality
```bash
black src/ tests/
isort src/ tests/
mypy src/
flake8 src/ tests/
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests
5. Submit pull request

## License
MIT
```

### Step 7: Create .gitignore

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
ENV/

# Distribution / packaging
dist/
build/
*.egg-info/
*.egg

# Test / coverage
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
*.tmp
.env
```

### Step 8: Set Up Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Unix/Mac)
source .venv/bin/activate

# Install dependencies
python -m pip install -e ".[dev]"

# Verify installation
python -m pip list
```

### Step 9: Verify Setup

```bash
# Run tests
pytest tests/

# Format code
black src/ tests/

# Check types
mypy src/

# Lint
flake8 src/ tests/

# Run application
python src/main.py
```

### Step 10: Initialize Git

```bash
git init
git add .
git commit -m "Initial project structure"
```

## Project Type Variations

### CLI Tool
```toml
dependencies = [
    "click>=8.0",
    "rich>=12.0"
]
```

### Web API (FastAPI)
```toml
dependencies = [
    "fastapi>=0.100",
    "uvicorn>=0.22",
    "pydantic>=2.0",
    "sqlalchemy>=2.0"
]
```

Additional structure:
```
src/
├── api/
│   ├── routes/
│   └── middleware/
├── models/
├── schemas/
└── services/
```

### Data Science
```toml
dependencies = [
    "pandas>=2.0",
    "numpy>=1.24",
    "matplotlib>=3.7",
    "jupyter>=1.0",
    "scikit-learn>=1.2"
]
```

Additional structure:
```
project/
├── notebooks/
├── data/
│   ├── raw/
│   └── processed/
└── models/
```

### Library/Package
```toml
[project]
name = "my-library"

[project.optional-dependencies]
docs = ["sphinx", "sphinx-rtd-theme"]
```

Additional files:
- LICENSE
- MANIFEST.in
- docs/conf.py

## Quality Checklist

- [ ] Directory structure created
- [ ] pyproject.toml configured
- [ ] Virtual environment set up
- [ ] Dependencies installed
- [ ] Tests pass
- [ ] Linting passes
- [ ] Documentation complete
- [ ] Git initialized
- [ ] README accurate
- [ ] CHANGELOG started

## Related Skills

- `test-structure` - Set up comprehensive testing
- `docstrings` - Add documentation
- `python-cleanup` - Code cleanup
- `code-commit-workflow` - Git workflow

---

**Version**: 1.0.0
**Last Updated**: December 2025


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
