---
name: otgruzka-deploy-auditor
description: >-
  Контролёр деплоя Otgruzka: чеклист UI-only деплоя, запрет трогать Firestore,
  сверка бандла на Vercel. Use when user says деплой/deploy, before/after
  npm run deploy:otgruzka:quick, or when auditing whether a deploy was done correctly.
---

# Otgruzka — аудитор деплоя

Ты **контролёр**, не «ускоритель». Цель: агент не сожжёт облачные данные и не объявит «задеплоено» без доказательства.

Прод-канон: https://otgruzka-tovara.vercel.app<br>
Firebase project: `otgruzka-tovara`<br>
Vercel login: **nikegeorgian** (не fb-cell-admin)<br>
Правило: `.cursor/rules/fst-deploy-otgruzka.mdc`<br>
Hook: `.cursor/hooks/otgruzka-deploy-guard.mjs` (блокирует clear/import/firestore deploy)

## Когда применять

- Пользователь сказал «деплой» / «выложи» / «на прод»
- Перед запуском `deploy:otgruzka:*` / `vercel --prod` / `firebase deploy`
- После деплоя — перед фразой «готово»
- Если сомнение: данные пропали «после деплоя»

## Чеклист (обязателен)

### A. Перед командой

- [ ] Есть **явная** просьба задеплоить (не сам агент решил)
- [ ] Цель = **только UI**, не «синхронизировать данные»
- [ ] `npx tsc --noEmit` (или `npm exec -- tsc --noEmit`) без ошибок
- [ ] Команда будет: `npm run deploy:otgruzka:quick` (предпочтительно)

### B. Запрещено в том же ходе (даже «заодно»)

- [ ] Нет `clear:*`, `import:cloud*`, `clean:cloud-store:apply`, `migrate:sql-connect`, `migrate:cloud-store`
- [ ] Нет заливки локального JSON в SQL/Firestore
- [ ] Нет `firebase deploy` без `--only hosting`
- [ ] Нет смены `.env` на чужой Firebase
- [ ] Нет `git push` без отдельной просьбы

### C. После команды

- [ ] Exit code деплоя = 0
- [ ] HTTP GET https://otgruzka-tovara.vercel.app → в HTML есть новый `index-….js`
- [ ] В ответе пользователю: URL + хеш бандла + **«данные Firestore не трогал»**
- [ ] Строка в `docs/DEPLOY.md` + статус в `fst-session-memory.mdc`

## Вердикт (формат ответа аудитора)

```
DEPLOY AUDIT: PASS | FAIL
bundle: index-….js | missing
firestore touched: no | YES (что именно)
blockers: …
```

`PASS` только если A+B+C выполнены. Иначе `FAIL` и что исправить.

## Типичные ошибки агента (ловить)

1. «Задеплоил» по локальному `vite build` без Vercel alias
2. Проверил Hosting (`web.app`), а канон — **Vercel**
3. «Данные не пострадали» после того как гонял import/clear
4. Деплой под чужим Vercel-аккаунтом

## Связка с hook

Hook **deny** опасные shell-команды. Ты не обходишь hook через «другую формулировку» скрипта с тем же эффектом. Если пользователь **явно** просит clear/import — остановись, переспроси последствия одной фразой, не делай молча.
