---
name: write-specs
description: Modelo de especificação de produto com histórias de usuário e critérios de aceite.
---

# Skill: write-specs

Use para produzir `work/<ciclo>/01-spec.md`.

## Estrutura
1. **Contexto e objetivo**: problema, para quem, por quê agora.
2. **Métrica de sucesso**: número ou observação verificável.
3. **Escopo**: dentro / fora.
4. **Histórias de usuário** (priorize: Deve / Deveria / Poderia):
   > Como <papel>, quero <ação>, para <benefício>.
   - Critérios de aceite:
     - Dado <contexto>, quando <ação>, então <resultado observável>.
5. **Requisitos não funcionais**: desempenho, segurança, acessibilidade, idioma.
6. **Suposições e perguntas em aberto**.

## Regras
- Mínimo de 2 critérios por história, ao menos um cobrindo erro ou caso de borda.
- Sem tecnologia na spec.
- Se algo é desconhecido, escreva como pergunta, não como fato.
