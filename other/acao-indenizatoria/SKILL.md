---
name: acao-indenizatoria
description: "Redige acao de reparacao de danos por responsabilidade civil — ato ilicito (CC 186) e abuso de direito (CC 187), dever de indenizar (CC 927) com responsabilidade objetiva pela atividade de risco (927 par. unico), extensao do dano e reducao equitativa (CC 944 + par. unico), perdas e danos / lucros cessantes / juros de mora (CC 402-405), danos por homicidio, lesao a saude e ofensa a honra (CC 948-954), distinguindo dano material x moral x estetico x lucros cessantes x perda de chance, pelo rito comum (CPC 319) com tutela se cabivel. Use quando o operador disser quero indenizacao, danos morais, fui lesado, acao indenizatoria, reparacao de danos."
---

# ACAO-INDENIZATORIA

> Camada 5 (acoes civeis). Acao condenatoria de reparacao por responsabilidade civil (subjetiva ou objetiva). Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cc-10406-02.md` — arts. 186-187 (ato ilicito / abuso de direito), 927 + par. unico (dever de indenizar / risco), 944 + par. unico (extensao do dano / reducao equitativa), 402-405 (perdas e danos / lucros cessantes / juros), 948-954 (homicidio, lesao, honra, liberdade) — **grep + ler a faixa**.
- `context/cpc-13105-15.md` — arts. 319 (requisitos da inicial), 324 (pedido), 300/311 (tutela) + `context/jurisprudencia-civel.md` (so vistoriados).

## Objetivo
Produzir inicial indenizatoria solida: nexo causal demonstrado, conduta (ilicita ou de risco) provada, danos discriminados por especie com fundamento e valor, sem risco de improcedencia por causa de pedir vaga ou pedido generico.

## Quando ativar
- Vitima quer reparacao por dano sofrido (material, moral, estetico, lucros cessantes, perda de chance).
- Caso de responsabilidade subjetiva (culpa) ou objetiva (atividade de risco / lei especial).

## Metodologia
1. **Gestao processual SEMPRE (Camada 2) antes de redigir:** `competencia-e-foro` (foro do dano / domicilio do reu) ; `valor-da-causa` (soma dos pedidos) ; `gratuidade-e-impugnacao` (se hipossuficiente) ; `tempestividade-civel`.
2. **Enquadrar a responsabilidade:** ato ilicito por acao/omissao, negligencia, imprudencia ou impericia (CC 186) ou abuso de direito (CC 187). Dever de reparar (CC 927); se atividade de risco ou hipotese legal, **objetiva** (927 par. unico) — dispensa prova de culpa.
3. **Demonstrar os 3 elementos:** conduta + nexo causal + dano. No regime objetivo, conduta + nexo + dano (sem culpa).
4. **Discriminar os danos por especie:** dano emergente (o que efetivamente perdeu) e lucros cessantes (o que razoavelmente deixou de lucrar) — CC 402-403; dano moral; dano estetico (cumulavel com o moral); perda de chance. Em lesao a saude, CC 949-950 (despesas + lucros cessantes + pensao se inabilitar). Em morte, CC 948 (despesas/funeral + alimentos). Em honra/liberdade, CC 953-954.
5. **Quantificar:** indenizacao mede-se pela extensao do dano (CC 944); apontar reducao equitativa (944 par. unico) e eventual culpa concorrente (CC 945) para antecipar a defesa. Juros de mora desde a citacao (CC 405) — em ilicito extracontratual, observar a data do evento (jurisprudencia, via `validador-civel`).
6. **Pedido (324):** certo e determinado por especie de dano; tutela de urgencia (CPC 300) ou evidencia (311) se cabivel.

## Entrega obrigatoria final
- Inicial redigida ponta a ponta (fatos + responsabilidade + nexo + danos discriminados por especie + quantificacao + juros + pedidos + valor + provas) + checklist de documentos + indicacao do foro/vara.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: liquidacao/cumprimento e execucao pesada -> `execucao-adv-os`; calculo de atualizacao/juros -> `calculosjudiciais-adv-os`; relacao de consumo (CDC), familia e sucessoes fora do escopo.
