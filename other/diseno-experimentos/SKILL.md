---
name: diseno-experimentos
description: Úsalo al definir el holdout de una campaña, al formular su hipótesis, y al interpretar resultados de lift (get_campaign_results).
---

# Diseño y lectura de experimentos (holdout / lift)

En FinZen cada broadcast se mide contra un grupo de control (holdout): usuarios
del segmento que NO reciben el mensaje. El **lift** = tasa de transacción de
expuestos − tasa del holdout, en puntos porcentuales. Es la única medida causal
que tenemos — protégela.

## 1. Toda campaña lleva hipótesis

Formato (antes de proponer, inclúyela en el rationale):

> "Como [observación con datos de los tools], creemos que [este mensaje a este
> segmento] producirá [resultado esperado]. Lo sabremos si [lift en X a 7 días]."

Si no puedes llenar la observación con datos reales, no tienes campaña — tienes
una corazonada. Vuelve a `get_kpis` / `get_campaign_results`.

## 2. Elegir el holdout según el tamaño del segmento

Regla de FinZen (ya validada en campañas anteriores):

| Tamaño del segmento (count real) | Holdout | Por qué |
|---|---|---|
| ≥ 300 usuarios | 10-20% | Deja masa expuesta sin renunciar del todo al control |
| 100-299 | 20% | Por debajo de ~30 el brazo de control deja de existir en la práctica |
| < 100 | **No se propone** | Un holdout de 10 personas no mide nada, y desde el plan de mensajería (26/10/2026) no hay campañas sin control: `propose_campaign` rechaza `holdout_pct: 0`. Dilo y sugiere esperar a que el segmento crezca o usar uno más grande |

> **Esta tabla reparte alcance, NO garantiza poder estadístico.** Se eligió para
> no perder demasiados usuarios expuestos, no para poder detectar un lift chico.
> Un holdout de 30-60 personas produce márgenes de error de dos dígitos: casi
> ningún lift que midas con esos tamaños va a ser distinguible de cero.
>
> Antes de interpretar el resultado, consulta el margen que corresponde al brazo
> más chico en el skill **`lectura-kpis-finzen` §3**. Esa tabla manda sobre
> cualquier intuición de esta sección.
>
> *(Pendiente con Junior, 2026-08-20: dimensionar el holdout por lift mínimo
> detectable en vez de por porcentaje del segmento. Hasta que llegue esa
> respuesta, esta tabla se usa para elegir el reparto y la de él para decidir si
> el resultado se puede leer.)*

- El default del API es 10%. Ajústalo con `holdout_pct` en `propose_campaign`
  según esta tabla y di en el rationale cuál elegiste y por qué. **Nunca 0**: la
  tool lo rechaza.
- La métrica y la ventana las fija el **objetivo** del mensaje (tabla en
  `campanas-retencion` §4): un mensaje de hábito se lee en 8 semanas, uno de
  monetización por pruebas iniciadas o pagos, no por transacción a 7 días.
- Nunca prometas "significancia estadística" con segmentos chicos: sé honesto
  — "con este tamaño la lectura será direccional, no concluyente".
- **Di el margen esperado ANTES de lanzar**, no después de ver el resultado. Si
  el lift que esperas es más chico que el margen del holdout, la campaña no se
  va a poder evaluar: eso hay que decirlo al proponerla, no al reportarla.

## 3. Un cambio por experimento

Si quieres probar mensaje A vs B, son **dos campañas separadas al mismo tipo de
segmento en momentos distintos**, no una campaña con dos ideas mezcladas. Si la
campaña cambia segmento Y mensaje Y superficie a la vez respecto a la anterior,
no sabrás qué causó la diferencia — dilo al proponer.

## 4. Leer resultados (get_campaign_results) sin engañarse

- **Usa la `lectura` calculada de cada campaña** (detalle en `lectura-experimentos`
  §1 bis): `no_medible_entrega`, `ventana_abierta` y `sin_control` no se leen;
  el efecto se reporta como usuarios incrementales ± margen real.
- **Espera la ventana completa (7 días)** antes de declarar éxito o fracaso.
  Un lift a día 2 puede evaporarse.
- **Antes de leer el signo, mira el tamaño del brazo más chico** y busca su
  margen de error en `lectura-kpis-finzen` §3. Si el lift no supera ese margen,
  la lectura correcta es *"sin cambio distinguible de ruido"*, no *"leve
  mejora"* ni *"leve caída"*. Un `lift_pts` positivo con un holdout de 30
  personas no es señal: el margen a ese tamaño es de más de diez puntos.
- Solo cuando el lift supera el margen, repórtalo como "X puntos de lift sobre
  el control", y di igualmente cuál era el margen.
- Lift ~0 o negativo **y por encima del margen** → el mensaje no movió; NO lo
  maquilles. Di qué aprendimos y qué cambiarías (causa, gancho, momento).
- Lift ~0 o negativo **por debajo del margen** → no aprendiste que no funcionó,
  aprendiste que no se pudo medir. Son cosas distintas y hay que decirlas
  distinto.
- Campañas viejas con `holdout_pct: 0` (o enviadas desde el panel sin control)
  → la métrica pre/post es **descriptiva**: puede estar contaminada por
  estacionalidad (quincena, fin de mes). Preséntala siempre con ese disclaimer.
- **No compares lifts entre segmentos distintos** como si fueran la misma vara:
  reactivar dormidos parte de una base más baja que empujar activos.

## 5. Acumular aprendizaje (el playbook)

Cuando un patrón se repita (ej. "los ganchos con dato propio del usuario dan
más lift en dormidos"), dilo explícitamente al socio y sugiérele guardarlo en
el Cerebro (`save_content_draft` con un mini-informe si te lo pide). Los
experimentos valen por lo que se aprende, no por ganar.

---
*Adaptado de `ab-testing` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT).*
