---
name: consignacao-em-pagamento
description: "Redige a acao de consignacao em pagamento (CPC 539-549; CC 334-345): hipoteses de consignacao (CC 335), requisitos do deposito (CC 336-337), efeitos da consignacao procedente (CC 339-343), deposito no prazo de 5 dias (CPC 542 I), insuficiencia do deposito (CPC 545) e a via EXTRAJUDICIAL bancaria com prazo de recusa de 10 dias (CPC 539 §1 a §4). Use quando o operador disser consignar pagamento, consignacao em pagamento, credor recusa receber, deposito judicial de divida, ou mora do credor."
---

# CONSIGNACAO-EM-PAGAMENTO

> Camada 5 (acoes civeis). Liberacao do devedor pelo deposito quando o credor recusa, falta ou ha duvida sobre quem deva receber. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cc-10406-02.md` — arts. 334 (deposito extingue a obrigacao), 335 (hipoteses), 336-337 (requisitos e lugar do deposito), 339-345 (efeitos) — **grep + ler a faixa**.
- `context/cpc-13105-15.md` — arts. 539 (consignacao + extrajudicial bancaria §1-§4), 542 (inicial e deposito em 5 dias), 544-545 (contestacao e insuficiencia), 547-548 (duvida sobre o credor) — **grep + ler a faixa**.
- `context/cpc-cc-alteracoes-recentes.md` + `context/jurisprudencia-civel.md` (so ✅).

## Objetivo
Liberar o devedor da obrigacao via deposito (CC 334), enfrentando a mora do credor, com a via correta (judicial ou extrajudicial bancaria) e deposito tempestivo, sem extincao por falta de deposito (CPC 542 par. unico).

## Quando ativar
- Credor recusa receber, nao se sabe quem deva receber, ou ha mora do credor.
- Devedor quer depositar para se exonerar da divida.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2) antes de redigir:** `competencia-e-foro` (lugar do pagamento — CPC 540) · `valor-da-causa` · `gratuidade-e-impugnacao` · `tempestividade-civel`.
2. **Enquadrar a hipotese (CC 335)** — recusa do credor, ausencia, incapacidade, duvida sobre quem recebe, litigio sobre o objeto.
3. **Via extrajudicial bancaria (CPC 539 §1-§4):** deposito em estabelecimento bancario + cientificacao do credor por AR com prazo de 10 dias para recusa; sem recusa, devedor liberado (§2); com recusa, ajuizar em 1 mes (§3).
4. **Via judicial (CPC 542):** requerer o deposito (a efetivar em 5 dias do deferimento — inciso I) + citacao do reu para levantar ou contestar (II); nao depositado no prazo, extincao sem merito (par. unico).
5. **Insuficiencia (CPC 545):** alegada na contestacao, o autor pode completar em 10 dias; prestacoes sucessivas (CPC 541; CC 343 quanto a despesas).
6. **Efeitos (CC 334, 339-340):** procedente, extingue a obrigacao; cessam juros e riscos a partir do deposito (CPC 540).

## Entrega obrigatoria final
- Peca redigida ponta a ponta (hipotese 335 + pedido de deposito + citacao + extincao da obrigacao) + checklist de documentos (prova da recusa/mora, calculo do valor) + indicacao da via (judicial x extrajudicial) e foro/vara.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria. Entrega pela `suprema-corte-civel`. Cross-link, nao duplicar: calculo do valor consignado -> `calculosjudiciais-adv-os`; consignacao de aluguel/locacao e familia fora do escopo; consumidor (CDC) fora.
