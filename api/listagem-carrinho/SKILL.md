---
name: tray-listagem-carrinho
description: >
  Nova API de Listagem de Carrinho da Tray. Utilize quando o desenvolvedor
  precisar listar todos os carrinhos de compra da loja com paginação. Endpoint
  separado da API principal de carrinho.
---

# Nova API de Listagem de Carrinho — Tray

Documentação oficial: https://developers.tray.com.br/#novo-api-de-listagem-de-carrinho

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/carts` | Listagem de todos os carrinhos com paginação |

**Autenticação:** `?access_token={token}`

## Paginação

| Parâmetro | Descrição |
|:--|:--|
| `limit` | Itens por página (máximo **50**, padrão **30**) |
| `page` | Número da página |

## Exemplo

```http
GET /carts?access_token={token}&limit=30&page=1
```

## Observação

Este endpoint é **separado** da API principal de Carrinho de Compras. Use-o para listar todos os carrinhos da loja. Para operações individuais (consultar, criar, atualizar, excluir), consulte o skill `tray-carrinho-compras`.

## Como Usar no Claude Code

### Exemplos de Prompt

- "lista todos os carrinhos abandonados da loja"
- "quantos carrinhos estão ativos no momento?"
- "implementa um relatório de carrinhos abandonados com paginação"

### O que o Claude faz

1. Gera o código para `GET /carts` com paginação configurada
2. Itera por todas as páginas para relatórios completos
3. Aponta para `tray-carrinho-compras` para operações em carrinhos individuais

### O que você recebe

- Código de listagem paginada com `limit` e `page`
- Lógica de iteração por páginas para exportação completa

### Pré-requisitos

- `access_token` configurado
