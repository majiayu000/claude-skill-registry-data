---
name: impl-infra
description: Implementar clientes de infraestrutura em infrastructure/. Use quando criar client externo, configuração, integração LLM, tracing, ou conexão com serviços fora do synth-lab.
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Implementar Infrastructure (Camada de Infraestrutura)

## Regras Arquiteturais (NON-NEGOTIABLE)

1. **Serviços externos**: toda comunicação fora do synth-lab passa por infrastructure
2. **Configuração via env vars**: usar `os.getenv()` com defaults
3. **Singleton pattern**: clients com função `get_*()` para reutilização
4. **Retry logic**: usar Tenacity para operações que podem falhar
5. **Tracing**: integrar Phoenix para observabilidade de LLM
6. **Logging**: usar Loguru com component binding

## Estrutura de Arquivos

```
src/synth_lab/infrastructure/
├── config.py                 # Configurações e paths
├── database.py               # DatabaseManager (PostgreSQL)
├── llm_client.py             # LLMClient (OpenAI)
├── phoenix_tracing.py        # Setup de tracing
└── {external}_client.py      # Clientes de APIs externas
```

**Convenções de nome:**
- Arquivo: `{service}_client.py` ou `{service}.py`
- Classe: `{Service}Client` ou `{Service}Manager`
- Singleton: `get_{service}_client()` ou `get_{service}()`

## Padrões de Código

### Configuração (config.py)

```python
"""
Configuration for synth-lab.

All external configuration via environment variables.
"""

import os
import sys
from pathlib import Path

from loguru import logger

# === Paths ===
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
DB_PATH = Path(os.getenv("SYNTHLAB_DB_PATH", str(OUTPUT_DIR / "synthlab.db")))

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Configuration ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
DEFAULT_MODEL = os.getenv("SYNTHLAB_DEFAULT_MODEL", "gpt-4o-mini")
DEFAULT_TIMEOUT = float(os.getenv("SYNTHLAB_TIMEOUT", "60.0"))


def configure_logging() -> None:
    """Configure loguru with LOG_LEVEL from environment."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - {message}",
    )


def ensure_directories() -> None:
    """Ensure all required directories exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

### Client com Singleton

```python
"""
{Service} client for synth-lab.

Integration with {service} API.
"""

import os
from functools import lru_cache

from loguru import logger

from synth_lab.infrastructure.config import {SERVICE}_API_KEY


class {Service}Client:
    """Client for {service} API."""

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
        self.api_key = api_key or {SERVICE}_API_KEY
        self.timeout = timeout
        self.logger = logger.bind(component="{service}_client")

        if not self.api_key:
            raise ValueError("{SERVICE}_API_KEY not configured")

    def call_api(self, data: dict) -> dict:
        """Call {service} API."""
        self.logger.debug(f"Calling {service} API")
        # Implementation
        return response


@lru_cache(maxsize=1)
def get_{service}_client() -> {Service}Client:
    """Get singleton {service} client instance."""
    return {Service}Client()
```

### LLM Client Pattern

```python
"""
LLM client for synth-lab.

Centralized OpenAI SDK access with retry and tracing.
"""

from functools import lru_cache

from loguru import logger
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from synth_lab.infrastructure.config import DEFAULT_MODEL, OPENAI_API_KEY


class LLMClient:
    """Client for LLM operations."""

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str | None = None,
        max_retries: int = 3,
    ):
        self.api_key = api_key or OPENAI_API_KEY
        self.default_model = default_model or DEFAULT_MODEL
        self.max_retries = max_retries
        self.client = OpenAI(api_key=self.api_key)
        self.logger = logger.bind(component="llm_client")

    def complete(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs,
    ) -> str:
        """Generate chat completion with retry."""
        return self._complete_with_retry(
            messages=messages,
            model=model or self.default_model,
            **kwargs,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    def _complete_with_retry(self, messages, model, **kwargs) -> str:
        """Internal completion with retry logic."""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content

    def complete_json(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> dict:
        """Generate JSON completion."""
        import json

        content = self.complete(
            messages=messages,
            response_format={"type": "json_object"},
            **kwargs,
        )
        return json.loads(content)


@lru_cache(maxsize=1)
def get_llm_client() -> LLMClient:
    """Get singleton LLM client instance."""
    return LLMClient()
```

### Phoenix Tracing

```python
"""
Phoenix tracing setup for synth-lab.

Observability for LLM operations.
"""

import os

from opentelemetry import trace


def setup_phoenix_tracing() -> None:
    """Setup Phoenix tracing if endpoint configured."""
    endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
    if not endpoint:
        return

    from openinference.instrumentation.openai import OpenAIInstrumentor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    provider = TracerProvider()
    exporter = OTLPSpanExporter(endpoint=endpoint)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # Instrument OpenAI
    OpenAIInstrumentor().instrument()


def get_tracer(component: str) -> trace.Tracer:
    """Get tracer for component."""
    return trace.get_tracer(f"synth_lab.{component}")


def shutdown_tracing() -> None:
    """Shutdown tracing gracefully."""
    provider = trace.get_tracer_provider()
    if hasattr(provider, "shutdown"):
        provider.shutdown()
```

### Uso de Tracing em Services

```python
# Em um service:
from synth_lab.infrastructure.phoenix_tracing import get_tracer

_tracer = get_tracer("my_service")


class MyService:
    def generate(self, data):
        with _tracer.start_as_current_span("generate"):
            # LLM call aqui (automaticamente traced)
            result = self.llm.complete_json(messages=[...])
            return result
```

## Checklist de Verificação

Antes de finalizar, verificar:

- [ ] Configuração via `os.getenv()` com defaults
- [ ] Singleton via `@lru_cache` + `get_*()` function
- [ ] Logger com `logger.bind(component=...)`
- [ ] Retry logic com Tenacity para operações instáveis
- [ ] API keys nunca hardcoded ou logados
- [ ] Timeout configurável
- [ ] Phoenix tracing integrado para LLM
- [ ] Tratamento de erros com exceções específicas
- [ ] Docstrings em métodos públicos
- [ ] Type hints em parâmetros e retornos
