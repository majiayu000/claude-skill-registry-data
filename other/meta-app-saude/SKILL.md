---
name: meta-app-saude
description: Checagem de saúde dos apps de desenvolvedor da Meta (os seus apps de WhatsApp, rastreamento etc.) pelo MCP de tecnologias sociais da Meta (DevTools). Use quando o usuário perguntar se os apps estão ok, se tem pendência de conformidade, risco de perder acesso, limite de chamadas (rate limit), depreciação de versão da Graph API, novidades no changelog, assinaturas de webhook dos apps, ou para pesquisar a documentação oficial da Meta.
---

# Saúde dos apps Meta (DevTools)

Os apps mudam (nome, status, permissões). Sempre reler com `devtools_app_list`.

## Checagem mensal (só leitura)
1. `devtools_app_list` (`action=list`): lista dos apps, papel do usuário, permissões, status (restrito ou desativado aparece aqui).
2. Para cada app:
   - `devtools_compliance` (`action=status`): ações obrigatórias, violações, recomendações. **Pendência de conformidade não resolvida leva a app restrito.**
   - `devtools_api_usage` (`action=rate_limits`): `overall_status` (healthy, warning ≥70, critical ≥90, throttled).
   - `devtools_api_usage` (`action=deprecations`): versões e campos em depreciação, com o guia de migração. Cruzar com a versão da Graph API usada no seu rastreador e no seu backend (procurar `graph.facebook.com/v` no código).
   - `devtools_webhook_list` (`action=list_subscriptions`): tópicos e campos assinados.
   - `whatsapp_biz_publish_app`: publicado ou em desenvolvimento (só para apps de WhatsApp).
3. **Novidades:**
   - `devtools_api_changelog` (`action=get_changelog_url`, `product=business-messaging` e `ads-commerce`);
   - ler a página do changelog (WebFetch) e destacar o que afeta WhatsApp, CAPI ou Marketing API.
4. **Dúvidas técnicas:** `devtools_discovery` (`action=search_docs`, `query`, `max_results` de 3 a 6). As respostas podem ser grandes: extrair só o trecho útil.

## Leituras sensíveis (só com autorização explícita)
- `devtools_app` (`basic_settings`, `advanced_settings`, `security`) e `devtools_app_review` (`privileges` etc.) podem trazer dados como o segredo do app.
- Se o usuário autorizar, mostrar só o necessário e **nunca** gravar segredo em nota ou memória.

## Alterações (com OK, via `confirm_token`)
- `devtools_webhook_manage`: subscribe, unsubscribe, update_fields. Para o WhatsApp, preferir a skill `wa-webhook`.
- `devtools_webhook_test`: envia um payload de teste para a URL.
