---
name: '1C EDT: разработка интерфейсов'
description: >-
  Use when writing managed form modules, list forms, print commands, or user
  dialogs in a 1C:EDT project.
---
# 1C EDT: разработка интерфейсов

Apply when writing managed form modules, list forms, print commands, or user dialogs in a 1C:EDT project (`Forms/<Форма>/Module.bsl` and `Form.form`). This is implementation, not the 8.3 layout standard (that skill covers sections, totals, and 1280×768). Checklist distilled from ITS v8std, not a copy of the articles.

## Opening and the form module (№404, №741, №630, №800, №742)

- Open a form with `ОткрытьФорму`. Do not get the form and open it by hand.
- Opening parameters are declared on the form and passed into `ОткрытьФорму`. Do not set up elements after the form is already open.
- Return a result through the notification and `Закрыть`.
- Do not open another form from `ПриОткрытии`, and do not open and close a form in one handler.
- The main list, processor, and report forms stay available from “All functions”.
- A parameterized form that cannot be opened from “All functions” is not the main form. If it is the only form, it is the main one and a missing parameter fails on the server with a clear error.
- Parameters are declared on the Parameters tab. Read them directly. Do not test whether the property exists.
- The form module holds only what this form needs. No general export routines. Those live in the object, manager, or a common module.
- Do not use an export form method to pass parameters at open or to refresh another form. Use `ОткрытьФорму`, a notification, and `Оповестить`.
- Shared client and server logic is a context-free procedure. Pass the context in.
- Change an object only because the user asked. They can cancel and keep the original.
- Do not write an object without a clear intent. If a save is surprising, explain it and offer to cancel.
- Do not write an object you got from `РеквизитФормыВЗначение`.
- Do not change the object in the open, read, and save handlers listed by the standard. A new object is filled in `ОбработкаЗаполнения`.
- Do not force `Модифицированность` to `Ложь`.
- An ordinary form that is one continuous task blocks the owner window. A workplace that needs other forms, comparison, many links, or a parameterized report opens independently.
- Do not use the separate-window mode on 8.3.9 or earlier, unless the configuration is limited to that client.

## Server calls, collections, appearance (№703, №636, №628, №710, №734, №399, №536, №545, №537)

- No modal forms or dialogs when the web client is supported. Modal usage is “do not use”. Calls are asynchronous.
- Do not start an asynchronous call from `ПриЗавершенииРаботыСистемы`. In `ПередЗавершениемРаботыСистемы`, cancel the exit and continue it from the completion notification.
- Turn on the check for synchronous calls. Exclude a real server or non-web case by hand.
- A contextual server call is for when the platform’s transfer of the form context is worth the cost. Otherwise the call is context-free and carries only the data it needs.
- Do not make a contextual or implicit server call from a client handler where it is forbidden. Defer it, or use a context-free call.
- Row activation uses a one-shot wait handler and does not repeat work for the same row.
- Do not pass a form collection or a spreadsheet by value. Process it on the server through an explicit call.
- A form collection is transferred in portions. About 20 rows or more is iterated on the server. `НайтиСтроки` runs on the server, preferably in one call.
- Do not hide a whole table row with conditional appearance. Prefer the dynamic list’s own conditional appearance when it is enough.
- Set conditional appearance in form code, during creation. Do not change it later, except while generating controls. Prefer references and metadata over string literals.
- From compatibility 8.3.3, vertical scrolling is usually “Automatic”. A form with HTML, formatted text, a text document, or a spreadsheet that is not a report uses “When necessary”. Recheck forms that were created on 8.3.2 or earlier.
- A conditional ban on editing a table cell is a warning on the field, not a silent lock. The text is set on the form. Update it when the row activates or the inputs change. An existing invalid value stays editable so the user can clear it.
- Do not rely on controls the platform builds by itself. It recreates them and drops your property changes. Reapply button and panel settings after that.
- Code cannot assume a control the user added with “edit form” is there. `CurrentPage` and `CurrentItem` may be `Неопределено`. Check before reading properties.
- A command that changes object data, or might, has “changes data” set. A confirmation or a branch that sometimes does nothing does not clear the flag.

## Lists (№489, №495, №397, №558, №702, №732, №745, №768, №744, №730)

- Group a dynamic list when the set is reliably small. A large list groups only by indexed fields. A multi-level group needs the first field indexed and selective. Do not group by characteristics. Do not expand the whole tree at once. Hide the search bar only when the standard search cannot do the main task.
- A list command must accept a selection that includes group rows. Skip group rows when the command works on objects. If the only selected row is a group, warn the user.
- Related scenarios share one parameterized list form. Columns, filters, order, and the title come from the parameters. It is the main list form, and opening it with no parameters still works.
- Each scenario is its own common command. The form title matches the command. The commands sit in the right subsystems, workplaces, and forms. Settings are stored per usage context.
- After a list command changes an object, refresh the list. Several objects: one notification, not a refresh per row. A dynamic list with no main table is refreshed when its data changes. A change made in another form uses the post-save notification. Check the notification name. If several objects changed, the reference is `Неопределено`.
- A list of reference objects includes `Ссылка`, and the user may hide it. Characteristics and extra attributes may keep it. An invisible column is not available in code, because the user controls visibility. “Always use” loads the column even when it is hidden. Set that only when an algorithm needs the column, such as printing.
- Keep the dynamic-list query simple. Precompute a heavy status. Prefer dynamic reading. A non-dynamic read is for a small set, especially with no main table.
- Index fields used in joins, filters, order, grouping, and frequent user sorts. Do not index everything.
- Do not add a heavy `РАЗЛИЧНЫЕ` or `СГРУППИРОВАТЬ ПО`, a conditional expression in a filter or join, or an order by a computed condition, without a reason.
- Few real tables in joins, ideally one. No nested-query or virtual-table joins unless you can justify them. A temporary table only if it is small. A composite field is narrowed on purpose.
- The query in the editor is the full query you use most often. An alias of a table that code may replace ends with `Переопределяемый`.
- On first server creation, set the query and the main table before you touch list settings. Do not read settings between changing the query and the main table. Use the standard helper when the configuration has one. The design-time query matches the default query in code.
- Selection history stays Auto for most objects. Turn it off when repeat choice is useless or the choice is custom. Then the drop-down button is No, the choice button is Yes, and the button is shown in the field. A filled choice list or quick choice can leave the field settings as they are.
- Prefer a native control over an HTML document field. A link is a button, a hyperlink label, or a formatted string. HTML is for a read-only guide or an illustrated instruction, and it must render in every supported client and browser.

## Dialog, long operations, print (№400, №418, №700, №642, №755, №548, №789, №468, №430)

- A fill error is shown in the message panel and checked before the write transaction. An integrity check runs inside the transaction. On failure, cancel the write and tell the user.
- A log of what was done goes in its own field or form. A serious error is its own dialog. If the user can fix it, offer the fix.
- Say that a command succeeded only when the result is not obvious. Do not repeat an obvious one.
- If the form is not visible, notify when the work finishes. Client progress uses the form state. Do not use that state for a server operation.
- A message to the user is `СообщениеПользователю`, or the library `СообщитьПользователю`. Do not call `Сообщить`.
- Installing an add-in or a platform extension is the user’s own choice. The dialog says what it is for and what happens if they refuse. Offer it before the action that needs it. The user can install it later from settings or administration. File work uses the library procedures, not the obsolete global methods.
- Work that usually takes longer than about 8 seconds runs in a background job. After start, wait at most 0.8 seconds, then poll with a wait handler. Show an indicator or a blocking form with cancel.
- A long report does not block the form. The user can change settings. Closing the form cancels the build.
- Do not start a background job or write data in exclusive mode. Block those actions.
- The background procedure name is explicit. Parameters that came from the client are prepared on the server.
- Do not run a long operation in a wait handler or in a form-element event. Long client code starts only from an explicit user action. A network check or an update check runs on the server or from its own command. Do not probe a network path on every change of the path field.
- Printing needs the right to read the data and the right to run the print command.
- Several objects are printed with one query, then the result is processed.
- The printout keeps the rows of the on-screen tabular section, in the same order. Do not add a grouping. Print the line number. If the screen has none, number the rows in order. Sort by the line number so the order is the same on every DBMS.
- Do not cut data off, and do not set margins below the printer’s physical limit, including zero margins.
- The print-data template area `ДанныеПечати` keeps its fields. Do not rename or delete a field. Adding a field is allowed. If the area is missing, create it before you change attributes or tabular sections.
- Check that a template area exists before you get it. Fill parameters with a universal method, not a direct assignment.
- A required template change turns the user’s template off and tells them. An optional change still works with the old template.
- The object synonym is short and clear. A short object name is singular when the synonym does not fit. An extended name only when the short one is not enough. Lists are plural and understandable. Add one full sentence of explanation when the name does not show the purpose. A top-level subsystem with a command interface uses a 32×32 picture.
- Give a shortcut to an action people use often. A reserved shortcut stays on the action the standard names. Do not reuse it. Keep the platform shortcuts (copy, find, print, undo, and the rest of that list) and the applied ones the standard lists (full-text search, barcode search).

## Sources

- https://its.1c.ru/db/v8std/content/404/hdoc
- https://its.1c.ru/db/v8std/content/741/hdoc
- https://its.1c.ru/db/v8std/content/630/hdoc
- https://its.1c.ru/db/v8std/content/800/hdoc
- https://its.1c.ru/db/v8std/content/742/hdoc
- https://its.1c.ru/db/v8std/content/703/hdoc
- https://its.1c.ru/db/v8std/content/636/hdoc
- https://its.1c.ru/db/v8std/content/628/hdoc
- https://its.1c.ru/db/v8std/content/710/hdoc
- https://its.1c.ru/db/v8std/content/734/hdoc
- https://its.1c.ru/db/v8std/content/399/hdoc
- https://its.1c.ru/db/v8std/content/536/hdoc
- https://its.1c.ru/db/v8std/content/545/hdoc
- https://its.1c.ru/db/v8std/content/537/hdoc
- https://its.1c.ru/db/v8std/content/730/hdoc
- https://its.1c.ru/db/v8std/content/744/hdoc
- https://its.1c.ru/db/v8std/content/489/hdoc
- https://its.1c.ru/db/v8std/content/495/hdoc
- https://its.1c.ru/db/v8std/content/397/hdoc
- https://its.1c.ru/db/v8std/content/558/hdoc
- https://its.1c.ru/db/v8std/content/702/hdoc
- https://its.1c.ru/db/v8std/content/732/hdoc
- https://its.1c.ru/db/v8std/content/745/hdoc
- https://its.1c.ru/db/v8std/content/768/hdoc
- https://its.1c.ru/db/v8std/content/468/hdoc
- https://its.1c.ru/db/v8std/content/430/hdoc
- https://its.1c.ru/db/v8std/content/642/hdoc
- https://its.1c.ru/db/v8std/content/755/hdoc
- https://its.1c.ru/db/v8std/content/548/hdoc
- https://its.1c.ru/db/v8std/content/789/hdoc
- https://its.1c.ru/db/v8std/content/400/hdoc
- https://its.1c.ru/db/v8std/content/418/hdoc
- https://its.1c.ru/db/v8std/content/700/hdoc
