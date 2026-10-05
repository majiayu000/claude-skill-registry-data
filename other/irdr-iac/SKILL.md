---
name: irdr-iac
description: "Instaura/atua em IRDR — Incidente de Resolucao de Demandas Repetitivas (CPC 976, requisitos simultaneos: I efetiva repeticao sobre questao unicamente de direito + II risco a isonomia/seguranca; legitimados 977; admissibilidade 981; suspensao no Estado/regiao 982 I; tese aplicada a todos e aos casos futuros 985; revisao 986; REsp/RE 987) ou IAC — Incidente de Assuncao de Competencia (CPC 947, questao relevante de grande repercussao social SEM repeticao; acordao vinculante §3), com efeito vinculante da tese (CPC 927 III). Use quando o operador disser IRDR, incidente de resolucao de demandas repetitivas, IAC, assuncao de competencia, tese vinculante regional, muitos processos iguais, suspensao por IRDR."
---

# IRDR-IAC

> Camada 8 (incidentes processuais). Forma teses vinculantes no tribunal local/regional. IRDR = questao que se repete; IAC = questao relevante sem repeticao. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — IRDR: arts. 976 (requisitos I-II simultaneos + §4 incabivel se tribunal superior ja afetou repetitivo), 977 (legitimados: juiz/relator, partes, MP, Defensoria), 981 (admissibilidade), 982 (admitido: I suspensao no Estado/regiao, III MP), 985 (tese a todos e aos casos futuros + §1 reclamacao), 986 (revisao), 987 (REsp/RE). IAC: art. 947 (questao relevante de grande repercussao social sem repeticao + §3 vinculacao). Vinculacao: art. 927 III — **grep + ler a faixa**.

## Objetivo
Usar a tese vinculante como instrumento estrategico: provocar a instauracao quando a uniformizacao favorece o cliente, ou requerer suspensao/aplicacao da tese firmada; escolher entre IRDR (ha repeticao) e IAC (nao ha).

## Quando ativar
- Efetiva repeticao sobre a mesma questao unicamente de direito, com risco a isonomia/seguranca (IRDR — CPC 976).
- Questao de direito relevante, de grande repercussao social, SEM repeticao (IAC — CPC 947).
- O processo do cliente pode ser suspenso por IRDR instaurado, ou ha tese firmada a aplicar/afastar.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `estrategia-processual` (a tese vinculante e arma de dois gumes — confirmar se a uniformizacao favorece o cliente antes de provocar); `memoria-de-caso-civel`.
2. **Escolher o incidente:** HA efetiva repeticao sobre questao unicamente de direito + risco a isonomia/seguranca = IRDR (CPC 976, I e II SIMULTANEOS). Questao relevante de grande repercussao social mas SEM repeticao = IAC (CPC 947). Conferir 976 §4: incabivel IRDR se tribunal superior ja afetou repetitivo sobre a mesma questao.
3. **IRDR — legitimidade e admissibilidade:** dirigir ao presidente do tribunal (CPC 977 — juiz/relator por oficio; partes, MP, Defensoria por peticao), instruido com a demonstracao dos pressupostos. O orgao colegiado faz o juizo de admissibilidade pelos pressupostos do art. 976 (CPC 981).
4. **IRDR — suspensao e tese:** admitido, o relator suspende os processos no Estado/regiao (CPC 982, I) e intima o MP (982, III). Julgado, a tese aplica-se a todos os processos sobre identica questao na area do tribunal e aos casos futuros (CPC 985, I e II); descumprida, cabe reclamacao (985 §1). Revisao pelo mesmo tribunal (986). Do merito cabe REsp/RE (987).
5. **IAC — sem repeticao:** o acordao vincula todos os juizes e orgaos fracionarios, salvo revisao de tese (CPC 947 §3) — uniformizacao para questao nova e relevante sem multiplos processos.
6. **Efeito vinculante (CPC 927 III):** IRDR e IAC integram o rol de precedentes obrigatorios — fundamentar a forca da tese sobre o caso concreto.

## Entrega obrigatoria final
- Peca redigida ponta a ponta conforme o incidente (peticao de instauracao com os pressupostos + delimitacao da questao unicamente de direito OU requerimento de suspensao/aplicacao da tese firmada) + analise de conveniencia estrategica + orgao destinatario.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: pesquisa e aplicacao de tese repetitiva/repercussao geral dos tribunais superiores e modulacao -> `jurisprudencia-civel` + `validador-civel`; conflito entre juizos -> `conflito-de-competencia`.
