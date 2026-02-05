---
name: impl-service
description: Implementar serviços de lógica de negócio em services/. Use quando criar service, lógica de negócio, orquestração de repositórios, ou integração com LLM.
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Implementar Service (Camada de Lógica de Negócio)

## Regras Arquiteturais (NON-NEGOTIABLE)

1. **TODA lógica de negócio** deve estar em services, NUNCA em routers ou repositories
2. **Validações de negócio** (limites, regras, constraints) ficam no service
3. **Prompts de LLM** ficam no service, NUNCA em routers
4. **Chamadas LLM** DEVEM usar tracing Phoenix: `_tracer.start_as_current_span()`
5. **Dependency Injection**: repositories são injetados no `__init__`
6. **Orquestração**: services chamam repositories, NUNCA acessam DB diretamente
7. **Bloco de validação**: todo service DEVE ter `if __name__ == "__main__":`

## Estrutura de Arquivos

```
src/synth_lab/services/
├── {entity}_service.py      # Um arquivo por domínio
├── errors.py                 # Exceções de negócio
└── {feature}/                # Subpastas para features complexas
    ├── __init__.py
    └── {sub_service}.py
```

**Convenções de nome:**
- Arquivo: `{entity}_service.py` (singular, snake_case)
- Classe: `{Entity}Service` (PascalCase)
- Métodos: `{verbo}_{substantivo}` (ex: `create_experiment`, `list_synths`)

## Padrões de Código

### Service Básico (sem LLM)

```python
"""
{Entity} service for synth-lab.

Business logic layer for {entity} operations.
"""

from synth_lab.models.pagination import PaginatedResponse, PaginationParams
from synth_lab.repositories.{entity}_repository import {Entity}Repository


class {Entity}Service:
    """Service for {entity} business logic."""

    # Constantes de validação
    NAME_MAX_LENGTH = 100

    def __init__(self, repository: {Entity}Repository | None = None):
        """Initialize with dependency injection."""
        self.repository = repository or {Entity}Repository()

    def list_{entities}(
        self,
        params: PaginationParams | None = None,
    ) -> PaginatedResponse[{Entity}Summary]:
        """List {entities} with pagination."""
        params = params or PaginationParams()
        return self.repository.list_{entities}(params)

    def get_{entity}(self, {entity}_id: str) -> {Entity}Detail:
        """Get {entity} by ID."""
        return self.repository.get_by_id({entity}_id)

    def create_{entity}(self, name: str) -> {Entity}:
        """Create new {entity} with validation."""
        # Validação de negócio
        if not name or not name.strip():
            raise ValueError("name is required")
        if len(name) > self.NAME_MAX_LENGTH:
            raise ValueError(f"name exceeds {self.NAME_MAX_LENGTH} chars")

        # Criar e persistir
        entity = {Entity}(name=name.strip())
        return self.repository.create(entity)
```

### Service com LLM

```python
"""
{Feature} LLM service for synth-lab.

LLM-powered business logic.
"""

from loguru import logger

from synth_lab.infrastructure.llm_client import LLMClient, get_llm_client
from synth_lab.infrastructure.phoenix_tracing import get_tracer

_tracer = get_tracer("{feature}_service")


class {Feature}Service:
    """Service with LLM integration."""

    def __init__(self, llm_client: LLMClient | None = None):
        self.llm = llm_client or get_llm_client()
        self.logger = logger.bind(component="{feature}_service")

    def generate(self, data: InputData) -> Result:
        """Generate result using LLM."""
        with _tracer.start_as_current_span("generate"):
            prompt = self._build_prompt(data)
            response = self.llm.complete_json(
                messages=[{"role": "user", "content": prompt}],
                operation_name="generate_result",
            )
            self.logger.info(f"Generated for {data.id}")
            return self._parse_response(response)

    def _build_prompt(self, data: InputData) -> str:
        """Build LLM prompt (private method)."""
        return f"""
        Instrução: ...
        Dados: {data.model_dump_json()}
        """

    def _parse_response(self, response: dict) -> Result:
        """Parse and validate LLM response."""
        return Result(**response)
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
    service = {Entity}Service()

    # Test 1: Operação básica
    total_tests += 1
    try:
        result = service.list_{entities}()
        if result.pagination.total < 0:
            all_validation_failures.append("Invalid total")
    except Exception as e:
        all_validation_failures.append(f"List failed: {e}")

    # Test 2: Validação de erro
    total_tests += 1
    try:
        service.get_{entity}("invalid_id")
        all_validation_failures.append("Should raise NotFoundError")
    except {Entity}NotFoundError:
        pass  # Expected
    except Exception as e:
        all_validation_failures.append(f"Wrong exception: {e}")

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

- [ ] Lógica de negócio está no service (não em router/repository)
- [ ] Validações de input (required, max length, format)
- [ ] Repository injetado via DI no `__init__`
- [ ] Chamadas LLM usam `_tracer.start_as_current_span()`
- [ ] Prompts em métodos privados `_build_prompt()`
- [ ] Bloco `if __name__ == "__main__":` com validação real
- [ ] Exceções específicas do domínio (ex: `{Entity}NotFoundError`)
- [ ] Docstrings em todos os métodos públicos
- [ ] Type hints em parâmetros e retornos
