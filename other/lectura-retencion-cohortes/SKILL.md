---
name: lectura-retencion-cohortes
description: Úsalo cuando vayas a interpretar retención de FinZen (D1, D7, D30, cohortes, racha, TX por usuario) o cuando alguien afirme que la retención mejoró o empeoró. La métrica que gobierna en FinZen no es D1 ni D7 por separado, sino la sobrevida entre las dos.
---

# Leer retención y cohortes en FinZen

FinZen tiene un problema de retención bien localizado y una serie de lecturas equivocadas en su historia porque se miraron D1 y D7 como métricas independientes. Este skill fija dónde mirar y qué descartar.

## 0. Antes de empezar

1. `get_kpis` con la ventana pedida.
2. `search_cerebro` con "sobrevida D1 D7 FinZen" para traer la serie histórica.
3. `search_cerebro` con "experimentos activos FinZen" **antes** de explicar cualquier movimiento. Si hay un experimento vivo, la lectura es por brazo y no agregada.

> ### Lo que este skill NO puede ejecutar hoy (2026-08-20)
>
> `get_kpis` devuelve `engagement.retention_d1_pct`, `retention_d7_pct` y
> `retention_d30_pct`: **tres números agregados del periodo, sin dimensión de
> cohorte.** La Agent API no expone retención por cohorte de semana de registro.
>
> En consecuencia, con las tools de hoy **no puedes**: calcular la sobrevida
> D1→D7 de un cohorte (§1), evaluar madurez de ventana de un cohorte concreto
> (§2), ni separar cohorte orgánico de pagado (§4).
>
> Lo que sí puedes hacer: reportar los tres agregados con su marca de
> comparabilidad, y traer del Cerebro la serie de sobrevida ya calculada por un
> humano (paso 2 de arriba) citándola como dato histórico, **nunca como cálculo
> propio del periodo actual**.
>
> Si te piden la sobrevida del periodo, la respuesta correcta es que la Agent
> API no la expone todavía — no la estimes a partir de los agregados: D1 y D7
> del periodo son poblaciones distintas y su cociente no es una sobrevida.

## 1. El hallazgo que gobierna

Entre mayo y julio de 2026, D1 subió de 14-16% a 22-26% mientras D7 se quedó plano en 8-11%. La sobrevida D1 a D7 (qué fracción de los que volvieron el día 1 seguía viva el día 7) cayó de forma monótona:

`64% → 62% → 50% → 43% → 42% → 37% → 30%`

**El producto no retiene mejor: pierde más tarde.** La fuga estructural está en el tramo D1 a D7.

**Regla:** cuando reportes retención, reporta siempre la sobrevida D1→D7, no solo los dos extremos. Un D1 que sube con D7 plano es una señal de deterioro, no de mejora, y el tablero lo presenta como si fuera lo contrario.

## 2. Madurez de ventana: qué NO se puede leer

El export rolling de 7 días se genera el día que cierra la ventana.

- El cohorte registrado el último día no tuvo tiempo de llegar a D1.
- Ningún cohorte registrado dentro de la ventana llegó a D7, salvo el del primer día.
- La tabla de cohortes solo trae las semanas registradas dentro de la ventana; el resto aparece en guiones.

**Prueba de que el efecto es grande:** el 27-jul-2026 el cohorte del 20-jul leía D1 15.17% (64 usuarios). Días después, el mismo cohorte leía **24.88% (106)**. La diferencia no fue una mejora del producto: fue maduración.

**Reglas duras:**

- Nunca leas D7 ni D30 de un cohorte registrado dentro de la misma ventana. Si el valor es 0.00%, la lectura correcta es "inmaduro por construcción", no "cero retención".
- Nunca compares un cohorte fresco contra uno maduro. Es la comparación más engañosa disponible en este tablero.
- Para cohortes maduros usa la ventana de 90 días, no la de 7.

## 3. Bandas de referencia

| Métrica | Banda vigente | Meta | Nota |
|---|---|---|---|
| D1 | 19-26% | sin meta fijada | Subió sin que D7 la siguiera |
| D7 | 8-11% | sin meta fijada | **Plano desde mayo 2026.** Es el guardrail de varios experimentos |
| D30 | 2.5-5% | 10% | Cae por debajo de la meta de forma sostenida |
| Sobrevida D1→D7 | 30-45% | recuperar 60%+ | La métrica que importa |
| Racha de hábito | 43-60% | sin meta | Lee sobre usuarios activos, base variable |
| TX / usuario activo | 5.3-6.8 | sin meta | Máximo de la serie: 6.77 (semana orgánica) |

Antes de usar cualquiera de estas bandas, confirma con `search_cerebro` que siguen vigentes.

## 4. Composición del cohorte: orgánico contra pagado

Verificado en la semana del 10-17 ago 2026, la única sin campañas de toda la serie: con tráfico pagado apagado, TX por usuario activo subió a 6.77, el máximo histórico, sobre 70 usuarios activos contra 155 la semana anterior.

**El cohorte orgánico y el pagado no se comportan igual.** Consecuencia práctica: si la retención se mueve en una ventana donde cambió la mezcla de tráfico, no puedes atribuir el movimiento al producto.

**Línea base orgánica congelada (10-17 ago 2026):** 5.9 registros/día, 12.20% de activación, 6.77 TX por usuario activo, 70 activos. Es la única medición limpia que existe.

## 5. Cuando hay un experimento vivo

Si `search_cerebro` devuelve un experimento activo que toca retención:

- **Se lee brazo contra brazo, nunca contra la serie histórica.** La comparación no concurrente se contamina con el cambio de mezcla de tráfico; la concurrente no, porque la aleatorización reparte la mezcla por igual entre los dos brazos.
- No hagas peeking. Si el diseño fijó una fecha de corte, respétala.
- La población del experimento es la del punto de asignación. Si asigna en la primera transacción, el denominador son los **activados**, no los registrados, y eso cambia por completo cuánto tarda en alcanzar poder.

## Anti-patrones

- **Celebrar un D1 que sube.** Sin mirar la sobrevida, es probable que sea una fuga que se movió de lugar.
- **Leer D7 = 0.00% como catástrofe.** En una ventana de 7 días es el valor esperado.
- **Comparar racha de hábito entre semanas con bases muy distintas.** 60% sobre 155 activos y 54% sobre 70 no son comparables.
- **Explicar un movimiento de retención sin chequear experimentos.** Pasó el 6-jul-2026 y produjo una lectura falsa.
- **Usar la ventana de 7 días para curvas de cohorte.** Para eso está la de 90.
- **Comparar contra la banda histórica cuando existe un brazo control.** El control es la referencia limpia; la historia no.

## Formato de entrega

1. D1, D7, D30 con su n, y cada uno marcado como maduro o inmaduro.
2. **Sobrevida D1→D7 con la serie de las últimas semanas.** Es el titular.
3. Composición del cohorte: hubo campañas en la ventana, sí o no.
4. Si hay experimento vivo: resultado por brazo, nunca agregado.
5. Qué no se pudo leer y por qué. Esa lista es parte del entregable, no una disculpa.
