---
name: medidas-executivas-atipicas
description: "Requer medidas executivas atipicas com base no poder geral de efetivacao (CPC 139 IV — o juiz determina TODAS as medidas indutivas, coercitivas, mandamentais ou sub-rogatorias necessarias para assegurar o cumprimento, inclusive nas acoes de prestacao pecuniaria), sistematizadas pela tutela especifica das obrigacoes de fazer/nao fazer (CPC 536-537), com limites de proporcionalidade, contraditorio, fundamentacao concreta e subsidiariedade (so apos esgotar os meios tipicos). Use quando o operador disser medidas atipicas, art. 139 IV, suspender CNH do devedor, apreender passaporte, medidas coercitivas execucao, devedor contumaz."
---

# MEDIDAS-EXECUTIVAS-ATIPICAS

> Camada 7 (cumprimento & execucao). Municao de ultima rampa contra o devedor que pode pagar e nao paga. Da a base civel do requerimento; o fluxo pesado de execucao vive em `execucao-adv-os`. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — art. 139 IV (poder geral de efetivacao — todas as medidas indutivas, coercitivas, mandamentais ou sub-rogatorias, inclusive nas acoes de prestacao pecuniaria), arts. 536 (efetivacao da tutela especifica nas obrigacoes de fazer/nao fazer) e 537 (multa — suficiente, compativel e com prazo razoavel) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so vistoriados).

## Objetivo
Obter medidas atipicas eficazes e que sobrevivam ao crivo recursal: requerimento fundamentado na contumacia do devedor, na subsidiariedade (meios tipicos exauridos) e na proporcionalidade — nunca como punicao gratuita.

## Quando ativar
- Esgotados os meios tipicos (SISBAJUD, RENAJUD, INFOJUD, penhora) sem satisfacao do credito.
- Devedor mantem padrao de vida incompativel com a alegada insolvencia (contumaz / ocultacao patrimonial).
- Obrigacao de fazer/nao fazer que demanda coercao indireta.

## Metodologia
1. **Gestao processual (Camada 2):** `competencia-e-foro` (juizo da execucao) ; `tempestividade-civel` ; debito -> `calculosjudiciais-adv-os`.
2. **Fundamento (CPC 139 IV):** o juiz pode determinar **todas as medidas** indutivas, coercitivas, mandamentais ou sub-rogatorias necessarias ao cumprimento, **inclusive nas acoes de prestacao pecuniaria** — base expressa para a medida atipica tambem na execucao por quantia.
3. **Base sistematica (CPC 536-537):** nas obrigacoes de fazer/nao fazer o juiz determina as medidas necessarias a tutela especifica ou ao resultado pratico equivalente (536) e fixa multa suficiente, compativel e com prazo razoavel (537) — logica que orienta o desenho da medida.
4. **Subsidiariedade:** comprovar nos autos o **esgotamento dos meios tipicos** (relatorio das diligencias frustradas) antes de pedir a medida atipica; sem isso, ela tende a cair em sede recursal.
5. **Contumacia e utilidade:** indicios concretos de capacidade de pagar com ocultacao de patrimonio, e nexo entre a medida e a coercao ao pagamento (a medida deve induzir o adimplemento, nao apenas restringir).
6. **Proporcionalidade e contraditorio:** medida adequada, necessaria e proporcional; contraditorio previo e fundamentacao concreta (vedada decisao generica); pedir gradacao (medidas menos gravosas primeiro).
7. **Jurisprudencia (constitucionalidade das atipicas — apreensao de CNH/passaporte, com ressalvas, reconhecida pelo STF em controle concentrado):** so com numero (ex.: ADI) se constar em `context/jurisprudencia-civel.md`; senao, entendimento do STF — a confirmar via `validador-civel`, **sem numero**, ressalvando que a admissao e excepcional e exige fundamentacao concreta.

## Entrega obrigatoria final
- Peticao com fundamento no CPC 139 IV (e 536-537 quando pertinente) + relatorio do esgotamento dos meios tipicos + indicios de contumacia + medida pedida com gradacao e proporcionalidade + debito atualizado.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: execucao pesada / recuperacao de credito complexa -> `execucao-adv-os`; atualizacao/juros -> `calculosjudiciais-adv-os`.
