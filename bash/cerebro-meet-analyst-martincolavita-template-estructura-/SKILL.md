---
name: cerebro-meet-analyst
description: >
  Habilidad para analizar transcripciones de reuniones del equipo del proyecto
  y extraerlas al OKF con estructura estandarizada. Incluye checklist obligatorio,
  Consulta Interactiva de Decisión ítem por ítem, detección de contradicciones
  con el cerebro digital y actualización automática de pendientes.
  Trigger: Cuando el usuario comparta un archivo de transcripción (.docx o .txt)
  de una reunión del equipo, o pida analizar/registrar una reunión.
license: Apache-2.0
metadata:
  author: equipo
  version: "1.1"
---

# cerebro-meet-analyst

## Cuándo se usa

Activar esta skill cuando:
- El usuario comparta un archivo `.docx` de transcripción de Teams
- El usuario pida registrar, analizar o incorporar el contenido de una reunión al cerebro digital
- El usuario mencione "meet", "reunión", "transcripción"

---

## Paso 0 — Extracción del texto (si el archivo es .docx)

Usar el script nativo:

```powershell
.\bin\extraer-reunion.ps1 "<ruta-al-archivo.docx>"
```

El script genera `scratch/transcript-YYYY-MM-DD.txt` listo para analizar. (Sólo existe en
PowerShell; en otro shell, extraé el texto del `.docx` con la herramienta que tengas a mano.)
Si el texto ya está disponible en `.txt`, saltear este paso.

---

## Paso 1 — Clasificar el tipo de reunión

Antes de analizar, identificar el tipo:

| Tipo | Descripción | Sección principal |
|------|-------------|-------------------|
| **Kick-off / Dominio** | Se explica el sistema actual, se presenta el problema | `dolores`, `contexto` |
| **Arquitectura** | Se toman decisiones técnicas y funcionales | `decisiones`, `RNs` |
| **Funcional** | Se relevan reglas de negocio con usuarios | `RNs`, `pendientes` |
| **Revisión** | Se revisa trabajo previo, se ajustan definiciones | `correcciones`, `pendientes` |

---

## Paso 2 — Análisis estructurado (checklist obligatorio)

Leer la transcripción completa y completar mentalmente este checklist antes de escribir:

```
[ ] DECISIONES: ¿Se tomó alguna decisión confirmada? (DEC-XXX)
[ ] REGLAS DE NEGOCIO: ¿Se definió alguna regla operativa? (RN-XXX)
[ ] DOLORES: ¿Se levantaron dolores del sistema actual? (solo en reuniones de dominio)
[ ] HIPÓTESIS: ¿Se mencionaron ideas/propuestas sin confirmar?
[ ] PENDIENTES: ¿Quedaron preguntas sin responder? (P-XXX)
[ ] CONTRADICCIONES: ¿Algo contradice documentos existentes en el OKF?
[ ] ACTORES: ¿Se mencionaron roles o personas nuevas?
```

**Regla:** No empezar a escribir el archivo hasta completar el checklist.

---

## Paso 3 — Verificar contradicciones con el OKF

Antes de escribir, leer obligatoriamente:
- `cerebro-digital/contexto.md`
- la ficha funcional del flujo que toca la reunión (`cerebro-digital/modulo-ejemplo/funcional/<flujo>.md`)
- `cerebro-digital/modulo-ejemplo/arquitectura/decisiones.md`

Marcar explícitamente en el borrador si algo contradice el OKF existente.

---

## Paso 4 — Confirmar cada ítem detectado (Consulta Interactiva de Decisión)

Antes de escribir nada, cada DEC-XXX, RN-XXX, dolor, hipótesis o pendiente identificado en el checklist del Paso 2 dispara **su propia interacción estructurada de decisión** — nunca se listan ni se resumen como texto o tabla dentro de la respuesta normal.

- Usar la herramienta nativa de preguntas/decisiones interactivas del entorno cuando esté disponible (ej. `AskUserQuestion` en Claude Code). Si el entorno no la tiene, simular el mismo aislamiento: una interacción por ítem, nunca mezclada en el cuerpo de la respuesta.
- El enunciado de cada interacción es una paráfrasis fiel de lo dicho en la transcripción (tipo DEC/RN/dolor/hipótesis/pendiente + contenido), sin agregar nada que no se haya dicho. Si algo no quedó claro en la reunión, se marca así explícitamente en el enunciado y se pregunta igual — nunca se completa el hueco por cuenta propia.
- Si además el ítem contradice el OKF (Paso 3), esa contradicción se incluye en el enunciado de la interacción.
- Opciones fijas de cada interacción — exactamente estas, sin variar el texto:
  - **Guardar** — el ítem entra al Paso 5 tal cual fue detectado.
  - **Ignorar** — el ítem no entra al archivo de la reunión.
  - **Editar y Guardar** — pedirle al usuario el texto corregido antes de incluirlo en el Paso 5; nunca reescribirlo por cuenta propia.
  - **Otro** — si la herramienta del entorno la ofrece nativamente, no agregarla como cuarta opción manual; si no la ofrece, agregarla como texto libre.

Solo los ítems marcados "Guardar" o "Editar y Guardar" (con su texto corregido) avanzan al Paso 5.

---

## Paso 5 — Escribir el archivo de reunión

**Ubicación del borrador:** `borrador/reuniones/meet-<tipo>-YYYYMMDD.md` (regla 3.1 de `AGENTS.md`: todo borrador nace en `borrador/`). Con el «sí» de una persona, `cerebro-curator` lo persiste en `cerebro-digital/modulo-ejemplo/extraccion-reuniones/meet-<tipo>-YYYYMMDD.md`.

> Las extracciones de reunión son **insumo crudo**, no conocimiento consolidado: por eso viven en `extraccion-reuniones/` y nunca dentro de los pilares `funcional/`, `metodologia/` o `arquitectura/`. El conocimiento validado que sale de una reunión se promueve al pilar que corresponda (ver Paso 6). Este archivo solo incluye los ítems confirmados en el Paso 4.

Usar el template estándar:

```markdown
---
id: meet-<tipo>-YYYYMMDD
tipo: extraccion-reunion
estado: F-Draft
modulo: modulo-ejemplo
title: <Tipo de reunión> — Meet DD/MM/YYYY
description: <Una línea con el propósito de la reunión>
tags: [<tipo>, <palabras-clave-del-contenido>]
last_updated: YYYY-MM-DD
author: "<usuario>"
fuentes: [meet-DDMMYYYY]
---

# <Título>

## Propósito
<Una o dos oraciones. Qué se buscó en esta reunión y qué marcó.>

**Asistentes:** <lista>

---

## Decisiones Clave
<Solo si hay decisiones confirmadas. Si no hay, omitir sección.>

### DEC-XXX — <Nombre>
**Estado:** Confirmado | En evaluación
...

---

## Reglas de Negocio
<Solo si se definieron RNs. Si no hay, omitir sección.>

### RN-XXX — <Nombre>
...

---

## Dolores del Sistema Actual
<Solo en reuniones de tipo Kick-off/Dominio.>

| # | Dolor | Detalle |
...

---

## Hipótesis (no confirmadas)
<Ideas mencionadas que no son decisiones. Siempre con nota de que son hipótesis.>

---

## Contradicciones detectadas con el OKF
<Si no hay, escribir: "Sin contradicciones detectadas.">

---

## Dudas y Preguntas
| # | Pregunta | Responsable |
...
```

---

## Paso 6 — Actualizar pendientes.md

**Siempre** al finalizar una reunión, comparar las preguntas abiertas confirmadas en el Paso 4 contra `pendientes.md`:

1. Leer `cerebro-digital/modulo-ejemplo/pendientes.md`
2. Por cada pregunta nueva → agregar con el siguiente número disponible (P-XXX)
3. Si alguna pregunta existente fue respondida en la reunión → moverla a "Resueltas" y trasladar el conocimiento al archivo correspondiente (`arquitectura/decisiones.md` o la ficha funcional que corresponda)

---

## Paso 7 — Actualizar log.md

Agregar una entrada en `cerebro-digital/log.md` con:
- Fecha
- Archivo creado
- Resumen de 2-3 líneas de lo que contiene
- Estado (F-Draft)
- "Validado por: <la persona que dio el sí>" (nunca el agente)

---

## Anti-patrones (PROHIBIDO)

- ❌ Escribir el archivo sin haber completado el checklist del Paso 2
- ❌ Omitir la verificación de contradicciones (Paso 3)
- ❌ Escribir el archivo sin haber pasado cada ítem por su propia Consulta Interactiva de Decisión (Paso 4)
- ❌ Renderizar los ítems detectados como texto o tabla dentro de la respuesta, en vez de disparar interacciones estructuradas
- ❌ Agrupar varios ítems en una sola interacción o pregunta genérica
- ❌ No actualizar `pendientes.md` al finalizar
- ❌ Mezclar hipótesis con decisiones confirmadas
- ❌ Poner estado `F-Verified` sin validación explícita del usuario
- ❌ Inventar datos que no están en la transcripción, incluso al procesar "Editar y Guardar" — si algo no quedó claro, va a `pendientes.md`
