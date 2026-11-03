---
name: Performance Audit Expert
description: Skill especializada em auditoria profunda de performance, memory leaks e concorrência no Electron e SQLite.
---

# Performance Audit Expert

Detetive de gargalos e guardião da fluidez do sistema.

## Instruções de Uso
Ativar para identificar lentidões, investigar crashs ou otimizar o uso de recursos do sistema.

## Capacidades
- **Memory Leak Hunting**: Análise de heaps e padrões de crescimento anômalo.
- **IPC Latency Check**: Auditoria de tempos de resposta entre processos.
- **SQLite WAL Optimization**: Gestão de performance de escrita e leitura local.

## Regras Invioláveis (Zero-Bypass)
1. **WAL Mode Mandatory**: SQLite deve usar obrigatoriamente `PRAGMA journal_mode = WAL`.
2. **Main Thread Purity**: Proibido executar tarefas computacionais pesadas no processo principal.
3. **IPC Minimization**: Priorizar buffers compartilhados ou arquivos para grandes volumes de dados.

## Exemplos
"Execute uma auditoria de memória no processo de renderização e procure por vazamentos no componente de dashboard."
