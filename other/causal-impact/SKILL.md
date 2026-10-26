---
name: causal-impact
description: 'Ejecuta análisis CausalImpact (inferencia causal bayesiana con series temporales estructurales BSTS) de extremo a extremo, desde un Excel de datos hasta un informe HTML entregable al cliente. Usar para medir el efecto incremental de una intervención (pausa de campaña, cambio de puja, lanzamiento, cambio creativo) cuando no hay grupo de control aleatorizado, apoyándose en series de control no afectadas. Triggers: causal impact, impacto causal, efecto incremental, BSTS, contrafactual, qué habría pasado si, medir el efecto de una pausa o de un cambio de campaña.'
---

# CausalImpact Analyst

Ejecuta análisis CausalImpact profesionales de extremo a extremo: desde cualquier Excel hasta un informe HTML entregable al cliente.

---

## Entorno requerido

| Componente | Valor |
|---|---|
| Python | 3.12 (`.venv` en raíz del proyecto) |
| Script principal | `analysis/causal_impact/run_analysis.py` |
| Config template | `analysis/causal_impact/config_template.json` |
| Outputs | `outputs/charts/`, `outputs/results/`, `outputs/reports/` |

**Variables de entorno obligatorias (ya en el script):**
```
TF_USE_LEGACY_KERAS=1          # TFP 0.25 necesita tf_keras
TF_ENABLE_ONEDNN_OPTS=0        # silencia logs oneDNN
TF_CPP_MIN_LOG_LEVEL=3         # silencia logs C++ de TF
```

**Versiones críticas (no cambiar):**
```
tensorflow==2.21.0
tensorflow-probability==0.25.0
tf-keras==2.21.0
tfp-causalimpact==0.2.0
pandas==2.1.4          # pandas 3.x rompe la API de causalimpact
numpy==1.26.4          # numpy 2.x elimina np.long (scipy falla)
scipy==1.11.4
```

---

## Flujo de trabajo

### 1. Recibir el Excel del usuario

Aceptar cualquier Excel. Moverlo a `CAUSAL IMPACT/<cliente>/` en el repo.

### 2. Inspeccionar la estructura

```python
import pandas as pd
xl = pd.ExcelFile("archivo.xlsx")
print(xl.sheet_names)
df = pd.read_excel("archivo.xlsx", sheet_name=0, index_col=0, parse_dates=True)
print(df.shape, df.dtypes, df.head(3))
```

Determinar:
- Columna **response** (variable objetivo, e.g. "sessions", "revenue")
- Columnas **control** (covariables, máx ~10)
- Rango de fechas y **fecha de intervención** (preguntar al usuario si no está clara)

### 3. Crear config JSON

Copiar `analysis/causal_impact/config_template.json` y rellenar:

```json
{
  "project": {
    "name": "Nombre del análisis",
    "client": "Cliente",
    "analyst": "Advanced Analytics WPP"
  },
  "data": {
    "file": "ruta/al/archivo.xlsx",
    "sheet_main": "Hoja 1",
    "sheet_extra": null,
    "date_column": "index",
    "response_column": "NombreColumnaResponse",
    "control_columns": ["Control_A", "Control_B", "Control_C"]
  },
  "model": {
    "pre_period": ["YYYY-MM-DD", "YYYY-MM-DD"],
    "post_period": ["YYYY-MM-DD", "YYYY-MM-DD"],
    "alpha": 0.05
  },
  "validation": {
    "min_correlation": 0.1,
    "max_vif": 10
  }
}
```

> **Truco ñ:** nombres con caracteres especiales en JSON → usar escape Unicode (`ñ` = `\u00f1`)

### 4. Ejecutar el análisis

```powershell
Set-Location <repo_root>
$env:PYTHONIOENCODING = "utf-8"
& .\.venv\Scripts\python.exe analysis\causal_impact\run_analysis.py --config analysis\causal_impact\config_<cliente>.json 2>&1 | Where-Object { $_ -notmatch "^WARNING|^I0000|oneDNN|tensorflow|DeprecationWarning|FutureWarning|UserWarning|note:" }
```

### 5. Verificar outputs

```
outputs/charts/01_time_series_overview.png
outputs/charts/02_pre_post_distribution.png
outputs/charts/03_correlation_analysis.png
outputs/charts/04_vif_multicollinearity.png
outputs/charts/05_causal_impact_main.png
outputs/charts/06_effect_summary.png
outputs/charts/07_model_diagnostics.png
outputs/charts/08_placebo_test.png
outputs/reports/causal_impact_report.html   ← entregable cliente
outputs/results/*_series.csv
outputs/results/*_effect_summary.csv
```

---

## Narrative Report

Además del summary tabular, el modelo genera un informe narrativo en inglés:

```python
ci_summary_text = str(ci.summary(result))              # tabla resumen
ci_report_text  = ci.summary(result, output_format='report')  # texto narrativo
```

El `report` describe el efecto en lenguaje natural (media observada vs predicha, efecto absoluto y relativo, p-valor interpretado). Se incluye en el HTML con traducción al español en el bloque de explicación.

---

## Tests Placebo Múltiples (5 cortes)

Se ejecutan **5 tests placebo** en cortes del pre-período: 20%, 35%, 50%, 65% y 80%.
Cada test finge una intervención ficticia en esa fecha y verifica que el modelo NO detecta efecto (p > 0.05).

- **Todos pasan**: modelo válido, el efecto real es distinguible del ruido ✅
- **1 falla**: aceptable, puede ser varianza natural en ese corte ⚠️
- **2+ fallan**: revisar controles, posible sobreajuste o tendencias compartidas ❌

El gráfico `08_placebo_tests.png` incluye:
- Fila superior: barras de p-valores de los 5 tests
- Filas inferiores: 5 mini-series con observado vs contrafactual en cada corte

```python
# La función retorna:
{
    "tests": [{"fraction": 0.2, "date": "...", "p_value": 0.34, "rel_effect_pct": 2.1, "passed": True}, ...],
    "passed_count": 4,
    "total_count": 5,
    "all_passed": False,
    "chart": "outputs/charts/08_placebo_tests.png"
}
```

---

## API de tfp-causalimpact (v0.2.0)

```python
import causalimpact as ci

# IMPORTANTE: usar índices enteros, NO fechas como índice
df_int = df.reset_index(drop=True)
pre_period  = (0, 403)    # enteros
post_period = (404, 454)  # enteros

result = ci.fit_causalimpact(df_int, pre_period, post_period)

# Acceso a resultados
result.series    # DataFrame con columnas:
                 # observed, posterior_mean, posterior_lower, posterior_upper
                 # point_effects_mean, point_effects_lower, point_effects_upper
                 # cumulative_effects_mean, cumulative_effects_lower, cumulative_effects_upper
                 # pre_period_start, pre_period_end, post_period_start, post_period_end

result.summary   # DataFrame con columnas:
                 # actual, predicted, predicted_lower, predicted_upper, predicted_sd
                 # abs_effect, abs_effect_lower, abs_effect_upper, abs_effect_sd
                 # rel_effect, rel_effect_lower, rel_effect_upper, rel_effect_sd
                 # p_value, alpha
                 # rows: 'average', 'cumulative'

# Métricas clave
p_value        = float(result.summary["p_value"].iloc[0])
rel_effect_pct = float(result.summary["rel_effect"].iloc[0]) * 100
abs_effect     = float(result.summary["abs_effect"].iloc[0])

# Re-alinear series con fechas originales
series = result.series.copy()
series.index = df.index[:len(series)]   # df tiene índice datetime
```

---

## Errores conocidos y soluciones

| Error | Causa | Solución |
|---|---|---|
| `AttributeError: 'CausalImpactAnalysis' has no attribute 'inferences'` | API antigua documentada en red | Usar `result.series` (no `result.inferences`) |
| `TypeError: '>' not supported between Timestamp and str` | Índice de fechas string en pandas 2.1.4 | `df.reset_index(drop=True)` → índices enteros |
| `resample("ME")` KeyError | `ME` introducido en pandas 2.2 | Usar `resample("M")` |
| `ax.boxplot(labels=...)` warning/error | Deprecado en matplotlib 3.11 | Separar: `ax.boxplot(...)` + `ax.set_xticklabels(...)` |
| TFP no encuentra tf_keras | TFP 0.25 requiere tf-keras separado | `$env:TF_USE_LEGACY_KERAS=1` antes de ejecutar |
| `np.long` not found | numpy 2.x eliminó `np.long` | Pin `numpy==1.26.4` |
| `is_datetime_or_timedelta_dtype` missing | pandas 3.x eliminó esta función | Pin `pandas==2.1.4` |

---

## Pipeline de 8 pasos (interno)

1. **Carga** — lee Excel con openpyxl, detecta índice de fechas, une hojas si hay columnas extra
2. **Validación** — nulos, outliers IQR, estadísticas pre/post
3. **EDA** — serie temporal con media móvil 7d, distribución pre vs post
4. **Correlaciones + VIF** — heatmap de Pearson, gráfico VIF; selección automática de controles (min corr 0.1, max VIF 10, eliminación iterativa)
5. **Estacionariedad** — ADF test en todas las series; aviso si no estacionarias (normal en datos de marketing)
6. **Modelo** — `ci.fit_causalimpact` con índices enteros; convierte fechas a índices y back
7. **Diagnósticos** — residuos en tiempo, histograma + normal teórica, Q-Q plot, ACF; Shapiro-Wilk, Durbin-Watson
8. **Placebo + Informe** — placebo en 70% del pre-período; informe HTML autocontenido con imágenes en base64

---

## Interpretación de resultados

### ¿Es significativo el resultado?
- `p_value < 0.05` → efecto estadísticamente significativo
- `p_value < 0.01` → muy significativo
- Siempre reportar también el intervalo de confianza

### Test placebo
- **PASSED** (p_placebo > 0.05): No hay efecto falso en pre → modelo válido ✅
- **FAILED** (p_placebo < 0.05): Señal en pre-período → posibles causas:
  - Controles correlacionan demasiado con tendencias comunes (típico en marketing)
  - Cambio de régimen en el pre-período
  - Recomendar al cliente interpretar con cautela

### Estacionariedad
- Series no estacionarias → normal en marketing (tendencias, estacionalidad)
- CausalImpact maneja esto internamente con su modelo estructural de series temporales
- Mencionar como limitación en el informe si hay muchas series no estacionarias

### Controles óptimos (para Paradisus)
Los controles seleccionados automáticamente para Paradisus fueron:
- `Control_SEM Clicks US sin PAR`
- `Control_OMC`
- `Control_Demanda_US_PUJ`
- `Control_Landings_Canada`
- `Control_Landings_UK`

---

## Caso de referencia: Paradisus

| Parámetro | Valor |
|---|---|
| Archivo | `CAUSAL IMPACT/ES Holistic/CAUSAL PARADISUS para el notebook - Landings Paradisus Sessions - Ok.xlsx` |
| Config | `analysis/causal_impact/config_paradisus.json` |
| Response | `Response` (sesiones de landing) |
| Pre-período | 2025-01-01 → 2026-02-08 (404 días) |
| Post-período | 2026-02-09 → 2026-03-31 (51 días) |
| Efecto medio diario | +708 sesiones (+23.1%) |
| Efecto acumulado | +36,112 sesiones |
| p-valor | 0.0133 (significativo) |
| Placebo | FAILED (señal en pre, interpretar con cautela) |

---

## Checklist antes de entregar al cliente

- [ ] p-valor < 0.05 (o explicar por qué no es significativo)
- [ ] Gráfico 05 (causal main) legible con bandas de confianza claras
- [ ] Test placebo OK, o si falla: explicación en el informe
- [ ] Diagnósticos: residuos sin patrón claro, ACF sin autocorrelación significativa
- [ ] Período pre suficientemente largo (mínimo 3× el período post)
- [ ] Informe HTML abierto y revisado visualmente antes de enviar
- [ ] Commit al repositorio con análisis completo

---

## Scripts de referencia rápida

```powershell
# Nuevo análisis desde cero
Set-Location <repo_root>
$env:PYTHONIOENCODING = "utf-8"
& .\.venv\Scripts\python.exe analysis\causal_impact\run_analysis.py --config analysis\causal_impact\config_<cliente>.json 2>&1 | Where-Object { $_ -notmatch "^WARNING|^I0000|oneDNN|tensorflow|DeprecationWarning|FutureWarning|UserWarning|note:" }

# Verificar venv
& .\.venv\Scripts\python.exe -c "import causalimpact; import tensorflow as tf; print('TF:', tf.__version__); print('CI OK')"

# Kernel Jupyter
& .\.venv\Scripts\python.exe -m ipykernel install --user --name advanced_analytics_melia --display-name "Python 3.12 (advanced_analytics_melia)"
```

---

## Diseño del informe HTML entregable al cliente

### Principios irrenunciables

1. **Es el documento que recibe el cliente.** Sin frases internas: nada de "Para el cliente:", "Lectura rápida:", "Para presentar al cliente:", "Nota interna:".
2. **Tono directo y profesional.** El lector es el cliente, no el analista.
3. **El output técnico en inglés** (texto de `ci.summary()`) va en un `<details>` colapsable — disponible si se necesita, pero no intrusivo.
4. **Probabilidad, no p-valor como valor principal.** El cliente entiende "98.1% de probabilidad de efecto causal" mejor que "p = 0.0189". El p-valor aparece entre paréntesis para referencia técnica.

### Estructura de secciones

```
1. Resumen Ejecutivo      — KPIs y conclusión en una pantalla
2. Datos y Período        — descripción serie temporal, EDA
3. Validación del Modelo  — correlaciones, VIF, estacionariedad
4. Resultados             — gráfico principal CI, efecto observado vs contrafactual
5. Magnitud del Efecto    — KPI cards (efecto diario, acumulado, % relativo, probabilidad)
6. Diagnóstico            — residuos, Q-Q, ACF, Shapiro-Wilk, Durbin-Watson
7. Tests Placebo          — 5 tests con gráfico combinado + tabla
```

### KPI box "Probabilidad de efecto causal"

```python
# En el gráfico matplotlib (06_effect_summary.png)
("p-valor", f"{p_val:.4f}", f"{(1-p_val)*100:.1f}% prob. efecto causal", sig_color)

# En el HTML
kpi_label = "Probabilidad de efecto causal"
kpi_value = f"{(1 - p_value) * 100:.1f}%"
kpi_sub   = f"Efecto significativo (α = {alpha}, p = {p_value:.4f})"
```

### CSS: variables y clases clave

```css
:root {
    --blue-dark: #1a3a5c;
    --blue-mid:  #2e6da4;
    --blue-light:#4a9fd5;
    --gold:      #c8a84b;
    --green:     #28a745;
    --red:       #dc3545;
    --bg:        #f8f9fa;
    --card-bg:   #ffffff;
}
.insight { border-left: 4px solid var(--blue-mid); padding: 1rem 1.5rem; margin: 1.5rem 0; background: #f0f7ff; }
.finding { background: #fff; border: 1px solid #dee2e6; border-radius: 6px; padding: 1rem; margin-top: 0.75rem; }
.kpi     { text-align: center; padding: 1.5rem; border-radius: 8px; }
.kpi.positive { background: #d4edda; border: 1px solid #28a745; }
.kpi.negative { background: #f8d7da; border: 1px solid #dc3545; }
.kpi.neutral  { background: #fff3cd; border: 1px solid #ffc107; }
.kpi-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-value { font-size: 2rem; font-weight: 700; margin: 0.5rem 0; }
.kpi-sub   { font-size: 0.85rem; color: #666; }
```

### Técnica KPI box matplotlib (evitar fondo blanco en savefig)

`ax.set_facecolor()` con `plt.subplots()` no persiste en `fig.savefig()`. Solución:

```python
fig = plt.figure(figsize=(14, 5), facecolor="#f8f9fa")
for i, (label, value, sub, color) in enumerate(kpis):
    ax = fig.add_axes([x_pos, 0.1, width, 0.8])   # posicionamiento manual
    ax.set_facecolor(color)
    patch = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, ...)
    ax.add_patch(patch)
    ax.text(0.5, 0.7, label, ...)
    ax.text(0.5, 0.45, value, ...)
    ax.text(0.5, 0.2, sub, ...)
    ax.axis("off")
fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight")
```

### Bug vif_rows (resuelto)

El helper que genera las filas de la tabla VIF debe incluir `<tr><td>`:

```python
def vif_rows_fn():
    rows = []
    for k, v in vif.items():
        color = "green" if v < 5 else ("orange" if v < 10 else "red")
        rows.append(f'<tr><td>{k.replace("Control_","")}</td>'
                    f'<td style="color:{color};font-weight:700">{v:.2f}</td>'
                    f'<td>{"✅ OK" if v < 10 else "⚠️ Alto"}</td></tr>')
    return "".join(rows)
```

### Sección cerrada correctamente (bug resuelto)

Cada `<div class="section">` debe cerrarse con `</div>` antes de abrir la siguiente. La omisión colapsa el layout completo.

---

## Tests placebo — criterios de diseño

- **5 cortes** en el pre-período: fracciones [0.20, 0.35, 0.50, 0.65, 0.80]
- **Misma duración** que el post-período real (calculada desde `config["model"]["post_period"]`)
- **Sin solapamiento**: todos operan solo con `df[df.index <= pre_end]`; si `placebo_end > pre_end`, se recorta
- **Interpretación**: ≥ 4/5 PASSED = validación sólida; 3/5 = aceptable con cautela; ≤ 2/5 = revisar controles

```python
post_start  = pd.to_datetime(config["model"]["post_period"][0])
post_end    = pd.to_datetime(config["model"]["post_period"][1])
post_window = (post_end - post_start).days + 1   # misma duración que el real
```

---

## ⚠️ REGLA OBLIGATORIA: Archivar cada proyecto

**Al finalizar CUALQUIER análisis CausalImpact, crear obligatoriamente una carpeta en `projects/causal-impact/`:**

```
projects/
├── causal-impact/               ← TODOS los causal impacts aquí
│   ├── paradisus-us-2026/
│   ├── <próximo-proyecto>/
│   └── ...
├── mmm/                         ← futuros Media Mix Models
├── forecasting/                 ← futuros modelos de previsión
└── ...

projects/causal-impact/<nombre-proyecto>/
├── data/           # Excel original del cliente (renombrar: <proyecto>-data.xlsx)
├── config/         # config JSON usado en el análisis
├── outputs/
│   ├── charts/     # Los 8 PNGs generados
│   └── reports/    # HTML entregable (nombre: causal_impact_report_<proyecto>.html)
└── README.md       # Ficha: cliente, fecha, intervención, métricas clave, notas
```

**Pasos de archivado al terminar:**
1. `New-Item -ItemType Directory -Force -Path "projects\<nombre>\data"` (y subcarpetas)
2. Copiar Excel → `projects/causal-impact/<nombre>/data/<nombre>-data.xlsx`
3. Copiar config JSON → `projects/causal-impact/<nombre>/config/`
4. Copiar `outputs/charts/*.png` → `projects/causal-impact/<nombre>/outputs/charts/`
5. Copiar HTML → `projects/causal-impact/<nombre>/outputs/reports/causal_impact_report_<nombre>.html`
6. Crear `README.md` con ficha del proyecto
7. Añadir fila a la tabla "Proyectos archivados" de este SKILL.md
8. `git add projects/<nombre>/ && git commit && git push`

---


```
projects/<nombre>/
├── data/           # Excel original
├── config/         # config JSON usado
├── outputs/
│   ├── charts/     # 8 PNGs
│   └── reports/    # HTML entregable (nombre_<proyecto>.html)
└── README.md       # Ficha del proyecto: fechas, métricas clave, notas
```

### Proyectos archivados

| Proyecto | Carpeta | Intervención | Efecto | p-valor |
|---|---|---|---|---|
| Paradisus US 2026 | `projects/causal-impact/paradisus-us-2026/` | 9 feb 2026 | +23.1% | 0.019 (98.1%) |
