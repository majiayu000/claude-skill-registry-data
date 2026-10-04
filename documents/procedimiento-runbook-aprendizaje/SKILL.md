---
name: procedimiento-runbook-aprendizaje
description: >-
  Ejecuta tareas bajo un runbook acordado y, al cerrar, sintetiza procedimiento,
  decisiones, orden y excepciones para persistir como conocimiento reutilizable
  del asistente (log/KB/skill). Usar cuando el usuario activa RUNBOOK,
  modo procedimiento aprendizaje, capturar lógica operativa, cerrar corrida con
  aprendizajes, o enriquecer conocimiento del bot tras ejecutar pasos repetibles.
---

# Procedimiento runbook + aprendizaje (bot knowledge)

## Objetivo

En una misma sesión: **(1)** ejecutar lo que haya que correr con claridad y trazabilidad, **(2)** extraer de esa ejecución la **lógica y el procedimiento** que valga la pena conservar, **(3)** dejarlo en un artefacto que el bot pueda reutilizar después (archivo en repo, skill derivada, o nota que el humano copia al Builder/KB).

## Activación (el humano debe decirlo explícito)

Activar leyendo esta skill cuando el usuario use cualquiera de:

- `RUNBOOK ON` / `RUNBOOK OFF` (OFF cierra solo el modo; no borra capturas)
- `modo procedimiento aprendizaje` / `capturar procedimiento`
- `corrida + aprendizajes` / `cerrar con runbook`

Si el mensaje es ambiguo, confirmar en una frase: objetivo de la corrida, entorno (local/prod), y si al final deben **persistirse** cambios en disco.

## Flujo obligatorio (orden fijo)

### 1) Intake breve (antes de tocar herramientas)

Registrar mentalmente o en el chat:

- **Qué** se debe lograr (criterio de “listo”).
- **Qué no** tocar (límites de alcance).
- **Orden** preferido de pasos si el humano lo dio; si no, proponer orden y pedir OK si hay riesgo (deploy, datos reales, facturación).

### 2) Ejecución (runbook vivo)

- Ejecutar con **checklist** visible en la respuesta (markdown `- [ ]` / `- [x]`).
- En cada paso delicado: comando exacto o acción, resultado esperado, y qué hacer si falla (un reintigo o ruta alternativa, no ramificar sin fin).
- Si aparece **nueva regla de negocio** o **excepción** (“excepto cuando…”, “nunca en prod…”), marcarla como **CANDIDATO A KB** en el propio checklist.

### 3) Cierre: paquete de conocimiento (siempre al terminar la corrida)

Generar un bloque titulado **`### RUNBOOK-CAPTURE`** con esta estructura mínima:

```markdown
### RUNBOOK-CAPTURE
- **Contexto**: …
- **Procedimiento resumido** (pasos numerados, 3–10 ítems): …
- **Decisiones / reglas** (imperativo, una línea cada una): …
- **Errores vistos y fix**: …
- **Anti-patrones** (qué no repetir): …
- **Siguiente mejora** (opcional, una sola): …
```

Mantener el capture **corto**; detalle largo va a un archivo solo si el humano lo pide.

### 4) Persistencia (solo con instrucción explícita del humano)

Opciones (el humano elige una):

| Destino | Cuándo usarlo |
|--------|----------------|
| Archivo log en repo (p. ej. `docs/team/RUNBOOK-LEARNING-LOG.md` o ruta que indique el humano) | Historial consultable por el equipo y por el agente en futuras sesiones |
| **Nueva skill** en `.cursor/skills/<nombre>/SKILL.md` | Procedimiento estable y repetible; seguir convenciones del repo y nombre en kebab-case |
| **Parche a skill existente** | Delta pequeño sobre una skill ya usada en Panelin/BMC |
| **Solo en chat** (sin commit) | Exploración; el humano copia al GPT Builder u otra KB externa |

**No** crear ni editar archivos de documentación fuera de lo que el humano autorice en ese mensaje o en el cierre de la corrida.

## Reglas de calidad del conocimiento

- Preferir **comandos y criterios verificables** sobre narrativa.
- Separar **hecho observado** vs **inferencia**; etiquetar inferencias como tal.
- Si algo depende de fecha, entorno o credencial, **nombrar la dependencia** explícitamente.
- Si el capture contradice una skill existente, **señalar la contradicción** y no silenciarla.

## Relación con otras skills

- Si el procedimiento madura y merece skill dedicada, usar el flujo de creación de skills del proyecto (estructura `SKILL.md` + `description` con triggers).
- No duplicar contenido enorme: en la skill nueva, enlazar al log o al doc canónico en una línea.

## Desactivación

`RUNBOOK OFF`: dejar de anexar `RUNBOOK-CAPTURE` en cada respuesta, salvo que el humano pida un capture final de esa sesión.
