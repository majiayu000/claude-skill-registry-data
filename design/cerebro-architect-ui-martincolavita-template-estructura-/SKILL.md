---
name: cerebro-architect-ui
description: >
  Analiza maquetas y prototipos visuales del proyecto (exportaciones de Stitch en HTML o PNG, Figma, HTML a mano) y los traduce a
  especificaciones técnicas, mapeando CADA control a su regla de negocio del OKF con wikilink.
  Trae los guardarraíles que impiden fake toggles, botones cosméticos, estados visuales
  huérfanos y reglas sin UI, más la trazabilidad inversa: toda RN del módulo tiene que tener
  un componente que la materialice.
  Trigger: "diseñá la UI de esta pantalla", "validá esta maqueta contra las reglas",
  "revisá este mockup", "pasá este diseño a spec técnica", "¿este toggle tiene regla?".
  NO genera el HTML del mockup (eso es cerebro-mockup-design) ni escribe código de
  componentes (eso es desarrollo).
license: Apache-2.0
metadata:
  author: equipo
  version: "2.0"
---

## Cuándo se usa

Cuando hay que evaluar una interfaz, un prototipo o una maqueta y asegurar que esté alineada
con el Cerebro Digital **antes** de escribir código.

## Principio rector

**Todo control visual mapea a una regla de negocio documentada en el OKF.**

- Un control **sin** regla que lo respalde → **no debe existir**.
- Una regla **sin** control que la materialice → **falta UI**.

Las dos direcciones se chequean. La segunda es la que más se saltea.

## 📋 Flujo de análisis y trazabilidad

1. **Lectura de maquetas** — archivos HTML, CSS, SVG o diseños en `entregables/disenos/` y
   `entregables/presentaciones/` (presentaciones en HTML). Ahí viven los artefactos ya
   promovidos desde `borrador/`.
2. **Mapeo funcional con wikilinks** — correlacionar cada botón, formulario y campo visible con
   su regla de negocio del OKF (`[[regla-negocio]]`).
3. **Definición de componentes (Atomic Design)** — átomos, moléculas y organismos.
4. **Generación de la especificación técnica** — en `entregables/especificaciones-tecnicas/`:
   qué APIs consumir, qué validaciones de front aplicar y qué comportamientos reactivos se
   esperan. **El código de la aplicación no vive en este repositorio** (`DEC-001`): la spec
   viaja acá y el repo de código hermano la referencia por ruta, no la copia.

## 🚫 Anti-patrones — prohibidos

| Anti-patrón | Qué es | Cómo se detecta |
|---|---|---|
| **Fake toggle** | Interruptor o botón que no persiste ni cambia estado real | No tiene una `RN-xxx` asociada, o al accionarlo no cambia ningún dato del dominio |
| **Botón cosmético** | Acción visible que no dispara ninguna operación | No hay flujo en el OKF que lo justifique |
| **Estado visual huérfano** | Un estado de UI (gris, deshabilitado) sin equivalente lógico | No existe regla que defina cuándo el elemento se deshabilita |
| **Regla sin UI** | Regla del OKF que ningún componente materializa | La regla existe y no aparece en pantalla |
| **Hardcode de estado** | Estado fijo en el código sin consultar el dominio | El componente no lee datos de negocio para decidir su estado |

## Cómo se valida

**Paso 1 — Inventariar las reglas.** Para la pantalla en cuestión, listar las `RN-xxx` del
bundle (`contexto.md`, el módulo, `fuentes.md`) que aplican.

**Paso 2 — Mapear cada control a su regla**, en una tabla: componente · regla del OKF ·
estado según la regla.

> **La trampa de este paso.** Una cita que **simula respaldo** es peor que no citar nada:
> pasa la revisión. Toda `RN-xxx` que se escriba en esa tabla se abre y se lee. Si no dice lo
> que se le atribuye, el hallazgo es la cita, no el componente.

**Paso 3 — Trazabilidad inversa.** Toda RN del módulo tiene que tener al menos un componente
que la materialice. Si sobra una RN sin UI, se reporta como hueco.

**Paso 4 — Checklist.**

- [ ] Cada toggle, botón y checkbox mapea a una RN del OKF, con wikilink.
- [ ] Ningún control está hardcodeado: lee el estado del dominio.
- [ ] Los estados deshabilitados o visibles corresponden a condiciones documentadas.
- [ ] No hay fake toggles: todo cambio de estado persiste.
- [ ] Toda RN del módulo tiene UI que la materialice.
- [ ] **Cada `RN-xxx` citada se abrió y dice lo que se le atribuye.**

## 🛡️ Reglas de validación visual

- **Consistencia de estados** — que los estados de los botones correspondan a la lógica de
  negocio (ej.: *"Confirmar"* inhabilitado si falta un dato obligatorio).
- **Trazabilidad bidireccional** — la especificación generada enlaza de vuelta a las reglas
  aprobadas del OKF, para que el analista y el programador entiendan el **porqué** de cada
  componente.

## Cómo se reporta

```
⚠️ [Componente] viola el guardarraíl [anti-patrón]:
- Regla esperada: RN-MOD-00X (wikilink a la nota)
- Estado actual: [descripción]
- Corrección sugerida: [acción]
```

**La corrección prioriza SIEMPRE la regla del OKF por sobre la maqueta.** Si la maqueta
contradice una regla verificada, la que está mal es la maqueta.
