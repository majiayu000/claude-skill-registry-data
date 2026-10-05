---
name: emenda-inicial
description: "Trata a fase de controle da inicial: emenda apos despacho do juiz (CPC 321 — prazo de 15 dias para sanar vicio ou completar requisitos do 319/320), o indeferimento da inicial (330) e a improcedencia liminar do pedido (332). Distingue o que e corrigivel do que e causa de extincao. Use quando o operador disser despacho de emenda, emendar a inicial, juiz mandou corrigir, indeferiu a inicial, improcedencia liminar, ou recebeu intimacao para sanar vicio da peticao inicial."
---

# EMENDA-INICIAL

> Camada 4 (conhecimento/1o grau). Resposta ao controle judicial da inicial. Cross-check com `tempestividade-civel` (prazo da emenda).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — art. 321 (emenda, 15 dias), 319/320 (requisitos a sanar), 330 (indeferimento), 332 (improcedencia liminar) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so ✅, p/ improcedencia liminar contra precedente).

## Objetivo
Sanar o vicio apontado e salvar a inicial; ou, se for caso de indeferimento (330)/improcedencia liminar (332), preparar a resposta correta (recurso/apelacao — cross-link recursos).

## Quando ativar
- Juiz determinou emenda (321) e ha prazo correndo.
- Inicial foi indeferida (330) ou houve improcedencia liminar (332) — analisar recurso.

## Metodologia
1. **Ler o despacho:** identificar o vicio apontado (requisito do 319/320 ausente, pedido indeterminado, valor incorreto, defeito que impeca julgamento).
2. **Prazo:** emenda em **15 dias** (321) — confirmar contagem via `tempestividade-civel`. Nao emendar no prazo -> indeferimento (321 par. unico + 330).
3. **Emendar:** corrigir/completar exatamente o apontado (e so o apontado, salvo conexao logica), reapresentando a inicial saneada. Cross-link `valor-da-causa`/`competencia-e-foro` se o vicio for desses.
4. **Indeferimento (330):** hipoteses (inepcia §1o, ilegitimidade, falta de interesse, nao atendida a emenda). Cabe **apelacao** (cross-link recursos) — juiz pode retratar-se.
5. **Improcedencia liminar (332):** so quando o pedido contraria sumula STF/STJ, repetitivo, IRDR/IAC ou sumula de TJ, ou ha prescricao/decadencia. Validar o precedente invocado (real e vigente) antes de aceitar; cabe **apelacao**.

## Entrega obrigatoria final
- Peticao de emenda saneando o vicio (ou parecer: cabe recurso) + prazo confirmado + checklist do que foi corrigido.

## Guard
Precedente invocado em improcedencia liminar so com `validador-civel`. Nao extrapolar a correcao. Entrega pela `suprema-corte-civel`.
