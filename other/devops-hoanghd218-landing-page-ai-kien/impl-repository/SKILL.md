---
name: impl-repository
description: Implementar repositórios de acesso a dados em repositories/. Use quando criar repository, acesso a banco, queries SQL, ou persistência.
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Implementar Repository (Camada de Acesso a Dados)

## Regras Arquiteturais (NON-NEGOTIABLE)

1. **SÓ acesso a dados**: repositories NÃO contêm lógica de negócio
2. **Queries parametrizadas**: SEMPRE usar `?` placeholders, NUNCA string interpolation
3. **Herdar BaseRepository**: para reutilizar paginação e helpers
4. **Conversão de dados**: métodos `_row_to_*` para converter rows em models
5. **Exceções de domínio**: lançar exceções específicas (ex: `SynthNotFoundError`)
6. **JSON1 extension**: usar `json_extract()` para campos JSON aninhados

## Estrutura de Arquivos

```
src/synth_lab/repositories/
├── base.py                   # BaseRepository com helpers
└── {entity}_repository.py    # Um arquivo por entidade
```

**Convenções de nome:**
- Arquivo: `{entity}_repository.py` (singular)
- Classe: `{Entity}Repository` (PascalCase)
- Métodos: CRUD padrão + queries específicas

## Padrões de Código

### Repository Básico

```python
"""
{Entity} repository for synth-lab.

Data access layer for {entity} data.
"""

from synth_lab.infrastructure.database import DatabaseManager
from synth_lab.models.pagination import PaginatedResponse, PaginationParams
from synth_lab.repositories.base import BaseRepository
from synth_lab.services.errors import {Entity}NotFoundError


class {Entity}Repository(BaseRepository):
    """Repository for {entity} data access."""

    def __init__(self, db: DatabaseManager | None = None):
        super().__init__(db)

    def list_{entities}(
        self,
        params: PaginationParams,
    ) -> PaginatedResponse[{Entity}Summary]:
        """List {entities} with pagination."""
        base_query = "SELECT * FROM {entities}"
        rows, meta = self._paginate_query(base_query, params)
        items = [self._row_to_summary(row) for row in rows]
        return PaginatedResponse(data=items, pagination=meta)

    def get_by_id(self, {entity}_id: str) -> {Entity}Detail:
        """Get {entity} by ID."""
        row = self.db.fetchone(
            "SELECT * FROM {entities} WHERE id = ?",
            ({entity}_id,),  # SEMPRE parametrizado
        )
        if row is None:
            raise {Entity}NotFoundError({entity}_id)
        return self._row_to_detail(row)

    def create(self, entity: {Entity}) -> {Entity}:
        """Create new {entity}."""
        self.db.execute(
            """
            INSERT INTO {entities} (id, name, created_at)
            VALUES (?, ?, ?)
            """,
            (entity.id, entity.name, entity.created_at),
        )
        return entity

    def update(self, entity: {Entity}) -> {Entity}:
        """Update existing {entity}."""
        self.db.execute(
            """
            UPDATE {entities}
            SET name = ?, updated_at = ?
            WHERE id = ?
            """,
            (entity.name, entity.updated_at, entity.id),
        )
        return entity

    def delete(self, {entity}_id: str) -> None:
        """Delete {entity} by ID."""
        result = self.db.execute(
            "DELETE FROM {entities} WHERE id = ?",
            ({entity}_id,),
        )
        if result.rowcount == 0:
            raise {Entity}NotFoundError({entity}_id)

    # === Conversões de dados ===

    def _row_to_summary(self, row) -> {Entity}Summary:
        """Convert row to summary model."""
        from datetime import datetime

        created_at = row["created_at"]
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        return {Entity}Summary(
            id=row["id"],
            name=row["name"],
            created_at=created_at,
        )

    def _row_to_detail(self, row) -> {Entity}Detail:
        """Convert row to detail model with nested data."""
        import json
        from datetime import datetime

        created_at = row["created_at"]
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        # Parse JSON field
        data = {}
        if row["data"]:
            data = json.loads(row["data"])

        return {Entity}Detail(
            id=row["id"],
            name=row["name"],
            created_at=created_at,
            nested_data=NestedModel(**data.get("nested", {})),
        )
```

### Queries com JSON

```python
def search_by_nested_field(self, field_value: str) -> list[{Entity}Summary]:
    """Search by nested JSON field."""
    rows = self.db.fetchall(
        """
        SELECT * FROM {entities}
        WHERE json_extract(data, '$.nested.field') = ?
        """,
        (field_value,),
    )
    return [self._row_to_summary(row) for row in rows]
```

### Validação de Query do Usuário (Power User)

```python
# Keywords bloqueados para queries de usuário
BLOCKED_KEYWORDS = frozenset([
    "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER",
    "TRUNCATE", "EXEC", "EXECUTE", "GRANT", "REVOKE", "UNION",
    "--", ";", "/*", "*/",
])

MAX_WHERE_LENGTH = 1000

def _validate_where_clause(self, where: str) -> None:
    """Validate user-provided WHERE clause."""
    if len(where) > MAX_WHERE_LENGTH:
        raise InvalidQueryError("WHERE clause too long")

    upper = where.upper()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in upper:
            raise InvalidQueryError(f"Keyword '{keyword}' not allowed")
```

### Bloco de Validação (OBRIGATÓRIO)

```python
if __name__ == "__main__":
    import sys

    from synth_lab.infrastructure.config import DB_PATH
    from synth_lab.infrastructure.database import DatabaseManager

    all_validation_failures = []
    total_tests = 0

    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        sys.exit(1)

    db = DatabaseManager(DB_PATH)
    repo = {Entity}Repository(db)

    # Test 1: List
    total_tests += 1
    try:
        result = repo.list_{entities}(PaginationParams(limit=10))
        if result.pagination.total < 0:
            all_validation_failures.append("Invalid total")
    except Exception as e:
        all_validation_failures.append(f"List failed: {e}")

    # Test 2: Get by ID (not found)
    total_tests += 1
    try:
        repo.get_by_id("invalid_id")
        all_validation_failures.append("Should raise NotFoundError")
    except {Entity}NotFoundError:
        pass  # Expected

    # Test 3: SQL injection prevention
    total_tests += 1
    try:
        repo.search(where_clause="1=1; DROP TABLE x")
        all_validation_failures.append("Should reject dangerous query")
    except InvalidQueryError:
        pass  # Expected

    db.close()

    if all_validation_failures:
        print(f"VALIDATION FAILED - {len(all_validation_failures)}/{total_tests}:")
        for f in all_validation_failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"VALIDATION PASSED - All {total_tests} tests OK")
        sys.exit(0)
```

## Checklist de Verificação

Antes de finalizar, verificar:

- [ ] Herda de `BaseRepository`
- [ ] Queries usam `?` placeholders (NUNCA string interpolation)
- [ ] Métodos `_row_to_summary()` e `_row_to_detail()`
- [ ] Exceções específicas (ex: `{Entity}NotFoundError`)
- [ ] Suporte a paginação via `_paginate_query()`
- [ ] Campos JSON usam `json_extract()`
- [ ] Validação de WHERE clause do usuário (se aplicável)
- [ ] Bloco `if __name__ == "__main__":` com validação real
- [ ] SEM lógica de negócio (só acesso a dados)
- [ ] Docstrings em métodos públicos
