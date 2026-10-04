---
name: tray-autorizacao
description: >
  Autenticação e autorização na API da Tray. Utilize quando o desenvolvedor
  precisar implementar o fluxo OAuth 2.0, gerar chaves de acesso (access_token),
  renovar tokens expirados via refresh_token, ou tratar erros de autenticação
  na plataforma Tray. Inclui o fluxo completo de 3 etapas, campos de resposta,
  tempos de expiração e códigos de erro.
when_to_use: >
  Use quando o desenvolvedor mencionar: autenticação, OAuth, access_token, refresh_token,
  consumer_key, consumer_secret, erro 401, token expirado, como conectar à API da Tray,
  primeiras credenciais, fluxo de autorização ou callback de autenticação.
---

# Autorização — API Tray

Documentação oficial: https://developers.tray.com.br/#autorizacao

## Fluxo OAuth 2.0 (3 etapas)

### Etapa 1 — Redirecionamento

Redirecione o lojista para a tela de autorização da Tray:

```
https://{dominio_loja}/auth.php?response_type=code&consumer_key={consumer_key}&callback={callback_url}
```

**Parâmetros:**
- `response_type` — sempre `code`
- `consumer_key` — chave do aplicativo (obtida ao criar o app na Tray)
- `callback` — URL de retorno do seu aplicativo

### Etapa 2 — Callback

Após o lojista autorizar, a Tray redireciona para sua `callback` com os parâmetros:

| Parâmetro | Descrição |
|:--|:--|
| `code` | Código de autorização (uso único) |
| `adm_user` | Identificador do usuário administrativo |
| `store` | URL da loja |
| `api_address` | Endereço base da API para esta loja |

### Etapa 3 — Gerar Chaves de Acesso

**Endpoint:** `POST https://{api_address}/auth`

**Parâmetros do body (JSON):**

| Campo | Tipo | Obrigatório | Descrição |
|:--|:--|:--|:--|
| `consumer_key` | string | Sim | Chave do aplicativo |
| `consumer_secret` | string | Sim | Segredo do aplicativo |
| `code` | string | Sim | Código recebido no callback |

**Resposta de sucesso (201):**

```json
{
  "code": 201,
  "message": "Created tokens",
  "access_token": "xxxxxxxxxxxxx",
  "refresh_token": "xxxxxxxxxxxxx",
  "date_expiration_access_token": "2026-03-21 15:00:00",
  "date_expiration_refresh_token": "2026-04-20 12:00:00",
  "date_activated": "2026-03-21 12:00:00",
  "api_host": "https://{api_address}/",
  "store_id": "123456"
}
```

## Renovar Chave de Acesso

**Endpoint:** `GET https://{api_address}/auth?refresh_token={refresh_token}`

**Resposta de sucesso (200):**

```json
{
  "code": 200,
  "message": "Refreshed tokens",
  "access_token": "novo_access_token",
  "refresh_token": "novo_refresh_token",
  "date_expiration_access_token": "2026-03-21 18:00:00",
  "date_expiration_refresh_token": "2026-04-20 15:00:00",
  "store_id": "123456"
}
```

## Expiração de Tokens

| Token | Expiração | Ação necessária |
|:--|:--|:--|
| `access_token` | **3 horas** | Renovar via `refresh_token` antes de expirar |
| `refresh_token` | **30 dias** | Requer nova autorização completa se expirar |

## Autenticação nas Requisições

Todas as chamadas à API (exceto rotas públicas) exigem o `access_token` como query parameter:

```
GET https://{api_address}/products?access_token={access_token}
POST https://{api_address}/products?access_token={access_token}
```

## Códigos de Erro de Autenticação

| Código | Situação | Ação recomendada |
|:--|:--|:--|
| `1000` | Token expirado, loja ativa | Renovar via refresh_token |
| `1001` | Token expirado, loja bloqueada | Verificar status com o lojista |
| `1002` | Token expirado, loja inativa | Verificar ativação da loja |
| `1003` | Token expirado, loja cancelada | Loja não está mais disponível |
| `1099` | Token inválido ou expirado (motivo desconhecido) | Verificar token e refazer autenticação |

> **Nota:** o campo retornado pela API é `error_code` (não `code`). Validado em teste real: token inválido retorna `error_code: 1099` com HTTP 401.

**Resposta de erro (401):**

```json
{
  "code": 401,
  "message": "Unauthorized",
  "causes": ["Token expired or invalid"]
}
```

## Limites de Requisições

| Tipo | Limite |
|:--|:--|
| Curto prazo | 180 requisições por minuto |
| Diário (padrão) | 10.000 requisições por dia |
| Diário (corporate) | 50.000 requisições por dia |

**Resposta de limite excedido (429):**
A API retorna HTTP 429 quando o limite é atingido. Implemente backoff exponencial.

## Boas Práticas

1. **Nunca hardcode tokens** — use variáveis de ambiente (`TRAY_ACCESS_TOKEN`, `TRAY_CONSUMER_KEY`, `TRAY_CONSUMER_SECRET`)
2. **Renove antes de expirar** — agende renovação antes das 3 horas (ex: a cada 2h30)
3. **Trate todos os códigos** — implemente tratamento para códigos 1000, 1001, 1002, 1003 e 1099
4. **Backoff exponencial** — para erros 429, aguarde progressivamente (1s, 2s, 4s, 8s...)
5. **Armazene o api_address** — ele é específico por loja e retornado no callback

## Como Usar no Claude Code

### Exemplos de Prompt

- "implementa o fluxo OAuth completo com a API da Tray"
- "como conecto minha aplicação à Tray pela primeira vez?"
- "adiciona renovação automática do access_token antes de expirar"
- "como trato o erro 1099 da Tray na autenticação?"

### O que o Claude faz

1. Explica o fluxo OAuth 2.0 de 3 etapas (redirecionamento → callback → geração de tokens)
2. Gera o código de autenticação na linguagem e framework do projeto
3. Implementa a lógica de renovação automática via `refresh_token` antes das 3 horas
4. Adiciona tratamento específico para cada código de erro (1000–1003, 1099)
5. Documenta as variáveis de ambiente necessárias

### O que você recebe

- Código funcional do fluxo OAuth pronto para integrar
- Helper ou middleware de renovação automática de tokens
- Handler com os 5 códigos de erro de autenticação mapeados
- Exemplo de `.env` com todas as variáveis necessárias

### Pré-requisitos

- `consumer_key` e `consumer_secret` do seu app na Tray (obtidos no painel de parceiros)
- URL de callback configurada e acessível publicamente
