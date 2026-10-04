---
name: tray-palavras-chave
description: >
  API de Palavras-Chave da Tray. Utilize quando o desenvolvedor precisar
  consultar palavras-chave de SEO associadas à loja. API somente leitura.
---

# API de Palavras-Chave — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-palavras-chave

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/keywords` | Listagem de palavras-chave |
| GET | `/keywords/:id` | Consultar dados de uma palavra-chave |

**Autenticação:** `?access_token={token}`

**Somente leitura** — esta API não permite criação, atualização ou exclusão.

## Paginação

`limit` (máximo 50, padrão 30), `page`.

## Uso

Útil para consultar as palavras-chave de SEO configuradas na loja e integrá-las com ferramentas de marketing e analytics.

## Como Usar no Claude Code

### Exemplos de Prompt

- "lista todas as palavras-chave de SEO da loja"
- "consulta as palavras-chave para integrar com minha ferramenta de analytics"

### O que o Claude faz

1. Gera o código para `GET /keywords` com paginação
2. Extrai as palavras-chave para uso em ferramentas externas de SEO/analytics

### O que você recebe

- Código de listagem de palavras-chave com paginação
- Nota de que a API é somente leitura

### Pré-requisitos

- `access_token` configurado
