---
name: definition-resource-design
description: Guide for designing Definition resources in OptAIC (the "Law"). Use when creating PipelineDef, StoreDef, AccessorDef, OpDef, MLModuleDef, or PortfolioOptimizerDef. Covers interface_spec, input/output schemas, compatibility rules, and embedded guardrail contracts.
---

# Definition Resource Design Patterns

Guide for designing Definition resources that serve as reusable plugin templates. Definitions are the "Law" that Instances must follow.

## When to Use

Apply when:
- Creating new plugin types (PipelineDef, StoreDef, etc.)
- Designing the interface contract a plugin must implement
- Specifying input/output schemas for validation
- Defining compatibility rules for upstream/downstream connections
- Embedding guardrail contracts that enforce data quality

## Core Concept: The Law

Definition resources contain the rules that Instance resources must follow:

```
Definition = The Law
├── interface_spec        # Abstract interface to implement
├── input_schema          # Expected input format
├── output_schema         # Expected output format
├── compatibility_rules   # What can connect upstream/downstream
└── guardrail_contracts   # Validation rules (enforced by Engine)
```

## Definition Types

| Type | Purpose | Example Implementations |
|------|---------|------------------------|
| `PipelineDef` | Data ingestion/transform | BloombergPipeline, FREDPipeline, ExpressionPipeline |
| `StoreDef` | Storage backend | ParquetStore, SQLiteStore, VirtualStore |
| `AccessorDef` | Data access pattern | SimpleAccessor, PITAccessor, FieldAccessor |
| `OpDef` | Mathematical operator | REF, DELTA, MEAN, CORR, RANK |
| `OpMacroDef` | Saved expression | User-defined formulas |
| `MLModuleDef` | ML model template | XGBoostModule, LSTMModule |
| `PortfolioOptimizerDef` | Optimization algo | MVO, HRP, BlackLitterman, RiskParity |

## Schema Structure

See [references/schema-structure.md](references/schema-structure.md) for complete JSON schema.

### Minimal Definition

```python
definition_metadata = {
    "interface_spec": "optaic.interfaces.BasePipeline",
    "input_schema": {"datasets": {"type": "array"}},
    "output_schema": {"type": "DataFrame", "columns": ["date", "entity", "value"]},
}
```

### Full Definition with Contracts

```python
definition_metadata = {
    "interface_spec": "optaic.interfaces.SignalPipeline",
    "version": "1.0",

    "input_schema": {
        "datasets": {"type": "array", "items": {"$ref": "#/DatasetInstance"}},
        "parameters": {"type": "object", "properties": {...}}
    },

    "output_schema": {
        "type": "DataFrame",
        "columns": ["date", "entity", "value"],
        "value_range": {"min": -1, "max": 1}
    },

    "compatibility_rules": {
        "upstream_types": ["DatasetInstance"],
        "downstream_types": ["SignalInstance", "BacktestInstance"]
    },

    "guardrail_contracts": [
        {"kind": "signal.bounds", "config": {"min": -1, "max": 1, "allow_nan": False}},
        {"kind": "pit.policy", "config": {"knowledge_date_required": True}},
    ]
}
```

## Implementation Checklist

1. [ ] Define `interface_spec` pointing to abstract base class
2. [ ] Specify `input_schema` with JSON Schema format
3. [ ] Specify `output_schema` with expected structure
4. [ ] Define `compatibility_rules` for resource graph connections
5. [ ] Embed `guardrail_contracts` for validation
6. [ ] Create extension table in `libs/db/models/`
7. [ ] Add to `ResourceType` enum

## Reference Files

- [Schema Structure](references/schema-structure.md) - Complete JSON schema spec
- [Examples](references/examples.md) - Example Definition implementations
