---
name: lectura-kpis-finzen
description: Úsalo cuando vayas a interpretar cualquier KPI agregado de FinZen (activación, MRR, churn, burn, break-even, DAU/MAU) antes de recomendar o proponer algo. Los KPIs de este tablero tienen trampas conocidas y varios significan algo distinto de lo que su nombre sugiere. Para los KPIs de redes sociales (Instagram, TikTok), el skill es lectura-kpis-social.
---

# Leer los KPIs de FinZen sin caer en las trampas del tablero

Casi todos los errores de lectura documentados en FinZen vinieron de tomar un KPI por su nombre. Este skill lista las trampas verificadas y da la regla de decisión para cada una. El resultado esperado es una lectura que se sostenga cuando alguien la audite dos semanas después.

## 0. Antes de empezar

Siempre, en este orden:

1. `get_kpis` para el periodo en cuestión.
2. `search_cerebro` con "rupturas de serie FinZen" antes de comparar dos periodos. Si hay una ruptura entre las dos puntas, la comparación no es válida (ver skill `verificar-comparabilidad`).
3. `search_cerebro` con "glosario métricas FinZen" si el KPI no está en la tabla de abajo.

Nunca interpretes un salto o una caída sin antes preguntarte si hubo un deploy, un experimento o un cambio de campaña en la ventana. Si lo hubo y no puedes separarlo, dilo en vez de explicarlo.

## 1. Las seis trampas verificadas

| Trampa | Qué parece | Qué es | Regla |
|---|---|---|---|
| **Churn Rate 0%** | Nadie se fue | "Cancelaciones (30d)" solo cuenta a quien pagó hace 30-60 días y NO en los últimos 30. Cualquier salida fuera de ese patrón es invisible. Falló 3 veces seguidas en jul-ago 2026 | Nunca uses Churn Rate para detectar pérdidas. Usa el delta de **Total Suscripciones** semana contra semana y el delta de **MRR** |
| **Gastos, Burn y Cobertura** | Subió el gasto | Son **acumulados del mes en curso**: crecen solos según avanza el mes | Prohibido compararlos semana contra semana. Solo mes cerrado contra mes cerrado |
| **Ventana rolling de 7d** | La activación bajó | El export se genera el día que cierra la ventana, así que el cohorte más reciente todavía no maduró | Nunca leas D7 ni D30 de un cohorte registrado dentro de la propia ventana |
| **"Activados"** | Activados del periodo | No tiene ventana de 7 días asociada; no es lo mismo que la activación del cohorte del funnel | Usa el funnel del cohorte para la tasa, no el panel de periodo |
| **Break-even (N suscriptores)** | Una meta | Se recalcula cada vez que cambia el gasto. Pasó de 82 a 37 a 36 en seis semanas sin que mejorara nada | Trátalo como espejo del gasto, no como meta. Si baja, primero revisa si bajó el costo |
| **DAU/MAU** | Stickiness | Con campañas activas el MAU se llena de registros que nunca volvieron | No lo leas en ventanas con campañas encendidas o recién apagadas |

## 2. Cohorte contra periodo: la confusión más cara

El tablero mezcla dos poblaciones y les pone nombres parecidos:

- **Cohorte:** usuarios registrados DENTRO de la ventana. Es lo que muestra el funnel.
- **Periodo:** todo lo que ocurrió en la ventana, incluyendo usuarios de la base previa.

Ejemplo real (10-17 ago 2026): el funnel decía "Trial 1 (2.44%)" y el panel decía "Trials Iniciados 3". No es contradicción: 1 del cohorte nuevo, 2 de la base previa.

**Regla:** cuando dos números que deberían coincidir no coinciden, antes de reportar una anomalía verifica si uno es de cohorte y el otro de periodo.

## 3. n chico: cuándo un número NO se puede leer

FinZen opera con cohortes semanales de 40 a 500 registros. A esos tamaños casi ningún movimiento es señal. Kaizen no ejecuta código, así que usa esta tabla en vez de calcular.

**Intervalo de confianza al 95% de una tasa observada:**

| n del cohorte | Margen aproximado |
|---|---|
| 20 | ±17 puntos |
| 40 | ±12 puntos |
| 75 | ±9 puntos |
| 100 | ±8 puntos |
| 200 | ±5.5 puntos |
| 400 | ±4 puntos |
| 800 | ±3 puntos |

**Cómo se usa:** si el cohorte tiene 41 registros y la activación dio 12.2%, el rango real va de 5% a 25%. Una lectura anterior de 20.3% cae dentro. **No bajó nada.**

**Regla dura:** antes de decir que una tasa subió o bajó, verifica que la diferencia supere el margen de la tabla. Si no lo supera, la frase correcta es "sin cambio distinguible de ruido", no "leve caída".

## 4. Qué reportar cuando el número no se puede leer

No lo omitas y no lo suavices. Repórtalo así:

> Activación 12.20% (5 de 41). Margen ±12 puntos: no distinguible del 20.29% de la semana anterior.

## Anti-patrones

- **Explicar un movimiento sin verificar si hubo deploy o campaña.** El 6-jul-2026 se reportó "onboarding y activación subieron" y era el efecto mecánico de un experimento corriendo 50/50.
- **Usar Churn Rate como señal de retención de pago.** Está roto por definición, no por bug.
- **Comparar Burn o Cobertura entre dos semanas.** Siempre da "empeoró" porque el mes avanza.
- **Redondear un intervalo a un titular.** "La activación cayó 8 puntos" con n=41 es falso aunque los números sean correctos.
- **Celebrar que bajó el break-even.** Casi siempre significa que se recortó gasto, no que se vendió más.
- **Inventar el valor de un KPI que `get_kpis` no devolvió.** Si no está, dilo.

## Formato de entrega

Para cada KPI que reportes:

1. Valor y base (`12.20% (5 de 41)`), nunca el porcentaje solo.
2. Comparación contra el periodo equivalente, **o** la razón por la que no es comparable.
3. Nivel de confianza cuando la afirmación sea material: alta / moderada / baja / desconocido.
4. Una línea de lectura. Si la lectura es "no se puede leer", esa es la lectura.

Cierra con las trampas que aplicaron en esta ventana, para que quien lea sepa qué se descartó y por qué.
