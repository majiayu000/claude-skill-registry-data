---
name: data-analysis
description: >
  Análisis estadístico de datasets con Pandas y NumPy — explora, correlaciona,
  testea hipótesis y extrae conocimiento no obvio.
  Trigger: Cuando necesitás analizar datasets, explorar variables, buscar patrones o correlaciones, o hacer análisis exploratorio (EDA).
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T3-balanced
---

# Skill: data-analysis

Análisis con rigor estadístico. No describir tablas — extraer conocimiento que no sea obvio.

## Trigger

- Cargaste un dataset y necesitás entender qué hay adentro
- Buscás correlaciones, tendencias o patrones ocultos
- Vas a presentar resultados y necesitás estar seguro de lo que decís
- Te pidieron un análisis exploratorio (EDA) completo

## Workflow LEND

```
1. ANALIZAR
   ├── Data Leakage Check: ¿hay variables con información del target?
   │   Si las hay → frená todo y avisale al Míster
   ├── Distribución y sesgo: skewness, curtosis
   │   ¿Normal? Shapiro-Wilk (n chico) o inspección visual (n grande)
   ├── Cardinalidad: tipos, nulos, duplicados, valores únicos
   └── Business alignment: ¿esto mueve la aguja del negocio o es ruido?

2. OFRECER (Menú del Senior)
   ├── A) EDA visual profundo — distribución de cada variable + correlaciones + outliers
   ├── B) Test de hipótesis formal — p-values, intervalos de confianza, poder estadístico
   └── C) Reducción de dimensionalidad — PCA/t-SNE/UMAP si hay muchas variables

3. ELEGIR → el usuario confirma camino

4. HACER
   ├── Exploración inicial con profiling (describe, info, isnull, duplicated)
   ├── Visualizaciones: histogramas, boxplots, scatter matrix, heatmap de correlación
   ├── Si hay correlaciones altas → analizar variables intervinientes o paradoja de Simpson
   ├── Correlación != Causalidad: nunca decir "X causa Y" sin experimento
   └── Documentar hallazgos en inglés técnico

5. VERIFICAR
   ├── Los hallazgos son reproducibles (mismos datos = mismo resultado)
   ├── No hay conclusiones basadas en correlaciones espurias
   └── Todo está documentado para el informe final
```

## Patrones

- **Data Leakage Check**: antes de cualquier análisis, verificá que ninguna feature contenga info del futuro o del target
- **Correlación != Causalidad**: correlación alta no implica causalidad. Buscá variables intervinientes.
- **Paradoja de Simpson**: la tendencia general puede revertirse al segmentar por grupos. Siempre segmentá.
- **Business alignment**: si un hallazgo no mueve la aguja del negocio, es ruido. Priorizá lo que importa.
- **Shapiro-Wilk**: para probar normalidad en muestras chicas (< 50). Para muestras grandes, usá inspección visual.
- **Spearman vs Pearson**: Pearson asume linealidad y normalidad. Spearman es rank-based y no asume nada.

## Anti-patrones

- ❌ Decir "X causa Y" solo por correlación alta
- ❌ No verificar leakage — variables con info del futuro inflan métricas
- ❌ Ignorar la paradoja de Simpson — la tendencia general miente
- ❌ Presentar resultados sin contexto de negocio ("esta correlación es 0.8... ¿y?")
- ❌ Hacer EDA sin preguntas de negocio claras — análisis sin dirección = ruido
