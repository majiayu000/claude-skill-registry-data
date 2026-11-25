---
name: meta-mcp
description: Índice das conexões MCP da Meta (Meta Ads, WhatsApp Business e Apps/DevTools). Use no começo de qualquer pedido que envolva Meta Ads, gerenciador de anúncios, campanhas de cliente, WhatsApp oficial, Cloud API, número de WhatsApp, template, webhook, BM, app da Meta, pixel, dataset ou CAPI, e sempre que não estiver claro qual skill seguir. Diz qual skill usar e as regras que valem sempre.
---

# Conexões Meta: por onde começar

**Contexto:** escrito para uma agência que gerencia dezenas de contas de anúncio de clínicas (saúde e estética) no Brasil. Ajuste as regras ao seu caso.

## Qual skill usar
| Pedido do usuário | Skill |
|---|---|
| "como estão as contas", "o que pegou fogo", revisão semanal | `ads-auditoria` |
| analisar um cliente, por que caiu, o que mudar | `ads-diagnostico-cliente` |
| concorrentes, Biblioteca de Anúncios, reunião com prospect | `ads-concorrencia` |
| subir ou montar campanha, duplicar anúncio, criativo novo | `ads-montar-campanha` |
| público, lista de clientes, lookalike, exclusão | `ads-publicos` |
| pixel, dataset, EMQ, eventos, CAPI chegando? | `ads-sinal-conversao` |
| teste A/B, lift, provar resultado | `ads-experimentos` |
| como está o WhatsApp de uma BM, o que falta configurar | `wa-diagnostico` |
| colocar número novo na API oficial | `wa-numero` |
| webhook, não chegam mensagens, apontar para o seu backend | `wa-webhook` |
| templates (confirmação de consulta, lembrete etc.) | `wa-templates` |
| mandar mensagem de teste | `wa-envio-teste` |
| saúde dos apps Meta, limites, depreciações, conformidade | `meta-app-saude` |

## Regras que valem sempre
1. **Ler antes de escrever.** Toda escrita na Meta é mostrada ao usuário e só sai com o OK do usuário.
   - WhatsApp: a 1ª chamada vai sem `confirm`, a 2ª com `confirm=true`.
   - DevTools: devolve um `confirm_token`, que é reenviado depois do OK.
   - Ads: publicar ou ativar só com OK explícito.
2. **Não existe desfazer** no MCP do WhatsApp. Para reverter, o usuário usa os links de `manage_links` do `whatsapp_biz_onboarding_status`.
3. **Ads em modo rascunho:** o que for criado fica em draft ou pausado. `ads_activate_entity` publica e **coloca no ar ATIVO**.
4. **Orçamento:** nunca inventar valor nem cadência; perguntar. Os valores vão em centavos de BRL.
5. **Credenciais:**
   - token de System User e segredo do app são colados pelo usuário direto no `.env` do servidor;
   - `devtools_app` (basic_settings/security) e `devtools_app_review` só com autorização explícita, porque podem expor segredo.
6. **LGPD:** dado de paciente não sai do servidor. Listas para público vão com hash (a ferramenta faz) e com base legal ou consentimento.
7. **Ads MCP, campos em toda chamada:**
   - `client_conversation_id`: 20 caracteres aleatórios, o mesmo na conversa inteira;
   - `client_model`: o modelo atual;
   - `advertiser_request`: as palavras do usuário.

## Custo das mensagens (desde 01/10/2026)
- Toda mensagem enviada pela API do WhatsApp é cobrada, inclusive a resposta livre dentro da janela de 24h e o template de utilidade dentro da janela.
- **Grátis** só dentro da janela de 72h aberta por anúncio CTWA ou botão da Página.
- Sem forma de pagamento, nada chega.

## Limites das conexões
- **WhatsApp MCP:** é para setup e teste, uma mensagem por vez, não para disparo. Templates com pagamento, agendamento ou lembrete no botão não saem por ele.
- **Ads MCP:** não mexe em formulário de lead nem em CRM. Contas fora do rollout (`is_ads_mcp_enabled=false`) não podem ser usadas.
