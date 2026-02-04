---
name: pydantic-model-generator
description: Auto-generate Pydantic models from schema descriptions with type hints, validation rules, examples, and JSON schema export. 75% token savings (2,000→500).
---

# Pydantic Model Generator

Generate standardized Pydantic models for LiquidationHeatmap data structures with complete type safety and validation.

## Quick Start

**User says**: "Create Pydantic model for TransactionOutput with amount, script_type, and timestamp"

**Skill generates**:
```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class TransactionOutput(BaseModel):
    """Bitcoin transaction output (UTXO)"""

    amount: Decimal = Field(
        ...,
        description="BTC amount in satoshis",
        ge=0,
        example=50000000
    )
    script_type: str = Field(
        ...,
        description="Script type (P2PKH, P2WPKH, P2SH, etc.)",
        example="P2WPKH"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When output was seen in mempool"
    )

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Amount must be non-negative')
        return v

    @validator('script_type')
    def script_type_must_be_valid(cls, v):
        valid_types = ['P2PKH', 'P2WPKH', 'P2SH', 'P2WSH', 'P2TR']
        if v not in valid_types:
            raise ValueError(f'Invalid script type: {v}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 50000000,
                "script_type": "P2WPKH",
                "timestamp": "2025-10-18T12:00:00Z"
            }
        }
```

## Templates

### 1. Basic Model Template
```python
from pydantic import BaseModel, Field
from typing import Optional

class {ModelName}(BaseModel):
    """{}"""

    {field_name}: {type} = Field(
        ...,
        description="{description}",
        example={example_value}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "{field_name}": {example_value}
            }
        }
```

### 2. Model with Validators
```python
from pydantic import BaseModel, Field, validator

class {ModelName}(BaseModel):
    """{}"""

    {field_name}: {type} = Field(..., ge=0)

    @validator('{field_name}')
    def {field_name}_validator(cls, v):
        if {condition}:
            raise ValueError('{error_message}')
        return v
```

### 3. Nested Model Template
```python
from pydantic import BaseModel
from typing import List

class {NestedModel}(BaseModel):
    """{}"""
    {nested_field}: {type}

class {ParentModel}(BaseModel):
    """{}"""

    items: List[{NestedModel}]
    count: int = Field(default=0)

    @property
    def total_items(self) -> int:
        return len(self.items)
```

### 4. WebSocket Message Template
```python
from pydantic import BaseModel, Field
from typing import Literal, Union
from datetime import datetime

class PriceUpdateMessage(BaseModel):
    """WebSocket price update message"""

    type: Literal["price_update"] = "price_update"
    price: float = Field(..., description="BTC/USD price estimate")
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HistogramMessage(BaseModel):
    """WebSocket histogram snapshot message"""

    type: Literal["histogram"] = "histogram"
    bins: dict = Field(..., description="Histogram bins")
    total_txs: int = Field(..., ge=0)

# Union type for all message types
WebSocketMessage = Union[PriceUpdateMessage, HistogramMessage]
```

### 5. Config Model Template
```python
from pydantic import BaseModel, Field, validator
from pathlib import Path
from typing import Optional

class {ConfigName}(BaseModel):
    """Configuration for {module}"""

    bitcoin_rpc_url: str = Field(
        default="http://127.0.0.1:8332",
        description="Bitcoin Core RPC endpoint"
    )
    zmq_endpoint: str = Field(
        default="tcp://127.0.0.1:28332",
        description="ZMQ rawtx endpoint"
    )
    data_dir: Path = Field(
        default=Path.home() / ".bitcoin",
        description="Bitcoin data directory"
    )

    @validator('data_dir')
    def data_dir_must_exist(cls, v):
        if not v.exists():
            raise ValueError(f'Data directory does not exist: {v}')
        return v

    class Config:
        validate_assignment = True
```

## Usage Patterns

### Pattern 1: From Schema Description
```
User: "Create model for PriceEstimate with price (float), confidence (0-1), and tx_count (int)"

Skill:
1. Parse field descriptions
2. Infer validators (confidence: 0-1 range)
3. Generate Field() with constraints
4. Add example data
5. Write to live/backend/models.py or live/shared/models.py
```

### Pattern 2: From Existing JSON
```
User: "Generate Pydantic model from this JSON: {...}"

Skill:
1. Parse JSON structure
2. Infer types from values
3. Generate model with Optional fields
4. Add validators for ranges/enums
5. Include original JSON as example
```

### Pattern 3: WebSocket Message Types
```
User: "Create WebSocket message models for price updates and histogram snapshots"

Skill:
1. Generate base message class
2. Create specific message types with Literal discriminators
3. Use Union type for message dispatch
4. Add type="message_type" fields
```

### Pattern 4: Configuration Models
```
User: "Create config model for Bitcoin RPC connection"

Skill:
1. Generate settings with defaults
2. Add path validators
3. Include environment variable loading
4. Add Config class with validate_assignment
```

## Field Type Mapping

| Description | Python Type | Validation |
|-------------|-------------|------------|
| "BTC amount" | `Decimal` | `ge=0` |
| "timestamp" | `datetime` | `default_factory=datetime.utcnow` |
| "percentage 0-100" | `float` | `ge=0, le=100` |
| "percentage 0-1" | `float` | `ge=0.0, le=1.0` |
| "count" | `int` | `ge=0` |
| "file path" | `Path` | `validator: path.exists()` |
| "URL" | `str` | `regex=r'https?://...'` |
| "optional field" | `Optional[T]` | `default=None` |
| "list of items" | `List[T]` | `default_factory=list` |
| "enum/choice" | `Literal["A", "B"]` | type checking |

## Validators Library

### Bitcoin-Specific Validators
```python
@validator('satoshis')
def validate_satoshis(cls, v):
    """Validate satoshi amount (max 21M BTC)"""
    if v < 0:
        raise ValueError('Satoshis must be non-negative')
    if v > 21_000_000 * 100_000_000:
        raise ValueError('Exceeds max Bitcoin supply')
    return v

@validator('script_type')
def validate_script_type(cls, v):
    """Validate Bitcoin script type"""
    valid = ['P2PKH', 'P2WPKH', 'P2SH', 'P2WSH', 'P2TR', 'NULLDATA']
    if v not in valid:
        raise ValueError(f'Invalid script type: {v}')
    return v
```

### Range Validators
```python
@validator('confidence')
def validate_confidence(cls, v):
    """Validate confidence score 0-1"""
    if not 0.0 <= v <= 1.0:
        raise ValueError('Confidence must be between 0 and 1')
    return v
```

### Path Validators
```python
@validator('bitcoin_data_dir')
def validate_data_dir(cls, v):
    """Validate Bitcoin data directory exists"""
    path = Path(v)
    if not path.exists():
        raise ValueError(f'Directory does not exist: {v}')
    if not (path / 'blocks').exists():
        raise ValueError(f'Not a valid Bitcoin data directory: {v}')
    return path
```

## JSON Schema Export

Auto-include schema export method:
```python
class MyModel(BaseModel):
    """..."""
    field1: str
    field2: int

    @classmethod
    def schema_json(cls, **kwargs):
        """Export JSON schema for API docs"""
        return cls.model_json_schema(**kwargs)

    class Config:
        json_schema_extra = {
            "example": {...}
        }
```

## Output Format

**Generated model file**:
```python
"""
{Module} Data Models

Pydantic models for {description}.
Auto-generated by pydantic-model-generator Skill.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal, Union
from datetime import datetime
from decimal import Decimal
from pathlib import Path

# Model definitions here...

# JSON Schema export
if __name__ == "__main__":
    print({ModelName}.model_json_schema(indent=2))
```

## Automatic Invocation

**Triggers**:
- "create pydantic model for [name]"
- "generate model for [description]"
- "pydantic schema for [fields]"
- "websocket message model for [type]"
- "config model for [module]"
- "model from json [data]"

**Does NOT trigger**:
- Complex business logic (use subagent)
- Database ORM models (different pattern)
- API endpoint models (use OpenAPI generator)

## Integration with LiquidationHeatmap

### Backend Models (`live/backend/models.py`)
```python
# Configuration
class BitcoinConfig(BaseModel): ...
class ZMQConfig(BaseModel): ...

# Data structures
class Transaction(BaseModel): ...
class TransactionOutput(BaseModel): ...
class Histogram(BaseModel): ...
class PriceEstimate(BaseModel): ...
```

### Shared Models (`live/shared/models.py`)
```python
# WebSocket messages
class PriceUpdateMessage(BaseModel): ...
class HistogramMessage(BaseModel): ...
WebSocketMessage = Union[PriceUpdateMessage, HistogramMessage]
```

### Usage Example
```python
# In mempool_analyzer.py
from live.backend.models import PriceEstimate, Histogram

def calculate_price(histogram: Histogram) -> PriceEstimate:
    price = estimate_from_histogram(histogram)
    return PriceEstimate(
        price=price,
        confidence=0.85,
        tx_count=histogram.total_txs
    )
```

## Token Savings

| Task | Without Skill | With Skill | Savings |
|------|--------------|------------|---------|
| Basic model (3 fields) | ~800 tokens | ~200 tokens | 75% |
| Model with validators | ~1,200 tokens | ~300 tokens | 75% |
| WebSocket messages (3 types) | ~2,000 tokens | ~500 tokens | 75% |
| Config model | ~1,500 tokens | ~400 tokens | 73% |

**Average Savings**: 75% (2,000 → 500 tokens)
