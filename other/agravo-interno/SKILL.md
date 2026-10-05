---
name: agravo-interno
description: "Redige agravo interno do CPC 1.021 contra decisao MONOCRATICA do relator em tribunal, levando a materia ao colegiado, no prazo de 15 dias uteis, com impugnacao especifica dos fundamentos (1.021 §1) e alerta sobre a multa de 1-5 por cento (1.021 §4). Use quando o operador disser agravo interno, recorrer da decisao monocratica, decisao do relator, levar ao colegiado, agravo regimental."
---

# AGRAVO-INTERNO — CPC 1.021

> Camada 6 (recursos). Devolve ao colegiado a decisao que o relator tomou sozinho. Impugnacao generica = inadmissibilidade + risco de multa.

## Anexos obrigatorios (context/)
- `context/recursos-tutelas-civel.md` (§2.3 agravo interno).
- `context/cpc-13105-15.md` (art. 1.021; **grep + faixa**).
- `context/jurisprudencia-civel.md` (se houver tese pertinente ao caso).

## Objetivo
Levar ao colegiado a decisao monocratica do relator, atacando especificamente cada fundamento, sem incorrer na multa do §4.

## Quando ativar
- O relator decidiu **monocraticamente** (negou seguimento, deu/negou provimento, inadmitiu) e o RI permite o agravo interno.
- Tambem cabe contra a decisao do presidente/vice nos incisos I e III do 1.030 (juizo de admissibilidade — ver `agravo-em-recurso-excepcional`).
- Gatilhos: "agravo interno", "decisao monocratica", "decisao do relator", "levar ao colegiado", "agravo regimental".

## Metodologia
1. **Cabimento (1.021 — grep):** decisao **monocratica do relator** -> agravo ao orgao colegiado, conforme o **regimento interno** do tribunal. Confirmar que nao e caso de outro recurso (ED, agravo do 1.042).
2. **Tempestividade:** **15 dias uteis** (1.003 §5), dobro por sujeito. Cruzar com `tempestividade-civel`.
3. **Impugnacao especifica (1.021 §1):** o agravo **deve impugnar especificamente** os fundamentos da decisao agravada — peticao que apenas repete a inicial/recurso e inadmitida. Enfrentar cada fundamento do relator, ponto a ponto.
4. **Retratacao (1.021 §2):** o relator intima o agravado (15 dias) e, **nao havendo retratacao**, leva a julgamento. O §3 veda ao relator limitar-se a reproduzir a decisao agravada.
5. **Multa (1.021 §4 + §5):** se o agravo for declarado **manifestamente inadmissivel ou improcedente em votacao unanime**, multa de **1% a 5%** do valor atualizado da causa; novo recurso fica condicionado ao **deposito previo** da multa (salvo Fazenda e beneficiario da gratuidade — pagam ao final). Avaliar o risco antes de agravar.
6. **Preparo:** conforme o RI do tribunal. Conferir com `valor-da-causa`.
7. Redigir: enderecamento ao **orgao colegiado** competente (via relator) + impugnacao especifica + pedido de provimento.

## Entrega obrigatoria final
- Agravo interno redigido com impugnacao especifica de cada fundamento da decisao monocratica.
- Parecer de tempestividade + alerta sobre a multa do §4 (votacao unanime) e o deposito previo do §5.

## Guard
Tese/sumula so via `validador-civel`. Impugnacao generica = risco real de multa — exigir enfrentamento ponto a ponto. Entrega final pela `suprema-corte-civel`.
