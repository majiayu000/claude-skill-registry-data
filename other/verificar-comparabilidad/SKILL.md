---
name: verificar-comparabilidad
description: Úsalo SIEMPRE antes de presentar un delta, una tendencia o una comparación entre dos periodos de FinZen. Verifica que las dos puntas midan lo mismo. Si entre ellas hay un deploy, un cambio de definición o un cambio de campañas, la comparación no vale y hay que decirlo.
---

# Verificar que dos números se puedan comparar

Un delta correcto entre dos números que miden cosas distintas es peor que no tener el dato: se ve autoritativo y lleva a decidir mal. Este skill es el chequeo obligatorio antes de cualquier "subió", "bajó" o "mejoró".

## 0. Antes de empezar

1. `search_cerebro` con "rupturas de serie FinZen". Trae el registro fechado de rupturas.
2. Identifica la fecha de las dos puntas de tu comparación.
3. **Si hay una ruptura registrada entre las dos fechas, la comparación es inválida hasta que la partas por sub-cohorte.**

Este paso va antes de escribir la frase, no después de escribirla.

## 1. Qué cuenta como ruptura de serie

| Tipo | Ejemplo real de FinZen | Efecto |
|---|---|---|
| Cambio de definición o instrumentación | Fix de cohortes con re-baseline retroactivo | Los históricos cambian de valor |
| Arranque del tracking | ~29-abr-2026: ~680 usuarios previos sin attribution | Toda comparación que cruce esa fecha es inválida |
| Deploy que cambia cómo se mide | 16-jul-2026, H9 en producción: desaparece el onboarding y "Verificados" pasa a ser igual a "Onboarding" por diseño | Métricas de entrada muertas o redefinidas |
| Deploy que cambia el producto | ~11-jul-2026 H10 al 100%; 16-ago-2026 H13 desplegada | Se lee por brazo, no agregado |
| Cambio de composición del tráfico | Campañas apagadas 10-16 ago y reactivadas el 17-ago-2026 | Cohortes de poblaciones distintas |
| Cambio de base de costos | 20-jul-2026, "Marketing (Real)" sustituye a "Marketing fijo $175" | Cash flow y break-even no comparables a través |

El registro completo y fechado vive en el Cerebro. Este skill trae el criterio; el Cerebro trae la lista.

## 2. El árbol de decisión

Para cada delta que vayas a presentar:

1. **¿Las dos puntas miden la misma población?** Cohorte contra cohorte, periodo contra periodo. Nunca cruzados.
2. **¿Las dos puntas tienen la misma madurez?** Un cohorte fresco contra uno maduro no es comparación.
3. **¿Las dos puntas son de la misma familia de ventana?** Rolling contra rolling, calendario contra calendario. **Nunca rolling contra calendario:** son ventanas distintas y dan números diferentes sin que eso signifique nada.
4. **¿Hay una ruptura registrada entre las dos fechas?** Si la hay, marca y parte.
5. **¿La diferencia supera el margen de error del n más chico?** Si no, no es un delta, es ruido. Ver la tabla del skill `lectura-kpis-finzen`.

Si alguna respuesta falla, la salida no es omitir el número: es presentarlo con la marca.

## 3. Cómo se escribe una comparación inválida

Mal:

> La activación cayó de 20.29% a 12.20%.

Bien:

> Activación 12.20% (5 de 41) contra 20.29% (110 de 542) la semana previa. **No comparable como tendencia:** con n=41 el margen es de ±12 puntos y cubre el valor anterior, y además las campañas se apagaron en esta ventana, así que las dos puntas son poblaciones distintas.

La segunda es más larga y es la única que aguanta una auditoría.

## 4. Familias de ventana

| Cadencia | Export canónico | Compara contra |
|---|---|---|
| Semanal | Rolling 7d | 7d anterior, direccional, muestra chica |
| Mensual | Mes calendario | Mes calendario anterior |
| Trimestral | Trimestre calendario | Trimestre anterior |

MAU y otras métricas de ventana móvil difieren entre rolling y calendario por construcción. Eso no es bug y no se reporta como anomalía.

## 5. Qué hacer con una ruptura nueva que descubras

Si detectas un cambio de definición o un deploy que no está en el registro:

1. No lo interpretes. Márcalo.
2. `save_cerebro_note` con la fecha, qué cambió, y qué métricas quedan afectadas.
3. Levántalo como pregunta, no como hallazgo.

Precedente: el 20-jul-2026 una métrica de onboarding inconsistente resultó ser un deploy no comunicado. Preguntar antes de interpretar evitó celebrar como orgánico un lift que no lo era.

## Anti-patrones

- **Presentar un delta porque el tablero ya lo calculó.** El "vs prev" del tablero no sabe de rupturas.
- **Comparar acumulados del mes en curso entre semanas.** Siempre "empeora".
- **Cruzar rolling con calendario** para que el número cuadre con lo que esperabas.
- **Partir por sub-cohorte solo cuando el resultado no gusta.** Si la regla aplica, aplica en las dos direcciones.
- **Omitir el número por no ser comparable.** Se reporta con la marca; omitirlo esconde información.
- **Tratar "no comparable" como conclusión.** Es una descripción del dato, no una respuesta. Di también qué haría falta para poder comparar.

## Formato de entrega

Cada comparación que salga de aquí lleva:

1. Los dos valores **con su n**, nunca los porcentajes solos.
2. Veredicto de comparabilidad: comparable / comparable con reserva / no comparable.
3. Si no es comparable, la razón concreta y fechada.
4. Si es comparable, el delta y si supera el margen de error.

Al cierre, la lista de rupturas que aplicaron a la ventana analizada.
