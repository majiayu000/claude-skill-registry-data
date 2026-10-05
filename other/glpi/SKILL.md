---
name: glpi
description: Tickets, triagem, followups, solução, usuários, grupos, ativos, projetos e base de conhecimento no GLPI via MCP glpi.
metadata:
  version: 1.2.0
---

# GLPI

Você gerencia o GLPI (ITSM) usando a skill `glpi` e o servidor MCP `glpi`. A
mesma skill funciona em Claude Code, Codex e Hermes. Se o runtime não expuser
as tools, não simule resultados: consulte a referência operacional e peça o
setup ao usuário.

## Mapa de intenção → tool

| Intenção | Tool |
|---|---|
| Buscar chamados | `search_tickets` |
| Detalhar chamado | `get_ticket` |
| Abrir chamado | `create_ticket` |
| Atualizar campos | `update_ticket` — não aceita `status: "closed"` |
| Acompanhar/comentar | `add_ticket_followup` |
| Solucionar/fechar | `close_ticket` — exige texto de solução |
| Anexar arquivo | `upload_document` + `link_document` |
| Validação | `request_ticket_validation` / `answer_ticket_validation` |
| Pessoas e grupos | `search_users` / `get_user` · `search_groups` / `get_group` |
| Ativos | `search_assets` / `get_asset` |
| Projetos | `search_projects` / `get_project` |
| Base de conhecimento | `search_kb` / `get_kb_article` |

## Prompts e resources MCP

- Triagem: `triage_ticket {ticket_id}`.
- Panorama: `summarize_tickets {filter?, limit?}`.
- Contexto: `glpi://ticket/{id}`, `glpi://asset/{itemtype}/{id}` e `glpi://kb/{id}`.

O servidor expõe exatamente 20 tools, 2 prompts e 3 resources. É compatível
com GLPI 10.x e 11.x pela API REST Legacy V1 em `/apirest.php`, usando
`@soarescbm/mcp-glpi@0.4.0`.

## Regras ITSM

- Toda mutação exige confirmação explícita antes da chamada.
- Nunca defina `priority`: proponha `urgency` e `impact` (1–5); o GLPI calcula a prioridade pela matriz.
- Fechar é fluxo próprio: solução aprovada e então `close_ticket`; `force_close` requer consentimento explícito.
- Comunique-se pelo ID numérico e preserve o idioma da instância.
- Usuários, grupos, ativos, projetos e KB são somente leitura; não há Problems/Changes, SLA/OLA ou administração.

## Fluxos

- Abrir: título, descrição, urgency/impact → proposta → confirmação → criação.
- Triar: prompt de triagem, prioridade justificada e próximas ações.
- Relatar: panorama somente leitura; ações sempre após confirmação.

Para filtros, autenticação e contexto, siga as referências distribuídas com o
plugin, conforme o runtime que carregou a skill.
