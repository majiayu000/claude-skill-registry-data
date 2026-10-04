---
name: ci-cd
description: CI/CD на GitHub Actions — эталонный PR-workflow (lint+typecheck+test с кэшем npm/pnpm), deploy-workflow с environment и secrets, concurrency (отмена устаревших прогонов), matrix, безопасность (минимальные permissions, опасность pull_request_target, секреты и fork-PR), интеграция с Render (deploy hook / auto-deploy). Use when настраиваешь или чинишь GitHub Actions, pipeline, кэширование CI или деплой по пушу.
version: 1.0.0
---

# Навык: CI/CD на GitHub Actions

CI — единственный честный gate качества: workflow должен быть валиден (проверен парсером до пуша) и **реально зелёный** в Actions. Секреты — только в GitHub secrets, никогда в YAML/коде.

## 1. Эталонный PR-workflow
```yaml
# .github/workflows/pr.yml
name: PR checks
on: pull_request
permissions:
  contents: read                      # минимальные права — по умолчанию для всех jobs
concurrency:
  group: pr-${{ github.ref }}
  cancel-in-progress: true            # новый пуш в PR отменяет устаревший прогон
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22            # = версия в Dockerfile/engines — локалка ≈ CI ≈ прод
          cache: npm                  # кэш по lockfile; для pnpm: cache: pnpm + pnpm/action-setup ДО setup-node
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
```
Шаги — только реально существующие скрипты из `package.json`; не выдумывай `npm run typecheck`, если его нет.

## 2. Deploy-workflow (main → прод)
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: deploy-production
  cancel-in-progress: false           # деплой не отменяем на середине
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production           # environment-secrets + опциональный required reviewer как ручной gate
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci && npm run build
      - name: Trigger Render deploy
        run: curl -fsS "${{ secrets.RENDER_DEPLOY_HOOK }}"
```

## 3. Matrix (кратко)
```yaml
strategy:
  matrix: { node: [20, 22] }
steps:
  - uses: actions/setup-node@v4
    with: { node-version: ${{ matrix.node }}, cache: npm }
```
Нужен только библиотекам/пакетам с поддержкой нескольких версий; приложению — одна версия (та же, что в проде).

## 4. Безопасность
- **`permissions` минимальные:** верхнеуровнево `contents: read`; расширяй точечно в job (`pull-requests: write` для комментатора и т.п.). Без блока `permissions` токен получает широкие дефолты.
- **`pull_request_target` опасен:** запускается с секретами в контексте base-ветки, но легко ошибиться и выполнить код из fork-PR (checkout head) → утечка секретов. Не используй без крайней нужды; никогда не сочетай с checkout PR-кода.
- **Секреты и fork-PR:** в `pull_request` из форков `secrets.*` пусты — PR-workflow не должен зависеть от секретов; деплой — только из `push` в main.
- Пинь actions хотя бы мажором (`@v4`); для повышенных требований — по SHA. Никогда не `echo` секреты (маскирование обходимо через трансформации).
- Валидируй YAML до пуша: `actionlint` (если установлен) или парсер (`python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/pr.yml'))"`). Помни: реальный прогон подтвердит только push.

## 5. Интеграция с Render
| Способ | Как | Когда |
|---|---|---|
| **Auto-deploy** | Render сам деплоит по пушу в подключённую ветку (настройка сервиса) | по умолчанию — проще всего, CI отдельно гоняет тесты |
| **Deploy hook** | секретный URL сервиса; `curl $RENDER_DEPLOY_HOOK` шагом workflow **после** зелёных тестов | нужен gate «деплой только после CI» — тогда auto-deploy у сервиса выключи |
Hook-URL — секрет (даёт право деплоя) → только GitHub secrets. Наблюдение за деплоем (статус, логи, метрики) — через агента `render` (MCP `get_deploy`/`list_logs`). Прод-деплой и необратимые активации — только с явного подтверждения владельца.

## 6. Типовые ошибки
- Кэш не работает → нет lockfile в корне / `cache: npm` при pnpm-проекте / `pnpm/action-setup` после `setup-node`.
- «Секрет пустой» → fork-PR, environment-секрет без `environment:` в job, или опечатка в имени.
- Дублирующиеся прогоны жгут минуты → нет `concurrency` с `cancel-in-progress`.
- CI зелёный, прод падает → версии Node/баз в CI ≠ прод; выравнивай с Dockerfile (`node-version`, services).
