---
name: tray-produtos-vendidos
description: >
  API de Produtos Vendidos da Tray. Utilize quando o desenvolvedor
  precisar consultar o histórico de vendas e analytics de produtos vendidos
  na loja. API somente leitura com filtros de data.
---

# API de Produtos Vendidos — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-produtos-vendidos

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/products-sold` | Listagem de produtos vendidos |

**Autenticação:** `?access_token={token}`

**Somente leitura** — esta API não permite criação, atualização ou exclusão.

## Filtros

| Parâmetro | Descrição |
|:--|:--|
| `created` | Filtrar por data de venda |
| `product_id` | Filtrar por produto |

## Paginação

`limit` (máximo 50, padrão 30), `page`.

## Uso

Ideal para relatórios de vendas, analytics e dashboards. Consulte periodicamente para manter dados atualizados.

## Como Usar no Claude Code

### Exemplos de Prompt

- "gera um relatório dos produtos mais vendidos no último mês"
- "consulta o histórico de vendas do produto 123"
- "implementa um dashboard de analytics de vendas por produto"

### O que o Claude faz

1. Gera o código para `GET /products-sold` com filtros de data e `product_id`
2. Itera pelas páginas para relatórios completos
3. Organiza os dados para exibição em dashboard ou exportação

### O que você recebe

- Código de consulta com filtros de data (`created`) e produto (`product_id`)
- Lógica de paginação para exportação completa do histórico
- Estrutura para relatório de produtos mais vendidos

### Pré-requisitos

- `access_token` configurado
