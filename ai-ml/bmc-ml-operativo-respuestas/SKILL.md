---
name: bmc-ml-operativo-respuestas
description: >-
  Ciclo operativo Mercado Libre (BMC): levantar API y OAuth, exportar corpus de
  preguntas, priorizar UNANSWERED, iterar la KB de respuestas con el humano,
  cotizar con /calc/cotizar, normalizar moneda (U$S→USD) y publicar con
  POST /ml/questions/:id/answer. Usar cuando pidan operar preguntas ML,
  mejorar ML-RESPUESTAS-KB-BMC, publicar respuestas al vendedor, o repetir el
  flujo “servicios listos → KB → ML” sin improvisar pasos.
---

# BMC — ML operativo (KB + publicación de respuestas)

Orquesta el mismo flujo que un agente humano+IA en Cursor: **servicios listos → datos de preguntas → mejora de conocimiento → redacción con precio → publicación en ML**.

**Complementa (léelo primero si falta contexto técnico):** [`.cursor/skills/bmc-mercadolibre-api/SKILL.md`](../bmc-mercadolibre-api/SKILL.md), [`docs/ML-OAUTH-SETUP.md`](../../../docs/ML-OAUTH-SETUP.md), [`docs/team/panelsim/knowledge/ML-TRAINING-SYSTEM.md`](../../../docs/team/panelsim/knowledge/ML-TRAINING-SYSTEM.md).

**KB canónica de tono y criterios:** [`docs/team/panelsim/knowledge/ML-RESPUESTAS-KB-BMC.md`](../../../docs/team/panelsim/knowledge/ML-RESPUESTAS-KB-BMC.md) (voz, checklist, §4 por familia de publicación, **§12** borradores / anexo).

**Inventario para agentes:** [`docs/team/panelsim/knowledge/KNOWLEDGE-INVENTORY-FOR-AI-AGENTS.md`](../../../docs/team/panelsim/knowledge/KNOWLEDGE-INVENTORY-FOR-AI-AGENTS.md).

---

## 0. Reglas de oro (no negociar con el cliente en ML)

1. **Precio primero** cuando el caso lo permita (cotización real vía API de calculadora).
2. **No** pedir al comprador que “verifique MATRIZ” ni exponer jargon interno.
3. **Cortes:** amoladora (no “sierra” genérica); límites + solución + precio si aplica.
4. **Medidas ya suficientes:** no repreguntar lo que el hilo ya dio.
5. **Moneda en texto que va a ML:** el servidor aplica `normalizeMlAnswerCurrencyText` (`U$S`/`u$s` → `USD`, luego mitigación de `$`); ver [`server/lib/mlAnswerText.js`](../../../server/lib/mlAnswerText.js). Redactar pensando en **USD** + montos legibles.
6. **Human-in-the-loop:** el humano aprueba/edita KB y **cada** texto antes de `POST` si el contexto es sensible o legal.

---

## 1. Servicios listos (local)

| Paso | Comando / acción |
|------|-------------------|
| `.env` presente | `npm run env:ensure` |
| API en **:3001** | `npm run start:api` (o stack completo según [`AGENTS.md`](../../../AGENTS.md)) |
| OAuth ML OK | `npm run ml:verify` (requiere API arriba) |
| HTTPS / callback si OAuth falla | `npm run ml:local` o ngrok según [`docs/ML-OAUTH-SETUP.md`](../../../docs/ML-OAUTH-SETUP.md) |

No inventar “tokens OK”: usar salida real de `ml:verify` o `/auth/ml/status`.

---

## 2. Obtener y filtrar preguntas

| Objetivo | Comando |
|----------|---------|
| Lista viva desde ML (API) | `GET http://127.0.0.1:3001/ml/questions` (Bearer `API_AUTH_TOKEN` si aplica) |
| Corpus offline para análisis | `npm run ml:corpus-export` → JSON bajo `docs/team/panelsim/reports/ml-corpus/exports/` (gitignored salvo que se versione a propósito) |
| Priorizar hilos abiertos | En el JSON exportado, filtrar por estado **`UNANSWERED`** (`jq` / script; ver `reference.md`) |

Tratar IDs y texto de compradores con **mínima exposición** en commits y en `PROJECT-STATE` (solo IDs si hace falta trazabilidad).

---

## 3. Mejorar la KB con el humano

1. Abrir [`ML-RESPUESTAS-KB-BMC.md`](../../../docs/team/panelsim/knowledge/ML-RESPUESTAS-KB-BMC.md).
2. Ajustar **§2–§4**, **§7** checklist, **§12** borradores o anexos según correcciones del humano (ej. babeta adosar 16 cm, chapa galv. prepintada c24, etc.).
3. Alinear el modelo automático: bloque **Canal Mercado Libre** en [`server/lib/chatPrompts.js`](../../../server/lib/chatPrompts.js) debe reflejar la KB (sin secretos).
4. Tras cambios sustantivos en KB/prompts: línea breve en [`docs/team/PROJECT-STATE.md`](../../../docs/team/PROJECT-STATE.md) → **Cambios recientes**.

---

## 4. Cotizar para fundamentar el precio en la respuesta

Usar la API local (misma base que `start:api`):

- Escenarios típicos: `POST /calc/cotizar` (ej. `solo_fachada`, dimensiones, lista según política interna).
- Aproximaciones de solo panel: `POST /calc/cotizar/presupuesto-libre` con m².

Detalle de payloads en [`reference.md`](./reference.md). **No** citar en ML el nombre interno de lista (“web/BMC”); sí monto + IVA según criterio ya acordado en KB.

---

## 5. Publicar respuesta en Mercado Libre

**Solo con texto aprobado por el humano** (o política explícita de auto‑post).

```http
POST http://127.0.0.1:3001/ml/questions/:questionId/answer
Content-Type: application/json
Authorization: Bearer <API_AUTH_TOKEN>

{ "text": "…" }
```

- El servidor normaliza moneda antes de enviar a ML (`mlAnswerText`).
- **200** → hilo pasa a contestado en ML; revisar en UI vendedor.
- Respuestas ya publicadas **no** se reemplazan por el mismo endpoint: correcciones van por **UI ML** si hace falta.

---

## 6. Verificación y cierre

- `npm test` si se tocó `server/lib/mlAnswerText.js` o reglas asociadas.
- Si el comportamiento depende del **runtime Cloud Run**, recordar deploy API según [`AGENTS.md`](../../../AGENTS.md) / skill deploy.
- Opcional: `npm run ml:corpus-export` de nuevo y diff de conteos `UNANSWERED`.

---

## 7. Referencia rápida

Ver **[`reference.md`](./reference.md)** (`curl`, variables de entorno, ejemplos `jq`, plantillas JSON).
