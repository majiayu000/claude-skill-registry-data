---
name: tray-pedidos
description: >
  API de Pedidos da Tray. Utilize quando o desenvolvedor precisar
  gerenciar o ciclo completo de pedidos: listagem com filtros, consulta de dados
  simples e completos, criação, atualização, cancelamento, e gestão de produtos
  dentro do pedido. Inclui todos os campos, status e fluxos de pedido.
when_to_use: >
  Use quando o desenvolvedor mencionar: pedido, order, status de pedido, cancelar pedido,
  atualizar pedido, GET /orders, POST /orders, ciclo de vida do pedido, fluxo de compra
  ou rastrear pedido.
---

# API de Pedidos — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-pedidos

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/orders` | Listagem de pedidos com paginação e filtros |
| GET | `/orders/:id` | Dados do pedido por ID |
| GET | `/orders/:id/full` | Dados completos (produtos, cliente, pagamento, frete) |
| POST | `/orders` | Cadastrar novo pedido |
| PUT | `/orders/:id` | Atualizar dados do pedido |
| PUT | `/orders/:id/cancel` | Cancelar pedido |
| POST | `/orders/:id/products` | Incluir produtos no pedido |
| DELETE | `/orders/:id/products/:product_id` | Excluir produto do pedido |

**Autenticação:** `?access_token={token}`

## Campos do Pedido

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `id` | number | ID do pedido |
| `store_id` | number | ID da loja |
| `status_id` | number | ID do status atual |
| `client_id` | number | ID do cliente |
| `adm_user` | string | Usuário administrativo |
| `total_amount` | decimal | Valor total do pedido |
| `shipping_cost` | decimal | Custo do frete |
| `shipping_method` | string | Método de envio |
| `tracking_number` | string | Código de rastreamento |
| `payment_method` | string | Método de pagamento |
| `coupon_code` | string | Código do cupom aplicado |
| `discount` | decimal | Valor do desconto |
| `taxes` | decimal | Impostos |
| `created_at` | datetime | Data de criação |
| `updated_at` | datetime | Data de atualização |

## Consulta Completa

O endpoint `GET /orders/:id/full` retorna dados completos incluindo:

- **Produtos** — lista de itens com quantidade, preço e variação
- **Cliente** — dados completos do comprador
- **Endereço** — endereço de entrega
- **Pagamento** — dados do método e status de pagamento
- **Frete** — dados de envio e rastreamento

## Filtros de Listagem

| Filtro | Descrição |
|:--|:--|
| `status` | Filtrar por status do pedido |
| `created_at` | Filtrar por data de criação |
| `updated_at` | Filtrar por data de atualização |
| `customer_id` | Filtrar por cliente |
| `payment_method` | Filtrar por método de pagamento |

## Cancelamento

Para cancelar um pedido, use `PUT /orders/:id/cancel`. O cancelamento atualiza o status e pode disparar webhooks.

## Incluir/Excluir Produtos

- `POST /orders/:id/products` — adiciona produtos ao pedido existente
- `DELETE /orders/:id/products/:product_id` — remove produto do pedido

## Paginação

`limit` (máximo 50, padrão 30), `page`.

## Ciclo de Vida do Pedido

```
Criação → Aguardando Pagamento → Pago → Em Separação → Enviado → Entregue
                                    ↘ Cancelado
```

## Boas Práticas

1. **Use `/orders/:id/full`** — para obter todos os dados em uma única chamada
2. **Webhook de pedido** — configure o webhook `order` para receber notificações em tempo real
3. **Código de rastreamento** — atualize o `tracking_number` quando o pedido for enviado
4. **Não exclua pedidos** — use cancelamento ao invés de exclusão

## Como Usar no Claude Code

### Exemplos de Prompt

- "lista os pedidos em aberto dos últimos 7 dias"
- "busca os dados completos do pedido ID 1001 incluindo produtos e pagamento"
- "cancela o pedido ID 2050"
- "atualiza o código de rastreamento do pedido 1500"

### O que o Claude faz

1. Identifica a operação desejada (listar, consultar, atualizar ou cancelar)
2. Usa `/orders/:id/full` para consultas completas e `/orders/:id` para dados básicos
3. Gera o código com os filtros adequados na listagem (status, data, cliente)
4. Inclui o tratamento da resposta e extração dos campos relevantes

### O que você recebe

- Código de consulta com os filtros aplicados e paginação configurada
- Chamada para `/orders/:id/full` com os dados completos do pedido
- Código de atualização com os campos necessários
- Código de cancelamento via `PUT /orders/:id/cancel`

### Pré-requisitos

- `access_token` configurado
- `order_id` disponível para operações em pedidos específicos
