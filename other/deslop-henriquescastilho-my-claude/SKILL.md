---
name: deslop
description: Remover codigo com cara de IA -- comentarios obvios, over-engineering, abstraccoes prematuras, try/catch desnecessarios. Usar automaticamente antes de commits ou quando o codigo parece inflado.
allowed-tools: Read Edit Bash Grep Glob
---

# Limpeza de Codigo -- Padrao DME

Analisar o diff da branch atual e remover padroes tipicos de codigo gerado por IA.

## Execucao

```bash
git fetch origin main 2>/dev/null || git fetch origin master 2>/dev/null
git diff origin/main...HEAD --stat 2>/dev/null || git diff origin/master...HEAD --stat
git diff origin/main...HEAD 2>/dev/null || git diff origin/master...HEAD
```

## O que remover

- Comentarios que repetem o que o codigo ja diz
- Blocos try/catch defensivos em caminhos internos confiaveis
- Casts para `any` usados so pra silenciar o TypeScript
- Abstraccoes criadas pra uma unica chamada (helpers, factories prematuros)
- Codigo com aninhamento profundo que poderia usar early return
- Hacks de compatibilidade (`_vars` renomeadas, re-exports, `// removed`)
- Features, refatoracoes ou "melhorias" que ninguem pediu
- Docstrings e type annotations em codigo que nao foi alterado
- Error handling pra cenarios impossiveis

## Regras

- Manter o comportamento identico -- so limpar, nao mudar logica
- Edicoes minimas e focadas, nao reescritas amplas
- Tres linhas similares e melhor que uma abstracao prematura
- Verificar que o que foi removido e realmente inutil antes de apagar
- Rodar lint/type-check apos as edicoes

## Saida

- Lista de padroes encontrados com localizacao
- Edicoes aplicadas
- Resumo em uma linha do que foi limpo
