---
name: dispatching-parallel-agents
description: Orquestrar trabalho paralelo com multiplos sub-agents quando ha 2+ tarefas independentes. Usar automaticamente quando detectar tarefas sem dependencia entre si.
---

# Despacho de Agentes Paralelos -- Padrao DME

Quando ha multiplas tarefas independentes, despachar um agent por dominio.

## Quando usar

- 2+ falhas/bugs em subsistemas diferentes
- Tarefas que nao compartilham estado (frontend + backend + testes)
- Pesquisa em areas independentes do codebase

## Quando NAO usar

- Tarefas que dependem uma da outra
- Edicoes no mesmo arquivo
- Trabalho sequencial

## Processo

1. Listar todas as tarefas pendentes
2. Classificar como INDEPENDENTE ou DEPENDENTE
3. Agrupar independentes por dominio
4. Despachar um agent por grupo com prompt especifico
5. Aguardar resultados
6. Sintetizar e reportar

## Regras

- Cada agent recebe contexto completo do seu dominio
- Nunca dois agents editando o mesmo arquivo
- Usar modelo apropriado por agent (Haiku pra pesquisa, Sonnet pra implementacao)
