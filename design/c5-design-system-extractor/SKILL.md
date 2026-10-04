---
name: c5-design-system-extractor
display_name: "Extractor de Sistemas de Diseño e Interfaz UI"
description: "Extracción de sistemas de diseño, tokens de interfaz (colores, tipografía, espaciado) y generación de código Vanilla CSS/React desde capturas de pantalla de UI. Dispara con \"design system\", \"extraer UI\", \"design system builder\", \"ui screenshot to code\", \"tokens de diseño\"."
---

# Skill: C5 Design System Extractor

Este protocolo descompila capturas de pantalla de interfaces de usuario para extraer sistemas de diseño coherentes y generar código listo para producción siguiendo las guías estéticas de CORTEX.

---

## 1. Pipeline de Extracción y Síntesis UI

1. **Extracción de Tokens de Diseño (Decompilation):**
   - **Paleta de Colores:** Extraer primarios, secundarios, fondos (dark/light), acentos HSL y gradientes.
   - **Escala Tipográfica:** Identificar familias de fuentes, pesos (`font-weight`), tamaños (`font-size`) y alturas de línea (`line-height`).
   - **Escala de Espaciado y Radio:** Mapear padding/margin y `border-radius` (4px, 8px, 12px, etc.).
   - **Efectos y Sombras:** Detectar `box-shadow`, elevaciones y capas de glassmorphism (`backdrop-filter`).

2. **Generación del Design System:**
   - Crear el archivo CSS de tokens (`tokens.css` o `index.css`) definiendo variables CSS nativas (`:root`).
   - Construir componentes atómicos (Botones, Cards, Modales, Badges) reutilizables.

---

## 2. Invariantes de Calidad Estética CORTEX

- **Cero Paletas Genéricas:** Uso exclusivo de paletas adaptadas HSL de alta armonía.
- **Transiciones y Micro-animaciones:** Efectos `:hover` y `:active` fluidos.
- **Tipografía Moderna:** Integración nativa con Google Fonts (Inter, Outfit, Fira Code).
