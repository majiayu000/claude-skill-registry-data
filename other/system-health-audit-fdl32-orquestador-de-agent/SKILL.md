---
name: system-health-audit
description: Auditoria periodica de salud de las tres capas (repo_motor, repo_destino e integracion) tras cambios, con un recolector determinista que junta la evidencia y el agente que la audita en solo lectura. Usar cuando hubo cambios en el motor o en un repo_destino y hay que saber si el sistema sigue sano de extremo a extremo. No usar para meta-auditar un pipeline cerrado (ver audit-pipeline), para el listo-para-publicar de un repo (ver audit-git-publication) ni como snapshot rapido (ver local-audit); el reporte del recolector no es el veredicto.
---

Lee `skills/system-health-audit/SKILL.md`.
