---
name: tray-newsletter
description: >
  API de Newsletter da Tray. Utilize quando o desenvolvedor precisar
  gerenciar assinaturas de newsletter da loja, incluindo listagem de assinantes,
  inscrição e confirmação de cadastro.
---

# API de Newsletter — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-newsletter

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/newsletters` | Listagem de assinantes da newsletter |
| POST | `/newsletters` | Cadastrar assinante |
| POST | `/newsletters/confirm` | Confirmar cadastro de newsletter |

**Autenticação:** `?access_token={token}`

## Exemplo de Inscrição

```json
{
  "Newsletter": {
    "email": "cliente@exemplo.com",
    "name": "João Silva"
  }
}
```

## Fluxo de Inscrição

1. `POST /newsletters` — cadastra o e-mail
2. `POST /newsletters/confirm` — confirma a inscrição (double opt-in)

## Paginação

`limit` (máximo 50, padrão 30), `page`.

## Boas Práticas

1. **LGPD** — obtenha consentimento explícito antes de inscrever
2. **Double opt-in** — use o endpoint de confirmação para validar o e-mail

## Como Usar no Claude Code

### Exemplos de Prompt

- "inscreve um cliente na newsletter com double opt-in"
- "lista todos os assinantes da newsletter da loja"
- "implementa o fluxo completo de inscrição com confirmação por e-mail"

### O que o Claude faz

1. Gera o código de inscrição com wrapper `Newsletter` (nome + e-mail)
2. Gera o código de confirmação via `POST /newsletters/confirm`
3. Explica o fluxo double opt-in e a obrigatoriedade de consentimento (LGPD)

### O que você recebe

- Código de inscrição com `{"Newsletter": {"email": "...", "name": "..."}}`
- Código de confirmação double opt-in
- Listagem de assinantes com paginação

### Pré-requisitos

- `access_token` configurado
- Consentimento explícito do usuário (LGPD)
