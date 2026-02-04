---
name: sr-cardoso-core
description: Visao geral e regras de negocio do projeto Sr Cardoso Barbearia. Use quando pedir onboarding, entendimento do sistema, fluxos cliente/admin, arquitetura, estrutura do repo, premissas nao negociaveis e mapa de arquivos.
---

# Sr Cardoso Core

## Overview
Consolidar contexto do projeto para orientar qualquer tarefa sem quebrar regras de negocio ou arquitetura.

## Quick Start
- Ler `CONTEXTO.md` como fonte canonica de decisoes e regras.
- Consultar `README.md` para setup, dev e deploy.
- Consultar `documento.md` para infra GCP/Cloud Run/Secrets.
- Consultar `docs/WHATSAPP_INFRA_PLAN.md` quando o tema envolver WhatsApp/Evolution.

## Regras de negocio (nao negociar)
- Usar timezone `America/Sao_Paulo` em datas e slots.
- Manter slots de 30 minutos e domingo fechado.
- Manter barbeiro dono com id `sr-cardoso` e prioridade nas listas.
- Manter UI e mensagens em PT-BR.
- Manter RBAC: `master` com acesso total e `barber` escopado ao proprio barberId.

## Mapa rapido do repo
- `apps/web` para cliente/admin (React + Vite).
- `apps/server` para API (Express + Firestore).
- `packages/shared` para tipos/schemas/utils.
- `firebase` para rules e indexes do Firestore.

## Onde olhar primeiro
- Abrir `apps/web/src/lib/api.ts` para ver chamadas do frontend.
- Abrir `apps/server/src/routes/public.ts` e `apps/server/src/routes/admin.ts` para rotas.
- Abrir `packages/shared/src` para tipos e validacoes.

## Checklist de consistencia
- Verificar strings em PT-BR.
- Verificar timezone e regras de horario.
- Verificar ordem de barbeiros (sr-cardoso primeiro).
- Verificar escopo de acesso de barber nas rotas admin.
