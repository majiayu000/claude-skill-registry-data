---
name: lectura-adquisicion-finzen
description: Úsalo cuando vayas a evaluar el rendimiento de campañas de FinZen, calcular CAC o ROI, o recomendar dónde poner presupuesto de adquisición. La tabla de fuentes tiene una ambigüedad de atribución sin resolver que invalida cualquier lectura ingenua de ROI.
---

# Leer adquisición y campañas en FinZen

El objetivo no es reportar cuánto tráfico entró, sino responder si el dinero de adquisición produce clientes. En FinZen esa respuesta hoy no se puede dar con certeza, y este skill explica por qué y qué se puede afirmar igual.

## 0. Antes de empezar

1. `get_campaign_results` para las campañas de la ventana.
2. `search_cerebro` con "atribución UTM tienda FinZen" para ver si la ambigüedad del §2 ya se resolvió. **Si sigue abierta, ninguna afirmación de ROI de campaña es defendible.**
3. `get_kpis` para el mismo periodo: necesitas registros y suscripciones para cerrar el embudo.

## 1. Definiciones que no significan lo que parecen

| Campo | Qué NO es | Qué es |
|---|---|---|
| **Leads** | Todos los clics de descarga | Solo clics de descarga de visitantes que **vienen de anuncio pago**. Orgánico y directo no cuentan. Por eso leads puede ser menor que registros; no es bug |
| **Registros** (en tabla de fuentes) | Signups en la app | AnonymousIds únicos que clickearon "Descargar", deduplicados. Es una proxy de atribución, no un registro confirmado |
| **Top Sources** | Datos del periodo | Es **lifetime**: no aplica el filtro de fechas. Muy útil, pero nunca lo compares contra un KPI de ventana |
| **Inversión** | Gasto del periodo | Costo total acumulado cargado a mano por campaña, sin granularidad temporal |

El glosario del tablero dice "todos los clics de descarga" para Leads, lo cual contradice la definición real. Está pendiente de alinear.

## 2. La ambigüedad de atribución: dos mundos, mismo dato

Dato verificado al 17-ago-2026, tabla lifetime: **25 campañas pagadas, $1,269.71 invertidos, 3,741 registros atribuidos, CERO suscripciones.** Las únicas 3 suscripciones atribuidas están en "Directo".

Eso admite dos explicaciones incompatibles:

- **Mundo A:** el tráfico pagado no convierte. Se compra gente sin intención de resolver un problema financiero.
- **Mundo B:** la atribución se rompe en el salto a la tienda. Si el UTM muere cuando el usuario sale al App Store y vuelve con la app instalada, **toda suscripción originada en pago aterriza en "Directo" por construcción**. Y "Directo" es justo donde están las 3.

**El tablero no puede distinguir A de B.** Hasta que exista atribución de instalación (install referrer de Google Play, deferred deep link, o equivalente iOS), toda lectura de ROI de campaña es especulación.

**Regla:** puedes reportar el dato crudo. No puedes concluir de él que las campañas funcionan ni que no funcionan. Si te piden la conclusión, entrega la pregunta pendiente en su lugar.

## 3. Lo que sí se sostiene sin resolver la ambigüedad

La prueba de la restricción vinculante no depende de la atribución, porque compara el embudo consigo mismo:

| Ventana | Registros del cohorte | Pagos del cohorte |
|---|---|---|
| 3-10 ago 2026 | 478 | 0 (0.00%) |
| 10-17 ago 2026 | 41 | 0 (0.00%) |

Multiplicar el tope del embudo por doce no movió la base ni una unidad. **La restricción está aguas abajo del registro, no en el tráfico.** Esa afirmación es defendible con confianza alta y no necesita atribución.

**Test general que puedes reutilizar:** si el volumen de entrada cambia en un orden de magnitud y la conversión final no se mueve en absoluto, el cuello no está en la entrada. Comprar más tope no puede mover la base.

## 4. Cómo calcular CAC sin engañarte

Reporta siempre las tres, en este orden, y nunca solo la primera:

1. **Costo por registro atribuido** = inversión / registros atribuidos. Es la más barata y la menos informativa.
2. **Costo por activado** = inversión / usuarios del cohorte con primera transacción.
3. **Costo por suscripción nueva** = inversión / suscripciones nuevas. **Si el denominador es 0, escribe "sin suscripciones atribuidas", nunca "N/A" ni un guion.**

Referencia de julio 2026: $0.22 por registro, $1.07 por activado, **$142.88 por suscripción**, equivalente a 14.8 meses de ARPU para recuperar. Ese contraste entre la primera y la tercera cifra es el punto de todo el ejercicio.

## 5. Objetivo de campaña contra restricción

Las 25 campañas históricas se llaman `Trafico_*` y están optimizadas para tráfico. El tráfico se compra barato ($0.34 por registro atribuido) y no es la restricción.

**Antes de recomendar más inversión, verifica que la campaña tenga una hipótesis de conversión escrita y un umbral de decisión fijado antes de encenderla.** Si no la tiene, esa es la recomendación, no el presupuesto.

## Anti-patrones

- **Declarar ROI de campaña mientras la ambigüedad de atribución siga abierta.** Es el error más caro disponible en este dominio.
- **Comparar Top Sources (lifetime) contra un KPI de ventana.** Miden poblaciones distintas.
- **Leer "Registros" de la tabla de fuentes como signups.** Son clics deduplicados.
- **Reportar solo el costo por registro.** Es la cifra que hace ver bien cualquier campaña.
- **Recomendar congelar campañas.** Junior decidió el 3-ago-2026 que corren de forma continua. Si tienes evidencia nueva, preséntala como evidencia y deja la decisión donde está.
- **Tratar "Directo" como orgánico puro.** Mientras B siga en pie, es un cajón de sastre.

## Formato de entrega

1. Tabla de campañas activas con inversión, registros atribuidos, activados y suscripciones.
2. Las tres CAC, en orden, con el denominador visible.
3. El test de la restricción: volumen de entrada contra conversión final, dos ventanas.
4. Estado de la ambigüedad de atribución: abierta o resuelta, y qué se puede afirmar en consecuencia.
5. Recomendación con nivel de confianza explícito.
