---
name: '1C EDT: клиент-сервер'
description: >-
  Use when writing managed forms and client-server calls in a 1C:EDT project:
  server calls, cache, files, memory, and timeouts.
---
# 1C EDT: клиент-сервер

Apply when writing managed forms, commands, and common modules in a 1C:EDT project (form `Module.bsl` and common modules under `src/`). Checklist distilled from ITS v8std, not a copy of the articles. Compiler directives and the client/server split of modules are in the language-constructs skill.

## Where code runs (№629, №487)

- Keep client code small. Heavy work runs on the server. Leave an algorithm on the client only when it is clearly faster than a round trip.
- Wrap client-mode-specific code in preprocessor instructions.
- A user action should not add configuration server calls beyond the one the platform already makes. Watch both the count and the payload, especially on a slow or mobile link.
- Do not call the server during startup. If startup data is required, fetch it in one call.
- Periodic client work runs no more often than about every 20 minutes. Prefer a server notification.
- Open a form in one call. Client handlers of opening (`ПриОткрытии` and the rest) do not call the server.
- A form command makes at most one server call. Building a report adds none.
- Large selection data goes through temporary storage. Delete it or reuse the address.
- Merge hidden extra calls. Send only the fields the operation needs.

## Cache and predefined values (№724, №459, №443)

- Cache an expensive calculation or a database or external result that will be reused. Do not cache a value that is cheaper to compute than to look up. Keep the input domain narrow.
- Do not change an object you got from the cache.
- A nested call is cached only if you call it through the module name.
- Do not return a query, a temporary-table manager, or another database object from a session-lifetime cache.
- Shared stable settings live in a session-lifetime reuse module, returned together in one call. Data of one form lives in that form’s attributes, filled on the server.
- Do not use application-module variables just to avoid a server call.
- On the client, get a predefined value with `ПредопределенноеЗначение`, or with the library helper `ПредопределенныйЭлемент` when the configuration has BSP 2.1.4 or later. Do not add your own client cache. Those functions already cache.

## Files (№542)

- Temporary names come from the platform. On the web client use the web-client API.
- Delete temporary files and directories yourself.
- Finish server file work inside one server call. Between calls, keep the data in temporary storage.
- Prefer an in-memory stream for binary data and close it after reading.
- Move a file between client and server through temporary storage and the asynchronous file API.
- Generated file names are Latin letters and digits, UTF-8. A name the user typed can be transliterated.
- Do not pass an untrusted path to a server procedure. Check the extension and stay inside allowed directories.
- Do not write into the 1C installation directory. Administrators should also use security profiles.

## Memory and timeouts (№725, №748)

- Do not assume unlimited memory. Process an unbounded set in portions and store intermediate results.
- Read a large selection in fixed batches.
- Do not load a large XML file into a string, DOM, HTML, or XDTO. Use a streaming reader and take only the fragment you need.
- Break cyclic references when the objects are done.
- Every web service, HTTP, FTP, and mail call has a timeout. Usually within three minutes, except a large transfer.
- Before a web-service call that may exceed about 20 seconds, do a short `Ping`. REST, FTP, and WebDAV get a similar cheap check.
- A long web-service operation is asynchronous: start, status, result.
- Rough ranges: about 7 seconds for a service description, 10–20 seconds for a quick check, 60–180 seconds for a normal exchange, and a size-based limit up to 12 hours for a very large download.

## Sources

- https://its.1c.ru/db/v8std/content/724/hdoc
- https://its.1c.ru/db/v8std/content/459/hdoc
- https://its.1c.ru/db/v8std/content/443/hdoc
- https://its.1c.ru/db/v8std/content/487/hdoc
- https://its.1c.ru/db/v8std/content/629/hdoc
- https://its.1c.ru/db/v8std/content/542/hdoc
- https://its.1c.ru/db/v8std/content/725/hdoc
- https://its.1c.ru/db/v8std/content/748/hdoc
