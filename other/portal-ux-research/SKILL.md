---
name: portal-ux-research
description: Design and execute UX research instruments for the Portal Centralizado de Datos Financieros. Use when building the Google Forms survey (13 questions, n>=15), running semi-structured interviews, writing personas and empathy maps, building journey maps with quote-to-pain traceability, running card sorting, or executing the SUS usability test (>=75 with >=5 participants).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal UX Research Skill

Cubre el trabajo de campo y los artefactos de investigación del EPIC UX: instrumentos, personas, mapas de empatía, journey maps, card sorting / IA y SUS. Fuente de verdad: `context/planeacion_proyecto.md` §5, §11, Anexos A y B.

## Rules — NON-NEGOTIABLE

- **Honestidad metodológica**: toda cifra que aparezca en un entregable sale de (a) la encuesta propia, (b) una fuente pública citada y verificada, o (c) se declara explícitamente como estimación del equipo. Jamás se inventan estadísticas de mercado.
- **Consentimiento y ética (Anexo A.3)**: encuesta anónima y voluntaria; entrevistas con consentimiento verbal registrado; datos solo para fines académicos del curso; sin datos confidenciales de instituciones reales.
- Cuadrantes de mapas de empatía etiquetados exactamente **"Says", "Thinks", "Does", "Feels"** (en inglés, como exige la rúbrica).
- **Trazabilidad**: cada pain point de un journey map se remonta a una cita o dato de campo (cadena cita→pain→oportunidad). Cada persona referencia al menos un dato o cita del trabajo de campo.
- Los roles Operativo/Analista/Directivo **no son excluyentes**: el hallazgo se valida con la pregunta E-08, no se asume.
- Prosa de entregables en español neutro; sin emojis en documentos ni artefactos.

## Encuesta Google Forms (Anexo A.1) — 13 preguntas, ~7 min, anónima

Meta: **n ≥ 15** respuestas con corte el **vie 24-jul**. Publicación lun 20-jul, distribución en ≥3 canales (LinkedIn, grupos de trabajo, contactos del sector de los 3 integrantes), recordatorio a las 48 h.

| Bloque | Pregunta | Contenido | Uso |
|--------|----------|-----------|-----|
| Screening/demografía | E-01 | Edad por rango | Demografía de audiencia |
| | E-02 | Género (opcional) | Demografía |
| | E-03 | Ciudad/país | Demografía |
| | E-04 | Rol actual: operaciones / análisis de datos / dirección / TI / otro | Segmentación por perfil |
| | E-05 | Años de experiencia en el sector financiero-datos | Screening |
| Comportamiento y pains | E-06 | ¿Cuántas fuentes/sistemas consultas para un análisis típico? (1 / 2–3 / 4–5 / 6+) | Pastel de fuentes → sección Problema |
| | E-07 | ¿Cuántas horas a la semana pierdes buscando o validando un dato? (rangos) | **Cuantificación del problema** (histograma) |
| | E-08 | ¿Alternas entre consultas rápidas y análisis profundos en una semana típica? (siempre/a veces/nunca) | **Valida "roles no excluyentes"** |
| | E-09 | ¿Qué es lo más frustrante de cruzar datos de áreas distintas? (múltiple + abierta) | Barras de pains |
| | E-10 | Cuando no sabes dónde vive un dato, ¿a quién/qué recurres primero? (colega / intranet / correo / adivino / otro) | Silos de conocimiento |
| | E-11 | ¿Qué formato de salida necesitas más? (pantalla / CSV-Excel / API / PDF) | Prioridad de exportación |
| | E-12 | Uso de un asistente "¿dónde está X dato y qué significa?" (Likert 1–5) + primera pregunta (abierta) | Apetito por el agente; seed Anexo C |
| Canales | E-13 | ¿Dónde te informas de herramientas/datos? (LinkedIn / Slack-Discord / YouTube / cursos / colegas) | Apartado "dónde se conectan" |

Montaje: preguntas obligatorias con validación de rangos. Procesamiento: exportar a Sheets y generar las 3 gráficas listas para el PDF — barras de pains (E-09), histograma de horas perdidas (E-07), pastel de fuentes consultadas (E-06).

## Entrevistas semiestructuradas (Anexo A.2) — 3 × 30 min

Una por perfil (Operativo, Analista, Directivo), una por integrante, antes del **sáb 25-jul**. Producto: notas y **≥5 citas textuales por entrevista** (insumo directo de "Says" y de la frase de cada persona).

Guion (7 preguntas):

1. Cuéntame tu rol y un día típico con datos.
2. Narra la última vez que necesitaste un dato de otra área: paso a paso, ¿cuánto tardó?, ¿qué se sintió? (sondear emociones para "Feels").
3. ¿Cómo validas que una cifra es correcta antes de usarla?
4. ¿Qué haces cuando la herramienta se queda corta? (Excel escapes, tickets, favores).
5. Si mañana existiera un portal único, ¿qué tendría que hacer en la primera semana para que confíes en él?
6. ¿Qué NO debería hacer jamás? (deal-breakers: opacidad, lentitud, borrar contexto).
7. Cierre: una frase que resuma tu relación con los datos de tu institución (candidata a "frase de la persona").

## Matriz de personas (§5.3) — 6 personas, 2 por integrante

Cobertura obligatoria: **2×Operativo, 2×Analista, 2×Directivo**. Cada integrante hace también los mapas de empatía de sus mismas 2 personas (consistencia narrativa persona↔mapa).

| Integrante | Persona 1 | Persona 2 |
|------------|-----------|-----------|
| Alexandro | Analista de datos (riesgo de mercado, power user Python/Excel) | Operativo (mesa de derivados, urgencia intradía) |
| Jacqueline | Directivo (dirección de liquidez, supervisión regulatoria) | Analista (riesgo de crédito, reportes mensuales) |
| Arthur | Operativo (tesorería, validación puntual) | Directivo (CFO/dirección de riesgos, decisión ejecutiva) |

## Plantilla de persona (Anexo B, idéntica para las 6)

- Foto de perfil generada con IA, estilo fotográfico consistente entre las 6.
- Nombre, edad, sexo, ocupación.
- Antecedentes: educación, situación familiar, intereses.
- Objetivos: 2–3, ligados al portal.
- Pain points y desafíos: 3–4, al menos 1 proveniente de encuesta/entrevista.
- Comportamientos y hábitos: relación con datos y herramientas.
- Frase/cita: idealmente derivada de la pregunta 7 de la entrevista.
- Revisión cruzada: cada integrante revisa las personas de otro antes de integrar.

Guía de coherencia: Operativo → urgencia, validación, desconfianza de cifras sin fuente. Analista → profundidad, exportación, fricción de accesos. Directivo → síntesis, riesgo, tiempo escaso, delegación.

## Plantilla de mapa de empatía (Anexo B)

- Cabecera con el nombre de la persona + 4 cuadrantes **Says / Thinks / Does / Feels**.
- **≥3 observaciones por cuadrante**, coherentes con la persona correspondiente.
- Al menos un "Says" por mapa es **cita textual** de las entrevistas.
- Plantilla visual uniforme entre los 6 mapas: misma retícula y código de color por perfil.

## Journey maps (A2)

- 3 escenarios narrativos, uno por perfil: validación urgente (Operativo), cruce multi-fuente + exportación (Analista), supervisión y decisión (Directivo).
- 3 journey maps con etapas, acciones, puntos de contacto, pensamientos, curva emocional, pain points y oportunidades; cada journey conecta explícitamente con una persona de A1.
- Los pain points provienen de la investigación (trazabilidad **cita→pain→oportunidad**); formato visual consistente entre los 3.

## Card sorting (A3)

- Remoto con ≥6 colegas, u optimizado con pre-validación sintética (skill `portal-synthetic-users`) **declarando el método** en el entregable.
- Impacto documentado en la taxonomía del catálogo y el sitemap; taxonomía alineada a la estrategia RAG bifurcada (paper 05).

## Evaluación SUS (A5)

- Protocolo de prueba moderada: 3 tareas por perfil sobre el prototipo desplegado en Cloud Run.
- **≥5 participantes reales** + cuestionario SUS; meta **SUS ≥ 75**.
- Hallazgos priorizados por severidad × frecuencia; correcciones aplicadas o backlogueadas.
- La pre-validación sintética previa (A3/A4) se reporta como complemento, nunca como sustituto de esta prueba con humanos.

## Checklist de campo

- [ ] Formulario publicado lun 20-jul con las 13 preguntas y validaciones
- [ ] n ≥ 15 al corte vie 24-jul (monitoreo diario, recordatorio a 48 h)
- [ ] 3 entrevistas ejecutadas con consentimiento registrado y ≥5 citas c/u
- [ ] 3 gráficas exportadas (E-09 barras, E-07 histograma, E-06 pastel)
- [ ] 6 personas según matriz §5.3, con revisión cruzada
- [ ] 6 mapas con cuadrantes en inglés y ≥1 cita textual en Says
- [ ] Trazabilidad cita→pain→oportunidad verificable en journeys

## When NOT to Use This Skill

- Maquetar y entregar el PDF de una actividad → `portal-ux-deliverables`.
- Pre-validación con evaluadores sintéticos LLM → `portal-synthetic-users`.
- Implementar patrones UX en el frontend → `portal-ux-patterns`.
