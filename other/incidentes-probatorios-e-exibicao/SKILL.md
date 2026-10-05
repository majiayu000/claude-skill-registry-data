---
name: incidentes-probatorios-e-exibicao
description: "Maneja exibicao de documento ou coisa — contra a PARTE (CPC 396-400: pedido 397, resposta em 5 dias 398, recusa nao admitida 399, presuncao de veracidade se recusa ilegitima 400) ou contra TERCEIRO (CPC 401-404: citacao em 15 dias, audiencia especial 402, deposito/apreensao 403, escusas 404) — e a arguicao de FALSIDADE documental (CPC 430-433: suscitada na contestacao/replica/15 dias da juntada 430, motivos e meios 431, exame pericial 432, coisa julgada se questao principal 433; onus da prova 429). Use quando o operador disser exibicao de documento, obrigar a apresentar documento, incidente de falsidade, documento falso nos autos, parte esconde documento, exibicao de coisa."
---

# INCIDENTES-PROBATORIOS-E-EXIBICAO

> Camada 8 (incidentes processuais). Dois incidentes da prova documental: forcar a exibicao do que a outra parte/terceiro retem e impugnar documento falso juntado aos autos. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — exibicao contra a PARTE: arts. 396 (ordem judicial), 397 (conteudo do pedido — redacao Lei 14.195/2021, admite categorias), 398 (resposta em 5 dias), 399 (recusa nao admitida), 400 (presuncao de veracidade + par. unico medidas indutivas). Contra TERCEIRO: arts. 401 (citacao em 15 dias), 402 (audiencia especial), 403 (deposito + apreensao), 404 (escusas I a VI). Falsidade: arts. 429 (onus da prova I-II), 430 (prazo/momento; incidental salvo pedido de principal), 431 (motivos e meios), 432 (pericia apos oitiva), 433 (coisa julgada se questao principal) — **grep + ler a faixa**.

## Objetivo
Trazer aos autos a prova retida (exibicao) ou neutralizar prova falsa (falsidade), com o incidente, o prazo e a sancao certos — presuncao de veracidade na exibicao, pericia e coisa julgada na falsidade.

## Quando ativar
- A parte contraria ou terceiro detem documento/coisa indispensavel e nao o junta.
- Foi juntado documento reputado falso ou de autenticidade impugnada.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `producao-de-provas` (pertinencia/necessidade do documento) e `tempestividade-civel` (a falsidade tem prazo proprio de 15 dias da juntada — CPC 430); `memoria-de-caso-civel`.
2. **Exibicao contra a PARTE (CPC 396-400):** pedido com os tres requisitos do art. 397 (descricao do documento/coisa ou categorias; finalidade com os fatos; circunstancias de que existe e esta em poder do adverso). Resposta em 5 dias (398). O juiz NAO admite a recusa nas hipoteses do art. 399 (obrigacao legal; mencao ao documento para constituir prova; documento comum). Sancao do 400: admite como verdadeiros os fatos a provar se nao exibe nem se manifesta (I) ou se a recusa e ilegitima (II); par. unico autoriza medidas indutivas/coercitivas/sub-rogatorias.
3. **Exibicao contra TERCEIRO (CPC 401-404):** citacao para responder em 15 dias (401). Se nega a obrigacao ou a posse, audiencia especial com depoimentos (402). Recusa sem justo motivo: deposito em 5 dias e, descumprido, mandado de apreensao com forca policial, multa e desobediencia (403). Conferir as escusas legitimas do art. 404 (familia, dever de honra, desonra/perigo penal, segredo profissional, motivos graves, disposicao legal).
4. **Arguicao de FALSIDADE (CPC 430-432):** suscitar na contestacao, na replica ou em 15 dias da intimacao da juntada (430). Resolve-se como questao incidental, salvo pedido para decidir como principal (430 par. unico). Expor os motivos e os meios de prova (431). Apos oitiva da outra parte em 15 dias, realiza-se o exame pericial (432); dispensada se quem produziu concordar em retirar o documento (432 par. unico).
5. **Onus da prova (CPC 429):** incumbe a quem argui a falsidade ou o preenchimento abusivo (I); incumbe a quem produziu, se impugnada a autenticidade (II) — alocar corretamente na peca.
6. **Efeito da decisao (CPC 433):** se suscitada como questao principal, a falsidade consta da parte dispositiva e faz coisa julgada — definir desde o inicio entre incidental (sem coisa julgada) e principal (com coisa julgada).

## Entrega obrigatoria final
- Peca redigida ponta a ponta conforme o incidente (exibicao com os requisitos do 397 e a sancao do 400, ou contra terceiro com citacao e apreensao; ou falsidade com motivos, meios, pericia e opcao incidental x principal) + alocacao do onus (CPC 429) + prazo aplicavel.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: producao antecipada autonoma de prova -> `producao-antecipada-de-provas`; saneamento e organizacao da instrucao -> `saneamento`.
