---
name: tray-parceiros
description: >
  API de Parceiros da Tray. Utilize quando o desenvolvedor precisar
  gerenciar parceiros/revendedores da loja, incluindo listagem, consulta,
  cadastro, atualização e exclusão.
---

# API de Parceiros — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-parceiros

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/partners` | Listagem de parceiros |
| GET | `/partners/:id` | Consultar dados do parceiro |
| POST | `/partners` | Cadastrar parceiro |
| PUT | `/partners/:id` | Atualizar dados do parceiro |
| DELETE | `/partners/:id` | Excluir parceiro |

**Autenticação:** `?access_token={token}`

## Exemplo de Criação

```json
{
  "Partner": {
    "name": "Parceiro Exemplo",
    "email": "parceiro@exemplo.com"
  }
}
```

## Paginação

`limit` (máximo 50, padrão 30), `page`.

## Como Usar no Claude Code

### Exemplos de Prompt

- "cadastra um parceiro revendedor com nome e e-mail"
- "lista todos os parceiros ativos da loja"
- "atualiza os dados de contato do parceiro ID 10"

### O que o Claude faz

1. Gera o código de criação com wrapper `Partner`
2. Gera o código de listagem e atualização de parceiros existentes
3. Inclui paginação na listagem

### O que você recebe

- Código de criação com `{"Partner": {"name": "...", "email": "..."}}`
- Código de listagem com paginação
- Código de atualização e exclusão

### Pré-requisitos

- `access_token` configurado
