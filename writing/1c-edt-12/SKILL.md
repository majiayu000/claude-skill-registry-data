---
name: '1C EDT: локализация'
description: >-
  Use when writing user-visible text, formats, templates, or money fields in a
  1C:EDT project so they can be localized.
---
# 1C EDT: локализация

Apply when writing user-visible text, formats, templates, or money fields in a 1C:EDT project. Form items live in `Form.form`, templates in the EDT template object. Checklist distilled from ITS v8std, not a copy of the articles.

## Scope (№458, №769)

- Plan for several interface languages. Data entry is in one language, which may differ from the configuration’s main language.
- Do not treat simultaneous data entry in several languages as the standard, and do not require multilingual metadata stored inside the data.
- National specifics live in objects that are absent from the international configuration. A national attribute stays only if the configuration still works after it is removed.
- National form items and algorithms live in their own objects or in localization modules. Do not leave national fragments, marked with a localization comment, inside an international module.
- The international configuration must run, and its versions ship together with the national ones.
- List localizable objects in `ЛокализуемыеОбъекты….txt`. Build a national version on top of the international one.

## Strings in code (№761, №764)

- A string the user sees goes through `НСтр`. A bare literal is not allowed.
- Use a whole phrase and `СтрШаблон`. Do not split a sentence into pieces that are translated apart.
- Do not show an internal name or an identifier. Take the presentation from metadata.
- Do not pass `L=` into the format and declension functions named by the standard.
- Do not call the Russian-only `ПолучитьСклоненияСтрокиПоЧислу`. Use the multilingual variant.
- Dialog buttons use the platform button codes, or your own captions go through `НСтр`.
- Do not wrap an internal identifier in `НСтр`. A constant you reuse is a function that returns it.
- Do not branch algorithms on a localized presentation or a localized type name. Predefined values are compared by their configuration name.

## Queries, forms, formats (№762, №765, №763)

- A user-visible string literal does not sit inside a query or a DCS expression. Pass it as a parameter and localize it where the standard allows.
- A calculated or renamed report column has an explicit synonym. Do not rely on a title generated from the name or the alias.
- Substitution parameters are replaced in the result-composition handler.
- Do not assign a non-localized string to a form-item attribute. Use a value list or an enumeration.
- Every table and every group has a title. A hidden title is turned off explicitly.
- Delete a meaningless tooltip and a title on an invisible service attribute.
- A calculated or renamed dynamic-list column has an explicit title.
- A field with a choice list has `РежимВыбораИзСписка`.
- Localize a format string through `НСтр` in the cases the standard names. A format set on a form property is always localized.
- Prefer the local date format. A custom format is localized too.
- Localize a number format that has a text zero, a template, or a non-standard separator. A Boolean format is always localized.
- Do not override the locale with `L=`.
- Persist the machine value, not the localized text. Dates in exchange use ISO.
- A money field uses the dedicated money type, not a fixed `Число(15, 2)`. If that type is unavailable, use `Число(31, 2)` within the DBMS limit (№778).
- Get the money type from the library function, not from a `Число` constructor. In a query, cast money to `Число(31, 2)`.
- A number format states the decimal places only, not the total length.

## Jobs, templates, generated data (№767, №766, №784)

- A predefined scheduled job has no name set in the designer. The synonym is enough. Do not type the name by hand, or it will not localize.
- A parameterized job’s name is built in code and passed through `НСтр`.
- A language copy of a binary or HTML template has the suffix `_language-code`. Look up the current language, then the main language, then the base name.
- When building a template for a chosen language, set `КодЯзыка` or `КодЯзыкаМакета`.
- A template that must stay in one language has the language suffix and the language code, and is not translated.
- Template texts are UTF-8 and follow the same parameter rules. Merge templates that differ only by language. Mind the locale of an add-in.
- A string the configuration writes into the infobase for the user is in the data language, not the current user’s language. Pass the infobase main language code into `НСтр`. Mark that string as data, not as interface text.
- The same rule covers the initial fill of predefined items. Adding a predefined item updates the versioned fill handlers.
- With BSP, initial data goes in `ПриНачальномЗаполненииЭлементов`, not in a handler you invent.

## Sources

- https://its.1c.ru/db/v8std/content/458/hdoc
- https://its.1c.ru/db/v8std/content/769/hdoc
- https://its.1c.ru/db/v8std/content/761/hdoc
- https://its.1c.ru/db/v8std/content/762/hdoc
- https://its.1c.ru/db/v8std/content/763/hdoc
- https://its.1c.ru/db/v8std/content/764/hdoc
- https://its.1c.ru/db/v8std/content/765/hdoc
- https://its.1c.ru/db/v8std/content/767/hdoc
- https://its.1c.ru/db/v8std/content/766/hdoc
- https://its.1c.ru/db/v8std/content/778/hdoc
- https://its.1c.ru/db/v8std/content/784/hdoc
