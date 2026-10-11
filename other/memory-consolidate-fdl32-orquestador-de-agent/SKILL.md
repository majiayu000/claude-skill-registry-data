---
name: memory-consolidate
description: Consolida de forma determinista observations.jsonl, deduplicando, filtrando ruido y archivando entradas antiguas, sin LLM ni cron. Usar cuando se cierra la sesion tras session_close_observations o cuando observations.jsonl ha crecido mucho. No usar para escribir observaciones nuevas (ver session-close-observations).
---

Lee `skills/memory-consolidate/SKILL.md`.
