---
name: python-patterns
description: |
  Padrões Pythonicos, PEP 8, type hints, dataclasses, decorators,
  context managers, geradores, concorrência e tooling para scripts
  de crawling e pipelines de dados.
origin: ECC (adaptado para Extra Consultoria)
---

# Python Patterns — Padrões Pythonicos para Dados e Crawling

## Quando Ativar

- Escrevendo código Python novo
- Revisando código Python existente
- Refatorando scripts ou pipelines
- Projetando pacotes e módulos

## Princípios Fundamentais

### 1. Legibilidade Importa

Código deve ser óbvio e fácil de entender:

```python
# ✅ Comprehensions para transformações simples
ativos = [f for f in fornecedores if f.status == "ativo"]

# ✅ Expanda para loop se a lógica crescer
resultados = []
for fonte in fontes:
    if fonte.ativa and fonte.tem_credenciais():
        dados = crawlear(fonte)
        resultados.extend(dados)
```

### 2. Explícito sobre Implícito

Sem side effects escondidos. Configuração visível:

```python
# ✅ Explícito
def crawlear(source: str, timeout: int = 30, retry: bool = True) -> list[dict]:
    """Crawl explícito — cada parâmetro declarado."""

# ❌ Implícito — timeout e retry vêm de variáveis globais
def crawlear(source: str) -> list[dict]:
    ...
```

### 3. EAFP (Easier to Ask Forgiveness Than Permission)

Estilo Pythonico: tente, trate o erro. Não pré-verifique:

```python
# ✅ EAFP — tenta e trata
try:
    dados = response.json()
except json.JSONDecodeError as e:
    logger.error("Resposta não é JSON válido", extra={"url": url, "error": str(e)})
    return []

# ❌ LBYL — pré-verificação desnecessária
if "application/json" in response.headers.get("content-type", ""):
    dados = response.json()
else:
    logger.error("não é JSON")
    return []
```

## Type Hints

### Anotações Básicas (Python 3.9+)

```python
# Use built-in generics (Python 3.9+), não typing.List/Dict
def buscar_licitacoes(
    uf: str,
    dias: int = 30,
    categorias: list[str] | None = None,
) -> list[dict[str, object]]:
    ...

# Optional = Union com None
from typing import Optional  # para compatibilidade

def get_fornecedor(cnpj: str) -> dict | None:
    ...
```

### Type Aliases para Complexidade

```python
from typing import Union, Any

JSON = Union[dict[str, Any], list[Any], str, int, float, bool, None]

LicitacaoDict = dict[str, Any]  # JSON de uma licitação
FornecedorDict = dict[str, Any]  # JSON de um fornecedor

def parse_licitacao(raw: JSON) -> LicitacaoDict:
    ...

def parse_fornecedor(raw: JSON) -> FornecedorDict:
    ...
```

### Protocol para Duck Typing Estruturado

```python
from typing import Protocol

class Crawlavel(Protocol):
    """Qualquer fonte que pode ser crawlada."""
    def crawlear(self, mode: str) -> list[dict]: ...
    @property
    def name(self) -> str: ...

# Qualquer classe com crawlear() e name é Crawlavel
def executar_crawl(fonte: Crawlavel) -> list[dict]:
    logger.info(f"Crawling {fonte.name}")
    return fonte.crawlear(mode="full")
```

## Dataclasses (em vez de dicts brutos)

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class CrawlResult:
    source: str
    total: int
    status: str  # "success" | "partial" | "failed"
    started_at: datetime
    finished_at: datetime | None = None
    errors: list[dict] = field(default_factory=list)
    items: list[dict] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        if self.finished_at is None:
            return 0
        return (self.finished_at - self.started_at).total_seconds()

    @property
    def error_rate(self) -> float:
        if self.total == 0:
            return 0
        return len(self.errors) / self.total

# Com validação no __post_init__
@dataclass
class CrawlConfig:
    source: str
    timeout: int = 30
    max_retries: int = 3

    def __post_init__(self):
        if self.timeout <= 0:
            raise ValueError(f"timeout deve ser positivo, recebeu {self.timeout}")
        if self.max_retries < 0:
            raise ValueError(f"max_retries não pode ser negativo")
```

## Context Managers

Sempre use `with` para recursos — arquivos, conexões, locks:

```python
# ✅ Context manager garante close
with open("resultados.json", "w") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

# ✅ Custom context manager com @contextmanager
from contextlib import contextmanager
import time

@contextmanager
def timed_operation(name: str):
    """Mede duração de uma operação."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.info(f"{name} concluído", extra={"duration_ms": elapsed * 1000})

# Uso
with timed_operation("crawl_pncp"):
    dados = crawlear_portal("pncp")
```

## Geradores para Grandes Volumes

Crawlers e pipelines processam milhares de itens — use geradores:

```python
# ✅ Gerador — memória constante
def ler_licitacoes(arquivo: str) -> Iterator[dict]:
    """Lê JSON linha a linha sem carregar tudo em memória."""
    with open(arquivo) as f:
        for line in f:
            yield json.loads(line)

# ✅ Generator expression para filtro lazy
licitacoes_sc = (
    l for l in ler_licitacoes("pncp_2026.jsonl")
    if l.get("uf") == "SC"
)

# ❌ Tudo em memória — explode com arquivos grandes
with open("pncp_2026.jsonl") as f:
    todas = [json.loads(line) for line in f]
licitacoes_sc = [l for l in todas if l.get("uf") == "SC"]
```

## Decorators

```python
import functools
import time

def log_execucao(func):
    """Registra início, fim e duração da função."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"{func.__name__} iniciado")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.debug(f"{func.__name__} concluído", extra={"duration_ms": elapsed * 1000})
            return result
        except Exception:
            elapsed = time.perf_counter() - start
            logger.exception(f"{func.__name__} falhou", extra={"duration_ms": elapsed * 1000})
            raise
    return wrapper

@log_execucao
def crawlear_portal(source: str) -> list[dict]:
    ...
```

## Concorrência para Crawlers

| Cenário | Abordagem | Por quê |
|---------|-----------|---------|
| I/O-bound (HTTP, rede) | `ThreadPoolExecutor` | GIL não bloqueia I/O |
| Muitos requests assíncronos | `asyncio` + `aiohttp` | Mais leve que threads |
| CPU-bound (parse pesado) | `ProcessPoolExecutor` | Burla o GIL |

```python
# ThreadPoolExecutor — múltiplos crawlers em paralelo
from concurrent.futures import ThreadPoolExecutor, as_completed

def crawlear_todas_fontes(fontes: list[str]) -> dict[str, CrawlResult]:
    resultados = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(crawlear_portal, f): f for f in fontes}
        for future in as_completed(futures):
            fonte = futures[future]
            try:
                resultados[fonte] = future.result(timeout=300)
            except Exception as e:
                logger.error(f"Crawl de {fonte} falhou", extra={"error": str(e)})
                resultados[fonte] = CrawlResult(
                    source=fonte, total=0, status="failed",
                    started_at=datetime.now(), errors=[{"error": str(e)}]
                )
    return resultados

# asyncio + gather para requests paralelos
import asyncio
import aiohttp

async def crawlear_async(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_json(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
        resp.raise_for_status()
        return await resp.json()
```

## Tooling

```bash
# Formatação
ruff format scripts/

# Lint
ruff check scripts/

# Type check
mypy scripts/ --strict

# Testes com cobertura
pytest --cov=scripts --cov-report=term-missing -v

# Segurança
bandit -r scripts/ -ll

# Dependências
pip-audit
```

### Configuração pyproject.toml

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "B", "SIM", "UP"]

[tool.mypy]
strict = true
python_version = "3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --strict-markers"
markers = ["unit", "integration", "slow"]

[tool.bandit]
exclude_dirs = ["tests", ".venv"]
```

## Anti-Padrões — O que NUNCA Fazer

| Anti-padrão | Correção |
|-------------|----------|
| `def f(dados=[])` — mutable default | `def f(dados=None): dados = dados or []` |
| `type(x) == dict` — type check | `isinstance(x, dict)` |
| `x == None` — comparação com None | `x is None` |
| `from modulo import *` — wildcard | Importe explícito |
| `except:` — bare except | `except Exception:` ou específico |
| `except Exception: pass` — swallow | No mínimo `logger.exception()` |
| `str += "..."` em loop — O(n²) | `"".join(parts)` |
| `open()` sem `with` — leak | `with open(...) as f:` |

## Checklist Rápido

- [ ] Type hints em funções públicas (Python 3.9+ generics)
- [ ] `@dataclass` em vez de dict para estruturas conhecidas
- [ ] `with` para recursos (arquivos, conexões, locks)
- [ ] Geradores para volumes grandes (não carregar tudo em lista)
- [ ] `functools.wraps` em decorators
- [ ] `__slots__` em classes com milhares de instâncias
- [ ] `pathlib.Path` em vez de `os.path`
- [ ] f-strings em vez de `.format()` ou `%`
- [ ] `enumerate` em vez de `range(len(...))`
- [ ] `is None`, não `== None`
- [ ] `isinstance`, não `type()`
