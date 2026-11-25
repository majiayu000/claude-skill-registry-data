---
name: wa-webhook
description: Configura e testa o webhook do WhatsApp oficial (Cloud API) para o seu backend, pelo MCP do WhatsApp Business e pelo MCP de Apps da Meta. Use quando o usuário pedir para ligar o webhook, apontar o WhatsApp para o seu backend, não chegam mensagens ou eventos, inscrever uma conta do WhatsApp num app, ou adicionar campos como automatic_events, smb_message_echoes e history.
---

# Webhook do WhatsApp → seu backend

Nos testes reais, as mensagens chegaram ao backend em 1 a 3 segundos.

**Webhook só funciona com três coisas ao mesmo tempo:**
1. **URL** configurada no app (`whatsapp_biz_configure_webhooks`);
2. **conta inscrita** no app (`whatsapp_biz_subscribe_webhook`, uma vez por conta);
3. **app publicado** (Go Live, feito pelo usuário).

## Pré-requisitos
- **O endpoint já precisa responder** ao desafio GET (`hub.mode=subscribe`, `hub.verify_token`, `hub.challenge`), porque a Meta valida a URL na hora de salvar.
  - Testar antes, do servidor: `curl -s "https://SEU-DOMINIO/api/webhooks/whatsapp-cloud?hub.mode=subscribe&hub.verify_token=<TOKEN>&hub.challenge=123"` tem que devolver `123`.
  - Ler o token do `.env` sem imprimir.
- **O verify token** fica no `.env` do seu backend. Não é credencial de acesso, mas não vai para nota nem memória.
- **O segredo do app** precisa estar no `.env` (colado pelo usuário) para o seu backend validar `X-Hub-Signature-256`.

## Passo a passo
1. **Estado atual:** `whatsapp_biz_onboarding_status` com o `business_id` (e o `app_id` se houver mais de um app). É a **única** forma de olhar sem mexer.
2. **Configurar a URL:** `whatsapp_biz_configure_webhooks` com `business_id`, `callback_url` e `verify_token`.
   - **`fields`:** se omitido, a ferramenta **adiciona** o conjunto padrão dela. Se passado, **substitui** a assinatura inteira, então mandar a lista completa:
     - `messages`;
     - `message_template_status_update`;
     - `automatic_events`;
     - `smb_message_echoes`, só se o número estiver em coexistência (é a resposta dada pelo celular).
     - `history` e `smb_app_state_sync` só trazem dados no Embedded Signup de coexistência. Não precisam ser assinados antes disso.
   - 1ª chamada sem `confirm` → resumo ao usuário → OK → `confirm=true`.
   - **Cuidado: sobrescreve a URL atual.** Nunca chamar só para consultar.
3. **Inscrever a conta:** `whatsapp_biz_subscribe_webhook` com `waba_id` (ou `phone_number_id`) e `app_id`.
   - É aditivo: não remove outros apps (ex.: um CRM) que já recebem essa conta.
4. **App publicado?** `whatsapp_biz_publish_app`. Se não estiver, passar o `publish_url` ao usuário.
5. **Conferir pelo DevTools:** `devtools_webhook_list` (`list_subscriptions`) para ver tópico e campos.
6. **Teste:** `devtools_webhook_test` com `topic=whatsapp_business_account` e `field=messages`.
   - Ter sido gravado prova que a assinatura passou, ou seja, o segredo do app no `.env` está certo.
7. **Teste real:** mandar uma mensagem para o número a partir de um celular e ver a conversa aparecer no seu backend. Para o teste de anúncio, clicar num anúncio CTWA e conferir o `ctwa_clid` gravado.

## Problemas comuns
| Sintoma | Causa provável |
|---|---|
| Nada chega | falta inscrição da conta ou o app não está publicado |
| A Meta não salva a URL | o endpoint não respondeu ao desafio ou o verify token não bate |
| Chega e o seu backend recusa | assinatura inválida: segredo do app errado ou o corpo foi alterado antes da validação |
| Duplicados | a Meta reenvia: tratar idempotência por wamid (o backend precisa tratar) |
| Chega mas não aparece no app | o backend não reconhece aquele phone_number_id: conferir o cadastro do número e o log de eventos |
| Mensagens antigas não aparecem | webhook não é retroativo: só entra o que chegou depois da inscrição |

## Reverter
Não há desfazer no MCP. O usuário usa os links de `manage_links` do `onboarding_status` (página de configuração do webhook no painel do app).
