---
name: wa-templates
description: Cria, revisa, edita, arquiva e apaga templates de mensagem do WhatsApp oficial pelo MCP do WhatsApp Business, para a agência e para clínicas clientes. Use quando o usuário pedir template de confirmação de consulta, lembrete, pós-procedimento, retorno ou retoque, aviso de pedido, ou quiser saber por que um template foi rejeitado ou mudou de categoria.
---

# Templates do WhatsApp

**Regra:** **biblioteca primeiro.**
- Um template da biblioteca da Meta usado **sem mudar o texto** pode pular a revisão e já nasce com a categoria certa.
- Escrever do zero só quando nada da biblioteca serve.

## Achar a conta
`whatsapp_biz_accounts` com o `business_id` ou com o `phone_number_id` do número. Os templates pertencem à **conta do WhatsApp**.
- Ao falar com o usuário, chamar de "conta do WhatsApp", nunca de "WABA".

## Biblioteca (preferencial)
1. `whatsapp_biz_template_library` com:
   - `search` (ex.: "appointment", "reminder", "consulta");
   - `language=pt_BR`;
   - `waba_id`, para filtrar o que a conta pode usar.
2. Mostrar ao usuário 3 a 5 opções **com o texto do corpo** e o campo `pre_approved`.
3. `whatsapp_biz_create_template_from_library` com `library_template_name` e `language` exatos, mais `template_name` novo (minúsculas, números e `_`).
   - Os valores de `required_inputs` (ex.: nome da clínica, URL do botão) **vêm do usuário**.
   - 1ª chamada sem `confirm`, depois `confirm=true`.

## Custo (desde 01/10/2026)
- Todo template enviado é cobrado conforme a categoria. O template de utilidade **dentro** da janela de 24h também passou a ser cobrado.
- Exceção: janela de 72h aberta por anúncio CTWA.
- A categoria continua sendo decidida pelo conteúdo, **nunca pelo preço**.

## Template próprio
`whatsapp_biz_create_template` com `waba_id`, `template_name`, `language=pt_BR`, `category` e `body_text`.
- **Categoria pelo conteúdo, nunca pelo preço:**
  - **UTILITY** = sem nada promocional **e** específico da pessoa: consulta marcada por ela, pedido dela, instrução do procedimento que ela fez.
  - Qualquer promoção, reativação ou retorno sugerido pela clínica = **MARKETING**.
  - Categoria errada repetida gera punição na conta toda.
- **Regras do corpo:**
  - não começar nem terminar com placeholder;
  - nada de `{{1}} {{2}}` colados;
  - no máximo uma linha em branco entre parágrafos;
  - até 1024 caracteres;
  - emojis: até 6 em UTILITY, 10 em MARKETING;
  - `body_example` com um exemplo por placeholder.
- **Rodapé:** até 60 caracteres, sem placeholder.
- **Botões:** QUICK_REPLY, URL (no máximo 2), PHONE_NUMBER (1) etc.
  - Botões de pagamento (Pix/Boleto), agendamento (BOOKING_STATUS) ou lembrete **existem**, mas não podem ser enviados pelo MCP. Só servem quando o seu backend fizer o envio.
- **Estilo de texto (sugestão):**
  - sem travessão;
  - "você" no singular;
  - voz da clínica em primeira pessoa;
  - sem "promoção", "últimas vagas", "avaliação gratuita" em cliente premium;

## Conjunto base para clínicas
| Template | Categoria | Observação |
|---|---|---|
| confirmação de consulta (data, hora, endereço) | UTILITY | da biblioteca, se houver em pt_BR |
| lembrete da véspera | UTILITY | |
| orientação pós-procedimento | UTILITY | só instrução, sem oferta |
| retorno ou retoque (ex.: toxina após alguns meses) | MARKETING | exige opt-in do paciente |

## Acompanhar e manter
- **Status:**
  - `whatsapp_biz_list_templates` (filtros `status`, `name_or_content`);
  - `whatsapp_biz_get_template` para ver motivo de rejeição, categoria e componentes;
  - no seu backend, o webhook `message_template_status_update` avisa.
- **Editar:** `whatsapp_biz_update_template` manda o conteúdo **completo** (o que ficar de fora é removido). Nome e idioma não mudam. A categoria só muda se o template foi rejeitado por categoria errada.
- **Arquivar ou restaurar:** `whatsapp_biz_manage_templates_archival` (só APPROVED ou REJECTED), com `confirm`.
- **Apagar:** `whatsapp_biz_delete_template` é **irreversível**. Confirmar nome e ID com o usuário.
