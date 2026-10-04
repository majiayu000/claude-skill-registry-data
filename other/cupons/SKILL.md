---
name: tray-cupons
description: >
  API completa de cupons de desconto da Tray (discount_coupons).
  Permite criar, editar, excluir e consultar cupons, além de
  gerenciar relacionamentos com clientes, produtos, categorias,
  marcas e fretes. Contém 21 endpoints.
---

# Cupons de Desconto — API Tray

Documentação oficial: https://developers.tray.com.br/#api-de-cupom

> **Atenção:** O endpoint base é `/discount_coupons` (não `/coupons`). O wrapper de resposta é `DiscountCoupon` (não `Coupon`).

## Autenticação

Todas as requisições utilizam query string: `?access_token={token}`

## Paginação

Endpoints de listagem suportam: `?limit=30&page=1` (máximo 50 por página)

## Endpoints — CRUD

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/discount_coupons` | Listar cupons |
| GET | `/discount_coupons/:id` | Detalhes de um cupom |
| POST | `/discount_coupons` | Criar cupom |
| PUT | `/discount_coupons/:id` | Atualizar cupom |
| DELETE | `/discount_coupons/:id` | Excluir cupom |

## Endpoints — Consulta de Relacionamentos (GET)

| Endpoint | Descrição |
|:--|:--|
| `/discount_coupons/customer_relationship/:id` | Listar clientes vinculados |
| `/discount_coupons/product_relationship/:id` | Listar produtos vinculados |
| `/discount_coupons/category_relationship/:id` | Listar categorias vinculadas |
| `/discount_coupons/brand_relationship/:id` | Listar marcas vinculadas |
| `/discount_coupons/shipping_relationship/:id` | Listar fretes vinculados |
| `/discount_coupons/gift_relationship/:id` | Consultar cupom-presente vinculado |

> **Dica:** Ao listar cupons (`GET /discount_coupons`), o campo `coupon_type` indica qual relacionamento buscar: `cliente` → customer_relationship, `loja` com `local_application=produtos` → product_relationship, etc.

## Endpoint — Criação de Relacionamentos (POST)

Todos os tipos de relacionamento usam o **mesmo endpoint**:

```
POST /discount_coupons/create_relationship/:id
```

O tipo de relacionamento é definido pelo corpo da requisição (máximo 100 registros por POST):

**Vincular clientes:**
```json
{
  "DiscountCouponCustomer": [
    { "customer_id": "10" },
    { "customer_id": "20" }
  ]
}
```

**Vincular produtos:**
```json
{
  "DiscountCouponProduct": [
    { "product_id": "10" },
    { "product_id": "20" }
  ]
}
```

**Vincular categorias:**
```json
{
  "DiscountCouponCategory": [
    { "category_id": "10" }
  ]
}
```

**Vincular marcas:**
```json
{
  "DiscountCouponBrand": [
    { "brand_id": "10" }
  ]
}
```

**Vincular fretes (método de envio):**
```json
{
  "DiscountCouponShipping": [
    { "shipping_id": "10" }
  ]
}
```

**Vincular frete grátis (valor zerado):**
```json
{
  "DiscountCouponShipping": {
    "value": "0"
  }
}
```

**Vincular desconto de frete (valor específico):**
```json
{
  "DiscountCouponShipping": {
    "value": "10"
  }
}
```

**Criar cupom de troca a partir de pedido:**
```json
{
  "DiscountCouponCustomer": {
    "order_id": "10"
  }
}
```

## Campos — Criar/Atualizar Cupom

O body usa `Content-Type: application/x-www-form-urlencoded` com o wrapper `["DiscountCoupon"]["campo"]`. A estrutura JSON equivalente:

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `code` | string | Sim | Código do cupom — sem espaços nem acentos |
| `description` | string | Não | Descrição do cupom |
| `coupon_type` | string | Não | Tipo: `loja`, `cliente`, `troca`, `presente` |
| `starts_at` | date | Não | Início da validade (`YYYY-MM-DD`) |
| `ends_at` | date | Não | Fim da validade (`YYYY-MM-DD`) |
| `value` | decimal | Sim | Valor do desconto |
| `type` | string | Sim | `$` = reais / `%` = percentual |
| `value_start` | decimal | Não | Valor mínimo do produto para aplicar desconto |
| `value_end` | decimal | Não | Valor máximo do produto para aplicar desconto |
| `usage_sum_limit` | decimal | Não | Limite total acumulado de uso |
| `usage_counter_limit` | integer | Não | Limite de usos totais do cupom |
| `usage_counter_limit_customer` | integer | Não | Limite de usos por cliente |
| `cumulative_discount` | number | Não | `1` = acumula com desconto progressivo |

> **Campos `local_application`:** `loja`, `produtos`, `marcas`, `categorias`
> **Campos `freight_application`:** `nao_aplicavel`, `desconto`, `frete_gratis`

## Exemplos

### Listar cupons

```http
GET /discount_coupons?access_token={token}&limit=30&page=1
```

Resposta:

```json
{
  "paging": { "total": 7, "page": 1, "offset": 0, "limit": 30, "maxLimit": 50 },
  "DiscountCoupons": [
    {
      "DiscountCoupon": {
        "id": "7",
        "code": "NATAL25",
        "description": "Cupom de Natal",
        "value": "10.00",
        "type": "%",
        "starts_at": "2019-12-01",
        "ends_at": "2019-12-31",
        "usage_counter_limit": "0",
        "coupon_type": "loja",
        "local_application": "loja",
        "freight_application": "nao_aplicavel",
        "usage_counter_limit_customer": "10"
      }
    }
  ]
}
```

### Criar cupom

```http
POST /discount_coupons?access_token={token}
Content-Type: application/x-www-form-urlencoded

["DiscountCoupon"]["code"]=PROMO10&["DiscountCoupon"]["description"]=Promo Abril&["DiscountCoupon"]["starts_at"]=2026-04-01&["DiscountCoupon"]["ends_at"]=2026-04-30&["DiscountCoupon"]["value"]=10.00&["DiscountCoupon"]["type"]=%&["DiscountCoupon"]["usage_counter_limit_customer"]=5
```

Estrutura JSON equivalente do body:

```json
{
  "DiscountCoupon": {
    "code": "PROMO10",
    "description": "Promo Abril",
    "starts_at": "2026-04-01",
    "ends_at": "2026-04-30",
    "value": "10.00",
    "type": "%",
    "usage_counter_limit": "",
    "usage_counter_limit_customer": "5",
    "cumulative_discount": "0"
  }
}
```

Resposta de sucesso:

```json
{ "message": "Created", "id": "1", "code": 201 }
```

### Vincular produtos ao cupom

```http
POST /discount_coupons/create_relationship/7?access_token={token}
Content-Type: application/json

{
  "DiscountCouponProduct": [
    { "product_id": "456" },
    { "product_id": "789" }
  ]
}
```

### Consultar clientes do cupom

```http
GET /discount_coupons/customer_relationship/7?access_token={token}
```

Resposta:

```json
{
  "DiscountCouponCustomers": [
    { "DiscountCouponCustomer": { "customer_id": "1" } },
    { "DiscountCouponCustomer": { "customer_id": "20" } }
  ]
}
```

## Tipos de Cupom — Lógica de Uso

| `coupon_type` | Comportamento |
|:--|:--|
| `loja` | Genérico — aplica a toda a loja e todos os clientes |
| `cliente` | Restrito a clientes vinculados via `create_relationship` |
| `troca` | Gerado a partir de um pedido (`order_id`) |
| `presente` | Vincula a um produto como presente |

> Cupom sem nenhum relacionamento criado = cupom genérico válido para toda a loja.

## Boas Práticas

- O campo `code` não aceita espaços nem acentos.
- Campos `value_start` e `value_end` vazios = sem restrição de valor de produto.
- `usage_counter_limit` e `usage_counter_limit_customer` precisam ser consistentes entre si — se o cliente pode usar 2 vezes, o limite geral não pode ser menor que 2.
- Use `coupon_type=loja` sem relacionamentos para promoções gerais. Adicione relacionamentos para restrições.
- Limite de 100 registros por POST de relacionamento — divida lotes maiores.
- Consulte `coupon_type` e `local_application` no GET principal para saber qual endpoint de relacionamento chamar.

## Como Usar no Claude Code

### Exemplos de Prompt

- "cria um cupom PROMO10 de 10% de desconto válido por 30 dias"
- "cria um cupom de frete grátis para compras acima de R$ 150"
- "vincula o cupom VIP20 exclusivamente aos clientes do perfil Atacado"
- "lista todos os cupons ativos na loja"

### O que o Claude faz

1. Gera o código de criação com formato `x-www-form-urlencoded` e wrapper `DiscountCoupon`
2. Define os campos de validade (`starts_at`, `ends_at`), tipo (`percentage`/`value`) e limites de uso
3. Gera o código de relacionamento para cupons restritos a clientes, produtos ou categorias
4. Orienta sobre a diferença entre `coupon_type` (loja/cliente/troca/presente)

### O que você recebe

- Código de criação de cupom com todos os campos configurados
- Exemplo com `Content-Type: application/x-www-form-urlencoded` correto
- Código de relacionamento via `POST /discount_coupons/create_relationship/:id`
- Listagem de cupons ativos com filtros

### Pré-requisitos

- `access_token` configurado
- `customer_id`, `product_id` ou `category_id` se o cupom tiver restrições de relacionamento
