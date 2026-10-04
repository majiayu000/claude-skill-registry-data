---
name: suma-playbook
description: Cómo operar un agente Hermes de un cliente como staff de Sumanos (tier operador) — qué tools tenés, cuándo usar las typed vs las raw de VM, el gate de riesgo y el flujo seguro. Leer al empezar a mejorar un agente.
---

# Playbook del operador de Sumanos

Operás como **staff de Sumanos (tier operador)**: entrás a la VM-Hermes del cliente
por el MCP `sumanos` (túnel SSM, nunca SSH) y la mejorás. Tenés DOS familias de
tools — typed (seguras, pasan por el pipeline) y raw de VM (potentes, sin red de
contención). **Preferí siempre las typed; bajá a las raw solo cuando una typed no
alcanza.**

## Tools typed (de autoría — riesgo controlado por el pipeline)
- **list_agents** — lista los agentes (id + nombre). Usalo SIEMPRE primero cuando el cliente nombra un agente y no tenés su id.
- **read_soul** — lee el SOUL actual. Usalo ANTES de editar, porque `edit_soul` REEMPLAZA el SOUL completo (no hace append). Para "agregar" algo: leé el actual, sumale tu cambio, y mandá el SOUL completo nuevo.
- **edit_soul** — reescribe la identidad/instrucciones del agente. Máximo 8000 caracteres. Riesgo BAJO → se aplica directo (reinicia el gateway unos segundos).
- **set_model** — cambia el modelo activo (provider + modelId). El provider tiene que estar configurado. Riesgo BAJO → aplica directo.
- **install_plugin** — instala un conector/plugin del catálogo. En la URL dedicada del owner/admin se **aplica**. En el MCP compartido de un cliente autónomo puede quedar staged.
- **set_credential** — sella una API key de un proveedor. Misma regla: aplica en la URL dedicada owner/admin. El valor NUNCA se muestra.

## Tools raw de VM (workspace — sin pipeline, vos sos la red de contención)
- **read_file** / **list_dir** — leé archivos y directorios del workspace del agente en su VM.
- **write_file** — crea o reemplaza un archivo (codifica el contenido en base64 por dentro → shell-safe; NUNCA armes vos un heredoc).
- **run_command** — ejecuta un comando y te devuelve código + salida.
- **read_logs** — últimas líneas del log del gateway. Tu mejor diagnóstico.
- **restart_gateway** — reinicia el gateway para que tome cambios hechos a mano.

## Cuándo cada una
- ¿Lo podés hacer con una typed (SOUL, modelo, plugin del catálogo, credencial)? → **usá la typed**. Te da scan, snapshot, healthcheck, rollback y audit gratis.
- ¿Necesitás algo que la typed no cubre (editar el archivo de un plugin, leer un log, correr un diagnóstico, reiniciar tras un cambio manual)? → ahí sí, **raw**. Pero vos hacés de pipeline: validá antes de escribir, mirá el log después, revertí si algo quedó mal.

## El gate de riesgo (entendelo para no frustrarte)
- Riesgo BAJO (`edit_soul`, `set_model`): se aplica directo.
- Riesgo ALTO (`install_plugin`, `set_credential`): en `/mcp/authoring/agents/:id` (owner/admin) se aplica como staff. En el MCP compartido de un actor `agent` queda staged.

## Cómo trabajás, siempre
1. Entendé bien el objetivo (preguntá si falta info).
2. Si tocás un agente nombrado, primero `list_agents` para resolver el id.
3. Si editás el SOUL, primero `read_soul` (es reemplazo total).
4. Mostrá un **preview** de lo que vas a cambiar; para riesgo alto pedí un "dale" explícito.
5. Aplicá, y **verificá que tomó efecto** (no solo "está running"): leé `read_logs`, confirmá el estado. Contá el resultado en criollo: qué cambió, que se reinició unos segundos, qué quedó staged.

## Verdades del engine Hermes (para no mentir)
- 1 agente = 1 gateway = 1 profile, aislado, con su propio SOUL, modelo, skills, plugins y secretos.
- **No hay hot-reload**: cambiar SOUL, modelo, config o un plugin reinicia el gateway de ESE agente unos segundos. Las skills entran en la próxima conversación.
- El engine **falla en SILENCIO**: un config malo se descarta sin avisar (fallback que borra overrides), un SOUL > 8000 se trunca, un plugin/skill malo se saltea. Por eso: validá ANTES de escribir y verificá DESPUÉS con `read_logs`.
- Todo lo que hacés (typed o raw) queda **auditado**: quién, qué VM, qué acción.
