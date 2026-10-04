---
name: Informe semanal de Publicidad Movistar
key: informe-semanal-publicidad
description: Ingesta y uso del informe semanal de campanas que produce Analitica de Comunicacion de Telefonica. Unica fuente de rendimiento real por campana y por creatividad. Alimenta el criterio de reutilizacion de activos.
version: 1.0.0
owner: comunicacion-movistar
status: active
loaded_by: Maia Strategist, Maia Planner, Maia Copywriter, Maia Campaign Manager
---

# Informe semanal de Publicidad

## 1. Qué es

Un informe que el equipo de **Analítica de Comunicación** (Dirección de Comunicación y Publicidad, Telefónica España) envía cada viernes a los responsables de publicidad. Recoge cómo están rindiendo las campañas que están en el aire.

Es la única fuente de rendimiento real de la que dispone el sistema. Todo lo demás que entra en MAIA es intención: lo que el área quiere hacer, lo que el mercado sugiere, lo que MAIA recomienda. Esto es lo que ha pasado.

Su valor específico, y la razón por la que merece ser un input formal del workflow, es que baja al nivel de **creatividad individual con código propio**: no dice solo "la campaña de Vuelta al Cole funciona", dice qué pieza concreta lidera el tráfico, cuál gana peso en captación y cuál es la más eficiente de toda la campaña, con su CTR, sus leads y su CPL.

---

## 2. Entrada

### 2.1 Cuándo

El informe es **semanal**, el ciclo de MAIA es **mensual**. La regla es: **los informes de las 4 semanas del mes anterior se adjuntan juntos al ticket, al inicio del run**, con el PPT del área y los trend flashes.

No se ingieren de uno en uno ni fuera de ciclo. La variación semana a semana es parte de la señal (una campaña que sube 3 semanas y cae la cuarta cuenta algo distinto que una que cae siempre), así que el bloque de 4 se lee como una serie, no como cuatro fotos sueltas.

### 2.2 Formato

**Formato recomendado: PDF.** El informe llega como email con el contenido en imágenes embebidas. Los datos por creatividad, las comparativas de eficiencia y los key visuals viven en esas imágenes, no en el texto del cuerpo. Un PDF impreso desde el cliente de correo preserva ambas cosas y el agente lo lee directamente con su capacidad multimodal, igual que hace con los trend flashes.

**Formato alternativo: `.eml`.** Aceptable, pero el agente debe extraer las imágenes del MIME antes de leerlas. Si solo procesa el texto del cuerpo, pierde la parte más valiosa del informe y debe registrarlo como flag, no continuar en silencio.

Nunca se transcribe el informe a mano a un documento intermedio: se pierde el detalle y se introduce error de copia.

### 2.3 Naming y almacenamiento

Los informes se guardan en `Inputs/informes-semanales/YYYY-MM/`, con el patrón `YYYY_MM_DD_informe_semanal_publicidad.pdf` (la fecha es la del envío, viernes).

El almacenamiento es para tener histórico. **El input operativo del run son los archivos adjuntos al ticket**, no la carpeta.

### 2.4 No es bloqueante

Si faltan informes, el agente **continúa**. No se detiene la cadena ni se pide iteración por esto.

Pero la ausencia no es neutra: **degrada lo que el sistema puede afirmar**. El **Maia Strategist** es el único agente que lee los informes, y registra la cobertura en el brief para que los demás sepan con qué confianza trabajan:

```json
"cobertura_informes": {
  "semanas_esperadas": 4,
  "semanas_disponibles": 3,
  "semanas_faltantes": ["2026-08-28"],
  "nivel_confianza": "alto|medio|bajo"
}
```

- **4 de 4**: confianza alta. Las conclusiones de rendimiento pueden sostenerse.
- **2 o 3 de 4**: confianza media. Las conclusiones se emiten con la salvedad de la cobertura parcial.
- **1 de 4 o ninguno**: confianza baja. **Ninguna decisión puede presentarse como basada en datos**, y se vuelve al modo cualitativo de `eficiencia-creativa-movistar`.

Con ningún informe disponible, se registra flag de severidad baja y el run continúa exactamente como antes de existir esta skill.

---

## 3. Qué contiene

La estructura varía de semana a semana, pero el informe se organiza por campaña activa y para cada una cubre estos bloques:

| Bloque | Contenido típico |
|---|---|
| Evolución | Impactos acumulados y por persona, variación vs. semana anterior (S-1), reparto por soporte |
| Tráfico | Sesiones totales y variación, fuentes (Orgánico, BTL, Directo, de pago) y cuál tracciona |
| Estrategia de medios | Rendimiento por bloque (Display, Social, Vídeo) con CTR, leads, CPL y variación |
| **Detalle por creatividad** | Piezas individuales con su código, qué hace cada una y sus métricas de respuesta |
| Comparativas | Cuando conviven dos estrategias (dos terminales, dos ofertas), comparación directa en CTR, impresiones y VTR |
| Ventas | Unidades o altas, variación vs. S-1 y vs. año anterior (A-1) |

El bloque de **detalle por creatividad** es el que aporta lo que el sistema no tenía. Ejemplo real (semana del 11/09/2026, campaña Vuelta al Cole, bloque display):

> `FUTBOL26-BASE` lidera el tráfico con 154K clics y 0,73% de CTR. `BASE` gana peso en captación con 336 leads, +22% vs. S-1. `Fibra Adicional / FA-FOTO` lidera la conversión con 1.494 leads y es la más eficiente de toda la campaña. `FIBRA300-AMARILLO` mejora eficiencia y volumen con 324 leads a 9,23 € de CPL. `MAX-A` mejora su CPL a 8,07 €, un 14% menos que la semana anterior.

Ahí hay cinco activos identificados por código con su rendimiento medido. Eso es materia prima directa para decidir qué se reutiliza.

---

## 4. Qué métrica sirve para qué (CRÍTICO)

No todas las métricas del informe tienen el mismo valor probatorio, y confundirlas reintroduce exactamente el problema que el sistema intenta resolver: presentar una inferencia con autoridad de dato.

### 4.1 Métricas de respuesta de la pieza: SÍ deciden sobre el activo

CTR, leads, CPL, VTR, clics, interacción. Miden cómo responde la gente **a esa creatividad concreta**. Son atribuibles a la pieza porque la pieza es lo que el usuario vio antes de actuar.

Estas son las que sostienen una decisión REUSE / ADAPT / REFRESH / CREATE sobre un activo.

### 4.2 Métricas de cobertura: describen el plan, no la pieza

Impactos, impresiones, frecuencia, reparto por soporte, sesiones totales. Dicen cuánto se ha invertido y dónde, no si la creatividad funciona. Un activo con muchos impactos no es un activo que funcione: es un activo con presupuesto.

Sirven al Planner para calibrar presión y mix. **No sirven para juzgar una creatividad.**

### 4.3 Ventas: NO son atribución

Las ventas que reporta el informe son ventas del periodo, no ventas causadas por la campaña. El propio informe lo reconoce cuando explica una caída del 10% "en un contexto de menor intensidad futbolística": la variable que mueve la venta es el calendario deportivo, no la creatividad.

**Prohibido derivar una decisión sobre un activo creativo a partir de las ventas.** Una campaña puede vender menos con la mejor creatividad posible, y al revés.

Las ventas entran en el sistema como contexto de negocio, con su procedencia, y nada más.

### 4.4 Los juicios ya redactados del informe

El informe incluye conclusiones escritas por el equipo de Analítica ("Samsung rinde mejor en eficiencia de respuesta y Pixel en alcance", "FA-FOTO: más eficiente de toda la campaña"). Son valiosas y **se citan tal cual**, atribuidas a su fuente.

No se reinterpretan ni se convierten en una conclusión propia de MAIA. Si MAIA deriva algo distinto de los mismos números, esa lectura es `propuesta`, separada de la del informe.

---

## 5. Procedencia

Todo lo que salga de este informe es **`insight_estrategia`**, nunca `plan_area`.

La razón: `plan_area` significa "lo declara el plan comercial del área". El informe lo produce Analítica de Comunicación, no el área comercial, y no forma parte del plan. Es un dato objetivo del cliente que MAIA incorpora desde fuera del plan, que es exactamente la definición de `insight_estrategia` en la sección 7 de `contexto-sistema-maia`.

```json
"procedencia": {
  "nivel": "insight_estrategia",
  "fuente": "Informe semanal Publicidad, Analitica Comunicacion Telefonica, semana del 11/09/2026",
  "validacion": "confirmado"
}
```

La `fuente` **siempre nombra la semana concreta**. Un dato de rendimiento sin fecha no es verificable y envejece rápido.

Cuando una afirmación se apoya en varias semanas, la fuente las nombra: "semanas del 21/08 al 11/09".

---

## 6. Cómo lo usa cada agente

**Regla de circulación del dato.** Solo el Maia Strategist recibe y lee los informes. Los demás agentes **no los reciben**: leen lo que el Strategist extrajo y volcó en el Golden Briefing, en los campos `cobertura_informes` y `rendimiento_periodo_anterior`. Si el dato no está en el brief, para el resto de la cadena no existe.

### 6.1 Maia Strategist

Lo lee en el Paso 0d, junto a los trend flashes, y hace dos cosas.

**Extrae y vuelca.** Es su responsabilidad principal respecto a esta skill, y sin ella todo lo demás es inútil. Rellena `rendimiento_periodo_anterior` con sus tres listas: `por_creatividad` (piezas con código y métricas de respuesta), `por_campana` (reparto de soportes y tracción) y `contexto_negocio` (ventas con su salvedad). Mapea cada creatividad al territorio de MAIA correspondiente en `territorio_asociado`.

**Enriquece su propia lectura.** Los datos del mes anterior alimentan la lectura ejecutiva, marcados como `insight_estrategia`.

Sobre el criterio C12 de la rúbrica (aprendizajes anteriores): el criterio mide lo que aporta **el área en su documento**, no lo que aportan los informes. Un brief que no trae aprendizajes sigue puntuando AUSENTE; lo que cambia es que el Strategist puede rellenar el hueco en la lectura ejecutiva y señalar en el formulario que esa información existía y el área no la usó.

### 6.2 Maia Planner

Lee `rendimiento_periodo_anterior.por_campana` del brief. Es donde más cambia una decisión concreta: hoy reparte presión y prioriza canales con criterio de manual, y el campo le da el reparto real de soportes y la tracción de tráfico del mes anterior.

Todo lo que derive de ahí sigue siendo **`propuesta`** en cuanto a la recomendación, con el dato citado como `insight_estrategia` en el racional. La recomendación es de MAIA aunque el dato sea de Analítica.

El Planner **sí puede** usar impactos, impresiones y frecuencia: para calibrar presión y mix son exactamente las métricas correctas. La prohibición de la sección 4.2 es sobre juzgar creatividades, no sobre planificar.

### 6.3 Maia Copywriter

Lee `rendimiento_periodo_anterior.por_creatividad` del brief. Es quien desbloquea el criterio de reutilización. Para cada territorio, antes de emitir su `decision_produccion`, comprueba si hay entrada con `territorio_asociado` igual a ese territorio.

Decide el modo así:

- `cobertura_informes.nivel_confianza` es `bajo`: **todas** las decisiones del ciclo van en `modo: cualitativo`, sin excepción. Con un informe de cuatro no hay serie.
- Confianza alta o media y hay entrada para el territorio: `modo: con_dato`, con `evidencia_rendimiento` completa.
- Confianza alta o media pero el territorio no tiene entrada: `modo: cualitativo`. Que haya datos del mes no significa que los haya de este territorio.

**Cuando una creatividad trae varias métricas**, el Maia Strategist ya eligió una como `metrica_principal` y dejó el resto en `metricas_secundarias`. Copia la principal en `evidencia_rendimiento`. Puedes usar una secundaria si sostiene mejor tu decisión, pero solo una: `evidencia_rendimiento` admite una métrica, no una lista. El orden de preferencia que usa el Strategist es: la que el propio informe destaca en su lectura, luego leads, CPL, CTR, VTR, y por último clics o interacción. La más pertinente, no la más favorable.

En los dos modos la procedencia de la decisión es `nivel: propuesta` y `validacion: no_confirmado`. Ver `eficiencia-creativa-movistar` sección 3.

### 6.4 Maia Campaign Manager

No consume el informe ni el campo directamente. Lo usa como referencia para auditar el criterio V23: que toda decisión en modo con dato traiga una métrica de respuesta y no una de cobertura o de ventas, que ninguna esté en modo con dato si la cobertura es baja, y que si hay semanas disponibles el brief no traiga `rendimiento_periodo_anterior` vacío.

---

## 7. Qué NO hace esta skill

- **No sustituye al inventario de activos.** El informe cubre las campañas que estuvieron en el aire en el periodo. Un activo que existe pero no se emitió el mes pasado no aparece, y sobre él no hay dato. El inventario completo sigue pendiente del cliente.
- **No construye serie histórica.** Cada run lee los informes de su mes. El sistema no acumula ni compara contra meses anteriores, porque un email no es una base de datos. Cuando exista el dato en tabla, esta limitación desaparece.
- **No mide marca.** El informe es de respuesta y negocio. No dice nada sobre notoriedad, atribución de marca ni percepción, así que no se puede usar para juzgar territorios de construcción de marca.
- **No evalúa el trabajo de las agencias.** Para eso están los principios de comunicación de `matriz-soportes-movistar`.

---

## 8. Dependencia pendiente

Lo que de verdad convertiría esto en el criterio basado en datos que pide el cliente es recibir los mismos números **en tabla**, no en imágenes dentro de un email. Con tabla, en tres o cuatro meses el sistema tendría una serie por activo y la decisión de reutilización dejaría de ser propuesta.

Es una petición al equipo de Analítica de Comunicación, no un desarrollo. Mientras tanto, esta skill opera con la lectura multimodal del PDF, que funciona pero no acumula.
