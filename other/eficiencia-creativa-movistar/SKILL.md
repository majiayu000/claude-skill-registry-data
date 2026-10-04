---
name: Eficiencia creativa Movistar
key: eficiencia-creativa-movistar
description: Principio de reutilizar antes que producir y framework de decision REUSE / ADAPT / REFRESH / CREATE por territorio. Define cuanto trabajo creativo nuevo hay que hacer realmente cada mes, con dato de rendimiento cuando existe y con criterio cualitativo cuando no.
version: 1.1.0
owner: comunicacion-movistar
status: active
loaded_by: Maia Copywriter, Maia Campaign Manager, Maia Storyteller
---

# Eficiencia creativa Movistar

## 1. El principio

**No partimos de cero cada mes.** Priorizamos el uso de activos, códigos y formatos ya construidos y validados. La creación nueva se concentra allí donde existe una nueva necesidad de comunicación o donde los activos actuales no cumplen el objetivo.

Dicho de otra forma: reutilizar antes que producir. Si ya existe una idea, pieza, formato o recurso que ha funcionado y sigue siendo válido, se reaprovecha. La creatividad nueva se reserva para cuando cambia de verdad el problema de comunicación, el producto o el contexto.

Este principio va **antes** de toda la sección de orientación de comunicación en el documento ejecutivo, no como nota al pie. Cambia la pregunta que se hace el comité: no solo "qué vamos a comunicar" sino "cuánto trabajo nuevo hay realmente que hacer".

No tiene sentido que octubre genere una campaña nueva para todo simplemente porque empieza un mes nuevo.

---

## 2. Las cuatro decisiones

Cada territorio lleva una decisión previa, antes de cualquier orientación creativa.

| Decisión | Cuándo se aplica |
|---|---|
| REUSE | La pieza existente sigue resolviendo el objetivo y funciona en ese soporte. |
| ADAPT | La idea funciona, pero hay que actualizar fecha, oferta, producto, target o CTA. |
| REFRESH | Se mantiene el territorio o el código, pero necesita novedad o relevancia para el momento. |
| CREATE | No existe un activo válido, o el problema de comunicación ha cambiado sustancialmente. |

La decisión se toma **por territorio**, no por pieza. Un territorio puede tener matices por soporte (REUSE en digital, ADAPT en CRM), y en ese caso se declara la decisión dominante y el matiz en el racional.

---

## 3. Dos modos de decidir, según haya dato o no

El criterio para decidir qué activo merece seguir vivo, cuál hay que adaptar y dónde hace falta crear algo nuevo debería basarse en rendimiento. Desde septiembre de 2026 el sistema tiene una fuente parcial de ese rendimiento: el **informe semanal de Publicidad** de Analítica de Comunicación, que baja al detalle de creatividad individual con código propio y sus métricas de respuesta. Ver `informe-semanal-publicidad`.

Eso parte la decisión en dos modos, y el agente debe saber siempre en cuál está.

### 3.1 Modo con dato (preferente)

El brief trae, en `rendimiento_periodo_anterior.por_creatividad`, una entrada cuyo `territorio_asociado` es este territorio, con al menos una métrica de respuesta medida: CTR, leads, CPL, VTR, clics o interacción.

- La decisión **cita el dato** con la semana y la métrica concreta. Ejemplo de racional válido: "REUSE. La pieza FA-FOTO lidera la conversión de la campaña con 1.494 leads y es la más eficiente del periodo (informe del 11/09)."
- `modo`: `con_dato`.
- `evidencia_rendimiento`: completo, con métrica, valor, creatividad y semana.
- `necesita_validacion_inventario`: `false` para ese territorio.
- `procedencia`: `nivel: propuesta` y `validacion: no_confirmado`, **igual que en el modo cualitativo**. Esto no es un descuido: la sección 7.2 de `contexto-sistema-maia` establece que toda afirmación de nivel `propuesta` es `no_confirmado` hasta que un gate humano la apruebe, y una decisión de producción lo es tenga o no dato detrás. Lo que distingue los dos modos es `modo` y `evidencia_rendimiento`, no la procedencia. El dato respalda la recomendación; no la aprueba.

### 3.2 Modo sin dato (degradado)

No hay informes disponibles, la cobertura es baja, o el territorio no tuvo actividad medida el mes anterior.

- La decisión es un **juicio cualitativo** argumentado con las señales de la sección 4.
- `modo`: `cualitativo`.
- `evidencia_rendimiento`: `null`.
- `necesita_validacion_inventario`: `true`.
- `procedencia`: `nivel: propuesta` y `validacion: no_confirmado`.
- **Está prohibido presentar la decisión como basada en datos.** Nada de "según el rendimiento histórico" ni "los datos indican". Presentar un juicio cualitativo como decisión basada en datos es exactamente el problema que este sistema intenta resolver.

### 3.3 Qué métricas cuentan y cuáles no

Solo las **métricas de respuesta de la pieza** deciden sobre un activo: CTR, leads, CPL, VTR, clics, interacción. Miden cómo reacciona la gente a esa creatividad concreta.

No deciden sobre un activo, y usarlas para ello es un error:

- **Impactos, impresiones, frecuencia, reparto por soporte.** Miden inversión, no calidad. Un activo con muchos impactos es un activo con presupuesto.
- **Ventas.** No están atribuidas a la creatividad. Una campaña puede vender menos con la mejor pieza posible porque cambió el contexto de mercado.

Detalle completo en la sección 4 de `informe-semanal-publicidad`.

### 3.4 Lo que sigue faltando

El informe cubre lo que estuvo en el aire el mes anterior. Un activo que existe pero no se emitió no aparece, y sobre él no hay dato. Por eso el **inventario completo de activos vivos sigue pendiente del cliente**: el informe da rendimiento de lo emitido, no catálogo de lo disponible.

---

## 4. Señales cualitativas admisibles

Estas son las señales que sostienen una decisión en **modo cualitativo**, y que también enriquecen el racional en modo con dato. Siempre etiquetadas con su procedencia:

- **El propio plan comercial plantea continuidad.** Si la PPT del área habla de continuidad de formatos y espacios en lugar de reinvención, es señal de REUSE o ADAPT (`nivel: plan_area`).
- **Existe una campaña de marca viva que el plan pide conectar.** Si el plan pide explícitamente enganchar el BTL con una campaña de TV en emisión, es REUSE del código de campaña más ADAPT al servicio concreto (`nivel: plan_area`).
- **El territorio funcional está establecido pero el problema de octubre es nuevo.** Si el mensaje base sigue siendo válido y lo que cambia es una fricción concreta a resolver, es ADAPT o REFRESH (`nivel: propuesta`).
- **Hay códigos de producto o campaña ya construidos.** Si el territorio se apoya en códigos que el mercado ya reconoce, la tarea es orquestar y actualizar, no producir un universo nuevo (`nivel: propuesta`).
- **El producto o el contexto competitivo ha cambiado de verdad.** Solo aquí CREATE está justificado (`nivel: plan_area` si el cambio viene declarado, `insight_estrategia` si viene de trend flash o mercado).

Una decisión CREATE sin ninguna de estas señales que la respalde es la que más escrutinio necesita. El sesgo por defecto del sistema es hacia REUSE.

---

## 5. Schema

```json
"decision_produccion": {
  "decision": "REUSE | ADAPT | REFRESH | CREATE",
  "activo_referencia": "string | null",
  "racional": "string (2-3 frases: que sostiene esta decision)",
  "matiz_por_soporte": "string | null",
  "modo": "con_dato | cualitativo",
  "evidencia_rendimiento": {
    "metrica": "CTR | leads | CPL | VTR | clics | interaccion",
    "valor": "string",
    "creatividad": "string (codigo de la pieza en el informe)",
    "semana": "YYYY-MM-DD"
  },
  "necesita_validacion_inventario": false,
  "procedencia": {
    "nivel": "propuesta",
    "fuente": "Recomendacion Maia Copywriter sobre informe semanal del <fecha>",
    "validacion": "no_confirmado"
  }
}
```

Reglas del schema:

- `activo_referencia` nombra el activo, código o campaña que se reutiliza, con el nombre que usa el equipo de Movistar. Es `null` solo cuando la decisión es CREATE.
- `modo` declara en cuál de los dos modos de la sección 3 se tomó la decisión. Es obligatorio y el Maia Campaign Manager lo audita.
- `evidencia_rendimiento` solo existe cuando `modo` es `con_dato`. Es `null` en modo cualitativo, y en ese caso la `fuente` no menciona ningún informe.
- `necesita_validacion_inventario` es `false` en modo con dato y `true` en modo cualitativo.
- `procedencia` es siempre `nivel: propuesta` y `validacion: no_confirmado`, haya dato o no. El dato respalda la recomendación; no la aprueba. Solo un gate humano promociona.
- Las métricas admitidas en `evidencia_rendimiento.metrica` son exactamente estas seis: CTR, leads, CPL, VTR, clics, interaccion. Ninguna otra.

---

## 6. Cómo lo usa cada agente

**Maia Copywriter.** Emite la decisión por territorio antes de escribir la orientación de comunicación. La decisión condiciona la orientación: un territorio en REUSE no necesita "por dónde explorar", necesita decir qué activo se reactiva y qué se ajusta.

**Maia Campaign Manager.** Verifica que todo territorio lleva decisión con su `modo` declarado, que las de modo cualitativo no se presentan como basadas en datos, que las de modo con dato traen `evidencia_rendimiento` completa y con métrica de respuesta (nunca impactos ni ventas), y cuenta cuántas siguen con `necesita_validacion_inventario: true` para el resumen de cierre.

**Maia Storyteller.** Renderiza el principio de eficiencia creativa arriba de la sección de orientación, y la decisión por territorio en la sección de producción, agrupada por tipo de decisión para que el comité vea de un vistazo cuánto trabajo nuevo hay. Cuando una decisión viene en modo con dato, muestra la evidencia junto a ella en una línea. El aviso de estado de la sección se adapta a la cobertura real: no se dice que no hay datos si los hay para parte de los territorios.

---

## 7. Dependencia pendiente

Esta skill opera hoy en modo mixto: con dato para los territorios que tuvieron actividad medida el mes anterior, cualitativo para el resto.

Faltan dos cosas para cerrarla del todo:

1. **El inventario de activos vivos.** Códigos de campaña, territorios construidos, piezas y formatos en uso, estén o no emitiéndose. Lo tiene que aportar el cliente; no se puede reconstruir desde los outputs de MAIA ni desde los informes semanales.
2. **Los datos de rendimiento en tabla.** Hoy llegan como imágenes dentro de un email, que un agente puede leer una vez pero que no construye serie histórica. Con tabla, en tres o cuatro meses habría una serie por activo.

Es una petición al cliente y a su equipo de Analítica de Comunicación, no un desarrollo.
