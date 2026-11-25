---
name: ads-montar-campanha
description: Monta campanhas de Meta Ads para clientes da agência pelo Meta Ads MCP, de forma segura (rascunho/pausado), a partir de um briefing. Use quando o usuário pedir para subir, criar ou montar uma campanha, um conjunto ou um anúncio, duplicar um anúncio vencedor, trocar criativo, ou preparar a campanha de um cliente para ele revisar. Nada vai ao ar sem OK explícito.
---

# Montar campanha (rascunho → prévia → OK → publicar)

**Regra de ouro:** criar, mostrar a prévia e **parar**. Publicar é outra ordem do usuário.
- O Ads MCP da agência está em **modo rascunho**: anúncio criado vira draft.
- `ads_activate_entity` publica e deixa **ATIVO**.

## Antes de criar: o briefing mínimo
Perguntar o que faltar. Não inventar:
- **cliente e conta:** conferir `is_ads_mcp_enabled=true` e se a conta tem forma de pagamento;
- **objetivo e destino:** WhatsApp (CTWA), site ou formulário, perfil do Instagram;
- **camada do funil:**
  - campanha de **conversão nunca roda para público frio**;
  - frio vai para tráfego de perfil;
  - morno e quente (seguidores, engajados, visitantes, lista) recebem conversão;
- **orçamento:** valor e cadência ditos pelo usuário (diário ou total), em centavos de BRL. "R$ 2.000 por mês" não é orçamento diário: perguntar;
- **região:** cidade e raio, ou estado;
- **criativos:** URL pública da imagem ou do vídeo, ou um post existente.

## Nomenclatura (sugestão)
Sempre em CAIXA ALTA, sem nome de paciente (trocar por PACIENTE), sem travessão longo e sem sobra de "Cópia".

**Campanha:** `[SIGLA][ORÇAMENTO][OBJETIVO][ETAPA] DESTINO OU ASSUNTO DD.MM`
- ORÇAMENTO: `ABO` ou `CBO`.
- OBJETIVO: `ENG` (engajamento), `TFG` (tráfego) ou `VENDA` (vendas). Outro objetivo (cadastros, reconhecimento): usar forma curta e confirmar com o usuário.
- ETAPA: `TOPO`, `MEIO` ou `FUNDO`.
- DESTINO OU ASSUNTO: `WHATSAPP`, `SEGUIDORES PERFIL`, `THRUPLAY`, `QUEBRA DE OBJEÇÕES`, nome do empreendimento etc.
- DATA: dia e mês de criação, `DD.MM`.
- Exemplos: `[AG][ABO][VENDA][FUNDO] WHATSAPP 21.10` · `[AG][ABO][TFG][TOPO] SEGUIDORES PERFIL 21.10` · `[AG][CBO][ENG][MEIO] QUEBRA DE OBJEÇÕES 21.10`

**Conjunto:** `NN- TEMPERATURA [SEXO IDADE][LOCAL][FONTE DO PÚBLICO]`
- NN: começa em `00` e não repete dentro da campanha (00, 01, 02...).
- TEMPERATURA: `FRIO`, `MORNO` ou `QUENTE`, pela composição real do público.
- [SEXO IDADE]: `[MULHERES 25-55]`, `[HOMENS 30-60]`, `[TODOS 25-60]`.
- [LOCAL]: `[TATUAPÉ 10KM]`, `[GOIÂNIA 40KM]`, `[FORTALEZA 15KM]`, `[CIDADES REGIÕES]`.
- [FONTE DO PÚBLICO]: `[ENV. 365D]`, `[ABERTO]`, `[LAL 1% SEGUIDORES]`, `[ENV. 365D + LISTA]`.
- Exemplos: `00- QUENTE [MULHERES 25-55][GOIÂNIA 40KM][ENV. 365D]` · `00- FRIO [MULHERES 25-55][TATUAPÉ 10KM][ABERTO]`

**Anúncio:** `ADNN- TRECHO QUE IDENTIFICA`
- Numeração nova a cada campanha, na ordem em que sobe: `AD01`, `AD02`, `AD03`... (sempre 2 dígitos), mesmo que o criativo já tenha sido usado em outra campanha.
- O mesmo vídeo em mais de um conjunto da mesma campanha leva o mesmo número.
- Se for exatamente o mesmo vídeo de um AD antigo e fizer sentido manter a referência, pode usar o número antigo.
- TRECHO: começo da legenda do post ou parte curta que identifique o criativo, até uns 40 caracteres.
- Exemplos: `AD01- SE ELA JÁ É LINDA, POR QUE HARMONIZAR` · `AD02- HARMONIZAÇÃO É ARTE` · `AD03- DEPOIS DE PERDER 35 KG`

**Classificação do criativo** (gancho, prova, tom, oferta, CTA da taxonomia) **não vai no nome**: fica na planilha mestre, ligada pelo `ad_id`.

## Passo a passo
1. **Página e Instagram:** `ads_get_ad_account_pages` (e `ads_get_ig_accounts` para pegar o `instagram_user_id`). Para formulário de lead, a página precisa de `leadgen_tos_accepted=true`.
2. **Campanha:** `ads_create_campaign` com `objective` ODAX e `buying_type=AUCTION`.
   - CBO por padrão (`campaign_daily_budget` ou `campaign_lifetime_budget`), salvo se o usuário pedir ABO.
   - `special_ad_categories="[]"`, a não ser que seja crédito, imóvel ou emprego.
   - Conferir o resultado com `ads_get_ad_entities` (`object_ids=[id]`, `level=campaign`, campos alterados + `effective_status`).
3. **Conjunto:** `ads_create_ad_set`.
   - `optimization_goal` vem da lista válida que a campanha devolveu.
   - **WhatsApp:** `optimization_goal=CONVERSATIONS` + `destination_type=WHATSAPP` (em OUTCOME_LEADS só vale com WHATSAPP); `promoted_object` com `page_id`.
   - **Site:** `promoted_object` com `pixel_id`.
   - `billing_event=IMPRESSIONS`.
   - `targeting`: geografia ampla. **Nunca inventar IDs de interesse.** Públicos personalizados de morno ou quente vêm da skill `ads-publicos`.
4. **Mídia:** `ads_creative_upload_media` com `upload_source=URL`, `media_type` e `media_url` pública. Vídeo: esperar `ready` em `ads_get_ad_videos`.
5. **Criativo:** `ads_create_creative` com `page_id`, `instagram_user_id`, `message`, `headline`, `call_to_action_type` (WhatsApp: `WHATSAPP_MESSAGE`) e `link_url` quando a ferramenta exigir.
   - `self_ai_disclosure` é decisão do usuário: sempre perguntar.
6. **Anúncio:** `ads_create_ad` com o `creative_id`. Fica em rascunho. Para duplicar um vencedor, usar `source_ad_id`.
7. **Prévia:** `ads_get_ad_preview` com `ad_id` (se der erro de anúncio recém-criado, tentar com `creative_id`). **Mandar o `preview_url` ao usuário.**
8. **Parar aqui.** Mostrar o resumo: estrutura, orçamento, público, criativo, prévia.

## Publicar (só depois do "pode publicar")
1. `ads_get_ad_entities` com `object_state=draft` para pegar os IDs de campanha, conjunto e anúncio.
2. `ads_activate_entity` com `object_ids` (tudo junto) e `publish_as_active=true` se o usuário pediu para ativar.
3. Resposta `PUBLISHING` = **entregue para publicação**, ainda não confirmado. Reler em 2 minutos.
4. Depois de publicado: `ads_get_opportunity_score` para ver se a estrutura segue as boas práticas.

## Mudanças em campanha que já está no ar
- **Nome, orçamento, status:** `ads_update_entity`, com os nomes da API: `name`, `daily_budget`, `status=PAUSED`. Nunca `ACTIVE` por aqui.
- **Criativo não se edita:** criar um anúncio novo com o criativo novo e pausar o antigo.
- **Duplicar anúncio:**
  - o `source_ad_id` sozinho pode ser recusado ("creative is required");
  - passar `creative={"creative_id":"<id>"}`; o id sai de `ads_get_ad_entities` com o campo `creative_id`.
- **Anúncio de visita ao perfil do Instagram:** se a API recusar a criação, ela fica com o usuário no Gerenciador, e orçamento e status seguem pelo MCP.
