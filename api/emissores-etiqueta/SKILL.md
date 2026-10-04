---
name: tray-emissores-etiqueta
description: >
  API de Emissores de Etiqueta da Tray. Utilize quando o desenvolvedor
  precisar integrar geração de etiquetas de envio, cadastrando URLs de etiqueta
  e vinculando-as a pedidos.
---

# API de Emissores de Etiqueta — Tray

Documentação oficial: https://developers.tray.com.br/#api-de-emissores-de-etiqueta

## Endpoints

| Método | Endpoint | Descrição |
|:--|:--|:--|
| POST | `/label-emitters` | Cadastrar URL da etiqueta |
| POST | `/label-emitters/:order_id` | Vincular URL da etiqueta ao pedido |
| DELETE | `/label-emitters/:id` | Excluir URL da etiqueta |

**Autenticação:** `?access_token={token}`

## Fluxo de Uso

1. **Cadastrar a URL** — registre a URL base do seu sistema de etiquetas
2. **Vincular ao pedido** — associe a etiqueta gerada a um pedido específico
3. **Excluir** — remova a etiqueta se necessário

## Exemplo de Cadastro

```http
POST /label-emitters?access_token={token}
Content-Type: application/json

{
  "LabelEmitter": {
    "url": "https://meusistema.com/etiquetas"
  }
}
```

## Exemplo de Vinculação ao Pedido

```http
POST /label-emitters/12345?access_token={token}
Content-Type: application/json

{
  "LabelEmitter": {
    "label_url": "https://meusistema.com/etiquetas/pedido-12345.pdf"
  }
}
```

## Como Usar no Claude Code

### Exemplos de Prompt

- "integra meu sistema de etiquetas externo com a Tray"
- "cadastra a URL do meu emissor de etiquetas e vincula ao pedido 12345"
- "implementa o fluxo completo de geração e vinculação de etiquetas ao pedido"

### O que o Claude faz

1. Gera o código de cadastro da URL base do emissor com `POST /label-emitters`
2. Gera o código de vinculação da etiqueta ao pedido com `POST /label-emitters/:order_id`
3. Guia o fluxo de 3 etapas: cadastrar URL → vincular ao pedido → excluir se necessário

### O que você recebe

- Código de cadastro da URL do emissor com wrapper `LabelEmitter`
- Código de vinculação de etiqueta PDF gerada ao pedido
- Código de exclusão via `DELETE /label-emitters/:id`

### Pré-requisitos

- `access_token` configurado
- URL do sistema externo de geração de etiquetas
- `order_id` do pedido para vinculação
