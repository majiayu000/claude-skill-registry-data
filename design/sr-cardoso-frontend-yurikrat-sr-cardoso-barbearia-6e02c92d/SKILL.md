---
name: sr-cardoso-frontend
description: Frontend React/Vite/PWA do Sr Cardoso. Use quando editar paginas, componentes, hooks, fluxo de agendamento, painel admin, consumo de API REST e UX mobile-first.
---

# Sr Cardoso Frontend

## Overview
Executar tarefas no frontend web (cliente e admin) mantendo fluxo mobile-first, PT-BR e contratos com a API.

## Entradas e rotas
- Partir de `apps/web/src/App.tsx` (rotas) e `apps/web/src/main.tsx`.
- Fluxo cliente: `apps/web/src/pages/BookingPage.tsx`, `apps/web/src/pages/SuccessPage.tsx`, `apps/web/src/pages/CancelBookingPage.tsx`.
- Fluxo admin: paginas em `apps/web/src/pages/admin/*`.

## API e dados
- Usar `apps/web/src/lib/api.ts` para chamadas REST.
- Usar `apps/web/src/lib/api-compat.ts` apenas para compatibilidade legada.
- Nao usar Firebase SDK no frontend.

## Estado e storage
- Usar `apps/web/src/hooks/useBookingState.tsx` para estado do booking.
- Respeitar chaves de storage: `sr-cardoso-booking-state`, `sr_admin_token`, `sr_remembered_customer`.
- Usar `apps/web/src/hooks/useAuth.ts` para sessao admin.

## Constantes e branding
- Usar `apps/web/src/utils/constants.ts` para IDs, labels e timezone.
- Usar `apps/web/src/hooks/useBranding.ts` para logo e cache.

## UI e UX
- Manter strings em PT-BR.
- Manter timezone `America/Sao_Paulo`.
- Respeitar regras de horario e schedule do barbeiro.
- Manter layout admin em `apps/web/src/components/admin/AdminLayout.tsx`.
- Manter indicador offline em `apps/web/src/components/OfflineIndicator.tsx`.

## PWA
- Ajustar manifest e assets em `apps/web/vite.config.ts`.
