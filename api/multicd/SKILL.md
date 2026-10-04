---
name: tray-multicd
description: >
  API de Multi-CD (Centros de Distribuição) da Tray. Utilize quando o
  desenvolvedor precisar gerenciar múltiplos centros de distribuição, incluindo
  cadastro, atualização, exclusão de CDs, gestão de estoque por produto/variação
  em cada CD, e configuração de prioridade e cobertura regional. Inclui documentação
  de webhooks para sincronização de estoque entre sistemas.
when_to_use: >
  Use quando o desenvolvedor mencionar: MultiCD, multi-cd, centro de distribuição,
  CD, estoque por CD, distribution center, estoque distribuído, /multicd,
  sincronizar estoque entre depósitos ou estoque regionalizado.
---

# API de Multi-CD (Centros de Distribuição) — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-multicd

## Endpoints — Centros de Distribuição

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/multicd/distribution-centers` | Listar centros de distribuição |
| GET | `/multicd/distribution-centers/:id` | Consultar CD por ID |
| POST | `/multicd/distribution-centers` | Cadastrar novo centro de distribuição |
| PUT | `/multicd/distribution-centers/:id` | Atualizar dados do CD |
| DELETE | `/multicd/distribution-centers/:id` | Excluir centro de distribuição |

## Endpoints — Estoque por CD

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/multicd/stock/detailed/product/:id` | Consultar estoque detalhado de produto em todos os CDs |
| GET | `/multicd/stock/detailed/variant/:id` | Consultar estoque detalhado de variação em todos os CDs |
| PUT | `/multicd/distribution-centers/:id/stock` | Atualizar estoque do CD (produto ou variação) |

**Autenticação:** `?access_token={token}` em todas as chamadas.

## Campos do Centro de Distribuição

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `id` | number | — | ID do CD (retornado pela API) |
| `name` | string | Sim | Nome do centro de distribuição (ex: "CD São Paulo", "CD Minas") |
| `zip_code` | string | Sim | CEP do CD (apenas números, ex: "01310100") |
| `address` | string | Sim | Endereço completo do CD |
| `city` | string | Sim | Cidade do CD |
| `state` | string | Sim | Estado/UF do CD (ex: "SP", "MG") |
| `priority` | number | Não | Prioridade do CD (menor número = maior prioridade) |
| `active` | number | Não | 1 = ativo, 0 = inativo |

## Campos do Estoque por CD

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `product_id` | number | — | ID do produto |
| `variant_id` | number | — | ID da variação (quando aplicável) |
| `stock` | number | Sim | Quantidade em estoque no CD |
| `distribution_center_id` | number | — | ID do centro de distribuição |

## Paginação

| Parâmetro | Descrição |
|:--|:--|
| `limit` | Itens por página (máximo **50**, padrão **30**) |
| `page` | Número da página |

**Resposta inclui:** `total`, `page`, `offset`, `limit`, `maxLimit`

## Corpo da Requisição — Criar CD (POST)

```json
{
  "DistributionCenter": {
    "name": "CD São Paulo",
    "zip_code": "01310100",
    "address": "Av. Paulista, 1000",
    "city": "São Paulo",
    "state": "SP",
    "priority": 1,
    "active": 1
  }
}
```

## Corpo da Requisição — Atualizar CD (PUT)

```json
{
  "DistributionCenter": {
    "name": "CD São Paulo - Matriz",
    "priority": 1,
    "active": 1
  }
}
```

## Corpo da Requisição — Atualizar Estoque no CD (PUT)

**Produto:**
```json
{
  "DistributionCenterProduct": {
    "stock": 150
  }
}
```

**Variação:**
```json
{
  "DistributionCenterVariant": {
    "stock": 75
  }
}
```

## Respostas

| Operação | Código | Mensagem |
|:--|:--|:--|
| Criação | 201 | `{"message": "Created", "id": 5, "code": 201}` |
| Atualização | 200 | `{"message": "Saved", "id": 5, "code": 200}` |
| Exclusão | 200 | `{"message": "Deleted", "id": 5, "code": 200}` |

## Exemplo de Resposta — Listar CDs

```json
{
  "paging": {
    "total": 3,
    "page": 1,
    "offset": 0,
    "limit": 30,
    "maxLimit": 50
  },
  "DistributionCenters": [
    {
      "DistributionCenter": {
        "id": "1",
        "name": "CD São Paulo",
        "zip_code": "01310100",
        "address": "Av. Paulista, 1000",
        "city": "São Paulo",
        "state": "SP",
        "priority": "1",
        "active": "1"
      }
    },
    {
      "DistributionCenter": {
        "id": "2",
        "name": "CD Belo Horizonte",
        "zip_code": "30130000",
        "address": "Av. Afonso Pena, 500",
        "city": "Belo Horizonte",
        "state": "MG",
        "priority": "2",
        "active": "1"
      }
    }
  ]
}
```

## Exemplo de Resposta — Estoque por CD

```json
{
  "DistributionCenterProducts": [
    {
      "DistributionCenterProduct": {
        "product_id": "100",
        "stock": "50",
        "distribution_center_id": "1"
      }
    },
    {
      "DistributionCenterProduct": {
        "product_id": "101",
        "stock": "30",
        "distribution_center_id": "1"
      }
    }
  ]
}
```

## Lógica de Seleção do CD

Quando um pedido é realizado, a Tray seleciona o CD com base nos seguintes critérios:

1. **Disponibilidade** — o CD deve ter estoque suficiente para todos os itens
2. **Prioridade** — CDs com menor número de prioridade são preferidos
3. **Proximidade** — o CEP do CD é comparado com o CEP de entrega para otimizar frete e prazo
4. **Status ativo** — apenas CDs com `active: 1` são considerados

## Webhooks de Estoque

Quando o MultiCD está ativo, a Tray dispara webhooks nos escopos `product_stock` e `variant_stock` para qualquer alteração de estoque em qualquer CD, permitindo sincronização em tempo real com ERPs e sistemas externos.

| Evento (`scope_name`) | `act` | Descrição |
|:--|:--|:--|
| `product_stock` | `update` | Estoque de produto alterado em qualquer CD |
| `variant_stock` | `update` | Estoque de variação alterado em qualquer CD |

### Payload do Webhook

O formato é **`application/x-www-form-urlencoded`** (igual a todos os webhooks da Tray):

```
seller_id=391250&scope_id=100&scope_name=product_stock&act=update&app_code=718&url_notification=https://suaurldenotificacao
```

O `scope_id` corresponde ao ID do produto ou variação alterada. Após receber o webhook, consulte `GET /multicd/stock/detailed/product/:id` para obter os estoques atualizados por CD.

> Para detalhes completos sobre formato de payload, campos e lógica de retry, consulte o skill `tray-webhooks`.

## Boas Práticas

1. **CEP do CD é fundamental** — o CEP do CD é usado para calcular frete; informe o CEP correto do endereço físico
2. **Prioridade planejada** — defina prioridades estrategicamente (ex: CD mais central com prioridade 1)
3. **Estoque sincronizado** — mantenha o estoque de cada CD atualizado em tempo real via integração
4. **Estoque total** — o estoque exibido na vitrine é a soma do estoque de todos os CDs ativos
5. **Variações por CD** — se o produto tem variações, gerencie o estoque de cada variação individualmente por CD
6. **Desative antes de excluir** — mude `active` para `0` antes de excluir um CD para evitar impacto em pedidos
7. **Teste o cálculo de frete** — após configurar CDs, teste o frete com diferentes CEPs usando o skill `tray-frete` (`GET /shippings/cotation/`)
8. **Recursos relacionados** — consulte os skills `tray-frete`, `tray-configuracao-frete` e `tray-webhooks`

## Como Usar no Claude Code

### Exemplos de Prompt

- "cadastra os centros de distribuição de SP (prioritário) e MG"
- "atualiza o estoque do produto 100 para 150 unidades no CD de São Paulo"
- "implementa a sincronização de estoque por CD via webhook"
- "consulta o estoque detalhado do produto 100 em todos os CDs"

### O que o Claude faz

1. Gera o código de criação de CD com wrapper `DistributionCenter` e configuração de prioridade
2. Gera o código de atualização de estoque por CD (produto ou variação)
3. Implementa o fluxo de recebimento de webhook `product_stock` e atualização via API
4. Demonstra a consulta de estoque detalhado por CD

### O que você recebe

- Código de criação de CDs com prioridade e cobertura regional
- Código de atualização de estoque: `PUT /multicd/distribution-centers/:id/stock`
- Fluxo de sincronização via webhook `product_stock` + consulta detalhada
- Consulta de estoque por produto em todos os CDs

### Pré-requisitos

- `access_token` configurado
- MultiCD ativo na loja (configurado no painel Tray)
- Produtos já cadastrados com `product_id` disponível
