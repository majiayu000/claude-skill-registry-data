---
name: estilo-civel
description: "Define o estilo juridico das pecas civeis do plugin — peticoes iniciais, contestacoes, replicas, recursos, manifestacoes, razoes. Use sempre que outra skill for redigir um texto civel, para garantir tom, estrutura, enderecamento e terminologia processual corretos. Acionada internamente pelas skills de redacao."
---

# ESTILO-CIVEL

> Tier 0. Camada de estilo. Consultada pelas skills de redacao antes de entregar a peca.

## Anexos obrigatorios (context/)
- `context/metodologia-civel.md` (terminologia e regras de ouro).

## Terminologia correta (nao confundir)
- **Tutela de urgencia** (antecipada/cautelar, art. 300) ≠ **tutela de evidencia** (art. 311, dispensa perigo).
- **Decisao interlocutoria** (agravo de instrumento) ≠ **sentenca** (apelacao) ≠ **decisao monocratica** (agravo interno).
- **Preliminar** (art. 337, sem resolucao de merito) ≠ **prejudicial de merito** (prescricao/decadencia).
- **Reconvencao** (pedido proprio do reu na mesma peca, art. 343) ≠ pedido contraposto.
- **Valor da causa** sempre indicado; **gratuidade** requerida quando cabivel.

## Estrutura padrao por tipo
- **Peticao inicial (CPC 319):** enderecamento ao juizo competente + qualificacao das partes + fatos + fundamentos juridicos + pedido (especifico, com tutela se cabivel) + valor da causa + provas + requerimentos.
- **Contestacao (CPC 335-342):** preliminares (337) + impugnacao especifica dos fatos (341) + merito + reconvencao se cabivel + provas.
- **Recurso:** enderecamento ao orgao correto + tempestividade + preparo + razoes (error in judicando/in procedendo) + pedido.
- **Manifestacao/replica:** objetiva, ponto a ponto.

## Tom
Tecnico, objetivo, assertivo. Sem promessa de resultado (Codigo de Etica OAB). Citacoes so via `validador-civel`.

## Guard
Toda citacao legal/jurisprudencial passa por `validador-civel`. Antes de entregar, `suprema-corte-civel` (R4 cuida da forma/pedidos/tempestividade/valor/gratuidade).
