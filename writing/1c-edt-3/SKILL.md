---
name: '1C EDT: тексты запросов'
description: >-
  Use when writing or reviewing 1C query text in an EDT project: layout,
  aliases, unions, sorting, LIKE, and row counts.
---
# 1C EDT: тексты запросов

Apply when writing or reviewing query text in a 1C:EDT project: a query string in `.bsl`, a query in a template, or a DCS data set. Not a configurator dump. Checklist distilled from ITS v8std, not a copy of the articles. Query performance rules live in a separate skill.

## Layout (№437, №758)

- Query keywords are uppercase.
- A field alias always has `КАК`. Aliases are explicit and stable. Do not rely on a generated name.
- The query is several lines, not one long line.
- A complex query has a short comment. If the text is built in code, comment each stage. Keep fragments valid for the query wizard.
- Do not glue metadata names into the text. Pass dynamic fields and tables through parameters or a controlled replacement.
- Every source alias says what the source is in this query. Domain words, each word capitalized, no spaces.
- Do not start an alias with `_` and do not use a one-letter alias.
- Do not name a source just `Справочник` or `Документ` when that hides its role. A generic alias is only for a universal or fully dynamic query.

## How many queries (№436, №438)

- Do not run the same query inside a loop. Take the set with `В`, `ОБЪЕДИНИТЬ ВСЕ`, or a batch.
- Prefer a batch API of the library over one call per object.
- Split queries only when that is simpler, faster, or required by an update, a bulk job, or an import.
- Test an empty result with `Результат.Пустой()`. Do not open a selection only to see if it is empty.
- Skip `Пустой()` when the next step is to iterate the result anyway.

## Unions and joins (№434, №435)

- Prefer `ОБЪЕДИНИТЬ ВСЕ`. Use `ОБЪЕДИНИТЬ` only when duplicates must be removed.
- Avoid `ПОЛНОЕ ВНЕШНЕЕ СОЕДИНЕНИЕ`, especially on PostgreSQL. Rewrite it when a correct equivalent exists. Do not rewrite it mechanically if the rewrite is wrong.
- Do not use a full join together with a tabular section in `ВЫБРАТЬ`.

## Order (№412)

- Add `УПОРЯДОЧИТЬ ПО` when later code or the user depends on order. Do not assume an unordered result is stable.
- Normalize `NULL` sort keys, because DBMSs order them differently.
- User-visible lists sort by primitive values. A reference sorts by its presentation.
- Omit sorting when order does not matter, the rows are not shown, or there is exactly one row.
- With `РАЗЛИЧНЫЕ`, sort only by selected fields.
- Do not combine `ПЕРВЫЕ` with `АВТОУПОРЯДОЧИВАНИЕ`.
- `АВТОУПОРЯДОЧИВАНИЕ` is only when the exact order does not matter but the order must be stable across DBMSs. Comment why.

## Numbers and LIKE (№535, №726, №787)

- When the magnitudes are known, multiply before you divide.
- Force precision with `ВЫРАЗИТЬ(... КАК Число(m, n))` on the operands or the result. Use the smallest precision that still holds the value.
- Count rows with `КОЛИЧЕСТВО`, not `СУММА(1)`. If a conditional count cannot use `КОЛИЧЕСТВО`, widen the number with `ВЫРАЗИТЬ`.
- `ПОДОБНО` takes a string literal or a query parameter only. Do not build the pattern by concatenation or from a field.
- Portable patterns use only `%` and `_`. No character classes `[...]`. Pattern length is at most 1024.
- Escape a literal `_ % [ ] ^` and double the escape character. The escape is declared with `СПЕЦСИМВОЛ`. Putting it only in a parameter does not escape anything.
- Comparison is case-insensitive. Use the library search-string helper when the configuration has one.

## Sources

- https://its.1c.ru/db/v8std/content/437/hdoc
- https://its.1c.ru/db/v8std/content/436/hdoc
- https://its.1c.ru/db/v8std/content/438/hdoc
- https://its.1c.ru/db/v8std/content/435/hdoc
- https://its.1c.ru/db/v8std/content/434/hdoc
- https://its.1c.ru/db/v8std/content/412/hdoc
- https://its.1c.ru/db/v8std/content/535/hdoc
- https://its.1c.ru/db/v8std/content/726/hdoc
- https://its.1c.ru/db/v8std/content/758/hdoc
- https://its.1c.ru/db/v8std/content/787/hdoc
