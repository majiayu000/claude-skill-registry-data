---
name: cobranca-e-monitoria
description: "Redige acao de cobranca pelo rito comum (quando nao ha prova escrita) ou acao monitoria (CPC 700-702 - prova escrita SEM eficacia de titulo executivo): cheque prescrito, nota promissoria sem forca, contrato sem aceite. Mandado de pagamento + honorarios 5% (701); embargos ao mandado (702); prazos prescricionais (CC 206). Use quando o operador disser cobrar divida, acao de cobranca, monitoria, cheque prescrito, nota promissoria sem forca, ou contrato sem titulo executivo."
---

# COBRANCA-E-MONITORIA

> Camada 5 (acoes civeis). Credito SEM titulo executivo. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 700 (monitoria - prova escrita sem eficacia executiva), 701 (mandado de pagamento + honorarios 5% + prazo 15 dias), 702 (embargos a acao monitoria) + 318-321/324 (rito comum) — **grep + ler a faixa**.
- `context/cc-10406-02.md` — art. 206 (prazos prescricionais) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so vistoriados).

## Objetivo
Cobrar credito quando NAO ha titulo executivo: via monitoria (se ha prova escrita sem eficacia executiva — CPC 700) ou via cobranca pelo rito comum (se nao ha prova escrita), com a prescricao do CC 206 sob controle.

## Quando ativar
- Credor tem prova escrita sem forca de titulo (cheque prescrito, NP sem forca, contrato sem aceite, e-mails/recibos de confissao) -> **monitoria**.
- Credor nao tem prova escrita do credito -> **cobranca pelo rito comum**.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `competencia-e-foro` · `valor-da-causa` (na monitoria, corresponde a importancia do CPC 700 §2o/§3o) · `gratuidade-e-impugnacao` · `tempestividade-civel`.
2. **Triagem da via:** ha prova escrita sem eficacia de titulo executivo (700)? Sim -> monitoria. Nao -> cobranca de conhecimento.
3. **Prescricao (CC 206):** localizar o prazo aplicavel ao credito e confirmar que NAO prescreveu antes de ajuizar.
4. **Monitoria (700-702):** explicitar a importancia devida com memoria de calculo (700 §2o, I); pleitear a expedicao do mandado de pagamento com honorarios de 5% e prazo de 15 dias (701); antecipar que, nao pagos e nao opostos embargos (702), constitui-se titulo executivo judicial de pleno direito (701 §2o).
5. **Cobranca pelo rito comum:** pedido condenatorio certo (324), instruido com a prova disponivel; requerer producao de prova.
6. **Instruir** com a prova escrita (na monitoria) e antecipar o controle (330/332).

## Entrega obrigatoria final
- Inicial (monitoria OU cobranca) ponta a ponta + memoria de calculo do credito + analise de prescricao (CC 206) + checklist de documentos + foro/vara.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria. Entrega pela `suprema-corte-civel`. Cross-link OBRIGATORIO: se JA existe TITULO EXECUTIVO -> `execucao-adv-os` (esta skill e so para credito SEM titulo). Calculo pesado -> nao duplicar.
