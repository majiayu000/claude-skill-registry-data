---
name: tray-caracteristicas
description: >
  API de Características de Produtos da Tray. Utilize quando o desenvolvedor
  precisar gerenciar características (propriedades) dos produtos, incluindo cadastro,
  atualização, consulta e exclusão. Permite criar características globais reutilizáveis
  e associar valores específicos a cada produto (ex: cor, tamanho, material, voltagem).
---

# API de Características de Produtos — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-caracteristicas

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/products/:product_id/properties` | Listar características de um produto |
| POST | `/products/:product_id/properties` | Cadastrar ou atualizar característica no produto |
| POST | `/properties` | Criar característica global (reutilizável em vários produtos) |
| DELETE | `/products/:product_id/properties/:id` | Excluir característica de um produto |

**Autenticação:** `?access_token={token}` em todas as chamadas.

## Campos da Característica

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `id` | number | — | ID da característica (retornado pela API) |
| `property` | string | Sim | Nome da característica (ex: "Cor", "Material") |
| `value` | string | Sim | Valor da característica (ex: "Azul", "Algodão") |
| `product_id` | number | Sim | ID do produto associado |

## Campos da Característica Global

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `name` | string | Sim | Nome da característica global |
| `presentation` | string | Não | Tipo de apresentação (ex: "select", "text") |

## Corpo da Requisição — Cadastrar/Atualizar no Produto (POST)

```json
{
  "Property": {
    "property": "Cor",
    "value": "Azul"
  }
}
```

## Corpo da Requisição — Criar Característica Global (POST)

```json
{
  "Property": {
    "name": "Material",
    "presentation": "select"
  }
}
```

## Respostas

| Operação | Código | Mensagem |
|:--|:--|:--|
| Criação | 201 | `{"message": "Created", "id": 123, "code": 201}` |
| Atualização | 200 | `{"message": "Saved", "id": 123, "code": 200}` |
| Exclusão | 200 | `{"message": "Deleted", "id": 123, "code": 200}` |

## Exemplo de Resposta — Listar Características

```json
{
  "Properties": [
    {
      "Property": {
        "id": "1",
        "property": "Cor",
        "value": "Azul",
        "product_id": "123"
      }
    },
    {
      "Property": {
        "id": "2",
        "property": "Material",
        "value": "Algodão",
        "product_id": "123"
      }
    }
  ]
}
```

## Boas Práticas

1. **Use características globais** — crie características globais com `POST /properties` para padronizar nomes e evitar duplicidade
2. **Padronize valores** — mantenha consistência nos valores (ex: sempre "Azul" e nunca "azul" ou "AZUL")
3. **Consulte antes de criar** — verifique as características existentes do produto antes de adicionar novas
4. **Características para filtros** — as características são usadas como filtros na vitrine; escolha nomes claros para o consumidor final
5. **Não confunda com variações** — características são informativas; para opções que geram SKUs diferentes (estoque separado), use variações

## Como Usar no Claude Code

### Exemplos de Prompt

- "adiciona as características Cor, Material e Voltagem ao produto 123"
- "como padronizo características reutilizáveis entre vários produtos?"
- "cria características globais de Material e depois vincula ao produto"
- "lista todas as características do produto 456"

### O que o Claude faz

1. Distingue características globais (reutilizáveis) de características por produto
2. Gera código de criação global via `POST /properties` quando a padronização é necessária
3. Gera código de vínculo com o produto via `POST /products/:id/properties`
4. Inclui o wrapper `Property` correto em cada chamada

### O que você recebe

- Código do fluxo: criar global → vincular ao produto (quando aplicável)
- Código de adição direta de característica a um produto específico
- Exemplos com múltiplas características em sequência
- Consulta de características existentes via `GET /products/:id/properties`

### Pré-requisitos

- Produto já cadastrado com `product_id` disponível
- `access_token` configurado
