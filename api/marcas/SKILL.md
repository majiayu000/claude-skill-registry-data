---
name: tray-marcas
description: >
  API de Marcas da Tray. Utilize quando o desenvolvedor precisar gerenciar
  as marcas (fabricantes) dos produtos da loja, incluindo listagem, consulta individual,
  criação, atualização e exclusão. Inclui campos de nome, slug, descrição e imagem
  da marca, além de paginação e filtros.
---

# API de Marcas — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-marca-do-produto

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/products/brands` | Listagem de marcas com paginação e filtros |
| GET | `/products/brands/:id` | Consultar dados de uma marca por ID |
| POST | `/products/brands` | Cadastrar nova marca |
| PUT | `/products/brands/:id` | Atualizar dados da marca |
| DELETE | `/products/brands/:id` | Excluir marca |

**Autenticação:** `?access_token={token}` em todas as chamadas.

> **Alias não oficial:** a rota `/brands` (sem o prefixo `/products/`) também retorna HTTP 200 nesta API, mas não é documentada oficialmente pela Tray. Use sempre `/products/brands` para garantir compatibilidade e aderência à documentação oficial.

## Campos da Marca

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `id` | number | — | ID da marca (retornado pela API) |
| `name` | string | Sim | Nome da marca |
| `slug` | string | Não | Slug para URL amigável (gerado automaticamente se não informado) |
| `description` | string | Não | Descrição da marca |
| `image` | string | Não | URL da imagem/logotipo da marca |

## Paginação

| Parâmetro | Descrição |
|:--|:--|
| `limit` | Itens por página (máximo **50**, padrão **30**) |
| `page` | Número da página |

**Resposta inclui:** `total`, `page`, `offset`, `limit`, `maxLimit`

## Filtros de Listagem

| Filtro | Tipo | Descrição |
|:--|:--|:--|
| `id` | number | Filtrar por ID da marca |
| `name` | string | Filtrar por nome da marca |
| `slug` | string | Filtrar por slug |

## Corpo da Requisição (POST/PUT)

```json
{
  "Brand": {
    "name": "Nike",
    "slug": "nike",
    "description": "Marca esportiva internacional",
    "image": "https://exemplo.com/logo-nike.png"
  }
}
```

## Respostas

| Operação | Código | Mensagem |
|:--|:--|:--|
| Criação | 201 | `{"message": "Created", "id": 10, "code": 201}` |
| Atualização | 200 | `{"message": "Saved", "id": 10, "code": 200}` |
| Exclusão | 200 | `{"message": "Deleted", "id": 10, "code": 200}` |

## Exemplo de Resposta — Listar Marcas

```json
{
  "paging": {
    "total": 25,
    "page": 1,
    "offset": 0,
    "limit": 30,
    "maxLimit": 50
  },
  "Brands": [
    {
      "Brand": {
        "id": "1",
        "name": "Nike",
        "slug": "nike",
        "description": "Marca esportiva internacional",
        "image": "https://exemplo.com/logo-nike.png"
      }
    }
  ]
}
```

## Exemplo de Resposta — Consultar Marca por ID

```json
{
  "Brand": {
    "id": "1",
    "name": "Nike",
    "slug": "nike",
    "description": "Marca esportiva internacional",
    "image": "https://exemplo.com/logo-nike.png"
  }
}
```

## Boas Práticas

1. **Crie marcas antes dos produtos** — ao cadastrar produtos, o `brand_id` deve referenciar uma marca existente
2. **Use slugs descritivos** — o slug é usado na URL da página de marca na vitrine; mantenha-o limpo e legível
3. **Evite duplicidade** — consulte a listagem antes de criar para evitar marcas duplicadas
4. **Imagem da marca** — forneça uma URL pública e acessível para o logotipo; formatos recomendados: PNG ou JPG
5. **Exclusão segura** — não exclua marcas que possuam produtos associados; reatribua os produtos antes

## Como Usar no Claude Code

### Exemplos de Prompt

- "cadastra as marcas Nike, Adidas e Puma com seus logos"
- "lista todas as marcas disponíveis na loja"
- "verifica se a marca Samsung já existe antes de criar"
- "atualiza o logo e a descrição da marca ID 10"

### O que o Claude faz

1. Gera o código de criação com wrapper `Brand` e slug automático
2. Inclui verificação de duplicidade via `GET /products/brands?name=...` antes de criar
3. Monta o payload com nome, slug, descrição e URL do logo
4. Explica que o `brand_id` retornado deve ser usado ao cadastrar produtos

### O que você recebe

- Código de criação de marca com wrapper `{"Brand": {...}}` correto
- Verificação de duplicidade antes de criar
- `brand_id` extraído da resposta para uso em produtos
- Código de listagem com paginação

### Pré-requisitos

- `access_token` configurado
- URLs públicas dos logos (opcional, mas recomendado)
