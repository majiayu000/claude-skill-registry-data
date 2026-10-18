---
name: repo-audit
version: 1.0.0
description: Auditoria multifase multiagente de un repo (dead code, legacy, seguridad, proceso) con bucle adversarial de verificacion antes de proponer limpieza. Usar cuando el repo ha crecido y hace falta un censo repetible antes de limpiar/refactorizar a escala. No usar para un solo archivo ya identificado (ver refactor-manager) ni como sustituto de audit_portability_legacy_surface.md cuando el objetivo es la taxonomia legacy-stub-declared especifica del motor.
triggers: [/repo-audit-multiagent, audit-repo-multiagent, /cleanup-audit]
author: agent
role: auditor
stage: review
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system, audit, security]
source_prompt: prompts/repo_audit_multiagent.md
contract_id: cid-repo-audit-multiagent-v1
---

# repo-audit

Skill minima que apunta al nucleo de auditoria multiagente de repos. Esta
skill SOLO apunta: no re-declara criterios del nucleo ("skill apunta,
prompt gobierna" — X-09).

## Fuente canonica

- **Nucleo:** `prompts/repo_audit_multiagent.md`
- Todo el contenido normativo (las 7 fases, el gate de sostenibilidad, la
  composicion del bucle adversarial, el formato de salida, las
  restricciones y los riesgos) vive SOLO ahi. Leelo entero antes de
  ejecutar esta skill.

## Cuando usarla

- El repo (motor o destino) ha crecido y hace falta un censo de codigo
  obsoleto, archivos legacy, vulnerabilidades de seguridad o malas
  practicas, antes de decidir que limpiar.
- Se quiere repetir la auditoria periodicamente con el mismo criterio
  (misma composicion de lanes, mismo gate de sostenibilidad, mismo
  presupuesto de bucle adversarial).

## Cuando NO usarla

- Ya se identifico UN archivo concreto a refactorizar: usa
  `skills/refactor-manager` directamente, sin pasar por las 7 fases.
- El objetivo es auditar especificamente la taxonomia
  legacy-stub-declared del propio motor (alias de frontmatter, stubs
  declarados): usa `prompts/audit_portability_legacy_surface.md`. Si el
  ambito de esta auditoria es `motor`, Fase 0 y Fase 3 del nucleo ya
  declaran como dedupicar con ese prompt si ambos aplican a la vez.
- Se quiere optimizar la VELOCIDAD de la suite de tests (no su valor ni el
  codigo de produccion): usa `skills/suite-optimization`.

## Workflow (apunta al nucleo, no lo repite)

1. Leer `prompts/repo_audit_multiagent.md` entero.
2. Ejecutar sus Fases 0-6 en orden, segun las define el nucleo (Secciones
   1-7 del nucleo), sin excepcion ni abreviacion.
3. Entregar el informe segun el formato que define la Seccion 8 del
   nucleo.

## Distincion con skills hermanas

- `code-audit` / `test-audit`: recolectores de UNA sola fase, sin fan-out
  multiagente ni bucle adversarial. `repo-audit` los **invoca** en su
  Fase 1 (dead-code), no los duplica.
- `refactor-manager`: ejecuta el cambio sobre UN archivo ya identificado.
  Es el **consumidor** de los follow-ups de `repo-audit` en Fase 6, no
  decide que auditar.
- `audit_portability_legacy_surface.md`: auditoria legacy ACOTADA al
  propio motor (naming/alias/stubs). Complementaria, no sustituible.

## Constraints

- **NUNCA** re-declarar aqui ningun criterio normativo del nucleo (gate de
  sostenibilidad, composicion del bucle, presupuesto, condicion de
  ejecucion de Fase 6, formato de salida) — todos viven SOLO en
  `prompts/repo_audit_multiagent.md`, esta skill solo remite a sus
  secciones.
- Si el nucleo diverge de esta skill, prevalece el nucleo — corregir esta
  skill, no el nucleo.

## References

- `references/lane-examples.md` — ejemplos de declaracion de lanes para
  repos Python puros vs multi-lenguaje.

---

**Version:** 1.0.0
**Autor:** agent-system
**Ultima actualizacion:** 2026-10-16 (propuesta v3 validada por bucle
adversarial DBL-4, 8 lentes, 0 bloqueantes)
