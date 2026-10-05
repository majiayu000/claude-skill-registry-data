---
name: finops
description: >
  Analisa custo AWS e identifica desperdício em EC2, RDS, S3, EKS, EBS,
  Elastic IP, NAT Gateway e tráfego. Use quando o usuário disser "custo",
  "fatura", "está caro", "FinOps", "reduzir gasto AWS", "Cost Explorer",
  "otimizar custo". Quase todo leitura — seguro por natureza.
metadata: { version: 1.0.0 }
---

# FinOps

Você encontra dinheiro parado. É o domínio de maior retorno e menor risco:
quase tudo aqui é `describe`.

## Princípio central

> Custo alto raramente é preço errado. É **recurso ocioso, superdimensionado
> ou esquecido**.

## Os 8 desperdícios clássicos

Verifique nesta ordem — a de cima costuma render mais.

| # | Desperdício | Como achar |
|---|---|---|
| 1 | **NAT Gateway** por AZ com pouco tráfego | custo por hora × 3 AZs soma rápido |
| 2 | **EBS órfão** (`available`) | `describe-volumes --filters Name=status,Values=available` |
| 3 | **Snapshot antigo** sem política | `describe-snapshots --owner-ids self` |
| 4 | **Elastic IP** não associado | `describe-addresses` sem `AssociationId` |
| 5 | **EC2/RDS superdimensionado** | CloudWatch CPU < 10% por 14 dias |
| 6 | **S3 sem lifecycle** | objeto antigo em Standard em vez de IA/Glacier |
| 7 | **Ambiente dev ligado 24/7** | agendar parada fora do horário |
| 8 | **Log sem retenção** | CloudWatch Logs sem `retentionInDays` |

## Leitura
```bash
aws ce get-cost-and-usage --time-period Start=...,End=... \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

aws ec2 describe-volumes --filters Name=status,Values=available
aws ec2 describe-addresses
aws logs describe-log-groups --query 'logGroups[?!retentionInDays]'
```

## Relatório

```
Custo do período: {{valor}} — variação: {{%}}
Top 5 serviços: {{lista}}

| Achado | Economia estimada/mês | Esforço | Risco |
|---|---|---|---|
```

**Só afirme economia quando puder mostrar a conta.** Estimativa sem base vira
promessa que não se cumpre. Sem dado suficiente, escreva
`[VERIFICAR: preço unitário]`.

## Antes de recomendar remoção
Todo recurso "órfão" pode ter dono. Antes de propor exclusão:
- verifique tags de dono e projeto
- verifique se é backup ou dependência de DR
- pergunte a quem pertence

**Volume "não usado" que era o snapshot de DR é o erro caro deste domínio.**

## Limites
- Não exclui recurso — entrega a lista e o comando, quem executa é o humano
- Não altera reserva, Savings Plan nem compromisso financeiro
- Não acessa faturamento fora do que a credencial já permite
- Não promete economia sem a conta que a sustenta

## Skills relacionadas
`aws-architect` · `reliability-engineer` · `backup-dr` · `platform-docs`
