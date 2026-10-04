---
name: tray-pagamentos
description: >
  API de Pagamentos da Tray. Utilize quando o desenvolvedor precisar
  gerenciar informações de pagamento da loja, incluindo listagem de pagamentos,
  consulta individual, criação, atualização, exclusão, opções de pagamento
  disponíveis e configurações. Suporta múltiplos tipos de pagamento: cartão de
  crédito, boleto bancário, PIX, transferência bancária e depósito.
---

# API de Pagamentos — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-informacoes-de-pagamento

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/payments` | Listagem de pagamentos com paginação e filtros |
| GET | `/payments/:id` | Consultar dados de um pagamento por ID |
| POST | `/payments` | Cadastrar novo pagamento |
| PUT | `/payments/:id` | Atualizar dados do pagamento |
| DELETE | `/payments/:id` | Excluir pagamento |
| GET | `/payments/options` | Listar opções/métodos de pagamento disponíveis na loja |
| GET | `/payments/settings` | Consultar configurações de pagamento da loja |

**Autenticação:** `?access_token={token}` em todas as chamadas.

## Campos do Pagamento

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `id` | number | — | ID do pagamento (retornado pela API) |
| `order_id` | number | Sim | ID do pedido associado |
| `payment_method` | string | Sim | Método de pagamento utilizado |
| `payment_type` | string | Sim | Tipo: "credit_card", "boleto", "pix", "transfer", "deposit" |
| `amount` | decimal | Sim | Valor do pagamento |
| `installments` | number | Não | Número de parcelas (para cartão de crédito) |
| `installment_value` | decimal | — | Valor de cada parcela |
| `status` | string | — | Status do pagamento (ex: "pending", "approved", "refused", "refunded") |
| `transaction_id` | string | — | ID da transação no gateway de pagamento |
| `card_brand` | string | — | Bandeira do cartão (ex: "Visa", "Mastercard", "Elo") |
| `card_last_digits` | string | — | Últimos 4 dígitos do cartão |
| `boleto_url` | string | — | URL do boleto para impressão |
| `boleto_barcode` | string | — | Código de barras do boleto |
| `pix_qrcode` | string | — | Código QR do PIX |
| `pix_key` | string | — | Chave PIX para pagamento |
| `paid_at` | datetime | — | Data/hora do pagamento |
| `created_at` | datetime | — | Data de criação |
| `updated_at` | datetime | — | Data da última atualização |

## Tipos de Pagamento

| Tipo | Descrição | Campos Específicos |
|:--|:--|:--|
| `credit_card` | Cartão de crédito | `card_brand`, `card_last_digits`, `installments`, `installment_value` |
| `boleto` | Boleto bancário | `boleto_url`, `boleto_barcode` |
| `pix` | PIX (pagamento instantâneo) | `pix_qrcode`, `pix_key` |
| `transfer` | Transferência bancária | `transaction_id` |
| `deposit` | Depósito bancário | `transaction_id` |

## Status do Pagamento

| Status | Descrição |
|:--|:--|
| `pending` | Aguardando pagamento |
| `processing` | Em processamento |
| `approved` | Pagamento aprovado |
| `refused` | Pagamento recusado |
| `refunded` | Pagamento estornado |
| `cancelled` | Pagamento cancelado |
| `chargeback` | Chargeback (contestação) |

## Paginação

| Parâmetro | Descrição |
|:--|:--|
| `limit` | Itens por página (máximo **50**, padrão **30**) |
| `page` | Número da página |

**Resposta inclui:** `total`, `page`, `offset`, `limit`, `maxLimit`

## Filtros de Listagem

| Filtro | Tipo | Descrição |
|:--|:--|:--|
| `order_id` | number | Filtrar por pedido |
| `payment_type` | string | Filtrar por tipo de pagamento |
| `status` | string | Filtrar por status |
| `created_at` | date | Filtrar por data de criação |

## Corpo da Requisição — Criar Pagamento (POST)

```json
{
  "Payment": {
    "order_id": 1001,
    "payment_method": "PagSeguro",
    "payment_type": "credit_card",
    "amount": "299.90",
    "installments": 3,
    "status": "approved",
    "transaction_id": "PAG-123456",
    "card_brand": "Visa",
    "card_last_digits": "4321"
  }
}
```

## Corpo da Requisição — Atualizar Pagamento (PUT)

```json
{
  "Payment": {
    "status": "approved",
    "transaction_id": "PAG-123456",
    "paid_at": "2026-03-21 14:30:00"
  }
}
```

## Respostas

| Operação | Código | Mensagem |
|:--|:--|:--|
| Criação | 201 | `{"message": "Created", "id": 800, "code": 201}` |
| Atualização | 200 | `{"message": "Saved", "id": 800, "code": 200}` |
| Exclusão | 200 | `{"message": "Deleted", "id": 800, "code": 200}` |

## Exemplo de Resposta — Listar Pagamentos

```json
{
  "paging": {
    "total": 50,
    "page": 1,
    "offset": 0,
    "limit": 30,
    "maxLimit": 50
  },
  "Payments": [
    {
      "Payment": {
        "id": "800",
        "order_id": "1001",
        "payment_method": "PagSeguro",
        "payment_type": "credit_card",
        "amount": "299.90",
        "installments": "3",
        "installment_value": "99.97",
        "status": "approved",
        "transaction_id": "PAG-123456",
        "card_brand": "Visa",
        "card_last_digits": "4321",
        "paid_at": "2026-03-21 14:30:00",
        "created_at": "2026-03-21 14:25:00",
        "updated_at": "2026-03-21 14:30:00"
      }
    }
  ]
}
```

## Exemplo de Resposta — Opções de Pagamento

```json
{
  "PaymentOptions": [
    {
      "PaymentOption": {
        "id": "1",
        "name": "Cartão de Crédito",
        "type": "credit_card",
        "active": "1",
        "max_installments": "12",
        "min_installment_value": "10.00"
      }
    },
    {
      "PaymentOption": {
        "id": "2",
        "name": "Boleto Bancário",
        "type": "boleto",
        "active": "1",
        "discount": "5.00"
      }
    },
    {
      "PaymentOption": {
        "id": "3",
        "name": "PIX",
        "type": "pix",
        "active": "1",
        "discount": "10.00"
      }
    }
  ]
}
```

## Exemplo de Resposta — Configurações de Pagamento

```json
{
  "PaymentSettings": {
    "gateway": "PagSeguro",
    "environment": "production",
    "max_installments": 12,
    "min_installment_value": "10.00",
    "boleto_days_to_expire": 3,
    "pix_minutes_to_expire": 30,
    "anti_fraud_enabled": true
  }
}
```

## Boas Práticas

1. **Não armazene dados sensíveis** — nunca armazene número completo do cartão; use apenas `card_last_digits` e `card_brand`
2. **Atualize o status** — mantenha o status do pagamento sincronizado com o gateway (use webhooks quando possível)
3. **PIX com expiração** — pagamentos PIX possuem tempo de expiração; verifique `pix_minutes_to_expire` nas configurações
4. **Boleto com vencimento** — configure `boleto_days_to_expire` adequadamente para evitar pedidos pendentes indefinidamente
5. **Parcelamento** — respeite `max_installments` e `min_installment_value` das configurações da loja
6. **Webhook de pagamento** — configure o webhook `payment` para receber notificações em tempo real de alterações de status
7. **Conciliação** — use `transaction_id` para conciliar pagamentos entre a Tray e o gateway
8. **Múltiplos pagamentos** — um pedido pode ter múltiplos pagamentos (ex: parte no cartão, parte no boleto)
9. **Recursos relacionados** — consulte os skills `tray-pedidos` e `tray-webhooks` para operações complementares

## Como Usar no Claude Code

### Exemplos de Prompt

- "lista os métodos de pagamento disponíveis na loja"
- "consulta todos os pagamentos aprovados do dia de hoje"
- "registra o pagamento via PIX para o pedido 1001"
- "implementa a conciliação de pagamentos entre a Tray e meu gateway"

### O que o Claude faz

1. Gera o código de consulta de opções de pagamento via `GET /payments/options`
2. Gera o código de registro de pagamento com wrapper `Payment` e campos específicos por tipo
3. Filtra pagamentos por status, tipo e data conforme necessário
4. Implementa conciliação usando `transaction_id` do gateway

### O que você recebe

- Código de listagem de opções e configurações de pagamento da loja
- Código de criação de pagamento com campos específicos por tipo (PIX, boleto, cartão)
- Filtros de consulta por status e data
- Lógica de conciliação com `transaction_id`

### Pré-requisitos

- `access_token` configurado
- `order_id` do pedido para registro de pagamento
- Gateway de pagamento configurado na loja Tray
