---
name: acao-rescisoria
description: "Redige acao rescisoria - acao autonoma de impugnacao para desconstituir coisa julgada (CPC 966 hipoteses I a VIII; 967 legitimidade; 968 requisitos + deposito de 5% no inciso II; 969 nao suspende o cumprimento em regra; 975 prazo decadencial de 2 anos do transito em julgado). Competencia originaria do tribunal. Use quando o operador disser acao rescisoria, rescindir sentenca transitada, desconstituir coisa julgada, violacao de norma na sentenca, ou prova nova depois do transito."
---

# ACAO-RESCISORIA

> Camada 5 (acoes civeis). Acao autonoma de impugnacao da coisa julgada, de competencia originaria do tribunal. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 966 (hipoteses I a VIII), 967 (legitimidade), 968 (requisitos + deposito 5%), 969 (nao impede o cumprimento, ressalvada tutela provisoria), 975 (prazo decadencial 2 anos) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so vistoriados).

## Objetivo
Desconstituir decisao de merito transitada em julgado dentro de uma das hipoteses taxativas do CPC 966, observado o deposito previo e o prazo decadencial, perante o tribunal competente.

## Quando ativar
- Existe decisao de merito transitada em julgado e ha fundamento rescisorio do CPC 966.
- Surgiu prova nova apos o transito (966, VII) ou houve violacao manifesta de norma juridica (966, V).

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `competencia-e-foro` (competencia ORIGINARIA do tribunal) · `valor-da-causa` · `gratuidade-e-impugnacao` (dispensa o deposito — 968 §1o).
2. **Hipotese rescisoria (CPC 966, I a VIII):** enquadrar o caso — I prevaricacao, concussao ou corrupcao do juiz; II juiz impedido ou juizo absolutamente incompetente; III dolo/coacao da parte vencedora, simulacao ou colusao; IV ofensa a coisa julgada; V violacao manifesta de norma juridica; VI prova falsa; VII prova nova ignorada ou de que nao pode fazer uso; VIII erro de fato verificavel dos autos.
3. **Legitimidade (967):** parte/sucessor, terceiro juridicamente interessado, Ministerio Publico, ou quem nao foi ouvido onde sua intervencao era obrigatoria.
4. **Requisitos (968):** observar o art. 319 (inicial); cumular ao pedido de rescisao, se for o caso, o de novo julgamento (iudicium rescindens + rescissorium); **depositar 5% sobre o valor da causa** (968, II), salvo as isencoes do §1o.
5. **Cumprimento (969):** a propositura NAO impede o cumprimento da decisao rescindenda — para suspender, pleitear tutela provisoria.
6. **Prazo (975):** confirmar que NAO se passaram os 2 anos contados do transito em julgado da ultima decisao do processo (prazo DECADENCIAL — fatal).

## Entrega obrigatoria final
- Inicial rescisoria ponta a ponta (cabeca + hipotese do 966 enquadrada + iudicium rescindens/rescissorium + valor + comprovante de deposito 5% ou pedido de dispensa) + analise do prazo do 975 + tribunal competente.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria. Entrega pela `suprema-corte-civel`. Cross-link, nao duplicar: recursos ordinarios -> camada de recursos; execucao da decisao rescindida -> `execucao-adv-os`.
