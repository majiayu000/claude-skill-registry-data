---
name: financeiro-precificacao
description: Estrutura ou revisa a precificação de um serviço/pacote da Creative Marketing, considerando custo, margem e posicionamento. Habilidade acionada pela skill orquestradora financeiro-gerente. Use quando o pedido for sobre definir preço de um serviço, revisar tabela de preços, ou avaliar se um preço cobre custo e margem — não usar pra proposta comercial em si a um cliente específico (isso é comercial-jornada-cliente-proposta, que pode consultar esta skill como referência de faixa de preço).
---

# Habilidade: Precificação

## Contexto obrigatório
Leia `/memoria/negocio.md` (serviços oferecidos) e `/financeiro/contexto.md`.

## O que pedir se não tiver
Custo real de entrega do serviço (tempo/pessoas envolvidas, ferramentas, custos diretos) — sem isso, qualquer preço sugerido é chute.

## Procedimento
1. Levante o **custo de entrega** do serviço (tempo da equipe, ferramentas/licenças, custos diretos).
2. Defina a **margem desejada** com base na meta financeira do negócio (ver `/memoria/negocio.md`).
3. Calcule o **preço mínimo viável** (custo + margem) e compare com o que o mercado/nicho do cliente costuma pagar, se essa informação existir.
4. Considere o modelo de cobrança adequado (fixo mensal, por projeto, por performance) — coerente com o tipo de serviço.
5. Apresente ao CEO com a lógica por trás do número, não só o valor final.

## Entrega
Salvar em `/saidas/AAAA-MM-DD/financeiro/precificacao-<servico>.md`.

## Regras
- Não fixar preço final sem aprovação explícita do CEO — esta skill recomenda, não decide.
- Não inventar custo — pedir o dado real.

## Skills complementares
Pode consultar `pricing` como apoio técnico — sem pular as regras acima.
