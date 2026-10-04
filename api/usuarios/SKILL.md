---
name: tray-usuarios
description: >
  API de Usuários da Tray. Utilize quando o desenvolvedor precisar
  listar os usuários administrativos da loja. API somente leitura.
---

# API de Usuários — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-usuario

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/users` | Listagem de usuários administrativos da loja |

**Autenticação:** `?access_token={token}`

**Somente leitura** — esta API não permite criação, atualização ou exclusão de usuários.

## Uso

Permite consultar os usuários com acesso administrativo à loja Tray. Útil para identificar responsáveis e configurar permissões na sua integração.

## Como Usar no Claude Code

### Exemplos de Prompt

- "lista os usuários administrativos da loja"
- "quais usuários têm acesso ao painel da loja?"

### O que o Claude faz

1. Gera o código para `GET /users?access_token={token}`
2. Itera pelos usuários retornados para exibição ou auditoria

### O que você recebe

- Código de listagem de usuários administrativos
- Nota de que a API é somente leitura (sem criação/atualização/exclusão)

### Pré-requisitos

- `access_token` configurado
