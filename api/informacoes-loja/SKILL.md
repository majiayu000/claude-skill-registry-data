---
name: tray-informacoes-loja
description: >
  API de Informações da Loja da Tray. Utilize quando o desenvolvedor
  precisar consultar dados de configuração da loja como nome, domínio, CNPJ,
  endereço, plano contratado e status da loja.
---

# API de Informações da Loja — Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-informacoes-da-loja

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/store` | Consultar informações da loja |

**Autenticação:** `?access_token={token}`

## Dados Retornados

O endpoint retorna informações gerais da loja:

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `id` | number | ID da loja |
| `name` | string | Nome da loja |
| `domain` | string | Domínio principal |
| `cnpj` | string | CNPJ da empresa |
| `address` | string | Endereço completo |
| `city` | string | Cidade |
| `state` | string | Estado (UF) |
| `zip_code` | string | CEP |
| `phone` | string | Telefone |
| `email` | string | E-mail de contato |
| `plan` | string | Plano contratado |
| `status` | string | Status da loja (ativa, bloqueada, inativa, cancelada, suspensa) |
| `currency` | string | Moeda (ex: BRL) |
| `language` | string | Idioma |
| `logo` | string | URL do logo |
| `created_at` | datetime | Data de criação |

## Uso Recomendado

Este endpoint é ideal para:

1. **Primeira chamada de teste** — após obter o `access_token`, use `GET /store` para validar que a autenticação funcionou
2. **Dados de configuração** — obter informações da loja para configurar sua integração
3. **Verificação de status** — confirmar que a loja está ativa antes de realizar operações

## Exemplo de Resposta

```json
{
  "Store": {
    "id": "123456",
    "name": "Minha Loja",
    "domain": "minhaloja.com.br",
    "status": "active",
    "plan": "professional",
    "currency": "BRL"
  }
}
```

## Como Usar no Claude Code

### Exemplos de Prompt

- "valida se minha autenticação com a Tray está funcionando"
- "consulta os dados da loja para configurar minha integração"
- "verifica o status e o plano contratado da loja"

### O que o Claude faz

1. Gera o código para `GET /store?access_token={token}`
2. Extrai os campos relevantes da resposta (status, plano, domínio)
3. Inclui verificação de `status === "active"` antes de prosseguir com operações

### O que você recebe

- Código de consulta de dados da loja
- Verificação de status ativo
- Extração dos dados de configuração necessários para a integração

### Pré-requisitos

- `access_token` configurado (use `tray-autorizacao` primeiro)
