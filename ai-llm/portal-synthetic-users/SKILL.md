---
name: portal-synthetic-users
description: Run PerceptUI-style synthetic user pre-validation for the Portal Centralizado de Datos Financieros. Use when pre-validating wireframes (A3) or high-fidelity prototypes (A4) with LLM evaluators conditioned on the 8 personas from A1, before real-user testing. Always reported as complementary pre-validation, never as a substitute for the human SUS test of A5.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Synthetic Users Skill

Implementa el diferenciador metodológico de la pista UX: evaluadores sintéticos LLM **condicionados por persona** (paper 08, PerceptUI, arXiv:2606.05697) para pre-validar interfaces antes de las pruebas con usuarios reales. Aplica a wireframes/taxonomía (A3, apoyo a card sorting) y a prototipos de alta fidelidad (A4), y se reporta en A5 como parte del proceso.

## Rules — NON-NEGOTIABLE

- La pre-validación sintética es **complementaria**: NUNCA sustituye la prueba con humanos que pide la rúbrica (SUS con ≥5 participantes reales en A5). Todo reporte lo declara explícitamente.
- **Sesgos declarados** en cada reporte: los evaluadores heredan sesgos del LLM y de la redacción de las personas; sus respuestas son predicciones plausibles, no datos de campo. No se mezclan con las cifras de la encuesta ni cuentan para n.
- Condicionamiento exclusivamente con las **8 personas de A1** (matriz §5.3; A1 entregó 8 sobre las 6 que pedía la rúbrica, y A3 corrió con las 8): el valor metodológico es reutilizar investigación real como condicionamiento, no inventar perfiles ad-hoc. Las salidas crudas de A3 están en `docs/entregables/datos/a3_sorts/P1..P8.json`.
- Al menos **1 iteración de diseño documentada** derivada de los hallazgos sintéticos (criterio de aceptación del plan): hallazgo → cambio aplicado → versión posterior.
- Salidas con racionales en lenguaje natural (no solo puntuaciones): el "por qué" es lo accionable.
- Honestidad metodológica transversal: en los entregables, los hallazgos sintéticos se rotulan como "pre-validación sintética (PerceptUI)".

## Fundamento (paper 08)

PerceptUI predice cómo respondería un usuario específico a preguntas sobre una interfaz, con racionales en lenguaje natural, condicionado por persona. Logra realismo a nivel humano y generaliza a personas y preguntas no vistas, atacando el costo/lentitud de reclutar participantes en iteración temprana. En este proyecto no se re-entrena el framework: se adopta su **protocolo de condicionamiento por persona** con el LLM disponible, con la humildad metodológica que el propio paper exige.

## Protocolo de sesión sintética

1. **Preparar el estímulo**: capturas o descripciones estructuradas de la interfaz (wireframe A3 o pantalla de alta fidelidad A4), con el flujo de tarea que se evalúa.
2. **Condicionar por persona**: un evaluador por persona (6 en total), usando la ficha completa de A1 (demografía, antecedentes, objetivos, pains, hábitos, frase).
3. **Preguntar sobre la interfaz**: batería fija por pantalla + preguntas específicas de la tarea.
4. **Recoger racionales**: cada respuesta exige justificación en lenguaje natural anclada a la persona ("como analista de riesgo, esperaría...").
5. **Sintetizar**: agrupar hallazgos por severidad × frecuencia entre las 8 personas; separar consenso (accionable) de idiosincrasia (observación). Conteos en absolutos sobre 8, nunca en porcentajes: con esa n un porcentaje exagera la fuerza de la evidencia.
6. **Iterar y documentar**: aplicar al menos 1 cambio de diseño y registrar el antes/después.

### Plantilla de prompt condicionado (inglés, como todo artefacto de código)

```text
You are {persona.name}, a {persona.age}-year-old {persona.occupation}.
Background: {persona.background}
Goals: {persona.goals}
Pain points: {persona.pain_points}
Habits with data tools: {persona.habits}
Signature quote: "{persona.quote}"

You are shown the following interface of a centralized financial data portal:
{interface_description_or_capture}

Task under evaluation: {task}

Answer AS THIS PERSON, in first person, grounding every answer in your
background and pain points. For each question give (a) your answer and
(b) a natural-language rationale.

1. What do you think this screen is for? What would you click first?
2. Can you complete the task? Walk through your steps and where you hesitate.
3. What is missing or confusing for someone in your role?
4. Would you trust the numbers shown? What would make you trust them more?
5. Rate the ease of the task 1-5 and justify the score.
```

## Baterías por actividad

| Actividad | Estímulo | Foco de las preguntas | Salida |
|-----------|----------|-----------------------|--------|
| A3 | Sitemap, taxonomía del catálogo, wireframes | ¿Dónde buscarías X? Agrupaciones esperadas (apoyo/optimización del card sorting, declarando método) | Ajustes de taxonomía y navegación |
| A4 | **Capturas reales del prototipo web navegable**, 7 pantallas (acceso, inicio, exploración y extracción, gobierno del dato, asistente, administración, exportación) — nunca mockups: es lo que distingue esta pre-validación de una revisión de diseño | Comprensión, confianza (fuente/linaje), fricción por rol, jerarquía visual | Hallazgos priorizados + ≥1 iteración documentada (hallazgo → cambio → versión, con antes y después) |
| A5 | — | Se reporta el proceso y sus límites junto a los resultados SUS reales | Sección de método en el documento final |

## Estructura del reporte de pre-validación

1. Objetivo y estímulos evaluados.
2. Método: protocolo, LLM utilizado, personas condicionantes (referencia a A1).
3. **Declaración de sesgos y límites** (obligatoria).
4. Hallazgos por persona y consolidados (severidad × frecuencia).
5. Iteración(es) de diseño aplicadas con evidencia antes/después.
6. Relación con la validación humana: qué queda pendiente de confirmar en A5.

## Checklist

- [ ] 6 evaluadores condicionados con las fichas de personas de A1
- [ ] Racionales en lenguaje natural capturados para cada respuesta
- [ ] Sesgos y límites declarados en el reporte
- [ ] ≥1 iteración de diseño documentada (hallazgo → cambio → versión)
- [ ] Reporte rotulado como pre-validación complementaria, nunca sustituto de A5
- [ ] Hallazgos sintéticos separados de los datos de campo reales

## When NOT to Use This Skill

- Trabajo de campo con humanos (encuesta, entrevistas, SUS) → `portal-ux-research`.
- Redactar/maquetar el documento de la actividad → `portal-ux-deliverables`.
- Construir el agente conversacional del producto → `portal-adk-agent` (los evaluadores sintéticos son tooling de diseño, no features del portal).
