---
name: switch-context
description: Genera un resumen de entrega (handoff) para cambiar de LLM entre fases sin perder contexto ni reglas.
---

# Skill: Transición de Contexto entre Modelos (Handoff)

Genera un informe sintético para transferir la ejecución al siguiente modelo asignado en la matriz:

1. **Estado Actual:** Resumen exacto de los archivos creados/modificados en la fase que termina.
2. **Servidores MCP Utilizados:** Herramientas MCP consumidas durante el bloque.
3. **Siguiente Modelo Asignado:** Nombre del LLM para la próxima fase y su rol especifico.
4. **Instrucción de Continuidad:** Prompt listo para copiar y pegar en la sesión del nuevo modelo, incluyendo restricciones de TypeScript y null-safety.
5. **Registro:** Guarda este resumen en la sección correspondiente de `AI_LOG.md`.