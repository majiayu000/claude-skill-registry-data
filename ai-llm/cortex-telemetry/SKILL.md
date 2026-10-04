---
name: cortex-telemetry
display_name: "Inspección & Telemetría Runtime de Transcripciones CORTEX"
description: "Extracción, análisis e inspección de telemetría runtime y logs de transcripción (transcript.jsonl). Dispara con \"telemetría\", \"cortex telemetry\", \"transcript logs\", \"historial de prompts\", \"analizar transcripciones\"."
---

# Habilidad: Cortex Telemetry (Auditoría de Historial)

Cuando el operador solicite extraer datos, estadísticas, contar prompts o ver palabras usadas en su historial, debes seguir este protocolo:

1. **Ubicación de Datos:** Los registros del usuario se encuentran en el patrón: `~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl`.
2. **Extracción:** Usa scripts de Python (ejecutados vía `run_command` en `/tmp/`) que iteren sobre estos archivos JSONL.
3. **Filtro de Input:** Filtra únicamente las líneas donde `"type" == "USER_INPUT"`.
4. **Fechas:** Utiliza la clave `"created_at"` (formato ISO 8601) si el usuario pide métricas desde una fecha concreta (ej. "desde diciembre").
## 5. Frecuencia de Palabras y Purificación de Input
Al calcular la frecuencia de palabras en los prompts, el Transductor **DEBE limpiar el ruido del sistema** antes de tokenizar.
- El campo `"content"` del archivo JSONL contiene metadatos inyectados automáticamente (ej. `<ADDITIONAL_METADATA>` o `<USER_SETTINGS_CHANGE>`).
- El script de Python debe extraer **únicamente** el texto que se encuentra dentro de las etiquetas `<USER_REQUEST> ... </USER_REQUEST>` (o eliminar mediante Regex cualquier bloque XML del sistema) para garantizar que el conteo refleje el vocabulario real del usuario, evitando falsos positivos de palabras en inglés introducidas por el Kernel.

## 6. Análisis Forense y Purgas Termodinámicas (C5-REAL)
Si el usuario percibe que faltan datos históricos, o solicita una "auditoría de purgas", el Kernel debe rastrear la aniquilación de entropía siguiendo estos vectores:
- **Git History:** Ejecutar `git log --oneline | grep -iE 'purge|purga|colapso|entrop|consolid'` en el monorepo para localizar los ciclos de `Octal Anergy Purge` o `Hyper-Colapso BFT`.
- **Ledger Actual (CORTEX-PERSIST):** Inspeccionar la base de datos `1_Operaciones_Activas/02_CORTEX_ENGINE/cortex-persist/cortex_ledger.db` (ej. tabla `bft_taint_log`) buscando los rastros de inyección BFT.
- **Legacy Ledgers:** En caso de que se busquen datos muy antiguos (ej. 2025), inspeccionar `~/.cortex/truth_ledger.db` (tabla `epistemic_ledger`) o `~/.cortex/cassandra_audit_ledger.jsonl`.
- **Interpretación:** Al presentar los resultados, explicar rigurosamente cómo el sistema trata la charla histórica como "Anergía Estocástica" que es destruida para consolidar código/conocimiento ("Exergía") de forma determinista, justificando así la pérdida de historiales de texto plano.

## 7. Perfilado Epistémico y Análisis Semántico
Tras extraer conteos de palabras o métricas, el Transductor NO debe limitarse a escupir listas de datos crudos. Debe ejecutar un análisis semántico que incluya:
- **Detección de Idioma / Entorno:** Evaluar el contraste entre idiomas (ej. Spanglish técnico) para deducir qué proporción del prompt es código/logs (generalmente en inglés) vs. directivas estructuradas (generalmente en español).
- **Extracción de Entidades y Modelos:** Señalar frecuencias anómalas o interesantes de herramientas específicas, nombres de proyectos (ej. Teorema, Robinson) o modelos LLM rivales (ej. opus, pro, flash).
- **Conclusión de Perfil Epistémico:** Emitir un resumen rápido sobre cómo está pensando y operando el usuario en base a la entropía inyectada.

---

## Autonomy Contract (Ω10 / Ω11 / Ω12)

> **ZERO PAUSE INVARIANT:** The Transducer SHALL NEVER pause execution to request Operator permission when this skill is triggered. Ambiguities MUST be resolved autonomously via `/grill-you` (Ω12) before any halt. Technical frictions MUST be resolved via the path of least thermodynamic resistance (Ω10). Refusal to execute when this skill matches the request constitutes C4-SIM Anergy (Ω11 violation).

- **Fallback Chain:** `~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl` -> `cortex_ledger.db` -> `truth_ledger.db`.
- **Degradation Mode:** If log file missing or corrupted, parse remaining available transcripts and emit partial metrics notice without halting.
- Auto-Trigger: Self-activates whenever user asks for prompt counts, word frequencies, historical telemetry, usage statistics, or temporal activity summaries (e.g. 'piensa en ayer', 'qué hice ayer', 'resumen de jornada').
