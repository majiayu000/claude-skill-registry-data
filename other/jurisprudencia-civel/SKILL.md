---
name: jurisprudencia-civel
description: "Busca de precedente civel para fundamentar peca, recurso ou parecer: primeiro no corpus mapeado em context/jurisprudencia-civel.md (organizado por tema com selo de verificacao), e so se faltar busca ao vivo (WebSearch/WebFetch nativo; Firecrawl/Perplexity fallback) exigindo link de fonte real (STJ/STF/CJF/tribunal). Zero acordao inventado. Use quando precisar de sumula, tema repetitivo, enunciado de Jornada, acordao ou tese civel, ou quando o operador disser tem jurisprudencia sobre X, qual a sumula/tema sobre Y, precedente para a tese, acha um acordao do STJ sobre, fundamenta com jurisprudencia."
---

# JURISPRUDENCIA-CIVEL — Busca de precedente civel verificado

> Camada 1 (Fundacao). Entrega precedente cujo existir e teor foram confirmados. Trabalha colada ao `validador-civel` e ao guard global `anti-alucinacao-juridica`.

## Anexos obrigatorios (context/)
- `context/jurisprudencia-civel.md` — corpus mapeado por tema, com selo de verificacao: **✅** (fonte primaria oficial confirmada — citar) · **🟡** (fonte secundaria confiavel — conferir inteiro teor antes de citar) · **❌/NAO CONFIRMADO** (nunca citar).
- `context/cpc-cc-alteracoes-recentes.md` — para nao citar tese contra reforma vigente.
- `context/metodologia-civel.md` — quando chamada pelo `civel-master`.

## Objetivo
Devolver precedente civel **real, pertinente e citavel**, com fonte verificavel, ou declarar honestamente que nao foi encontrado — nunca preencher a lacuna com acordao/sumula/tema inventado.

## Quando ativar
- Uma skill de peca/recurso/parecer precisa de respaldo jurisprudencial.
- O operador pede sumula, tema, enunciado, leading case ou tese sobre um ponto civel.
- Ha duvida se um precedente existe, esta vigente ou se aplica ao caso.

## Metodologia
1. **Corpus primeiro.** Buscar no anexo por tema (os blocos sao `## TEMA N`):
   `grep -niE "tutela|gratuidade|tempestividade|responsabilidade|recurso|repetitivo" context/jurisprudencia-civel.md` e ler a faixa.
   - **✅** → pode citar (use a fonte ja registrada no anexo).
   - **🟡** → so apos conferir o inteiro teor na fonte oficial (fazer a busca ao vivo do passo 2 e confirmar a tese antes de citar).
   - **❌ / NAO CONFIRMADO / divergencia** → nao citar; se houver racha (ex.: estabilizacao da tutela art. 304, 3ª x 1ª Turma), **avisar a divergencia** e adotar a postura honesta registrada no anexo.
2. **Busca ao vivo (so se faltar no corpus ou se 🟡):** `WebSearch`/`WebFetch` nativos primeiro; **Firecrawl/Perplexity como fallback**. Priorizar fonte oficial: stj.jus.br, portal.stf.jus.br, cjf.jus.br (Jornadas), tribunal de origem. Exigir **link real** e abrir a pagina para confirmar que a tese/ementa esta la.
3. **Validar antes de devolver:** acionar `validador-civel` — orgao + numero + tese + data conferem e a fonte abre com o trecho? Sem isso, marcar como NAO VERIFICADO e nao usar em peca.
4. **Pertinencia e vinculacao:** checar se o precedente se aplica ao caso (distinguishing) e se e vinculante (CPC 927 — repetitivo, RG, sumula vinculante, IRDR/IAC).

## Entrega obrigatoria final
- Tabela: orgao/numero · tese (1-2 linhas) · selo (✅ corpus / ✅ ao vivo verificado) · link da fonte · pertinencia ao caso · vinculacao (CPC 927?). Bloco de citacao pronto so para itens verificados. Itens nao confirmados ficam de fora, listados como "nao localizado".

## Guard
Zero acordao/sumula/tema/enunciado inventado. So entra em peca o que e **✅** no corpus ou foi **confirmado ao vivo com link real aberto**. 🟡 sem conferencia e ❌ NUNCA. Integra `validador-civel` + guard global `anti-alucinacao-juridica`; gate final `suprema-corte-civel` (R3). Na duvida, remover e checar.
