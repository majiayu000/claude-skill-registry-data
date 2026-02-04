---
name: finwiz-security
description: "Security and type safety standards for FinWiz including API key management, input validation, and mypy strict mode. Use when handling sensitive data, API keys, or implementing type safety."
allowed-tools: ["Read", "Edit"]
---

# FinWiz Security & Type Safety Standards

Critical security practices and type safety requirements for FinWiz development.

## Type Safety (mypy strict mode)

### Required Type Annotations

All public functions and methods MUST have complete type annotations:

```python
# ✅ CORRECT
def analyze_stock(ticker: str, period: int = 365) -> StockAnalysis:
    return StockAnalysis(ticker=ticker, period=period)

def log_analysis(ticker: str) -> None:
    logger.info(f"Analyzing {ticker}")

# ❌ WRONG - Missing return type
def analyze_stock(ticker: str):
    return StockAnalysis(ticker=ticker)
```

### Type Annotation Rules

- Return type required (use `-> None` if no return)
- All parameters must have type hints
- Use modern Python 3.12+ syntax: `str | None` instead of `Optional[str]`
- Use `list[Type]` instead of `List[Type]`
- Use `# type: ignore` only with explanatory comment

## API Key Security (CRITICAL)

### Environment Variables Only

NEVER hardcode API keys:

```python
# ✅ CORRECT
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# ❌ WRONG - Hardcoded
api_key = "sk-proj-abc123..."
```

### Required Environment Variables

**Core APIs (Required):**

- `OPENAI_API_KEY` - OpenAI API
- `SERPER_API_KEY` - Serper search
- `FIRECRAWL_API_KEY` - Web scraping
- `ALPHA_VANTAGE_API_KEY` - Financial data

**Enhanced Features (Optional):**

- `TWELVE_DATA_API_KEY` - Market data (technical analysis)
- `PPLX_API_KEY` - Perplexity search (enhanced research)
- `SEC_API_API_KEY` - SEC filings (optional)
- `CHART_IMG_API_KEY` - Chart generation
- `COINMARKETCAP_API_KEY` - Cryptocurrency data

### Logging Security

NEVER log full API keys:

```python
# ✅ CORRECT - Masked (first 8 chars only)
logger.info(f"Using API key: {api_key[:8]}...")

# ❌ WRONG - Full key exposed
logger.info(f"API key: {api_key}")
```

## Input Validation (Pydantic v2 strict)

### All External Inputs Must Be Validated

```python
from pydantic import BaseModel, Field, field_validator

class TickerInput(BaseModel):
    """Validate ticker input with strict security."""
    
    model_config = {
        "str_strip_whitespace": True,
        "str_upper": True,
        "extra": "forbid"  # Reject unknown fields
    }
    
    symbol: str = Field(..., pattern=r'^[A-Z]{1,5}$')
    
    @field_validator('symbol')
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError('Ticker must contain only letters')
        return v.upper()
```

### Validation Requirements

- `extra='forbid'` - Reject unknown fields
- `Field()` constraints - pattern, min_length, ge, le
- `@field_validator` - Complex validation logic
- Sanitize inputs - Strip whitespace, normalize case
- Clear error messages - Actionable feedback

## Data Privacy

### Never Log Personal Financial Data

```python
# ✅ CORRECT - Anonymized
logger.info(f"Analyzing portfolio with {len(holdings)} holdings")

# ❌ WRONG - Exposes personal data
logger.info(f"Analyzing portfolio: {holdings}")
```

### Error Messages

Generic to users, detailed internally:

```python
# ✅ CORRECT
try:
    result = api_call(ticker)
except Exception as e:
    logger.error(f"API call failed for {ticker}: {e}", exc_info=True)
    raise ValueError("Unable to fetch data. Please try again later.")

# ❌ WRONG - Exposes internals
except Exception as e:
    raise ValueError(f"API call to {api_url} failed: {e}")
```

## Rate Limiting & Timeouts

### Rate Limiting (Required)

```python
from finwiz.utils.rate_limiter import RateLimiter

limiter = RateLimiter(max_calls=20, period=60)

@limiter.limit
async def fetch_stock_data(ticker: str) -> dict:
    return await api_client.get(f"/stock/{ticker}")
```

### Timeouts (Required)

Always set explicit timeouts:

```python
# ✅ CORRECT
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url)

# ❌ WRONG - Can hang indefinitely
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

## Secure Coding Patterns

### SQL Injection Prevention

```python
# ✅ CORRECT - Parameterized queries
cursor.execute(
    "SELECT * FROM stocks WHERE ticker = %s",
    (ticker,)
)

# ❌ WRONG - SQL injection risk
cursor.execute(f"SELECT * FROM stocks WHERE ticker = '{ticker}'")
```

### Path Traversal Prevention

```python
from pathlib import Path

# ✅ CORRECT - Validate paths
def read_report(filename: str) -> str:
    # Validate filename
    if not filename.replace('-', '').replace('_', '').isalnum():
        raise ValueError("Invalid filename")
    
    # Resolve path safely
    base_path = Path("reports")
    file_path = (base_path / filename).resolve()
    
    # Ensure path is within base directory
    if not str(file_path).startswith(str(base_path.resolve())):
        raise ValueError("Path traversal attempt")
    
    return file_path.read_text()

# ❌ WRONG - Path traversal risk
def read_report(filename: str) -> str:
    with open(f"reports/{filename}") as f:
        return f.read()
```

### Command Injection Prevention

```python
import subprocess
import shlex

# ✅ CORRECT - Safe command execution
def run_analysis(ticker: str) -> str:
    # Validate input
    if not ticker.isalpha():
        raise ValueError("Invalid ticker")
    
    # Use list form (safer)
    result = subprocess.run(
        ["python", "analyze.py", ticker],
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout

# ❌ WRONG - Command injection risk
def run_analysis(ticker: str) -> str:
    result = subprocess.run(f"python analyze.py {ticker}", shell=True)
    return result.stdout
```

## Dependency Security

### Dependency Scanning

```bash
# Check for known vulnerabilities
uv audit

# Update dependencies regularly
uv sync --upgrade
```

### Secure Dependencies

- Keep dependencies updated
- Use dependency scanning tools
- Review third-party packages before adding
- Use lock files (uv.lock)
- Remove unused dependencies regularly

## Infrastructure Security

### HTTPS Configuration

```python
# ✅ CORRECT - Force HTTPS
import httpx

client = httpx.AsyncClient(
    verify=True,  # Verify SSL certificates
    timeout=30.0
)

# ❌ WRONG - Insecure connection
client = httpx.AsyncClient(verify=False)
```

### Secure Headers

```python
# Add security headers
headers = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
}
```

## Security Checklist

Before committing code:

- [ ] **API keys in environment variables only**
- [ ] **No sensitive data in logs** (mask keys, anonymize financial data)
- [ ] **All inputs validated** with Pydantic strict models
- [ ] **All public functions have type annotations**
- [ ] **Rate limiting configured** for API calls
- [ ] **Timeouts set** for all external requests (30s default)
- [ ] **Error messages generic** to users, detailed internally
- [ ] **No hardcoded credentials**
- [ ] **mypy passes** with no errors
- [ ] **Dependencies scanned** for vulnerabilities

## Quick Reference

| Security Concern | Solution |
|-----------------|----------|
| API keys | Environment variables + validation at startup |
| Sensitive logs | Mask keys (first 8 chars), anonymize financial data |
| Input validation | Pydantic v2 strict mode with `extra='forbid'` |
| Type safety | Full annotations, `mypy` strict mode |
| Rate limits | `RateLimiter` decorator, CrewAI `max_rpm=20` |
| Timeouts | `httpx.AsyncClient(timeout=30.0)` |
| Error messages | Generic to users, detailed to logs |
| SQL injection | Parameterized queries |
| Path traversal | Path validation and resolution |
| Command injection | List form subprocess calls |

## Development Practices

### Secure Development Lifecycle

- Use static code analysis tools (ruff, mypy)
- Implement security testing in CI/CD
- Code reviews for security issues
- Security training for developers
- Incident response procedures

### Monitoring and Logging

- Log security events (failed auth, suspicious activity)
- Monitor for unusual patterns
- Set up alerts for security incidents
- Regular security audits
- Penetration testing

Apply these security standards consistently across all FinWiz development to protect sensitive financial data and maintain system integrity.
