---
name: '1C EDT: конструкции языка'
description: >-
  Use when writing or reviewing BSL constructs in a 1C:EDT project: expressions,
  preprocessor, types, variables, the event log, and exceptions.
---
# 1C EDT: конструкции языка

Apply when writing or reviewing BSL in a 1C:EDT project (`.bsl` under `src/`, not a configurator dump). Pair with the module-layout skill. This is a checklist distilled from ITS v8std, not a copy of the articles.

## Expressions (№441, №444)

- Spell language keywords in the canonical form.
- Align only neighboring assignments, not the whole module.
- Do not compare a Boolean with `Истина` or `Ложь`. Put a heavy expression in a temporary variable before comparing it.
- Prefer platform constants such as `Символы.ПС`.
- Wrap lines past 120 characters unless wrapping makes the line worse.
- Arithmetic operators start the continuation line. Indent continuation operands the same way.
- Split long string literals with the platform line-break form. Do not split text that the user sees in `СообщениеПользователю`.
- String `+` usually starts the next line. At the end of the previous line is acceptable for a long concatenation.
- Parameter lists and complex conditions use one consistent indent. Formatter output is fine.

## Duplication and client/server split (№440, №439)

- Do not copy the same behavior. Move a reused routine to a common module.
- Duplication is acceptable when the copies are expected to diverge.
- Compiler directives (`&НаКлиенте`, `&НаСервере`, and the rest) belong only in managed form modules and command modules. Other modules use preprocessor instructions.
- Do not use `#Если Сервер` or `#Если Клиент` in a client-server common module to pick the context. Put client code and server code in their own common modules. The client-server module keeps only the shared part.
- Client-mode branches (`ВебКлиент`, thin, thick) are allowed in client modules.
- Do not cut an expression, a declaration, a call, or another grammar construct with a preprocessor instruction or a region.

## Types and metadata (№442, №445)

- Get a type with `ТипЗнч` and `Тип`. Do not guess it from a metadata name or another indirect sign.
- If the metadata kind is known, call `Метаданные()` on that object or reference. Do not search the global `Метаданные` collection for a known kind.
- If the kind is unknown, use `Метаданные.НайтиПоТипу`.

## Form handlers and variables (№492, №639, №494)

- A form handler attached from code is named with the prefix `Подключаемый_`.
- Avoid module variables when a platform mechanism is clearer.
- Pass extra data into object-module handlers through `ДополнительныеСвойства`, not through exported variables. Non-exported object variables may link handlers inside that module.
- Return and error codes are strings, not numeric module variables.
- Cache an expensive repeated result in a reuse-return common module. On a form, do not cache a predefined value that is cheap to read.
- Inside one call chain, pass intermediate data as parameters. Between client calls, keep it in form attributes.
- Client form variables are for waiting, external events, and client element handlers. Session parameters on the client may live in application variables.
- Initialize a local variable before branches if later code depends on its type or value, so it does not stay `Неопределено`.

## Event log (№498)

- Add a log event only when the platform does not already record what an administrator needs.
- One event per write: event type, severity, comment. Severity matches the meaning (error, warning, information, note).
- Group event names by area. Do not put a document number or other instance data into the event type. Put metadata and data in their own parameters. Localize the event type and the comment.
- Do not pack several events into one comment, and do not write unbounded text (about 10 KB is the ceiling). For an exception, use the detailed error presentation.
- Do not query the event log on a hot path. Use a register or a dedicated platform object.

## Exceptions (№499, №790)

- Do not catch exceptions by habit. Let the platform show and log them.
- Catch only to add context (external resource, service, input, configuration failure). Keep the `Попытка` small so it does not hide an unrelated error.
- Do not parse localized exception text to decide the cause. Show the original text and add what the user was doing.
- Do not swallow an exception. If suppression is deliberate, say why in a comment and write the event log.
- Do not use `ОписаниеОшибки` or a short presentation when a detailed or user-facing helper exists.
- Do not raise exceptions for ordinary failures. A user-facing business error has no category unless a more specific one fits. Network, printer, and rights failures use their categories. Configuration defects use `ОшибкаКонфигурации`.
- Check rights with the dedicated method. An access-rights exception is only for a rare role check.
- If the caller must branch on the error, use a string code, a platform category, or a string passed to `ВызватьИсключение`. Prefix a code with the subsystem. Nested coded exceptions go through the library helper when the configuration uses one.
- Do not raise an exception just to block saving. Set `Отказ = Истина` and show every relevant message.

## Goto (№547)

- Do not use `Перейти`. It is forbidden in managed-client common modules, command modules, and client code of managed forms, because the web client does not support it.

## Sources

- https://its.1c.ru/db/v8std/content/441/hdoc
- https://its.1c.ru/db/v8std/content/444/hdoc
- https://its.1c.ru/db/v8std/content/440/hdoc
- https://its.1c.ru/db/v8std/content/439/hdoc
- https://its.1c.ru/db/v8std/content/442/hdoc
- https://its.1c.ru/db/v8std/content/445/hdoc
- https://its.1c.ru/db/v8std/content/492/hdoc
- https://its.1c.ru/db/v8std/content/639/hdoc
- https://its.1c.ru/db/v8std/content/494/hdoc
- https://its.1c.ru/db/v8std/content/498/hdoc
- https://its.1c.ru/db/v8std/content/499/hdoc
- https://its.1c.ru/db/v8std/content/790/hdoc
- https://its.1c.ru/db/v8std/content/547/hdoc
