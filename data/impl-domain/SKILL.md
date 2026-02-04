---
name: impl-domain
description: Implementar entidades de domínio em domain/entities/. Use quando criar entity, modelo de domínio, ou estrutura de dados core.
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Implementar Domain Entity (Camada de Domínio)

## Regras Arquiteturais (NON-NEGOTIABLE)

1. **Estruturas de dados puras**: entidades são modelos Pydantic
2. **SEM lógica de negócio**: apenas validação de dados via Pydantic
3. **SEM dependências externas**: não importar services, repositories, etc.
4. **Imutabilidade**: preferir `frozen=True` quando possível
5. **IDs prefixados**: seguir padrão `{prefix}_{uuid}` (ex: `exp_`, `grp_`)

## Estrutura de Arquivos

```
src/synth_lab/domain/
└── entities/
    ├── __init__.py
    └── {entity}.py           # Um arquivo por entidade
```

**Convenções de nome:**
- Arquivo: `{entity}.py` (singular, snake_case)
- Classe: `{Entity}` (PascalCase, singular)
- Campos: snake_case

## Padrões de Código

### Entidade Básica

```python
"""
{Entity} domain entity for synth-lab.

Core business entity representing a {entity}.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class {Entity}(BaseModel):
    """Core {entity} entity."""

    id: str = Field(
        ...,
        pattern=r"^{prefix}_[a-f0-9]{{8}}$",
        description="{Entity} ID ({prefix}_xxxxxxxx)",
    )
    name: str = Field(..., min_length=1, max_length=100, description="Name")
    description: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)
```

### Entidade com Nested Models

```python
"""
{Entity} domain entity with nested structures.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class NestedComponent(BaseModel):
    """Nested component of {Entity}."""

    field_a: str = Field(..., description="Field A")
    field_b: int = Field(default=0, ge=0, description="Field B")


class AnotherComponent(BaseModel):
    """Another nested component."""

    items: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


class {Entity}(BaseModel):
    """Core {entity} entity with nested data."""

    id: str = Field(..., description="{Entity} ID")
    name: str = Field(..., min_length=1, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)

    # Nested models
    component: NestedComponent | None = Field(default=None)
    another: AnotherComponent | None = Field(default=None)

    # JSON field for flexible data
    data: dict | None = Field(default=None, description="Additional JSON data")
```

### Entidade Imutável (para Value Objects)

```python
"""
Immutable value object.
"""

from pydantic import BaseModel, Field


class Location(BaseModel, frozen=True):
    """Immutable location value object."""

    cidade: str = Field(..., description="City name")
    estado: str = Field(..., pattern=r"^[A-Z]{2}$", description="State (UF)")
    regiao: str | None = Field(default=None, description="Region")
```

### Gerar ID

```python
"""
ID generation helper.
"""

import uuid


def generate_{entity}_id() -> str:
    """Generate a new {entity} ID."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# Uso:
# id = generate_experiment_id()  # -> "exp_a1b2c3d4"
```

### Exports em __init__.py

```python
"""Domain entities exports."""

from synth_lab.domain.entities.{entity} import (
    {Entity},
    NestedComponent,
    generate_{entity}_id,
)

__all__ = [
    "{Entity}",
    "NestedComponent",
    "generate_{entity}_id",
]
```

## Padrões de ID por Entidade

| Entidade | Prefixo | Exemplo |
|----------|---------|---------|
| Experiment | `exp_` | `exp_a1b2c3d4` |
| SynthGroup | `grp_` | `grp_f5e6d7c8` |
| Task | `task_` | `task_12345678` |
| Insight | `ins_` | `ins_abcdef12` |

## Checklist de Verificação

Antes de finalizar, verificar:

- [ ] Herda de `pydantic.BaseModel`
- [ ] Arquivo em `domain/entities/` (singular)
- [ ] SEM imports de services, repositories, infrastructure
- [ ] SEM lógica de negócio (só validação Pydantic)
- [ ] ID com padrão `{prefix}_{uuid}` e regex de validação
- [ ] Campos com type hints e Field descriptions
- [ ] Nested models para dados complexos
- [ ] `frozen=True` para value objects imutáveis
- [ ] Função `generate_{entity}_id()` para gerar IDs
- [ ] Exports no `__init__.py`
