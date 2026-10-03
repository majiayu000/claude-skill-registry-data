---
name: crear-release
description: Crea GitHub Release con changelog automático desde commits recientes.
---

# Skill: Crear Release

Genera y publica un release profesional en GitHub.

## Instrucciones para el Agente:

### 1. Determinar versión
- Leer `MASTER_PLAN.md` sección 17 para saber la versión de la fase actual
- Si no existe, preguntar al usuario

### 2. Generar changelog
```bash
# Obtener último tag
ULTIMO_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$ULTIMO_TAG" ]; then
  git log --oneline
else
  git log $ULTIMO_TAG..HEAD --oneline
fi
```

### 3. Crear archivo CHANGELOG.md temporal
```markdown
## vX.Y.Z — Nombre de la Fase

### Cambios
- commit 1
- commit 2
```

### 4. Verificar estado
```bash
pnpm typecheck && pnpm test:unit && pnpm test:e2e
```
- Si PASS → release stable
- Si FAIL → release prerelease

### 5. Crear tag y release
```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z

# Stable:
gh release create vX.Y.Z --title "Fase X: nombre" --notes-file CHANGELOG.md

# Prerelease:
gh release create vX.Y.Z --prerelease --title "Fase X: nombre (RC)" --notes-file CHANGELOG.md
```

### 6. Limpiar
- Eliminar CHANGELOG.md temporal
