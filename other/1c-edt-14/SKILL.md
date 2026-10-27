---
name: '1C EDT: обмен данными'
description: >-
  Use when changing exchange plans, registration rules, classifier sync, or
  EnterpriseData in a 1C:EDT project.
---
# 1C EDT: обмен данными

Apply when changing exchange plans, registration rules, classifier sync, or EnterpriseData in a 1C:EDT project. Exchange plans and their modules live in the EDT tree under `src/`. Checklist distilled from ITS v8std, not a copy of the articles. `ОбменДанными.Загрузка` in object handlers is a separate skill.

## Classifiers (№637)

- Match a classifier object by reference id first, then by the search fields.
- Conversion rules must do the id lookup and the fallback field search.
- A hard identification case gets its own search-fields handler.
- Do not put a record-set classifier into the exchange. Keep that classifier up to date in each database on its own.

## Exchange plans and registration (№701, №799)

- Register changes in the object’s write and delete events, through the exchange plan.
- A table that is exchanged must be self-contained for registration. The rule must not depend on fields of a linked table or on the order messages are loaded.
- A registration error must not abort loading of exchange data.
- Do not exchange data that each database can calculate on its own.
- If related tables are in the exchange, register the change for all of the related data. That registration must tolerate a row that is not there yet.
- For a non-DIB conversion that uses the standard subsystem, defer registration of reference objects until loading finishes.
- Keep the registration rules in configuration modules, for example a common registration manager.
- Do not change safe mode or privileged mode from a registration rule, and do not use a construct that does.
- A fix to exchange rules ships as an extension or a patch.

## EnterpriseData (№771)

- A new exchange between configurations on BSL is EnterpriseData.
- Do not start a new exchange on conversion rules, except a solution for budget organizations.
- Support every current EnterpriseData version that the embedded BSL includes.
- Do not ship a configuration that drops a format version its embedded BSL still supports.
- Leave out a format version that does not have the functionality this exchange needs.
- Tell the user which EnterpriseData versions the solution supports.
- Do not put arbitrary data in `AdditionalInfo` in a standard exchange. That field is for an urgent legal change or a defect that blocks synchronization.

## Sources

- https://its.1c.ru/db/v8std/content/637/hdoc
- https://its.1c.ru/db/v8std/content/701/hdoc
- https://its.1c.ru/db/v8std/content/799/hdoc
- https://its.1c.ru/db/v8std/content/771/hdoc
