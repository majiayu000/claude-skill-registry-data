---
name: frontend-design
description: Crea y refina frontends web (HTML/CSS/JS) para que resultados clínicos o técnicos queden claros, auditables y listos para reunión, con narrativa ejecutiva, jerarquía visual y controles de lectura rápida.
metadata:
  short-description: Diseño de interfaces para presentaciones clínicas
---

# Frontend Design

## Objetivo

Diseñar artefactos frontend estáticos de alto contraste y baja fricción cognitiva para presentación y revisión clínica:

- convertir reportes densos a una narrativa visual ordenada,
- reducir ambigüedad con jerarquía de mensajes,
- mantener trazabilidad de evidencia y semáforos.

## Cuándo usar

Usa este skill cuando el usuario pida:

- rediseñar una salida HTML/markdown a formato de sesión ejecutiva,
- crear dashboard visual para claims, matrices, scores o estados clínicos,
- mejorar legibilidad mobile/desktop sin perder semántica ni fuentes de evidencia.

## Flujo de trabajo

1. Definir audiencia y objetivo de decisión.
   - Si es audiencia clínica: priorizar claridad diagnóstica, semáforos explícitos, y sección de advertencias críticas.
2. Definir estructura de lectura.
   - Cabecera resumen -> métricas clave -> hallazgos prioritarios -> tabla detallada -> anexos/métodos.
3. Aplicar sistema visual.
   - Paleta sobria con contraste adecuado,
   - tipografías legibles (preferible `Inter`, `Arial`, `Segoe UI`),
   - espaciado generoso,
   - estados por color consistentes (VERDE/AMBAR/ROJO).
4. Implementar componentes.
   - Cards con métricas,
   - tablas con encabezados fijos si hay mucho detalle,
   - badges para estado,
   - bloque de métodos y supuestos,
   - listas separadas por criticidad.
5. Revisar legibilidad rápida.
   - Orden de importancia por importancia clínica,
   - textos cortos por fila,
   - links trazables claramente visibles.
6. Validar consumo en reunión.
   - Responsivo a móvil,
   - contraste AA mínimo,
   - navegación por secciones (índice/ancorajes),
   - evitar ruido visual y lenguaje especulativo.

## Convenciones visuales (obligatorias)

- No usar jerga innecesaria en títulos principales.
- Semáforos siempre con etiqueta textual además de color.
- Incluir sección explícita de “estado de evidencia” y “métodos”.
- Usar animación mínima y funcional (ej. reveal suave al hacer scroll), nunca ornamental.
- Mantener HTML autosuficiente para ejecución local (sin build externo).

## Patrones recomendados

- **Modo reunión**: máximo foco en conclusiones y riesgos.
  - 1 bloque de “hallazgos críticos”.
  - 1 bloque de métricas globales.
  - 1 bloque de detalle expandible o filtrado.
- **Modo técnico**: incluir enlaces fuente y observaciones por fila.

## Resultado esperado

- Un único HTML limpio, legible, mobile-friendly, con anclajes y jerarquía de riesgo.
- Prioridad visual: rojo/ámbar/verde, luego severidad por prompt/modelo, luego evidencia.
- Capas de lectura: ejecutivo, operativa y técnica.

