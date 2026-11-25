---
name: ads-sinal-conversao
description: Diagnostica a saúde do sinal de conversão (pixel/dataset, CAPI) de um cliente da agência pelo Meta Ads MCP. Use quando o usuário perguntar se o pixel está funcionando, se os eventos do seu rastreador (Lead, Purchase) estão chegando na Meta, qualidade da correspondência (EMQ), volume de eventos, conversões personalizadas, ou quiser criar uma regra de evento sem código no site.
---

# Sinal de conversão (pixel, dataset e CAPI)

**Por que importa:**
- A Meta otimiza pelo que recebe.
- O seu rastreador manda Lead e Purchase por CAPI (servidor) com o pixel de cada cliente.
- Se o sinal chega fraco ou não chega, a campanha otimiza errado.

## Passo a passo (só leitura)
1. **Achar o dataset:** `ads_get_datasets` com `ad_account_id` (ou `business_id`). `ads_get_dataset_details` para o detalhe.
2. **Volume:** `ads_get_dataset_stats` com `aggregation=event`.
   - Repetir com `event_source=SERVER_ONLY`: mostra o que veio do seu rastreador por CAPI.
   - Repetir com `event_source=WEB_ONLY`: mostra o que veio do navegador.
   - Os tempos `start_time` e `end_time` vão em Unix (string). No máximo 28 dias.
   - **Sinalizar evento com volume zero** que uma campanha ativa usa para otimizar.
3. **Qualidade:** `ads_get_dataset_quality`. Ver:
   - EMQ por evento;
   - cobertura das chaves (telefone, e-mail, `external_id`, fbc/fbp);
   - atualização do envio.
   - EMQ baixo no servidor = o seu rastreador está mandando poucas chaves. Proposta: incluir telefone com hash e `external_id`.
4. **Conversões personalizadas:** `ads_get_customconversions`.

## Criar regra de evento sem código (com o OK do usuário)
- `ads_pixel_event_create` com `items`: `pixel_id`, `event_type` padrão (Lead, Purchase...), `rule_type` (`URL` para carregamento de página ou `TOKENIZED_BUTTON_TEXT` para clique de botão), `match_value` e `domain_uri`.
- Para Purchase, incluir `parameters` (value + currency).
- **O evento nasce inativo:** ativar com `ads_pixel_event_update` e `status=ACTIVE`, só se o usuário pediu.

- O CAPI de conversas de WhatsApp usa `action_source=business_messaging`, `messaging_channel=whatsapp` e `ctwa_clid`. Esses eventos também aparecem no dataset.
