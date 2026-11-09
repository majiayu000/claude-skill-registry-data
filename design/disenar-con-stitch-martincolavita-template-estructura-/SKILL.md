---
name: disenar-con-stitch
description: >-
  Diseñar las pantallas del producto con Google Stitch (por MCP o pegando el prompt): armar el brief
  desde la ficha del Cerebro (propósito, pasos, reglas, estados, glosario, tokens), generar la pantalla
  en Stitch, dejar que la persona la pula allá, exportar HTML y captura a borrador/disenos/, promover con
  un "sí" a entregables/disenos/ como maqueta vigente (fuente_maqueta en la ficha), llevar los tokens al
  design system y darle bajada al front por cerebro-architect-ui. Usar cuando se pida "diseñá la
  pantalla de X", "armá el diseño en Stitch", "pasá la ficha a Stitch", "exportá las pantallas",
  "/disenar-con-stitch". Sin PHI en prompts ni pantallas. No escribe código del front. Español
  (Argentina).
---

# Diseñar con Stitch

Stitch es donde **nace y se pule lo visual**. Esta skill no dibuja: convierte lo que el Cerebro ya sabe
de una pantalla en un brief que Stitch entiende, deja que la persona itere allá, y trae de vuelta la
maqueta como dato del Cerebro para que el front la baje. Setup y herramientas:
[[integracion-stitch-mcp/00-index]].

## Precondición

- Una **ficha de flujo** del Cerebro con `## Flujo` (los pasos), `## Reglas de negocio` y `## Pantalla`.
  Sin ficha no hay brief: una pantalla sin reglas detrás es un fake (G de `cerebro-architect-ui`).
- El MCP de Stitch registrado. Si no está, **modo manual**: la skill entrega el prompt listo para pegar
  en `stitch.withgoogle.com` y el resto del flujo es igual. Nunca se da por generado lo que no se vio.

## Flujo

1. **Brief desde la ficha** (sin preguntar lo que la ficha ya dice): plataforma (web o móvil), para
   quién, qué hace la pantalla (propósito), los **pasos** del flujo que ocurren en ella, **cada control
   con la regla que lo justifica** (`[RN-…]`), los **estados** (vacío, cargando, error, éxito, sin
   permiso), textos y avisos en español, el glosario (nombres exactos), y los **tokens** del design system
   si `diseno/diseno-sistema.md` ya los tiene. Datos de ejemplo con marcadores (`<persona>`, `<documento>`):
   **nunca** un dato real.
2. **Proyecto de Stitch**: uno por módulo. `list_projects` para reusarlo; `create_project` sólo si no
   existe, con el nombre del módulo.
3. **Generar**: `generate_screen_from_text` con el brief como prompt (se muestra el prompt antes, y se
   corre con el «sí»: gasta cuota). Una pantalla por pedido; variantes sólo si la persona las pide.
4. **Pulir en Stitch**: la persona itera en el canvas (variantes, voz, agente). La skill no insiste: espera
   que le digan «ésta».
5. **Exportar**: el HTML (`get_screen` / `get_screen_code`) y la captura (`get_screen_image`, o exportada a
   mano) a `borrador/disenos/<ficha>/<pantalla>.html` y `.png`, con el brief al lado (`brief.md`).
6. **Promover** con un «sí» a `entregables/disenos/<pantalla>.*`, escribir `fuente_maqueta` en la ficha y
   la línea en `log.md` (lo persiste `cerebro-curator`). Desde ese momento es **la maqueta vigente**: decide
   textos, botones, estados y orden de campos; si contradice una regla del Cerebro, **gana el Cerebro** y se
   avisa.
7. **Tokens al design system**: colores, tipografías y radios que salieron del diseño se proponen para
   `diseno/diseno-sistema.md` (con «sí»); `cerebro-mockup-design` revisa que ningún hexadecimal quede suelto.
8. **Bajada al front**: `cerebro-architect-ui` mapea cada control a su regla y produce la especificación;
   `redactar-tarea` arma las Tareas de front; el HTML exportado es **referencia**, no se pega tal cual: se
   adapta al stack (`DEC-003`) y al contrato.

## Salida

- `borrador/disenos/<ficha>/` con `brief.md`, el HTML y la captura; lo promovido en `entregables/disenos/`.
- La ficha con `fuente_maqueta` y, en `## Pantalla`, el brief resumido.
- Un veredicto: **OK** (pantalla exportada, citada y mapeada), **HALLAZGO** (un control sin regla, un
  estado sin diseñar, un dato real en el prompt), **SIN DATOS** (no hay MCP ni exportación a la vista).

## Barreras

- **Sin PHI** en prompts, pantallas, capturas ni briefs.
- **El Cerebro gana a la maqueta**; una maqueta que ninguna ficha cita no decide nada.
- **La cuota es de la persona**: cada generación se muestra antes y se corre con un «sí».
- **No escribe código del front** ni copia el HTML de Stitch al repo: eso es una Tarea con TDD.
- La API key vive en una variable de entorno; nunca en un archivo ni en el chat.
- Todo en español (Argentina).
