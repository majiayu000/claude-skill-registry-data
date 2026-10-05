---
name: fst-action-journals
description: >-
  Журналы действий Otgruzka: appendAudit, hrJournal, itemHistories, warehouse.auditLog.
  Use when adding mutations, renaming (people, brigades, items, meals), or auditing
  whether an action is logged. Before claiming «есть журнал».
---

# Журналы действий Otgruzka

Правило: `.cursor/rules/fst-action-journals.mdc`<br>
Карта дыр: `.cursor/context/JOURNALS_AUDIT.md`

## Когда читать

- Новая кнопка Сохранить / Провести / Удалить / Переименовать
- Смена ФИО, названия бригады, номенклатуры, комплекса, роли
- Раздел «Журналы» не показывает действие
- Перед фразой «всё пишется в журнал»

## Куда писать

| Действие | API |
|----------|-----|
| Табель, HR карточка, доступ, финансы, обеды, справочники | `appendAudit(store, { action, detail, oldValue?, newValue?, ...actorAuditFields(getActor) })` |
| Склад док / движение / погрузка | `appendWarehouseAudit` |
| Переименование позиции склада | `appendItemHistory` (`itemHistories`) |
| ФИО / бригада / ЗП / должность сотрудника | `appendEmployeeJournal` через `applyEmployeeMovementJournal` |
| Закупка статусы | `statusHistory` на заказе (collect уже читает) |

Лента UI: `collectJournalEntries` + `classifyAuditEntry`. Роли видят не все категории (`journals/access.ts`).

## Чеклист новой мутации

- [ ] `appendAudit` или доменный журнал в том же `setStore`
- [ ] actor `by` / `byName`
- [ ] rename: `old → new` в `detail`
- [ ] новый `action` в `AuditEntry` + label + classify
- [ ] если сущность долгоживущая (сотрудник, item) — ещё `hrJournal` / `itemHistories`
- [ ] i18n не обязателен для `AUDIT_ACTION_LABEL` (сейчас RU в коде); HR-виды — `hr/labels.ts` RU+KA

## Кольца (не вечные)

`auditLog` 2000, `warehouse.auditLog` 300, `hrJournal` 200. История ФИО живёт на карточке (`hrJournal`), не только в кольце.

## Не делать

Полный rewrite логгера, отдельная БД аудита, логирование каждого клика UI.
