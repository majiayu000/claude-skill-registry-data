---
name: perf-audit
description: Analisa código buscando gargalos de performance, complexidade algorítmica (Big-O) ineficiente e vazamentos de memória. Use para "otimizar esta query", "reduzir alocação de memória" ou "auditar gargalos".
---

## Foco de Análise (Checklist)

- **Complexidade (Time/Space)**: Loops aninhados desnecessários (O(N^2)), algoritmos de busca/ordenação ineficientes.
- **Gerenciamento de Memória**: Alocações excessivas em rotas quentes (Zero-Allocation patterns), vazamento de referências, objetos não coletados (Garbage Collection pressure).
- **I/O e Banco de Dados**: Problemas de N+1 queries, ausência de paginação em grandes conjuntos de dados, chamadas de rede síncronas bloqueantes, falta de índices.
- **Concorrência**: Deadlocks, race conditions, uso inadequado de mutex/locks, subutilização de threads/goroutines/assincronismo.

## Workflow

1. **Profiling Estático**: Lê o arquivo/módulo especificado e mapeia as áreas de maior custo computacional.
2. **Relatório de Gargalos**: Gera um documento técnico simples em `docs/todo/` contendo as ineficiências encontradas e a prova matemática/técnica da degradação.
3. **Plano de Refatoração**: Se o Tech Lead autorizar, propõe as mudanças de código (ex: introdução de cache, batching, reescrita de loops) repassando para o Developer aplicar.
