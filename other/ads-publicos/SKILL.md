---
name: ads-publicos
description: Cria e gerencia públicos personalizados no Meta Ads MCP para clientes da agência, respeitando a LGPD. Use quando o usuário pedir público de engajamento (Instagram ou página), visitantes do site, lista de clientes ou pacientes para exclusão ou semelhante, lookalike, ou para revisar os públicos existentes de uma conta.
---

# Públicos personalizados (com LGPD)

**Para que servem no método:** a campanha de conversão só roda para público **morno ou quente**. São esses os públicos que alimentam a conversão:
- engajados no Instagram ou na página;
- visitantes do site;
- lista de clientes.

O público frio vai para tráfego de perfil.

## Ler o que já existe
- `ads_get_ad_account_custom_audiences` com o `ad_account_id`.
- `ads_get_custom_audience` para o detalhe de um público.
- `ads_get_custom_audience_adsets` para ver quais conjuntos usam o público.

## Criar (com o OK do usuário)
`ads_create_custom_audience` com `ad_account_id`, `name` e `subtype`:

- **ENGAGEMENT (o mais usado nas clínicas):**
  - `rule` como **string JSON**, com `event_sources` do tipo `ig_business` (ID da conta do Instagram, via `ads_get_ig_accounts`) ou `page`;
  - `retention_seconds` de 30 a 365 dias;
  - usar só nomes de evento documentados.
- **WEBSITE:**
  - `rule` com `event_sources` `pixel`;
  - template `ALL_VISITORS` com filtro `url` / `i_contains` / valor vazio;
  - pixel via `ads_get_datasets`.
- **CUSTOM (lista):**
  - `customer_file_source=USER_PROVIDED_ONLY`;
  - cria vazio; depois vem o upload abaixo.
- **LOOKALIKE:**
  - `origin_audience_id` (nunca outro lookalike) e `lookalike_ratio` de 0.01 a 0.05;
  - não perguntar o país.

## Subir lista de clientes ou pacientes (portão de LGPD)
1. **Só com base legal:** o cliente (clínica) precisa ter consentimento ou base legal para usar os dados em anúncio. Perguntar ao usuário antes. **Na dúvida, usar só para exclusão** (não mostrar anúncio a quem já é paciente).
2. **Dados mínimos:** telefone e/ou e-mail. Nada de dado de saúde (procedimento, diagnóstico) na lista nem no nome do público.
3. **Upload:** `ads_update_custom_audience_users` com `audience_id`, `schema` (ex.: `["PHONE","EMAIL"]`) e `data` em linhas.
   - A ferramenta normaliza e aplica o hash SHA-256 antes de enviar.
   - `customer_consent=true` só se houver consentimento de verdade.
   - Lotes de no máximo alguns milhares de linhas por chamada.
4. **Remover pessoas:** a mesma ferramenta com `operation=REMOVE`. Pode ser recusado se o público ficar pequeno demais para campanhas ativas.

## Editar e apagar
`ads_update_custom_audience` e `ads_delete_custom_audience`, sempre com o OK do usuário. Antes de apagar, conferir com `ads_get_custom_audience_adsets` se algum conjunto ativo usa o público.
