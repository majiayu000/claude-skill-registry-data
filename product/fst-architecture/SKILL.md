---
name: fst-architecture
description: Deep architecture and conventions of the FST accounting app — modules (planner, sales, production, formulations/mixer, warehouse, technologist), AppStore/slices wiring, view/role registration, production chain, i18n, build and deploy. Use when implementing or extending features, adding a view/role/store/slice, wiring data flow, or needing how a domain module works. Reads one reference file on demand to save tokens.
---

# FST architecture

Компактная карта всегда в правиле `.cursor/rules/fst-architecture.mdc`.
Здесь — глубина по требованию. **Открывай ОДИН справочник по теме задачи**, не все сразу.

## Что читать под задачу

- Добавляешь/меняешь раздел (view) или роль/доступ → [references/views-roles.md](references/views-roles.md)
- Трогаешь стор / срез (slice) / персистентность / миграции → [references/data-store.md](references/data-store.md)
- Работаешь в домене (planner, sales, production, formulations/mixer, warehouse, technologist, procurement) → [references/modules.md](references/modules.md)
- Конвенции, i18n, печать, сборка, деплой → [references/conventions.md](references/conventions.md)

## Золотые правила

- Общий код — в `src/`; импорт через алиас `@` → `src/`.
- Новый `ViewId` регистрируется в 8 местах (полный чек-лист в `references/views-roles.md`).
- i18n: ключи добавлять синхронно в `src/i18n/ru.ts` **и** `src/i18n/ka.ts`.
- Полный `Record<AccessRoleId, …>` (напр. `journals/access.ts`) — при новой роли добавить ключ, иначе ошибка типов.
- Готовность: `npx tsc --noEmit` и `npm run build` зелёные; затронутые файлы — без линт-ошибок.
