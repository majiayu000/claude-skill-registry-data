---
name: task-onboarding
description: Skill para preparar contexto de tarefas de desenvolvimento; bloqueia início se artefatos obrigatórios faltarem.
---

# Quando usar

Acionar antes de qualquer análise ou implementação para garantir contexto mínimo completo.

# Objetivo

Validar presença de artefatos críticos, gerar Quick Context e registrar gaps antes de prosseguir.

# Passos

1) Acionar `context-manager` para gerar **Quick Context (<500 tokens)** cobrindo objetivo, escopo, artefatos carregados, integrações críticas, gaps.  
2) Verificar obrigatórios: `tasks.md`, todos `*_*task.md`, `prd.md`, `techspec.md`, instruções de execução (comandos yarn/npm, envs, deps externas).  
3) Se faltar algo: PAUSAR, listar faltantes, solicitar ao solicitante e não avançar.  
4) Opcional: registrar diagramas fornecidos (arquitetura/seq/DB).  
5) Confirmar número da task ativa e dependências entre `n_task.md`.  
6) Registrar checkpoint inicial via context-manager.

# Saídas esperadas

- Quick Context salvo pelo context-manager.  
- Lista de gaps ou confirmação de completude.  
- Checkpoint inicial do contexto.
