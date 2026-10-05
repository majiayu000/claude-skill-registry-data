---
name: embargos-de-terceiro
description: "Redige embargos de terceiro (CPC 674-681) para quem, nao sendo parte, sofre constricao ou ameaca de constricao sobre bem que possui ou sobre o qual tem direito incompativel (674; proprietario/possuidor/fiduciario no par. 1; equiparados no par. 2), no prazo do CPC 675 (ate 5 dias depois da adjudicacao/alienacao/arrematacao e antes da assinatura da carta; a qualquer tempo no conhecimento enquanto nao transitada), distribuidos por dependencia (676), com prova sumaria de posse/dominio (677) e liminar de suspensao/manutencao/reintegracao mediante caucao (678 par. unico), ate o cancelamento da constricao (681). Use quando o operador disser embargos de terceiro, penhoraram bem que nao e do devedor, meu bem foi constrito em processo alheio, ou defender bem de penhora indevida."
---

# EMBARGOS-DE-TERCEIRO

> Camada 5 (acoes civeis) — defesa de quem NAO e parte contra constricao judicial sobre bem proprio. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 674 (terceiro que sofre constricao/ameaca; par. 1 proprietario/possuidor/fiduciario; par. 2 equiparados a terceiro), 675 (prazo), 676 (distribuicao por dependencia ao juizo da constricao), 677 (inicial com prova sumaria de posse/dominio + rol), 678 (suspensao das constricoes + manutencao/reintegracao provisoria; par. unico caucao), 681 (cancelamento da constricao indevida) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` — confirmar eventual Sumula 134 STJ **so se constar ✅**; nao citar se ausente.

## Objetivo
Embargos que comprovam a qualidade de terceiro e a titularidade (posse/dominio) do bem constrito, obtendo a liminar de suspensao da constricao dentro do prazo do CPC 675, sem perder a janela antes da assinatura da carta.

## Quando ativar
- Bem de terceiro foi penhorado/constrito (ou ameacado) em processo do qual ele nao e parte.
- Equiparado a terceiro (CPC 674 par. 2) precisa defender o bem.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2) antes de redigir:** `competencia-e-foro` (distribuicao por dependencia — CPC 676) · `valor-da-causa` · `gratuidade-e-impugnacao` · `tempestividade-civel`.
2. **Verificar o prazo (CPC 675):** no conhecimento, a qualquer tempo enquanto nao transitada; no cumprimento/execucao, ate 5 dias depois da adjudicacao/alienacao/arrematacao e SEMPRE antes da assinatura da carta. Prazo critico — calcular primeiro.
3. **Demonstrar a qualidade de terceiro (CPC 674):** nao ser parte e ter posse ou direito incompativel com o ato constritivo (par. 1: proprietario, possuidor, fiduciario; par. 2: equiparados).
4. **Prova sumaria (CPC 677):** instruir a inicial com documentos de posse/dominio e rol de testemunhas.
5. **Liminar (CPC 678):** requerer a suspensao das constricoes e a manutencao/reintegracao provisoria; o juiz pode exigir caucao (par. unico), ressalvada a hipossuficiencia economica.
6. **Pedido:** desfazimento/inibicao da constricao e seu cancelamento (CPC 681), com reconhecimento do dominio/posse.

## Entrega obrigatoria final
- Inicial redigida ponta a ponta (qualidade de terceiro + prova de posse/dominio + prazo 675 + liminar 678 + caucao + pedido de cancelamento 681) + checklist de documentos + indicacao do juizo (dependencia 676).

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel` (inclusive Sumula 134 STJ — so se ✅ no anexo). Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: defesa do proprio executado -> `impugnacao`/`embargos a execucao` (`execucao-adv-os`); defesa pela posse -> `possessorias`; reivindicacao pelo dominio -> `reivindicatoria-petitoria`.
