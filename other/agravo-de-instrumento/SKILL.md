---
name: agravo-de-instrumento
description: "Redige agravo de instrumento do CPC 1.015-1.020 contra decisao interlocutoria — rol do 1.015 (I a XI e XIII; o XII foi vetado) + taxatividade mitigada (Tema 988/STJ), pecas obrigatorias do 1.017, comunicacao ao juizo de 1a (1.018), efeito suspensivo / antecipacao da tutela recursal (1.019 I), prazo 15 dias uteis. Use quando o operador disser agravo de instrumento, agravar a interlocutoria, recorrer da liminar, decisao interlocutoria, efeito suspensivo no agravo, Tema 988."
---

# AGRAVO-DE-INSTRUMENTO — CPC 1.015-1.020

> Camada 6 (recursos). Recurso contra interlocutoria. Falha em peca obrigatoria ou foro errado = nao conhecimento.

## Anexos obrigatorios (context/)
- `context/recursos-tutelas-civel.md` (§2.2 AI + §3 Tema 988).
- `context/cpc-13105-15.md` (arts. 1.015-1.020; **grep + faixa**).
- `context/jurisprudencia-civel.md` (Tema 988/STJ ✅ — taxatividade mitigada).

## Objetivo
Atacar a interlocutoria cabivel com instrumento completo, no prazo, com pedido de efeito suspensivo/tutela recursal bem fundamentado.

## Quando ativar
- Decisao interlocutoria do **rol do 1.015** (ou liquidacao/cumprimento/execucao/inventario — par. unico).
- Interlocutoria fora do rol com **urgencia/inutilidade do julgamento na apelacao** (Tema 988).
- Gatilhos: "agravo de instrumento", "agravar", "recorrer da liminar/interlocutoria", "efeito suspensivo", "Tema 988".

## Metodologia
1. **Cabimento (1.015 — grep):** conferir se a materia esta no rol (I tutelas; II merito; III arbitragem; IV IDPJ; V gratuidade; VI exibicao; VII exclusao de litisconsorte; VIII limitacao do litisconsorcio; IX intervencao de terceiros; X efeito suspensivo a embargos a execucao; XI redistribuicao do onus da prova; XIII outros em lei) + par. unico (liquidacao/cumprimento/execucao/inventario).
2. **Fora do rol — Tema 988/STJ ✅:** taxatividade **mitigada** — cabe AI se demonstrada **urgencia decorrente da inutilidade do julgamento da questao na apelacao**. Sem isso, a interlocutoria nao-agravavel vai em **preliminar de apelacao ou contrarrazoes** (1.009 §1) — registrar essa ressalva.
3. **Tempestividade:** **15 dias uteis** (1.003 §5), dobro por sujeito. Cruzar com `tempestividade-civel`.
4. **Pecas obrigatorias (1.017, I — grep):** inicial, contestacao, peticao que ensejou a decisao, **decisao agravada**, certidao de intimacao (ou prova de tempestividade) e **procuracoes**. **§5: dispensadas em autos eletronicos.** Falta de peca -> relator intima para sanar (932 par. unico).
5. **Comunicacao ao juizo de 1a (1.018):** em **autos fisicos** e **obrigatorio juntar copia do agravo na origem em 3 dias** (§2); descumprimento arguido e provado -> inadmissibilidade (§3). Em autos eletronicos, dispensado.
6. **Pedido de efeito suspensivo / tutela recursal (1.019, I):** fundamentar **probabilidade de provimento + risco de dano** — o relator decide em 5 dias.
7. **Preparo:** custas + porte quando devidos (1.017 §1). Conferir com `valor-da-causa`.
8. Redigir: enderecamento ao **tribunal** + razoes (reforma/invalidacao) + pedido de efeito suspensivo + nomes/enderecos dos advogados (1.016).

## Entrega obrigatoria final
- Agravo redigido + **lista das pecas obrigatorias do 1.017** (ou nota de dispensa em autos eletronicos) + minuta da comunicacao do 1.018 se autos fisicos.
- Parecer de tempestividade + cabimento (rol ou Tema 988) + pedido de efeito suspensivo fundamentado.

## Guard
Tema 988 e demais teses so via `validador-civel` (Tema 988 ✅ ja conferido). Fora do rol sem urgencia/inutilidade demonstrada = risco de nao conhecimento — avisar e oferecer a via da preliminar de apelacao. Entrega final pela `suprema-corte-civel`.
