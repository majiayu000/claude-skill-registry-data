---
name: orchestrate-destination-batch
description: Orquesta en un lote secuencial varios repo_destino hasta un estado de publicacion explicito, uno a uno, clasificandolos con batch_destination_controller.py, conduciendo Contract Formation y el pipeline por ticket con los prompts canonicos y dejando un manifest global reanudable. Usar cuando hay que preparar y auditar varios repo_destino para publicacion remota en un unico lote. No usar para sustituir el pipeline por destino (ver orchestrate-pipeline), Contract Formation (ver contract_formation_pipeline) ni la auditoria de publicacion (ver audit-git-publication); no crea repos remotos ni hace push.
---

Lee `skills/orchestrate-destination-batch/SKILL.md`.
