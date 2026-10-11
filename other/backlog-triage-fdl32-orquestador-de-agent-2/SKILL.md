---
name: backlog-triage
description: Planificador pre-pipeline de solo lectura que reconcilia el backlog con git, clasifica la aptitud de cada ticket, propone un DAG de grupos y recomienda por cual empezar; solo escribe su informe y su JSON. Usar cuando hay que decidir que pipeline o batch autonomo lanzar sobre el backlog vivo. No usar para ejecutar el pipeline ni mutar el backlog (ver orchestrate-pipeline), para auditar un pipeline cerrado (ver audit-pipeline) ni para dar de alta tickets (ver backlog-admit).
---

Lee `skills/backlog-triage/SKILL.md`.
