---
name: notebook-integration
description: >
  Integración con Jupyter Notebooks — workflow, buenas prácticas,
  magia de IPython y tips para análisis reproducible en .ipynb.
  Trigger: Cuando trabajás con Jupyter, .ipynb, notebooks, o necesitás ejecutar código en celdas.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: notebook-integration

Jupyter notebooks hechos como la gente. No son archivos basura.

## Trigger

- Trabajás en un .ipynb para análisis exploratorio
- Necesitás integrar código Python con visualizaciones inline
- Querés presentar resultados en formato reproducible
- Vas a commitear un notebook y no querés que sea un bardo

## Workflow LEND

```
1. ANALIZAR
   ├── Tipo: exploratorio (EDA), tutorial, o reporte
   ├── Estructura: celdas de texto y código, orden lógico
   ├── Dependencias: ¿qué librerías necesita el notebook?
   └── Versión: ¿notebook clásico (.ipynb) o Quarto (.qmd)?

2. OFRECER (Menú del Senior)
   ├── A) Notebook clásico — Jupyter Lab, .ipynb, análisis interactivo
   ├── B) Quarto — .qmd, texto + código, mejor versionado
   └── C) Script + nbconvert — .py con # %% celdas, convertido a notebook

3. ELEGIR → confirmación

4. HACER
   ├── Celda 1: imports (TODO en una celda, ordenadas: stdlib → externas → locales)
   ├── Celdas de texto: markdown con contexto, no solo código
   ├── Outputs: no imprimir DataFrames de 1000 filas — .head() o .sample()
   ├── Gráficos inline: %matplotlib inline o plotly.io.renderers.default = "notebook"
   ├── Limpiar: restart kernel + run all antes de commitear
   └── Outputs: si es para Git, limpiar outputs con nbstripout o Quarto

5. VERIFICAR
   ├── Run all pasa sin errores
   ├── Los outputs son los esperados
   └── El notebook se entiende sin ejecutarlo (texto + resultados)
```

## Patrones

- **Run all antes de commitear**: si no corre de principio a fin, no es reproducible
- **Markdown entre celdas de código**: el notebook debe contar una historia
- **Imports ordenados**: stdlib, externas, locales. Una celda, todas juntas.
- **nbstripout para Git**: no committear outputs de 10MB en el repo
- **Quarto > .ipynb**: mejor versionado, más flexible

## Anti-patrones

- ❌ Notebooks sin markdown — solo celdas de código sin contexto
- ❌ Outputs de 1000 filas en el notebook — usá .head() o .sample()
- ❌ Commitear notebooks con outputs sucios — outputs de errores, warnings, prints al pedo
- ❌ Celdas en desorden — imports mezclados, funciones definidas donde se usan
- ❌ No limpiar estado — restart kernel y correr todo de nuevo antes de entregar
