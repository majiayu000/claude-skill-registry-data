---
name: meridian-mmm
description: >
  Marketing Mix Modeling con Google Meridian: instalación y requisitos, API Python real
  (InputData, ModelSpec, PriorDistribution, Meridian, Analyzer, BudgetOptimizer), diagnóstico
  de convergencia MCMC y Health Score, ROI/mROI y curvas de respuesta, optimización de
  presupuesto cross-channel (con y sin Reach & Frequency), y patrones de aplicación práctica. Usar al
  construir, depurar, interpretar o actualizar un modelo Meridian, o al compararlo con
  CausalImpact/MTA.
license: MIT
metadata:
  version: 1.0.0
  author: MichelRojo86WPP
  category: marketing-analytics
  domain: mmm
  tier: POWERFUL
  updated: 2026-09-01
  frameworks: google-meridian, tensorflow-probability, jax, mlflow
---

# Meridian MMM

Modela y optimiza el mix de medios con [Google Meridian](https://github.com/google/meridian), la librería open-source de MMM bayesiano de Google. Cubre el ciclo completo: preparación de datos → especificación del modelo → ajuste MCMC → diagnóstico → ROI/mROI → optimización de presupuesto → actualización periódica.

**Keywords:** Meridian, Marketing Mix Modeling, MMM, MCMC bayesiano, ROI, mROI, curvas de respuesta, Adstock, Hill saturation, Reach & Frequency, BudgetOptimizer, PriorDistribution, health score, R-hat, geo model, national model, incrementalidad, atribución.

## Entorno requerido

| Componente | Requisito |
|---|---|
| Python | 3.11 – 3.13 (3.10 eliminado desde v1.5.3) |
| Instalación | `pip install google-meridian` (o `[jax]`, `[and-cuda]`, `[mlflow]`, `[scenarioplanner,schema]`) |
| TensorFlow | `>=2.21,<2.22` |
| TFP | `tfp-nightly==0.26.0.dev20260130` ⚠️ versión **nightly**, no la estable |
| NumPy | `>=2.0.2,<2.4.0` |
| GPU | Prácticamente obligatoria — T4 mínimo, 16 GB RAM de GPU (MCMC en CPU puede tardar horas) |
| Versión de referencia | Meridian 1.8.0 (agosto 2026), licencia Apache 2.0 |

> ⚠️ **Aviso crítico #1:** usar la versión estable de TFP en vez de la nightly especificada causa errores en tiempo de ejecución.
>
> ⚠️ **Aviso crítico #2 — API inventada:** nunca generes código Meridian por plausibilidad. Métodos/clases que **NO existen** y aparecieron por error en documentación previa del equipo: `meridian.Model(...)`, `model.fit()`, `model.get_incremental_outcome()`, `model.optimize_budget()`, `model.plot_roi()`, `meridian.validate_data()`, parámetros `num_chains`/`num_warmup`/`num_samples`/`batch_size`/`prior_scale`, `geo_column=` como parámetro de constructor. Usa siempre el API real documentado en `references/api-reference.md` y verificalo contra los ejemplos de `references/notebooks-demos.md`.

## Flujo de trabajo (7 fases)

```
1. PREPARACIÓN (pre-modeling)
   ├── Recolectar datos: KPI semanal por geografía (2-3 años)
   ├── Preparar medios: impresiones + gasto por canal, geo, semana
   ├── Preparar controles: estacionalidad, eventos, GQV para SEM
   ├── EDA: verificar correlaciones, VIF, varianza del KPI
   └── Evaluar cantidad de datos vs. número de parámetros

2. ESPECIFICACIÓN DEL MODELO
   ├── Elegir tipo de prior: 'roi' si hay experimentos, 'contribution' si KPI no monetario
   ├── Calibrar priors: lognormal_dist_from_mean_std() con valores de experimentos/benchmarks
   ├── Configurar knots: enable_aks=True (recomendado) o valor fijo
   ├── Configurar max_lag: 8 semanas (default), ajustar si el canal tiene efectos largos
   └── Decidir national vs. geo model

3. AJUSTE DEL MODELO
   ├── mmm.sample_posterior(n_chains=4, n_adapt=1000, n_burnin=1000, n_keep=1000)
   ├── Verificar convergencia: R-hat < 1.2 para todos los parámetros
   └── GPU recomendada (T4 mínimo)

4. DIAGNÓSTICO POST-MODELADO
   ├── Health Score: objetivo ≥ 90
   ├── PPP (posterior predictive p-value): debe ser ≥ 0.05
   ├── P(baseline < 0): debe ser < 0.2
   ├── Shift prior→posterior: verificar que el modelo aprende de los datos
   └── Curvas de Hill/Adstock: prior vs. posterior coherentes

5. RESULTADOS E INTERPRETACIÓN
   ├── ROI por canal con intervalos creíbles al 90%
   ├── mROI: identificar canales sobre/bajo-invertidos (mROI<1 → sobreinvertido)
   ├── Curvas de respuesta: identificar puntos de saturación
   └── Waterfall de contribuciones: baseline vs. canales individuales

6. OPTIMIZACIÓN DE PRESUPUESTO
   ├── Definir escenario: presupuesto fijo o flexible (ROI/mROI objetivo)
   ├── Establecer restricciones por canal (ej. ±50% del histórico)
   ├── Interpretar: círculo (actual) vs. cuadrado (óptimo) en curvas de respuesta
   └── Para R&F: calcular frecuencia óptima primero (use_optimal_frequency=True)

7. ACTUALIZACIÓN PERIÓDICA
   ├── Frecuencia: trimestral o anual
   ├── Agregar datos nuevos al histórico (no modelar solo los nuevos)
   ├── Usar AKS Hybrid para consistencia de nudos entre actualizaciones
   └── Documentar cambios en priors y las razones de negocio
```

## Clases principales del API

| Clase | Módulo | Propósito |
|---|---|---|
| `DataFrameInputDataBuilder` | `meridian.data.data_frame_input_data_builder` | Construye `InputData` desde DataFrames con API fluent (`.with_kpi()`, `.with_media()`, `.with_controls()`...) |
| `InputData` | `meridian.data` | Contenedor de todos los tensores de entrada (KPI, media, controles, población) |
| `ModelSpec` | `meridian.model.spec` | Configuración del modelo (nudos, lags, priors, tipo de distribución) |
| `PriorDistribution` | `meridian.model.prior_distribution` | Distribuciones a priori para todos los parámetros del modelo |
| `Meridian` | `meridian.model.model` | Clase principal: carga datos + spec y ejecuta `sample_prior()`/`sample_posterior()` |
| `Analyzer` | `meridian.analysis.analyzer` | ROI, mROI, resultado incremental, curvas de respuesta |
| `BudgetOptimizer` | `meridian.analysis.optimizer` | Optimización de presupuesto (fijo, o flexible con ROI/mROI objetivo) |
| `Summarizer` | `meridian.analysis.summarizer` | Exporta resultados a DataFrames/HTML para reporting |
| `ModelDiagnostics` / `ModelFit` | `meridian.analysis.visualizer` | Gráficos diagnósticos: prior vs. posterior, Adstock, Hill, bondad de ajuste |
| `ModelReviewer` | `meridian.analysis.review` | Health checks automáticos y Health Score (0-100) |

## When to Use

- Diseñar o revisar la especificación de un modelo Meridian (priors, nudos, Adstock/Hill, national vs. geo).
- Depurar problemas de convergencia MCMC (R-hat alto, health score bajo, baseline negativo).
- Interpretar ROI/mROI, curvas de respuesta o resultados de optimización de presupuesto.
- Adaptar uno de los notebooks/demos oficiales (Getting Started, R&F, MLflow, Full Funnel) a un caso propio.
- Aplicar Meridian a un caso de negocio real (medición de campaña, cross-channel, geo multi-país).
- Comparar Meridian con otros enfoques de atribución (ver skill `marketing-attribution` para MTA/Shapley/incrementalidad).

## References

Carga la referencia que corresponda a la tarea — mantén este archivo ligero y consulta el detalle bajo demanda:

- **[references/api-reference.md](references/api-reference.md)** — instalación, requisitos de versión, arquitectura del paquete, historial de cambios, y referencia detallada de `InputData`, `ModelSpec`, `PriorDistribution`, `Analyzer`, `BudgetOptimizer` y mensajes proto. Leer al construir o depurar código Meridian.
- **[references/notebooks-demos.md](references/notebooks-demos.md)** — Getting Started (TF/JAX), demo de Reach & Frequency, simulación de datos R&F, ROI/mROI y curvas de respuesta, integración MLflow, y Full Funnel. Leer al adaptar un notebook oficial.
- **[references/conceptual-guides.md](references/conceptual-guides.md)** — guías conceptuales oficiales completas: pre-modelado, especificación matemática, nudos/priors/adstock, national vs. geo, health checks y health score, interpretación de resultados, optimización, planificación de escenarios, depuración y actualización del modelo. Leer para entender el "por qué" detrás de un parámetro o resultado.
- **[references/wpp-context.md](references/wpp-context.md)** — patrones de aplicación práctica (medición de campaña, optimización cross-channel, geo multi-país, troubleshooting, integración con CausalImpact/Looker Studio, best practices) con código usando el API real. Leer para trabajo aplicado a un caso de cliente.

## Scope & Limitations

**Esta skill cubre:**
- Especificación, ajuste, diagnóstico e interpretación de modelos Meridian (bayesiano, MCMC).
- Optimización de presupuesto con y sin Reach & Frequency.
- Adaptación de los notebooks/demos oficiales del repo `google/meridian`.
- Casos de uso y troubleshooting aplicados a un cliente concreto.

**Esta skill NO cubre:**
- Modelos de atribución multi-touch (MTA), Shapley values, o tests de incrementalidad/holdout — ver skill `marketing-attribution`.
- Análisis de impacto causal de una intervención puntual (campaña, lanzamiento) sobre una serie temporal — ver skill `causal-impact`.
- Analítica de eventos/atribución en GA4, Google Ads o Meta Ads a nivel de plataforma — ver skills `ga4-analyst`, `google-ads-analyst`, `meta-ads-analyst`.

## Integration Points

| Skill | Integración | Flujo de datos |
|-------|-------------|----------------|
| `marketing-attribution` | Alternativa/complemento: MTA para optimización táctica, MMM (Meridian) para asignación estratégica de presupuesto | Resultados de ROI/mROI de Meridian pueden contrastarse con iROAS de incrementalidad |
| `causal-impact` | Complementario: CausalImpact para medir el efecto de una campaña puntual; Meridian para el mix completo de medios en el tiempo | Un lift medido con CausalImpact puede usarse como prior informativo (`roi_m`) en Meridian |
| `data-analyst` / `data-scientist` | Preparación de datos (EDA, VIF, limpieza) previa a construir `InputData` | Datasets validados alimentan `DataFrameInputDataBuilder` |

> **Nota de origen:** el contenido técnico de esta skill proviene de una investigación exhaustiva (repo GitHub, referencia proto, notebooks oficiales, y toda la documentación `developers.google.com/meridian/docs/`) realizada en septiembre de 2026, con verificación cruzada del API real contra ejemplos de código fuente y notebooks — no se generó ningún fragmento de código por plausibilidad.
