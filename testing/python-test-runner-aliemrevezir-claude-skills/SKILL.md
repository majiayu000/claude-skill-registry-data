---
name: python-test-runner
description: >
  Run and debug Python test pipelines using pytest or unittest. Handles dependency
  installation, test path selection, coverage reporting, and failure analysis. Also
  validates AI tool integrations by checking environment variables, API keys, and
  performing health checks for OpenAI, Anthropic, Google/Gemini, and custom proxy
  endpoints. Use when the user asks to run tests, check CI, measure coverage,
  troubleshoot failing test suites, or verify AI API configuration in Python projects.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            if echo "$TOOL_INPUT" | grep -qE "pytest|python -m unittest"; then
              if ! command -v pytest >/dev/null 2>&1 && echo "$TOOL_INPUT" | grep -q "pytest"; then
                echo "⚠️  pytest not found - install with: pip install pytest pytest-cov"
                exit 1
              fi
            fi
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            if echo "$TOOL_INPUT" | grep -qE "pytest|python -m unittest"; then
              echo "✓ Test execution completed - check output above for results"
            fi
---

# Python Test Runner & AI Integration Validator

You are helping the user run and debug Python test suites (pytest/unittest) and validate AI tool integrations.

## Core Capabilities

1. **Test Execution**: Run pytest or unittest with coverage reporting
2. **Dependency Management**: Install test dependencies when needed
3. **Failure Analysis**: Parse and summarize test failures
4. **AI Integration Validation**: Check API keys and health of AI services

## Step-by-Step Instructions

### 1. Initial Assessment

When the user asks to run tests:

1. Check if this is a Python project (look for `setup.py`, `pyproject.toml`, `requirements.txt`, or `tests/` directory)
2. Identify the test framework:
   - Look for `pytest.ini`, `pyproject.toml` with pytest config, or `tests/` with pytest-style files → use pytest
   - Look for unittest-style test files → use unittest
3. Check for existing test configuration files

### 2. Dependency Installation

Before running tests, check if dependencies are installed:

```bash
# Check if pytest is available
python -m pytest --version 2>/dev/null || echo "pytest not installed"

# If pytest is missing and needed, install it
pip install pytest pytest-cov
```

For projects with dependency files:
```bash
# Install from requirements
pip install -r requirements-test.txt  # or requirements.txt, or requirements-dev.txt

# Or from pyproject.toml
pip install -e ".[test]"
```

### 3. Running Tests

**Default approach**: Run all tests with coverage

```bash
# pytest with coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing

# unittest with coverage
python -m coverage run -m unittest discover -s tests -v
python -m coverage report -m
```

**Selective testing**: If user specifies paths or patterns

```bash
# Specific test file
python -m pytest tests/test_specific.py -v

# Specific test function
python -m pytest tests/test_file.py::test_function -v

# Pattern matching
python -m pytest -k "test_pattern" -v
```

**Useful pytest flags**:
- `-v` or `-vv`: Verbose output
- `-x`: Stop on first failure
- `--lf`: Run last failed tests
- `--tb=short`: Shorter traceback format
- `-s`: Show print statements

### 4. Analyzing Test Failures

When tests fail:

1. **Extract failure information**:
   - Test name and location
   - Assertion error message
   - Relevant traceback lines
   - Expected vs actual values

2. **Summarize for the user**:
   ```
   Test Failures Summary:
   ----------------------
   1. tests/test_auth.py::test_login_invalid_credentials
      - AssertionError: Expected 401, got 200
      - Location: tests/test_auth.py:45
   
   2. tests/test_api.py::test_rate_limiting
      - Timeout: Request took 31s (limit: 30s)
      - Location: tests/test_api.py:78
   ```

3. **Suggest next steps**:
   - Read the failing test file to understand the test logic
   - Check recent changes that might have caused the failure
   - Review logs or error messages for more context

### 5. AI Integration Validation

When the user asks to validate AI tool integrations or when AI-related tests fail:

#### Step 5.1: Check Environment Variables

```bash
# Check which AI providers are configured
echo "=== AI Provider Configuration ==="
[ -n "$OPENAI_API_KEY" ] && echo "✓ OpenAI API key found" || echo "✗ OpenAI API key missing"
[ -n "$ANTHROPIC_API_KEY" ] && echo "✓ Anthropic API key found" || echo "✗ Anthropic API key missing"
[ -n "$GOOGLE_API_KEY" ] && echo "✓ Google/Gemini API key found" || echo "✗ Google API key missing"
[ -n "$GEMINI_API_KEY" ] && echo "✓ Gemini API key found" || echo "✗ Gemini API key missing"

# Check for custom endpoints
[ -n "$OPENAI_BASE_URL" ] && echo "ℹ Custom OpenAI endpoint: $OPENAI_BASE_URL"
[ -n "$ANTHROPIC_BASE_URL" ] && echo "ℹ Custom Anthropic endpoint: $ANTHROPIC_BASE_URL"
```

#### Step 5.2: Perform Health Checks

Create a temporary health check script:

```python
# /tmp/ai_health_check.py
import os
import sys

def check_openai():
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Lightweight call - just list models
        models = client.models.list()
        print("✓ OpenAI: Connected successfully")
        print(f"  Default model: gpt-4 (or gpt-3.5-turbo)")
        return True
    except ImportError:
        print("✗ OpenAI: Package not installed (pip install openai)")
        return False
    except Exception as e:
        print(f"✗ OpenAI: Connection failed - {str(e)}")
        return False

def check_anthropic():
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # Minimal API call - count tokens
        response = client.messages.count_tokens(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": "test"}]
        )
        print("✓ Anthropic: Connected successfully")
        print(f"  Default model: claude-3-5-sonnet-20241022")
        return True
    except ImportError:
        print("✗ Anthropic: Package not installed (pip install anthropic)")
        return False
    except Exception as e:
        print(f"✗ Anthropic: Connection failed - {str(e)}")
        return False

def check_google():
    try:
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        # List models as health check
        models = genai.list_models()
        print("✓ Google/Gemini: Connected successfully")
        print(f"  Default model: gemini-pro")
        return True
    except ImportError:
        print("✗ Google/Gemini: Package not installed (pip install google-generativeai)")
        return False
    except Exception as e:
        print(f"✗ Google/Gemini: Connection failed - {str(e)}")
        return False

if __name__ == "__main__":
    print("=== AI Provider Health Checks ===\n")
    results = []
    
    if os.getenv("OPENAI_API_KEY"):
        results.append(check_openai())
    
    if os.getenv("ANTHROPIC_API_KEY"):
        results.append(check_anthropic())
    
    if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
        results.append(check_google())
    
    if not results:
        print("⚠️  No AI provider API keys found in environment")
        sys.exit(1)
    
    if all(results):
        print("\n✓ All configured providers are healthy")
        sys.exit(0)
    else:
        print("\n✗ Some providers failed health checks")
        sys.exit(1)
```

Run the health check:
```bash
python /tmp/ai_health_check.py
```

#### Step 5.3: Report Configuration

Summarize the AI integration status:
```
AI Integration Status:
---------------------
✓ OpenAI configured (gpt-4)
✓ Anthropic configured (claude-3-5-sonnet-20241022)
✗ Google/Gemini not configured
ℹ Custom endpoint: https://api.custom-proxy.com/v1
```

### 6. Coverage Reporting

After running tests with coverage:

```bash
# Generate detailed coverage report
python -m coverage report -m

# For HTML report (optional)
python -m coverage html
echo "HTML coverage report generated in htmlcov/index.html"
```

Interpret coverage results:
- **90%+**: Excellent coverage
- **70-90%**: Good coverage
- **50-70%**: Moderate coverage, consider adding tests
- **<50%**: Low coverage, significant gaps

## Common Workflows

### Workflow 1: Run All Tests with Coverage
```bash
# Install dependencies
pip install pytest pytest-cov

# Run tests
python -m pytest tests/ -v --cov=. --cov-report=term-missing

# Summarize results for user
```

### Workflow 2: Debug Failing Tests
```bash
# Run only failed tests with verbose output
python -m pytest --lf -vv

# Read the failing test file to understand what's being tested
# Analyze the error and suggest fixes
```

### Workflow 3: Validate AI Integration
```bash
# Check environment variables
env | grep -E "OPENAI|ANTHROPIC|GOOGLE|GEMINI"

# Run health check script
python /tmp/ai_health_check.py

# Report status to user
```

### Workflow 4: CI/CD Simulation
```bash
# Simulate CI pipeline
pip install -r requirements-test.txt
python -m pytest tests/ -v --cov=. --cov-report=xml --cov-report=term
python -m pylint src/
python -m black --check src/

# Report CI status
```

## Examples

### Example 1: User asks "run the tests"

1. Check for test framework → found pytest
2. Install dependencies: `pip install pytest pytest-cov`
3. Run tests: `python -m pytest tests/ -v --cov=. --cov-report=term-missing`
4. Parse output and report: "15 tests passed, 2 failed. Coverage: 78%"
5. Summarize failures if any

### Example 2: User asks "why are the AI tests failing?"

1. Run the AI-specific tests: `python -m pytest tests/test_ai_integration.py -v`
2. Check environment: Look for API keys
3. Run health check script
4. Report: "OpenAI API key is missing. Set OPENAI_API_KEY environment variable."

### Example 3: User asks "check if our Anthropic integration is working"

1. Verify `ANTHROPIC_API_KEY` is set
2. Run health check for Anthropic
3. Report: "✓ Anthropic: Connected successfully. Using claude-3-5-sonnet-20241022"

## Important Notes

- **Always install pytest-cov** if running pytest with coverage
- **Respect .env files**: If present, suggest loading them: `source .env` or use `python-dotenv`
- **Security**: Never log or display full API keys - only confirm presence
- **Timeouts**: Some AI health checks may be slow - warn user if taking >10s
- **Custom proxies**: Respect `*_BASE_URL` environment variables for custom endpoints
- **Test isolation**: Suggest using `-x` flag to stop on first failure for faster debugging

## Error Handling

If tests fail to run:
1. Check Python version compatibility
2. Verify all dependencies are installed
3. Look for syntax errors in test files
4. Check for missing test fixtures or data files
5. Ensure test discovery patterns are correct

If AI health checks fail:
1. Verify API key format (not empty, not placeholder)
2. Check network connectivity
3. Verify the AI package version is compatible
4. Look for rate limiting or quota issues
5. Check custom endpoint URLs if configured