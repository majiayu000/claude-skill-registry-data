---
name: portal-ux-deliverables
description: Assemble, verify and submit the course deliverables A1-A5 for the Portal Centralizado de Datos Financieros. Use when writing or laying out an activity document, applying the A1 rubric breakdown, running the excellence checklist, absorbing a newly published rubric (A2-A5 protocol), or citing the 10 anchor papers in APA format.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal UX Deliverables Skill

Cubre la producción documental del EPIC UX (el documento integrador de cada actividad A1–A5). La investigación de campo vive en `portal-ux-research`; aquí vive el documento que la escuela califica. Fuente de verdad: `context/planeacion_proyecto.md` §2, §24, §25.2.

## Rules — NON-NEGOTIABLE

- Nombre de archivo exacto: **"Entregable Actividad N_equipo_8"** (N = 1..5), formato **PDF**, entrega por **Canvas**. Cuenta para todo el Project Group.
- **Deadline interno: sábado 20:00** anterior a cada entrega dominical (buffer de 24 h). Integración final: Arthur.
- Toda cifra respeta la regla de honestidad metodológica (encuesta propia, fuente citada o estimación declarada — ver `portal-ux-research`).
- Referencias en formato **APA**; estilos, paginación e identidad visual consistentes entre A1 y A5.
- Prosa en español neutro, sin emojis. Los cuadrantes de mapas de empatía se rotulan en inglés (exigencia de rúbrica).
- Al publicarse una rúbrica A2–A5: aplicar el protocolo de absorción (abajo) **antes** de cualquier trabajo de esa actividad.

## Calendario de entregas

| Actividad | Tema | Entrega | Rúbrica | Sprint |
|-----------|------|---------|---------|--------|
| A1 | Definición del producto e instrumentos de investigación | dom 26-jul-2026 | Publicada (15 pts) | S1 |
| A2 | Escenarios y Journey Maps | dom 2-ago-2026 | Pendiente | S2 |
| A3 | Análisis competitivo y Arquitectura de Información | dom 9-ago-2026 | Pendiente | S3 |
| A4 | Interfaces de alta fidelidad | dom 16-ago-2026 | Pendiente | S4 |
| A5 | Entrega final | dom 23-ago-2026 | Pendiente | S5 |

## Rúbrica A1 — desglose exacto (§2.2)

Fuente: `docs/general/semana_1/rubrica_tarea_1_UI.pdf`.

| # | Apartado | Peso | Modalidad | Puntos (de 15) |
|---|----------|------|-----------|----------------|
| 1 | Portada con nombres de los integrantes | 2 % | Equipo | 0.30 |
| 2 | Introducción | 3 % | Equipo | 0.45 |
| 3 | Identificación de la audiencia | 5 % | Equipo | 0.75 |
| 4 | Descripción general del problema | 20 % | Equipo | 3.00 |
| 5 | Definición del producto digital | 20 % | Equipo | 3.00 |
| 6 | Dos mapas de empatía por integrante (6 en total) | 25 % | Individual | 3.75 |
| 7 | Dos user personas por integrante (6 en total) | 25 % | Individual | 3.75 |

Elementos obligatorios por sección:

- **Audiencia**: clientes y necesidades; pain points; demografía (edad, sexo, ubicación); intereses; dónde se conectan; **herramienta de investigación utilizada y sus resultados**.
- **Problema**: identificación; cuantificación (datos de encuesta E-06/E-07); impacto; solución. **≥2 elementos visuales** (diagrama de silos antes/después + gráfica de encuesta).
- **Producto digital**: tipo (plataforma web); características y beneficios (tabla módulo→perfil→beneficio §6.1; patrones UX 2026 §6.2).
- **Mapas de empatía**: cuadrantes "Says", "Thinks", "Does", "Feels" con observaciones clave basadas en la información recopilada.
- **Personas**: foto + básicos (nombre, edad, sexo, ocupación); antecedentes; objetivos; pain points; comportamientos; frase/cita.

## Checklist de excelencia A1 (§24) — con responsables

| Rubro (peso) | Banda "Completo" | Extra de excelencia | Responsable |
|--------------|------------------|---------------------|-------------|
| Portada (2 %) | Nombres de los 3 integrantes; curso/equipo 8 | Identidad visual del producto reutilizable en A2–A5 | Alexandro |
| Introducción (3 %) | Qué se hizo y organización del documento | Párrafo de método: instrumentos + n + fechas de campo | Jacqueline |
| Audiencia (5 %) | Todos los elementos de §2.2, herramienta y resultados | Gráficas de encuesta; tabla 3 perfiles (§5.1); nota "roles no excluyentes" con dato E-08 | Jacqueline |
| Problema (20 %) | Identificación, cuantificación, impacto, solución; visuales | Diagrama silos antes/después; horas/semana de la encuesta; impacto por perfil | Arthur |
| Producto (20 %) | Tipo + características y beneficios | Tabla módulo→perfil→beneficio; patrones UX 2026 con citas; mockup conceptual | Alexandro |
| 6 mapas (25 %) | 4 cuadrantes Says/Thinks/Does/Feels | Citas textuales reales en "Says"; plantilla uniforme | Cada quien ×2 |
| 6 personas (25 %) | Foto, básicos, antecedentes, objetivos, pains, hábitos, frase | Conexión persona↔perfil↔dato de campo; fotos IA consistentes | Cada quien ×2 |
| Formato | PDF "Entregable Actividad 1_equipo_8" por Canvas | Referencias APA; paginación y estilos consistentes | Arthur |

## Protocolo de absorción de rúbricas A2–A5 (§25.2)

Cuando se publique una rúbrica en Canvas:

1. **T+0 h**: leerla completa; volcarla a una tabla criterio→peso→banda "Completo" (mismo formato que la tabla A1 de arriba).
2. **T+1 h**: mapear cada criterio a la historia UX correspondiente del plan; ajustar sus criterios de aceptación provisionales; recalcular SP.
3. **T+1 día**: si excede lo previsto, congelar STRETCH técnicos del sprint en orden **E5 → E4 → E2** hasta cubrir el delta.
4. Registrar el ajuste en `context/planeacion_proyecto.md` (sección de la actividad + registro de cambios) con fecha.

## Referencias APA — los 10 papers ancla (`docs/papers/`)

Citar donde aplique; los archivos llevan prefijo numérico:

1. Bai, J., Zhang, Z., Zhang, J., & Zhu, Z. (2026). *Insight Agents: An LLM-based multi-agent system for data insights*. arXiv:2601.20048.
2. Agarwal, S., Biswal, A., Zeighami, S., Cheung, A., Gonzalez, J., & Parameswaran, A. G. (2026). *Arming data agents with tribal knowledge*. arXiv:2602.13521.
3. Singh, G., Kavehzadeh, P., Xia, J., Fu, X.-Y., Bouvier Tremblay, J., Laskar, M. T. R., Lum, V., & Bhushan TN, S. (2026). *Beyond Text-to-SQL: An agentic LLM system for governed enterprise analytics APIs*. arXiv:2605.21027.
4. Kim, H. J., Khoeurn, S., & Yoon, Y. J. (2026). *A semantic-layer-mediated agent for natural language to SQL over heterogeneous enterprise databases*. arXiv:2606.31041.
5. Sun, Y., Wei, P., & Hsieh, L. B. (2026). *Don't retrieve, navigate: Distilling enterprise knowledge into navigable agent skills for QA and RAG*. arXiv:2604.14572.
6. Jang, J., & Li, W.-S. (2026). *TwinBI: An agentic digital twin for efficient augmented interactions with business intelligence dashboards*. arXiv:2606.13731.
7. Naik, S., Passi, S., Vorvoreanu, M., Saponas, S., & Hall, A. (2026). *"So there's a catch-22 here": How early adopters who build multi-agent LLM systems conceptualize transparency*. arXiv:2606.08323.
8. Bougie, N., Ye, X., Marconi, G. M., & Watanabe, N. (2026). *PerceptUI: LLM agents as human-aligned synthetic users for UI/UX evaluation*. arXiv:2606.05697.
9. Peng, Y.-H., Das, S., Bigham, J. P., & Wu, J. (2026). *Efficient personalization of generative user interfaces*. arXiv:2604.09876.
10. Bachkaniwala, R., Luo, C., So, R., Mahajan, D., & Rong, K. (2026). *Stream2LLM: Overlap context streaming and prefill for reduced time-to-first-token (TTFT)*. arXiv:2604.16395.

## Coherencia A1→A5 como caso de estudio

- La identidad visual (logo/nombre del producto) definida en la portada de A1 reaparece en A2–A5.
- Cada actividad consume artefactos de la anterior: personas (A1) → journeys (A2) → sitemap/taxonomía (A3) → alta fidelidad + pre-validación sintética (A4) → SUS y documento integrador (A5).
- A5 hila todo el proceso como caso de estudio UX (estándar del Grocery Shopping App del curso, superado con producto real y métricas de §22), más video demo de 3 min y presentación final.

## Checklist de cierre por actividad

- [ ] Rúbrica (o criterios provisionales) volcada a tabla y cubierta al 100 %
- [ ] Checklist de excelencia de la actividad verificado con responsables
- [ ] Cifras auditadas contra la regla de honestidad metodológica
- [ ] Referencias APA presentes donde se usa un paper
- [ ] PDF con nombre exacto, estilos consistentes y paginación
- [ ] Subido a Canvas antes del deadline interno (sáb 20:00)

## When NOT to Use This Skill

- Diseñar o ejecutar instrumentos de campo → `portal-ux-research`.
- Pre-validación sintética de interfaces → `portal-synthetic-users`.
- Implementar el prototipo Nuxt que evidencia A4 → skills de frontend.
