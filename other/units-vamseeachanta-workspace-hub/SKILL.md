---

name: units
version: "1.0.0"
category: engineering
description: "Unit-safe engineering calculations with provenance tracking, dimensional consistency verification, and unit conversion across SI, inch, and metric systems."
type: reference
tags: []
scripts_exempt: true
---

# /units — Engineering Unit Tracking

Unit-safe engineering calculations with provenance tracking across the workspace-hub ecosystem.

## Usage

```
/units [subcommand]
```

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `wrap <file>` | Analyze a Python file and suggest TrackedQuantity wrapping for raw numerics |
| `audit <file>` | Generate a CalculationAuditLog from an instrumented script |
| `check <file>` | Verify dimensional consistency across a calculation chain |
| `convert <value> <from> <to>` | Quick unit conversion with provenance |
| `systems` | List available unit systems (SI, inch, metric_engineering) |
| `registry` | Show all registered units including custom energy/offshore units |

## Quick Reference

### Core API (assetutilities.units)

```python
from assetutilities.units import (
    TrackedQuantity,       # Unit-tracked value with provenance
    CalculationAuditLog,   # Aggregate audit trail
    UnitMismatchError,     # Dimension mismatch exception
    UnitSystemPolicy,      # Project-wide unit enforcement
    unit_checked,          # Decorator for function-level validation
    get_registry,          # Singleton pint UnitRegistry
)
```

### TrackedQuantity

```python
# Create with source provenance
depth = TrackedQuantity(1300.0, "m", source="gulf_of_mexico")

# Convert (provenance recorded automatically)
depth_ft = depth.to("ft")

# Dimension analysis
depth.dimensions          # "[length]"
depth.is_compatible("ft") # True
depth.is_compatible("kg") # False
depth.check_dimensions("[length]")  # passes or raises ValueError

# Arithmetic (provenance merged from operands)
pressure = rho * g * depth  # compound units handled by pint

# Serialize
data = depth.to_dict()
restored = TrackedQuantity.from_dict(data)
```

### OrcaFlex Adapter (rock_oil_field.units.orcaflex_adapter)

```python
from rock_oil_field.units.orcaflex_adapter import (
    wrap_orcaflex_value,     # Single value → TrackedQuantity
    unwrap_for_orcaflex,     # TrackedQuantity → raw float (converts to OrcaFlex units)
    wrap_model_parameters,   # Dict of (value, type) → TrackedQuantity dict
    wrap_environment,        # Config dict → TrackedQuantity dict with unit inference
    ORCAFLEX_UNITS,          # Default unit mapping per parameter type
)
```

### Instrumented Workflow Pattern

```python
from rock_oil_field.workflows.diffraction import (
    setup_environment,       # Water depth, mesh positions
    setup_vessel_inertia,    # Mass, CoG, inertia tensor, draught
    setup_wave_parameters,   # Headings, periods
    run_instrumented_setup,  # Full workflow → CalculationAuditLog
)
```

## Unit Systems

| System | Length | Stress | Force | Temperature |
|--------|--------|--------|-------|-------------|
| `SI` | m | Pa | N | degC |
| `inch` | inch | psi | lbf | degF |
| `metric_engineering` | mm | MPa | kN | degC |

## OrcaFlex Default Units

| Type | Unit | Type | Unit |
|------|------|------|------|
| length | m | mass | tonne |
| force | kN | stiffness | kN/m |
| moment | kN*m | period | s |
| angle | deg | pressure | kPa |
| velocity | m/s | acceleration | m/s^2 |
| density | tonne/m^3 | | |

## Wrapping Raw Parameters

When instrumenting a script with raw numerics:

```python
# BEFORE (raw — no unit safety)
seabed_depth = 1300
diff.SetData('WaterDepth', 0, seabed_depth)

# AFTER (tracked — full provenance)
from rock_oil_field.units.orcaflex_adapter import wrap_orcaflex_value, unwrap_for_orcaflex

seabed_depth = wrap_orcaflex_value(1300.0, "length", source="gulf_of_mexico")
diff.SetData('WaterDepth', 0, unwrap_for_orcaflex(seabed_depth, "length"))
```

## Visualization

```python
from assetutilities.units.visualization import LineageGraph

graph = LineageGraph.from_audit_log(audit)
graph.to_html()   # Standalone HTML (no dependencies)
graph.to_svg()    # SVG via graphviz (optional)
graph.to_dot()    # Graphviz DOT text
graph.to_dict()   # JSON-serializable dict
```

## Related

- Full guide: `assetutilities/docs/units-guide.md`
- Tests: `assetutilities/tests/units/`, `client-b/tests/unit/`
- S7 reference scripts: `client-b/s7/analysis_general/`
