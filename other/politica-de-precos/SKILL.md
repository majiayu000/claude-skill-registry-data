---
name: politica-de-precos
description: Cálculo de preço mínimo, margem e promoção, com fórmulas e dados fornecidos pelo lojista.
---

# Skill: politica-de-precos

## Entradas (fornecidas pelo lojista)
Custo do produto, impostos sobre a venda (%), taxa do canal (%), taxa de pagamento (%), frete subsidiado (R$), embalagem (R$), margem-alvo (%).

## Fórmulas
- **Custos percentuais totais (p)** = impostos + taxa do canal + taxa de pagamento
- **Preço mínimo (margem zero)** = (custo + frete + embalagem) / (1 − p)
- **Preço com margem-alvo m** = (custo + frete + embalagem) / (1 − p − m)
- **Margem (R$)** = preço × (1 − p) − (custo + frete + embalagem)
- **Margem (%)** = Margem (R$) / preço
- **Desconto máximo sem prejuízo** = 1 − preço mínimo / preço atual
- **CPA máximo para anúncios** = Margem (R$) antes do anúncio

## Regras
- Mostre a conta passo a passo e salve em CSV.
- Valor ausente = peça ao lojista ou marque A CONFIRMAR; não estime.
- Promoções devem manter margem acima do mínimo definido pelo lojista.
- Isto não é orientação tributária; o lojista confirma alíquotas com contador.
