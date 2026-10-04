---
name: c5-weighted-decision-matrix
display_name: "Matriz de Decisión Ponderada y Estimación PERT"
description: "Matrices de decisión multicriterio ponderadas para selección tecnológica y evaluación de proveedores, análisis de sensibilidad y estimación formal de esfuerzo PERT con intervalos de confianza. Dispara con \"weighted scorer\", \"matriz de decisión\", \"pert estimation\", \"estimación de proyectos\", \"evaluación tecnológica\"."
---

# Skill: C5 Weighted Decision Matrix & PERT Estimation

Este protocolo proporciona soporte cuantitativo para la toma de decisiones complejas, selección de arquitectura/proveedores y estimación probabilística de proyectos.

---

## 1. Módulos de Cálculo

1. **Matriz Multicriterio Ponderada (Weighted Scoring):**
   - Definición de criterios $C_1, C_2, \dots, C_k$ con pesos $w_i \in [0, 1]$ tales que $\sum w_i = 1$.
   - Puntuación $s_{i,j} \in [1, 10]$ por alternativa y cálculo del score ponderado $S_j = \sum w_i \cdot s_{i,j}$.
   - **Análisis de Sensibilidad:** Prueba de variación de pesos para verificar la estabilidad de la opción ganadora.

2. **Estimación PERT (Program Evaluation and Review Technique):**
   - Para cada paquete de trabajo, definir:
     - $O$: Valor optimista.
     - $M$: Valor más probable (Most Likely).
     - $P$: Valor pesimista.
   - **Tiempo Esperado:** $E = \frac{O + 4M + P}{6}$.
   - **Varianza:** $\sigma^2 = \left(\frac{P - O}{6}\right)^2$.

---

## 2. Salida Estructurada

Tabla resumen con matriz de decisión, gráfico de sensibilidad en texto/SVG e intervalo de confianza de estimación PERT al 95%.
