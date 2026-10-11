---
name: builder-run-quality-gates
description: Ejecutar los quality gates que corresponden al deliverable_type del work_plan activo mediante run_gates_dispatch.py. Usar cuando el Builder termino un cambio sustancial y necesita validarlo antes de pedir review. No usar para autorizar el handoff, porque un exit 0 no autoriza BUILDER_EXIT ni READY_FOR_REVIEW (ver builder-self-audit).
---

Lee `skills/builder-run-quality-gates/SKILL.md`.
