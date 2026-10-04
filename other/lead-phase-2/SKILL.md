---
name: lead-phase-2
description: Fase 2 do lead-finder — Google WebSearch para descoberta de perfis
user-invocable: false
---

# Fase 2 — Google WebSearch (Descoberta)

Leia o state file:
```bash
cat data/_state/lead-finder-progress.json
```

## 2.1 Executar WebSearch para cada query

Para CADA query gerada na Fase 1, use WebSearch:
```
WebSearch: site:instagram.com "psicologa" "florianopolis"
```

De cada resultado, extraia o username do Instagram da URL.
Formato: `https://www.instagram.com/USERNAME/`

**Regex para extrair username:**
- Capture o path apos `instagram.com/`
- IGNORE: `/p/`, `/reel/`, `/explore/`, `/stories/`, `/tv/`, `/accounts/`
- Um username valido: letras, numeros, pontos, underscores

## 2.2 Deduplicar

- Remova duplicatas (mesmo username de queries diferentes)
- Remova usernames ja encontrados no cache local (Fase 1)

## 2.3 Checar cache de visitados

Para cada username na lista, use o MCP de cache:
```
instagram_check_visited(username, param_key)
```
- Se "VISITADO" → pule (0 custo)
- Se "NOVO" → mantenha na lista

## 2.4 Ordenar

Ordene a lista do MENOS provavel de ser popular ao MAIS provavel.
Perfis que aparecem em menos resultados de busca tendem a ser menores/mais novos — esses sao prioridade.

## 2.5 Salvar no state

Atualize: candidates (lista de usernames novos para validar).

Mostre ao usuario:
```
Google Search: X resultados totais
Usernames unicos: Y
Do cache (pulados): Z
Novos para validar: W
```

## CRITERIO DE CONCLUSAO
- Todas as queries executadas via WebSearch
- Usernames extraidos e deduplicados
- Cache de visitados checado
- Lista de candidatos ordenada e salva no state
- Progresso mostrado ao usuario
