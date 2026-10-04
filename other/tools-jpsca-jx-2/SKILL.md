---
title: Skill de Claude
description: Skill de Claude para generar componentes Jx a partir de descripciones en lenguaje natural
---

El ["skill" de Claude](https://jx.scaletti.dev/skill.zip) te ayuda a generar componentes Jx a partir de descripciones en lenguaje natural. Puedes usarlo en [Claude Web](https://claude.ai){target="_blank"} o en [Claude Code](https://claude.ai/code){target="_blank"}.

## Instalación

### Claude Web

Ve a la [página de Skills de Claude](https://claude.ai/customize/skills){target="_blank"}, haz clic en "+" > "Create a skill" -> "Upload a skill" y arrastra el archivo zip descargado desde [jx.scaletti.dev/skill.zip](https://jx.scaletti.dev/skill.zip).

![Instalación del skill en Claude Web](/assets/images/claude-web-install.png)

### Claude Code

Para instalar el skill, descárgalo desde [jx.scaletti.dev/skill.zip](https://jx.scaletti.dev/skill.zip) y descomprímelo dentro de tu carpeta `.claude/skills`. Si no tienes una carpeta `skills`, debes crearla primero.

## Uso

Una vez instalado, puedes usar el skill invocándolo en una conversación con Claude. Por ejemplo, en Claude Code, puedes escribir:

```bash
✦ ❯ claude
╭─── Claude Code v5.6.789 ───────────────────────────╮
│                                                    │
│                       ▐▛███▜▌                      │
│                      ▝▜█████▛▘                     │
│                        ▘▘ ▝▝                       │
╰────────────────────────────────────────────────────╯

❯  Crea un componente Jx que muestre la tarjeta de perfil de\
   un usuario con su nombre, avatar y bio.

... ✨ Sucede la magia ✨ ...
```

Claude detecta el skill a partir de tu prompt y usa su conocimiento empaquetado de los idioms de Jx — importaciones explícitas, props tipadas, pasada de atributos con `attrs`, CSS/JS por componente — para escribir el archivo `.jx` por ti. No necesitas escribir un slash command ni un prefijo especial; basta con que describas lo que quieres.

## Qué sabe el skill

El skill cubre dos áreas:

**Autoría de componentes.**: Botones, tarjetas, modales, dropdowns, formularios, tablas, layouts, navegación, acordeones, toasts y otros elementos básicos de UI. Sigue un enfoque de "HTML nativo primero".

**Mecánica de la librería.** Cómo configurar un `Catalog`, registrar carpetas con prefijos, integrar con Flask / Django / FastAPI / htmx, etc.

Ejemplos de prompts:

- *"Hazme un componente de notificación toast con variantes `success`, `error` e `info` y auto-cierre después de 5 segundos."*
- *"Crea un layout de sidebar que se colapse en un drawer deslizante en móvil."*
- *"Muéstrame cómo compartir el `jinja_env` de Flask con un Catalog de Jx."*
- *"¿Por qué `<Button {{ attrs.render() }} />` no funciona cuando paso los attrs a un componente hijo?"*
- *"¿Cómo ejecuto `jx check` en CI y hago que falle el build si hay errores?"*

No necesitas mencionar "Jx" explícitamente en cada mensaje — una vez que el skill se carga, Claude lo mantiene activo durante los turnos siguientes de la misma conversación.

## Actualizar el skill

Para incorporar nuevas versiones del skill, vuelve a descargar `skill.zip` desde [jx.scaletti.dev/skill.zip](https://jx.scaletti.dev/skill.zip) y:

- **Claude Web** — ve a la [página de Skills](https://claude.ai/customize/skills){target="_blank"}, elimina el skill `jx` existente y vuelve a subir el nuevo zip.
- **Claude Code** — reemplaza el contenido de la carpeta `.claude/skills/jx/` con el nuevo.

El skill está versionado junto con la documentación, así que cada nuevo release de Jx incluye un skill actualizado que refleja la API actual.
