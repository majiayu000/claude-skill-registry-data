---
name: financeiro-cobranca
description: Estrutura a cobrança de um cliente em atraso e a comunicação de negociação de pagamento da Creative Marketing. Habilidade acionada pela skill orquestradora financeiro-gerente. Use quando o pedido for sobre cliente inadimplente, cobrança de pagamento atrasado, ou negociar um débito — não usar para a proposta comercial original (isso é comercial-jornada-cliente-proposta) nem para retenção geral de cliente sem inadimplência (isso é comercial-jornada-cliente-retencao).
---

# Habilidade: Cobrança

## Contexto obrigatório
Leia `/memoria/tom-de-voz.md` e `/financeiro/contexto.md`.

## O que pedir se não tiver
Valor exato em atraso, data de vencimento, e histórico de pagamento do cliente (é a primeira vez ou é recorrente) — isso muda o tom da abordagem.

## Procedimento
1. Escreva a **primeira cobrança**: tom cordial, direto, sem acusação — lembrete de que o pagamento está em aberto, com valor e data exatos.
2. Se não houver resposta, escreva um **segundo contato** um pouco mais firme, ainda profissional, oferecendo abertura pra negociar se houver dificuldade real.
3. Para negociação: apresentar opções (parcelamento, nova data) sem comprometer nada sem aprovação do CEO.
4. Nunca ameaçar ou usar tom agressivo — preservar o relacionamento sempre que possível, já que cliente recuperado vale mais que cliente perdido por atrito.

## Entrega
Mensagens de cobrança prontas, salvas em `/saidas/AAAA-MM-DD/financeiro/cobranca-<cliente>.md`.

## Regras
- Nunca enviar cobrança real ao cliente sem aprovação explícita do CEO.
- Nunca oferecer desconto/parcelamento sem confirmação do CEO.
- Nunca inventar valor ou data — confirmar antes.

## Skills complementares
Nenhuma skill do ecossistema específica de cobrança foi encontrada — este procedimento é próprio da Creative.
