---
name: handoff-automatico
description: Genera HANDOFF + actualiza AI_LOG + prepara prompt para siguiente fase/modelo.
---

# Skill: Handoff Automático

Genera la transición completa entre fases sin perder contexto.

## Instrucciones para el Agente:

### 1. Generar HANDOFF_FASE_X.md
Crear archivo `docs/handoffs/HANDOFF_FASE_X_Y.md` con:

```markdown
# Handoff: Fase X → Fase Y
**Fecha:** YYYY-MM-DD HH:MM
**Modelo que entrega:** [nombre]
**Modelo que recibe:** [nombre]

## Estado Actual
- Archivos creados/modificados: [lista]
- DB: [estado del schema]
- Tests: [resultado]

## Servidores MCP Utilizados
- sqlite: ✅/❌
- github: ✅/❌
- playwright: ✅/❌

## Siguiente Fase
- Nombre: [nombre]
- Tareas pendientes: [lista]
- Modelo asignado: [nombre]

## Instrucciones de Continuidad
[Prompt listo para copiar/pegar en la sesión del nuevo modelo]

## Restricciones
- TypeScript estricto: 0 errores
- Null-safety en campos opcionales
- Seguir convenciones existentes
```

### 2. Actualizar AI_LOG.md
Agregar entrada en `docs/AI_LOG.md`:
```markdown
## Fase X — YYYY-MM-DD
- **Modelo:** [nombre]
- **Archivos:** [lista]
- **Tests:** [resultado]
- **Errores corregidos:** [lista]
- **Siguiente fase:** [nombre]
```

### 3. Verificar
- Confirmar que el handoff contiene toda la información necesaria
- Confirmar que AI_LOG está actualizado
