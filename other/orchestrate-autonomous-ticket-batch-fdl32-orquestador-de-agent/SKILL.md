---
name: orchestrate-autonomous-ticket-batch
description: Ejecutor autonomo que consume el DAG de backlog-triage y cierra el maximo de tickets con barreras duras por ticket, delegando cada uno en el pipeline canonico del modo detectado; crea commits, mueve filas al archivo, escribe bus, ledger y memoria, puede publicar con push y nunca se audita a si mismo. Usar cuando hay un triage con DAG validado y fresco y un tercero ha resuelto el recibo de aislamiento de arranque. No usar para un pipeline por ticket (ver orchestrate-pipeline, orchestrate-pipeline-codeonly), para producir el DAG (ver backlog-triage) ni para auditar el batch (ver audit-autonomous-ticket-batch); nunca ejecuta tickets REQUIERE_HUMANO ni DISENO_PRIMERO.
---

Lee `skills/orchestrate-autonomous-ticket-batch/SKILL.md`.
