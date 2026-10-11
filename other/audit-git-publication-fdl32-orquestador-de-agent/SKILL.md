---
name: audit-git-publication
description: Auditoria dry-run de si un repo_destino puede publicarse en Git sin secretos, PII, artefactos privados ni deuda sin decision, con classify_publication.py y doble pasada de verificacion y refutacion. Usar cuando se prepara la primera publicacion de un repo_destino o una revision de su exposicion. No usar para instalar el destino (ver setup-agent-system) ni como gate pre-push de estado vivo (ver check_destino_publish_ready.py); no publica, no commitea ni borra nada.
---

Lee `skills/audit-git-publication/SKILL.md`.
