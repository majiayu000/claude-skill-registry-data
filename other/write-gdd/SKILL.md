---
name: write-gdd
description: Modelo de documento de design de jogo (GDD) enxuto e testável.
---

# Skill: write-gdd

Um GDD por mecânica ou sistema, em `docs/gdd/<nome>.md`. Curto e verificável.

## Estrutura
1. **Pilar atendido**: qual pilar do jogo esta mecânica serve.
2. **Resumo em 2 linhas**.
3. **Regras**: lista numerada, sem ambiguidade.
4. **Números iniciais**: tabela (valor, mínimo, máximo, "a validar").
5. **Casos de borda**: o que acontece quando as regras colidem.
6. **Feedback ao jogador**: visual, sonoro, tátil (vibração) e de interface.
7. **Dependências**: outras mecânicas, arte, áudio.
8. **Hipótese de diversão e como testar**: o que o playtest deve mostrar.
9. **Fora de escopo**.

## Regras
- Dois programadores diferentes devem implementar igual.
- Sem pilar, sem mecânica.
