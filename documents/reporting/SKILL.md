---
name: reporting
description: >
  Generación de reportes profesionales — HTML, PDF, Markdown. Automatizá
  informes con tablas, gráficos y conclusiones.
  Trigger: Cuando necesitás generar un reporte de análisis, exportar resultados a un formato presentable, o automatizar la producción de informes.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: reporting

Reportes profesionales. Que tus análisis no mueran en un notebook.

## Trigger

- Terminaste un análisis y necesitás presentarlo
- Querés automatizar informes periódicos
- Necesitás exportar resultados a PDF, HTML o Markdown
- El cliente quiere algo que pueda leer sin abrir Python

## Workflow LEND

```
1. ANALIZAR
   ├── Audiencia: ¿técnica, ejecutiva, cliente? define el nivel de detalle
   ├── Formato: ¿PDF formal, HTML interactivo, Markdown para GitHub?
   ├── Contenido: tablas, gráficos, conclusiones, recomendaciones
   └── Frecuencia: one-shot o reporte automático recurrente

2. OFRECER (Menú del Senior)
   ├── A) Markdown + Quarto — liviano, versionable, ideal para GitHub
   ├── B) HTML + Jinja2 — templates custom, gráficos embebidos, interactivo
   └── C) PDF con ReportLab — formal, exportable, para clientes

3. ELEGIR → confirmación

4. HACER
   ├── Estructura: resumen ejecutivo → metodología → resultados → conclusiones
   ├── Tablas: Pandas + styler para formato condicional
   ├── Gráficos: Matplotlib/Seaborn con configuración publicable
   ├── Markdown/Quarto: .qmd con código + texto + gráficos
   ├── HTML: Jinja2 template con CSS custom
   └── PDF: ReportLab o WeasyPrint para PDFs desde HTML

5. VERIFICAR
   ├── El reporte se lee bien sin necesidad de ejecutar código
   ├── Los números son consistentes entre tablas y texto
   └── Las conclusiones están justificadas por los datos mostrados
```

## Patrones

- **Resumen ejecutivo primero**: que alguien pueda leer solo la primera página y entender todo
- **Una tabla, un mensaje**: no pongas tablas sin contexto. Cada tabla responde una pregunta.
- **Gráfico publicable**: 300 DPI, leyenda, etiquetas, colores accesibles
- **Reproducible**: el reporte se genera con un comando, no a mano
- **Automático**: si es recurrente, que se genere solo y se mande solo

## Anti-patrones

- ❌ Reportes de 50 páginas que nadie lee — lo importante en las primeras 2 páginas
- ❌ Tablas sin contexto — "acá están los números" no es análisis
- ❌ Gráficos en baja calidad — borrosos, ilegibles en PDF
- ❌ Reportes manuales — si hay que armarlos a mano cada vez, están mal diseñados
- ❌ Sin fecha/versión — "esto es de la semana pasada o del mes pasado?"
