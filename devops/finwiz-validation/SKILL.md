---
name: finwiz-validation
description: "FinWiz data validation standards using Pydantic v2 strict mode. Use when creating schemas, validating data, or implementing quality standards for financial analysis outputs."
allowed-tools: ["Read", "Edit"]
---

# FinWiz Validation Standards

Data validation rules and quality standards for FinWiz development using Pydantic v2 strict mode.

## Core Validation Principles

### 1. Schema Compliance

- Use strict Pydantic v2 models with `extra='forbid'`
- All outputs must conform to registered schemas
- Validate at crew boundaries
- Provide field-level error context

### 2. Validation Modes

Configure via `VALIDATION_STRICTNESS` environment variable:

- `off`: Validation disabled (development only)
- `warn`: Errors converted to warnings, processing continues (default)
- `error`: Strict enforcement, halt on validation errors (production)

### 3. Risk Assessment Standards

- Use `RiskAssessmentStandardized` schema
- 0-5 scale scoring (0=Very Low, 5=Very High)
- Include systematic and idiosyncratic risk components
- Follow standardized risk taxonomy

## Pydantic v2 Patterns

### Standard Model Pattern

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class StockAnalysis(BaseModel):
    """Stock analysis with strict validation."""
    
    model_config = {
        "extra": "forbid",           # Reject unknown fields
        "str_strip_whitespace": True, # Auto-clean strings
        "validate_assignment": True,  # Validate on assignment
        "use_enum_values": True      # Use enum values, not names
    }
    
    ticker: str = Field(..., pattern=r'^[A-Z]{1,5}$', description="Stock ticker symbol")
    recommendation: Literal["BUY", "HOLD", "SELL"] = Field(..., description="Investment recommendation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level 0-1")
    risk_score: int = Field(..., ge=1, le=10, description="Risk score 1-10")
    
    @field_validator('ticker')
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError('Ticker must contain only letters')
        return v.upper()
```

### Input Validation Pattern

```python
class TickerInput(BaseModel):
    """Validate ticker input with strict rules."""
    
    model_config = {
        "str_strip_whitespace": True,
        "str_upper": True,
        "extra": "forbid"
    }
    
    symbol: str = Field(..., pattern=r'^[A-Z]{1,5}$')
    
    @field_validator('symbol')
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError('Ticker must contain only letters')
        return v.upper()
```

## Validation Manager Usage

```python
from finwiz.validation import get_validation_manager

manager = get_validation_manager()

# Validate crew output
result = manager.validate_crew_output(data, "stock", "analysis")

if result.is_valid:
    processed_data = result.sanitized_data
else:
    for error in result.errors:
        logger.error(f"Validation error at {error.field_path}: {error.message}")
```

## Schema Registry

All schemas must be registered:

```python
from finwiz.validation import get_registry

registry = get_registry()

# Register crew schema
registry.register_crew_schema("stock", "analysis", TenKInsight)

# Lookup schema
schema = registry.get_schema("TenKInsight")
```

## A+ Investment Validation Criteria

### Backtesting Requirements (25% weight)

- **Minimum Period**: 5 years historical data
- **Market Regimes**: Test across bull, bear, sideways markets
- **Minimum Return**: 8% annualized
- **Rejection**: <8% annual return

### Risk-Adjusted Performance (20% weight)

- **Sharpe Ratio**: Minimum 1.0
- **Sortino Ratio**: Downside risk assessment
- **Calmar Ratio**: Risk-adjusted with max drawdown
- **Rejection**: Sharpe <1.0

### Downside Risk Control (20% weight)

- **Maximum Drawdown**: -25% maximum
- **Value at Risk**: 95% confidence level
- **Expected Shortfall**: Tail risk assessment
- **Rejection**: Max drawdown >-25%

### Consistency Requirements (15% weight)

- **Win Rate**: Minimum 45%
- **Trade Consistency**: Across time periods
- **Performance Stability**: Across market conditions
- **Rejection**: Win rate <45%

### Regime Consistency (20% weight)

- **Multi-Regime Performance**: Reasonable across all regimes
- **Minimum Consistency**: 60% score
- **Regime Analysis**: Bull, bear, sideways markets
- **Rejection**: Consistency <60%

### Overall Validation

- **Passing Threshold**: 70% overall score
- **Grade Assignment**: Only ≥70% receive A+ recommendations

## Asset-Specific Validation

### ETFs

```python
class ETFValidation(BaseModel):
    tracking_error: float = Field(..., le=0.20, description="≤0.20% (3-year)")
    expense_ratio: float = Field(..., le=0.25, description="≤0.15% (broad) or ≤0.25% (specialized)")
    aum: float = Field(..., ge=1e9, description="≥$1B")
    ucits_compliant: bool = Field(..., description="UCITS compliant for European investors")
```

### Stocks

```python
class StockValidation(BaseModel):
    roe: float = Field(..., ge=0.20, description="≥20%")
    revenue_growth: float = Field(..., ge=0.15, description="≥15% annually")
    debt_equity_ratio: float = Field(..., le=0.3, description="≤0.3")
    free_cash_flow_positive: bool = Field(..., description="Positive and growing")
```

### Crypto

```python
class CryptoValidation(BaseModel):
    market_cap: float = Field(..., ge=10e9, description="≥$10B")
    daily_volume: float = Field(..., ge=500e6, description="≥$500M")
    operating_years: int = Field(..., ge=3, description="≥3 years")
    regulatory_compliance: bool = Field(..., description="Clear compliance pathway")
```

## Data Quality Standards

### Required Fields Validation

```python
class DataQuality(BaseModel):
    """Ensure all required fields are present and valid."""
    
    model_config = {"extra": "forbid"}
    
    # All required fields must be present
    required_field: str = Field(..., min_length=1)
    
    # No null values for required fields
    non_null_field: str = Field(..., description="Cannot be null")
    
    # Proper data types enforced
    numeric_field: float = Field(..., description="Must be numeric")
    
    # Valid enum values only
    status: Literal["active", "inactive"] = Field(..., description="Valid status only")
```

### Data Freshness Validation

```python
from datetime import datetime, timedelta

class DataFreshness(BaseModel):
    """Validate data timestamps and freshness."""
    
    timestamp: datetime = Field(..., description="Data timestamp")
    
    @field_validator('timestamp')
    @classmethod
    def validate_freshness(cls, v: datetime) -> datetime:
        if datetime.now() - v > timedelta(days=30):
            raise ValueError('Data is stale (>30 days old)')
        return v
```

### Data Sources Validation

```python
class DataSources(BaseModel):
    """Validate data source citations."""
    
    sources: list[str] = Field(..., min_length=1, description="At least one source required")
    as_of_dates: list[datetime] = Field(..., description="As-of dates for each source")
    urls: list[str] = Field(default=[], description="Source URLs where applicable")
    limitations: list[str] = Field(default=[], description="Data limitations")
    
    @field_validator('as_of_dates')
    @classmethod
    def validate_dates_match_sources(cls, v, info):
        sources = info.data.get('sources', [])
        if len(v) != len(sources):
            raise ValueError('Must have as-of date for each source')
        return v
```

## Error Handling

### Validation Error Model

```python
class ValidationError(BaseModel):
    """Structured validation error information."""
    
    field_path: str = Field(..., description="Path to the field with error")
    message: str = Field(..., description="Human-readable error message")
    error_type: str = Field(..., description="Type of validation error")
    context: dict = Field(default={}, description="Additional error context")
```

### Error Response Pattern

```python
def handle_validation_error(error: ValidationError) -> dict:
    """Handle validation errors with clear messaging."""
    
    response = {
        "error": True,
        "field": error.field_path,
        "message": error.message,
        "suggestion": get_remediation_suggestion(error.error_type),
        "context": error.context
    }
    
    # Log for debugging
    logger.error(f"Validation failed: {error.field_path} - {error.message}")
    
    return response
```

### Graceful Degradation

```python
def validate_with_fallback(data: dict, schema: type[BaseModel]) -> BaseModel:
    """Validate with graceful degradation."""
    
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        
        # Use cached data if available
        cached_data = get_cached_data()
        if cached_data:
            return schema.model_validate(cached_data)
        
        # Fall back to baseline analysis
        return create_baseline_analysis()
```

## Validation Checklist

Before accepting any data:

1. ✅ **Schema Validation**: Conforms to Pydantic model
2. ✅ **Required Fields**: All required fields present
3. ✅ **Data Types**: Correct types for all fields
4. ✅ **Value Ranges**: Within acceptable ranges
5. ✅ **Enum Values**: Valid enum selections
6. ✅ **Data Freshness**: Within freshness threshold
7. ✅ **Risk Assessment**: Standardized 0-5 scale
8. ✅ **Citations**: All sources cited
9. ✅ **Completeness**: No missing critical data
10. ✅ **Consistency**: Internally consistent data

## Rejection Documentation

When rejecting data/recommendations:

1. **Specific Reason**: Clear rejection reason
2. **Quantitative Evidence**: Numerical backing
3. **Threshold Violated**: Which threshold failed
4. **Alternative Suggestions**: Improvements needed
5. **Audit Trail**: Log all rejections

## Common Validation Patterns

### CrewAI Output Validation

```python
@task
def analysis_task(self) -> Task:
    return Task(
        description="Analyze stock with validation",
        expected_output="Validated StockAnalysis object",
        output_pydantic=StockAnalysis,  # Automatic validation
        output_json=True,               # Machine-readable format
        agent=self.analyst()
    )
```

### Manual Validation

```python
def validate_analysis_result(data: dict) -> StockAnalysis:
    """Manually validate analysis result."""
    
    try:
        return StockAnalysis.model_validate(data)
    except ValidationError as e:
        logger.error(f"Analysis validation failed: {e}")
        raise ValueError(f"Invalid analysis data: {e}")
```

Apply these validation standards consistently across all FinWiz data processing and analysis workflows.
