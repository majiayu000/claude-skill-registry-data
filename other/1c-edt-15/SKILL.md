---
name: '1C EDT: задания, подсистемы, время'
description: >-
  Use when adding scheduled jobs, subsystems, direct register queries, or
  session time handling in a 1C:EDT project.
---
# 1C EDT: задания, подсистемы, время

Apply when adding a scheduled job, a subsystem, a direct register query, or server time handling in a 1C:EDT project. Jobs and subsystems are metadata objects under `src/`. Checklist distilled from ITS v8std, not a copy of the articles.

## Scheduled jobs (№540, №402, №539, №760)

- A scheduled job is for work that must run on a schedule, once or repeatedly.
- Use a predefined job when nobody needs to create or delete it at runtime. A job that depends on data is a non-predefined parameterized instance.
- Do not run a job whose feature is turned off. Tie it to the functional option.
- In a copy of the database (test, support), disable jobs that call external resources.
- With the BSP job subsystem, the handler starts with the standard “may this job run” check.
- Do not schedule a job more often than the business needs. Most jobs run once a day. Never more often than once a minute. A frequent job must finish well inside its interval.
- Heavy jobs run when the server is quiet, and not all at the same moment.
- Give the user a manual way to do what the job does. A workplace shows how fresh the data is and a command to refresh, if the user is allowed.
- A job that touches many workplaces, or that builds reports and mailings, gets its own workplace.
- Block scheduled jobs while the infobase is updating. At the start of the handler, stop if an update is unfinished. BSP has the standard check.
- In 1cFresh, a scheduled job is not a separating attribute. Regular work inside a data area goes through the BSP job queue, or an equivalent queue.
- Do not manage those jobs through the platform API. Use the BSP server interface.
- The queue may run late. Do not show schedule settings to a service user as a rule.
- An urgent update is a push or work done while the user is in the application. Keep the server operation short.

## Registers (№477, №633)

- A register does not depend on its registrar. Reports and register logic use only the register’s own data.
- Do not read a registrar’s attributes through the register. That is an extra join and can break in a distributed database.
- A query against a register that can hold inactive records filters by activity. The same filter is in universal reports and other generic logic.
- Cancelling movements the user can edit deactivates them. It does not delete them.

## Subsystems (№543)

- Subsystems build the command interface and also group metadata by function.
- A subsystem that is a section the user sees has “include in the command interface” on.
- A functional grouping that is not one interface section is a separate hierarchy, with “include in the command interface” off.
- Modules, scheduled jobs, and other objects with no visual place belong only to functional subsystems.

## Time zones (№643)

- The configuration works when the server’s time zone is not the user’s.
- Server code uses the session’s local time, not the server computer’s clock.
- A timestamp that must not depend on the current session is universal time. Convert it when you show it.
- Client code does not call the ordinary current-time function. Take the session time from the server, or use the document date.
- With BSP, use the session-date helper. Inside one procedure, compute the time once and reuse it.
- If you really need the server computer’s clock, say why in a comment.

## Sources

- https://its.1c.ru/db/v8std/content/540/hdoc
- https://its.1c.ru/db/v8std/content/402/hdoc
- https://its.1c.ru/db/v8std/content/539/hdoc
- https://its.1c.ru/db/v8std/content/760/hdoc
- https://its.1c.ru/db/v8std/content/477/hdoc
- https://its.1c.ru/db/v8std/content/633/hdoc
- https://its.1c.ru/db/v8std/content/543/hdoc
- https://its.1c.ru/db/v8std/content/643/hdoc
