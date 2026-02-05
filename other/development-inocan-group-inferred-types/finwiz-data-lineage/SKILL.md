---
name: finwiz-data-lineage
description: "Ensures complete traceability of financial calculations from raw data to final output. Use when implementing calculations, scoring systems, or any data transformations that need audit trails for regulatory compliance and debugging."
allowed-tools: ["Read", "Edit", "Bash"]
---

# FinWiz Data Lineage Standards

**Core Principle**: Every calculation must be traceable from raw data source to final output.

All financial calculations, scores, and recommendations in FinWiz must track complete lineage for reproducibility, debugging, validation, and regulatory compliance.

## Why Data Lineage Matters

- **Reproducibility**: Recreate any calculation from source data
- **Debugging**: Trace errors back to their origin  
- **Validation**: Verify calculation correctness at each step
- **Audit Trail**: Demonstrate compliance with financial regulations
- **Transparency**: Show users how recommendations were derived

## Required Lineage Components

### 1. Data Source Attribution

Every data point must include source information:

```python
from finwiz.schemas.data_lineage import DataSource

source = DataSource(
    provider="yahoo_finance",           # API/service name
    endpoint="/v8/finance/quote",       # Specific endpoint
    timestamp=datetime.now(UTC),        # When data was fetched
    parameters={"symbol": "AAPL"},      # Request parameters
    raw_response_hash="abc123..."       # Hash of raw response
)
```

### 2. Calculation Lineage

Track every transformation step:

```python
from finwiz.schemas.data_lineage import CalculationStep

step = CalculationStep(
    operation="calculate_sharpe_ratio",
    inputs={
        "returns": [0.01, 0.02, -0.01],
        "risk_free_rate": 0.04
    },
    output=1.25,
    formula="(mean_return - risk_free_rate) / std_dev",
    timestamp=datetime.now(UTC)
)
```

### 3. Score Derivation

Document how composite scores are computed:

```python
from finwiz.schemas.data_lineage import ScoreLineage

lineage = ScoreLineage(
    final_score=0.85,
    component_scores={
        "fundamental": 0.90,
        "technical": 0.80,
        "sentiment": 0.85
    },
    weights={
        "fundamental": 0.40,
        "technical": 0.35,
        "sentiment": 0.25
    },
    calculation_steps=[step1, step2, step3],
    data_sources=[source1, source2]
)
```

## Implementation Patterns

### ✅ CORRECT: Lineage-Aware Data Extraction

```python
from finwiz.utils.data_extractor import extract_with_lineage

# Tracks data source automatically
result = extract_with_lineage(
    data=api_response,
    path="financialData.currentPrice",
    source=DataSource(provider="yahoo_finance", ...)
)

# Access both value and lineage
price = result.value
lineage = result.lineage
```

### ✅ CORRECT: Calculation with Lineage

```python
from finwiz.scoring.deep_analysis_scorer import calculate_with_lineage

# Tracks calculation steps automatically
score_result = calculate_with_lineage(
    operation="composite_score",
    inputs={
        "fundamental_score": 0.90,
        "technical_score": 0.80
    },
    weights={"fundamental": 0.6, "technical": 0.4}
)

final_score = score_result.value
calculation_steps = score_result.lineage.calculation_steps
```

### ❌ WRONG: No Lineage Tracking

```python
# Missing data source tracking
price = api_response["financialData"]["currentPrice"]

# Missing calculation lineage
final_score = 0.90 * 0.6 + 0.80 * 0.4

# Hardcoded values without source
RISK_FREE_RATE = 0.04  # Where did this come from?
```

## Schema Integration

### All Analysis Results Must Include Lineage

```python
from pydantic import BaseModel
from finwiz.schemas.data_lineage import DataLineage

class StockAnalysis(BaseModel):
    ticker: str
    recommendation: str
    composite_score: float
    lineage: DataLineage  # REQUIRED for all analysis results
```

### Lineage Validation

```python
from finwiz.schemas.data_lineage import validate_lineage

# Validate lineage completeness before saving
validate_lineage(
    analysis.lineage,
    require_sources=True,
    require_calculations=True,
    require_timestamps=True
)
```

## Anti-Patterns to Avoid

### ❌ Hardcoded Values

```python
# WRONG - No source tracking
RISK_FREE_RATE = 0.04
composite_score = fundamental * 0.6 + technical * 0.4

# CORRECT - Source everything
risk_free_rate = get_risk_free_rate_with_lineage(source="fred", series="DGS10")
weights = get_scoring_weights_with_lineage(asset_class="stock", strategy="balanced")
```

### ❌ Missing Calculation Steps

```python
# WRONG - Black box calculation
final_score = complex_calculation(data)

# CORRECT - Track each step
step1 = calculate_with_lineage("normalize_data", inputs={"data": data})
step2 = calculate_with_lineage("apply_weights", inputs={"normalized": step1.value})
final_score = step2.value
```

## Lineage in Reports

### Include Data Sources in HTML Reports

```html
<section class="data-lineage">
    <h3>📊 Data Sources</h3>
    <ul>
        <li>Yahoo Finance (2025-10-29 14:30 UTC)</li>
        <li>Alpha Vantage (2025-10-29 14:25 UTC)</li>
    </ul>
    
    <h3>🔢 Calculation Method</h3>
    <p>Composite Score = (Fundamental × 0.60) + (Technical × 0.40)</p>
    
    <h3>⏱️ Analysis Timestamp</h3>
    <p>2025-10-29 14:35:22 UTC</p>
</section>
```

### Export for Auditing

```python
# Export complete lineage to JSON for audit trail
lineage_json = analysis.lineage.model_dump_json(indent=2)
with open(f"lineage/{ticker}_{timestamp}.json", "w") as f:
    f.write(lineage_json)
```

## Testing Requirements

### Test Lineage Tracking

```python
def test_should_track_data_source_lineage(mocker):
    """Verify data extraction includes source lineage."""
    mock_api = mocker.patch('finwiz.tools.yahoo_finance_tool.get_data')
    mock_api.return_value = {"price": 150.0}
    
    result = extract_with_lineage(
        data=mock_api.return_value,
        path="price",
        source=DataSource(provider="yahoo_finance")
    )
    
    assert result.value == 150.0
    assert result.lineage.source.provider == "yahoo_finance"
    assert result.lineage.source.timestamp is not None

def test_should_track_calculation_lineage(mocker):
    """Verify calculations include step-by-step lineage."""
    result = calculate_with_lineage(
        operation="sharpe_ratio",
        inputs={"returns": [0.01, 0.02], "risk_free_rate": 0.04}
    )
    
    assert result.value > 0
    assert len(result.lineage.calculation_steps) > 0
    assert result.lineage.calculation_steps[0].operation == "sharpe_ratio"
```

## Compliance Checklist

Before committing code with calculations:

- [ ] **Data sources documented**: All inputs have DataSource attribution
- [ ] **Calculations tracked**: All transformations have CalculationStep records  
- [ ] **Timestamps included**: All lineage components have timestamps
- [ ] **No hardcoded values**: All constants sourced with lineage
- [ ] **Lineage validated**: `validate_lineage()` passes
- [ ] **Lineage exported**: JSON export available for auditing
- [ ] **Tests include lineage**: Unit tests verify lineage tracking
- [ ] **Reports show lineage**: HTML reports include data sources

## Benefits

✅ **Regulatory Compliance**: Demonstrate calculation transparency  
✅ **Debugging Efficiency**: Trace errors to source quickly  
✅ **Reproducibility**: Recreate any analysis from lineage  
✅ **User Trust**: Show users how recommendations were derived  
✅ **Quality Assurance**: Validate calculations at each step  
✅ **Audit Trail**: Complete history of data and calculations

Remember: If you can't trace how a number was calculated, it shouldn't be in a FinWiz report.