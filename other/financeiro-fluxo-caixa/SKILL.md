---
name: financeiro-fluxo-caixa
description: Organiza e projeta o fluxo de caixa da Creative Marketing — entradas, saídas, saldo e projeção futura. Habilidade acionada pela skill orquestradora financeiro-gerente. Use quando o pedido for sobre controlar entradas/saídas, saldo de caixa, ou projetar o caixa dos próximos meses — não usar para definir preço (isso é financeiro-precificacao) nem para cobrar cliente (isso é financeiro-cobranca).
---

# Habilidade: Fluxo de Caixa

## Contexto obrigatório
Leia `/memoria/negocio.md` (metas de faturamento) e `/financeiro/contexto.md`.

## O que pedir se não tiver
Dados reais de entradas e saídas do período (não estimar). Sem isso, a skill não monta um fluxo de caixa confiável.

## Procedimento
1. Organize as **entradas** (recebimentos de clientes, outras receitas) e **saídas** (custos fixos, variáveis, impostos) do período.
2. Calcule o **saldo** do período e o saldo acumulado.
3. Se houver dados de períodos anteriores, monte uma **projeção simples** dos próximos meses com base na tendência (nunca apresentar projeção como certeza — deixar claro que é estimativa).
4. Sinalize pontos de atenção: saldo negativo projetado, dependência de poucos clientes, sazonalidade.

## Template
```
# Fluxo de Caixa — <período>

| Categoria | Entrada | Saída |
|---|---|---|

Saldo do período: 
Saldo acumulado: 
```

## Entrega
Salvar em `/saidas/AAAA-MM-DD/financeiro/fluxo-caixa-<periodo>.md`.

## Regras
- Nunca inventar valor — pedir o dado real.
- Não executar nenhuma movimentação financeira de fato.

## Skills complementares
Pode consultar `xlsx`/`google-sheets` (planilha) e `data:analyze`/`data:create-viz` (visualização) como apoio técnico — sem pular as regras acima.
