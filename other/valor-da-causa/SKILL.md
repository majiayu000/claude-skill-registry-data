---
name: valor-da-causa
description: "Fixa o valor da causa civel conforme os criterios do CPC (arts. 291-293) e trata a impugnacao ao valor da causa. Cobre os criterios por tipo de pedido (cobranca, ato juridico, alimentos, divisao, indenizacao com pedido liquido), a soma de pedidos cumulados, e a impugnacao na contestacao. Use quando o operador disser valor da causa, quanto colocar de valor, impugnar valor da causa, custas, ou ao redigir a inicial/contestacao."
---

# VALOR-DA-CAUSA

> Camada 2 (gestao processual). Acionada em toda inicial e quando ha impugnacao.

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 291-293 (valor da causa) + 337 III (impugnacao). **grep + ler a faixa.**

## Objetivo
Atribuir o valor da causa correto (obrigatorio em toda acao, mesmo sem conteudo economico imediato) e saber impugnar o adversario.

## Quando ativar
- Ao redigir a peticao inicial (valor obrigatorio).
- Na contestacao, para impugnar o valor (preliminar art. 337 III).

## Metodologia
1. **Criterio por pedido (art. 292):** cobranca = valor do debito; ato/negocio juridico = valor do contrato; alimentos = 12 prestacoes; indenizacao (inclusive dano moral) = valor pretendido; etc.
2. **Cumulacao de pedidos:** somar (292 §1º); pedidos alternativos/subsidiarios = o de maior valor.
3. **Correcao de oficio** (292 §3º) ou por impugnacao do reu.
4. **Impugnacao (337 III):** arguida na contestacao; o juiz decide e corrige.
5. Indicar o valor + memoria do criterio.

## Entrega obrigatoria final
- Valor da causa fixado + criterio (artigo) + (se defesa) impugnacao fundamentada.

## Guard
Valor da causa nunca em branco. Citacao por `validador-civel`; valor adequado e item de R1/R4 da `suprema-corte-civel`.
