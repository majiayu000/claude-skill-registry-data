---
name: tray-webhooks
description: >
  Sistema de Notificação (Webhook) da Tray. Utilize quando o desenvolvedor
  precisar implementar notificações em tempo real para alterações em produtos,
  pedidos, clientes, variações e configurações da loja. Inclui todos os escopos
  suportados, formato de payload, lógica de retry e boas práticas de implementação.
when_to_use: >
  Use quando o desenvolvedor mencionar: webhook, notificação, evento, listener,
  endpoint receptor, escopo de notificação, product_stock, order_insert,
  payload x-www-form-urlencoded, retry de notificação ou sincronização em tempo real.
---

# Sistema de Notificação (Webhook) — API Tray

Documentação oficial: https://developers.tray.com.br/#apis-de-sistema-de-notificacao-webhook

## Ativação

Os webhooks devem ser ativados via **ticket de suporte da Tray**, informando a URL do endpoint receptor do seu aplicativo.

## Escopos Suportados

| Escopo | Ações | Descrição |
|:--|:--|:--|
| `product` | insert, update, delete | Criação, atualização ou exclusão de produto |
| `product_price` | update | Alteração de preço de produto |
| `product_stock` | update | Alteração de estoque de produto |
| `variant` | insert, update, delete | Criação, atualização ou exclusão de variação |
| `variant_price` | update | Alteração de preço de variação |
| `variant_stock` | update | Alteração de estoque de variação |
| `order` | insert, update | Criação ou atualização de pedido |
| `customer` | insert, update, delete | Criação, atualização ou exclusão de cliente |
| `store_config` | update | Alteração de configuração da loja (inclui ativação de MultiCD) |

> **Ativação de escopos:** por padrão, a Tray libera apenas o escopo `order`. Para habilitar outros escopos, abra um chamado no suporte Tray informando a URL de notificação e os escopos desejados.

> **Sobre pagamentos:** **não existe escopo de webhook `payment`**. Notificações de pagamento chegam via escopo `order` — o objeto de pedido retornado pela API contém o campo `payments_notification` com a URL e os dados de pagamento. Consulte o skill `tray-pagamentos` para detalhes.

## Formato do Payload

O webhook envia um POST com `Content-Type: application/x-www-form-urlencoded` — **sempre**, incluindo os de MultiCD.

| Campo | Tipo | Descrição |
|:--|:--|:--|
| `seller_id` | integer | ID da loja que disparou o evento |
| `scope_id` | integer | ID do recurso afetado (ex: ID do produto) |
| `scope_name` | string | Nome do escopo (ex: `product`, `order`) |
| `act` | string | Ação realizada: `insert`, `update` ou `delete` |
| `app_code` | string | Código do aplicativo que recebe a notificação |
| `url_notification` | string | URL de notificação cadastrada no aplicativo |

**Exemplo de payload completo:**

```
seller_id=391250&scope_id=4375797&scope_name=order&act=update&app_code=718&url_notification=https://suaurldenotificacao
```

**Leitura em PHP:**

```php
$sellerID  = $_POST["seller_id"];
$scopeName = $_POST["scope_name"];
$scopeID   = $_POST["scope_id"];
$act       = $_POST["act"];

switch ($scopeName . "_" . $act) {
    case "product_insert":
    case "product_update":
        $productID = $scopeID;
        break;
    case "order_insert":
    case "order_update":
        $orderID = $scopeID;
        break;
    case "customer_delete":
        $customerID = $scopeID;
        break;
}
```

## Lógica de Retry

- Se o endpoint retornar **qualquer código diferente de 200**, a Tray reenvia a notificação
- O reenvio segue **backoff progressivo** (intervalos crescentes entre tentativas)
- A Tray mantém as notificações por até **20 dias** após a desinstalação do app

## Webhook com MultiCD

Quando o MultiCD está ativo na loja, os webhooks de `product_stock` e `variant_stock` são disparados para alterações de estoque em qualquer centro de distribuição.

## Boas Práticas

1. **Responda rápido** — retorne HTTP 200 imediatamente, antes de processar o evento
2. **Processamento assíncrono** — coloque o evento em uma fila e processe em background
3. **Idempotência** — trate notificações duplicadas (o mesmo evento pode chegar mais de uma vez)
4. **Validação** — valide o `seller_id` para confirmar que o evento pertence à loja esperada
5. **Consulta complementar** — após receber o webhook, consulte a API para obter dados atualizados do recurso
6. **Logs** — registre todos os webhooks recebidos para debug e auditoria

## Exemplo de Endpoint Receptor

Ao receber um webhook, seu endpoint deve:

1. Responder HTTP 200 imediatamente
2. Extrair `scope_name`, `scope_id` e `act` do payload
3. Se necessário, consultar a API Tray para obter dados completos
4. Processar a alteração na sua aplicação

## Como Usar no Claude Code

### Exemplos de Prompt

- "implementa um endpoint receptor de webhooks da Tray em Node.js"
- "cria a lógica de processamento para os eventos order_insert e order_update"
- "como configuro meu app para receber notificações de estoque em tempo real?"
- "implementa tratamento de webhooks com fila assíncrona e idempotência"

### O que o Claude faz

1. Gera o endpoint receptor com leitura do payload `x-www-form-urlencoded`
2. Implementa o switch por `scope_name + "_" + act` para rotear eventos
3. Adiciona resposta imediata HTTP 200 + processamento assíncrono via fila
4. Inclui validação do `seller_id` e tratamento de duplicatas (idempotência)

### O que você recebe

- Endpoint receptor com parsing correto de `application/x-www-form-urlencoded`
- Switch de roteamento por evento (order_insert, product_stock, customer_update, etc.)
- Lógica de resposta rápida + processamento em background
- Handler de idempotência para evitar processamento duplicado

### Pré-requisitos

- URL de endpoint publicamente acessível (HTTPS recomendado)
- Ativação do webhook via ticket de suporte Tray informando a URL
- `access_token` configurado para chamadas complementares à API
