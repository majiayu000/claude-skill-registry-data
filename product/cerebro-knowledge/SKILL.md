---
name: cerebro-knowledge
description: >
  Directivas de consulta obligatoria del Cerebro Digital (OKF) del proyecto: qué se lee, en qué
  orden y cómo se cita. Trigger: cualquier pregunta sobre el dominio, una regla de negocio, una
  decisión, un pendiente o el estado de avance del proyecto.
license: Apache-2.0
---

## Cuándo se usa
- Preguntas sobre el dominio del proyecto {{PROYECTO}}: reglas, flujos, estados, roles, integraciones, decisiones, pendientes.
- Antes de redactar cualquier ticket, spec o mockup que cite una regla `[RN-…]` o una decisión `[DEC-…]`.

## Fuente de conocimiento
LEER DIRECTAMENTE los archivos del bundle OKF en `cerebro-digital/`, con la herramienta nativa de lectura del entorno, de forma ordenada:

1. **`index.md`** — el mapa: qué módulos hay y dónde está cada cosa. **REGLA CLAVE:** antes de buscar un dato de un módulo, leé el `index.md` de su pilar (`funcional/`, `metodologia/`, `arquitectura/`) para saber en qué ficha está.
2. **`contexto.md`** — origen del proyecto, organización, producto, alcance y equipo.
3. **La ficha del pilar** que corresponda:
   - `<modulo>/funcional/<ficha>.md`: reglas de negocio (`RN-<MOD>-nnn`), flujos y pantallas.
   - `<modulo>/arquitectura/decisiones.md` y `esqueleto-proyectos.md`: decisiones (`DEC-nnn`) y estructura técnica.
   - `<modulo>/metodologia/`: cómo trabaja el equipo.
   - `<modulo>/aplicacion/`: lo que **existe y se aprendió** construyendo la aplicación: `mapa.md` (qué módulos hay, qué exponen, qué Historias los construyeron, en qué estado están), `aprendizajes.md` (`AP-nnn`) y `deuda.md` (`DT-nnn`). Es lo primero que se abre antes de tocar un módulo que ya existe.
4. **`<modulo>/pendientes.md`** — lo que todavía no está decidido (`P-nnn`). Si la respuesta está ahí, la respuesta es «está pendiente», no una suposición.
5. **`fuentes.md`** — de qué documento de origen sale cada regla, por si hace falta citarlo.
6. **`roadmap.md`** — estado de avance del análisis y del desarrollo.
7. **`configuracion-ia/agentes.md`** — perfiles y checklists del ecosistema.

## Reglas
- **Citar por ruta**, nunca copiar la ficha entera en la respuesta: `cerebro-digital/<modulo>/funcional/<ficha>.md § RN-MOD-003`.
- **No inventar.** Un concepto que no está en el OKF se responde como «pendiente por el equipo funcional», con la pregunta propuesta para `pendientes.md`. Una regla `[RN-…]` se cita sólo si existe, y después de abrirla y leer que dice lo que se le atribuye.
- **Una ficha por vez** cuando se consulta desde un repositorio de código (skill `consultar-cerebro`): el desarrollo es autosuficiente con la Tarea; el Cerebro se abre sólo si hace falta el porqué.
- **Lo que se detecta como conocimiento nuevo o cambiado en la conversación** no se escribe acá: se dispara la Consulta Interactiva de Decisión de `cerebro-orquestador`.
