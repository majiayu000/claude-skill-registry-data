---
name: tray-notas-fiscais
description: >
  API de Notas Fiscais (NF-e) da Tray. Utilize quando o desenvolvedor
  precisar gerenciar notas fiscais eletrônicas associadas a pedidos, incluindo
  listagem geral, consulta por ID, consulta por pedido, criação e atualização.
  Inclui campos como número, série, chave de acesso, CFOP, link do DANFE e
  valor total, essenciais para integração com ERPs e sistemas fiscais.
---

# API de Notas Fiscais (NF-e) — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-nota-fiscal

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/invoices` | Listagem de notas fiscais com paginação e filtros |
| GET | `/invoices/:id` | Consultar nota fiscal por ID |
| GET | `/orders/:order_id/invoices` | Consultar notas fiscais de um pedido |
| POST | `/orders/:order_id/invoices` | Cadastrar nota fiscal para um pedido |
| PUT | `/invoices/:id` | Atualizar dados da nota fiscal |

**Autenticação:** `?access_token={token}` em todas as chamadas.

## Campos da Nota Fiscal

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `id` | number | — | ID da nota fiscal (retornado pela API) |
| `order_id` | number | — | ID do pedido associado (definido na URL no POST) |
| `number` | string | Sim | Número da nota fiscal |
| `series` | string | Sim | Série da nota fiscal (ex: "1", "001") |
| `issue_date` | date | Sim | Data de emissão (formato: YYYY-MM-DD) |
| `key` | string | Sim | Chave de acesso da NF-e (44 dígitos) |
| `cfop` | string | Não | Código Fiscal de Operações e Prestações (ex: "5102", "6102") |
| `link` | string | Não | URL do DANFE (PDF da nota fiscal) |
| `total_amount` | decimal | Não | Valor total da nota fiscal |
| `created_at` | datetime | — | Data de criação do registro |
| `updated_at` | datetime | — | Data da última atualização |

## Paginação

| Parâmetro | Descrição |
|:--|:--|
| `limit` | Itens por página (máximo **50**, padrão **30**) |
| `page` | Número da página |

**Resposta inclui:** `total`, `page`, `offset`, `limit`, `maxLimit`

## Filtros de Listagem

| Filtro | Tipo | Descrição |
|:--|:--|:--|
| `order_id` | number | Filtrar por ID do pedido |
| `number` | string | Filtrar por número da NF |
| `issue_date` | date | Filtrar por data de emissão |
| `created_at` | date | Filtrar por data de criação |

## Corpo da Requisição — Criar Nota Fiscal (POST)

```json
{
  "Invoice": {
    "number": "000123456",
    "series": "1",
    "issue_date": "2026-03-21",
    "key": "35260312345678000100550010001234561234567890",
    "cfop": "5102",
    "link": "https://exemplo.com/danfe/123456.pdf",
    "total_amount": "299.90"
  }
}
```

## Corpo da Requisição — Atualizar Nota Fiscal (PUT)

```json
{
  "Invoice": {
    "link": "https://exemplo.com/danfe/123456-v2.pdf",
    "total_amount": "310.50"
  }
}
```

## Respostas

| Operação | Código | Mensagem |
|:--|:--|:--|
| Criação | 201 | `{"message": "Created", "id": 500, "code": 201}` |
| Atualização | 200 | `{"message": "Saved", "id": 500, "code": 200}` |

## Exemplo de Resposta — Listar Notas Fiscais

```json
{
  "paging": {
    "total": 150,
    "page": 1,
    "offset": 0,
    "limit": 30,
    "maxLimit": 50
  },
  "Invoices": [
    {
      "Invoice": {
        "id": "500",
        "order_id": "1001",
        "number": "000123456",
        "series": "1",
        "issue_date": "2026-03-21",
        "key": "35260312345678000100550010001234561234567890",
        "cfop": "5102",
        "link": "https://exemplo.com/danfe/123456.pdf",
        "total_amount": "299.90",
        "created_at": "2026-03-21 10:30:00",
        "updated_at": "2026-03-21 10:30:00"
      }
    }
  ]
}
```

## Exemplo de Resposta — Consultar por Pedido

```json
{
  "Invoices": [
    {
      "Invoice": {
        "id": "500",
        "order_id": "1001",
        "number": "000123456",
        "series": "1",
        "issue_date": "2026-03-21",
        "key": "35260312345678000100550010001234561234567890",
        "cfop": "5102",
        "link": "https://exemplo.com/danfe/123456.pdf",
        "total_amount": "299.90"
      }
    }
  ]
}
```

## Chave de Acesso da NF-e

A chave de acesso (`key`) possui 44 dígitos e contém informações codificadas:

| Posição | Tamanho | Descrição |
|:--|:--|:--|
| 1-2 | 2 | Código da UF |
| 3-6 | 4 | Ano e mês de emissão (AAMM) |
| 7-20 | 14 | CNPJ do emitente |
| 21-22 | 2 | Modelo do documento (55 = NF-e) |
| 23-25 | 3 | Série |
| 26-34 | 9 | Número da NF |
| 35-43 | 9 | Código numérico |
| 44 | 1 | Dígito verificador |

## CFOP Comuns no E-commerce

| CFOP | Descrição |
|:--|:--|
| `5102` | Venda de mercadoria (operação interna — mesmo estado) |
| `6102` | Venda de mercadoria (operação interestadual) |
| `5405` | Venda de mercadoria com ST (substituição tributária) — mesmo estado |
| `6404` | Venda de mercadoria com ST — interestadual |

## Boas Práticas

1. **Chave de acesso válida** — a chave deve ter exatamente 44 dígitos numéricos; valide antes de enviar
2. **Link do DANFE** — forneça uma URL pública e acessível para o PDF do DANFE; o cliente pode consultar
3. **Uma NF por pedido** — na maioria dos casos, cada pedido possui uma nota fiscal; porém, pedidos com produtos de CDs diferentes podem ter múltiplas NFs
4. **Data de emissão** — use a data real de emissão da NF no formato YYYY-MM-DD
5. **Integração com ERP** — automatize o envio de NFs via integração com seu ERP após a emissão fiscal
6. **CFOP correto** — use o CFOP adequado para a operação (venda interna vs. interestadual)
7. **Série consistente** — mantenha a série da NF consistente com o emissor fiscal configurado
8. **Recursos relacionados** — consulte o skill `tray-pedidos` para gerenciar pedidos associados

## Como Usar no Claude Code

### Exemplos de Prompt

- "registra a NF-e do pedido 1001 com chave de acesso e link do DANFE"
- "lista todas as notas fiscais emitidas no mês de março"
- "consulta as notas fiscais do pedido ID 2050"
- "implementa a integração de envio automático de NF-e após emissão no ERP"

### O que o Claude faz

1. Gera o código de registro da NF-e com wrapper `Invoice` e todos os campos obrigatórios
2. Valida o formato da chave de acesso (44 dígitos) antes de montar a chamada
3. Usa o endpoint correto `POST /orders/:order_id/invoices` com o `order_id` na URL
4. Inclui filtros de data e `order_id` para listagens

### O que você recebe

- Código de registro de NF-e com todos os campos (número, série, chave, CFOP, DANFE)
- Validação da chave de acesso de 44 dígitos
- Código de consulta por pedido via `GET /orders/:order_id/invoices`
- Exemplo de integração com fluxo de ERP

### Pré-requisitos

- `access_token` configurado
- `order_id` do pedido já existente na Tray
- Dados da NF-e emitida pelo sistema fiscal (número, série, chave de acesso)
