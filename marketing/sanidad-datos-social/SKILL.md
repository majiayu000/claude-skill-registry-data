---
name: sanidad-datos-social
description: Úsalo cuando una cifra de redes se mueva >20%, cuando dos paneles den números distintos para lo mismo, o antes de declarar un récord o un colapso en Instagram o TikTok. Distingue problema de tubería (dato roto, sync pendiente) de problema de negocio (realidad rota). Para comparar dos periodos del tablero interno, el skill es verificar-comparabilidad.
---

# Sanidad de datos: tubería vs realidad

La pregunta que ordena todo: ¿se rompió el dato o se rompió el negocio? Actuar sobre un dato roto quema una semana; ignorar una caída real la quema dos.


> ### Qué fuente social tiene Kaizen, y qué no (actualizado 2026-09-11)
>
> **Instagram, parcial:** `get_instagram_profile` lee los perfiles guardados en
> Marketing → Configuración (`list_marketing_accounts` dice cuáles). Trae lo
> PÚBLICO: seguidores, seguidos, y por publicación likes y comentarios, con un
> resumen ya calculado (promedios, mediana, por tipo, top 3). Eso es **pulso**:
> sirve para contextualizar, no para decidir. **No trae** alcance, impresiones,
> guardados, retención de video, clicks al link ni registros atribuidos —
> ninguno de los 5 KPIs del funnel—, y los números son del instante en que se
> lee, sin histórico.
>
> **TikTok, parcial (2026-09-18):** `get_tiktok_profile` lee SOLO la cuenta de
> FinZen (la Display API no lee terceros): seguidores, likes totales, videos, y
> por video views/likes/comentarios/compartidos/duración, con mediana de views y
> engagement sobre views calculados. **No trae** retención de video, alcance,
> vistas de perfil ni taps al link: esos siguen en el panel nativo. Criterio en
> `lectura-perfil-tiktok`.
>
> Para lo que la tool no trae, lo único que puedes hacer es aplicar el método a
> números que el socio te pegue en el chat, o citar los que estén guardados en
> el Cerebro. **No inventes cifras de redes ni las estimes**: si te piden un KPI
> social que no tienes, di que Kaizen no tiene acceso a esa fuente todavía.

## 0. Antes de empezar

1. `search_cerebro("rupturas de serie")` — la mitad de los "colapsos" son rupturas ya registradas.
2. `get_kpis` de los 4 periodos previos: la anomalía se define contra la mediana, no contra ayer.
3. Si la cifra viene de una campaña: `get_campaign_results` para contrastar la misma cifra desde la segunda fuente.

## 1. Tabla causa → acción

| Síntoma | Diagnóstico probable | Acción |
|---|---|---|
| TODO en cero el mismo día (incluidos totales acumulados que no pueden ser 0) | Sync pendiente, no caída real | Marcar "sin dato", releer al día siguiente. Nunca reportar como caída |
| Caída >90% en una métrica con las demás sanas | Puede ser real (hay precedente verificado en FinZen) | No asumir tubería: verificar contra segunda fuente antes de descartar |
| Dos cifras distintas para lo mismo, el mismo día | Dos definiciones o dos ventanas con el mismo nombre | Usar la fuente consolidada, declarar cuál se usó y por qué |
| Métrica idéntica varios periodos seguidos (0%, 100%, mismo valor exacto) | Métrica sin poblar o muerta tras un deploy | Marcar "no instrumentado"; proponer retirarla del reporte |
| Ratio que explota (ER 11.96% vs ~1.3% histórico) | Denominador colapsado | El ratio no es comparable; leer numerador y denominador por separado |
| Churn 0% mientras el MRR cae y hay pagos fallidos | La métrica no captura el caso involuntario | Leer el flujo de dinero, no el flag; escalar la definición |
| Lift reportado con brazo de control n=0 o n<30 | Artefacto de panel | Estado correcto: "sin control, no medible". Jamás citar el lift |
| Misma partida listada dos veces (p. ej. filas cpc y paid de la misma campaña) | Doble conteo al sumar | Sumar solo la vista consolidada |
| % de cohorte redondeado justo en la frontera de decisión | Redondeo de panel | Exigir conteos (numerador/denominador) antes del veredicto |

## 2. Regla de cierre

- **Sin dato ≠ 0 ≠ rojo.** El rojo de negocio se gana con dato verificado.
- **Dos periodos seguidos sin dato = rojo de tubería**: se reporta como problema del sistema de medición, con dueño, no como problema de performance.
- Si tras verificar, la caída es real: **se reporta como real aunque duela**. La sanidad protege contra falsas alarmas, no contra malas noticias.

## 3. Ejemplo bueno y malo (datos FinZen reales)

- **Bueno:** la misma semana, TikTok llegó "todo en cero con total_followers=0" (diagnóstico: sync pendiente, se releyó al día siguiente: 266 seguidores intactos) e Instagram cayó −98% en alcance. La segunda se verificó contra el detalle diario y resultó real: 10 días consecutivos de colapso. Mismo síntoma superficial, dos veredictos opuestos, porque se verificó antes de clasificar.
- **Malo:** un panel imprimió "Lift de activación: +18.53 pts (variante 18.53% vs control 0%)" con control n=0 (el experimento corría al 100%). Citar ese lift en cualquier resumen o deck es fabricar un hallazgo. El estado correcto era "sin control, no medible".
- **Malo:** una cohorte apareció como 22% (21/95) en un reporte y 16% (6/37) en otro con dos días de diferencia. Se detectó porque se pidieron conteos; con porcentajes solos habría pasado.

## Anti-patrones

- Declarar caída de negocio el mismo día que aparece un cero masivo, sin releer.
- Descartar como "error de datos" una caída que incomoda, sin segunda fuente.
- Promediar o comparar por encima de una cifra marcada "no comparable".
- Reportar la anomalía y la recomendación en la misma línea (primero causa, luego consejo).

## Formato de entrega

Por cada cifra auditada: **síntoma → verificación hecha (qué fuente contra qué fuente) → veredicto (tubería / real / sin resolver) → qué se puede afirmar y qué no**. Lo "sin resolver" va con la pregunta exacta que lo resuelve y a quién se le hace.
