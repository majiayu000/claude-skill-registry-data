---
name: '1C EDT: библиотеки'
description: >-
  Use when a 1C:EDT project is a library, embeds one, or overrides BSP-style
  modules, roles, and infobase update handlers.
---
# 1C EDT: библиотеки

Apply when a 1C:EDT project is a library, embeds a library, or overrides BSP-style modules. Objects stay in the EDT tree under `src/`. Checklist distilled from ITS v8std, not a copy of the articles. Roles in a final configuration are a separate skill.

## Shape of a library (№551, №552, №705)

- Share code and metadata through a library configuration. If one library depends on another, the libraries form a hierarchy.
- Split three layers: the public API, the library-service API, and the internal code of a subsystem. An API for one consumer is documented in its own section.
- Names must not clash between a library and the configuration that embeds it. The lower library wins. The consumer renames its object to be more specific.
- Generic names belong in the lowest library. Higher libraries and the final configuration use domain names. Add a library or solution qualifier when you extend or distinguish similar functionality.
- Every library object belongs to one root subsystem that has no command interface. Another root subsystem with a command interface is only when you really need it.

## Overrides (№553, №554, №739)

- Do not edit a library object that is not marked overridable. An emergency edit is lost on the next update.
- Adapt the library through overridable objects, type identifiers, type extensions, predefined items, and override modules. Keep the override small.
- An override module’s name ends with `Переопределяемый`. Consumer code does not call it. The call goes through a stable library API module.
- An override module contains only empty export procedures. The default logic lives elsewhere. On update, sync the module by hand.
- The base override module is declared in the lowest library. A higher library adds behavior in its own implementation module. The override module is a chain of calls, not a copy of the implementation. The order is base library, then higher libraries, then the consumer.
- Settings shared by a subsystem or a group of objects live in the override module, as a structure with defaults. Connected objects are listed in dedicated override procedures.
- Do not discover supported objects or handlers by catching errors in `Попытка`.
- Settings and handlers of one object live in that object’s manager module. One procedure per action. Whether a handler exists is declared in the settings procedure.

## Compatibility, roles, infobase update (№644, №668, №690)

- Inside one subedition, stay backward compatible. Version digits mean: a breaking architecture or subedition change, then new features, then a bug-fix build.
- Do not change the public API or its behavior. You may only extend it. A permitted break is documented with a migration path.
- A renamed or removed export stays as a deprecated wrapper.
- Extend an API with an optional parameter at the end or with an extensible structure. Call the library API. Do not touch its metadata from outside.
- A library contains only what is meant to be reused. Consumer-specific objects are created in the implementation.
- The library ships ready roles for its data objects. Skip a role when the object is subordinate, is a skeleton that the consumer overrides heavily, or the library is algorithms only.
- RLS should work as shipped. Change or drop it on integration only for a stated exception. Every library role is delivered as “changes allowed”.
- Each library publishes its name, version, update handlers, and dependencies in a module `ОбновлениеИнформационнойБазы…`.
- A handler is an export procedure, usually in the manager module of the object it changes. Pick exclusive, operational, or deferred.
- No interactive user logic. A handler can be run again and must finish safely.
- While it writes, turn off business logic and exchange registration that are not needed.
- Each handler says which version it targets and what it changes. Adopting a new library version increments the configuration version.

## Sources

- https://its.1c.ru/db/v8std/content/551/hdoc
- https://its.1c.ru/db/v8std/content/552/hdoc
- https://its.1c.ru/db/v8std/content/553/hdoc
- https://its.1c.ru/db/v8std/content/705/hdoc
- https://its.1c.ru/db/v8std/content/554/hdoc
- https://its.1c.ru/db/v8std/content/739/hdoc
- https://its.1c.ru/db/v8std/content/644/hdoc
- https://its.1c.ru/db/v8std/content/668/hdoc
- https://its.1c.ru/db/v8std/content/690/hdoc
