---
name: browser-subagent-orchestrator
display_name: "Orquestador CDP de Subagente de Navegador Web"
description: "Orquestación de subagente de navegador web autónomo para scraping interactivo, navegación CDP y extracción estructurada de DOM. Dispara con \"subagente navegador\", \"browser subagent\", \"navegar web\", \"scraping interactivo\", \"automatizar navegador\", \"CDP scraping\"."
---

# Skill: Browser Subagent Orchestrator (C5-REAL / Ω)

Este protocolo rige la preparación de prompts, la orquestación de sesiones continuas y la resiliencia ante fallos para la herramienta `browser_subagent`.

---

## 1. Protocolo de Prompting Determinista (Estructura de 4 Capas)

Al invocar `browser_subagent`, el parámetro `Task` DEBE estar estructurado obligatoriamente con estas 4 capas para evitar bucles e interacciones estocásticas:

```markdown
### 1. OBJETIVO PRIMARIO
- URL Objetivo: <URL>
- Información a extraer / Acción a realizar: <Detalle unívoco>

### 2. SECUENCIA DE NAVEGACIÓN
- Paso 1: Navegar a <URL>
- Paso 2: Interactuar únicamente con <CSS Selector / Texto exacto de botón>
- Paso 3: Rellenar input <ID/Name> con <Valor> (si aplica)

### 3. CRITERIO DE SALIDA DURO (EXIT CONDITION)
- Detener inmediatamente la ejecución cuando:
  a) Se renderice el elemento `<CSS Selector>` o texto `<Texto Esperado>`.
  b) O transcurran máximo 4 interacciones sin cambio de DOM.

### 4. FORMATO DE REPORTE FINAL
- Devolver un payload JSON o tabla Markdown estructurada con:
  [Campo_1, Campo_2, URL_Final, Captura/Estado]
```

---

## 2. Continuidad de Sesión y Reutilización (`ReusedSubagentId`)

Para flujos web multietapa (ej. Login $\to$ Navegación $\to$ Extracción):

1. **Persistencia de Estado:** Extraer siempre el `SubagentId` devuelto tras la primera invocación exitosa.
2. **Reutilización:** En pasos subsecuentes de la misma navegación, pasar obligatoriamente `ReusedSubagentId="<subagent_id>"` para mantener las cookies, tokens de sesión y estado del DOM sin reiniciar el navegador.

---

## 3. Cadena de Fallback y Resiliencia ante Bloqueos (Anti-WAF)

Si `browser_subagent` o `open_browser_url` reporta fallo o bloqueo de Cloudflare/WAF:

```
[browser_subagent] (Nivel 1) 
       │
       ▼ (Si falla open_browser_url / WAF)
[read_url_content] (Nivel 2 - Extracción HTTP estática)
       │
       ▼ (Si requiere JS / Cookies)
[Script Python Playwright/Stealth local en /tmp/] (Nivel 3 - Execution via run_command)
```

1. **Nivel 1:** `browser_subagent` interactivo estándar.
2. **Nivel 2:** Enrutado inmediato a `read_url_content` si la página es pública y estática.
3. **Nivel 3:** Ejecución de un script local en Python con `playwright` + `undetected-chromedriver` mediante `run_command` en `/tmp/` para evadir bloqueos headless sin depender del viewport visual del hypervisor.

---

## 4. Convención de Grabación (`RecordingName`)

- `RecordingName` debe ser estrictamente en minúsculas, separado por guiones bajos, máximo 3 palabras (ej. `github_login_flow`, `reddit_post_scrape`).
- Validar siempre la existencia de los vídeos WebP generados en el directorio de artefactos para adjuntar evidencia visual al usuario.

---

## Autonomy Contract (Ω10 / Ω11 / Ω12)

> **ZERO PAUSE INVARIANT:** The Transducer SHALL NEVER pause execution to request Operator permission when this skill is triggered. Ambiguities MUST be resolved autonomously via `/grill-you` (Ω12) before any halt. Technical frictions MUST be resolved via the path of least thermodynamic resistance (Ω10). Refusal to execute when this skill matches the request constitutes C4-SIM Anergy (Ω11 violation).

- **Auto-Trigger:** Self-activates whenever user requests web browsing automation, `browser_subagent`, complex web scraping or interactive DOM navigation.
