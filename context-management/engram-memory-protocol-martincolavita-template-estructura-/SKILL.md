---
name: engram-memory-protocol
description: Protocolo de persistencia estructurada en Engram (mem_save/mem_search/mem_session_summary). Define cuándo guardar, formato What/Why/Where/Learned, tipos, scope y topic_key para el ecosistema del proyecto.
license: Apache-2.0
---

# Engram Memory Protocol — Persistencia Estructurada

## Cuándo se usa

> **Regla (2026-11-04): Engram es sólo para la continuidad entre sesiones** —en qué estaba, qué quedó a medias, qué decisión
> está en curso—, **nunca para conocimiento**: una regla, un estado, una decisión o una trampa del stack van al Cerebro
> con el «sí» de la persona (versionado, legible desde cualquier máquina, única fuente de verdad). Engram vive en una
> máquina, no se versiona y puede contradecir al Cerebro sin que nadie lo note. El **verificador no lo lee nunca**. Si
> Engram no está instalado, no falta nada: es opcional.

Para `cerebro-curator` cuando Engram está configurado en la máquina (si no, `log.md` es el registro), y recomendado para los demás agentes cuando:

- Se persiste un cambio estructural o de configuración en el OKF.
- Se toma una decisión de arquitectura, diseño o proceso.
- Se corrige un bug o se descubre un comportamiento no obvio.
- Se establece una convención nueva (naming, estructura, formato).
- Se aprende una preferencia o restricción del usuario.

NO es para contenido funcional de negocio (eso va en el OKF) — es para conocimiento sobre el PROCESO, las decisiones y los errores del proyecto.

## Cuándo guardar (PROACTIVO, no esperar a que pidan)

Llamar `mem_save` INMEDIATAMENTE después de:

| Disparador | Tipo sugerido |
|------------|---------------|
| Decisión de arquitectura o tradeoff | `decision` |
| Bug fix completado (con causa raíz) | `bugfix` |
| Descubrimiento no obvio del codebase | `discovery` |
| Convención establecida | `pattern` |
| Configuración o setup de entorno | `config` |
| Preferencia o restricción del usuario | `preference` |

Autochequeo al terminar cualquier tarea: "¿Tomé una decisión, arreglé un bug, aprendí algo no obvio o establecí una convención? Si sí → `mem_save` AHORA."

## Formato del contenido

Estructura canónica (obligatoria):

```
**What**: Una oración — qué se hizo.
**Why**: Qué lo motivó (pedido del usuario, bug, performance, etc.).
**Where**: Archivos o rutas afectadas.
**Learned**: Gotchas, edge cases, cosas que sorprendieron (omitir si no hay).
```

Ejemplo válido:

```
**What**: Se cambió el modelo del agente cerebro-auditor a Antigravity Gemini 3.1 Pro.
**Why**: El modelo anterior devolvía salida vacía al delegar bloques de auditoría.
**Where**: opencode.json (raíz del proyecto).
**Learned**: El config no se hot-reloada — requiere reiniciar opencode.
```

## Reglas de topic_key

- Tópicos distintos NO deben pisarse entre sí (ej: `bugfix` vs `decision` van separados).
- Si un tópico evoluciona (ej: decisiones de frontmatter), reutilizar el MISMO `topic_key` para hacer upsert en vez de crear observaciones duplicadas.
- Si no se sabe la key correcta: `mem_suggest_topic_key` primero y reutilizarla después.

## Recuperación (buscar antes de responder)

Ante "recordá", "qué hicimos", "cómo resolvimos", o referencias a trabajo previo:

1. `mem_context` — historial reciente de sesiones (rápido, barato).
2. Si no aparece: `mem_search` con keywords relevantes.
3. Si hay match: `mem_get_observation` para contenido completo sin truncar.

También buscar PROACTIVAMENTE al empezar una tarea que pueda haberse hecho antes.

## Cierre de sesión (obligatorio)

Antes de terminar ("listo", "done", fin de sesión) llamar `mem_session_summary` con:

```
## Goal
[Qué se estaba construyendo/analizando en esta sesión]

## Instructions
[Preferencias o restricciones del usuario descubiertas — omitir si no hay]

## Discoveries
- [Hallazgos técnicos, gotchas, aprendizajes no obvios]

## Accomplished
- [Items completados con detalles clave]

## Next Steps
- [Lo que queda pendiente para la próxima sesión]

## Relevant Files
- ruta/archivo — [qué hace o qué cambió]
```

NO es opcional. Si se omite, la próxima sesión arranca a ciegas.

## Post-compaction

Si aparece un mensaje de compactación o "FIRST ACTION REQUIRED":
1. `mem_session_summary` con el contenido del resumen compactado (persiste lo hecho antes de la compactación).
2. `mem_context` para recuperar contexto adicional de sesiones previas.
3. Recién entonces continuar trabajando.
