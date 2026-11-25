---
name: wa-envio-teste
description: Envia uma mensagem de teste pelo WhatsApp oficial (Cloud API) usando o MCP do WhatsApp Business. Use quando o usuário pedir para testar o envio de um número, mandar um template aprovado para um contato específico, ou checar se as mensagens estão chegando. Não serve para disparo em massa.
---

# Mensagem de teste pelo WhatsApp oficial

**Limites:**
- É **uma mensagem por vez, com confirmação**.
- Disparo, régua e automação ficam no seu backend com token de System User, **nunca** por aqui.

## Antes de enviar
1. **Número de envio:** `whatsapp_biz_phone_numbers` com `status=linked`.
   - Nunca pedir `phone_number_id` ao usuário: mostrar a lista e ele escolhe pelo número.
   - O número de teste da Meta não aparece aqui e não envia por esta ferramenta.
2. **Pagamento:** `whatsapp_biz_configure_payments` com `phone_number_id`. Sem forma de pagamento a mensagem é aceita e **provavelmente não chega**: avisar antes.
   - **Desde 01/10/2026 toda mensagem enviada pela API é cobrada,** inclusive texto livre dentro da janela de 24h. A exceção é a janela de 72h aberta por anúncio CTWA. Cada teste tem custo pequeno, mas tem.
3. **Destinatário:** **vem do usuário**, em E.164. Nunca inventar nem reaproveitar número de exemplo.
4. **Tipo:**
   - `text` (texto livre): só chega se a pessoa escreveu para o número **nas últimas 24h**.
   - `template`: chega a qualquer momento, mas o template precisa estar **APPROVED**. Ler os componentes com `whatsapp_biz_get_template` antes.
   - Valores dos placeholders: só dados reais ou dados do usuário, nunca os exemplos guardados no template.

## Enviar
1. `whatsapp_biz_send_message` com:
   - `phone_number_id` e `to`;
   - `message_type` (`text` + `message`, ou `template` + `template_name` + `language_code`);
   - `body_parameters` (array JSON em string), `header_parameter` e `button_parameters` quando o template pedir.
2. **1ª chamada sem `confirm`:** a ferramenta devolve o resumo (de qual app e número sai, para quem, conteúdo). Mostrar ao usuário.
3. Depois do OK, a **mesma chamada com `confirm=true`**. Guardar o `wamid` devolvido.

## Conferir
- Perguntar ao usuário se chegou.
- Com o webhook ligado, o status (sent, delivered, read, failed) aparece no seu backend pelo campo `messages`.
