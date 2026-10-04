---
name: verification-before-completion
description: Obrigar verificacao com evidencia antes de declarar trabalho completo. Usar automaticamente antes de commits, PRs, ou qualquer afirmacao de que algo esta pronto.
---

# Verificacao Antes de Concluir -- Padrao DME

Nenhuma afirmacao de conclusao sem evidencia fresca.

## Regra de ferro

SEM EVIDENCIA = SEM AFIRMACAO DE CONCLUSAO

Se o comando de verificacao nao foi executado NESTA mensagem, nao se pode afirmar que passa.

## Antes de declarar qualquer status

1. IDENTIFICAR: qual comando prova esta afirmacao?
2. EXECUTAR: rodar o comando completo (fresco, nao cache)
3. LER: analisar a saida real, nao assumir
4. SO ENTAO: declarar o status com base na saida

## Comandos de verificacao por tipo

| Afirmacao | Comando obrigatorio |
|-----------|-------------------|
| "Build passa" | npm run build ou equivalente |
| "Testes passam" | npm test ou pytest |
| "Lint limpo" | npx eslint . ou ruff check . |
| "Types ok" | npx tsc --noEmit |
| "Deploy pronto" | rodar deploy-check |
| "Bug corrigido" | reproduzir o cenario e mostrar que funciona |

## Proibido

- "Deve estar funcionando" -- sem evidencia nao conta
- "Acredito que passa" -- rodar e mostrar
- "Ja corrigi isso antes" -- rodar de novo agora
- Citar resultado de uma execucao anterior -- rodar fresco
