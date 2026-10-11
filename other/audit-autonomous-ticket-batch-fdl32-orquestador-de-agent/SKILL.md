---
name: audit-autonomous-ticket-batch
description: Auditoria aislada (contexto fresco, solo lectura) de un batch autonomo de tickets ya cerrado o parado, que re-deriva el PREDICATE de 8 condiciones comando a comando, audita las paradas y la recuperacion del ejecutor y propone, sin ejecutarlo, el cierre de sesion. Usar cuando un batch de orchestrate-autonomous-ticket-batch ha terminado o se ha detenido, ya no le quedan grupos ejecutables y existe su batch_run. No usar para auditar una cadena ticket a ticket (ver audit-pipeline, audit-pipeline-codeonly) ni desde el mismo agente que ejecuto el batch.
---

Lee `skills/audit-autonomous-ticket-batch/SKILL.md`.
