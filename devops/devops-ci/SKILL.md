---
name: devops-ci
description: GitHub Actions — PR-workflow (lint+typecheck+test с кэшем npm) и deploy-workflow (build+deploy, concurrency, GitHub secrets); валидация YAML (роль devops). Use когда нужно настроить или починить CI/CD-pipeline.
---

# Задача: настроить GitHub Actions

Настрой CI/CD (см. `$ci-cd`, `$nodejs`).

1. Изучи проект: пакетный менеджер (lockfile), реальные скрипты `lint`/`typecheck`/`test`/`build`, версия Node, существующие workflow.
2. PR-workflow (`.github/workflows/pr.yml`): `on: pull_request`; `actions/setup-node` с `cache: npm` (pnpm — `pnpm/action-setup` ДО setup-node); `npm ci` → lint → typecheck → test. Только существующие скрипты.
3. Deploy-workflow (`deploy.yml`): `push` в main; build + деплой; для Render — deploy hook (`curl $RENDER_DEPLOY_HOOK` из secrets) или auto-deploy; наблюдение — роль `$render`.
4. Дисциплина: `concurrency` + `cancel-in-progress: true` (для деплоя — `false`); `permissions: contents: read` верхнеуровнево; `pull_request_target` без нужды не используй; в fork-PR секреты пусты.
5. Валидируй YAML до выдачи (парсер/`actionlint`) и покажи вывод; честно пометь, что прогон подтвердит только реальный push.

Прод-деплой активируй только с явного подтверждения. Отдай пути + вывод валидации + список secrets для репозитория.
