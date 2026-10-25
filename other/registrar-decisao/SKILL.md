---
name: registrar-decisao
description: Registra uma decisão de produto, de dados ou técnica no DECISOES.md com motivo e impacto. Use quando o time ou o agente decidir algo que não estava em docs/fluxo-sistema.md, ou ao excluir pacientes da fila.
argument-hint: [descrição da decisão]
---

Registre a decisão: $ARGUMENTS

1. Leia `DECISOES.md` e descubra o próximo ID livre (`D-xx`; os IDs `D-01`..`D-10` vêm de `docs/fluxo-sistema.md`).
2. Se faltar o **motivo** ou a **alternativa descartada**, pergunte em uma frase antes de escrever.
3. Adicione uma linha na tabela "Decisões" com: ID, data (AAAA-MM-DD), decisão, motivo, alternativa descartada, quem decidiu (se informado), componente afetado (C-xx).
4. Se a decisão resolve uma questão aberta `Q-xx`, marque-a como resolvida em `docs/fluxo-sistema.md` §11 apontando para o novo ID.
5. Se a decisão exclui solicitações da fila, liste-as (ou a regra que as seleciona e a contagem) na seção "Solicitações fora da fila".
6. Não reescreva entradas antigas; decisões revertidas ganham nova linha "reverte D-xx".
