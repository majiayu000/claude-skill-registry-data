---
name: competencia-e-foro
description: "Define a competencia e o foro corretos da acao civel (CPC 42-66) e trata o foro de eleicao apos a Lei 14.879/2024. Analisa competencia absoluta x relativa, foro do domicilio do reu, foros especiais, conexao/continencia, e a exigencia de pertinencia do foro de eleicao (juizo aleatorio = abuso, declinacao de oficio). Use quando o operador disser onde ajuizar, qual o foro, competencia, foro de eleicao, declinacao, conflito de competencia, incompetencia."
---

# COMPETENCIA-E-FORO

> Camada 2 (gestao processual transversal). Acionada ANTES de toda inicial e na defesa (preliminar de incompetencia).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — competencia (arts. 42-66), foro (46-53), foro de eleicao (63). **grep o artigo + ler a faixa.**
- `context/cpc-cc-alteracoes-recentes.md` — **Lei 14.879/2024** (nova redacao do art. 63 §1º + §5º).

## Objetivo
Indicar com seguranca o juizo competente (e o foro), antecipando incompetencia e conflito.

## Quando ativar
- Antes de ajuizar (escolha do foro/juizo).
- Na contestacao, para arguir incompetencia (preliminar, art. 337 II).
- Em conflito de competencia.

## Metodologia
1. **Competencia absoluta x relativa:** materia/funcao/pessoa (absoluta, de oficio) x territorio/valor (relativa, prorrogavel).
2. **Foro:** regra do domicilio do reu (46); foros especiais (47-53 — imovel, alimentos, reparacao de dano/ato ilicito, consumidor quando aplicavel etc.).
3. **Foro de eleicao (63 + Lei 14.879/2024):** so vale com **pertinencia** (domicilio/residencia de uma parte ou local da obrigacao); ajuizamento em juizo aleatorio = abuso -> **declinacao de oficio** para o foro de domicilio do reu.
4. **Conexao/continencia** (55-57): reuniao de processos.
5. Concluir com o juizo competente + fundamento + alerta de risco de declinacao.

## Entrega obrigatoria final
- Juizo/foro competente + fundamento (artigos) + (se defesa) minuta da preliminar de incompetencia + alerta da Lei 14.879/2024.

## Guard
Confirmar a vigencia do art. 63 com a nova redacao (anexo de alteracoes). Citacao por `validador-civel`; foro correto e item de R1 da `suprema-corte-civel`.
