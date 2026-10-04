---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: Barrido sistemático de errores con un valor objetivo escalado a la base de código, escalado por duplicación, seguimiento de áreas y verificación final. Se utiliza al ejecutar /bugsweep o cuando el usuario solicita una revisión sistemática de errores.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="bugsweep banner">

> **Español** — Versión oficial en español de `bugsweep`.


# /bugsweep — Flujo de trabajo sistemático de depuración (Español)

Búsqueda iterativa de errores con un criterio de parada convergente. Escala con la base de código, se escala cuando la búsqueda resulta superficial y evita la repetición mediante el seguimiento de áreas.

## 1. Calcular la tasa base

```
LOC = productive source lines (src/, lib/ — excluding tests, configs, docs, generated)
x = max(1, ceil(LOC / 1500))
base_rate = x * 3
```

| LOC | x | Tasa base |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

Notificar al usuario: "Base de código: {LOC} LOC → tasa base = {base_rate} pasadas de búsqueda limpias."

## 2. Bucle de búsqueda

```
counter = 0
target = base_rate
any_bug_found = False
checked = []  # (area_name, type: code|task)

LOOP:
  area = pick_new_area()  # see area rules
  checked.append(area)

  Perform a thorough bug search

  IF bug found:
    any_bug_found = True
    Fix following bugfix-protocol (phases 4+5)
    Review: see model rule (newer model classes: no external review needed)
    Commit + push
    counter = 0  # RESET
  ELSE:
    counter += 1
    Report: "✓ Clean: {area} — {counter}/{target}"

  IF counter >= target:
    IF NOT any_bug_found:
      # Doubling escalation: not a single bug → search too shallow?
      target = base_rate * 2
      any_bug_found = True  # escalate only ONCE
      Report: "⚠ No bug in {base_rate} passes → target doubled to {target}."
      CONTINUE LOOP
    ELSE:
      GOTO final verification
```

### Notas prácticas sobre el bucle de búsqueda (aprendidas de barridos reales)

- **Repositorios no-git:** Donde no exista `git` (p. ej., carpetas de proyecto sincronizadas en la nube), una **copia de seguridad versionada** reemplaza a "commit + push": cree `file_<ts>.bak` antes de la primera corrección. **Atención — la copia de seguridad previa a la corrección NO es un respaldo de su trabajo:** tras la última corrección, realice una nueva copia de seguridad `_FINAL_`; de lo contrario, un fallo de sincronización podría borrar toda la sesión de corrección.
- **Muchos errores conocidos desde el principio:** Si al inicio ya se conocen N errores (p. ej., de una ejecución anterior), el esquema "por error: corregir → revisar → commit → reiniciar" resulta poco práctico. Procese los errores conocidos como UN SOLO bloque de corrección (revisión conjunta al final) y comience a contar la tasa base / bucle de búsqueda a partir del primer error ENCONTRADO DE NUEVO. La lógica de reinicio sigue aplicándose a los errores encontrados durante el barrido.
- **El mismo error en múltiples lugares:** Un defecto encontrado (p. ej., una regex errónea, una suposición de formato incorrecta) a menudo se copia en otros lugares. Después de cada corrección, busque el mismo patrón en otras ubicaciones; esa es una "área" dedicada muy valiosa.

## 3. Reglas de área (anti-manipulación)

Un "área" es o bien un **enfoque de código** o bien una **tarea** (propósito del código).

### Enfoque de código
- Se puede **ampliar** (más archivos) o **desplazar** (diferente parte) entre pasadas
- NO debe ser exactamente la misma selección que en una pasada anterior
- CORRECTO: pasada 1 = `maintenance.py`, pasada 5 = `maintenance.py + orchestrator.py` (ampliado)
- INCORRECTO: pasada 1 = `maintenance.py`, pasada 5 = `maintenance.py` (idéntico)

### Tarea (propósito)
- Se puede hacer **más granular** (revisar una subfunción) o **más amplia** (funciones relacionadas juntas)
- NO debe ser exactamente la misma tarea
- CORRECTO: pasada 1 = "seguridad de hilos en el watchdog", pasada 5 = "seguridad de hilos en toda la bandeja" (más amplia)
- CORRECTO: pasada 1 = "detección de procesos", pasada 5 = "coincidencia de marcadores de almacenamiento dentro de la detección de procesos" (más granular)
- INCORRECTO: pasada 1 = "seguridad de hilos en el watchdog", pasada 5 = "seguridad de hilos en el watchdog" (idéntico)

### Nombramiento
- El área DEBE nombrarse ANTES de la búsqueda (sin asignación retroactiva)
- Formato: `"{nombre}" ({tipo}: code|task)`

## 4. Verificación final

Una vez counter >= target Y any_bug_found:

**Paso A — fase 5 del bugfix-protocol:**
- [ ] Suite completa de pruebas en verde (`pytest`)
- [ ] **Ejecutar realmente la ruta de ejecución modificada al menos una vez**, no solo las pruebas. Las pruebas unitarias en verde sobre código que nunca llama a la ubicación modificada ofrecen una falsa seguridad. Ejecute la ruta realmente modificada (ejecución simulada, prueba de humo, invocación por CLI) y verifique la ausencia de rastreos de error (tracebacks), errores de firma o de sintaxis/nombres. `py_compile` o un simple import solo comprueban la sintaxis, no si la ruta funciona en ejecución.
- [ ] **Cada corrección tiene al menos una prueba que la cubre:** una corrección sin una prueba que active realmente la rama modificada se considera no verificada (para rutas de orquestación/red, combine mocks + ejecuciones simuladas si es necesario).
- [ ] Verificación de tipos (si está configurada)
- [ ] Linter (si está configurado)
- [ ] Casos límite de las correcciones de la sesión revisados

**Paso B — revisión (regla de modelos):**
- **Clases de modelos más recientes (p. ej., Claude 5 / clase Fable):** NO se requiere revisión externa por parte de un asesor o segundo modelo. El Paso A (pruebas + una ejecución de humo real) constituye la verificación. Opcionalmente, ante una incertidumbre real, se puede usar un subagente de revisión nuevo; sin embargo, verifique sus hallazgos empíricamente (probando contra el código no modificado) antes de contabilizarlos como errores. Contexto (experiencia de barrido 2026-06-11): el segundo revisor no estaba disponible, el subagente sustituto entregó 1 hallazgo (confianza 85%) que una prueba demostró que no era un error; una revisión externa no alteró el resultado.
- **Modelos más antiguos:** discusión final con el asesor (opción de reserva: un segundo modelo como revisor); el asesor confirma o señala deficiencias.

**Si se encuentra un error durante la verificación:**
→ Corregir + probar + commit
→ REINICIAR: counter = 0, target = base_rate (nuevo, SIN duplicación)
→ Volver al bucle de búsqueda (la lista checked se conserva, any_bug_found = True)

**Si la verificación es limpia:**
→ COMPLETADO. Commit + push. Imprimir el protocolo.

## 5. Protocolo (al final)

```markdown
## Bug Sweep Result

- **Codebase:** {LOC} LOC
- **Base rate:** {base_rate} (escalated: {target})
- **Areas checked:** {len(checked)}
- **Bugs found:** {count}
- **Resets:** {reset_count}
- **Doubling triggered:** yes/no
- **Fixes:**
  - {title} — {commit_hash}
  - ...
- **Final test suite:** {passed}/{total} green
- **Review verdict:** self-verification (newer model class) / advisor confirmed / gaps named
```

## Cuándo usar este flujo de trabajo

- Después del desarrollo de funcionalidades (garantía de calidad)
- Antes de un lanzamiento (barrido de aceptación)
- Periódicamente como control de higiene
- Cuando el usuario escribe `/bugsweep`

## Interacción con otras habilidades

- **bugfix-protocol:** procedimiento de corrección (fases 4+5) para cada error encontrado
- **systematic-debugging:** para errores difíciles de reproducir dentro del barrido
- **code-review:** se puede utilizar como un área de tarea

---

## Historial de cambios

### 1.1.0 (2026-06-13)
- Se incorporó la regla de modelos para el paso B (desde la instalación local de la habilidad, estado 2026-06-11): las clases de modelos más recientes se autoverifican mediante pruebas + una ejecución de humo real, sin necesidad de revisión externa; el campo del protocolo "Veredicto de revisión" se amplió en consecuencia

### 1.0.0 (2026-06-13)
- Primera publicación en la biblioteca de habilidades (adoptado desde la instalación local de la habilidad, estado 2026-06-01)
