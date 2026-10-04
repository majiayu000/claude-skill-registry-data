---
name: commits-real
description: >
  Commits, PRs e issues con voz humana — español rioplatense cálido.
  Límite 300 líneas. Modo técnico (inglés) también disponible.
  Trigger: When writing commits, creating PRs, filing issues, or writing documentation.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "4.0"
  model_tier: T3-balanced
---

# Skill: commits-real

Commits que cuentan una historia, no que parecen generados por una máquina.

## Trigger

- Terminaste un cambio y hay que comitear
- Estás creando un PR o issue
- Necesitás actualizar un CHANGELOG
- Vas a versionar semver

## Modos de commit

### Modo Humano (default — español rioplatense)
Cálido, claro, directo. Como si se lo explicaras a un colega.

```
feat(api): agrego endpoint de login pa que los users entren tranqui

Ahora se puede autenticar con email + password. Devuelve un JWT
con expiración de 24hs. Implementé middleware de verificación
también, así que ya estamos cubiertos del lado del server.

Closes #42
```

```
fix(data): corrijo el cálculo de interés compuesto

El error estaba en la línea 47 — estaba usando la tasa nominal
cuando tenía que ser la tasa efectiva mensual. Afectaba todos
los préstamos con periodo > 30 días.
```

```
feat(ui): agrego dark mode que tanto venías pidiendo

Toggle en el header, usa CSS variables, persiste en localStorage.
Anda en todos los browsers que importan.
```

### Modo Técnico (inglés — para proyectos open source / internacional)
Conventional Commits clásico en inglés US.

```
feat(api): add JWT authentication endpoint

Implements email+password login returning a signed JWT.
Token expires in 24h. Includes middleware for route protection.

Closes #42
```

## Reglas de oro

1. **Máximo 300 líneas por commit/PR/issue** — si supera, usá `chained-pr`
2. **Atomic commits** — un cambio lógico por commit
3. **Contá una historia** — el título dice QUÉ, el body dice POR QUÉ y el PATRÓN
4. **Nunca hagas commit sin testear antes** — primero delegá a `lend-ai-testing`
5. **Engram siempre** — guardá lo que se hizo con mem_save

## Workflow LEND

1. ANALIZAR
   ├── ¿Qué cambió? archivos, funcionalidad, bug, refactor?
   ├── Scope: ¿qué módulo? (api, ui, data, infra, docs)
   ├── Breaking: ¿rompe compatibilidad hacia atrás?
   └── Issues: ¿hay issues o PRs relacionados?

2. OFRECER (Menú del Senior)
   ├── A) Modo humano — español rioplatense, título + breve descripción
   ├── B) Modo técnico — conventional commit en inglés
   ├── C) Full — commit + PR + changelog update
   └── D) Chained PR — si supera 300 líneas, partilo en PRs encadenados

3. ELEGIR → user confirma

4. HACER (PRE-COMMIT GATES primero!)
   ├── ¿Ya corriste tests? Si no → `task('lend-ai-testing', 'verificar que todo anda')`
   ├── ¿Está todo en verde? Ok seguí
   ├── ¿Supera 300 líneas? → `task('chained-pr', ...)`, no commits gigantes
   ├── Formato humano: `tipo(scope): título en español cálido`
   ├── Tipos: feat, fix, chore, docs, refactor, test, style, perf, ci
   ├── Mensaje: imperativo, presente, < 60 chars título, < 80 chars body
   ├── Atomic: un cambio por commit
   └── Issues: `Closes #123` en el body

5. VERIFICAR
   ├── El mensaje es claro y útil para el futuro
   ├── No hay archivos no relacionados
   ├── Breaking changes están documentados
   └── Tests pasan (siempre)

### Post-task (siempre)
1. mem_save a Engram con lo que se hizo
2. Revisar si hay que actualizar docs (README, AGENTS.md, ARCHITECTURE.md)

## Regla del título (modo humano)

```
tipo(scope): qué hace, en menos de 60 caracteres, en español

Tipos: feat (nueva funcionalidad), fix (bug fix), refactor, test,
       docs, style, chore, perf, ci
Scope: api, ui, data, infra, docs, deps, config

Ejemplos:
  feat(api): agrego ruta de login con JWT
  fix(data): corrijo cálculo de interés compuesto
  refactor(ui): extraigo Navbar a componente separado
  test(api): agrego tests para auth middleware
  docs(readme): actualizo ejemplos de uso
  chore(deps): actualizo pandas a 2.0
```

## Comment/Voice rules (PRs, issues, reviews)

- **Cálido y directo**: "Che, esto está mal porque..." no "Se sugiere reconsiderar..."
- **Corto**: 1-2 oraciones. Expandí solo si hace falta.
- **Explicá el por qué**: cada observación incluye la razón
- **Idioma**: español rioplatense con voseo
- **Sé útil rápido**: arrancá con lo que importa

## Comment formula

```
Observación directa → Por qué importa → Acción concreta

"Este hook necesita useCallback. Sin memoization se recrea en cada
render y rompe las dependencias del useEffect de abajo.
Metele useCallback con [] y tiramos."
```

## PR guidelines

- Qué revisar PRIMERO (archivos de alto impacto)
- Qué está FUERA DE SCOPE (no hagas adivinar al reviewer)
- Link de contexto si es parte de una cadena de PRs
- Test plan: qué se testeó manual y automáticamente

## Anti-patterns

- ❌ Mensajes vagos: "update", "fix", "cambios"
- ❌ Múltiples features en un solo commit
- ❌ Breaking changes sin nota
- ❌ Archivos no relacionados en el mismo commit
- ❌ Commits sin test previo
- ❌ Superar 300 líneas sin partir en chained-pr
