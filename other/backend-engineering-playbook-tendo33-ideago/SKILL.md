---
name: backend-engineering-playbook
description: Use when implementing IdeaGo backend API, pipeline, cache, or anonymous runtime tasks.
---
# Backend Engineering Playbook

This legacy skill is a thin Trellis pointer.

Read `.trellis/spec/backend/index.md` and `.trellis/spec/shared/verification.md`
before backend work. Keep FastAPI handlers thin, report contracts typed,
anonymous session semantics stable, and hosted-only dependencies out of `main`.
