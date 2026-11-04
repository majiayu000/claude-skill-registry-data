---
name: umbrales-semaforo
description: Úsalo cuando haya que definir el éxito de una campaña, experimento o KPI (antes de lanzarlo), o cuando haya que calificar un número en verde/ámbar/rojo y no exista umbral escrito. También cuando alguien proponga mover un umbral existente.
---

# Umbrales y semáforo: dos cortes, sin trampa

Un umbral definido después de ver el resultado no es un umbral: es una racionalización. Este skill fija cómo se ponen, cómo se aplican y cuándo (no) se mueven.

## 0. Antes de empezar

1. `search_cerebro("umbrales vigentes")` — si ya existe umbral para esa métrica, se APLICA, no se rediseña.
2. `get_kpis` de los últimos 4+ periodos para calibrar (excluyendo periodos marcados anómalos o no comparables).
3. Al fijar un umbral nuevo: `save_cerebro_note` con los cortes, el razonamiento, la fecha de revisión y quién lo aprobó.

## 1. La estructura: dos cortes → tres colores

- **Mínimo aceptable**: por debajo = ROJO. Caer ahí significa que algo se rompió.
- **Línea de mejora**: alcanzarla = VERDE. Se gana superando lo mejor ya demostrado.
- Entre ambos = ÁMBAR: aceptable, sin celebrar.
- **Sin dato = GRIS ("n/d"), nunca rojo.** Dos periodos seguidos sin dato = rojo de tubería (culpa del sistema de medición, con dueño).

## 2. Reglas de calibración

| Regla | Cómo se aplica |
|---|---|
| Calibrar solo con periodos limpios | Los periodos bajo anomalía declarada se excluyen y se dice que se excluyeron |
| La mediana histórica cae en ÁMBAR | El umbral empuja, no consagra: si la mediana quedara en verde, el umbral premia el statu quo |
| Verde = superar lo mejor demostrado | La línea de mejora se ancla en el máximo real observado, no en un deseo |
| El cero crónico no se consagra | Si una métrica lleva semanas en 0, su mínimo aceptable es ≥1: vivir en rojo es la presión correcta para arreglar el eslabón, no un castigo |
| n<3 periodos limpios = umbral provisional | Se marca "provisional", con confianza declarada y fecha de recalibración |
| Umbral de decisión ANTES del resultado | Para experimentos: el gate se firma antes del levantamiento (pre-registro), con la forma "si <X pasa Y, si >Z pasa W" |

## 3. Cuándo se mueven (y cuándo no)

Los umbrales quedan **congelados hasta su revisión programada** (trimestral por defecto) o hasta un **cambio estructural declarado y documentado** (cambio de mezcla de tráfico por diseño, redefinición de la métrica, pivote de formato). **Nunca se mueven en caliente por una mala semana — ni por una buena.** Si un periodo anómalo pinta todo rojo, el semáforo lo dice y el umbral no se toca.

## 4. Ejemplo bueno y malo (datos FinZen reales)

- **Bueno:** el gate del trial se firmó ANTES de leer el dato: "% de FREE que choca el techo: <5% mata el mecanismo, >15% mata la tesis del empaque", con predicción escrita (<5%). Cualquier resultado tiene interpretación pactada de antemano.
- **Bueno:** seguidores netos semanales con historial +34/+39/+46 → mínimo +20 (la mitad del ritmo demostrado = algo se rompió), mejora +50 (supera la mejor semana). La mediana (+39) queda en ámbar: empuja.
- **Malo:** una métrica hermana llevaba 4 semanas en 0 y la tentación era "umbral: 0 está bien mientras crece views". Se rechazó: mínimo +1, rojo permanente hasta romper el cero, con decisión de formato programada si no rompe en la revisión.

## Anti-patrones

- Fijar o ajustar el umbral en la misma sesión en que se lee el resultado que lo incumple.
- Calibrar incluyendo el periodo anómalo "porque es el más reciente".
- Semáforo verde por default cuando falta el dato.
- Umbral sin fecha de revisión ni razonamiento escrito (queda imposible de auditar).
- Copiar umbrales de benchmarks externos sin pasar por el histórico propio.

## Formato de entrega

Por métrica: **mínimo aceptable · línea de mejora · base observada (conteos y periodos usados) · razonamiento en 1-2 líneas · confianza · fecha de revisión**. Si es provisional, decirlo en la misma línea. El conjunto se guarda en el Cerebro y el semáforo posterior solo referencia, no rediscute.
