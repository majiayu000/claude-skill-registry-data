---
name: tray-categorias
description: >
  API de Categorias da Tray. Utilize quando o desenvolvedor precisar
  gerenciar a árvore de categorias da loja, incluindo consulta hierárquica,
  criação de subcategorias, reordenação e exclusão. Inclui consulta de árvore
  completa e dados individuais por ID.
---

# API de Categorias — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-categorias

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/categories` | Consultar árvore de categorias |
| GET | `/categories/all` | Consultar dados de todas as categorias |
| GET | `/categories/:id` | Consultar dados de uma categoria por ID |
| POST | `/categories` | Cadastrar nova categoria |
| PUT | `/categories/:id` | Atualizar dados da categoria |
| PUT | `/categories/:id/order` | Atualizar ordem da categoria |
| DELETE | `/categories/:id` | Excluir categoria |

**Autenticação:** `?access_token={token}`

**Nota:** O endpoint de árvore de categorias (`GET /categories`) também está disponível **publicamente** sem autenticação via prefixo `/web_api/categories`.

## Campos da Categoria

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `name` | string | Nome da categoria (obrigatório) |
| `parent_id` | number | ID da categoria pai (0 = raiz) |
| `description` | string | Descrição da categoria |
| `slug` | string | Slug da URL |
| `order` | number | Posição de ordenação |
| `has_product` | boolean | Indica se possui produtos |

## Corpo da Requisição (POST/PUT)

```json
{
  "Category": {
    "name": "Eletrônicos",
    "parent_id": 0,
    "description": "Produtos eletrônicos"
  }
}
```

## Árvore de Categorias

O endpoint `GET /categories` retorna a hierarquia completa com categorias aninhadas. Cada categoria inclui suas subcategorias no array `children`.

## Reordenação

Para reordenar categorias, use `PUT /categories/:id/order` com o campo `order` indicando a nova posição.

## Boas Práticas

1. **Crie categorias antes de produtos** — o `category_id` é obrigatório na criação de produto
2. **Use a árvore pública** — para vitrines, use `/web_api/categories` sem autenticação
3. **Hierarquia** — planeje a estrutura antes de criar (máximo de níveis varia por plano)

## Como Usar no Claude Code

### Exemplos de Prompt

- "cria a estrutura de categorias da loja: Eletrônicos > Celulares e Eletrônicos > Notebooks"
- "lista todas as categorias em formato de árvore hierárquica"
- "como crio subcategorias dentro de uma categoria existente?"
- "reordena as categorias por relevância"

### O que o Claude faz

1. Gera o código de criação de categoria pai (com `parent_id: 0`) e subcategorias
2. Monta a hierarquia com chamadas sequenciais (pai antes do filho)
3. Inclui o wrapper `Category` correto no body de cada chamada
4. Demonstra como buscar a árvore completa com `GET /categories`

### O que você recebe

- Código de criação de categorias com hierarquia correta
- Sequência de chamadas respeitando a dependência pai → filho
- Código de consulta da árvore completa
- Exemplo de reordenação via `PUT /categories/:id/order`

### Pré-requisitos

- `access_token` configurado
- Estrutura de categorias planejada previamente (nomes e hierarquia)
