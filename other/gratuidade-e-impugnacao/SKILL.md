---
name: gratuidade-e-impugnacao
description: "Redige pedido de gratuidade da justica (CPC 98-102) e impugnacao a gratuidade da parte contraria. Trata a diferenca PF x PJ: pessoa fisica tem presuncao relativa (CPC 99 §3); pessoa juridica deve PROVAR a insuficiencia (Sumula 481/STJ). Use ao requerer ou impugnar justica gratuita, ao analisar declaracao de hipossuficiencia, quando o operador disser pedir gratuidade, justica gratuita, hipossuficiencia, impugnar a gratuidade do autor, beneficio da assistencia. Acionada pelo civel-master na gestao processual transversal."
---

# GRATUIDADE-E-IMPUGNACAO — Pedido e impugnacao da justica gratuita

> Camada 2 — gestao processual transversal. Esquecer o pedido custa caro; impugnar a tempo bloqueia a gratuidade indevida do adversario.

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 98 (direito), 99 (formulacao + §3 presuncao PF), 100 (impugnacao + prazo 15 dias), 101 (recurso: AI ou apelacao), 102 (revogacao).
- `context/jurisprudencia-civel.md` — Sumula 481/STJ (PJ deve provar) — citar so o que esta como ✅.

## Objetivo
(a) Redigir pedido de gratuidade calibrado ao tipo de parte (PF x PJ); (b) redigir impugnacao a gratuidade do adversario quando ha indicios de capacidade economica. Grep o artigo no anexo antes de citar.

## Quando ativar
- Cliente sem condicoes de arcar com custas — requerer gratuidade na inicial, contestacao, recurso ou peticao (CPC 99).
- Parte contraria obteve gratuidade que parece indevida — impugnar.
- Gatilhos: "pedir gratuidade", "justica gratuita", "hipossuficiencia", "impugnar a gratuidade", "beneficio da assistencia judiciaria".

## Metodologia
1. **Identificar o tipo de parte** — pessoa fisica ou juridica. Esta e a bifurcacao central.
2. **Pessoa fisica (CPC 99 §3 — grep)**: ha **presuncao relativa** de veracidade da alegacao de insuficiencia. Basta a **declaracao de hipossuficiencia** na peca; o juiz so pode indeferir com elementos concretos em sentido contrario. Anexar declaracao.
3. **Pessoa juridica (Sumula 481/STJ — anexo jurisprudencia)**: **NAO ha presuncao** — a PJ (com ou sem fins lucrativos) **deve demonstrar** a impossibilidade de arcar com os encargos. Instruir com prova: balanco, DRE, extratos, certidao de negativa de movimentacao, recuperacao judicial etc.
4. **Onde e quando pedir (CPC 99 — grep)**: na inicial, na contestacao, no ingresso de terceiro ou em recurso. Pedido superveniente por peticao simples.
5. **Impugnacao (CPC 100 — grep)**: oferecer na contestacao, replica, contrarrazoes ou peticao simples (pedido superveniente/terceiro), **prazo 15 dias**, sem suspender o curso. O **onus probatorio e do impugnante** — apontar sinais de capacidade economica (imoveis, veiculos, contratacao de advogado particular, gastos incompativeis). Em PJ, lembrar que ja cabia a ela provar.
6. **Recurso (CPC 101 — grep)**: do indeferimento/revogacao cabe **agravo de instrumento**; se resolvido na sentenca, **apelacao**. Mencionar como advertencia estrategica.
7. **Revogacao (CPC 102 — grep)**: efeitos do trancito em julgado da revogacao (recolhimento de todas as despesas + sancoes).

## Entrega obrigatoria final
- Peca redigida (pedido OU impugnacao) com fundamentacao especifica ao tipo de parte.
- Para PJ requerente: lista de provas a anexar. Para impugnacao: indicios concretos de capacidade + onus do impugnante.
- Alerta de prazo (15 dias na impugnacao) e via recursal cabivel.

## Guard
Nenhum dispositivo/sumula entra sem `validador-civel`; so citar a Sumula 481 como ✅ no anexo. Nunca tratar PJ como PF (presuncao nao se aplica a PJ). Pedido de gratuidade ausente quando cabivel reprova em R4 na `suprema-corte-civel`.
