---
name: local-audit
version: 2.0.0
description: Genera un snapshot rapido y estructurado del estado del repositorio (version, estado del agente, salud, skills) con scripts/local_audit.py. Usar cuando arranca una sesion o antes de comparar con otro repositorio. No usar para auditar la salud del sistema tras un cambio (ver system-health-audit) ni para auditar codigo (ver code-audit).
triggers: [/local-audit, /repo-audit, /snapshot]
author: agent
role: auditor
stage: support
cycle_phase: [F0-arranque-sesion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# local-audit

Skill para generar y revisar una foto operativa y estructurada del estado del repositorio (auditoría local).

## Overview

Cuando se invoca este skill, ejecuta el script `scripts/local_audit.py` que consolida la información más importante del repositorio de forma eficiente y rápida (version, estado del agente, checks de salud, skills disponibles, configuración y logs recientes).

El resultado es consumible tanto por agentes (JSON) como por humanos (MD).

## Workflow

### Paso 1: Ejecutar la auditoría

```bash
python scripts/local_audit.py
```

Este comando generará dos archivos:
- `.agent/runtime/audit/audit.json`
- `.agent/runtime/audit/AUDIT.md`

### Paso 2: Leer el resultado

El agente debe leer e incorporar al contexto el contenido de `.agent/runtime/audit/AUDIT.md`.

### Paso 3: Análisis de salud (Opcional)

Si el reporte indica que hay `Errors` o `Warnings` en la sección "Health Check", el agente debe notificar al usuario para evaluar si es seguro proceder con el trabajo o si se debe abrir un ticket para corregir la deriva.

## Casos de Uso

- **Arranque de sesión**: Ejecutar esta skill ayuda a ganar contexto rápido de qué está pasando en el repo sin leer múltiples archivos dispersos.
- **Antes de comparar repos**: Provee el inventario de "lo que ya tenemos" para no proponer funcionalidades repetidas.
- **Pre-closeout**: Validación rápida del estado global del proyecto.
