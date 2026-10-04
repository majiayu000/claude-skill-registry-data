---
name: c5-academic-peer-reviewer
display_name: "Simulador de Revisión Académica por Pares"
description: "Simulación de revisión por pares académica para papers científicos. Genera dictámenes estructurados (Accept / Major Revision / Minor Revision / Reject) en 4 dimensiones. Dispara con \"peer review\", \"academic reviewer\", \"revisar paper\", \"auditoría de paper\", \"dictamen académico\"."
---

# Skill: C5 Academic Peer Reviewer

Este protocolo simula la evaluación crítica desapiadada de un revisor senior (Area Chair) de conferencias de primer nivel para identificar debilidades antes del envío formal.

---

## 1. Dimensiones de Evaluación

1. **Originalidad y Novedad Técnica:**
   - ¿La contribución propone una mejora sustancial o es un ajuste incremental sin novedad matemática/algorítmica?
2. **Corrección Técnica y Rigor:**
   - Auditoría de demostraciones matemáticas, asunciones simplificadoras ocultas y posibles fallas en las deducciones.
3. **Claridad y Estructura:**
   - Evaluación de la narrativa, calidad visual de figuras, explicaciones intuitivas y notación consistente.
4. **Reproducibilidad y Validez Empírica:**
   - Verificación de baselines comparativos, semillas aleatorias, tamaño de muestra y disponibilidad de código/datos.

---

## 2. Estructura del Dictamen de Revisión

- **Summary of the Paper:** Breve resumen del artículo sin sesgo.
- **Strengths (Puntos Fuertes):** 3-5 viñetas sobre los aportes reales.
- **Weaknesses & Actionable Concerns (Debilidades Principales):**
  - *Major Revisions:* Puntos críticos que invalidan el resultado si no se solucionan.
  - *Minor Revisions:* Correcciones tipográficas, adición de referencias o aclaraciones de formato.
- **Final Rating & Confidence:** Accept (8-10), Weak Accept (6-7), Borderline (5), Reject (1-4).
