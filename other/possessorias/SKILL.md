---
name: possessorias
description: "Redige acoes possessorias pelo procedimento especial (CPC 554-568): manutencao de posse (turbacao), reintegracao de posse (esbulho) e interdito proibitorio (ameaca/CPC 567-568), com fungibilidade (554), cumulacao com perdas e danos (555), forca NOVA (dentro de ano e dia -> liminar 562) x forca VELHA (rito comum 558 par. unico), fundada na posse (CC 1.196-1.210) e na posse justa (CC 1.200). Use quando o operador disser reintegracao de posse, manutencao de posse, interdito proibitorio, esbulho, turbacao, fui despejado da posse, ou invasao de imovel."
---

# POSSESSORIAS

> Camada 5 (acoes civeis). Procedimento especial possessorio fundado na POSSE (nao no dominio). Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 554 (fungibilidade), 555 (cumulacao perdas/danos), 556 (defesa = pedido possessorio), 557 (vedacao alegar dominio), 558 (forca nova x velha) + par. unico, 560-562 (manutencao/reintegracao, prova, liminar), 567-568 (interdito proibitorio) — **grep + ler a faixa**.
- `context/cc-10406-02.md` — arts. 1.196 (conceito de posse), 1.200 (posse justa: nao violenta/clandestina/precaria), 1.210 (mantido na turbacao, restituido no esbulho, segurado da violencia iminente), 1.224 (perda da posse) + `context/jurisprudencia-civel.md` (so ✅).

## Objetivo
Inicial possessoria que prova a posse anterior, o vicio (turbacao/esbulho/ameaca) e a data, garantindo a tutela liminar quando forca nova, sem cair no rito comum por perda do prazo de ano e dia.

## Quando ativar
- Possuidor sofreu turbacao (manutencao), esbulho (reintegracao) ou ameaca iminente (interdito proibitorio).

## Metodologia
1. **Gestao processual SEMPRE (Camada 2) antes de redigir:** `competencia-e-foro` · `valor-da-causa` · `gratuidade-e-impugnacao` · `tempestividade-civel`.
2. **Classificar a lesao a posse (CC 1.210):** turbacao -> manutencao; esbulho -> reintegracao; ameaca/justo receio -> interdito proibitorio (CPC 567).
3. **Forca nova x velha (CPC 558):** dentro de ano e dia do esbulho/turbacao -> procedimento especial com liminar (CPC 562); apos ano e dia -> rito comum (558 par. unico), sem perder o carater possessorio.
4. **Provar os requisitos (CPC 561):** a posse; a turbacao/esbulho do reu; a data; a continuacao (manutencao) ou a perda (reintegracao) da posse.
5. **Fungibilidade (CPC 554) + cumulacao (CPC 555):** pedir perdas/danos e medida contra nova turbacao/esbulho. Lembrar vedacao de discutir dominio na pendencia (CPC 557).
6. **Liminar (CPC 562):** inicial instruida -> mandado sem ouvir o reu; senao, justificacao previa. PJ de direito publico exige previa audiencia (562 par. unico).

## Entrega obrigatoria final
- Inicial redigida ponta a ponta (posse + vicio + data + forca nova/velha + liminar + cumulacao + pedidos + valor + provas) + checklist de documentos + indicacao do foro/vara.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: acao fundada no titulo/dominio -> `reivindicatoria-petitoria`; usucapiao -> `usucapiao-judicial`; execucao/cumprimento pesado -> `execucao-adv-os`.
