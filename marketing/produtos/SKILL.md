---
name: tray-produtos
description: >
  API de Produtos da Tray. Utilize quando o desenvolvedor precisar listar,
  consultar, cadastrar, atualizar ou excluir produtos no catálogo de uma loja Tray.
  Inclui todos os campos do produto (nome, preço, estoque, EAN, NCM, dimensões,
  SEO), filtros de listagem, paginação, ordenação e exclusão de kits.
when_to_use: >
  Use quando o desenvolvedor mencionar: cadastrar produto, atualizar produto,
  sincronizar catálogo, preço, estoque, EAN, SKU, imagem de produto, POST /products,
  PUT /products, variação de produto ou importar produtos.
---

# API de Produtos — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-produtos

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/products` | Listagem de produtos com paginação, filtros e ordenação |
| GET | `/products/:id` | Consultar dados detalhados de um produto |
| POST | `/products` | Cadastrar novo produto |
| PUT | `/products/:id` | Atualizar dados do produto |
| DELETE | `/products/:id` | Excluir produto |
| DELETE | `/kits/:id` | Excluir kit de produto |

**Autenticação:** `?access_token={token}` em todas as chamadas.

## Campos do Produto

### Dados Básicos

| Campo | Tipo | Limite | Descrição |
|:--|:--|:--|:--|
| `name` | string | 200 chars | Nome do produto |
| `ean` | string | 120 chars | Código de barras (EAN) |
| `ncm` | string | 8 chars | Classificação fiscal (NCM) |
| `description` | string | 4800 chars | Descrição completa |
| `description_small` | string | 500 chars | Descrição curta |
| `reference` | string | 120 chars | Referência interna |

### Preços

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `price` | decimal | Preço de venda |
| `cost_price` | decimal | Preço de custo |
| `promotional_price` | decimal | Preço promocional |
| `start_promotion` | date (YYYY-MM-DD) | Início da promoção |
| `end_promotion` | date (YYYY-MM-DD) | Fim da promoção |
| `ipi_value` | decimal | Valor do IPI |

### Dimensões e Peso

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `weight` | number | Peso em gramas |
| `length` | number | Comprimento |
| `width` | number | Largura |
| `height` | number | Altura |
| `cubic_weight` | number | Peso cúbico |

### Estoque e Disponibilidade

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `stock` | number | Quantidade em estoque |
| `available` | number | 0=indisponível, 1=disponível |
| `available_in_store` | number | 0=oculto da vitrine, 1=visível |
| `availability` | string | Texto de disponibilidade (ex: "Disponível em 3 dias") |
| `availability_days` | number | Dias até disponível |

### Classificação

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `category_id` | number | ID da categoria principal |
| `brand` | string (120) | Nome da marca |
| `brand_id` | number | ID da marca |
| `model` | string (150) | Modelo |
| `related_categories` | array | IDs de categorias adicionais |

### Exibição e Marketing

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `hot` | number | 0=normal, 1=destaque |
| `release` | number | 0=lançado, 1=lançamento |
| `release_date` | date | Data de lançamento |
| `virtual_product` | string | 0=físico, 1=digital/virtual |
| `free_shipping` | number | 0=frete normal, 1=frete grátis |
| `warranty` | string | Descrição da garantia |
| `upon_request` | number | Produto sob consulta |

### SEO

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `metatag` | object | `{type: "keywords", content: "..."}` |
| `shortcut` | string | Slug da URL |

## Paginação

| Parâmetro | Descrição |
|:--|:--|
| `limit` | Itens por página (máximo **50**, padrão **30**) |
| `page` | Número da página |

**Resposta inclui:** `total`, `page`, `offset`, `limit`, `maxLimit`

## Filtros de Listagem

`id`, `name`, `reference`, `ean`, `category_id`, `brand`, `available`, `available_in_store`, `stock`, `price`, `price_range`, `promotion`, `free_shipping`, `release`, `hot`, `quantity_sold`, `created`, `modified`

**Ordenação:** parâmetro `sort` com nome do campo. `rand` para aleatório.

## Corpo da Requisição (POST/PUT)

O body JSON deve envolver os dados na chave `"Product"`:

```json
{
  "Product": {
    "name": "Camiseta Exemplo",
    "price": "99.90",
    "stock": 100,
    "category_id": 1,
    "available": 1
  }
}
```

## Respostas

| Operação | Código | Mensagem |
|:--|:--|:--|
| Criação | 201 | `{"message": "Created", "id": 123, "code": 201}` |
| Atualização | 200 | `{"message": "Saved", "id": 123, "code": 200}` |
| Exclusão | 200 | `{"message": "Deleted", "id": 123, "code": 200}` |

## Resposta de Consulta Individual

O endpoint `GET /products/:id` retorna o objeto `Product` com dados adicionais:

- `Properties` — características do produto
- `payment_option_details` — opções de parcelamento
- `related_categories` — categorias associadas
- `all_categories` — todas as categorias
- `ProductImage` — array de imagens com thumbnails (30px, 90px, 180px em HTTP e HTTPS)
- `Variant` — array de variações do produto

## Como Usar no Claude Code

### Exemplos de Prompt

- "cadastra um novo produto na loja com preço, estoque e categoria"
- "atualiza o estoque e o preço promocional do produto ID 123"
- "lista todos os produtos sem estoque disponível"
- "como filtro produtos por categoria e faixa de preço?"

### O que o Claude faz

1. Identifica a operação desejada (criar, atualizar, listar ou consultar)
2. Gera o código com o wrapper `Product` obrigatório no body
3. Inclui os campos relevantes para o caso de uso (preço, estoque, dimensões, SEO)
4. Adiciona paginação e filtros se for listagem

### O que você recebe

- Código funcional da chamada à API com todos os campos necessários
- Wrapper `{"Product": {...}}` correto no body
- Parâmetros de paginação (`limit`, `page`) e filtros aplicados
- Tratamento da resposta com os IDs gerados

### Pré-requisitos

- `access_token` configurado
- `category_id` válido se for criar produto (use `tray-categorias` antes)
- `brand_id` válido se quiser associar marca (use `tray-marcas` antes)
