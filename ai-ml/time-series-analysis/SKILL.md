---
name: time-series-analysis
description: >
  Análisis de series temporales — tendencia, estacionalidad, forecasting
  con Prophet, statsmodels, y Machine Learning.
  Trigger: Cuando trabajás con datos de fecha/hora, tendencias, estacionalidad, forecasting, o series de tiempo.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T4-reasoning
---

# Skill: time-series-analysis

Series temporales. El tiempo es la dimensión más traicionera de los datos.

## Trigger

- Tus datos tienen una columna de fecha/hora
- Querés saber si hay tendencia, estacionalidad o ciclos
- Necesitás pronosticar valores futuros
- Comparás períodos (mes contra mes, año contra año)

## Workflow LEND

```
1. ANALIZAR
   ├── Frecuencia: diaria, horaria, mensual? ¿es regular o tiene gaps?
   ├── Componentes: tendencia, estacionalidad, residuo
   ├── Estacionariedad: ¿la media y varianza cambian en el tiempo? (Dickey-Fuller)
   └── Outliers temporales: feriados, eventos extraordinarios, errores de medición

2. OFRECER (Menú del Senior)
   ├── A) Descomposición clásica — statsmodels, tendencia + estacionalidad + residuo
   ├── B) Prophet — maneja feriados, change points, outliers. Bueno para negocios.
   └── C) ML-based — LightGBM con features temporales (lag, rolling window, día de semana, mes)

3. ELEGIR → confirmación

4. HACER
   ├── timestamp como índice, freq explícita
   ├── Descomposición: seasonal_decompose o STL (más robusto)
   ├── Test de estacionariedad: ADF (p-value < 0.05 = estacionaria)
   ├── Si no es estacionaria → diferencias o transformación (log, Box-Cox)
   ├── Prophet: df con ds (fecha) e y (valor), feriados del país
   ├── ML: features de calendario + lags + rolling window + diff
   └── Evaluar forecast con MAE, RMSE, MAPE (y siempre contra un baseline naive)

5. VERIFICAR
   ├── El forecast es mejor que un baseline naive (último valor = próximo valor)
   ├── Los residuos son ruido blanco (no hay patrón en los errores)
   └── Los intervals de confianza tienen sentido (no son absurdamente anchos)
```

## Patrones

- **Frecuencia explícita**: `.asfreq('D')` para evitar gaps silenciosos
- **Estacionariedad**: modelos clásicos (ARIMA) requieren series estacionarias. ML no.
- **Prophet para negocios**: maneja automáticamente feriados, change points, outliers
- **Baseline naive**: el forecast del mes siguiente = valor de este mes. Si tu modelo no le gana a eso, no sirve.
- **Cross-validation temporal**: siempre en orden cronológico, nunca aleatorio

## Anti-patrones

- ❌ No fijar la frecuencia — gaps silenciosos sesgan tendencias
- ❌ Modelar sin descomponer primero — no sabés si hay estacionalidad
- ❌ Forecast sin intervalo de confianza — "va a subir" sin rango no es útil
- ❌ Cross-validation aleatoria en tiempo — rompés la estructura temporal
- ❌ Ignorar feriados — "diciembre tiene ventas bajas" porque nadie labura, no porque sea tendencia
