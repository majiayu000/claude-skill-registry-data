---
name: Matriz de soportes Movistar
key: matriz-soportes-movistar
description: Papel comunicativo de cada soporte en el mix Movistar y principios transversales que ordenan como baja un territorio a cada soporte. Base de la capa de orientacion de comunicacion.
version: 1.0.0
owner: comunicacion-movistar
status: active
loaded_by: Maia Planner, Maia Copywriter, Maia Storyteller, Maia Campaign Manager
---

# Matriz de soportes Movistar

Esta skill define qué trabajo hace cada soporte en el mix de Movistar. Es la base de la capa de orientación de comunicación: en lugar de dibujar doce piezas por territorio, el sistema declara qué papel juega cada soporte y qué misión específica tiene en ese territorio concreto.

La matriz es **común a todos los territorios**. Lo que cambia por territorio son dos cosas: qué soportes se activan y cuál es su misión concreta. No todos los territorios necesitan estar en todos los canales.

---

## 1. La matriz

La columna "Papel" es fija: describe qué hace ese soporte siempre, en cualquier territorio. La columna "Aplicación al territorio" la rellena el Maia Copywriter para cada territorio activo, en una línea.

| Soporte | Papel | Producción MAIA | Playbook |
|---|---|---|---|
| TV / ATL | Construye significado y valor amplio. No intenta explicar la oferta completa. | No | -- |
| Exterior | Una idea que se entiende en segundos. | No | -- |
| Digital | Captura intención. Beneficio primero, oferta después. | Sí | `channel-playbook-digital` |
| M+ Spot / Preroll | Habla en el momento de consumo. Contextual y de baja presión. | Sí | `channel-playbook-movistarplus` |
| M+ Banner | Recordatorio contextual, no tablón comercial. Un mensaje, una acción. | Sí | `channel-playbook-movistarplus` |
| Email / BTL | Segmenta, personaliza y activa. Aquí sí cambia la oferta según colectivo, con una sola propuesta por cliente. | Sí | `channel-playbook-email` |
| RCS | Explica algo más que un SMS, pero mantiene simplicidad visual. Beneficio, oferta y CTA sin convertirlo en folleto. | No | -- |
| Notipush | Detonador, no explicación. Hito más urgencia. | No | -- |
| Tienda / PLV | Abre conversación. El precio ayuda a cerrar, no tiene que ser siempre el titular. | Sí | `channel-playbook-tienda` |
| Caballete / material táctico | Activación concreta y legible. Oferta o hito puntual, nada de narrativa compleja. | Sí | `channel-playbook-tienda` |
| TMK / Atención | Explica, resuelve objeciones y cierra. Propensión e intención para dar al agente el mejor argumento. | No | -- |
| Web / Landing | Lugar donde sí puede vivir la explicación completa: producto, competiciones, promoción, FAQs, condiciones y contratación. | Sí | `channel-playbook-web` |

### 1.1 La columna "Producción MAIA"

Distingue dos cosas que conviene no mezclar:

- **Producción MAIA = Sí**: MAIA produce orientación de comunicación y, cuando la fase de materialización está activa, piezas para ese soporte. Tiene playbook operativo asociado.
- **Producción MAIA = No**: el soporte aparece en la matriz porque forma parte de la orquestación y el comité necesita ver qué papel juega, pero MAIA no genera copy ni piezas para él. Se describe su misión en el territorio y ahí termina.

TV/ATL y Exterior están en la matriz como contexto de orquestación. La decisión de 2026-07-13 que deja ATL fuera de alcance sigue vigente y esta skill no la modifica: MAIA dice qué papel juega la TV en el territorio, no escribe el spot.

Un soporte con `Producción MAIA = No` nunca lleva copy prototype, nunca lleva pieza y nunca entra en el scoring de principios por pieza. Si un agente produce copy para uno de estos soportes, es un fallo que el Maia Campaign Manager bloquea.

---

## 2. Los cinco principios transversales

Estos principios ordenan cómo baja un territorio a cada soporte. Son el criterio objetivo con el que después se evalúa el trabajo de las agencias creativas, así que se presentan de forma visible en el documento ejecutivo, no como nota al pie.

1. **Una pieza, una idea dominante.** Especialmente en CRM y BTL: segmentar no significa acumular argumentos.
2. **Cada soporte hace un trabajo distinto.** No se adapta mecánicamente una creatividad master a todos los formatos.
3. **Cuanto más masivo es el medio, más simple y más de valor debe ser el mensaje.** Cuanto más dirigido, más se puede personalizar oferta y CTA.
4. **El contexto manda.** Movistar+ habla desde el consumo, la tienda desde la conversación, el CRM desde el conocimiento del cliente, Search desde la intención.
5. **La profundidad vive al final del journey.** ATL inspira, digital y CRM activan, web y landing explican, el canal humano resuelve y cierra.

---

## 3. Regla de activación por territorio

Para cada territorio, el sistema declara qué soportes se activan y por qué. Cada activación lleva su procedencia según la sección 7 de `contexto-sistema-maia`:

- El soporte viene declarado en el plan comercial del área: `nivel: plan_area`.
- El soporte lo recomienda MAIA porque el objetivo del territorio lo pide: `nivel: propuesta`.

Esta distinción es obligatoria. Un soporte que MAIA añade por criterio propio nunca se presenta como si viniera del plan del área.

El Maia Planner lo escribe agrupado por territorio, en el campo `soportes_activos_por_territorio`. El Maia Copywriter lo hereda y lo escribe dentro de cada campaña como `soportes_activos`. La forma de cada entrada es la misma en los dos:

```json
"soportes_activos": [
  {
    "soporte": "Email / BTL",
    "mision_en_territorio": "string (una linea: que trabajo concreto hace este soporte en este territorio)",
    "procedencia": { "nivel": "plan_area|propuesta", "fuente": "string", "validacion": "confirmado|a_validar|no_confirmado" }
  }
]
```

Los soportes no activados no se listan con una justificación larga. Basta con que no aparezcan. Si un soporte se descarta de forma deliberada y esa decisión tiene valor informativo (por ejemplo, se descarta tienda en un territorio puramente digital), va en un campo `soportes_descartados` con motivo en una línea.

### 3.1 Cuántos soportes por territorio

No hay número fijo, pero un territorio con los doce soportes activos casi siempre es un territorio mal acotado. La pregunta de control es: ¿este soporte hace un trabajo que ningún otro hace en este territorio? Si la respuesta es no, no se activa.

---

## 4. Cómo lo usa cada agente

**Maia Planner.** Decide qué soportes se activan por territorio y marca la procedencia de cada activación. Cruza esta matriz con `matriz-objetivo-canal` y `rol-medios-movistar`: la matriz de soportes dice qué papel juega cada uno, la matriz objetivo-canal dice cuál encaja con el objetivo, y el rol de medios da el peso en el mix.

**Maia Copywriter.** Rellena la misión por territorio de cada soporte activo, en una línea. No escribe copy para soportes con `Producción MAIA = No`. Verifica cada territorio contra los cinco principios transversales.

**Maia Storyteller.** Renderiza la matriz común una vez en el documento, y por territorio solo la fila de los soportes activos con su misión. No repite la matriz completa en cada territorio: sería convertir el documento en una enciclopedia.

**Maia Campaign Manager.** Audita en V22 que cada soporte activo referencia un nombre existente en esta matriz, que lleva misión y procedencia, y que ningún soporte con `Producción MAIA = No` tiene copy, pieza o scoring asociado.

---

## 5. Qué no es esta skill

No es un playbook. Un playbook define la operativa de producción de un canal: formatos, medidas, reglas de copy, anti-patrones de maquetación. Esta matriz define el papel comunicativo del soporte en el mix. Para los soportes con playbook, ambas cosas conviven: la matriz dice qué trabajo hace, el playbook dice cómo se produce.

No es una decisión de inversión ni de reparto de presupuesto. Eso queda fuera del alcance de MAIA.
