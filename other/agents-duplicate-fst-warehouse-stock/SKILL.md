---
name: fst-warehouse-stock
description: >-
  Склад Otgruzka/FST: документы прихода/расхода, движения, остатки, журналы,
  аудит, отмена через сторно (не удаление SLE). Use when working on warehouse,
  stock movements, inventory ledger, journals warehouse_*, приход/расход,
  остатки, инвентаризация, погрузка, nomenclature, as-of snapshot склада.
---

# Склад · движения · журналы (fst-warehouse-stock)

Источник лучших практик с GitHub (адаптировано под FST, **без** переноса чужой БД/скриптов):

| Источник | Зачем |
|----------|--------|
| [avansaber/erpclaw](https://github.com/avansaber/erpclaw) Inventory | Draft → Submit → Cancel; immutable stock ledger; cancel = reversal; отчёты balance/ledger |
| `references/erpclaw-inventory.md` | Выжимка Inventory-раздела upstream |
| Lean SCOR (опц.) | Операции склада — см. `references/warehouse-ops.md` |

**В приложении не ставим ERPClaw SQLite / MCP Dolibarr.** Канон — `src/lib/warehouse/*` + Firestore `otgruzka-tovara`. Скил учит агента **как** вести склад и журналы в этой кодовой базе.

## Когда читать

- Правки прихода/расхода/перемещения/инвентаризации
- Движения (`StockMovement`), остатки, as-of
- Журналы `warehouse_movements` / `warehouse_documents` / `warehouse_audit`
- «Почему остаток X», «кто списал», «сторно документа»
- Погрузка / очередь РС / номенклатура

## Канон в коде FST

| Что | Где |
|-----|-----|
| Типы / движения / документы | `src/lib/warehouse/types.ts` |
| Проведение / черновик / сторно | `src/lib/warehouse/documents.ts` |
| Остатки / дельты / as-of | `src/lib/warehouse/stock.ts` |
| Карточка движений по позиции (ledger) | `src/lib/warehouse/stockLedger.ts` |
| Аудит склада | `src/lib/warehouse/audit.ts` |
| Журнал (лента) | `src/lib/journals/collect.ts` → `warehouse_*` |
| UI движений | `WarehouseMovementsTab` |
| UI документов | `WarehouseDocumentsTab`, `WarehouseDocumentEditor` |
| UI аудита | `WarehouseAuditTab` |
| Журналы UI | `JournalsPage`, `JournalDocumentTrail` |
| As-of | `AsOfSnapshotBar` + `compute*AsOf` |

## Жёсткие правила (из ERPClaw → FST)

1. **Черновик не двигает остаток** — `saveWarehouseDocumentDraft` без `movements`.
2. **Проведение = движения** — `postWarehouseDocument` / `postExistingWarehouseDocument` создают `StockMovement` с `documentId`.
3. **Не удалять движения проведённого документа** — `deleteStockMovement` уже отказывает при `documentId`. Отмена = **сторно / unpost**, не правка старых строк «на месте».
4. **SLE по смыслу иммутабельны** — история движений — источник правды для остатка; не «чинить» остаток тихой правкой quantity в старой записи.
5. **Журналы = мониторинг** — события и документы видны в `journals` с категориями склада; trail связывает документ ↔ движения.
6. **As-of** — срезы остатков/движений через `asOfIso`, не дублировать фильтры ad-hoc.
7. **Данные Firestore священны** — не заливать локальный склад поверх облака.
8. **i18n** — RU+KA (+EN) синхронно.

## Жизненный цикл документа

```
draft ──post──► posted ──cancel/unpost──► cancelled / draft
  │                │
  │                └── movements (+audit)
  └── без movements
```

Покупной приход по накладной — через документ прихода (и реестр счетов), не «голое» движение без документа, если есть номер накладной (анти-двойной учёт, как PO→Receipt в ERPClaw).

## Мониторинг (что проверять)

| Вопрос | Где смотреть |
|--------|----------------|
| Что двигалось сегодня? | Склад → Движения / Журналы → «Склад · движения» |
| Кто провёл документ? | Журналы → документы / аудит |
| Остаток позиции по цепочке | Ledger по itemId (`buildItemStockLedger`) |
| Было ли на дату T? | As-of на складе / в журналах |
| Связь движение↔документ | `JournalDocumentTrail` |

## Чеклист перед сдачей складской правки

- [ ] Черновик не меняет баланс
- [ ] Проведение пишет movements + audit
- [ ] Документные движения нельзя hard-delete
- [ ] Журнал показывает событие / документ с корректным `link` / trail
- [ ] As-of не сломан
- [ ] i18n RU+KA(+EN)
- [ ] Не трогали Firestore import/clear

## Запрещено этим скилом

- Подмена склада на ERPClaw / Dolibarr / другую ERP
- Массовый rewrite складского стора
- Удаление исторических movements «чтобы сошлось»
- Deploy / cloud overwrite без явной просьбы
