---
name: data-cleaning
description: >
  Limpieza quirúrgica de datos — nulos, outliers, duplicados, tipos e
  inconsistencias. Integridad y reproducibilidad ante todo.
  Trigger: Cuando necesitás limpiar datos, manejar nulos, duplicados, outliers, o preparar datasets crudos para análisis.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: data-cleaning

Limpieza quirúrgica de datos. Nada de parches pedorros.

## Trigger

- El dataset está lleno de nulos, tipos raros o valores inconsistentes
- Hay outliers que pueden sesgar el análisis
- Recibiste un CSV que parece un campo de batalla
- Estás por modelar y necesitás datos confiables

## Workflow LEND

```
1. ANALIZAR
   ├── Null Anatomy: clasificá cada nulo
   │   MCAR (azar total), MAR (relacionado a otra variable), MNAR (no azar)
   │   → Nunca dropna() sin justificar pérdida de información
   ├── Outlier Strategy: IQR o Z-Score robusto (MAD)
   │   → ¿Es un error o un dato real? Si es real → Winsorization, no borrado
   ├── Tipos: verificá que cada columna tenga el tipo esperado
   └── Duplicados: siempre primero, antes de imputar nulos

2. OFRECER (Menú del Senior)
   ├── A) Limpieza agresiva — borrar ruido, ideal para modelos rápidos
   ├── B) Imputación inteligente — KNN o MICE para mantener volumen
   └── C) Flagging & Capping — marcar errores sin sesgar el análisis

3. ELEGIR → el usuario confirma

4. HACER
   ├── Duplicados primero (drop_duplicates antes de imputar)
   ├── Nulos: media (sin outliers), mediana (con outliers), moda (categórica),
   │   ffill (series temporales), o eliminar columna si >50% nulos
   ├── Outliers: IQR (no asume normalidad) vs Z-score (asume normalidad)
   │   Para Z-score robusto: usar MAD (median absolute deviation)
   ├── Strings: strip(), lower(), regex para limpieza de texto
   │   Si hay typos → fuzzy matching con Levenshtein
   ├── Prohibido df.iterrows() — todo vectorizado con Pandas/NumPy
   └── Pipeline reproducible (function que toma datos sucios y devuelve limpios)

5. VERIFICAR
   ├── El pipeline corre sin errores
   ├── No se perdió información valiosa sin justificación
   └── El dataset transformado mantiene la estructura esperada
```

## Patrones

- **Null Anatomy**: no todos los nulos son iguales. MCAR se puede borrar, MAR se imputa, MNAR requiere modelo.
- **Outliers con IQR**: no asume normalidad. Z-score funciona mal con distribuciones asimétricas.
- **Winsorization**: capar outliers en los percentiles 1 y 99 en vez de borrarlos.
- **Vectorizado siempre**: `df['col'] * 2` en vez de `for i in range(len(df))`.
- **Pipeline > Script**: una función que toma data_raw y devuelve data_clean es más testeable y reproducible.

## Anti-patrones

- ❌ `dropna()` sin mirar — si los nulos no son MCAR, estás introduciendo sesgo
- ❌ Imputar todo con la media — si hay outliers, la media está sesgada
- ❌ Borrar outliers solo porque "se ven feos" — si es un dato real, se queda
- ❌ `df.iterrows()` — lento, ilegible, no vectorizado
- ❌ No revisar `dtypes` después de `read_csv` — Pandas a veces se equivoca
- ❌ Asumir que no hay duplicados — una join mal hecha upstream te duplica filas sin aviso
