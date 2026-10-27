---
name: '1C EDT: безопасность кода'
description: >-
  Use when a 1C:EDT change exposes a server call, runs dynamic code, stores a
  password, or launches an external program.
---
# 1C EDT: безопасность кода

Apply when a 1C:EDT change adds a server call, `Выполнить` / `Вычислить`, a password, an external component, or a launch of another program. Common-module flags live in `.mdo`. Checklist distilled from ITS v8std, not a copy of the articles. Roles and RLS are a separate skill.

## Server API (№678, №679)

- Every procedure a client can call is a public server API. Review it as one.
- Keep business logic out of the server part of a form module when a common module can hold it.
- Privileged mode and privileged common modules get a separate review.
- Do not run untrusted external code or an arbitrary query text on the server.
- External reports, data processors, COM, and add-ins are untrusted until audited.
- A form receives the finished result, not private source data or intermediate rows.
- Set “server call” only on a common module whose functions are meant for the client. Those functions do only what the current user may do, and return only what that user may see.
- Server-only routines live in a module without “server call”.
- Do not create or look up metadata objects on the client in a managed thick client. Turn off managed thick-client modes the configuration does not support.

## Passwords (№740)

- Ask for a password and pass it on. Do not store it.
- Do not keep passwords or other secrets in the infobase if you can avoid it. If you cannot, warn the user: storage only reduces the risk.
- A stored secret lives in its own metadata object with tight rights, or in the library secure store when BSP is present.
- Do not put a password in a form attribute. Read it on the server immediately before use.
- Privileged mode covers only that read or write, then clear the value from the form.

## External code (№669, №770, №801)

- Do not run unaudited external code on the server in unsafe mode.
- Connect extensions, external reports, processors, and add-ins through the library subsystems when the configuration has them.
- Interactive opening of external reports and processors is off by default. An administrator can turn it on, with a warning.
- Warn an administrator before loading external code and let them cancel until it is audited.
- Update, restore, and import of a configuration are an interactive administrator action, with a warning about the source.
- Control uploaded file types. Do not open an executable from the application.
- A non-administrator does not install or attach an add-in on the server.
- Load external code only from a trusted source over an authenticated protected connection.
- Do not `Выполнить` or `Вычислить` arbitrary text. Only immutable, already audited code.
- Build a user formula from approved pieces, not from raw text.
- If evaluation is unavoidable, use safe mode and an allowlist of methods. Do not evaluate text built from client or database input.
- Prefer a direct call or an approved library wrapper. Check the method name and the parameters immediately before a dynamic call.
- Unsafe code that cannot be removed goes into an audited extension or external processor that an administrator controls.
- A scheduled job that runs arbitrary code runs as a restricted service user. Safe mode alone is not enough.
- On the client the same ban applies. Do not take text from the server or the database and execute it on the client. An unavoidable formula is evaluated on the server, in safe mode, with an allowlist.

## Launching programs and external resources (№774, №775, №794)

- Build a launch command only from checked parts. Validate anything that came from the user, storage, or the database.
- Untrusted fragments must not contain shell metacharacters.
- Open files, navigation links, and programs through the library API when it exists.
- Do not open files with a `file://` link.
- Do not generate an executable. Call a fixed program with arguments or a parameter file.
- An elevated launch is a button or a menu item on a managed form, with a shield icon.
- An application opened through an open interface must not run arbitrary code.
- Disable Word and Excel macros before opening a document through COM. Leave macros off by default.
- If macros are required, client and server have separate settings, defaulting to signed macros only. Each user controls their client setting. Only an administrator controls the server setting. Check the signature before an automatic macro, and reject an unsigned document when the setting requires it.
- Prefer a platform feature over an add-in, an OS program, or COM.
- Use security profiles through the library subsystem when it is in the configuration.
- Declare required external resources in the override module meant for that. Ask an administrator before turning on or off a feature that needs them.

## Sources

- https://its.1c.ru/db/v8std/content/678/hdoc
- https://its.1c.ru/db/v8std/content/679/hdoc
- https://its.1c.ru/db/v8std/content/740/hdoc
- https://its.1c.ru/db/v8std/content/669/hdoc
- https://its.1c.ru/db/v8std/content/770/hdoc
- https://its.1c.ru/db/v8std/content/801/hdoc
- https://its.1c.ru/db/v8std/content/774/hdoc
- https://its.1c.ru/db/v8std/content/775/hdoc
- https://its.1c.ru/db/v8std/content/794/hdoc
