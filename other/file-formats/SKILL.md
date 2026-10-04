---
name: file-formats
description: >
  Lectura y escritura multi-formato con Pandas — CSV, Excel, Parquet, JSON,
  Feather. Elegí el formato correcto para cada caso.
  Trigger: Cuando necesitás leer o guardar datos en distintos formatos, convertir entre formatos, o elegir el formato correcto para tu caso.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T1-ultra-fast
---

# Skill: file-formats

Multi-formato. Cada formato tiene un propósito — elegí bien.

## Trigger

- Te pasaron datos en un formato que no conocés
- Necesitás convertir entre formatos
- Querés elegir el formato óptimo para velocidad, tamaño o compatibilidad
- Un CSV de 5GB no entra en memoria y necesitás alternativas

## Workflow LEND

```
1. ANALIZAR
   ├── Origen: ¿qué formato tenés? ¿es tabular, anidado, texto?
   ├── Destino: ¿quién va a usar estos datos? ¿qué formato necesita?
   ├── Volumen: ¿KB, MB, GB? define la urgencia de optimizar
   └── Presupuesto: tiempo de carga vs espacio en disco

2. OFRECER (Menú del Senior)
   ├── A) CSV — universal, cualquiera lo abre. Lento y grande.
   ├── B) Parquet — rápido, comprimido, con schema. Ideal para pipelines.
   └── C) Feather — rapidísimo (C++ en backend). Para datos intermedios.

3. ELEGIR → confirmación

4. HACER
   ├── CSV: pd.read_csv('archivo.csv', parse_dates=['fecha'], dtype={'col': 'int32'})
   ├── Parquet: pd.read_parquet('archivo.parquet') / df.to_parquet('archivo.parquet')
   ├── Feather: pd.read_feather('archivo.feather') / df.to_feather('archivo.feather')
   ├── Excel: pd.read_excel('archivo.xlsx', sheet_name='Sheet1')
   ├── JSON: pd.read_json('archivo.json') / json_normalize para anidados
   └── Conversión entre formatos con Pandas (read → to)

5. VERIFICAR
   ├── Los datos se leen sin errores
   ├── Los tipos se infirieron correctamente
   └── El tamaño del archivo es razonable para el formato elegido
```

## Patrones

- **CSV para compartir**: cualquiera lo abre, pero no tiene schema y es lento
- **Parquet para pipelines**: comprimido, con schema, columnar. Lectura rápida de subsets.
- **Feather para datos intermedios**: más rápido que Parquet, pero solo para Pandas/R
- **Optimizar tipos**: `dtype={'col': 'int32'}` en read_csv reduce memoria ~50%
- **JSON para APIs**: Pandas json_normalize para datos anidados

## Anti-patrones

- ❌ CSV para datos grandes — 5GB de CSV es invivible. Usá Parquet.
- ❌ Excel para automatización — es lento, frágil, no scalable
- ❌ No especificar tipos al leer CSV — Pandas infiere, pero a veces se equivoca
- ❌ JSON anidado sin json_normalize — te perdés en diccionarios anidados
