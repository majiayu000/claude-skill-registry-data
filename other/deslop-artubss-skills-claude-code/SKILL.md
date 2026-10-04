---
name: deslop
description: Remove código gerado por IA de uma branch. Use ao limpar código gerado por IA, removendo comentários desnecessários, validações defensivas ou conversões de tipo. Verifica diff contra main e corrige inconsistências de estilo.
---

# Remover Slop de Código IA

Verifique o diff contra main e remova todo o slop gerado por IA introduzido nesta branch.

## O que Remover

- Comentários extras que um humano não adicionaria ou que são inconsistentes com o resto do arquivo
- Validações defensivas extras ou blocos try/catch que são anormais para essa área do código (especialmente se chamados por caminhos de código confiáveis/validados)
- Conversões para `any` para contornar problemas de tipo
- Imports inline em Python (mover para o topo do arquivo com outros imports)
- Qualquer outro estilo que seja inconsistente com o arquivo

## Processo

1. Obtenha o diff contra main: `git diff main...HEAD`
2. Revise cada arquivo alterado procurando por padrões de slop
3. Remova o slop identificado enquanto preserva mudanças legítimas
4. Relate um resumo de 1-3 sentenças do que foi alterado