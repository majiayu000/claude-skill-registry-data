---
name: coding-standards
description: |
  Convenções de código Python para o projeto Extra Consultoria.
  Cobre nomenclatura, imutabilidade, legibilidade, KISS, DRY, YAGNI,
  organização de arquivos e detecção de code smells.
origin: ECC (adaptado para Extra Consultoria)
---

# Coding Standards — Padrões de Código Python

## Quando Ativar

- Iniciando novos módulos ou scripts
- Conduzindo code review
- Refatorando para alinhar com convenções
- Configurando lint/format/type-check
- Onboarding de novos contribuidores

## Escopo

**Ativar para:**
- Nomenclatura descritiva
- Imutabilidade por padrão
- Legibilidade, KISS, DRY, YAGNI
- Expectativas de tratamento de erro
- Detecção de code smells

**Não usar como fonte primária para:**
- Padrões específicos de crawling (ver `error-handling`)
- Padrões Pythonicos detalhados (ver `python-patterns`)
- Arquitetura de sistema (ver `@architect`)

## Princípios de Qualidade

### 1. Legibilidade em Primeiro Lugar

Código é lido mais do que escrito. Priorize clareza.

```python
# ✅ Bom — nomes descritivos
licitacoes_por_uf = agrupar_por_estado(resultados_busca)
fornecedores_ativos = [f for f in fornecedores if f.status == "ativo"]

# ❌ Ruim — nomes vagos
x = agrupar(res)
fs = [f for f in fs if f.s == "ativo"]
```

### 2. KISS (Keep It Simple, Stupid)

Solução mais simples que funciona. Sem over-engineering.

```python
# ✅ Simples e claro
if config.get("fontes"):
    for fonte in config["fontes"]:
        crawlear(fonte)

# ❌ Over-engineered
class CrawlOrchestratorFactory:
    def create_orchestrator(self, strategy: CrawlStrategy) -> CrawlOrchestrator:
        ...
```

### 3. DRY (Don't Repeat Yourself)

Extraia lógica repetida em funções reutilizáveis.

```python
# ✅ DRY — extraído para função
def requisicao_com_retry(url: str, **kwargs) -> requests.Response:
    return with_retry(lambda: session.get(url, timeout=30, **kwargs))

# ❌ WET — copypaste em cada crawler
def crawlear_pncp():
    try:
        resp = requests.get(url, timeout=30)
    except Exception:
        ...
def crawlear_sc():
    try:
        resp = requests.get(url, timeout=30)
    except Exception:
        ...
```

### 4. YAGNI (You Aren't Gonna Need It)

Não construa antes de precisar. Comece simples, refatore quando necessário.

```python
# ✅ Suficiente para agora
def salvar_resultados(dados: list[dict], arquivo: str) -> None:
    with open(arquivo, "w") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ❌ YAGNI — "vai que precise de outro formato depois"
class ResultadoSerializer:
    def to_json(self): ...
    def to_csv(self): ...
    def to_parquet(self): ...
    def to_excel(self): ...
```

## Nomenclatura Python

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Módulo/arquivo | `snake_case` | `sc_compras_crawler.py` |
| Função | `snake_case` verbo + substantivo | `crawlear_portal()`, `parsear_licitacao()` |
| Classe | `PascalCase` | `CrawlMonitor`, `DataLakeClient` |
| Constante | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Variável | `snake_case` descritiva | `total_licitacoes`, `uf_origem` |
| Booleano | `is_`, `has_`, `should_` | `is_ativo`, `has_anexos`, `should_retry` |
| Privado | `_` prefixo | `_cache_interno`, `_ibge_cache` |

```python
# ✅ Bom — nomes expressivos
def buscar_licitacoes_por_uf(uf: str, dias: int = 30) -> list[dict]:
    ...

# ❌ Ruim — nome vago, sem type hints
def busca(u, d=30):
    ...
```

## Imutabilidade (CRÍTICO)

Sempre crie novos objetos, nunca modifique os existentes:

```python
# ✅ Criar novo
config_atualizado = {**config, "timeout": 60}
resultados = [*resultados_anteriores, novo_resultado]

# ❌ Mutação in-place
config["timeout"] = 60
resultados.append(novo)
```

Para estruturas complexas, use `dataclasses.replace` ou crie nova instância:

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)  # frozen = imutável
class CrawlResult:
    source: str
    total: int
    items: tuple  # tuple, não list

# "Modificar" = criar novo
resultado_atualizado = replace(resultado, total=resultado.total + 1)
```

## Estrutura de Arquivos do Projeto

```
scripts/
├── crawl/              # Crawlers de fontes governamentais
│   ├── monitor.py      # Orquestrador principal
│   ├── pncp_crawler.py # Crawler PNCP
│   └── sc_compras_crawler.py  # Crawler SC Compras
├── intel_pipeline.py   # Pipeline de inteligência
├── local_datalake.py   # CLI do DataLake
├── reports/            # Relatórios
│   └── panorama.py
config/
├── transparencia_config.yaml
tests/
├── conftest.py
├── test_cache_ibge.py
├── test_transformer.py
└── test_crawlers/
```

### Convenções de Import

Ordem: standard library → third-party → local

```python
# 1. Standard library
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta

# 2. Third-party
import requests
import yaml
from bs4 import BeautifulSoup

# 3. Local
from scripts.crawl.enricher import enrich_licitacao
from scripts.local_datalake import DataLakeClient
```

## Code Smells — O que Evitar

### Função Longa (> 50 linhas)

Divida em funções menores com responsabilidade única:

```python
# ✅ Dividido em etapas
def executar_pipeline(cnpj: str, ufs: list[str]) -> dict:
    dados_brutos = coletar_dados(cnpj, ufs)
    dados_validados = validar_dados(dados_brutos)
    dados_enriquecidos = enriquecer_dados(dados_validados)
    return gerar_relatorio(dados_enriquecidos)
```

### Aninhamento Profundo (> 4 níveis)

Use early returns para achatar:

```python
# ✅ Early return
def processar(item):
    if not item:
        return None
    if item.status != "ativo":
        return None
    if not item.tem_dados_validos():
        logger.warning("Dados inválidos", extra={"item_id": item.id})
        return None
    return transformar(item)

# ❌ Aninhamento profundo
def processar(item):
    if item:
        if item.status == "ativo":
            if item.tem_dados_validos():
                return transformar(item)
            else:
                logger.warning("...")
```

### Números Mágicos

Extraia para constantes nomeadas:

```python
# ✅ Constantes nomeadas
MAX_RETRIES = 3
TIMEOUT_PADRAO_MS = 30_000
LIMITE_LICITACOES_POR_PAGINA = 100

# ❌ Números soltos
for i in range(3):
    time.sleep(30)
    if len(results) > 100:
        break
```

## Comentários e Documentação

### Quando Comentar

- Explique **por que** uma decisão foi tomada, não **o que** o código faz
- Documente desvios intencionais (ex: mutação por performance)
- Nunca afirme o óbvio

```python
# ✅ Bom — explica o porquê
# PNCP retorna JSON com encoding ISO-8859-1 em algumas UFs (bug conhecido do portal)
# Forçamos UTF-8 com replace para não perder o lote inteiro por um caractere
texto = response.content.decode("utf-8", errors="replace")

# ❌ Ruim — afirma o óbvio
# Faz a requisição HTTP
response = requests.get(url)
```

### Docstrings para Funções Públicas

```python
def crawlear_portal(
    source: str,
    mode: str = "incremental",
    ano: int | None = None,
) -> CrawlResult:
    """Executa crawl de um portal de transparência.

    Args:
        source: Identificador da fonte (pncp, sc_compras, etc.)
        mode: Modo de crawl — "full" ou "incremental"
        ano: Ano filtro. None = todos os anos.

    Returns:
        CrawlResult com total de itens coletados e status.

    Raises:
        ConfigError: Se source não estiver em transparencia_config.yaml
        CrawlError: Se todas as tentativas de crawl falharem

    Example:
        >>> resultado = crawlear_portal("pncp", mode="full", ano=2026)
        >>> print(resultado.total)
        1543
    """
    ...
```

## Checklist Pre-Commit

- [ ] `ruff check scripts/` passa sem erros
- [ ] `ruff format --check scripts/` passa (ou `ruff format` aplicado)
- [ ] `mypy scripts/` sem novos erros
- [ ] Funções novas têm docstring
- [ ] Números mágicos extraídos para constantes
- [ ] Nenhum `except: pass` ou `except Exception: pass`
- [ ] Imports ordenados (stdlib → third-party → local)
- [ ] Nomes descritivos (sem `x`, `tmp`, `data`, `result`)
