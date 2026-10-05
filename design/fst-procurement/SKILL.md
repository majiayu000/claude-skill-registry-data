---
name: fst-procurement
description: >-
  Закупки Otgruzka/FST: заказы поставщикам (ЗЗ), статусы логистики, контейнерный
  трекинг, приёмка на склад, аналитика. Use when working on procurement,
  purchase orders, suppliers, containers, tracking, receive to warehouse,
  закупок, заказ поставщику, приёмка, контейнер, Maersk/MSC.
---

# Закупки (fst-procurement)

Источник лучших практик: [avansaber/erpclaw](https://github.com/avansaber/erpclaw) **Buying / procure-to-pay**<br>
(`references/erpclaw-buying.md`). **Не ставим ERPClaw SQLite** — только правила потока.

## Модель продукта Otgruzka (не полный P2P)

Фактический контур:

```
Поставщик → ЗЗ (draft…arrived) → трекинг контейнера → Принять → приход склада
```

| Этап ERPClaw | В FST |
|--------------|-------|
| Supplier | Контрагенты role supplier/both |
| RFQ / quotes | **Нет** — не строить без просьбы |
| Purchase order | `PurchaseOrder` / `ЗЗ-YYYY-NNNN` |
| Goods receipt | `receivePurchaseOrderInStore` → warehouse receipt |
| AP invoice / 3-way / pay | **Нет** (вложение invoice ≠ АП) — не строить без просьбы |

## Канон в коде

| Что | Где |
|-----|-----|
| Типы / статусы | `src/lib/procurement/types.ts`, `status.ts` |
| Приёмка | `src/lib/procurement/receive.ts` |
| Трекинг | `src/lib/procurement/tracking/*`, `server/tracking/*` |
| UI | `src/components/procurement/*`, `ProcurementPage` |
| Журналы | category `procurement` в `journals/collect.ts` |

## Жёсткие правила

1. **`received` только после приёмки на склад** (или ручного осознанного статуса) — **не** из carrier sync. Авто-статус с трекинга max = `arrived`.
2. **Приёмка пишет склад** — `purpose: 'purchase'`, comment = номер ЗЗ; не «голое» движение без документа при наличии заказа.
3. **Не удалять проведённый заказ** — только draft; иначе cancel.
4. **Черновик PO не двигает остаток**.
5. **Трекинг на Vercel** часто без `/api` — не обещать sync на веб-проде без сервера.
6. **Окно заказа** — `ModalBackdrop` с `dirty` + `onSaveDirty`.
7. **i18n** RU+KA(+EN). Данные Firestore священны.

## Чеклист аудита / правок

- [ ] Carrier не ставит `received`
- [ ] Приёмка доступна осознанно (не с draft без предупреждения)
- [ ] Журнал статусов + связь с приходом
- [ ] Контейнер: ref + carrier URL
- [ ] Не плодим RFQ/АП без явной просьбы

## Запрещено

- Rewrite закупок «под ERPClaw»
- Массовый clear/import облака
- Deploy без просьбы
