---
name: executive-report-template
description: "Estructura HTML, metricas y escala de madurez para el reporte ejecutivo de certificacion QA."
---

# Executive Report Template Skill

Template para generar el reporte HTML ejecutivo de certificacion QA.

## Metricas del Dashboard

| Metrica | Calculo |
|---------|---------|
| **Total Casos** | Cantidad de archivos `Evidencia-TC-*.html` |
| **Casos PASS** | Evidencias con resultado global PASS |
| **Casos FAIL** | Evidencias con resultado global FAIL |
| **Nivel de Madurez** | `(PASS / Total) * 100` redondeado a entero |

## Escala de Madurez

| Rango | Clasificacion | Color | CSS Class |
|-------|--------------|-------|-----------|
| >= 90% | Excelente | #28a745 (verde) | maturity-excellent |
| >= 70% | Bueno | #007bff (azul) | maturity-good |
| >= 50% | Regular | #ffc107 (amarillo) | maturity-regular |
| < 50% | Critico | #dc3545 (rojo) | maturity-critical |

## Estructura del Reporte HTML

1. **Header**: Gradiente purpura `linear-gradient(135deg, #667eea, #764ba2)`, titulo, nombre de app, fecha
2. **Dashboard**: 4 cards (Total, PASS, FAIL, Madurez %) en grid de 4 columnas
3. **Barra de Madurez**: Progress bar con porcentaje y clasificacion, color segun escala
4. **Detalle por TC**: Tabla con cada test case y su resultado (ID, nombre, tipo, pasos pass/fail, resultado)
5. **Problemas**: Cards de problemas con severidad (solo si hay FAILs)
   - Alta (funcionalidad principal), Media (alternativa), Baja (cosmetico)
   - Cada card: TC, paso fallido, esperado vs obtenido, severidad
6. **Conclusiones**: Resumen objetivo basado en datos
7. **Footer**: Timestamp

## Estilos CSS (inline)
- Fuente: system-ui, -apple-system, sans-serif
- Max-width: 1200px, centrado, responsive
- Cards del dashboard: background white, border-radius 12px, box-shadow
- Colores de cards: Total #6c757d, PASS #28a745, FAIL #dc3545, Madurez segun escala
- Progress bar: height 30px, border-radius 15px, transicion de color segun porcentaje
- Tabla de detalle: striped rows, hover effect
- Problemas: cards con borde izquierdo de color segun severidad

## Ejemplo de Dashboard Card

```html
<div class="dashboard-card card-pass">
  <div class="card-number">10</div>
  <div class="card-label">PASS</div>
</div>
```

## Ejemplo de Progress Bar

```html
<div class="maturity-bar-container">
  <div class="maturity-bar maturity-good" style="width: 83%">83% - Bueno</div>
</div>
```
