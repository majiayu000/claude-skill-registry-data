---
name: seo-researcher
description: Performs keyword research, competitive SERP analysis, and generates article outlines optimized for AI Overviews. Use before drafting any article. Focuses on long-tail keywords and semantic structure for LLM digestibility.
metadata:
  author: AndesRC
  version: "1.0"
---

# SEO Researcher

## Purpose
Perform keyword research, analyze competition, and generate article outlines optimized for Google AI Overviews and E-E-A-T compliance.

## Instructions

### Step 1: Keyword Research

1. Start with the primary keyword from the content brief.
2. Identify 3-5 secondary keywords (long-tail variations).
3. Check search volume and competition level.

**Priority Keywords by Language:**

**Spanish (LATAM + Spain):**
- `cómo empezar a correr` (8,100/month)
- `plan de entrenamiento running` (1,900/month)
- `prevención lesiones running` (720/month)

**English (Global):**
- `how to start running` (27,100/month)
- `running training plan` (14,800/month)
- `marathon training for beginners` (4,400/month)

### Step 2: Competitive Analysis

1. Analyze top 10 SERP results for the primary keyword.
2. Identify content gaps (topics they don't cover).
3. Note word count, structure, and multimedia usage.
4. Find opportunities to provide unique value (local expertise, scientific citations).

### Step 3: Generate Outline

**Structure for AI Overview Optimization:**

Each H2 section must begin with a "definition paragraph" (40-60 words) that directly answers the search intent.

**Example:**
```markdown
## ¿Qué es el Fartlek?

El Fartlek, o "juego de velocidad" en sueco, es un método de entrenamiento continuo que alterna ritmos rápidos y lentos de forma aleatoria, ideal para mejorar la resistencia aeróbica y la velocidad sin la rigidez de las series en pista.

[Detailed content follows...]
```

### Output Format

```json
{
  "primary_keyword": "plan 10k principiantes",
  "secondary_keywords": ["entrenamiento 10k desde cero", "correr 10k 8 semanas", "plan running 10 km"],
  "search_volume": 480,
  "competition": "medium",
  "outline": {
    "h1": "Plan de Entrenamiento 10K para Principiantes: Guía Completa 2025",
    "meta_title": "Plan 10K Principiantes | 8 Semanas para tu Primera Carrera",
    "meta_description": "Plan de entrenamiento 10K para principiantes. Programa de 8 semanas con progresión gradual, consejos de nutrición y prevención de lesiones. ¡Empieza hoy!",
    "sections": [
      {
        "h2": "¿Cuánto tiempo toma prepararse para un 10K?",
        "definition_paragraph": "La mayoría de principiantes necesitan entre 8 y 12 semanas para preparar su primer 10K de forma segura. Este tiempo permite construir una base aeróbica sólida y adaptar progresivamente los músculos y tendones al impacto de correr.",
        "subsections": ["Factores que influyen", "Señales de que estás listo"]
      }
    ]
  },
  "competitive_gaps": ["Ningún resultado menciona adaptación a altitud", "Falta localización para CDMX"],
  "unique_angle": "Incluir referencias a entrenamientos en El Ocotal y ajustes para altitud 2,240m"
}
```

## E-E-A-T Checklist

- [ ] Include first-person experience: "En nuestra experiencia con X corredores..."
- [ ] Cite clinical studies (e.g., Leppänen et al. 2024)
- [ ] Reference local geography (parques, rutas)
- [ ] Add medical disclaimer for YMYL content
