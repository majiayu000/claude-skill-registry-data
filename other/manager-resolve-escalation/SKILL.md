---
name: manager-resolve-escalation
version: 2.0.0
description: Resuelve un bloqueo o una escalacion del Builder con una decision documentada, clasificando el bloqueo y comparando opciones con sus trade-offs. Usar cuando el Builder queda BLOCKED dentro del ticket. No usar para escalar al motor un hallazgo detectado desde un destino (ver escalate-to-motor).
triggers: [/escalate, escalation, /resolve]
author: agent
role: manager
stage: review
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# manager-resolve-escalation

Skill para resolver bloqueos técnicos o decisiones arquitectónicas escaladas por el Builder.

## Overview

Cuando el Builder está `🟠 BLOCKED`, el Manager usa esta skill para:
1. Leer y entender la escalación
2. Clasificar tipo de bloqueo
3. Analizar opciones con trade-offs
4. Tomar decisión documentada
5. Comunicar resolución

## Workflow

### Paso 0: Verificar Turno
```bash
python .agent/agent_controller.py
```
Debe indicar `ROL ACTIVO: MANAGER` y acción `RESOLVE_BLOCK`.

### Paso 1: Leer Contexto Completo

Leer en orden:
1. `review_queue.md` - Escalación del Builder
2. `execution_log.md` - Contexto del problema
3. `work_plan.md` - Plan original y criterios
4. `references/escalation-levels.md` - Guía de niveles

### Paso 2: Clasificar Tipo de Bloqueo

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Técnico** | Error técnico o bug | "No puedo hacer que funcione la conexión" |
| **Diseño** | Decisión arquitectónica | "¿Usar clase o funciones?" |
| **Dependencia** | Bloqueo externo | "Esperando API del proveedor" |
| **Permisos** | Acceso requerido | "Necesito credenciales de BD" |
| **Requisito** | Ambigüedad en requisito | "No está claro qué debe hacer" |

### Paso 3: Analizar Opciones

Para cada opción presentada por el Builder (o identificadas):

```markdown
| Opción | Pros | Contras | Riesgo |
|--------|------|---------|--------|
| A | [+] | [-] | 🟢/🟡/🔴 |
| B | [+] | [-] | 🟢/🟡/🔴 |
```

**Criterios de decisión:**
- Simplicidad (KISS)
- Mantenibilidad a largo plazo
- Tiempo de implementación
- Riesgo de introducir bugs

### Paso 4: Tomar Decisión

**Decisión debe ser:**
- Clara y específica
- Accionable (el Builder sabe qué hacer)
- Documentada con razonamiento

**NO dejar ambigüedades.**

### Paso 5: Documentar en review_queue.md

```markdown
### 🚨 ESC-[ID]: [Título Corto] - RESUELTO
- **Plan ID:** WOT-XXX
- **Tipo:** ESCALATION
- **Urgencia:** 🔴/🟡/🟢 [Alta/Media/Baja]
- **Estado:** ✅ RESOLVED
- **Fecha resolución:** [YYYY-MM-DD HH:MM]

**Problema:**
[Resumen del bloqueo]

**Opciones analizadas:**
1. [Opción A] - Pros/Contras
2. [Opción B] - Pros/Contras

**Decisión:** [Opción elegida]

**Razonamiento:**
[Por qué se eligió esta opción]

**Próximo paso para Builder:**
[Instrucción específica y clara]
```

### Paso 6: Notificar al Builder

```markdown
## 📨 [FECHA] Escalación Resuelta: Manager → Builder
**Plan:** WOT-XXX
**Escalación:** ESC-[ID]
**Decisión:** [Resumen en 1 línea]
**Acción requerida:** Ver review_queue.md y continuar implementación
**Estado:** PENDING
```

### Paso 7: Actualizar Estados

En `execution_log.md`:
- Cambiar estado de `🟠 BLOCKED` a `🔵 IN_PROGRESS`
- Añadir nota de resolución

## Criterios para Escalar (Guía para Builder)

El Builder debe escalar cuando:
1. **3+ intentos fallidos** para tarea 🟢
2. **2+ intentos fallidos** para tarea 🟡
3. **1 intento fallido** para tarea 🔴
4. **30+ minutos bloqueado** sin progreso
5. **Decisión de arquitectura** requerida
6. **Bug en librería externa**
7. **Incertidumbre** entre opciones equivalentes

## Anti-Patrones (NO hacer)

- **NO** dejar al Builder adivinar
- **NO** dar respuestas vagas ("intenta otra cosa")
- **NO** cambiar requisitos sin documentar
- **NO** ignorar la escalación

## Output Format

### Resolución Completa
1. Entrada en `review_queue.md` con decisión clara
2. Notificación en `notifications.md`
3. Actualización de `execution_log.md`

## References

- `references/escalation-levels.md` - Guía de niveles de urgencia
- `.agent/protocols/escalation_protocol.md` - Protocolo completo
- `.agent/rules/manager/` - Restricciones del rol

## Constraints

- **SIEMPRE** dar decisión específica, no opciones múltiples
- **SIEMPRE** explicar razonamiento
- **NO** cambiar scope del plan sin documentar
- **NO** asignar nuevas tareas sin actualizar work_plan.md
