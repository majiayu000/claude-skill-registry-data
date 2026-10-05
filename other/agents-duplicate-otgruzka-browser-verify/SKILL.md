---
name: otgruzka-browser-verify
description: >-
  Проверка багов и UX Otgruzka на веб-проде (Vercel), не на локали. Сверка бандла,
  экрана, console errors. Use after UI fixes, before «починено/задеплоено», or when
  reproducing user-reported bugs on production.
---

# Otgruzka — верификация на веб-проде

Ты **не** считаешь задачу выполненной, пока не проверил **канонический прод**, а не `npm run dev` и не локальный JSON.

| Канон UI | https://otgruzka-tovara.vercel.app |
| Зеркало | https://otgruzka-tovara.web.app (бандл может отличаться) |
| Данные | SQL Connect `otgruzka-tovara-service` — локаль не доказательство |

Правила: `.cursor/rules/fst-web-prod-truth.mdc`, `fst-data-integrity.mdc`<br>
Соседние скилы: `browser-testing-with-devtools`, `otgruzka-deploy-auditor`

## Когда применять

- Пользователь сообщил баг на проде (табель, HR, склад, обеды, печать…)
- После правки UI — перед фразой «починено» / «готово»
- После деплоя — проверить **экран**, не только хеш бандла
- Конфликт «у меня локально работает» vs «на вебе нет»

## Чеклист (обязателен)

### A. Подготовка

- [ ] Цель ясна: **раздел**, **месяц/дата**, **роль/учётка**, **ожидаемое поведение**
- [ ] Если был деплой — известен ожидаемый `index-….js` (см. `otgruzka-deploy-auditor`)
- [ ] **Ctrl+F5** / hard refresh — иначе старый бандл из кэша

### B. Открыть прод

- [ ] URL = **Vercel** (`otgruzka-tovara.vercel.app`), не только Hosting
- [ ] В HTML страницы есть актуальный `index-….js` (если после деплоя)
- [ ] Войти под ролью, релевантной симптому (повар → `cook`, табель → нужная бригада/месяц)
- [ ] Тот же **месяц / неделя / сотрудник**, что у пользователя

### C. Проверка на экране

- [ ] Дошли до нужного `#/…` (напр. `#/meals`, `#/month`)
- [ ] UI совпадает с задачей (кнопки, галочки, состав комплекса, табель…)
- [ ] Нет блокирующих toast/alert об ошибке sync
- [ ] Console: **нет** необработанных errors (warnings — зафиксировать, если шумят)

### D. Данные (осторожно)

- [ ] **Не** заливать локальный стор в SQL «чтобы совпало»
- [ ] **Не** `clear:*` / `import:cloud*` без явной просьбы
- [ ] Если на проде «пусто» — искать сбой pull/sync, не seed
- [ ] Тестовые правки на проде — только если пользователь явно разрешил; иначе read-only проверка

### E. Вердикт

Формат:

```
PROD VERIFY: PASS | FAIL | BLOCKED
url: …#/…
bundle: index-….js | n/a
role/month: …
observed: …
console errors: none | …
data touched: no | YES (что)
blockers: login needed / no access / …
```

`PASS` — симптом воспроизведён как **исправленный** или **подтверждён** по сценарию.<br>
`FAIL` — симптом на проде остаётся.<br>
`BLOCKED` — нет доступа/данных; написать, что нужно от пользователя.

## Типичные ловушки

1. Проверка на локали и вывод «работает»
2. Hosting vs Vercel — разные бандлы
3. Другой месяц/бригада/роль — «баг» на самом деле другие данные
4. Старый кэш без Ctrl+F5
5. «Починил» кодом, но **не задеплоил** — на проде старый бандл

## Связка с Addy

- DOM/console/network → `browser-testing-with-devtools` (MCP browser или DevTools)
- Перед merge крупного UI → `code-review-and-quality`
- Спорная бизнес-логика (ЗП, права) → `doubt-driven-development` + `fst-chain-context`

## Brownfield (этот проект)

Полный Addy lifecycle не обязателен на каждый чих. Для Otgruzka минимум:

1. `fst-chain-context` — что трогать
2. Тонкий срез — `incremental-implementation`
3. **Этот скил** — прод-верификация
4. Деплой — только по просьбе + `otgruzka-deploy-auditor`
