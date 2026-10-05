---
name: conflito-de-competencia
description: "Suscita conflito de competencia ao tribunal (CPC 66 — positivo: dois juizes se declaram competentes; negativo: ambos incompetentes; ou controversia sobre reuniao/separacao), por parte, MP ou juiz (CPC 951), vedado a quem ja arguiu incompetencia relativa (CPC 952), por oficio ou peticao instruida (CPC 953), com designacao de juiz para medidas urgentes (CPC 955) e declaracao do juizo competente e dos atos validos (CPC 957). Use quando o operador disser conflito de competencia, dois juizes se dizem competentes, nenhum juizo aceita o processo, suscitar conflito, qual juizo e competente."
---

# CONFLITO-DE-COMPETENCIA

> Camada 8 (incidentes processuais). Define qual juizo julga quando dois (ou mais) divergem sobre a propria competencia. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 66 (positivo I, negativo II, reuniao/separacao III + par. unico — dever do juiz que nao acolhe a competencia declinada de suscitar), 951 (legitimados: parte, MP, juiz), 952 (vedacao a quem arguiu incompetencia relativa), 953 (forma: oficio/peticao instruida), 954 (oitiva dos juizes), 955 (sobrestamento + designacao para medidas urgentes + julgamento de plano), 956 (MP em 5 dias), 957 (declara o juizo competente e a validade dos atos) — **grep + ler a faixa**.

## Objetivo
Resolver a indefinicao de juizo: enquadrar o conflito (positivo, negativo ou de reuniao/separacao), suscitar ao tribunal competente com peticao instruida e, havendo risco, pedir designacao de juiz para os atos urgentes ate o julgamento.

## Quando ativar
- Dois ou mais juizes se declaram competentes para a mesma causa (positivo).
- Dois ou mais se consideram incompetentes, atribuindo um ao outro a competencia (negativo).
- Surge controversia entre juizes sobre reuniao ou separacao de processos.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `competencia-e-foro` (mapear a regra em disputa — absoluta x relativa); `memoria-de-caso-civel` (registrar as duas decisoes conflitantes).
2. **Enquadrar a especie (CPC 66):** positivo (I — ambos competentes), negativo (II — ambos incompetentes), ou de reuniao/separacao (III). O par. unico: o juiz que NAO acolher a competencia declinada deve ele proprio suscitar o conflito (salvo se atribuir a outro juizo).
3. **Checar legitimidade (CPC 951-952):** suscitam parte, MP ou juiz (951). NAO pode suscitar a parte que ja arguiu incompetencia relativa no processo (952) — armadilha que mata o incidente; conferir antes de redigir.
4. **Forma e instrucao (CPC 953):** pelo juiz por oficio; pela parte e pelo MP por peticao. Instruir com os documentos da prova do conflito (as duas decisoes divergentes). Dirigir ao tribunal competente.
5. **Medidas urgentes (CPC 955):** o relator pode, de oficio ou a requerimento, sobrestar o processo (no conflito positivo) e — positivo ou negativo — designar um dos juizes para resolver as medidas urgentes em carater provisorio; pedir essa designacao quando houver risco sem juizo definido. Julgamento de plano se a decisao se fundar em sumula ou tese de repetitivo/IAC (955 par. unico).
6. **Desfecho (CPC 957):** o tribunal declara o juizo competente e a validade dos atos do incompetente; antes, o MP e ouvido em 5 dias (956).

## Entrega obrigatoria final
- Peticao de suscitacao redigida ponta a ponta (especie do conflito + narrativa das duas decisoes + legitimidade do suscitante + regra de competencia + designacao para medidas urgentes se houver risco + declaracao do juizo competente) + copias das decisoes como instrucao + tribunal destinatario.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: escolha do foro/vara competente e foro de eleicao -> `competencia-e-foro`; recusa do proprio juiz por parcialidade -> `suspeicao-impedimento`.
