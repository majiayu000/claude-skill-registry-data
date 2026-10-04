---
name: insights
description: "Genera reportes de actividad y analytics de sesiones de Jarvis. Activar con: /insights, /insights --days 30, /insights --area jarvis — o cuando el usuario pida 'estadísticas', 'resumen de actividad', 'qué hemos hecho', 'cuánto hemos avanzado'. Inspirado en el sistema de analytics de Hermes Agent."
allowed-tools: Read, Glob, Bash
---

# Insights — Analytics de Sesiones Jarvis

> Inspirado en el sistema `/insights` de Hermes Agent (NousResearch).
> Analiza el cerebro/ wiki para generar métricas de actividad, áreas trabajadas y patrones de sesión.

---

## Comandos

- `/insights` — Reporte completo (últimos 30 días por defecto)
- `/insights --days N` — Reporte de los últimos N días
- `/insights --area <area>` — Filtrar por área (jarvis, ops, dev, design, personal)

---

## Protocolo de Generación

### Paso 1 — Recopilar datos

```
1. Leer ~/.claude/cerebro/log.md
   - Parsear entradas: ## [YYYY-MM-DD HH:MM] operacion | slug
   - Filtrar por rango de días solicitado

2. Glob ~/.claude/cerebro/sessions/*.md
   - Leer frontmatter: title, area, date, tags, status

3. Leer ~/.claude/cerebro/index.md
   - Extraer: Total nodes, áreas activas, última actualización

4. Leer ~/.claude/goals.md (si existe)
   - Cargar goals activos para calcular progreso
```

### Paso 2 — Calcular métricas

| Métrica | Cómo calcular |
|---------|--------------|
| Sesiones totales | Count de archivos en sessions/ dentro del período |
| Áreas más activas | Frecuencia de `area` en frontmatter de sesiones |
| Tags frecuentes | Top 10 tags en todas las sesiones del período |
| Operaciones en log | Count por tipo: ingest, update, curator, lint, etc. |
| Racha de días activos | Días consecutivos con al menos 1 sesión |
| Nodos creados | Count de operaciones `ingest` en log.md |

### Paso 3 — Generar reporte

**Formato terminal (en conversación):**
```
## 📊 Insights — Últimos 30 días
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Sesiones: 12
📝 Nodos en cerebro: 8 sesiones | 1 user-model
🗓️  Período: YYYY-MM-DD → YYYY-MM-DD

### Áreas más activas
1. jarvis    ████████████ 6 sesiones (50%)
2. ops       ████████     4 sesiones (33%)
3. dev       ████         2 sesiones (17%)

### Operaciones en log
- ingest: 8 | update: 4 | curator: 0 | lint: 1

### Tags frecuentes
hermes-agent, jarvis, tryvex, gsap, skills, memory

### Goals activos
🎯 goal-001: "Jarvis 85% autonomous — 55 días restantes"
   Progreso actual: 63% | Velocidad: ~0.5%/día ✅

### Racha actual
🔥 3 días activos consecutivos
```

**Formato gateway (Discord, condensado):**
```
📊 **Insights (30d):** 12 sesiones | 8 nodos
🔝 Áreas: jarvis (6) > ops (4) > dev (2)
🏷️  Tags top: hermes-agent, jarvis, tryvex
📈 Goal-001: Jarvis 63% → 85% | 55d restantes
```

---

## Análisis adicional — Velocidad de progreso

Si hay un goal activo con deadline:
```
Goal: [texto del goal]
Progreso actual: X%
Días restantes: N
Velocidad necesaria: ~X% por día
Velocidad actual (últimas 2 semanas): ~Y% por día
Estado: ✅ en ritmo / ⚠️ rezagado
```

## Sugerencia proactiva al final

Siempre incluir al final del reporte:
```
💡 Mayor impacto siguiente: [tarea de mayor valor de cerebro/sessions/ pendiente]
```

---

## Límites

- Solo lectura — nunca modifica archivos de cerebro/
- Si cerebro/ no existe → "Sin datos de sesión aún. Usa /memoria ingest para comenzar."
- Para períodos > 90 días, advertir que los datos pueden estar incompletos
