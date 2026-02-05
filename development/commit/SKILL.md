---
name: commit
description: Crea commits git con verificación obligatoria de calidad. Ejecuta dart analyze, format y tests antes de commitear.
model: claude-3-5-haiku-20241022
---

# Commit

Crea un commit con los cambios actuales, **después de verificar calidad del código**.

## Cuándo Usar Este Skill (Automático)

Aplicar automáticamente cuando:
- El usuario dice "commit", "commitea", "guarda los cambios"
- El usuario termina una tarea y hay cambios sin commitear
- Hay cambios staged listos para commit

## Reglas

### NO auto-mencionarse

**PROHIBIDO** añadir:
- `Generated with [Claude Code]`
- `Co-Authored-By: Claude`
- Cualquier mención a Claude, Anthropic, o IA

El commit debe parecer escrito por un humano.

### NO pedir confirmación

**PROHIBIDO** pedir confirmación para:
- Hacer `git add -A`
- Ejecutar el commit
- Ejecutar las verificaciones

Simplemente hazlo. El usuario confía en ti.

---

## Proceso

### Fase 1: Detectar paquetes afectados

```bash
git diff --name-only HEAD
```

Identificar qué paquetes tienen cambios:
- `packages/mot/**` → verificar packages/mot
- `packages/mot_flutter/**` → verificar packages/mot_flutter

### Fase 2: Verificaciones OBLIGATORIAS (DEBEN pasar)

Para `packages/mot` (Dart puro):

```bash
cd packages/mot
dart pub get
dart analyze --fatal-infos
dart format --set-exit-if-changed .
dart test
```

Para `packages/mot_flutter` (Flutter):

```bash
cd packages/mot_flutter
flutter pub get
flutter analyze --fatal-infos
flutter format --set-exit-if-changed .
flutter test
```

**Si CUALQUIER verificación falla:**
1. Mostrar los errores claramente al usuario
2. **NO continuar con el commit**
3. Informar: "Commit bloqueado. Hay X errores que arreglar."

### Fase 3: Crear el commit

Solo si Fase 2 pasó completamente:

1. `git status` para ver cambios
2. Si no hay staged, hacer `git add -A` automáticamente
3. Analizar cambios y generar mensaje:
   - Formato: `tipo: descripción breve`
   - Tipos: feat, fix, refactor, test, docs, chore, style
   - Inglés, max 72 chars primera línea
   - Body opcional si hay contexto importante
4. Ejecutar `git commit` directamente
5. Mostrar resultado con resumen de verificaciones

---

## Formato del Mensaje

```
tipo: descripción breve (max 72 chars)

[Body opcional - qué y por qué, no cómo]
```

## Output Esperado

### Commit exitoso:
```
Verificando calidad del código...

packages/mot:
  dart analyze: 0 errores
  dart format: formatted
  dart test: 23 tests passed

Todas las verificaciones pasaron

[main abc1234] feat: add beacon field implementation
 3 files changed, 45 insertions(+), 12 deletions(-)
```

### Commit bloqueado:
```
Verificando calidad del código...

packages/mot:
  dart analyze: 3 errores
    - lib/src/beacon.dart:66 - Type error...

Commit bloqueado. Arregla los 3 errores antes de commitear.
```

## Prohibido

- Commitear sin ejecutar verificaciones
- Ignorar errores de dart analyze
- Ignorar tests fallidos
- Pedir confirmación (JAMÁS)
- Añadir firmas o atribuciones
- Usar emojis en el mensaje de commit
- Mensajes genéricos como "update files"

## Casos Especiales

### Solo cambios en docs/
Si los únicos cambios son en `docs/**`, `*.md`, o archivos de configuración:
- Saltar verificaciones de código
- Proceder directamente al commit
