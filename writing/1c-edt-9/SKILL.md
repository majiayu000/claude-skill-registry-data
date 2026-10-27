---
name: '1C EDT: прикладные объекты'
description: >-
  Use when writing object modules, manager modules, collections, posting, or
  form data conversion in a 1C:EDT project.
---
# 1C EDT: прикладные объекты

Apply when writing object modules, manager modules, register writes, or form data conversion in a 1C:EDT project (`ObjectModule.bsl`, `ManagerModule.bsl`, form `Module.bsl` under `src/`). Checklist distilled from ITS v8std, not a copy of the articles.

## Where the code lives (№486, №544)

- Behavior of one instance, and work with its data, lives in the object module.
- Logic that does not need an instance lives in the manager module. A manager function must not require an object.
- Logic shared by several metadata objects lives in a common module.
- `ПолучитьОбъект` loads the whole object. Do not call it to read one attribute.
- Command modules and common-command modules have no export procedures or functions.

## Creating and copying (№451, №448)

- Create an applied object with its manager. Do not use `Новый` when a manager exists.
- After creation, call `Заполнить`. If there is nothing to fill from, pass `Неопределено`.
- A full load from exchange or from an XML copy of the database may skip that.
- Copy rows of a similar structure with `ЗаполнитьЗначенияСвойств`. Do not walk columns to find a match on every row.

## Collections (№452, №781, №782, №693)

- Index a column of a large value table when you search it often and the column is selective.
- Do not use `Найти` to search several columns of a large table.
- For `НайтиСтроки`, the indexed fields must match the search. A partial index does not apply, including a copy with a filter.
- A large array is a map or an indexed value table. Replace an unindexed value tree with a table, and enforce uniqueness once at the end.
- Sorting references loads their presentations from the database for every row. If you sort by name, store the presentation in a column first. Otherwise sort references with `СравнениеЗначений`, especially on a large or hot table.
- Mass string building uses `СтрСоединить` (collect the parts, use `СтрРазделить` when you start from one string). Do not concatenate with `+` across thousands of iterations, long strings, or a loop. A handful of concatenations may stay as `+` if that reads better.
- A structure constructor takes at most three properties. More than that is `Вставить` or a direct assignment.
- Do not nest another parameterized constructor inside a structure constructor, and do not call a function with more than three parameters there.
- A fixed structure is built with its properties and defaults already present.
- A structure that came from outside, or the platform form parameters, may break these constructor limits.

## Registers, posting, spreadsheets (№447, №450, №449)

- Read information-register rows with a query when you will not change them.
- Use the record manager only when the filter is every dimension at once. Otherwise use a record set. The record manager can do extra work, and the set handlers still run.
- Do not write register sets by hand inside posting. Let the platform write movements when posting finishes.
- An explicit write is only when a later step in the same procedure must read those movements. An extra write under concurrency causes lock waits.
- Do not put a reference into a spreadsheet cell whose fill type is “parameter”. Pass the presentation. Passing the reference is acceptable only when building the presentation up front would hit the database about as hard. Measure it, and count the hidden joins.

## Forms, choice, DCS (№411, №409, №407)

- Choice parameters and choice-parameter links that always apply are set on the metadata object. A form overrides them only when the scenario differs.
- Set them on objects that are not edited interactively too. Reports and dynamic lists use them.
- Do not always clear a dependent value. Check, and clear only when the current value is no longer allowed.
- Do not clear it when the user picks the same leading value again, or when the dependent value is still valid.
- An unconditional clear is only when the link is one-to-one and the same leading value cannot be chosen again unchanged.
- Creating an object from a choice form passes the restrictions in the filter structure so `ОбработкаЗаполнения` sees them.
- In a form module, convert form data with `РеквизитФормыВЗначение`. Use `ДанныеФормыВЗначение` when you must, and then name the type. They are equivalent in result and cost.
- Do not add a report parameter when a user filter is enough.
- Do not make a parameter required only so the user cannot turn it off.
- Use a DCS `{ГДЕ ...}` so turning the parameter off turns the condition off too.

## Sources

- https://its.1c.ru/db/v8std/content/452/hdoc
- https://its.1c.ru/db/v8std/content/447/hdoc
- https://its.1c.ru/db/v8std/content/448/hdoc
- https://its.1c.ru/db/v8std/content/450/hdoc
- https://its.1c.ru/db/v8std/content/449/hdoc
- https://its.1c.ru/db/v8std/content/451/hdoc
- https://its.1c.ru/db/v8std/content/486/hdoc
- https://its.1c.ru/db/v8std/content/544/hdoc
- https://its.1c.ru/db/v8std/content/411/hdoc
- https://its.1c.ru/db/v8std/content/409/hdoc
- https://its.1c.ru/db/v8std/content/407/hdoc
- https://its.1c.ru/db/v8std/content/693/hdoc
- https://its.1c.ru/db/v8std/content/781/hdoc
- https://its.1c.ru/db/v8std/content/782/hdoc
