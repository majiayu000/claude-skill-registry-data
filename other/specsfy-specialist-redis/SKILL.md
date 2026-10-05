---
name: specsfy-specialist-redis
description: Projetar e operar Redis para cache, filas, sessões, rate limiting, locks, streams e dados efêmeros com limites e falhas explícitos. Use quando houver Redis, Valkey-compatible clients, TTLs, Lua, clusters, Sentinel ou persistência; não trate Redis como banco durável sem requisitos explícitos.
---

# Redis

## Fluxo

1. Definir finalidade do dado, source of truth, consistência e tolerância à perda.
2. Estimar cardinalidade, tamanho, taxa, TTL e padrão de acesso.
3. Escolher estrutura e chave com namespace estável.
4. Projetar stampede, invalidação, retry, idempotência e falha do Redis.
5. Configurar limites de memória, eviction e persistência conforme o caso.
6. Testar concorrência, expiração, indisponibilidade e recuperação.
7. Medir hit rate, latência, memória, conexões e hot keys.

## Padrões

- Dar TTL a caches e definir quem invalida cada chave.
- Evitar comandos bloqueantes e varreduras globais no caminho de produção.
- Usar operações atômicas ou Lua quando a invariância exigir.
- Tratar locks distribuídos como leases com timeout e ownership verificável.
- Separar namespaces e políticas de eviction de workloads incompatíveis.
- Não serializar objetos sem versão nem armazenar segredos desnecessários.
- Confirmar semântica de entrega e reprocessamento em filas ou streams.

## Validação

- Exercitar miss, hit, expiração, stampede e Redis indisponível.
- Verificar limites, eviction, persistência e failover em ambiente representativo.
- Observar `INFO`, slow log e métricas do cliente sem expor valores sensíveis.
- Comparar comportamento com e sem cache para preservar correção.

Leia [references/standards.md](references/standards.md) para estruturas,
persistência, cluster, segurança e padrões de cache.
