---
name: tray-variacoes
description: >
  API de Variações de Produtos da Tray. Utilize quando o desenvolvedor
  precisar gerenciar variantes de produtos (SKUs) como diferentes tamanhos, cores
  ou modelos. Inclui listagem, consulta, cadastro, atualização, exclusão e
  informações sobre limitações de variações por produto.
---

# API de Variações de Produtos — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-variacao-de-produtos

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/variants` | Listagem de variações com paginação |
| GET | `/variants/:id` | Consultar dados de uma variação |
| POST | `/variants` | Cadastrar nova variação |
| PUT | `/variants/:id` | Atualizar dados da variação |
| DELETE | `/variants/:id` | Excluir variação |

**Autenticação:** `?access_token={token}`

## Campos da Variação

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `product_id` | number | ID do produto pai (obrigatório na criação) |
| `ean` | string | Código de barras da variação |
| `price` | decimal | Preço da variação (herda do produto se não informado) |
| `cost_price` | decimal | Preço de custo |
| `stock` | number | Estoque da variação |
| `weight` | number | Peso em gramas |
| `length` | number | Comprimento |
| `width` | number | Largura |
| `height` | number | Altura |
| `reference` | string | Referência interna da variação |
| `values` | array | Atributos da variação (ex: cor, tamanho) |

## Herança de Dados

Quando um campo não é informado na variação, ele herda o valor do produto pai. Isso se aplica a: `price`, `weight`, `length`, `width`, `height`.

## Limitação de Variações por Produto

A plataforma Tray impõe um limite de variações por produto. Consulte a seção "Limitação de variações por produto" na documentação oficial para os limites atuais.

## Corpo da Requisição (POST/PUT)

```json
{
  "Variant": {
    "product_id": 123,
    "ean": "7891234567890",
    "price": "89.90",
    "stock": 50,
    "values": [
      {"name": "Cor", "value": "Azul"},
      {"name": "Tamanho", "value": "M"}
    ]
  }
}
```

## Paginação

Mesmos parâmetros da API de Produtos: `limit` (máximo 50, padrão 30), `page`.

## Imagens de Variação

As imagens de variação são gerenciadas pela API de Imagens separada (`POST /variants/:id/images`). Consulte o skill `tray-imagens-produtos`.

## Como Usar no Claude Code

### Exemplos de Prompt

- "adiciona variações de tamanho e cor ao produto 456"
- "atualiza o estoque da variação tamanho M cor azul"
- "lista todas as variações do produto 123"
- "como crio variações com preço e estoque individuais?"

### O que o Claude faz

1. Gera o código com o wrapper `Variant` e o `product_id` do produto pai
2. Monta o array `values` com os atributos (cor, tamanho, modelo, etc.)
3. Define campos individuais da variação (preço, estoque, EAN) quando necessário
4. Explica a herança de dados do produto pai para campos não informados

### O que você recebe

- Código de criação de variação com wrapper `{"Variant": {...}}` correto
- Array `values` montado com os atributos desejados
- Lógica de herança explicada (quais campos herdam do produto pai)
- Exemplo de listagem por `product_id`

### Pré-requisitos

- Produto pai já cadastrado com o `product_id` disponível
- `access_token` configurado
