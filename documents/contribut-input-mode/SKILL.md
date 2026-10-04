---
name: contribut-input-mode
description: >
  Two-phase chat workflow: refine and enrich the user's raw message into a
  clear "official input" before doing heavy work. Activate with CONTRIBUT ON
  or phrases like "modo Contribut", "Contribut", "refinar mi input antes de
  responder". Deactivate with CONTRIBUT OFF. One-shot bypass: CONTRIBUT SKIP.
  Gate to full reply: user sends ACEPTO BORRADOR (optionally pasting the
  refined text). Use when the user wants higher input precision and alignment
  before execution.
---

# Contribut input mode (refinar input antes de ejecutar)

## Rol del agente

Actuar como **contributor**: primero **mejorar y explicitar** lo que el usuario quiere decir (con contexto de sesión, archivos relevantes y tarea actual). **No** ejecutar trabajo pesado (implementación larga, diffs grandes, investigación exhaustiva) hasta que el usuario **acepte** el borrador con la frase de paso.

## Activación y estado

| Comando / frase | Efecto |
|-----------------|--------|
| `CONTRIBUT ON` o "activá modo Contribut" / "modo Contribut" | Modo **activo** en este hilo hasta `CONTRIBUT OFF`. |
| `CONTRIBUT OFF` | Modo **inactivo**; respuestas normales. |
| `CONTRIBUT SKIP` | **Solo este mensaje**: saltar refinamiento; responder en modo normal. El siguiente mensaje vuelve al protocolo Contribut si el modo sigue ON. |
| `ACEPTO BORRADOR` | Cierre de fase 1; opcionalmente pegar debajo el texto refinado acordado. Luego ejecutar fase 2 (respuesta completa / código / búsquedas). |

**Con comandos que exigen ejecución (p. ej. `/nxt`):** si el modo Contribut está **ON** y el usuario pide un informe que requiere `git`/lectura de docs en el mismo turno, usar **`CONTRIBUT SKIP`** en ese mensaje (respuesta directa con herramientas), **o** enviar primero el borrador y luego **`ACEPTO BORRADOR`** antes del comando — así no choca la fase 1 “solo plantilla” con el flujo `/nxt`.

**Nota de producto:** Cursor no intercepta Enter; el usuario envía mensajes igual. El agente debe **autodisciplinarse** a este protocolo cuando el modo está ON.

## Cuándo aplicar esta skill

- El usuario invoca explícitamente: Contribut, modo Contribut, refinar input, CONTRIBUT ON, etc.
- En el hilo ya quedó establecido `CONTRIBUT ON` y no hubo `CONTRIBUT OFF`.

## Fase 1 — Solo borrador (modo ON, mensaje sin `CONTRIBUT SKIP`)

Ante un mensaje del usuario (intención bruta), responder **únicamente** con el siguiente bloque. **Prohibido** en esta respuesta: escribir código de solución, aplicar parches, o dar la "respuesta final" larga.

### Plantilla obligatoria (títulos visibles para el usuario)

Usar estos encabezados en Markdown:

#### Tu intención (resumida)

1–3 frases: qué quiere lograr el usuario con este turno.

#### Supuestos

- Lista corta de supuestos razonables inferidos del chat y contexto.
- Si algo no está respaldado por evidencia en el repo o el mensaje: marcar **`NEEDS_CONFIRMATION`** y una pregunta concreta.

#### Input refinado propuesto

Texto listo para copiar como **mensaje oficial** (párrafo o lista numerada): objetivo, alcance, restricciones, definición de "listo".

#### Preguntas mínimas (si aplican)

Como máximo **3** preguntas, solo si bloquean calidad o hay ambigüedad de riesgo. Si no hace falta: escribir *Ninguna.*

#### Cómo seguir

Línea fija al pie (puede ir en español):

> Cuando estés conforme, envía **`ACEPTO BORRADOR`** (y opcionalmente pega el texto refinado que quieras usar). Ahí paso a ejecutar / responder en serio.

## Fase 2 — Después de `ACEPTO BORRADOR`

- Tratar el **input refinado** (el propuesto o el pegado por el usuario) como la fuente de verdad.
- Entonces sí: herramientas, código, planes largos, etc., según la petición.

## Si el mensaje trae refinamiento + aceptación en un solo turno

Si el usuario en un mismo mensaje incluye el texto refinado **y** la línea `ACEPTO BORRADOR`, se puede **omitir** una vuelta extra de solo-borrador y pasar directo a fase 2 usando ese texto como input oficial.

## Memoria y contexto (proyecto BMC)

Si el repositorio tiene [`docs/team/PROJECT-STATE.md`](docs/team/PROJECT-STATE.md) u otro doc de sesión que el usuario esté usando, **considerar** leerlo cuando el modo Contribut esté ON y el mensaje hable de estado del proyecto, pendientes o handoff — sin bloquear el flujo si el archivo no existe.

## Al reconocer `CONTRIBUT ON`

Responder brevemente confirmando modo activo y recordar:

- `CONTRIBUT OFF` para salir
- `CONTRIBUT SKIP` para una respuesta directa puntual
- `ACEPTO BORRADOR` para cerrar el borrador y continuar

## Ejemplo mínimo

**Usuario:** `CONTRIBUT ON`  
**Agente:** Confirmación + recordatorio de frases.

**Usuario:** arregla lo del pdf  
**Agente:** Fase 1 con plantilla (intención, supuestos con NEEDS_CONFIRMATION si no está claro qué PDF, input refinado propuesto, preguntas).

**Usuario:** `ACEPTO BORRADOR`  
**Agente:** Fase 2 — investigar / proponer parche según el input refinado acordado.

## Verificación manual (dry-run)

1. Nuevo chat: `CONTRIBUT ON`.
2. Mensaje vago a propósito → comprobar que la respuesta es **solo** la plantilla de fase 1.
3. `ACEPTO BORRADOR` → comprobar que la siguiente respuesta **sí** ejecuta o responde en profundidad.
4. `CONTRIBUT SKIP` con modo ON → una respuesta directa sin plantilla; siguiente mensaje otra vez con plantilla si sigue ON.
