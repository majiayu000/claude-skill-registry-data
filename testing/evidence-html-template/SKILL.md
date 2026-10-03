---
name: evidence-html-template
description: "Estructura y estilo del template HTML para reportes de evidencia de ejecucion de test cases. Incluye header, tabla de pasos, badges PASS/FAIL y screenshots embebidos."
---

# Evidence HTML Template Skill

Template para generar reportes HTML de evidencia de ejecucion de test cases con Playwright.

## Estructura del Reporte

### 1. Header
- Gradiente azul: `linear-gradient(135deg, #1a73e8, #0d47a1)`
- Titulo: "Evidencia - {TC-ID}: {Nombre del Test Case}"
- Metadata: fecha, tipo de test, historia asociada

### 2. Informacion del Test Case
Tabla con: ID, nombre, historia asociada (HU), tipo (Happy Path/Negativo/Borde/E2E), prioridad

### 3. Pasos de Ejecucion
Por cada paso:
- Titulo Gherkin (Given/When/Then + descripcion)
- Accion realizada (que se hizo en el navegador)
- Resultado observado (que se vio en la pagina)
- Badge PASS (verde #28a745) o FAIL (rojo #dc3545)
- Screenshot embebido en base64

### 4. Metricas de Rendimiento
- Tiempo total de ejecucion
- Tiempo por paso (si aplica)

### 5. Resultado Final
- Resumen: X/Y pasos PASS
- Badge global PASS o FAIL
- Lista de pasos fallidos (si los hay)

### 6. Footer
- Timestamp de generacion

## Estilos CSS (inline)
- Fuente: system-ui, -apple-system, sans-serif
- Max-width: 1000px, centrado
- Badges: border-radius 12px, padding 4px 12px, font-weight 600
- Screenshots: max-width 100%, border 1px solid #e0e0e0, border-radius 8px
- Pasos: background #f8f9fa, border-left 4px solid (verde para PASS, rojo para FAIL)

## Screenshots
- Embebidos como base64: `<img src="data:image/png;base64,..." />`
- El HTML debe ser SELF-CONTAINED (sin dependencias externas)
- CSS inline en `<style>` tag

## Ejemplo de Paso

```html
<div class="step step-pass">
  <div class="step-header">
    <span class="step-keyword">When</span>
    <span class="step-description">el usuario ingresa un ID valido en el campo de busqueda</span>
    <span class="badge badge-pass">PASS</span>
  </div>
  <div class="step-detail">
    <p><strong>Accion:</strong> Se ingreso "12345678-9" en el input de busqueda y se presiono Enter</p>
    <p><strong>Resultado:</strong> Se muestra la tabla con los datos del contribuyente</p>
    <img src="data:image/png;base64,..." alt="Screenshot del paso" />
  </div>
</div>
```
