---
name: cortex-skill-genesis
display_name: "Génesis Autónoma de Skills CORTEX"
description: "Síntesis y generación automática de nuevos SKILL.md desde telemetría de sesiones y patrones observados. Dispara con \"generar skill\", \"skill genesis\", \"crear habilidad\", \"cortex skill genesis\"."
---

# Skill: Cortex Skill Genesis (Síntesis Predictiva de Skills)

Este protocolo analiza los patrones recurrentes de interacción en la telemetría de uso del sistema e identifica oportunas **transiciones de fase representacionales** para sintetizar de forma autónoma nuevos archivos `SKILL.md`.

---

## 1. Flujo de Generación Predictiva

```
Logs transcript.jsonl  --->  Filtrar prompts sin Skill activo  --->  Clusterización Semántica
                                                                            │
Borrador SKILL.md  <---  Axiomatizar Triggers & Workflow  <---  Si Frecuencia >= 3
```

1. **Escaneo de Vacíos**: Leer los registros `USER_REQUEST` en `transcript.jsonl` donde ninguna regla/skill fue disparado explícitamente.
2. **Clusterización Semántica**: Agrupar peticiones que comparten vector de intención o estructura de tarea.
3. **Criterio de Cristalización**: Si un cluster contiene $\ge 3$ repeticiones con una estructura común, se inicia el proceso de **Genesis**.
4. **Construcción del Borrador**:
   - Generar `name` descriptivo con guiones (ej. `rust-macro-diagnostics`).
   - Redactar `description` YAML con la regla unívoca `ACTIVA esta habilidad ante...`.
   - Definir la secuencia de pasos basada en la mejor resolución observada.
5. **Alineación con KERNEL**: Validar que el nuevo skill cumple con los axiomas de [KERNEL.md](file:///Users/borjafernandezangulo/.gemini/config/skills/KERNEL.md).

---

## 2. Plantilla Canónica de Salida

Todo skill generado por `cortex-skill-genesis` sigue la plantilla estándar del sistema:

```markdown
---
name: [nombre-del-skill]
description: [Descripción concisa]. ACTIVA esta habilidad ante peticiones de "[trigger_1]", "[trigger_2]" o [condición].
---

# Skill: [Título del Skill]

[Cuerpo explicativo con pasos deterministas y notación formal]
```

---

## 3. Integración con el Protocolo /learn

Las propuestas de `cortex-skill-genesis` se presentan siempre al operador mediante una propuesta estructurada de aprendizaje `/learn`, requiriendo confirmación antes de escribir el archivo en el sistema de archivos.
