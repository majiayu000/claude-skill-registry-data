---
name: '1C EDT: оформление модулей'
description: >-
  Use when writing or reviewing BSL in a 1C:EDT project (not a configurator file
  dump): module text, structure, names, comments, and the Отказ parameter.
---
# 1C EDT: оформление модулей

Apply when editing `.bsl` inside a 1C:EDT project. Sources live in the EDT tree (`src/CommonModules/<Имя>/Module.bsl`, `src/<Вид>/<Имя>/ObjectModule.bsl`, `ManagerModule.bsl`, `Forms/<Форма>/Module.bsl`, metadata in `.mdo`). Do not use configurator dump paths (`Ext/`, `ConfigDumpInfo.xml`) and do not rewrite EDT metadata into a dump layout.

Rules below are a working checklist distilled from 1C ITS standards (v8std). They are not a copy of the articles. Open the linked standard when a case is ambiguous.

## Text (№456)

- Write identifiers and comments in Russian. Foreign names are allowed only for web services and external systems.
- Do not use «ё» in code. It is allowed in user-visible interface strings.
- No non-breaking spaces and no non-standard dashes.
- Do not leave unused procedures, commented-out code, debug leftovers, TODO/MRG notes, or comments that change a query.
- One statement per line. Similar assignments may share a line.
- Indent with tabs. Tab width is 4.
- Wrap lines longer than 120 characters when it stays readable.
- Comments are short and only where the code is not obvious. A short note stays on the same line, a longer one goes above the code.

## Module structure (№455)

Order the regions that apply: header, variables, public interface, event handlers, service procedures and functions, initialization.

- Name regions by the same rules as variable names. Do not leave empty regions.
- Export routines meant for other objects or programs go in the public interface.
- Routines used only by this object, its forms, or its commands stay in the service section.
- Each form or element event has its own handler. Shared logic moves to a separate routine.
- Every module variable has a comment that says why it exists.
- Keep related service routines together. Initialization code stays in the initialization section.

## Names of procedures and functions (№647)

- Names come from the domain language and show the purpose.
- No spaces. Each word starts with a capital letter.
- Do not encode parameter or return types in the name unless the name is unclear without it.
- A procedure is an infinitive verb (the action).
- A function is named after the value it returns. Use `Новый` for constructors, `Это` or a participle for checks. If the function’s real job is an action, an infinitive is fine.

## Documentation comments (№453)

- Document the public programming interface.
- Document a routine when the behavior is not obvious. Skip a comment that only repeats the name or says it is an event handler.
- The comment sits immediately before the declaration, and before compiler directives. Separate declarations with a blank line.
- Parameter and return types are real platform types or types EDT supports. For an array, name the element type.
- For a function, describe what it returns. Add an example only when the call is easy to misuse.

## Parameters (№640, №641)

- Parameter names follow the same naming rules.
- Do not replace parameters with module variables or form attributes.
- Order parameters from general to specific. Required parameters come before optional ones with defaults.
- Prefer about seven parameters or fewer, and about three defaults or fewer. Many related values go into a structure, or the operation is split.
- Do not drop a required argument. Pass `Неопределено` explicitly, or make the parameter optional.
- A structure or value table passed as a parameter has a constructor that returns the template. Property names match the callee’s parameters. Defaults are filled in the constructor. In a library interface, document every property and column, including nested ones. Callers do not invent extra properties.

## Variable names (№454)

- Domain terms, each word capitalized, no spaces.
- Do not start a name with an underscore.
- No one-letter names except loop counters.
- A flag is named for the condition that makes it `Истина`.

## Parameter Отказ (№686)

- Never assign `Ложь` to `Отказ`. That clears a refusal already set by another check or subscription.
- On failure, set `Отказ` to `Истина` without wiping a previous `Истина` (`Отказ = Отказ Или <проверка>` or set only when the check failed).
- The same ban applies to `СтандартнаяОбработка` and `Выполнение`: do not reset them to the “allow” value.
- When an object event sets refusal, tell the user the reason (message or exception).

## Sources

- https://its.1c.ru/db/v8std/content/456/hdoc
- https://its.1c.ru/db/v8std/content/455/hdoc
- https://its.1c.ru/db/v8std/content/647/hdoc
- https://its.1c.ru/db/v8std/content/453/hdoc
- https://its.1c.ru/db/v8std/content/640/hdoc
- https://its.1c.ru/db/v8std/content/641/hdoc
- https://its.1c.ru/db/v8std/content/454/hdoc
- https://its.1c.ru/db/v8std/content/686/hdoc
