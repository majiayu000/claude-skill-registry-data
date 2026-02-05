---
name: feature-dev
description: Guía el desarrollo de nuevas features. Usar cuando se implementa funcionalidad nueva, se trabaja en issues de GitHub, se planifica arquitectura, o se crean PRs de desarrollo.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch, WebSearch
---

# Feature Development Skill

## Workflow

1. **Analizar requerimientos** - Leer issue/task y entender el objetivo
2. **Explorar código existente** - Usar Glob/Grep para encontrar patrones relevantes
3. **Diseñar solución** - Seguir arquitectura existente del proyecto
4. **Implementar** - Escribir código siguiendo convenciones
5. **Tests** - Añadir tests para nueva funcionalidad
6. **Verificar** - Ejecutar linting, tipos y tests

## Guidelines

### Código
- Seguir convenciones existentes en el codebase
- Cambios mínimos y focalizados - no refactorizar código no relacionado
- Usar tipos explícitos en TypeScript
- No añadir dependencias sin justificación

### Tests
- Tests unitarios para lógica nueva
- Tests de integración si afecta múltiples módulos
- Cubrir edge cases y error paths

### Documentación
- Documentar solo si la lógica no es obvia
- Actualizar README si cambia API pública
- No añadir comentarios redundantes

## Arquitectura oss-agent

```
src/
├── cli/           # Commands (Commander.js)
├── core/
│   ├── ai/        # AI providers (CLI/SDK)
│   ├── engine/    # Workflow engines
│   ├── git/       # Git operations
│   └── state/     # SQLite state management
├── infra/         # Utils, logging, errors
└── types/         # Zod schemas
```

### Convenciones del Proyecto

- **ESM modules** - Usar `.js` en imports
- **Strict TypeScript** - `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`
- **Zod para validación** - Schemas en `src/types/`
- **Commander.js para CLI** - Commands en `src/cli/commands/`

Ver [PATTERNS.md](PATTERNS.md) para patrones específicos del proyecto.
