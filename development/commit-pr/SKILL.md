---
name: commit-pr
description: Crea commits y pull requests. Usar cuando se necesita commitear cambios, crear PRs, escribir mensajes de commit, o gestionar branches.
allowed-tools: Bash(git:*), Bash(gh:*), Read
---

# Commit & PR Skill

## Commit Messages

### Formato
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
| Type | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Bug fix |
| `docs` | Solo documentación |
| `style` | Formato, sin cambio de lógica |
| `refactor` | Refactoring sin cambio de comportamiento |
| `test` | Añadir o modificar tests |
| `chore` | Cambios de build, CI, deps |
| `perf` | Mejoras de performance |

### Scope
Módulo o área afectada: `cli`, `ai`, `git`, `state`, `engine`, etc.

### Ejemplos
```
feat(cli): add --resume flag to work command

fix(ai): handle timeout in SDK provider gracefully

refactor(engine): extract CI handler to separate module

test(git): add worktree creation tests
```

## Pull Requests

### Título
Mismo formato que commits: `<type>(<scope>): <description>`

### Template de Descripción
```markdown
## Summary
- Bullet point 1 del cambio principal
- Bullet point 2 si aplica
- Bullet point 3 si aplica

## Test Plan
- [ ] Tests unitarios pasan
- [ ] Tests de integración pasan
- [ ] Probado manualmente con: [descripción]

## Related
- Closes #123 (si aplica)
- Related to #456 (si aplica)
```

### Labels Recomendados
- `enhancement` - Nueva feature
- `bug` - Bug fix
- `documentation` - Solo docs
- `refactor` - Refactoring
- `breaking-change` - Breaking changes

## Workflow de Git

### Crear Branch
```bash
# Formato: oss-agent/<issue-id>-<descripcion-corta>
git checkout -b oss-agent/123-add-resume-flag
```

### Antes de Commit
```bash
# Verificar cambios
git status
git diff

# Stage archivos específicos (preferido sobre git add .)
git add src/cli/commands/work.ts
git add tests/work.test.ts
```

### Commit
```bash
git commit -m "feat(cli): add --resume flag to work command

Allows resuming work on a previously started issue session.
The session ID is retrieved from the state database.

Closes #123"
```

### Push y PR
```bash
# Push branch
git push -u origin oss-agent/123-add-resume-flag

# Crear PR
gh pr create --title "feat(cli): add --resume flag" --body "..."
```

Ver [CONVENTIONS.md](CONVENTIONS.md) para convenciones específicas del proyecto.
