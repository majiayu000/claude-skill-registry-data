---
name: contestacao-civel
description: "Redige a contestacao com TODA a defesa em peca unica (CPC 335-342): preliminares do art. 337 (via preliminares-civel) + impugnacao especifica dos fatos (341 — o fato nao impugnado presume-se verdadeiro) + merito (defesa direta/indireta, fatos impeditivos/modificativos/extintivos) + provas requeridas. Prazo 15 dias uteis (335). Reconvencao na mesma peca (343 — via reconvencao). Use quando o operador disser contestacao, contestar, fui citado, defesa, vou responder a acao, prazo de contestacao, ou descrever um caso na posicao de reu."
---

# CONTESTACAO-CIVEL

> Camada 4 (conhecimento/1o grau). Defesa concentrada do reu em peca unica. Gestao processual transversal obrigatoria.

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 335 (prazo), 336 (concentracao), 337 (preliminares), 341 (impugnacao especifica), 342 (excecoes), 343 (reconvencao) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so ✅).

## Objetivo
Apresentar defesa completa e tecnicamente fechada: toda preliminar cabivel, toda impugnacao de fato, todo argumento de merito e todas as provas — sem deixar fato sem impugnacao (efeito do 341).

## Quando ativar
- Reu foi citado e ha prazo de defesa.
- Necessidade de avaliar nulidades/defeitos da inicial e fundamentar o merito.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `tempestividade-civel` (prazo 15 dias uteis — termo inicial conforme 335: audiencia 334, protocolo de desistencia, ou juntada do AR/citacao) · `preliminares-civel` (rol do 337) · `competencia-e-foro` · `gratuidade-e-impugnacao` (impugnar gratuidade do autor se for o caso, no 337 XIII).
2. **Principio da concentracao (336):** toda a materia de defesa de uma so vez. O que nao for alegado precluira (salvo as do 342).
3. **Preliminares (337, I a XIII):** acionar `preliminares-civel` — ordenar antes do merito.
4. **Impugnacao especifica dos fatos (341):** manifestar-se ponto a ponto sobre cada alegacao de fato da inicial. **Fato nao impugnado presume-se verdadeiro**, salvo as excecoes do 341 (nao admissivel confissao, peticao desacompanhada de instrumento que a lei exija, em contradicao com a defesa). Defensor publico/dativo/curador/MP — impugnacao por negativa geral (341 par. unico).
5. **Merito:** defesa direta (nega o fato/consequencia) e indireta (fato impeditivo, modificativo ou extintivo do direito do autor — abre replica, 350).
6. **Provas:** especificar e requerer (documental ja instruida; testemunhal com rol; pericial; depoimento pessoal do autor) — cross-link `producao-de-provas`.
7. **Reconvencao (343):** se ha pretensao propria conexa — na mesma peca, via `reconvencao`.

## Entrega obrigatoria final
- Contestacao redigida (preliminares + impugnacao especifica item a item + merito + provas) + reconvencao se cabivel + rol de testemunhas + prazo confirmado.

## Guard
Nenhum dispositivo/sumula sem `validador-civel`. Nao deixar fato sem impugnacao (suprema-corte confere). Entrega pela `suprema-corte-civel`.
