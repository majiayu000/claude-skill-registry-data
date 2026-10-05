---
name: apelacao-civel
description: "Redige apelacao do CPC 1.009-1.014 contra sentenca (terminativa 485 ou definitiva 487), no prazo de 15 dias uteis, com preparo sob pena de desercao (1.007), efeito suspensivo como regra (1.012, excecoes do §1), efeito devolutivo e causa madura (1.013 §3) e majoracao de honorarios recursais (85 §11). Use quando o operador disser apelar, apelacao, recorrer da sentenca, sentenca improcedente, error in judicando, efeito suspensivo da apelacao, causa madura."
---

# APELACAO-CIVEL — CPC 1.009-1.014

> Camada 6 (recursos). Recurso por excelencia contra a sentenca. Preparo no ato sob pena de desercao.

## Anexos obrigatorios (context/)
- `context/recursos-tutelas-civel.md` (§2.4 apelacao + §0 preparo/desercao 1.007).
- `context/cpc-13105-15.md` (arts. 1.009-1.014 + 85 §11 + 1.007; **grep + faixa**).
- `context/jurisprudencia-civel.md` (honorarios recursais 85 §11 — tese STJ ✅).

## Objetivo
Reformar ou anular a sentenca com razoes que ataquem cada capitulo/fundamento, tempestiva, preparada e com pedido de efeito adequado.

## Quando ativar
- Houve **sentenca** (485 terminativa ou 487 definitiva) e a parte quer recorrer.
- Gatilhos: "apelar", "apelacao", "recorrer da sentenca", "improcedente", "error in procedendo/in judicando", "efeito suspensivo", "causa madura".

## Metodologia
1. **Cabimento (1.009 — grep):** da **sentenca**. Questoes interlocutorias **nao agravaveis** nao precluem e vao em **preliminar de apelacao ou contrarrazoes** (§1) — levantar as que cabem.
2. **Tempestividade:** **15 dias uteis** (1.003 §5), dobro por sujeito (Fazenda 30 etc.). Cruzar com `tempestividade-civel`.
3. **Preparo (1.007):** comprovar **preparo + porte** no ato da interposicao, **sob pena de desercao**. Insuficiencia -> 5 dias para suprir (§2); ausencia -> recolher em **dobro** (§4). Isentos no §1. Calcular com `valor-da-causa`.
4. **Forma (1.010):** peticao de interposicao ao **juizo de 1o grau** + razoes; apelado intimado para contrarrazoes (15 dias). **Remessa ao tribunal independe de juizo de admissibilidade na origem** (§3).
5. **Error in procedendo x in judicando:** estruturar preliminares de nulidade (procedendo) e o merito recursal (judicando), atacando cada fundamento da sentenca.
6. **Efeito suspensivo (1.012):** **regra geral**. **Excecoes do §1 (efeito imediato):** homologacao de divisao/demarcacao; condenacao a **alimentos**; extincao/improcedencia de embargos do executado; instituicao de arbitragem; tutela provisoria confirmada/concedida/revogada; interdicao. Nestes casos, pedir efeito suspensivo ao relator (§4: probabilidade de provimento ou fundamentacao relevante + risco de dano).
7. **Efeito devolutivo + causa madura (1.013 §3):** o tribunal julga **desde logo o merito** se reformar sentenca 485, decretar nulidade, suprir omissao de pedido — requerer expressamente quando favoravel.
8. **Honorarios recursais (85 §11):** o tribunal **majora** os honorarios pelo trabalho em grau recursal, dentro dos limites dos §§2-3. **Tese STJ ✅:** a majoracao exige (a) condenacao anterior em honorarios na decisao recorrida E (b) recurso integralmente desprovido/nao conhecido — antecipar isso nas contrarrazoes/defesa.

## Entrega obrigatoria final
- Peticao de interposicao + razoes redigidas combatendo cada fundamento da sentenca (preliminares + merito) + pedido de efeito (suspensivo ou suspensivo ope iudicis nas hipoteses do §1).
- Comprovacao de preparo calculada + parecer de tempestividade + nota sobre causa madura e honorarios recursais.

## Guard
Sumula/tese (85 §11) so via `validador-civel` (✅ ja conferida). Preparo ausente/insuficiente = risco de desercao — calcular e avisar. Entrega final pela `suprema-corte-civel`.
