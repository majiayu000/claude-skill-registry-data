---
name: error-handling
description: |
  Padrões de tratamento de erro para Python em crawlers, pipelines de dados
  e scripts batch. Cobre exceções tipadas, retry com backoff, circuit breaker,
  logging estruturado e mensagens de erro para operadores.
origin: ECC (adaptado para Extra Consultoria)
---

# Error Handling — Tratamento Robusto de Erros em Python

## Quando Ativar

Ative esta skill ao:
1. **Projetar hierarquia de exceções** para um novo módulo ou pipeline
2. **Adicionar retry/circuit breaker** para chamadas externas (APIs, crawlers)
3. **Revisar endpoints ou scripts** com tratamento de erro ausente
4. **Implementar logging** para processos batch desassistidos
5. **Depurar falhas em cascata** ou erros silenciosos em crawlers

## Princípios Fundamentais

1. **Falhe rápido e alto** — erro na borda onde ocorre, não enterre
2. **Exceções tipadas, não strings** — erros são valores estruturados de primeira classe
3. **Mensagem pro operador ≠ mensagem pro desenvolvedor** — usuário vê texto amigável, log tem contexto completo
4. **Nunca engula exceções em silêncio** — todo `except` deve tratar, propagar ou logar
5. **Erros fazem parte do contrato** — every error code que um script pode retornar deve ser documentado

## Hierarquia de Exceções (Python)

```python
class AppError(Exception):
    """Base para todas as exceções de aplicação."""
    def __init__(self, message: str, code: str, status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class CrawlError(AppError):
    """Falha durante crawling de fonte externa."""
    def __init__(self, message: str, source: str, url: str, code: str = "CRAWL_ERROR"):
        self.source = source
        self.url = url
        super().__init__(message, code, status_code=502)

class ParseError(AppError):
    """Falha ao parsear resposta de fonte externa."""
    def __init__(self, message: str, source: str, html_snippet: str = ""):
        self.source = source
        self.html_snippet = html_snippet[:500]
        super().__init__(message, "PARSE_ERROR", status_code=502)

class ValidationError(AppError):
    """Dados não passaram na validação de schema."""
    def __init__(self, message: str, details: list[dict] | None = None):
        self.details = details or []
        super().__init__(message, "VALIDATION_ERROR", status_code=422)

class ConfigError(AppError):
    """Erro de configuração (YAML, env, parâmetros)."""
    def __init__(self, message: str, config_key: str = ""):
        self.config_key = config_key
        super().__init__(message, "CONFIG_ERROR", status_code=500)

class DataLakeError(AppError):
    """Erro no DataLake (query, conexão, integridade)."""
    def __init__(self, message: str, operation: str = ""):
        self.operation = operation
        super().__init__(message, "DATALAKE_ERROR", status_code=500)
```

## Retry com Backoff Exponencial

Padrão essencial para crawlers e chamadas HTTP:

```python
import time
import random
import logging
from typing import Callable, TypeVar

T = TypeVar("T")
logger = logging.getLogger(__name__)

def with_retry(
    fn: Callable[[], T],
    max_attempts: int = 3,
    base_delay_ms: int = 1000,
    max_delay_ms: int = 30000,
    retry_on: tuple = (ConnectionError, TimeoutError),
) -> T:
    """Executa fn com retry exponencial + jitter."""
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except retry_on as e:
            if attempt == max_attempts:
                logger.error(
                    "Todas as tentativas esgotadas",
                    extra={"attempt": attempt, "max_attempts": max_attempts}
                )
                raise
            delay = min(base_delay_ms * (2 ** (attempt - 1)), max_delay_ms)
            jitter = random.uniform(0, delay * 0.3)
            wait_ms = delay + jitter
            logger.warning(
                f"Tentativa {attempt} falhou, retry em {wait_ms:.0f}ms",
                extra={"attempt": attempt, "error": str(e), "wait_ms": wait_ms}
            )
            time.sleep(wait_ms / 1000)
```

### Quando usar retry

| Erro | Retry? | Motivo |
|------|--------|--------|
| ConnectionError, TimeoutError | ✅ Sim | Transitório |
| HTTP 429 (Rate Limit) | ✅ Sim | Respeitar Retry-After |
| HTTP 5xx | ✅ Sim | Erro do servidor |
| HTTP 4xx (exceto 429) | ❌ Não | Erro do cliente |
| ParseError, ValidationError | ❌ Não | Erro nos dados, não na rede |

## Logging Estruturado para Processos Batch

```python
import logging
import sys

def setup_logging(level: str = "INFO", json_format: bool = False) -> None:
    """Configura logging para scripts batch.

    Args:
        level: DEBUG, INFO, WARNING, ERROR
        json_format: True para output JSON (consumível por sistemas de monitoramento)
    """
    if json_format:
        # Para ingestão em sistemas de log (Loki, ELK, CloudWatch)
        import json_log_formatter
        formatter = json_log_formatter.JSONFormatter()
    else:
        # Para leitura humana (journalctl, terminal)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S"
        )

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper()))
    root.addHandler(handler)

# Uso
logger = logging.getLogger(__name__)

# SEMPRE inclua contexto
logger.info("Crawl iniciado", extra={
    "source": "pncp",
    "mode": "full",
    "year": 2026
})

# NUNCA logue dados sensíveis
logger.error("Falha na requisição", extra={
    "url": url,
    "status_code": response.status_code,
    "attempt": attempt
    # NÃO inclua: token, api_key, cnpj, cpf
})
```

## Circuit Breaker para APIs Externas

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class CircuitBreaker:
    """Protege contra chamadas a serviços que já estão falhando."""
    failure_threshold: int = 5
    recovery_timeout_seconds: int = 60

    failure_count: int = 0
    last_failure_time: datetime | None = None
    state: str = "CLOSED"  # CLOSED | OPEN | HALF_OPEN

    def call(self, fn):
        if self.state == "OPEN":
            if self._recovery_timeout_exceeded():
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker: OPEN → HALF_OPEN")
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker aberto. Tente novamente em "
                    f"{self._remaining_seconds():.0f}s"
                )

        try:
            result = fn()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.error(
                "Circuit breaker abriu",
                extra={"failures": self.failure_count}
            )

    def _recovery_timeout_exceeded(self) -> bool:
        if self.last_failure_time is None:
            return True
        return datetime.now() - self.last_failure_time > \
               timedelta(seconds=self.recovery_timeout_seconds)

    def _remaining_seconds(self) -> float:
        if self.last_failure_time is None:
            return 0
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return max(0, self.recovery_timeout_seconds - elapsed)

class CircuitBreakerOpenError(Exception):
    """Circuit breaker está aberto — serviço em falha."""
    pass
```

## Padrão Result (no-throw para operações esperadas)

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

@dataclass
class Ok(Generic[T]):
    value: T
    ok: bool = True

@dataclass
class Err(Generic[E]):
    error: E
    ok: bool = False

Result = Ok[T] | Err[E]

# Uso em crawler
def parse_licitacao(html: str) -> Result[dict, ParseError]:
    try:
        data = extract_data(html)
        return Ok(data)
    except Exception as e:
        return Err(ParseError(str(e), source="pncp", html_snippet=html[:200]))

result = parse_licitacao(html)
if result.ok:
    save(result.value)
else:
    logger.error("Parse falhou", extra={"error": result.error.message})
```

## Checklist Pre-Merge

Antes de mergear código com tratamento de erro:

- [ ] Todo `except` trata, propaga ou loga — zero silent swallowing
- [ ] Erros de API seguem envelope padrão `{error: {code, message}}`
- [ ] Mensagens para o operador não contêm stack traces ou detalhes internos
- [ ] Contexto completo está logado no servidor (nível, módulo, extra)
- [ ] Exceções customizadas herdam de `AppError` com campo `code`
- [ ] Funções async têm await — sem fire-and-forget sem fallback
- [ ] Retry só retry em erros retryable (não em 4xx)
- [ ] Crawlers têm timeout + retry em TODAS as chamadas HTTP
- [ ] Circuit breaker protege APIs externas com histórico de instabilidade
