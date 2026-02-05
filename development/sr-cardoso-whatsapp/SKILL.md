---
name: sr-cardoso-whatsapp
description: Integracao WhatsApp via Evolution API no Sr Cardoso. Use quando configurar EVOLUTION_*, conectar instancias, ajustar notificacoes, cron jobs, filas de retry e mensagens automaticas.
---

# Sr Cardoso WhatsApp

## Overview
Operar e evoluir o fluxo de mensagens automaticas via Evolution API e painel admin.

## Arquivos-chave
- `apps/server/src/services/whatsappNotifications.ts` (logica de envios).
- `apps/server/src/lib/evolutionApi.ts` (cliente HTTP para Evolution).
- `apps/server/src/routes/admin.ts` (endpoints admin WhatsApp).
- `apps/server/src/routes/public.ts` (cron endpoints).
- `packages/shared/src/schemas/whatsapp.schema.ts` (schemas de payload).
- `apps/web/src/pages/admin/WhatsappPage.tsx` (UI).

## Env vars e infra
- Usar `EVOLUTION_BASE_URL`, `EVOLUTION_API_KEY`, `EVOLUTION_INSTANCE_NAME`.
- Usar `CRON_SECRET` para `/api/cron/*`.
- Consultar `documento.md` e `docs/WHATSAPP_INFRA_PLAN.md` para rede/VM.

## Dados no Firestore
- Config em `settings/whatsapp-notifications`.
- Fila em `whatsappMessageQueue`.
- Logs/testes em `whatsappOutbound`.

## Fluxos principais
- Enviar confirmacao no `POST /api/bookings`.
- Enviar lembrete via `POST /api/cron/send-reminders`.
- Reprocessar fila via `POST /api/cron/process-queue`.
- Enviar cancelamento via `POST /api/public/cancel/:cancelCode`.

## Operacao da instacia
- Checar status em `GET /api/admin/whatsapp/status`.
- Conectar por QR ou pairing em `POST /api/admin/whatsapp/connect`.
- Desconectar em `POST /api/admin/whatsapp/disconnect`.
- Enviar teste em `POST /api/admin/whatsapp/send-test`.

## Observacoes de negocio
- Montar mensagens com nome do servico vindo de `settings/finance.services[].label`.
- Manter textos em PT-BR e evitar PII desnecessaria.
