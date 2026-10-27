---
name: '1C EDT: метаданные'
description: >-
  Use when adding or renaming metadata in a 1C:EDT project: names, synonyms,
  common modules, types, attributes, and functional options.
---
# 1C EDT: метаданные

Apply when adding or renaming metadata in a 1C:EDT project: objects under `src/`, properties in `.mdo`, not a configurator dump. Checklist distilled from ITS v8std, not a copy of the articles. Roles, queries, and module layout are separate skills.

## Configuration (№467)

- Use only documented platform features.
- The configuration must run on the DBMS, OS, browsers, and modes the platform supports.
- Key web-client behavior works without a file extension and uses asynchronous calls.
- The configuration check has no open errors, except a case you can justify.
- Keep ordinary-application and external-connection compatibility where it is still required.
- Follow platform defaults. A deviation needs a reason.
- Names, synonyms, comments, and user text are correct Russian.
- No unused metadata and no unused code.

## Names and synonyms (№550, №474)

- Names are short and mean something. No redundant word like `Справочник`, `Документ`, or `Отчет` when it adds nothing.
- Roles are named by the job or the action they grant. Exchange plans are named by the sync or by the pair of bases.
- Catalogs, journals, enumerations, filter criteria, and information registers are plural. Documents, business processes, tasks, and charts of accounts are singular.
- Forms, templates, groups, and style items are nouns. Commands and event subscriptions name the action.
- A report and a report variant have a specific name. A print form has a title.
- Web services and their operations are in English, without `Service` or `WebService` stuck on the name.
- Every object has a short synonym. Abbreviations only if the users already know them.
- Use the accepted term. No slang, no distorted names, no mixed-script transliteration.
- Standard attributes and tabular sections get a synonym that fits this object. `Родитель` and `Владелец` do not keep the default synonym.
- Two similar objects have synonyms that tell them apart.
- The name is built from the synonym: recognizable words, each word capitalized. No «ё». The name is at most 80 characters.
- A comment is a useful note for a developer and starts with a capital letter. Do not comment the obvious.

## Common modules (№469)

- Group routines by subsystem or by one mechanism.
- Pick the context: server, server call, client, or client-server.
- A server module that must also run in the ordinary client and the external connection is flagged for those modes.
- An export of a server-call module does not take a mutable object as a parameter.
- Client-only logic is a client module. Logic that is the same on both sides is a client-server module.
- Do not split client and server with preprocessor instructions inside one shared module. Use two modules.
- The module name is the subsystem or the mechanism, not `Процедуры` or `Модуль`.
- Add a suffix when the module is global, privileged, cached, overridable, or a localization module.

## Types and attributes (№704, №677, №728, №432)

- A defined type is for a domain type you reuse, a type that will change, a repeated length or precision, or a composite type shared by a subsystem. An embeddable subsystem uses one when the host configuration may narrow the type.
- Do not add a defined type as a pure alias, a one-off wrapper, or a reserve for later.
- A common attribute is either a separator or a real extension of several objects. It is not a convenient place for `Ответственный`, `Комментарий`, or `Организация`.
- Rights on a common attribute are separate from the host object. Separators are ordered the way session parameters must be initialized.
- A composite field used in a join, a filter, or an order contains only references. No string, number, date, Boolean, UUID, or value storage.
- A free-form value is its own reference object when that is practical. A table of a few rows may break this rule.
- Stored types are listed explicitly. `ЛюбаяСсылка` is only for a truly universal mechanism.
- A composite type reused across the configuration is a defined type. A wide composite type without a need slows queries and complicates deletion and input.
- A string is variable length with a stated maximum. Fixed length only when the width is really fixed.
- The maximum is the business limit. A concatenated string fits the sources. If there is no formal limit, pick a practical bound.
- Unlimited length is for a long user text or a technical payload.
- In a query, cast an unlimited string to a bounded length before compare, group, or `РАЗЛИЧНЫЕ`.
- A printed string is shown in full. If you cast it often, the attribute should be bounded.

## Codes, options, session, fill check (№473, №470, №413, №478)

- Add a code or a number when the list is large, lookup by code is useful, or the code means something in the domain.
- Do not auto-number a short label or a value that arrives from outside.
- Size an auto-number for the scope, the period, the owner, and the prefixes. Variable length. Usual lengths are 3, 5, 9, or 11.
- With the standard prefix subsystem, document and catalog numbers are at least 11 characters.
- A string code that is auto-numbered, entered from several sources, and later merged must support automatic prefixes.
- A functional option turns a feature on or off for a deployment. A parameter (constant or information register) is for a context.
- Do not use an option to hide one form or to cache data.
- The configuration itself must let an administrator set the option. There is no separate platform editor.
- A missing parameter record is `Ложь`. Several matching records combine with OR.
- After changing an option, refresh the interface.
- Do not parameterize an option by a high-cardinality value such as a product or a counterparty. Keep few parameters, no duplicates, and keep dependent options consistent.
- A session parameter is a per-session value needed in a query or in RLS.
- Not for a client-only value (use an application variable) and not as a server cache (use a reuse-return module).
- Do not initialize every parameter at startup. Initialize on demand in the session module, related parameters together, and remember which ones are already set.
- A hint only on a user field that is actually unclear. Not a manual. Delete a generated hint that says nothing.
- A required typed field, standard attribute, or tabular section raises an error when empty. Put the check in metadata. A conditional exception goes in the fill-check handler.
- Do not turn metadata checking off and reimplement it in code. Mark a field required on the form only for the situation that needs it.

## Sources

- https://its.1c.ru/db/v8std/content/467/hdoc
- https://its.1c.ru/db/v8std/content/550/hdoc
- https://its.1c.ru/db/v8std/content/474/hdoc
- https://its.1c.ru/db/v8std/content/469/hdoc
- https://its.1c.ru/db/v8std/content/704/hdoc
- https://its.1c.ru/db/v8std/content/677/hdoc
- https://its.1c.ru/db/v8std/content/470/hdoc
- https://its.1c.ru/db/v8std/content/413/hdoc
- https://its.1c.ru/db/v8std/content/432/hdoc
- https://its.1c.ru/db/v8std/content/728/hdoc
- https://its.1c.ru/db/v8std/content/473/hdoc
- https://its.1c.ru/db/v8std/content/478/hdoc
