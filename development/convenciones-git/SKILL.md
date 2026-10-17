---
name: convenciones-git
description: Convenciones de ramas y mensajes de commit de este proyecto. Usala siempre que vayas a crear una rama, escribir un mensaje de commit o commitear cambios.
when_to_use: Al crear una rama, al commitear, cuando el usuario pide "commiteá", "hacé un commit", "creá una rama" o pregunta cómo nombrar una rama o redactar un mensaje.
allowed-tools: Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git branch:*)
---

# Convenciones de Git

## Quién commitea

El trabajo con ticket lo commitea el **`delivery-specialist`**, que verifica el
árbol contra el ticket antes de escribir el mensaje. Los demás especialistas
dejan sus archivos en el árbol de trabajo y dicen qué cambiaron.

La sesión principal y el arquitecto commitean por su cuenta: documentación, ADR
y configuración están fuera del circuito de tickets a propósito.

## Antes de commitear

1. Revisá `git status` y `git diff` completos. No commitees a ciegas.
2. Verificá que no entren secretos, claves, correos ni rutas absolutas.
3. Confirmá que los cambios corresponden a **una sola intención**. Si hay dos,
   son dos commits.

Recién con esto en orden, escribí el mensaje.

## Tipos

Toda rama y todo commit se clasifican con uno de estos once tipos:

| Tipo | Cuándo |
| ---- | ------ |
| `feat` | Funcionalidad nueva |
| `fix` | Corrección de un error |
| `refactor` | Cambio interno sin alterar el comportamiento |
| `style` | Interfaz, estilos, experiencia de uso |
| `docs` | Documentación |
| `chore` | Mantenimiento que no encaja en los demás (dependencias, configuración) |
| `test` | Pruebas |
| `ci` | Integración continua |
| `build` | Sistema de build o dependencias externas |
| `perf` | Mejoras de rendimiento |
| `revert` | Revertir un commit anterior |

Siempre en minúscula, tanto en la rama como en el commit.

## Los tipos también titulan los issues

Un ticket y el commit que lo cierra describen el mismo trabajo, así que el título
de un issue usa **la misma convención que el título del commit** (ver más abajo):
`tipo(alcance): mensaje breve`. Ver `docs/agents/issue-tracker.md`.

## Nombre de rama

```
<tipo>/<número-de-ticket>-<descripción-en-kebab-case>
```

El número es el del ticket que **abre** la rebanada — si la rebanada cubre
varios tickets, va solo el primero; los demás quedan referenciados en los
commits, no en el nombre de rama. La descripción va **en inglés**, en
minúsculas, con guiones, y nombra **el alcance del trabajo**, no la tarea
puntual.

Ejemplos: `feat/29-curated-content-import` · `fix/31-catalog-search` ·
`docs/40-architecture-adr` · `style/26-hero-card`

Las ramas que ya existen con el formato viejo (sin número, o con descripción en
español, o con `bugfix`/`design` como tipo) no se renombran: la regla rige
desde acá en adelante, para las ramas nuevas.

## Mensaje de commit

**Título:**

```
tipo(alcance): descripción corta en minúscula
```

- El tipo es uno de la tabla de arriba, en minúscula, sin corchetes.
- El alcance va entre paréntesis y nombra el módulo o área que toca el commit
  (`catalogo`, `moderacion`, `aprendizaje`, `progreso`, `identidad`, `db`,
  `web`, `contenido`, `config`…). Si el commit no cae en un área puntual, se
  omite el alcance: `tipo: descripción`.
- La descripción va en minúscula y dice qué se hizo, sin punto final.

**Descripción:** dice exclusivamente dos cosas, en este orden, **en español y
en ítems**.

1. **Listado de las cosas que cambiaron.**
2. **Razones por las que estas cosas cambiaron.**

Nada más: ni instrucciones de uso, ni planes a futuro, ni comentarios.

**Sin sujeto.** Cada ítem describe el cambio, no a quien lo hizo: nunca "hice",
"agregué" ni "el agente implementó". Se redacta en impersonal o pasiva
refleja —"se estableció", "se agregó", "se corrigió", "quedó resuelto"—, porque
el commit documenta el estado del árbol, no la autoría de una sesión.

**Referencia al ticket:** si el commit corresponde a un ticket, cerrá el
mensaje con una última línea que lo referencie.

```
Ticket: #12
```

Es una **referencia, no un cierre**. No uses `Closes #12` ni `Fixes #12`: esas
palabras hacen que GitHub cierre el issue solo al publicar, y en este proyecto
el cierre es explícito y tiene una condición —el PR que trae el commit tiene
que estar mergeado en `development`—.

## Ejemplo

Rama: `feat/29-curated-content-import`

```
feat(contenido): importación de contenido desde archivos

Cambios:
- Se agregó el script de importación que lee `contenido/` y escribe en la
  base.
- Se validó cada ficha contra el descriptor Zod de su tipo.
- Se agregó su comando en `package.json`.

Razones:
- El contenido curado vive en archivos versionados (ADR 0004) y hacía falta
  el paso que lo lleva a la base, que es lo que sirve la aplicación.
- Validar en la importación evita que entre contenido que no cumple el
  esquema del tipo.

Ticket: #12
```
