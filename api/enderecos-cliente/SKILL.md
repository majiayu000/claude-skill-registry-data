---
name: tray-enderecos-cliente
description: >
  API de Endereços de Clientes da Tray. Utilize quando o desenvolvedor
  precisar gerenciar os endereços cadastrados dos clientes, incluindo listagem,
  consulta individual, criação e exclusão. Suporta endereços de entrega e cobrança,
  com campos completos do padrão brasileiro (CEP, bairro, cidade, estado, complemento).
---

# API de Endereços de Clientes — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-clientes

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/customers/:customer_id/addresses` | Listar endereços de um cliente |
| GET | `/customers/:customer_id/addresses/:id` | Consultar endereço específico por ID |
| POST | `/customers/:customer_id/addresses` | Cadastrar novo endereço para o cliente |
| DELETE | `/customers/:customer_id/addresses/:id` | Excluir endereço do cliente |

**Autenticação:** `?access_token={token}` em todas as chamadas.

## Campos do Endereço

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `id` | number | — | ID do endereço (retornado pela API) |
| `customer_id` | number | — | ID do cliente (definido na URL) |
| `recipient` | string | Sim | Nome do destinatário |
| `street` | string | Sim | Nome da rua/logradouro |
| `number` | string | Sim | Número do endereço |
| `complement` | string | Não | Complemento (apto, bloco, sala) |
| `neighborhood` | string | Sim | Bairro |
| `city` | string | Sim | Cidade |
| `state` | string | Sim | Estado (sigla UF, ex: "SP", "RJ") |
| `zipcode` | string | Sim | CEP (formato: "01001000" — apenas números) |
| `country` | string | Não | País (padrão: "Brasil") |
| `type` | string | Não | Tipo do endereço: "delivery" (entrega) ou "billing" (cobrança) |
| `is_default` | number | Não | 1 = endereço padrão, 0 = endereço secundário |

## Paginação

| Parâmetro | Descrição |
|:--|:--|
| `limit` | Itens por página (máximo **50**, padrão **30**) |
| `page` | Número da página |

## Corpo da Requisição (POST)

```json
{
  "Address": {
    "recipient": "João Silva",
    "street": "Rua Augusta",
    "number": "1500",
    "complement": "Apto 42",
    "neighborhood": "Consolação",
    "city": "São Paulo",
    "state": "SP",
    "zipcode": "01304001",
    "country": "Brasil",
    "type": "delivery",
    "is_default": 1
  }
}
```

## Respostas

| Operação | Código | Mensagem |
|:--|:--|:--|
| Criação | 201 | `{"message": "Created", "id": 200, "code": 201}` |
| Exclusão | 200 | `{"message": "Deleted", "id": 200, "code": 200}` |

## Exemplo de Resposta — Listar Endereços

```json
{
  "Addresses": [
    {
      "Address": {
        "id": "200",
        "customer_id": "50",
        "recipient": "João Silva",
        "street": "Rua Augusta",
        "number": "1500",
        "complement": "Apto 42",
        "neighborhood": "Consolação",
        "city": "São Paulo",
        "state": "SP",
        "zipcode": "01304001",
        "country": "Brasil",
        "type": "delivery",
        "is_default": "1"
      }
    }
  ]
}
```

## Exemplo de Resposta — Consultar Endereço por ID

```json
{
  "Address": {
    "id": "200",
    "customer_id": "50",
    "recipient": "João Silva",
    "street": "Rua Augusta",
    "number": "1500",
    "complement": "Apto 42",
    "neighborhood": "Consolação",
    "city": "São Paulo",
    "state": "SP",
    "zipcode": "01304001",
    "country": "Brasil",
    "type": "delivery",
    "is_default": "1"
  }
}
```

## Boas Práticas

1. **CEP apenas números** — envie o CEP sem pontos ou traços (ex: "01304001" e não "01304-001")
2. **Estado em sigla** — use a sigla de 2 letras da UF (ex: "SP", "RJ", "MG")
3. **Endereço padrão** — ao definir `is_default: 1`, esse passa a ser o endereço principal do cliente
4. **Tipo do endereço** — diferencie entre endereços de entrega ("delivery") e cobrança ("billing") para checkout correto
5. **Valide o CEP** — antes de cadastrar, valide o CEP via serviço externo (ex: ViaCEP) para garantir dados corretos
6. **Não edite, recrie** — a API não possui endpoint PUT para endereços; para alterar, exclua o antigo e crie um novo
7. **Recursos relacionados** — consulte o skill `tray-clientes` para gerenciar dados do cliente

## Como Usar no Claude Code

### Exemplos de Prompt

- "cadastra o endereço de entrega do cliente 50 em São Paulo"
- "lista todos os endereços do cliente ID 50"
- "implementa o fluxo de cadastro de múltiplos endereços para o cliente"
- "como altero o endereço padrão de um cliente?"

### O que o Claude faz

1. Gera o código de criação com wrapper `Address` e todos os campos obrigatórios
2. Formata o CEP sem pontuação e o estado em sigla UF
3. Explica que não há endpoint PUT — para alterar, deve excluir e recriar
4. Demonstra como definir `is_default: 1` e o `type` (delivery/billing)

### O que você recebe

- Código de criação com `{"Address": {...}}` e formatação correta dos campos
- Código de listagem dos endereços do cliente
- Fluxo de atualização: `DELETE` + novo `POST`
- Exemplo de endereço de entrega e cobrança separados

### Pré-requisitos

- `access_token` configurado
- `customer_id` do cliente já cadastrado via `tray-clientes`
