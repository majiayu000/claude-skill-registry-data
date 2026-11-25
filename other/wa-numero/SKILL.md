---
name: wa-numero
description: Coloca um número de telefone na API oficial do WhatsApp (Cloud API) pelo MCP do WhatsApp Business, no fluxo adicionar, verificar e registrar. Use quando o usuário quiser cadastrar um número novo para a agência ou para um cliente, terminar o registro de um número que ficou pela metade, ou entender por que um número está pendente.
---

# Número na Cloud API: adicionar → verificar → registrar

## Atenção antes de começar
- **Número que está em uso no app WhatsApp do celular:** este fluxo é para número **novo** ou **liberado**.
  - Registrar pela Cloud API um número que roda no app do celular **desconecta o app**.
  - Para manter o celular funcionando junto, o caminho é a **coexistência**, que usa o Embedded Signup de provedor de solução, não esta skill.
  - **Perguntar sempre** se o número está em uso no celular.
- **Não tem desfazer.** Para tirar um número depois, o usuário faz no Gerenciador de Negócios.
- **A BM precisa estar pronta:** perfil completo e pré-requisitos ok (`wa-diagnostico`).

## Passo a passo
1. **BM:** `whatsapp_biz_businesses`, confirmar com o usuário e checar `profile_complete` e `prerequisites_met`.
2. **Retomar ou começar:** `whatsapp_biz_phone_numbers` com `phone_number` (E.164).
   - Se o número já existe, seguir o `next_action` do usuário e **não recomeçar**.
   - `verified_not_registered` = falta só registrar.
3. **Adicionar:** `whatsapp_biz_add_phone_number` com:
   - `business_id`;
   - `display_name`: o nome que o paciente vê. Precisa bater com a marca, porque passa por revisão;
   - `vertical`: escolher pela atividade e dizer a escolha no resumo. Clínica ou consultório = `HEALTH`; estética e beleza = `BEAUTY`; agência = `PROF_SERVICES`; loja = `RETAIL`.
   - **1ª chamada sem `confirm`** → mostrar o resumo → OK → **mesma chamada com `confirm=true`**.
   - Criar uma conta nova do WhatsApp é o padrão. Só passar `waba_id` se o usuário pedir uma conta existente.
4. **Código:** `whatsapp_biz_send_verification_code` com o `phone_number_id` e `code_method=SMS` (ou `VOICE` se o número não recebe SMS). Também passa por `confirm`.
5. **O usuário informa o código** → `whatsapp_biz_verify_phone_number` com `verification_code`.
6. **Registrar:** `whatsapp_biz_register_phone_number` **sem PIN primeiro**.
7. **Conferir:** `whatsapp_biz_onboarding_status`.
   - Registrado não quer dizer que já manda mensagem: falta pagamento (`whatsapp_biz_configure_payments`) e webhook (`wa-webhook`).
   - Texto livre só chega a quem escreveu nas últimas 24h.

## Depois
- Templates de utilidade: skill `wa-templates`.
