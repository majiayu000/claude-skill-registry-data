---
name: resumen-semanal
description: El formato y los criterios del resumen semanal automático de crecimiento (corrida del cron de los lunes; también si un socio pide "el resumen de la semana").
---

# Resumen semanal de crecimiento

Un documento que un socio lee en 3 minutos un lunes por la mañana y sabe: cómo
vamos, qué funcionó, y qué hacer esta semana. Datos → lectura → acción. Nunca
un vertedero de números.

## 1. Datos (siempre en este orden, siempre de tools)

1. `get_kpis` de la semana que cerró (lunes a domingo).
2. `get_kpis` de la semana anterior — para comparar.
3. `get_campaign_results` del período — campañas medidas y su lift.
4. Si algo se sale de lo normal (caída/salto fuerte), `evaluate_segment` de los
   segmentos relacionados para dimensionar (ej. cayó retención → ¿creció
   `dormant`?).
5. **Marketing** (es el otro ámbito, pero el resumen es uno solo):
   `list_marketing_accounts` → `get_instagram_profile` de la cuenta de FinZen
   (y hasta 3 competidores guardados) + el skill `lectura-perfil-instagram`
   para el criterio; `get_tiktok_profile` de la cuenta de FinZen + el skill
   `lectura-perfil-tiktok` (otro criterio: mediana de views y compartidos); `get_meta_spend` de la semana si Meta está configurado.
   La comparación semanal de Instagram es `historico.delta_7d` (si es `null`,
   no hay lectura de hace 7 días: se dice, no se estima). Si algo no está
   configurado o falta un permiso, la sección lo dice en una línea — **se
   omite el dato, nunca la sección**.

## 2. Estructura del documento

```markdown
# Resumen semanal de crecimiento — {YYYY-MM-DD}
**Período:** {lunes} al {domingo} · Generado por Kaizen

## En una línea
La lectura de la semana en una frase honesta.

## Los números que importan (vs semana anterior)
3-5 movimientos RELEVANTES, cada uno: cifra actual, delta, y una línea de
lectura. No listar todos los KPIs — elegir los que cuentan la historia.

## Campañas
Por cada campaña medida: nombre, segmento, lift (o pre/post con su disclaimer)
y qué aprendimos. Si no hubo campañas: decirlo y qué oportunidad se perdió.

## Redes y pauta
Instagram de FinZen: seguidores y su delta de 7 días (con la distancia real
si no es 7), tasa de engagement y mediana de likes con la referencia de
tamaño dicha como referencia, y —si hay insights— alcance, guardados y taps
al link. Los taps van AL LADO de los registros atribuidos a instagram de
`get_kpis`: es el puente entre las redes y el negocio. TikTok de FinZen: seguidores a 30 y 7 días
(si hubo un salto, a qué video se debe), mediana de views, engagement sobre
views y lo más compartido. Competidores guardados (solo Instagram):
una línea cada uno, tasa comparada por tamaño, nada de "les va mejor". Meta:
gasto de la semana en la moneda de la cuenta y qué campañas gastaron de
verdad (`effective_status`); el CAC combinado SOLO si los nombres de campaña
unen con `utm_campaign`, y si no unen, decirlo. Sin credenciales o sin
perfiles guardados: una línea que lo diga, y seguir.

## Recomendaciones para esta semana (2-3)
Cada una: acción concreta + el dato que la respalda + impacto esperado.
Si una implica campaña: segmento con count real (evaluate_segment), mensaje
sugerido y medición — pero NO crearla (los socios la piden por chat si convence).

## Vigilar
1-2 señales a observar esta semana (métricas cerca de un umbral, experimentos
en ventana de medición).
```

## 3. Criterios de calidad

- **Honestidad primero**: si la semana fue mala, la primera línea lo dice. Un
  resumen que maquilla es peor que no tener resumen.
- **Pagar ≠ tener un plan.** `plan_distribution` incluye a los que están en
  prueba gratis: no lo reportes como "usuarios de pago" ni sumes sus categorías.
  Cruza siempre contra `mrr_usd` y `trials.active`; si el total no cuadra con
  los precios de los planes, di el desglose por plan y cuántos están en prueba
  en vez de inventar un número de pagos.
- **Toda campaña que menciones lleva su estado y su fecha real.** Las del bloque
  `campaigns` ya se enviaron (`sent_at` es la fecha de publicación, úsala tal
  cual). Un borrador que creaste y sigue en PENDING_APPROVAL **no salió**:
  dilo así, nunca lo reportes junto a las enviadas sin distinguirlo.
- **Deltas con contexto**: "MRR $1,480 (+3.2%)" y no "$1,480". Registros bajos
  en semana de asueto → decir el contexto, no gritar tendencia.
- **Ojo con muestras chicas**: cambios porcentuales grandes sobre números
  chicos (3→6 trials = "+100%") se reportan en absolutos.
- **Cada recomendación es accionable esta semana** — no "mejorar la retención"
  sino "campaña a los 95 dormidos FREE de 30+ días con gancho de racha".
- Convención de la API: los `*_pct` son puntos (31.0 = 31%).
- **En redes, likes son pulso.** "La pieza que más llamó la atención" sí;
  "la pieza que funcionó" solo con guardados y alcance (skill
  `lectura-perfil-instagram`). Un delta de seguidores menor al 1 % del total
  en la semana se reporta como "estable", sin adjetivo.

## 4. Entrega

`save_cerebro_note` (título `resumen-semanal-{YYYY-MM-DD}`, fecha del lunes
de generación) — sin pasar `subcarpeta`, para que caiga en `50-kaizen/`, que es
donde el socio revisa los lunes. NUNCA a Contenidos/assets (esa es para piezas
de redes ya terminadas, no para reportes). Formato Markdown con la estructura de
arriba.
