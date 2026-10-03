---
name: portal-semantic-layer
description: Implement the SMQ semantic layer (paper 04) that turns structured Pydantic queries into deterministic Polars expressions for the financial silos. Use when defining semantic query schemas, validating metrics/dimensions against the catalog, writing ml/semantic/compiler.py, or adding cross-silo joins (creditos x derivados).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Semantic Layer Skill (SMQ)

Compiler module: `! ls ml/semantic/ 2>/dev/null || echo "no semantic dir yet"`

## Rules — NON-NEGOTIABLE

- El LLM y el cliente NUNCA envían código libre (Polars, SQL, Python): solo consultas estructuradas `SemanticQuery` validadas con Pydantic (patrón SMQ, paper 04).
- Métricas y dimensiones válidas se declaran en el catálogo (`catalog_field`); toda consulta se valida contra él ANTES de compilar. Métrica inexistente → `UnknownMetricError` → 422 con fuzzy match (ver `portal-backend-api`).
- El único generador de expresiones Polars es el compilador determinístico `ml/semantic/compiler.py`: misma consulta + misma semilla ⇒ mismo resultado (base de las 10 consultas de referencia del plan).
- Todo con Polars **lazy** (`pl.scan_parquet` vía extractores de `portal-data-connectors`); `collect()` solo al final del plan.
- Joins entre silos solo por claves declaradas en el catálogo (p. ej. contraparte: `creditos ⋈ derivados`); jamás joins ad-hoc pedidos por el cliente.
- Filtros siempre parametrizados por el compilador; nunca interpolar strings del usuario en expresiones.

## Esquema Pydantic de consulta

```python
# backend/app/models/semantic.py
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field

class SemanticFilter(BaseModel):
    dimension: str
    op: Literal["eq", "neq", "in", "gte", "lte", "between"]
    value: str | float | list[str] | list[float]

class SemanticQuery(BaseModel):
    metric: str                                   # business name, e.g. "saldo_total"
    dimensions: list[str] = Field(default_factory=list, max_length=4)
    filters: list[SemanticFilter] = Field(default_factory=list, max_length=8)
    date_from: date | None = None
    date_to: date | None = None
    limit: int = Field(default=1000, le=100_000)

    @property
    def is_aggregation(self) -> bool:
        return bool(self.dimensions)

class SemanticResult(BaseModel):
    metric: str
    rows: list[dict]
    row_count: int
    sources: list[str]      # catalog citations (anti-hallucination)
```

## Validación contra el catálogo

```python
# ml/semantic/validator.py
def validate_query(query: SemanticQuery, catalog: CatalogIndex, silo: str) -> MetricSpec:
    """Resolve business names to physical columns; raise typed errors otherwise."""
    spec = catalog.get_metric(silo, query.metric)
    if spec is None:
        raise UnknownMetricError(metric=query.metric)
    for dim in query.dimensions:
        if not catalog.has_dimension(silo, dim):
            raise UnknownDimensionError(dimension=dim)
    return spec  # spec.physical_column, spec.agg ("sum"|"mean"|"count"), spec.source_id
```

## Compilador determinístico

```python
# ml/semantic/compiler.py
import polars as pl

AGG_FNS = {"sum": pl.sum, "mean": pl.mean, "count": pl.count, "max": pl.max}

def compile_query(lf: pl.LazyFrame, query: SemanticQuery, spec: MetricSpec,
                  catalog: CatalogIndex, silo: str) -> pl.LazyFrame:
    """Compile a validated SemanticQuery into a parameterized Polars lazy plan."""
    for f in query.filters:
        col = catalog.physical_column(silo, f.dimension)
        lf = lf.filter(_predicate(pl.col(col), f))          # parameterized, never f-strings
    if query.date_from or query.date_to:
        date_col = catalog.date_column(silo)
        if query.date_from:
            lf = lf.filter(pl.col(date_col) >= query.date_from)
        if query.date_to:
            lf = lf.filter(pl.col(date_col) <= query.date_to)
    metric_expr = AGG_FNS[spec.agg](spec.physical_column).alias(query.metric)
    if query.is_aggregation:
        dims = [catalog.physical_column(silo, d) for d in query.dimensions]
        return lf.group_by(dims).agg(metric_expr).limit(query.limit)
    return lf.select([spec.physical_column]).limit(query.limit)
```

## Join entre silos (exposición por contraparte)

```python
# ml/semantic/joins.py — join keys come from the catalog, never from the client
def counterparty_exposure(creditos: pl.LazyFrame, derivados: pl.LazyFrame) -> pl.LazyFrame:
    return (
        creditos.group_by("cli_ref").agg(pl.sum("sdo_cap").alias("credit_exposure"))
        .join(
            derivados.group_by("ctpty_cd").agg(pl.sum("mtm_val").alias("deriv_mtm")),
            left_on="cli_ref", right_on="ctpty_cd", how="full", coalesce=True,
        )
    )
```

## Consulta de referencia (suite del plan)

```python
# tests/backend/test_semantic_reference.py — 10 queries with expected results on the fixed seed
REF_QUERY = SemanticQuery(
    metric="saldo_total",
    dimensions=["producto"],
    filters=[SemanticFilter(dimension="mora", op="gte", value=90)],
    date_from=date(2026, 1, 1),
)

def test_saldo_total_por_producto(catalog, creditos_lf):
    spec = validate_query(REF_QUERY, catalog, silo="creditos")
    out = compile_query(creditos_lf, REF_QUERY, spec, catalog, "creditos").collect()
    assert out.height > 0 and out["saldo_total"].sum() == EXPECTED_SEED_TOTAL
```

## Referencias

| Pieza | Ubicación |
|-------|-----------|
| Esquema de consulta | `backend/app/models/semantic.py` |
| Validador + errores | `ml/semantic/validator.py` |
| Compilador | `ml/semantic/compiler.py` |
| Joins declarados | `ml/semantic/joins.py` |
| Suite de referencia | `tests/backend/test_semantic_reference.py` |
