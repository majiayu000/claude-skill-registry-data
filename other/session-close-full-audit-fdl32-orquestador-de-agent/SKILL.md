---
name: session-close-full-audit
description: Auditoria adversarial previa al cierre canonico de una sesion, que encadena tres auditorias de salud y una pasada adversarial sobre el codigo generado; el cierre lo ejecuta agent_controller.py --session-close y en modo FINAL tambien registra follow-ups y propone memoria. Usar cuando se cierra una sesion que toco codigo del motor o del destino, antes de --session-close; a mitad de vuelo solo los Bloques 1, 2 y 2.5 sin 2.5.f ni 2.5.g, y nunca los Bloques 3 a 5. No usar para el cierre operativo (ver orchestrator_session_close_chat), para arrancar una sesion (ver orchestrator_session_bootstrap) ni para dejar continuidad medida a la sesion siguiente (ver session-hop); nunca corre el Bloque 3 con un ticket IN_PROGRESS.
---

Lee `skills/session-close-full-audit/SKILL.md`.
