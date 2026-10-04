---
name: tray-informacoes-adicionais
description: >
  API de Informação Adicional da Tray. Utilize quando o desenvolvedor
  precisar gerenciar campos customizados de informação que podem ser vinculados
  a produtos, incluindo criação, atualização, vinculação e exclusão.
---

# API de Informação Adicional — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-informacao-adicional-additional_info

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| GET | `/additional-info` | Listagem geral das informações adicionais |
| GET | `/additional-info/:id` | Consultar dados por ID |
| POST | `/additional-info` | Cadastrar informação adicional |
| PUT | `/additional-info/:id` | Atualizar informação |
| PUT | `/products/:id/additional-info` | Atualizar informações relacionadas ao produto |
| POST | `/products/:id/additional-info` | Vincular informação adicional ao produto |
| DELETE | `/products/:id/additional-info/:info_id` | Excluir relação com produto |
| DELETE | `/additional-info/:id` | Excluir informação adicional |

**Autenticação:** `?access_token={token}`

## Exemplo de Criação

```json
{
  "AdditionalInfo": {
    "name": "Composição",
    "value": "100% Algodão"
  }
}
```

## Vinculação com Produto

Para vincular uma informação adicional a um produto:

```http
POST /products/123/additional-info?access_token={token}
```

```json
{
  "additional_info_id": 456
}
```

## Boas Práticas

1. **Crie antes de vincular** — primeiro crie a informação, depois vincule ao produto
2. **Reutilize** — a mesma informação pode ser vinculada a múltiplos produtos
3. **Paginação** — `limit` (máximo 50, padrão 30), `page`

## Como Usar no Claude Code

### Exemplos de Prompt

- "adiciona o campo Composição com valor '100% Algodão' ao produto 123"
- "como crio informações adicionais reutilizáveis para múltiplos produtos?"
- "vincula a informação adicional ID 45 aos produtos 101, 102 e 103"
- "lista todas as informações adicionais cadastradas"

### O que o Claude faz

1. Gera o código de criação da informação com wrapper `AdditionalInfo`
2. Gera o código de vinculação ao produto via `POST /products/:id/additional-info`
3. Explica quando criar nova informação vs. reutilizar uma existente (via ID)
4. Monta o fluxo completo: criar → vincular para múltiplos produtos quando necessário

### O que você recebe

- Código de criação com `{"AdditionalInfo": {"name": "...", "value": "..."}}`
- Código de vinculação com o `additional_info_id` retornado
- Exemplo de reutilização da mesma informação em múltiplos produtos
- Código de exclusão da relação via `DELETE /products/:id/additional-info/:info_id`

### Pré-requisitos

- Produto já cadastrado com `product_id` disponível
- `access_token` configurado
