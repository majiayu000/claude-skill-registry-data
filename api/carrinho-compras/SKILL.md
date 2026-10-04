---
name: tray-carrinho-compras
description: >
  API de carrinho de compras da Tray.
  Permite criar, consultar, atualizar e excluir carrinhos,
  incluindo suporte a kits de produtos. Contém 6 endpoints.
---

# Carrinho de Compras

API para gerenciamento de carrinhos de compras na plataforma Tray.

Referência oficial: [https://developers.tray.com.br/#apis-de-carrinho-de-compra](https://developers.tray.com.br/#apis-de-carrinho-de-compra)

## Autenticação

Todas as requisições utilizam query string para autenticação:

```
?access_token={token}
```

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/carts/{session_id}?access_token={token}` | Obter dados do carrinho |
| GET | `/carts/{session_id}/complete?access_token={token}` | Obter dados completos do carrinho |
| POST | `/carts?access_token={token}` | Criar carrinho |
| POST | `/carts/kit?access_token={token}` | Criar carrinho com kit de produtos |
| PUT | `/carts/{session_id}?access_token={token}` | Atualizar carrinho |
| DELETE | `/carts/{session_id}?access_token={token}` | Excluir carrinho |

## Campos Principais

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `customer_id` | integer | ID do cliente associado ao carrinho |
| `product_id` | integer | ID do produto |
| `variant_id` | integer | ID da variação do produto |
| `quantity` | integer | Quantidade do item |
| `session_id` | string | Identificador da sessão do carrinho |
| `total` | decimal | Valor total do carrinho |
| `subtotal` | decimal | Subtotal do carrinho (sem frete e descontos) |
| `shipping_cost` | decimal | Custo do frete |
| `coupon_code` | string | Código do cupom de desconto aplicado |

## Exemplos

### Obter dados do carrinho

```http
GET /carts/abc123session?access_token={token}
```

Resposta:

```json
{
  "Cart": {
    "session_id": "abc123session",
    "customer_id": "456",
    "subtotal": "250.00",
    "shipping_cost": "15.00",
    "total": "265.00",
    "coupon_code": "",
    "Products": [
      {
        "product_id": "789",
        "variant_id": "101",
        "quantity": "2",
        "price": "125.00"
      }
    ]
  }
}
```

### Criar carrinho

```http
POST /carts?access_token={token}
Content-Type: application/json

{
  "Cart": {
    "customer_id": 456,
    "product_id": 789,
    "variant_id": 101,
    "quantity": 2
  }
}
```

### Criar carrinho com kit

```http
POST /carts/kit?access_token={token}
Content-Type: application/json

{
  "Cart": {
    "customer_id": 456,
    "kit_id": 10,
    "products": [
      {"product_id": 789, "variant_id": 101, "quantity": 1},
      {"product_id": 790, "variant_id": 102, "quantity": 1}
    ]
  }
}
```

### Atualizar carrinho

```http
PUT /carts/abc123session?access_token={token}
Content-Type: application/json

{
  "Cart": {
    "product_id": 789,
    "variant_id": 101,
    "quantity": 5
  }
}
```

### Excluir carrinho

```http
DELETE /carts/abc123session?access_token={token}
```

## Boas Práticas

- Utilize o endpoint `/carts/{session_id}/complete` quando precisar de todas as informações do carrinho, incluindo detalhes de produtos e frete.
- O `session_id` é o identificador único do carrinho — armazene-o de forma segura na sessão do usuário.
- Ao criar carrinhos com kit, certifique-se de que todos os produtos do kit estão disponíveis em estoque.
- Antes de aplicar um cupom via `coupon_code`, valide se o cupom existe e está ativo utilizando a API de cupons.
- Ao atualizar quantidades, verifique o estoque disponível para evitar erros.
- Exclua carrinhos abandonados periodicamente para manter a base limpa.

## Como Usar no Claude Code

### Exemplos de Prompt

- "cria um carrinho para o cliente 456 com 2 unidades do produto 789 variação M"
- "busca os dados completos do carrinho da sessão abc123"
- "cria um carrinho com o kit ID 10 incluindo todos os seus componentes"
- "implementa a lógica de recuperação de carrinho abandonado"

### O que o Claude faz

1. Gera o código de criação de carrinho com wrapper `Cart` e os campos necessários
2. Diferencia `POST /carts` (produto simples) de `POST /carts/kit` (bundle)
3. Usa `/carts/{session_id}/complete` para consultas com dados completos de produtos e frete
4. Implementa lógica de persistência do `session_id` na sessão do usuário

### O que você recebe

- Código de criação de carrinho com `customer_id`, `product_id` e `quantity`
- Código para carrinho com kit e múltiplos componentes
- Código de consulta completa com dados de produtos, frete e cupom
- Exemplo de fluxo de atualização de quantidade

### Pré-requisitos

- `access_token` configurado
- `customer_id` do cliente (ou sessão anônima)
- `product_id` e `variant_id` dos produtos
