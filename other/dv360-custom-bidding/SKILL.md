---
name: dv360-custom-bidding
description: >
  Custom Bidding de Google Display & Video 360 (DV360): escritura, revisión y depuración de
  scripts de puja personalizada. Cubre el DSL completo (funciones de agregación
  max_aggregate/sum_aggregate/first_match_aggregate, casting, log), el catálogo de señales
  (dimensiones, geo, dispositivo, inventario, viewability, vídeo/audio, Floodlight, GA4),
  las limitaciones del lenguaje (sin bucles, sin def, sin try, sin slices), y patrones
  probados en producción: tROAS escalonado, CPA fijo, micro-conversiones de checkout,
  routing por insertion_order_id, panel de pesos centralizado y bloque fallback.
  Usar al crear un algoritmo de custom bidding, iterar sobre uno existente, diagnosticar
  underdelivery o data sparsity, o traducir un objetivo de negocio a una función de scoring.
license: MIT
metadata:
  version: 1.0.0
  author: MichelRojo86WPP
  category: marketing-analytics
  domain: programmatic
  tier: POWERFUL
  updated: 2026-09-02
  platforms: dv360, floodlight, google-analytics-4
---

# DV360 Custom Bidding

Escribe, revisa y depura scripts de **Custom Bidding** de Display & Video 360.
Un script asigna un **score** a cada impresión; DV360 entrena un modelo que puja por
maximizar ese score por unidad de coste (*Maximize custom value / cost*).

**Keywords:** DV360, Display & Video 360, custom bidding, custom bidding script, puja
personalizada, Maximize custom value/cost, tROAS, CPA, Floodlight, u-variables,
conversion_custom_variable, max_aggregate, sum_aggregate, first_match_aggregate,
score de impresión, data sparsity, underdelivery, algoritmo de puja.

---

## ⚠️ Regla número uno: no es Python

El script **parece** Python y por eso todo el mundo se equivoca igual. Es un DSL sandboxed.
Antes de escribir una sola línea, ten presente que **no existen**:

- `for`, `while` — no hay bucles de ningún tipo
- `def`, `lambda`, `class`, `import` — no puedes definir nada
- `try` / `except` / `raise` / `assert` — la robustez se hace con `if x == None:`
- `is` / `is not` — usa `== None` y `!= None`
- slices y subscripts: `lista[1:3]`, `lista[0]`
- atributos: `domain.length`
- argumentos con nombre: `func(a=1)`
- asignación múltiple, encadenada o aumentada: `_a, _b = 1, 2` · `_a = _b = 2` · `_i += 1`
- `break`, `continue`, `yield`, `del`, `pass`, `global`

Catálogo exhaustivo en [`references/syntax-reference.md`](references/syntax-reference.md).
**Nunca inventes una señal o función**: si no está en esa referencia, no existe.

---

## Anatomía de un script

```python
# ==========================================
# --- 1. CONFIGURACIÓN DE IDs ---
# ==========================================
_FL_SALES_ID = 9310399
_FL_CHECKOUT_ID = 9310405
_IOS_PROSPECTING = {27037546, 27044747, 27074041}

# ==========================================
# --- PANEL DE CONTROL DE PESOS ---
# ==========================================
_weight_dest = 1.5
_weight_other = 0.5
_checkout_val = 50

# ==========================================
# --- 2. EXTRACCIÓN DE DATOS ---
# ==========================================
_sales_count = total_conversion_count(_FL_SALES_ID, 0)
_sales_value = total_conversion_value(_FL_SALES_ID, 0)

if _sales_value == None:
    _sales_value = 0.0
else:
    _sales_value = float(_sales_value)

_has_sale = _sales_count > 0

# ==========================================
# --- 3. LÓGICA DE PUNTUACIÓN ---
# ==========================================
if insertion_order_id in _IOS_PROSPECTING:
    return max_aggregate([...])
else:
    return max_aggregate([...])
```

Cuatro bloques, siempre en este orden: **IDs → pesos → extracción → scoring**.
El "panel de control de pesos" separado es lo que permite iterar sin tocar la lógica.

---

## Elegir la función de agregación

| Función | Devuelve | Cuándo |
|---|---|---|
| `first_match_aggregate` | Peso del **primer** criterio verdadero | Cascada de prioridad estricta; el orden es la lógica. |
| `max_aggregate` | Peso **más alto** entre los verdaderos | Criterios solapables donde debe ganar la señal más valiosa (venta > checkout > clic). **El más usado.** |
| `sum_aggregate` | **Suma** de los pesos verdaderos | Señales genuinamente acumulables. Cuidado: infla el score y desbalancea el modelo. |

Regla práctica: si una impresión con venta también tiene checkout y clic, `sum_aggregate`
la puntuaría tres veces. Casi siempre quieres `max_aggregate`.

---

## Flujo de trabajo

### 1. Traducir el objetivo de negocio a scoring

| Objetivo | Score |
|---|---|
| Maximizar ingresos (ROAS) | Proporcional a `total_conversion_value` |
| Maximizar volumen (CPA) | Valor **fijo** por conversión, independiente del importe |
| Priorizar un subconjunto (hotel, producto, destino) | `conversion_custom_variable` + conjunto + peso |
| Combatir escasez de datos | Añadir micro-conversión (checkout, add-to-cart) con valor fijo bajo |
| Mejorar calidad de medio | `active_view_viewed`, `time_on_screen_seconds`, `video_completed` |

### 2. Escribir el script

Ver patrones listos para copiar en
[`references/patterns.md`](references/patterns.md).

### 3. Validar antes de guardar

- **Check syntax** en la ventana *New script*.
- **Test your script** sobre 10 000 impresiones muestreadas. Vigila:
  - **% de errores de ejecución** → debe ser ~0. Si no, hay `None` sin proteger.
  - **% de impresiones puntuadas** y **% con score > 0** → si es muy bajo, el script es
    demasiado restrictivo y provocará *underdelivery*.
  - Distribución de scores → si un tramo concentra casi todo el valor, aplana con `log()`
    o con tramos escalonados.
- Descarga el `.csv` para inspeccionar impresiones individuales.

> 🔌 **¿Publicar por API en vez de a mano?** El flujo (`uploadScript` → `media.upload` →
> `scripts.create`), la validación programática vía `errors[]` y la limitación que impide
> republicar sobre un algoritmo ya asignado a line items están en
> [`references/syntax-reference.md` § 8](references/syntax-reference.md#8-publicación-por-api).

### 4. Activar y medir

- Procesado del script: ~20 min. Entrenamiento del modelo: **1–3 días**.
  El modelo está listo cuando *Is the model ready?* = **Yes**.
- Activa en IO (*Optimization › Automate bid & budget…*) o en LI (*Bid strategy › Automated Bidding*),
  siempre con **Maximize custom value / cost**.
- Monta un **experimento A/B** con el custom bidding como variante frente al control.
  Sin control no hay lectura creíble.

### 5. Iterar

Cada iteración se documenta: fecha, síntoma observado, hipótesis, cambio aplicado.
Nunca sobrescribas el script anterior — el valor está en la trazabilidad.

Disciplina de iteración:

- **Un cambio por iteración.** Si tocas pesos, valor de checkout y segmentación a la vez,
  no sabrás qué funcionó.
- **Espera al menos una semana** entre cambios: el modelo necesita reaprender.
  Cambiar constantes a diario garantiza que nunca salga del periodo de aprendizaje.
- El "panel de control de pesos" hace que el diff entre iteraciones sea legible.

### Convenciones de estilo recomendadas

Estas convenciones vienen de scripts en producción y valen la pena por lo mismo que
en cualquier código: el script lo va a heredar otra persona.

- Prefijo `_` en **todas** las variables, para distinguirlas de las señales de DV360.
- `_MAYUSCULAS` para constantes (IDs, conjuntos, pesos globales);
  `_minusculas` para lo derivado dentro de la lógica.
- Sufijos consistentes: `_id`, `_count`, `_value`, `_weight`, `_val`, y `_has_` / `_is_`
  para booleanos.
- Cabeceras de bloque numeradas y delimitadas (`# --- 2. EXTRACCIÓN DE DATOS ---`)
  para poder navegar un script largo.
- Un único `return` por rama, siempre con una función de agregación.
  Evita cascadas de `if/else` dentro del `return`.

---

## Diagnóstico de problemas frecuentes

| Síntoma | Causa probable | Acción |
|---|---|---|
| **Underdelivery** / el IO no gasta | Muy pocas impresiones con score > 0; el modelo no encuentra inventario que cumpla | Añadir micro-conversiones, subir el suelo de score, revisar el bloque fallback |
| **Data sparsity** — el modelo no entrena | Menos conversiones de las que exigen los [requisitos de datos](https://support.google.com/displayvideo/answer/9723477) | Inyectar una señal intermedia (checkout, form) con valor fijo pequeño |
| **% de errores de ejecución > 0** | `None` sin guarda antes de `float()`, `str()` o una comparación | Añadir `if x == None:` para cada llamada a `conversion_*` |
| El script puntúa 0 siempre | El Floodlight **no está asignado** a los Line Items que usan el algoritmo | Asignar la conversión en *tracked conversions* de cada LI. Es el error operativo más repetido. |
| `conversion_custom_variable` devuelve siempre `None` | La u-variable **no se ha compartido** con DV360 | En **CM360**: *Admin › Floodlight configuration › Custom Floodlight variables › icono del ojo*. Verifica también el mapeo advertiser ↔ Floodlight group. Sin este paso no hay error de ejecución, solo `None` silencioso. |
| Puntúa conversiones que no son de esta campaña | Píxel global de Floodlight que dispara en todo el site | Segmentar por `conversion_custom_variable` (p. ej. ID de producto) en lugar de por el conteo global |
| Una conversión cara domina el entrenamiento | Cola larga de revenue | Escalonar por tramos (tROAS "aplanado") o `log(_value)` |
| Empeora al asignarlo a campañas ajenas | No hay rama por defecto | Añadir siempre un **bloque fallback** con peso bajo |

---

## Referencias de esta skill

| Fichero | Contenido |
|---|---|
| [`references/syntax-reference.md`](references/syntax-reference.md) | DSL completo: sintaxis, operadores, funciones, **todas** las señales, limitaciones y ciclo de vida operativo. |
| [`references/patterns.md`](references/patterns.md) | Patrones de código reutilizables, limpios y listos para pegar, con IDs de ejemplo anonimizados. |
| [`references/video-genre-ids.md`](references/video-genre-ids.md) | Mapeo de `video_genre_ids` y enlaces a las hojas de IDs de DV360. |
| [`references/ecosistema-y-recursos.md`](references/ecosistema-y-recursos.md) | Herramientas y repositorios externos (`bid2x`, *Script Builder*) con su nivel de confianza, y qué no se ha podido verificar. |

> Los scripts reales de cliente (Floodlight IDs, IOs, conjuntos de productos, historial de
> iteraciones) **no viven aquí**: este repositorio es público y portable. Van en el repo del
> cliente, en `projects/dv360-custom-scripts/`.

## Documentación oficial

- [Custom bidding script reference](https://support.google.com/displayvideo/answer/11967043)
- [Create a custom bidding script](https://support.google.com/displayvideo/answer/9728993)
- [Using Floodlight data in custom bidding scripts](https://support.google.com/displayvideo/answer/11969760)
- [Using impression level data in custom bidding scripts](https://support.google.com/displayvideo/answer/11968381)
- [Using data from Google Analytics in custom bidding scripts](https://support.google.com/displayvideo/answer/11969662)
- [Custom bidding data requirements](https://support.google.com/displayvideo/answer/9723477)
- [A/B experiments en DV360](https://support.google.com/displayvideo/answer/9040669)
- [DV360 API](https://developers.google.com/display-video/api/reference/rest)
- [Referencia del recurso `customBiddingAlgorithms.scripts`](https://developers.google.com/display-video/api/reference/rest/v4/customBiddingAlgorithms.scripts)

## Skills relacionadas

- `programmatic-analyst` — contexto general de DV360, deals, brand safety, viewability.
- `marketing-attribution` — decidir si un test de custom bidding necesita lectura incremental.
- `causal-impact` / `meridian-geox` — medir el impacto real del cambio de puja.
