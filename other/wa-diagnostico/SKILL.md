---
name: wa-diagnostico
description: Diagnóstico completo (só leitura) do WhatsApp oficial de uma BM pelo MCP do WhatsApp Business e pelo MCP de Apps da Meta. Use quando o usuário perguntar como está o WhatsApp de uma BM ou cliente, o que falta configurar, por que as mensagens ou webhooks não chegam, se o número está pronto, se tem pagamento, se o app está publicado ou se a empresa é verificada.
---

# Diagnóstico do WhatsApp oficial de uma BM

**Só leitura. Nada aqui altera a Meta.**
- Para olhar o webhook, usar `whatsapp_biz_onboarding_status`.
- **Nunca** usar `whatsapp_biz_configure_webhooks` ou `whatsapp_biz_subscribe_webhook` para "ver como está": eles alteram.

## Passo a passo
1. **Escolher a BM:** `whatsapp_biz_businesses` (`action=list`).
   - Mostrar a lista e confirmar a BM com o usuário, mesmo que pareça óbvio.
   - Se `profile_complete=false`: só passar o `complete_profile_url` e o `profile_note`. Não listar os campos que faltam.
   - Se `prerequisites_met=false`: passar o `blocked_by` como veio, junto com o `readiness_detail` e o `fix_url`, e parar.
2. **Checklist oficial:** `whatsapp_biz_onboarding_status` com o `business_id`.
   - Passar `app_id` se a BM tiver mais de um app.
   - Passar `phone_number_id` quando a pergunta for sobre um número.
   - Mostrar os passos **na ordem devolvida**, com status `done`, `todo`, `unknown` ou `info`.
   - `unknown` = não deu para ler. Não é o mesmo que "não feito".
3. **Números:** `whatsapp_biz_phone_numbers`. Para cada número: `status` (linked/pending), `onboarding_state` e `next_action`.
4. **Contas do WhatsApp:** `whatsapp_biz_accounts`, ou com `phone_number_id` para descobrir a conta de um número.
5. **Pagamento:** `whatsapp_biz_configure_payments` (só consulta + link do Billing Hub). Sem pagamento, as mensagens cobradas são aceitas e **não chegam**.
6. **Publicação do app:** `whatsapp_biz_publish_app` (só consulta + link do Go Live).
7. **Verificação da empresa:** `whatsapp_biz_verify_business` (só consulta + link da Central de Segurança).
8. **Saúde do app:**
   - `devtools_compliance` (`action=status`, `app_id`);
   - `devtools_webhook_list` (`action=list_subscriptions`, `app_id`).

## Como responder
- Checklist na ordem, com a próxima ação = o primeiro `todo`.
- Webhook só funciona com **três** coisas ao mesmo tempo: URL configurada + conta inscrita + app publicado.
- Ações que são do usuário no painel (pagamento, verificação, publicação, token) vão com o link exato devolvido pela ferramenta. Nunca escrever URL de memória.
- Não chamar a BM de "pronta": `prerequisites_met=true` só diz que os checks visíveis passaram.
