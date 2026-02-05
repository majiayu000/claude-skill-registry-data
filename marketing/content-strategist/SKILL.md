---
name: content-strategist
description: Defines editorial priorities for AndesRC blog. Maps topics to funnel stages (TOFU/MOFU/BOFU), identifies pillar vs. satellite content, and ensures alignment with the 4 content pillars. Use when starting a new content cycle or prioritizing the backlog.
metadata:
  author: AndesRC
  version: "1.0"
---

# Content Strategist

## Purpose
Define editorial priorities, map content to funnel stages, and ensure alignment with AndesRC's 4 content pillars.

## Content Pillars

| Pilar | Stage | Objetivo | Keywords Ejemplo |
|-------|-------|----------|------------------|
| **1. Empezar desde Cero** | TOFU | Captura demanda masiva | `empezar a correr`, `plan caminar correr` |
| **2. Planes por Distancia** | MOFU | Estructura y Retención | `plan 10k sub 50`, `fartlek para 5k` |
| **3. Prevención de Lesiones** | MOFU/BOFU | Autoridad Médica (YMYL) | `fascitis plantar`, `rodilla del corredor` |
| **4. WhatsApp Coaching** | BOFU | Conversión Final | `coach running cdmx`, `entrenador personal running online` |

## Topic Clusters

1. **Entrenamiento para Principiantes** - Pilar page: "Guía Completa para Empezar a Correr"
2. **Prevención de Lesiones** - Pilar page: "Guía Definitiva de Prevención de Lesiones"
3. **Nutrición e Hidratación** - Pilar page: "Nutrición para Runners: Guía Completa"
4. **Planes por Distancia** - Pilar page: "Planes de Entrenamiento por Distancia"
5. **Rutas y Comunidad Local** - Template by city
6. **Equipamiento** - Pilar page: "Guía de Equipamiento Running"
7. **Motivación y Mentalidad** - Pilar page: "Mentalidad del Runner Exitoso"

## Instructions

### When to Use
- At the start of each content cycle (weekly/monthly)
- When prioritizing the content backlog
- When a new content idea is proposed

### How to Prioritize

1. **Review funnel gaps**: Check which stage (TOFU/MOFU/BOFU) needs more content.
2. **Keyword volume**: Prioritize higher-volume keywords for TOFU.
3. **Seasonal relevance**: Consider upcoming races, seasons (New Year resolutions, marathon prep).
4. **Internal linking opportunities**: Prioritize satellite content that can link to pillar pages.

### Output Format

```json
{
  "title": "Método CaCo: Guía Completa para Caminar-Correr",
  "slug": "metodo-caco-caminar-correr",
  "lang": "es",
  "pilar": 1,
  "cluster": "Entrenamiento para Principiantes",
  "stage": "TOFU",
  "type": "satellite",
  "target_keyword": "plan caminar correr",
  "secondary_keywords": ["empezar a correr", "método caminando", "5k desde cero"],
  "priority": "high",
  "rationale": "High search volume, targets beginners, links to existing pillar page"
}
```

## Content Distribution (Year 1)

- 30% Entrenamiento
- 25% Prevención Lesiones
- 20% Rutas Locales
- 15% Nutrición
- 5% Equipamiento
- 5% Motivación
