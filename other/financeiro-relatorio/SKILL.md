---
name: financeiro-relatorio
description: Monta o relatório de performance financeira da Creative Marketing — receita, custos, margem, métricas de negócio (MRR, CAC, churn, etc.) e comparação com metas. Habilidade acionada pela skill orquestradora financeiro-gerente. Use quando o pedido for sobre relatório financeiro, dashboard, "como estamos financeiramente", ou métricas do negócio — não usar para fluxo de caixa detalhado (isso é financeiro-fluxo-caixa) nem para precificação (isso é financeiro-precificacao).
---

# Habilidade: Relatório Financeiro

## Contexto obrigatório
Leia `/memoria/negocio.md` (metas: +10 clientes, +R$10k/mês) e `/financeiro/contexto.md`.

## O que pedir se não tiver
Dados reais do período (receita, custos, número de clientes, cancelamentos). Sem dado real, não gerar número — sinalizar o que falta.

## Procedimento
1. Reúna os números do período: receita total, custos, margem, número de clientes ativos, novos clientes, cancelamentos.
2. Compare com as **metas registradas** em `/memoria/negocio.md` e com o período anterior, quando houver dado.
3. Calcule métricas relevantes quando os dados permitirem: ticket médio, receita recorrente, churn.
4. Traga uma **leitura qualitativa**, não só números — o que os números significam pro negócio.
5. Aponte os pontos de atenção mais importantes primeiro (não enterrar o principal insight em meio a uma lista de números).

## Template
```
# Relatório Financeiro — <período>

## Resumo
...

## Números
| Métrica | Este período | Anterior | Meta |
|---|---|---|---|

## Leitura
...
```

## Entrega
Salvar em `/saidas/AAAA-MM-DD/financeiro/relatorio-<periodo>.md`.

## Regras
- Nunca inventar número — sinalizar o que falta em vez de estimar.

## Skills complementares
Pode consultar `saas-metrics`, `saas-metrics-coach`, `saas-revenue-growth-metrics`, `saas-economics-efficiency-metrics`, `data:build-dashboard` e `data:create-viz` como apoio técnico — sem pular as regras acima.
