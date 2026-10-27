---
name: '1C EDT: права доступа'
description: 'Use when changing roles, RLS, or privileged mode in a 1C:EDT project.'
---
# 1C EDT: права доступа

Apply when changing roles, RLS, or a privileged call in a 1C:EDT project. Roles are role objects in the EDT tree, not a configurator `Rights.xml` dump. Checklist distilled from ITS v8std, not a copy of the articles.

## How roles are cut (№689, №488, №532)

- A role is one elementary function. An external-user role lists every right it needs.
- No role gets interactive deletion of reference objects. Deletion stays on `ПолныеПрава` and `АдминистраторСистемы`.
- “Rights for new objects” is on for `ПолныеПрава` only.
- Documents use privileged posting and unposting. Functional options use privileged get, unless the value must depend on parameters on purpose.
- Each object belongs to one elementary function. Do not mix objects from different libraries or subsystems in one role.
- Reference objects and independent information registers get separate read and edit roles.
- Shared non-secret access lives in the library basic-rights roles. A report or a workplace that must be granted on its own gets its own role.
- Extra permission checks go through roles. Drop `Удалить*` objects from every role except the two administrator roles.
- Access is configured with roles. Finer control is a profile that combines small roles.
- The configuration has `ПолныеПрава`, `АдминистраторСистемы`, and `ИнтерактивноеОткрытиеВнешнихОтчетовИОбработок`.
- `АдминистраторСистемы` is assigned only together with `ПолныеПрава`. The external-opening role is what allows opening external reports and processors.
- Do not hand out interactive deletion, including predefined data, across ordinary roles. Users who must delete marked objects and otherwise have no right get a separate `УдалениеПомеченныхОбъектов` role.
- Auditors, owners, and directors get a read-only role or profile. If they must see everything, remove the RLS limits on that read.
- Technical-specialist mode is for developers and rare troubleshooting, not for everyday users.
- An extension adds its own roles with a prefix. It does not edit `ПолныеПрава` or `АдминистраторСистемы`.
- A new role enables default rights for attributes and tabular sections. Independent rights on subordinate objects stay off.
- To grant rights on fields only, turn independent subordinate rights on and clear the default field and tabular-section rights first.
- Every new object and every new field is set in the roles that should have it.

## Checks in code (№737, №485, №415)

- With many roles, do not hide form controls by role. A big difference is a separate form. A small one is a check in code.
- Do not hide commands or the start page by role. Close the section, the form, or the object.
- Check an object right with `ПравоДоступа`, not by testing that a role is present.
- `РольДоступна` or `Пользователи.РолиДоступны` is only for a role that means an extra permission and grants no metadata rights.
- If privileged mode hides the normal check, test that role. Do not fake a right with `ГДЕ ЛОЖЬ` in RLS.
- Changing form visibility from code has a cost. Do not do it on every refresh without a reason.
- Privileged mode is for a bypass that is either required by the logic or a measured speedup.
- Recorder-subordinate registers are read-only for users. Posting writes them in privileged mode.
- If users do not report on a register and do not need it, give them no rights on it. Touch it only from controlled privileged code.
- If an allowed operation needs data the user must not see, read and use that data on the server. Do not send it to the client.
- Do not export a routine that always turns privileged mode on, unless every user is supposed to run it.
- When the caller must be allowed, call `ВыполнитьПроверкуПравДоступа` before the privileged part. A missing right raises the standard exception.
- Turn privileged mode on immediately before the sensitive action and off immediately after.
- Prefer the platform flags (privileged posting, a privileged common module) over a manual switch.
- Do not stamp `РАЗРЕШЕННЫЕ` on every query just to hide an access error. Business logic either sees all the rows it needs or stops with an access error. `РАЗРЕШЕННЫЕ` is for data the operation can skip, such as an optional contact.

## Session parameters (№491)

- Changing a session parameter or a functional option that RLS uses drops the access cache. Count that cost.
- Set session parameters on demand in `УстановкаПараметровСеанса`.
- Do not change functional-option values often while users are working.

## Sources

- https://its.1c.ru/db/v8std/content/689/hdoc
- https://its.1c.ru/db/v8std/content/488/hdoc
- https://its.1c.ru/db/v8std/content/532/hdoc
- https://its.1c.ru/db/v8std/content/737/hdoc
- https://its.1c.ru/db/v8std/content/485/hdoc
- https://its.1c.ru/db/v8std/content/415/hdoc
- https://its.1c.ru/db/v8std/content/491/hdoc
