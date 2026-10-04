---
name: data-visualization
description: >
  Gráficos profesionales con Matplotlib, Seaborn, Plotly — del exploratorio
  al publicable. Elige el gráfico correcto para cada historia.
  Trigger: Cuando necesitás crear gráficos, visualizar datos, o generar charts para análisis o presentaciones.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: data-visualization

Visualización que comunica. No es decoración, es análisis.

## Trigger

- Tenés datos y querés ver patrones visualmente
- Necesitás un gráfico para un informe o presentación
- Querés explorar distribuciones, correlaciones o tendencias
- El heatmap de correlación no te dice lo que necesitás

## Workflow LEND

```
1. ANALIZAR
   ├── Tipo de dato: numérico, categórico, temporal, geográfico
   ├── ¿Qué querés mostrar? distribución, comparación, tendencia, relación, composición
   ├── ¿Quién lo ve? vos (exploratorio) vs cliente (presentación)
   └── Cardinalidad: ¿cuántas categorías? ¿cuántos puntos?

2. OFRECER (Menú del Senior)
   ├── A) Exploratorio rápido — histogramas + boxplots + scatter matrix con Seaborn
   ├── B) Dashboard interactivo — Plotly con hover, zoom, tooltips
   └── C) Publicable — Matplotlib con estilo personalizado, tipografía, colores corporativos

3. ELEGIR → confirmación

4. HACER
   ├── Elegí el tipo de gráfico según la historia:
   │   Distribución → histograma + KDE
   │   Comparación → boxplot o violín
   │   Tendencia → línea + área
   │   Relación → scatter + regresión
   │   Composición → stacked bar o pie (solo si son <= 5 categorías)
   ├── Configurá: colores, etiquetas, título, leyenda, tamaño
   ├── Si es interactivo: Plotly, hover info, zoom, tooltips
   ├── Si es publicable: matplotlib + seaborn + estilo consistente
   └── Guardá en alta calidad (300 DPI para informes)

5. VERIFICAR
   ├── El gráfico comunica sin necesidad de explicación
   ├── Los ejes están etiquetados, las unidades son claras
   └── No hay elementos decorativos que distraigan
```

## Patrones

- **Un gráfico, una historia**: no meter 10 variables en un solo chart
- **Color con propósito**: no decorativo. Usá paletas sequentiales (numérico) o categóricas (grupos)
- **Menos es más**: sacá bordes, fondos grises, gridlines innecesarios
- **Tipo correcto**: barras para comparar, líneas para tendencias, scatter para relaciones
- **Accessibilidad**: daltonismo → viridis o cividis, no rainbow

## Anti-patrones

- ❌ Pie charts con 10 categorías — es ilegible. Usá barras.
- ❌ 3D charts — salvo contadas excepciones, son más confusos que útiles
- ❌ Dual axis engañoso — dos escalas diferentes en el mismo gráfico mienten
- ❌ Rainbow colormap — no es perceptualmente uniforme ni daltónico-friendly
- ❌ No etiquetar ejes — "sé qué significa" no es una excusa
