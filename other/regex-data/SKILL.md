---
name: regex-data
description: >
  Limpieza de texto con expresiones regulares — extracción, validación y
  transformación de strings en DataFrames.
  Trigger: Cuando necesitás limpiar strings, extraer patrones, o validar formatos en un DataFrame.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: regex-data

Regex para limpieza de datos. Strings sucios → datos limpios.

## Trigger

- Tenés una columna de texto con formatos inconsistentes
- Necesitás extraer emails, teléfonos, fechas o precios de texto sucio
- Hay que validar formatos de entrada (CUIL, CBU, mail)
- Los strings tienen espacios, caracteres raros o typos

## Workflow LEND

```
1. ANALIZAR
   ├── ¿Qué datos de texto necesitás limpiar o extraer?
   ├── ¿Hay un patrón claro? (regex detectable)
   ├── Volumen: ¿100 filas o 100k filas? (performance importa)
   └── ¿Qué hacer con los que no matchean? ¿descartar, flaggear, imputar?

2. OFRECER (Menú del Senior)
   ├── A) Regex directo — .str.extract(), .str.replace(), .str.contains()
   ├── B) Pattern compilado — re.compile() + apply(), más rápido en volumen
   └── C) Fuzzy matching — Levenshtein / difflib cuando no hay patrón exacto

3. ELEGIR → confirmación

4. HACER
   ├── .str.strip().str.lower() como prerrequisito
   ├── Extraer: df['col'].str.extract(r'(\d{4}-\d{2}-\d{2})')
   ├── Reemplazar: df['col'].str.replace(r'\s+', ' ', regex=True)
   ├── Validar: df['col'].str.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$')
   ├── Pattern compilado: re.compile(r'...').findall() para apply performance
   └── Fuzzy: difflib.get_close_matches() o thefuzz para typos

5. VERIFICAR
   ├── Las extracciones son correctas (verificar muestra manual)
   ├── No se perdieron filas válidas por un regex mal escrito
   └── Los casos borde (None, NaN, strings vacíos) se manejan
```

## Patrones

- **Raw strings**: `r"patrón"` para evitar escaping de backslashes
- **Compilar para performance**: `re.compile()` + `apply()` para >10k filas
- **Named groups**: `(?P<nombre>patrón)` para extraer múltiples campos
- **Validar vs extraer**: match() para validación, extract() para extracción
- **Cuidado con greedy**: `*` y `+` son greedy. Usá `*?` y `+?` para non-greedy.

## Anti-patrones

- ❌ Regex sin raw string — `\d` en vez de `r"\d"` rompe la expresión
- ❌ No compilar para grandes volúmenes — 100k filas con regex inline es lento
- ❌ Regex demasiado complejo — si el regex es ilegible, partilo en pasos
- ❌ No testear casos borde — None, NaN, strings vacíos, caracteres especiales
- ❌ Greedy sin querer — `.*` captura todo hasta el último match, no el primero
