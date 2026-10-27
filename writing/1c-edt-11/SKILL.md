---
name: '1C EDT: обработчики объектов'
description: >-
  Use when writing object event handlers, predefined items, constants, or
  document posting rules in a 1C:EDT project.
---
# 1C EDT: обработчики объектов

Apply when writing object-module event handlers, predefined data, constants, or posting rules in a 1C:EDT project (`ObjectModule.bsl` and manager module under `src/`). Checklist distilled from ITS v8std, not a copy of the articles. The `Отказ` parameter is in the module-layout skill.

## Write, delete, copy (№464, №465, №752, №466, №773)

- `ПередЗаписью` fills and checks attributes, including links to outside data, and is the place to read the previous values from the database.
- `ПриЗаписи` writes related data and reacts to the fact the object changed. Do not change the object itself. It is already in the database.
- `ПередУдалением` does the cleanup, such as clearing the owner’s references. That code may see data that is already cleared.
- `ПриКопировании` clears attributes that belong only to the source. Do not copy data that is about that one object.
- In `ПередЗаписью`, `ПриЗаписи`, `ПередУдалением`, and in subscriptions to those events, the first check is `ОбменДанными.Загрузка`.
- When the flag is set, skip business logic, checks, and extra changes. Exchange must store the data as it arrived.
- An exception to that skip is allowed only with a comment that says why.
- The caller who set the flag is responsible for integrity. Extra fill after load belongs in an export procedure of the object.
- Turn off object registration for the loaded data with `ОтключитьМеханизмРегистрацииОбъектов` when the exchange must not register them.

## Fill and presentation (№463, №396, №746)

- `ОбработкаПроверкиЗаполнения` is for a check that metadata cannot express. For a conditional check, remove the attributes that should not be checked from `ПроверяемыеРеквизиты`, collect them, and delete them with the standard procedure.
- Do not hide a conditional check in some other scheme that the fill settings do not show.
- This handler is not called on every programmatic write. Checks here run outside the write transaction.
- Integrity checks belong in the transactional write or posting handlers. Do not load the transaction with checks, and check every path that can change the data.
- Restrictions of “create based on” live in `ОбработкаЗаполнения`. Tell the user why with an exception. Do not add a separate command or move the check into an extra command handler just for that.
- Fill from `ДанныеЗаполнения` first, by its type. Then fill defaults only for attributes that are still empty. Prefer the metadata fill value when it is enough.
- Override a presentation in the manager handlers `ОбработкаПолученияПредставления` and `ОбработкаПолученияПолейПредставления` when the default is wrong.
- Those handlers do not run queries, do not get objects, and do not dot through a reference. Use as little data as possible.
- Do not touch a predefined item there that may be missing during exchange. Keep thick client, managed application, and client-server in mind.

## Predefined, constants, inactive, posting (№697, №632, №638, №603)

- Predefined items are created automatically. Leave `ОбновлениеПредопределенныхДанных` on `Авто`. Do not switch that mode from code without a reason.
- Users must not have the right to delete predefined items.
- In a subordinate DIB node, load predefined items before any code that uses them. Do not touch them in load logic until that is guaranteed.
- A table that is not in the DIB exchange plan uses `ОбновлятьАвтоматически`, not `Авто`.
- A conditional predefined item has auto-update off, and the code handles its absence.
- Write constants outside a transaction. Do not “fix” the lock by caching every constant in session parameters or common modules. Two sessions writing the same constant block each other.
- Do not delete an obsolete object if existing data can still reference it.
- Store an “inactive” flag, default `Ложь`, or use the library common attribute. Hide inactive items in autocomplete and quick choice, with a parameter to show them on purpose. Warn the user who picks one.
- Lists and choice forms filter inactive items out and offer a command to show them. The item form can mark and unmark inactivity, or use a checkbox.
- Marking for deletion also sets inactive. Unmarking deletion does not clear inactive.
- Most documents are posted, so the event lands in accounting. Do not apply business checks to an unposted draft.
- Do not post a document that is not for accounting, or one whose posting technology does not fit.
- If recording the event and reflecting it in accounting are one action, write the document in posting mode.
- Secondary data is written to registers on posting, automatically or by hand.
- An unposted or deletion-marked document has no active movements.
- Reposting does not rewrite movements when the data that posting depends on did not change.
- Posting uses the data stored on the document. Keep the dependence on settings small, and update the algorithm when the logic changes.

## Sources

- https://its.1c.ru/db/v8std/content/464/hdoc
- https://its.1c.ru/db/v8std/content/465/hdoc
- https://its.1c.ru/db/v8std/content/752/hdoc
- https://its.1c.ru/db/v8std/content/466/hdoc
- https://its.1c.ru/db/v8std/content/463/hdoc
- https://its.1c.ru/db/v8std/content/396/hdoc
- https://its.1c.ru/db/v8std/content/746/hdoc
- https://its.1c.ru/db/v8std/content/773/hdoc
- https://its.1c.ru/db/v8std/content/697/hdoc
- https://its.1c.ru/db/v8std/content/632/hdoc
- https://its.1c.ru/db/v8std/content/638/hdoc
- https://its.1c.ru/db/v8std/content/603/hdoc
