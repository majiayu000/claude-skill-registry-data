---
name: macos-lulu-firewall-diagnostics
display_name: "Diagnóstico de Firewall & Sockets macOS (LuLu / Little Snitch)"
description: "Diagnóstico de reglas de red local, sockets y firewall en macOS (LuLu / Little Snitch). Dispara con \"lulu firewall\", \"little snitch\", \"redes macos\", \"diagnóstico firewall\"."
---

# LuLu Firewall Diagnostic Protocol

Cuando el usuario comparta una alerta del firewall LuLu o Little Snitch bloqueando una conexión en macOS, ejecuta este protocolo para diagnosticar la legitimidad del tráfico:

## Fase 1: Identificación del Proceso y la IP
1. **Extraer el Proceso:** Identifica el binario que intenta la conexión (ej. `wasm-pack`, `cargo`, `node`, `python`, `curl`).
2. **Extraer la IP/Dominio Destino:** Identifica hacia dónde se intenta conectar.

## Fase 2: Verificación de Infraestructura (Fastly / CDNs)
- Si la IP de destino pertenece al rango `151.101.x.x` (Fastly CDN) y el proceso es una herramienta de compilación (como `wasm-pack` o `cargo`), clasifícalo como tráfico legítimo hacia el registro de paquetes (ej. `crates.io` o `registry.npmjs.org`).
- Para IPs desconocidas, utiliza la herramienta `run_command` con `whois <IP>` o busca la IP para determinar su ASN y propietario (ej. AWS, GCP, Cloudflare).

## Fase 3: Evaluación de Causalidad
- Cruza la identidad del binario con la infraestructura destino.
- Si el binario necesita la conexión para funcionar (ej. descarga de dependencias), determina que es un **Falso Positivo**.
- Si el binario es sospechoso o la conexión no tiene correlación con su propósito, evalúa un posible riesgo de exfiltración.

## Fase 4: Reporte (Brutalist Protocol Ω8)
- Emite un reporte en formato Brutalista indicando:
  - **Proceso:** [Nombre]
  - **Identidad/Uso:** [Descripción]
  - **Destino IP/CDN:** [Propietario]
  - **Causa Operativa:** [Por qué se conecta]
  - **Directiva de Acción:** Recomendar explícitamente "Permitir" o "Bloquear".
