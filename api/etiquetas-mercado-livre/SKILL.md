---
name: tray-etiquetas-mercado-livre
description: >
  API de Etiquetas do Mercado Livre da Tray. Utilize quando o desenvolvedor
  precisar consultar etiquetas de envio geradas pelo Mercado Livre para pedidos
  originados neste marketplace.
---

# API de Etiquetas do Mercado Livre — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-etiqueta-do-mercado-livre

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/mercado-livre/labels` | Consultar etiquetas do Mercado Livre |

**Autenticação:** `?access_token={token}`

## Uso

Este endpoint permite consultar as etiquetas de envio geradas automaticamente pelo Mercado Livre para pedidos originados neste marketplace e integrados à loja Tray.

## Exemplo

```http
GET /mercado-livre/labels?access_token={token}
```

## Observação

Somente leitura. As etiquetas são geradas pelo Mercado Livre e não podem ser criadas via API Tray.

## Como Usar no Claude Code

### Exemplos de Prompt

- "consulta as etiquetas de envio dos pedidos do Mercado Livre"
- "implementa a sincronização de etiquetas ML para impressão em lote"
- "busca a etiqueta de envio do pedido ML ID 98765"

### O que o Claude faz

1. Gera o código de consulta para `GET /mercado-livre/labels`
2. Explica que as etiquetas são somente leitura (geradas pelo ML)
3. Orienta sobre como usar as etiquetas retornadas para impressão

### O que você recebe

- Código de consulta de etiquetas com filtros disponíveis
- Orientação sobre o fluxo de etiquetas geradas pelo Mercado Livre
- Exemplo de integração para impressão em lote

### Pré-requisitos

- `access_token` configurado
- Integração com Mercado Livre ativa na loja Tray
