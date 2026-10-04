---
name: goal
description: "Objetivos persistentes que guían el comportamiento del agente entre sesiones. Activar con: /goal <objetivo>, /goal list, /goal clear <id>, /goal done <id> — o cuando el señor Ignacio diga 'quiero que recuerdes que...', 'mi objetivo es...', 'que no se te olvide que...'. Los goals persisten en ~/.claude/goals.md entre conversaciones."
allowed-tools: Read, Write, Edit, Glob
---

# Goal — Objetivos Persistentes Cross-Sesión

> Inspirado en el sistema `/goal` de Hermes Agent (NousResearch).
> Los goals persisten entre sesiones y guían el comportamiento del agente sin repetirlos cada vez.

---

## Concepto

Un **goal** es un objetivo que:
1. Persiste entre sesiones en `~/.claude/goals.md`
2. Se carga al inicio de cada sesión junto con `cerebro/index.md`
3. Orienta las decisiones del agente sin que el señor Ignacio deba repetirlo
4. Tiene estados: `active` / `paused` / `done` / `cleared`

**Diferencia con memoria:**
- Memoria = conocimiento acumulado del pasado
- Goal = objetivo que guía acciones hacia el futuro

---

## Archivo de persistencia

**Ruta:** `~/.claude/goals.md`

**Estructura:**
```markdown
# Goals — Jarvis

## Activos

### goal-001
- **Status:** active
- **Objetivo:** [descripción del goal]
- **Progreso:** [notas de avance — actualizar por sesión]
- **Creado:** YYYY-MM-DD HH:MM
- **Deadline:** YYYY-MM-DD (opcional)

---

## Completados

### goal-000
- **Status:** done
- **Objetivo:** [descripción]
- **Completado:** YYYY-MM-DD HH:MM
- **Resultado:** [cómo se logró]
```

---

## Comandos

### `/goal <objetivo>` — Crear goal

```
1. Leer ~/.claude/goals.md (crear si no existe)
2. Generar ID: goal-XXX (siguiente número disponible)
3. Agregar bajo ## Activos con status: active
4. Responder: "✅ Goal registrado (goal-XXX): [objetivo]"
```

### `/goal list` — Listar goals

```
1. Leer ~/.claude/goals.md
2. Mostrar solo status: active y paused
3. Formato: ID | Status | Objetivo | Días activo
```

### `/goal done <id>` — Completar goal

```
1. Localizar goal por ID
2. Cambiar status a: done
3. Agregar timestamp de completación + resultado breveen "Resultado"
4. Mover entrada a sección ## Completados
5. Celebrar brevemente: "🎉 Goal completado: [objetivo]"
```

### `/goal pause <id> [razón]` — Pausar goal

```
1. Cambiar status a: paused
2. Agregar "Razón de pausa: [razón]"
3. El goal no guía acciones mientras está pausado
```

### `/goal clear <id>` — Limpiar goal

```
1. Cambiar status a: cleared (NUNCA borrar — audit trail permanente)
2. El goal desaparece de /goal list pero queda en el archivo
```

---

## Integración automática en sesiones

**Al inicio de cada sesión** (paso adicional al protocolo del CLAUDE.md):

```
1. Verificar si ~/.claude/goals.md existe
2. Si existe → leer goals con status: active
3. Si hay goals activos → mostrar: "🎯 Goals activos: [lista corta]"
4. Orientar las acciones de la sesión hacia los goals
```

**Durante la sesión:** Si una decisión arquitectónica impacta un goal activo → mencionarlo.

---

## Ejemplo de uso

```
señor Ignacio: /goal Jarvis al 85% de capacidad autónoma para junio 2026

Jarvis: ✅ Goal registrado (goal-001):
        🎯 "Jarvis al 85% autonomous — deadline: 2026-06-30"
        Lo cargo automáticamente en cada sesión y oriento los sprints hacia él.
```

En la siguiente sesión, sin que el señor Ignacio lo repita:
```
Jarvis: 🎯 Goal activo: "Jarvis al 85% autonomous — 55 días restantes"
        Sprint de hoy avanza hacia: FTS5 cerebro + gateway unificado (+7%)
```

---

## Límites de seguridad

- `~/.claude/goals.md` **nunca se borra** — solo cambios de status
- Goals con `pinned: true` son inmunes a `/goal clear` automático
- Máximo 5 goals activos simultáneamente — si se excede, sugerir consolidar
- No crear goals contradictorios — verificar conflicto antes de registrar
