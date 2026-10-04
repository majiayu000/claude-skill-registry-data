---
name: tray-etiquetas-hub
description: >
  API de Etiquetas do HUB da Tray. Utilize quando o desenvolvedor
  precisar criar ou consultar etiquetas de envio através do sistema HUB
  de integração logística da Tray.
---

# API de Etiquetas do HUB — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-etiquetas-do-hub

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| POST | `/labels` | Criar etiquetas |
| GET | `/labels` | Consultar etiquetas |

**Autenticação:** `?access_token={token}`

## Criação de Etiquetas

```http
POST /labels?access_token={token}
Content-Type: application/json

{
  "Label": {
    "order_id": 12345
  }
}
```

## Consulta de Etiquetas

```http
GET /labels?access_token={token}&order_id=12345
```

## Observação

O sistema HUB é a integração logística interna da Tray para geração centralizada de etiquetas de envio.

## Como Usar no Claude Code

### Exemplos de Prompt

- "gera a etiqueta de envio para o pedido 12345 via HUB da Tray"
- "consulta as etiquetas geradas para o pedido 12345"
- "implementa a geração automática de etiquetas após confirmação de pagamento"

### O que o Claude faz

1. Gera o código de criação de etiqueta com `POST /labels` e o `order_id`
2. Gera o código de consulta com `GET /labels?order_id=...`
3. Orienta sobre o funcionamento do sistema HUB da Tray

### O que você recebe

- Código de criação de etiqueta com wrapper `{"Label": {"order_id": ...}}`
- Código de consulta por pedido
- Orientação sobre integração com o fluxo de pedidos

### Pré-requisitos

- `access_token` configurado
- Loja com HUB logístico ativo na Tray
- `order_id` do pedido com pagamento confirmado
