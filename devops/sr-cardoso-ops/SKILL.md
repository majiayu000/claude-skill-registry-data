---
name: sr-cardoso-ops
description: Operacoes e deploy do Sr Cardoso (Cloud Run, Firestore rules/indexes, env vars, scripts, Docker). Use quando configurar ambiente, rodar deploy, revisar infra GCP ou rotinas de setup.
---

# Sr Cardoso Ops

## Overview
Executar operacoes e deploy do sistema com Cloud Run, Firestore e scripts locais.

## Documentacao base
- Consultar `documento.md` para estado real da infra GCP e comandos usados.
- Consultar `README.md` para setup/dev/deploy basico.
- Consultar `docs/WHATSAPP_INFRA_PLAN.md` para Evolution/WhatsApp.

## Scripts principais
- Usar `scripts/deploy-cloudrun.sh` para deploy sem Cloud Build.
- Usar `scripts/init-barbers.ts` para seed de barbeiros.

## Env vars importantes (server)
- `ADMIN_JWT_SECRET`, `ADMIN_PASSWORD`, `ADMIN_USERNAME` (bootstrap).
- `GCP_PROJECT_ID`, `GCP_STORAGE_BUCKET`.
- `WEB_ORIGIN`, `CANCEL_LINK_PEPPER`.
- `EVOLUTION_BASE_URL`, `EVOLUTION_API_KEY`, `EVOLUTION_INSTANCE_NAME`.
- `CRON_SECRET`.

## Env vars (web)
- `VITE_API_BASE_URL` em `apps/web/.env`.

## Firestore
- Regras em `firebase/firestore.rules`.
- Indexes em `firebase/firestore.indexes.json`.

## Build e container
- Dockerfile em `apps/server/Dockerfile` faz build de web + server.
- Cloud Run serve `apps/web/dist` via `STATIC_DIR`.

## Alertas operacionais
- `gcloud run services update --set-env-vars` substitui a lista inteira.
- Manter secrets no Secret Manager quando possivel.
- Tratar `apps/functions` como legado (nao usar).
