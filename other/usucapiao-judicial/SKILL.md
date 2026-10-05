---
name: usucapiao-judicial
description: "Redige acao de usucapiao pela modalidade adequada: extraordinaria (CC 1.238 — 15 anos sem titulo/boa-fe; 10 anos com posse-trabalho/moradia no par. unico), especial rural (CC 1.239 — 5 anos), especial urbana (CC 1.240 — 5 anos / ate 250m2) e familiar (CC 1.240-A — 2 anos / abandono do lar), ordinaria (CC 1.242 — 10 anos com justo titulo e boa-fe; 5 anos se aquisicao onerosa com registro cancelado), com citacao por edital na usucapiao (CPC 259, I) e intimacao de confrontantes, Fazendas e MP. Use quando o operador disser usucapiao, usucapir imovel, posse prolongada vira propriedade, adquirir por usucapiao, ou acao de usucapiao."
---

# USUCAPIAO-JUDICIAL

> Camada 5 (acoes civeis). Acao declaratoria de aquisicao originaria da propriedade pela posse qualificada. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cc-10406-02.md` — arts. 1.238 (extraordinaria 15 anos / 10 com posse-trabalho no par. unico), 1.239 (especial rural), 1.240 (especial urbana ate 250m2) + 1.240-A (familiar 2 anos), 1.242 (ordinaria 10 anos com justo titulo e boa-fe / 5 anos par. unico) — **grep + ler a faixa**.
- `context/cpc-13105-15.md` — art. 259, I (edital na acao de usucapiao de imovel); requisitos da inicial (319) + `context/jurisprudencia-civel.md` (so ✅). Especial urbana (CF 183) e rural (CF 191): confirmar via `validador-civel` antes de citar numero.

## Objetivo
Inicial de usucapiao que enquadra corretamente a modalidade e o prazo, comprova a posse ad usucapionem (mansa, pacifica, ininterrupta, com animo de dono) e assegura a citacao ampla, sem risco de improcedencia por modalidade/prazo errados.

## Quando ativar
- Possuidor com posse prolongada pretende declaracao judicial da propriedade.
- Inviavel a via extrajudicial (sem consenso dos confrontantes ou documentacao incompleta).

## Metodologia
1. **Gestao processual SEMPRE (Camada 2) antes de redigir:** `competencia-e-foro` (foro da situacao do imovel) · `valor-da-causa` · `gratuidade-e-impugnacao` · `tempestividade-civel`.
2. **Escolher a modalidade pelo prazo e pelos requisitos:** extraordinaria (CC 1.238 — 15 anos; 10 com moradia/obras produtivas, par. unico); ordinaria (CC 1.242 — 10 anos com justo titulo e boa-fe; 5 anos se aquisicao onerosa com registro depois cancelado, par. unico); especial rural (CC 1.239); especial urbana / familiar (CC 1.240 e 1.240-A).
3. **Provar a posse ad usucapionem:** continua, sem oposicao, com animo de dono, pelo prazo da modalidade; instruir com planta, memorial e prova testemunhal.
4. **Citacao e intimacoes amplas:** edital na usucapiao de imovel (CPC 259, I); citacao dos confrontantes e do titular do registro; intimacao das Fazendas (Uniao/Estado/Municipio) e do Ministerio Publico.
5. **Pedido:** declaracao da propriedade por sentenca, que servira de titulo para registro no CRI.

## Entrega obrigatoria final
- Inicial redigida ponta a ponta (modalidade + posse qualificada + prazo + planta/memorial + citacao edital/confrontantes + Fazendas/MP + pedido declaratorio) + checklist de documentos + indicacao do foro/vara.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: se ha consenso e documentos completos -> via EXTRAJUDICIAL no cartorio (Lei 6.015 art. 216-A) — mencionar, sem duplicar; defesa de posse -> `possessorias`; reivindicacao pelo dominio -> `reivindicatoria-petitoria`.
