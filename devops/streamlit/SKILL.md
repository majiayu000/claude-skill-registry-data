---
name: streamlit
description: >
  Dashboards interactivos con Streamlit — de 0 a app en minutos. Visualizaciones
  en vivo, filtros, carga de archivos y despliegue.
  Trigger: Cuando necesitás crear dashboards, apps web interactivas, o visualizar datos con Streamlit.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "4.0"
  model_tier: T2-fast
---

# Skill: streamlit

Dashboards interactivos en minutos. De un script de análisis a una app que podés mostrar.

## Trigger

- Querés que otros puedan interactuar con tus datos
- Necesitás una UI rápida para un prototipo
- Un dashboard en Streamlit reemplazaría 10 correos con Excel adjuntos
- Querés mostrar resultados a alguien no técnico

## Workflow LEND

```
1. ANALIZAR
   ├── ¿Qué necesita ver el usuario? tablas, gráficos, filtros
   ├── ¿Quién lo usa? técnico (más controles) o ejecutivo (más simple)
   ├── ¿Datos estáticos o en vivo?
   └── ¿Hay que autenticar o es público?

2. OFRECER (Menú del Senior)
   ├── A) MVP — 1 archivo .py, carga de CSV, gráficos básicos, filtra
   ├── B) Modular — múltiples páginas, caché, inputs complejos
   └── C) Producción — auth, deploy en Cloud Run/Streamlit Cloud, logging

3. ELEGIR → confirmación

4. HACER
   ├── Layout: st.sidebar para controles, st.columns para gráficos
   ├── Cache: @st.cache_data para no recargar datos en cada interacción
   ├── Gráficos: Plotly (interactivo) o Altair (declarativo)
   ├── Carga de datos: st.file_uploader para CSV, st.dataframe para tablas editables
   ├── Sesión: st.session_state para estado entre re-runs
   └── Deploy: requirements.txt + runtime.txt + Dockerfile o Streamlit Cloud

5. VERIFICAR
   ├── La app carga sin errores
   ├── Los filtros actualizan los gráficos correctamente
   └── La caché funciona (segundo load es más rápido)
```

## Patrones

- **st.cache_data**: siempre cachear lectura de datos. Sin caché, cada interacción recarga todo.
- **st.session_state**: para estado persistente entre re-runs (lo que el usuario seleccionó).
- **st.columns > st.beta_columns**: API estable desde 1.18.
- **Plotly > Matplotlib**: zoom, hover, tooltips nativos en Streamlit.
- **Requerimientos explícitos**: requirements.txt con versiones fijas para deploy.

## Anti-patrones

- ❌ No cachear datos — cada click recarga el CSV entero
- ❌ Gráficos sin interactividad — Matplotlib estático mata el propósito de Streamlit
- ❌ Sin manejo de errores — un archivo mal formateado rompe toda la app
- ❌ Layout desordenado — todo en una columna sin estructura
- ❌ Hardcodear rutas de archivos — `st.file_uploader` o config, nunca rutas fijas
