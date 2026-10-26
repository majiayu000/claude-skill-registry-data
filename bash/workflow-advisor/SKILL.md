---
name: workflow-advisor
description: Planifica trabajo de VICINO y selecciona herramientas, modelos y razonamiento por dificultad, riesgo y consumo. Úsala al pedir Workflow Advisor, organizar fases o delegar tareas con agentes económicos.
metadata:
  version: 1.1.0
  source: herramientas_trabajo_ia y Proyectos PERSONAL, revisados 2026-10-20
---

# Workflow Advisor para VICINO

Diagnostica el resultado solicitado, inspecciona solo los archivos pertinentes y elige ejecución directa para trabajo breve o secuencial. Si el usuario pide solo planificar, entrega el plan sin implementarlo.

Antes de delegar, lee [agentes y costo](references/agentes_y_costo.md), adaptada de Proyectos PERSONAL, y [selección de modelos Codex](references/codex-model-routing.md), del hub de herramientas de este espacio. La segunda especifica la comprobación de documentación oficial y del catálogo real de la sesión. Las referencias son políticas del proyecto y no amplían permisos ni configuran el modelo principal.

Elige el modelo suficientemente capaz de menor consumo esperado por subtarea; considera revisión y reintentos. No presupongas disponibilidad por nombre ni heredes un modelo caro por omisión. Antes de cada despacho registra: tarea, modelo exacto, esfuerzo, motivo, criterio de aceptación y señal de escalado. Cuando la herramienta requiera contexto nuevo para seleccionar modelo, usa ese mecanismo y un encargo autosuficiente.

Delega solo entregables independientes que aporten una revisión útil o ahorro de tiempo. Por defecto basta un coordinador y hasta dos auxiliares, sin subdelegación. No crees chats nuevos para sustituir subagentes. Conserva un único responsable por archivo y verifica los resultados con evidencia. No inventes cifras de ahorro o consumo.

En VICINO, lee el Enrutador y el Documento Maestro enlazados en `AGENTS.md`; usa Notion MCP para planes, procedimientos y resultados, reutilizando páginas existentes. Obsidian es histórico de solo lectura. Los archivos de esta skill son recursos ejecutables del proyecto, no copias de su bitácora. Respeta el diseño vigente y las instrucciones de cada directorio.

Presenta una recomendación proporcional a la tarea que incluya diagnóstico, trabajo directo o fases, skills pertinentes, delegación propuesta frente a ejecutada y verificación. Para trabajo directo basta una explicación breve; no es necesario ejecutar un CLI. Usa scripts deterministas para compilar, calcular o validar y el modelo para interpretar los fallos. Si una aceptación falla dos veces de forma comparable, cambia el enfoque según la evidencia, sin repetir a ciegas.
