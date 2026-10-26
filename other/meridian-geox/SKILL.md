---
name: meridian-geox
description: >
  Diseño y análisis de geo-experimentos de incrementalidad con Google Meridian GeoX:
  API Python real (DesignConfig, Constraints, Budget, run_design, AnalysisConfig, analyze),
  tipos de experimento (holdback, go-dark, heavy-up), asignación estratificada de geos,
  Time-Based Regression (TBR), inferencia robusta por placebos, MDE y potencia estadística,
  activación en Google Ads y calibración de priors de Meridian MMM. Usar al diseñar,
  ejecutar, analizar o depurar un geo-experimento, o al convertir sus resultados en
  priors de ROI para un MMM.
license: MIT
metadata:
  version: 1.0.0
  author: MichelRojo86WPP
  category: marketing-analytics
  domain: geo-experiments
  tier: POWERFUL
  updated: 2026-09-02
  frameworks: meridian-geox, jax, pydantic, pandera, google-meridian
---

# Meridian GeoX

Diseña y analiza **geo-experimentos de incrementalidad** con [Google Meridian GeoX](https://github.com/google/meridian-geox), la librería open-source de Google que establece un estándar para la geo-experimentación. Cubre el ciclo completo: preparación de datos → diseño del estudio → activación en plataforma → análisis contrafactual → inferencia robusta → calibración del MMM.

**Keywords:** geo-experiment, geo-lift, incrementalidad, holdback, go-dark, heavy-up, go-dim, treatment/control geos, MDE, minimum detectable effect, potencia estadística, A/A test, stratified sampling, k-means, DTW, Sobol, TBR, time-based regression, ATT, counterfactual, placebo inference, design-aware inference, iROAS, iCPD, CpIC, cooldown, budget-neutral test, multi-cell, calibración de priors MMM.

---

## ⚠️ Lo primero: GeoX **no** es Meridian MMM

Son **dos librerías distintas** que se complementan. Confundirlas es el error más frecuente.

| | **Meridian MMM** (`google-meridian`) | **Meridian GeoX** (`meridian-geox`) |
|---|---|---|
| Qué hace | Modela el mix de medios sobre datos observacionales | Diseña y analiza experimentos geográficos |
| Import | `from meridian.model import model` | `import meridian_geox as geox` |
| Motor | TensorFlow Probability, MCMC bayesiano | **JAX** (vectorización, sin MCMC) |
| Salida | ROI/mROI, curvas de respuesta, presupuesto óptimo | Diseño de experimento, lift incremental, iCPD |
| Skill del repo | `skills/meridian-mmm/` | **esta skill** |

**Puente entre ambas:** el `AnalysisResult` de GeoX se convierte en priors de ROI del MMM vía `CalibrationBuilder` → ver `references/mmm-calibration.md`.

---

## Entorno requerido

| Componente | Requisito |
|---|---|
| Paquete | `pip install --upgrade meridian-geox` |
| Versión de referencia | **1.0.0** (release inicial, 2026-09-01), Apache 2.0 |
| Python | **≥3.10** (solo GeoX) · **≥3.11** si se combina con Meridian MMM |
| Con MMM | `pip install --upgrade 'google-meridian[meridian-geox]'` |
| Desarrollo | `pip install --upgrade git+https://github.com/google/meridian-geox.git` |
| Dependencias | `jax`, `jaxkd`, `matplotlib`, `numpy`, `pandas`, `pandera`, `pydantic>=2`, `scipy`, `seaborn`, `statsmodels`, `tslearn` |
| ⚠️ Dependencia no declarada | **`pip install absl-py`** — sin ella `import meridian_geox` falla con `ModuleNotFoundError: No module named 'absl'`. Verificado en 1.0.0. |
| GPU | **Opcional.** `pip install meridian-geox` instala JAX en CPU; recomendable JAX con GPU para simulaciones pesadas (por defecto se puntúan 100.000 candidatos) |

> A diferencia de Meridian MMM, **GeoX no requiere GPU** ni versiones nightly de TensorFlow Probability. Es mucho más ligero de ejecutar.

---

## ⚠️ Avisos críticos anti-alucinación

Este dominio es muy propenso a generar API plausible pero inexistente. Antes de escribir código, verifica contra `references/api-reference.md`.

**1 · El paquete es plano.** No existen subpaquetes `design/` ni `analysis/`. Son módulos de primer nivel: `api.py`, `design.py`, `analysis.py`, `generate_candidates.py`, `validation.py`, `util.py`, más `data_quality/` y `methodology/`. El directorio `meridian_geox/data/` contiene **datasets de ejemplo**, no código.

**2 · Solo TBR está soportada.** El enum `Methodology` contiene `TBR` y `SDID`, pero la FAQ oficial afirma que GeoX soporta la metodología TBR. La documentación menciona además "synthetic control" y "synthetic difference-in-differences" — **no los uses**: trata TBR como la única metodología plenamente soportada y documentada.

**3 · `GBR` y `trimmed match` NO forman parte de Meridian GeoX.** No aparecen en ninguna página de la documentación. GBR es terminología de la literatura previa de Google (Vaver & Koehler); `trimmed match` es una librería separada (`google/trimmed_match`). La única referencia legacy que la FAQ reconoce es **TBRMM** (time-based regression matched markets).

**4 · `design_scorer` está declarado pero no implementado.** En `run_design` el código hace literalmente `del design_scorer  # Unused in skeleton.` No lo uses.

**5 · Defaults que casi siempre se asumen mal:**

| Parámetro | Default **real** | Error habitual |
|---|---|---|
| `alpha` | **0.1** → CI del **90%** | asumir 0.05 / CI 95% |
| `power` | 0.8 | — |
| `min_r2` | **0.8** | — |
| `max_conversions_percent` | **0.3** (debe ser **<0.5**) | asumir 0.5 |
| `n_candidates` | 100.000 | — |
| `n_ranked_candidates` | 100 | — |
| `n_top_placebos` | **500** | — |
| `min_placebo_r2` | **0.6** (≠ `min_r2` del diseño) | confundirlos |
| `num_strata` | 4 | — |
| `seed` | 42 | — |
| `geo_assignment_rule` | `STRATIFIED_SAMPLING` | asumir `RANDOM` |
| `methodology` | `TBR` | — |
| `experiment_types` | `HOLDBACK` | — |

**6 · Datos: reglas duras.**
- Granularidad **diaria obligatoria**. Las series semanales se **rechazan explícitamente** (`'Weekly patterns are not supported.'`).
- Pretest **≥ 3× la duración del test** (regla 3N), tanto en diseño como en análisis.
- Geos ≥ `2 * (cell_count + 1)`.
- `conversions` debe ser **absoluta y sin valores negativos**. Las métricas ratio (ROAS) **no están soportadas**. Usar conversiones **raw, sin atribuir**.

**7 · Semántica de `Budget` por tipo de experimento** — se equivoca con frecuencia:

| Tipo | Cómo se expresa | Signo |
|---|---|---|
| `HOLDBACK` | `Budget(budget=500000)` — gasto total de la nueva campaña | absoluto |
| `HEAVY_UP` | `Budget(budget_pct=0.5)` — +50% sobre baseline | **positivo** (default `+1.0`) |
| `GO_DARK` | `Budget(budget_pct=-1.0)` apagado total · `-0.5` go-dim 50% | **negativo** (default `-1.0`) |

`Budget` exige **exactamente uno** de `budget` o `budget_pct`; pasar ambos o ninguno lanza `ValueError`.

---

## Import correcto

```python
import datetime
import pandas as pd
import meridian_geox as geox

# Símbolos disponibles tras el import (26 en total):
#   Diseño   : run_design, compare_designs, concat_design_reports, plot_design
#   Análisis : analyze, plot_analysis
#   Calidad  : check_design_data_quality, check_analysis_data_quality
#   Tipos    : DesignConfig, Constraints, Budget, Design, DesignSet,
#              AnalysisConfig, AnalysisResult, AnalysisMetrics, Estimate,
#              DataSchema, QualityCheckConfig, QualityCheckResult
#   Enums    : ExperimentType, Methodology, GeoAssignmentRule, TestType, GeoGroup
```

---

## Flujo de trabajo (7 fases)

```
1. DATOS PRETEST
   ├── Serie DIARIA por geo: date, location, conversions [, spend | spend_cell_k]
   ├── Conversiones raw sin atribuir, en condición BAU, sin negativos
   ├── spend obligatorio si GO_DARK o HEAVY_UP; opcional si HOLDBACK
   └── Longitud ≥ 3 × duración del test (6N o 1 año si hay estacionalidad fuerte)

2. DISEÑO DEL ESTUDIO
   ├── DesignConfig  : duración, tipo(s), cell_count, alpha, power, CpIC objetivo
   ├── Constraints   : geos excluidos/forzados, fechas excluidas, presupuesto
   ├── geox.run_design(data, design_config, constraints) → DesignSet
   ├── Revisar design_metrics: mde, budget, design_implied_cpic, r2, p_value (AA)
   ├── geox.plot_design(selected_design) → validar alineamiento pretest
   └── selected_design.export_to_json() → CONGELAR el diseño

3. ACTIVACIÓN EN PLATAFORMA
   ├── Geo-targeting por Presence + exclusión explícita de geos
   ├── Duplicación de campañas si el presupuesto está capped
   ├── Etiquetar campañas: 'Control' / 'Heavy-up' / 'Go-dark'
   └── Monitorizar pacing (Looker) — verificar fuga $0 en go-dark

4. RECOGIDA DE RESULTADOS
   ├── KPI diario por geo durante el vuelo + spend de las campañas testadas
   ├── Anotar learning periods y fechas con incidencias → excluirlas
   └── Cooldown opcional tras el fin del test

5. ANÁLISIS
   ├── Cargar el MISMO Design congelado: Design.load_from_json(...)
   ├── AnalysisConfig: design, analysis_start_date, analysis_end_date, pretest_end_date
   ├── geox.analyze(data, analysis_config) → AnalysisResult
   └── geox.plot_analysis(result) → 4-plot suite

6. INTERPRETACIÓN
   ├── metrics.icpd (point_estimate, standard_deviation) → coste por conversión incremental
   ├── incremental conversions, percent lift, iROAS, p-value, CI (1-alpha = 90%)
   ├── Verificar nº de placebos válidos (warning <100, ERROR <10)
   └── Revisar QualityCheckResult antes de comunicar nada

7. CALIBRACIÓN DEL MMM (opcional)
   └── AnalysisResult → CalibrationBuilder.with_meridian_geox_experiment_result()
       → CalibratedPriors → priors.roi_m → ModelSpec de Meridian MMM
```

---

## Tipos de experimento

| Tipo | Treatment | Control | Cuándo usarlo |
|---|---|---|---|
| **`HOLDBACK`** | Recibe *new spend* | Zero spend (held back) | Lanzar un canal/táctica **net-new** y validar su retorno incremental antes de escalar |
| **`GO_DARK`** | Spend apagado (ablado) | BAU spend | **Defender presupuestos**: demostrar el valor base que se perdería al apagar (p. ej. brand paid search) |
| **`HEAVY_UP`** | Spend incrementado +X% | BAU spend | Prever **retornos marginales** de subir presupuesto; o cuando el spend actual es demasiado bajo para dar potencia a un go-dark |

**Single-cell** es más robusto estadísticamente: concentra toda la potencia en una comparación, requiere menos geos y menos presupuesto para un MDE bajo. **Multi-cell** comparte un control común entre varios brazos — útil para tests budget-neutral (`{'cell_1': GO_DARK, 'cell_2': HEAVY_UP}`), comparación cross-publisher y experimentos de optimización.

---

## Plantilla mínima end-to-end

```python
import datetime
import pandas as pd
import meridian_geox as geox

# --- FASE 2: diseño ---------------------------------------------------------
design_data = pd.read_csv('pretest.csv')  # date, location, conversions, spend

design_config = geox.DesignConfig(
    experiment_duration=datetime.timedelta(days=28),
    experiment_types=geox.ExperimentType.HEAVY_UP,
    methodology=geox.Methodology.TBR,
    geo_assignment_rule=geox.GeoAssignmentRule.STRATIFIED_SAMPLING,
    design_output_count=5,
)

constraints = geox.Constraints(
    budget_constraint=geox.Budget(budget=100000),
)

design_set = geox.run_design(design_data, design_config, constraints)
print(design_set.design_metrics)          # mde, budget, design_implied_cpic, r2, p_value (AA)

selected_id = next(iter(design_set.designs))   # el DesignSet viene ya rankeado
selected_design = design_set.designs[selected_id]
geox.plot_design(selected_design)

with open('design.json', 'w') as f:            # CONGELAR el diseño
    f.write(selected_design.export_to_json())

# --- FASE 5: análisis (tras ejecutar el experimento) ------------------------
with open('design.json') as f:
    design = geox.Design.load_from_json(f.read())

analysis_data = pd.read_csv('posttest.csv')

analysis_config = geox.AnalysisConfig(
    design=design,
    analysis_start_date=pd.Timestamp('2026-05-01'),
    analysis_end_date=pd.Timestamp('2026-05-28'),
)

result = geox.analyze(analysis_data, analysis_config)
geox.plot_analysis(result)
```

---

## Referencias

| Fichero | Cuándo consultarlo |
|---|---|
| `references/api-reference.md` | **Siempre antes de escribir código.** API real completa: enums, dataclasses, firmas, defaults |
| `references/design-guide.md` | Diseñar el experimento: MDE, potencia, stratified sampling, presupuesto, restricciones |
| `references/analysis-guide.md` | Analizar resultados: TBR, ATT, placebos, métricas de salida, interpretación |
| `references/data-requirements.md` | Preparar y validar datos: esquema, regla 3N, quality checks, outliers |
| `references/google-ads-implementation.md` | Activar el test en plataforma: campañas, targeting, learning periods, cooldown |
| `references/mmm-calibration.md` | Convertir el resultado en priors de ROI para Meridian MMM |
| `references/notebooks-walkthrough.md` | Notebooks oficiales single-cell y multi-cell celda a celda |
| `references/troubleshooting-glossary.md` | El diseño no sale, el resultado no es significativo, glosario y FAQs |
| `references/wpp-context.md` | Convenciones del repo, aplicación a un cliente, relación con CausalImpact |

---

## Cuándo usar GeoX y cuándo no

| Situación | Herramienta |
|---|---|
| Quiero **medir causalmente** el efecto de una táctica y **puedo intervenir** en plataforma por geografía | **Meridian GeoX** |
| Ya ocurrió una intervención y solo tengo datos observacionales (pausa, cambio de estrategia) | **CausalImpact** (`skills/` + `projects/causal-impact/`) |
| Quiero repartir presupuesto entre canales sobre histórico observacional | **Meridian MMM** (`skills/meridian-mmm/`) |
| Tengo un MMM y quiero anclar su ROI con evidencia causal | **GeoX** → calibración → **MMM** |

---

## Recursos oficiales

- Documentación: <https://developers.google.com/meridian/geox/>
- Repositorio: <https://github.com/google/meridian-geox>
- Notebooks: <https://github.com/google/meridian-geox/tree/main/meridian_geox/colab>
- White paper: <https://research.google/pubs/pub1090193/>
- Activación en Google Ads: <https://support.google.com/google-ads/answer/18073432>
- Calibración de priors del MMM: <https://developers.google.com/meridian/docs/advanced-modeling/set-custom-priors-past-experiments>
