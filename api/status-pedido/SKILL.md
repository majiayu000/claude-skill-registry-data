---
name: tray-status-pedido
description: >
  API de Status de Pedido da Tray. Utilize quando o desenvolvedor precisar
  gerenciar os status personalizados de pedidos da loja, incluindo listagem, consulta
  individual, criação, atualização e exclusão. Permite configurar nome, descrição,
  cores e tipo do status para personalizar o fluxo de pedidos.
---

# API de Status de Pedido — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-status-do-pedido

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/orders/statuses` | Listagem de status de pedido |
| GET | `/orders/statuses/:id` | Consultar dados de um status por ID |
| POST | `/orders/statuses` | Cadastrar novo status de pedido |
| PUT | `/orders/statuses/:id` | Atualizar dados do status |
| DELETE | `/orders/statuses/:id` | Excluir status de pedido |

**Autenticação:** `?access_token={token}` em todas as chamadas.

## Campos do Status de Pedido

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `id` | number | — | ID do status (retornado pela API) |
| `name` | string | Sim | Nome do status (ex: "Aguardando Pagamento", "Enviado") |
| `description` | string | Não | Descrição detalhada do status |
| `background_color` | string | Não | Cor de fundo para exibição no painel (formato hexadecimal, ex: "#FF9900") |
| `font_color` | string | Não | Cor da fonte para exibição no painel (formato hexadecimal, ex: "#FFFFFF") |
| `type` | string | Não | Tipo do status que define o comportamento no fluxo do pedido |

## Tipos de Status

| Tipo | Descrição |
|:--|:--|
| `open` | Pedido aberto/em andamento |
| `closed` | Pedido concluído/finalizado |
| `cancelled` | Pedido cancelado |

## Corpo da Requisição (POST/PUT)

```json
{
  "OrderStatus": {
    "name": "Em Separação",
    "description": "Pedido sendo preparado para envio",
    "background_color": "#3498DB",
    "font_color": "#FFFFFF",
    "type": "open"
  }
}
```

## Respostas

| Operação | Código | Mensagem |
|:--|:--|:--|
| Criação | 201 | `{"message": "Created", "id": 15, "code": 201}` |
| Atualização | 200 | `{"message": "Saved", "id": 15, "code": 200}` |
| Exclusão | 200 | `{"message": "Deleted", "id": 15, "code": 200}` |

## Exemplo de Resposta — Listar Status

```json
{
  "OrderStatuses": [
    {
      "OrderStatus": {
        "id": "1",
        "name": "Aguardando Pagamento",
        "description": "Pedido criado, aguardando confirmação de pagamento",
        "background_color": "#F39C12",
        "font_color": "#FFFFFF",
        "type": "open"
      }
    },
    {
      "OrderStatus": {
        "id": "2",
        "name": "Pago",
        "description": "Pagamento confirmado",
        "background_color": "#27AE60",
        "font_color": "#FFFFFF",
        "type": "open"
      }
    },
    {
      "OrderStatus": {
        "id": "3",
        "name": "Enviado",
        "description": "Pedido despachado para entrega",
        "background_color": "#2980B9",
        "font_color": "#FFFFFF",
        "type": "open"
      }
    }
  ]
}
```

## Status Padrão da Plataforma

A Tray já possui status padrão pré-configurados que não podem ser excluídos. Você pode criar status personalizados adicionais para atender ao fluxo específico da loja.

## Boas Práticas

1. **Não exclua status em uso** — verifique se há pedidos vinculados ao status antes de excluí-lo
2. **Use cores contrastantes** — garanta que a `font_color` tenha contraste adequado com a `background_color` para boa legibilidade
3. **Defina o tipo correto** — o `type` impacta o comportamento do pedido na plataforma; use `open` para pedidos em andamento, `closed` para finalizados e `cancelled` para cancelados
4. **Nomeie de forma clara** — o nome do status é exibido para o cliente no acompanhamento do pedido
5. **Status padrão** — os status padrão da plataforma não podem ser editados ou excluídos; crie novos para personalizar
6. **Webhook** — ao alterar o status de um pedido, o webhook `order` é disparado automaticamente

## Como Usar no Claude Code

### Exemplos de Prompt

- "cria os status personalizados: Em Separação, Aguardando Retirada e Despachado"
- "lista todos os status de pedido disponíveis na loja"
- "atualiza a cor e descrição do status ID 15"
- "como configuro o fluxo de status para uma loja com retirada em loja?"

### O que o Claude faz

1. Gera o código de criação com wrapper `OrderStatus` e cores em hexadecimal
2. Define o `type` correto para cada status (open/closed/cancelled)
3. Explica os status padrão da plataforma que não podem ser modificados
4. Sugere um fluxo de status adequado ao caso de uso descrito

### O que você recebe

- Código de criação de status com nome, cores e tipo configurados
- Sequência de criação para um fluxo de status completo
- Listagem dos status existentes via `GET /orders/statuses`
- Nota sobre status padrão da plataforma vs. personalizados

### Pré-requisitos

- `access_token` configurado
