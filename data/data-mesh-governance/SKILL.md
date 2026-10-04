---
name: data-mesh-governance
description: Especialista em Arquitetura Data Mesh, Produtos de Dados (Data Products) e Governança Federada baseado nas obras Implementing Data Mesh (Jean-Georges Perrin) e The Enterprise Data Catalog (Ole Olesen-Bagneux). Cobre os 4 princípios do Data Mesh (Domain Ownership, Data as a Product, Self-Serve Data Platform, Federated Computational Governance), Data Contracts (OpenDataContract), linhagem de dados e catálogos corporativos.
---

# Arquitetura Data Mesh e Governança Federada de Dados

Esta skill estabelece os princípios arquiteturais e operacionais para transição de data lakes monolíticos centralizados para uma abordagem descentralizada orientada a domínios (**Data Mesh**), com governança automatizada e contratos formais de dados.

---

## 🏛️ 1. Os 4 Princípios Fundamentais do Data Mesh

1. **Propriedade Orientada a Domínio (Domain Ownership)**: Equipes de negócio/engenharia donas do domínio operacional são responsáveis pelos seus dados analíticos.
2. **Dados como Produto (Data as a Product - DaaP)**: Os dados analíticos possuem consumidores identificados, SLA/SLO de qualidade, documentação e contratos formais.
3. **Plataforma de Dados de Autosserviço (Self-Serve Data Platform)**: Infraestrutura agnóstica de domínio que abstrai a complexidade de provisionamento de pipelines, armazenamento e acessos.
4. **Governança Computacional Federada (Federated Computational Governance)**: Políticas de segurança, privacidade (LGPD/GDPR), conformidade e auditoria aplicadas automaticamente via código (*Policy as Code*).

---

## 📜 2. Estrutura de um Data Contract (OpenDataContract Specification)

```yaml
version: 1.0.0
dataset: orders_completed
domain: checkout_financial
owner: team-checkout@empresa.com
status: active
sla:
  freshness: 5m
  availability: 99.9%
schema:
  - name: order_id
    type: string
    description: "UUID da transação aprovada"
    required: true
    pii: false
  - name: customer_tax_id
    type: string
    description: "CPF/Tax ID do comprador"
    required: true
    pii: true
    classification: restricted
  - name: total_amount_cents
    type: integer
    description: "Valor em centavos de moeda corrente"
    required: true
```
