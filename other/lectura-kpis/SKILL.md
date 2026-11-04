---
name: lectura-kpis
description: Úsalo antes de resumir la semana, leer get_kpis, evaluar un segmento o proponer una campaña a partir de números. Convierte cifras en señal esquivando las trampas de medición conocidas de FinZen (madurez de ventana, rupturas de serie, familias de export).
---

# Lectura de KPIs: de cifra a señal

Un número solo es señal cuando sobrevive tres preguntas: ¿mide lo mismo que su punto de comparación?, ¿ya maduró?, ¿lo explica algo externo? Este skill es el orden de lectura que evita recomendar sobre ruido.

## 0. Antes de empezar

1. `search_cerebro("rupturas de serie")` y `search_cerebro("definiciones de métricas")` — sin esto no se compara nada.
2. `get_kpis` del periodo actual Y de los 4 periodos previos (la referencia es la mediana, no solo la semana pasada).
3. Si la lectura alimenta una campaña: `list_segments` después de leer, nunca antes.

## 1. Orden de lectura (siempre el mismo)

1. **Contexto**: ¿qué cambió afuera en la ventana? (deploy, campaña encendida/apagada, promo, experimento nuevo). Si algo cambió, toda la lectura se hace a la luz de eso.
2. **Sanidad**: pasar el skill `sanidad-datos` si algo se movió >20% o hay cifras en conflicto.
3. **Funnel primero, pulso después**: las métricas de decisión (activación, retención, conversión) se leen antes que las de volumen (registros, MAU, views). El pulso contextualiza; no decide.
4. **Señal**: solo lo que sobrevivió 1-3 califica para recomendación.

## 2. Tabla de comparación válida

| Situación | Acción |
|---|---|
| El periodo cruza una ruptura de serie registrada | Partir la comparación en la ruptura o marcar "no comparable" |
| Ventana rolling vs mes calendario | Nunca cruzar familias: rolling contra rolling, calendario contra calendario |
| Métrica con ventana abierta (cohorte reciente) | Marcar "inmaduro": el rolling subestima lo último. Comparar semanales entre sí vale (mismo sesgo); comparar contra umbral absoluto no |
| Delta semanal con n bajo | Lectura direccional con disclaimer, nunca veredicto |
| Cambio vs periodo previo <20% y dentro del rango de 4 periodos | Ruido probable: reportar sin recomendación atada |
| Desviación >20% vs la mediana de 4 periodos | Anomalía: investigar causa ANTES de recomendar (skill `sanidad-datos`) |

## 3. Reglas de detalle que ya costaron errores

- **Conteos, no porcentajes redondeados.** Un panel que muestra "8%" puede ser 7.51% (32/426) y la diferencia caer justo sobre la frontera de decisión. Pedir siempre numerador y denominador.
- **Cohortes por semana de registro.** Nunca mezclar cohortes con stock acumulado ("activos" es un stock; el funnel de cohorte no suma con métricas de periodo).
- **En tablas de cohortes, ignorar la primera fila (recortada por la ventana) y la última (inmadura).**
- **Un embudo donde un paso posterior supera al anterior** (activados > D1) es denominador mezclado, no milagro: marcar defecto de instrumentación, no leer.
- **Antes de interpretar cualquier salto: buscar experimento activo en el Cerebro.** El error clásico fue celebrar como orgánico un lift que era un deploy no comunicado.

## 4. Ejemplo bueno y malo (datos FinZen reales)

- **Malo:** el semanal del 27-jul reportó D1 de la cohorte 20-jul en 15.17% (64). Días después la misma cohorte marcó 24.88% (106). Quien recomendó sobre el 15.17% recomendó sobre una ventana sin madurar.
- **Bueno:** la semana 10-16 ago dio activación 12.20% vs 20.29% previa. Antes de declarar caída se verificó el intervalo (Wilson IC95 [5.3, 25.5] cubre 20.29) y el contexto (campañas apagadas = población distinta). Veredicto: "no comparable, línea base orgánica nueva", no "colapso".

## Anti-patrones

- Comparar contra la semana previa a secas, sin la mediana de 4 periodos.
- Emitir recomendación en el mismo párrafo donde se declara una anomalía sin causa.
- Tratar "sin dato" como cero.
- Citar un porcentaje de panel sin su numerador/denominador.
- Interpretar una métrica nueva o redefinida sin registrar que hubo redefinición.

## Formato de entrega

Señal por señal: **métrica → valor (conteo) → comparación válida usada → lectura de una línea → confianza (alta/media/baja)**. Máximo 3 recomendaciones, cada una atada a la métrica que la validará el periodo siguiente. Si un dato clave quedó "no comparable" o "inmaduro", decirlo en el resumen, no en nota al pie.
