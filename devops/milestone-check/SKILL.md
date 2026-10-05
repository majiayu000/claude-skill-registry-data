---
name: milestone-check
description: Проверяет готовность вехи курса В1–В5 реальным запуском команд и выдаёт таблицу «пункт / статус / доказательство». Ничего не исправляет. Аргумент — В1, В2, В3, В4 или В5.
model: haiku
---

# milestone-check — проверка вехи

Аргумент: `$ARGUMENTS`. Веха проверяется **запуском, а не рассказом**: каждый пункт подтверждается выводом команды или путём к файлу. Ничего не исправлять — только отчёт.

## В1. Продукт поднимается

- [ ] `git rev-parse --show-toplevel` совпадает с корнем проекта
- [ ] `git log --oneline` — есть коммиты, remote настроен (`git remote -v`)
- [ ] чистая установка: `git clone` во временную папку → `npm ci` проходит
- [ ] `npm run check` зелёный
- [ ] `docker compose up -d --build` → `curl -fsS localhost:<port>/healthz` возвращает 200
- [ ] README содержит шаги запуска, и они совпадают с тем, что реально сработало

## В2. Намерение и спецификация

- [ ] `docs/brief.md` существует, есть разделы «для кого», «что не делаем»
- [ ] `docs/spec/requirements.md` — есть REQ с критериями Given/When/Then
- [ ] `docs/tasks.md` — задачи ссылаются на REQ
- [ ] хотя бы одна задача `done`, её тесты с префиксом `REQ-` существуют (`grep -r "REQ-" --include=*.test.ts`)
- [ ] `npm run check` зелёный

## В3. Репозиторий готов для агента

- [ ] `docs/architecture.md` со схемой
- [ ] ≥ 3 ADR в `docs/adr/`
- [ ] `CLAUDE.md`, `.claude/skills/`, `.claude/agents/` на месте
- [ ] защита ветки: `gh api repos/{owner}/{repo}/branches/main/protection` не 404
- [ ] есть смёрженный PR с зелёными проверками: `gh pr list --state merged --limit 5`, `gh pr checks <n>`

## В4. Проверяемость

- [ ] в `package.json` есть все скрипты из раздела 6 CLAUDE.md
- [ ] `npm run check` зелёный, `npm run check:trace` зелёный
- [ ] в `docs/review/` есть отчёт `spec-reviewer` с **хотя бы одним** найденным расхождением
- [ ] найденные расхождения превращены в задачи или ADR

## В5. Границы и цена

- [ ] `docs/security/threat-model.md`, `docs/security/permissions.md`
- [ ] лимиты (размер сообщения, rate limit, подключения) заданы в конфиге сервера
- [ ] `npm run check:perms` существует и зелёный на `main`
- [ ] есть доказательство, что конвейер падает на опасном действии: красный CI-прогон демонстрационного PR (`gh run list --branch demo/dangerous-action`)

## Формат вывода

| Пункт | Статус | Доказательство |
|---|---|---|
| npm run check зелёный | ✅ | `Tests 42 passed` |
| защита ветки | ❌ | `gh api ... → 404 Branch not protected` |

В конце — список ❌ в порядке, в котором их стоит закрывать.
