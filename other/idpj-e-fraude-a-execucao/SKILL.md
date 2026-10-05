---
name: idpj-e-fraude-a-execucao
description: "Atinge o patrimonio escondido do devedor — Incidente de Desconsideracao da Personalidade Juridica (CPC 133-137: instauracao a pedido da parte/MP, suspensao do processo, citacao do socio/PJ e contraditorio em 15 dias, decisao interlocutoria) com pressupostos do CC 50 (desvio de finalidade e confusao patrimonial, Lei 13.874/2019), e fraude a EXECUCAO (CPC 790 VII e 792 — ineficacia perante o exequente), distinguindo da fraude CONTRA credores / acao pauliana (CC 158-165). Use quando o operador disser desconsideracao da personalidade juridica, IDPJ, atingir bens do socio, fraude a execucao, fraude contra credores, devedor blindou patrimonio, confusao patrimonial."
---

# IDPJ-E-FRAUDE-A-EXECUCAO

> Camada 7 (cumprimento & execucao). Estende a responsabilidade patrimonial alem do devedor formal: socio/PJ (IDPJ) e bens dissipados (fraude). Da a base civel; o redirecionamento pesado vive em `execucao-adv-os`. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 133 (instauracao a pedido da parte/MP), 134 (cabivel em todas as fases; § 2o dispensa se requerido na inicial; § 3o suspende o processo; § 4o demonstrar pressupostos), 135 (citacao do socio/PJ — 15 dias), 136 (decisao interlocutoria; agravo interno se pelo relator), 137 (ineficacia da alienacao em fraude), 790 VII (bens do responsavel), 792 (fraude a execucao — hipoteses, § 1o ineficacia, § 3o marco na desconsideracao, § 4o intimacao do terceiro em 15 dias) — **grep + ler a faixa**.
- `context/cc-10406-02.md` — art. 50 (abuso da personalidade: desvio de finalidade § 1o, confusao patrimonial § 2o — Lei 13.874/2019), arts. 158-165 (fraude contra credores / pauliana) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so vistoriados).

## Objetivo
Levar a execucao ao patrimonio efetivamente responsavel, com pressupostos provados e contraditorio respeitado, distinguindo IDPJ x fraude e fraude a execucao x fraude contra credores.

## Quando ativar
- PJ executada sem bens, com indicios de desvio de finalidade ou confusao patrimonial (atingir socio).
- Devedor alienou/onerou bens ja na pendencia de acao capaz de reduzi-lo a insolvencia (fraude a execucao).
- Devedor dilapidou patrimonio antes do processo, em prejuizo de credores (fraude contra credores).

## Metodologia
1. **Gestao processual (Camada 2):** `competencia-e-foro` ; `tempestividade-civel` ; debito -> `calculosjudiciais-adv-os`.
2. **Escolher o instituto:**
   - **IDPJ (CPC 133-137 + CC 50):** estender a responsabilidade ao socio/PJ por **abuso da personalidade** — desvio de finalidade (CC 50 § 1o) **ou** confusao patrimonial (§ 2o, incisos I a III). Demonstrar no requerimento (134 § 4o).
   - **Fraude a execucao (CPC 790 V/VII e 792):** alienacao/oneracao na pendencia de demanda capaz de gerar insolvencia (792 IV) ou demais hipoteses. Efeito: **ineficacia** perante o exequente (792 § 1o), reconhecida nos proprios autos, sem anular o negocio.
   - **Fraude contra credores / pauliana (CC 158-165):** vicio anterior, por ato gratuito do insolvente (158) ou oneroso com insolvencia notoria (159). Exige **acao autonoma**; resulta em **anulacao**, nao mera ineficacia.
3. **Rito do IDPJ:** a pedido da parte/MP (133); **suspende o processo** (134 § 3o), salvo se na inicial (134 § 2o); citar o socio/PJ para manifestar-se em **15 dias** (135); decisao **interlocutoria** (136) — agravo de instrumento (ou agravo interno se pelo relator).
4. **Efeitos:** acolhido o IDPJ ou reconhecida a fraude, o ato e **ineficaz perante o requerente** (137). Na desconsideracao, a fraude verifica-se a partir da citacao da parte cuja personalidade se pretende desconsiderar (792 § 3o).
5. **Contraditorio do terceiro:** antes de declarar a fraude, intima-se o terceiro adquirente, que pode opor embargos de terceiro em 15 dias (792 § 4o) -> `embargos-de-terceiro`.
6. **Jurisprudencia (Sumula 375 STJ sobre registro/ma-fe; teses de IDPJ):** so com numero se constar em `context/jurisprudencia-civel.md`; senao, entendimento dos tribunais — confirmar via `validador-civel`, **sem numero**.

## Entrega obrigatoria final
- Peticao do incidente (ou requerimento de fraude a execucao, ou inicial da pauliana) com instituto correto + pressupostos provados (CC 50 ou CPC 792) + bens a atingir + pedido de citacao/intimacao.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: redirecionamento pesado / recuperacao de credito complexa -> `execucao-adv-os`; debito -> `calculosjudiciais-adv-os`; oposicao do terceiro -> `embargos-de-terceiro`.
