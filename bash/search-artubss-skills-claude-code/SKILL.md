---
name: search
description: Busca no Google via API SERP do Bright Data. Retorna resultados JSON estruturados com título, link e descrição. Requer as variáveis de ambiente BRIGHTDATA_API_KEY e BRIGHTDATA_UNLOCKER_ZONE.
---

# Bright Data - Google Search

Busque no Google e obtenha resultados JSON estruturados usando a API SERP do Bright Data.

## Configuração

**1. Obtenha sua API Key:**
Obtenha uma chave no [Painel do Bright Data](https://brightdata.com/cp).

**2. Crie uma zona Web Unlocker:**
Crie uma zona em brightdata.com/cp clicando em "Add" (canto superior direito) e selecionando "Unlocker zone".

**3. Configure as variáveis de ambiente:**
```bash
export BRIGHTDATA_API_KEY="sua-api-key"
export BRIGHTDATA_UNLOCKER_ZONE="seu-nome-de-zona"
```

## Uso

```bash
bash scripts/search.sh "query" [cursor]
```

**Parâmetros:**
- `query` (obrigatório): Termo de busca
- `cursor` (opcional): Número da página para paginação (iniciado em 0, padrão: 0)

**Exemplos:**
```bash
# Busca básica
bash scripts/search.sh "mudanças climáticas"

# Obter página 2 de resultados
bash scripts/search.sh "mudanças climáticas" 1
```

## Formato de Saída

Retorna JSON com array `organic` estruturado:
```json
{
  "organic": [
    {
      "link": "https://example.com/article",
      "title": "Título do Artigo",
      "description": "Breve descrição da página..."
    }
  ]
}
```

## Dependências

- `curl` - Para requisições de API
- `jq` - Para processamento JSON