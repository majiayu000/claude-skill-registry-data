---
name: sumanos-capabilities
description: Catálogo de canales/conectores y modelos de Sumanos — qué se puede instalar en un agente Hermes y qué modelo elegir. Usar al construir o mejorar un agente.
---

# Capacidades de Sumanos: canales, conectores y modelos

> Portado del corpus de entrenamiento de autoría (`core/builder/src/builder-skills.ts`,
> skill `sumanos-capabilities`). Mantener en sync con esa fuente.

## Conectores / canales disponibles (catálogo)
El agente se conecta a un canal con `install_plugin <ref>` (riesgo alto → queda staged para aprobación humana). Los del catálogo:
- `whatsapp-web` — WhatsApp.
- `telegram` — Telegram.
- `slack` — Slack.
- `discord` — Discord.
- `chatwoot` — Chatwoot (mesa de ayuda / inbox omnicanal).

MCP del catálogo:
- `web-fetch` — permite al agente leer páginas web.

Si el cliente pide un canal que no está en el catálogo, decilo con amabilidad y ofrecé el más cercano; no inventes un conector que no existe.

## Modelos (proveedores y cuándo usar cada uno)
Cambiás el modelo con `set_model(provider, modelId)`. El provider tiene que estar configurado (key o cuenta).
- `openai-codex` — la cuenta ChatGPT del cliente (sin API key). Modelos: gpt-5.5, gpt-5.4, gpt-5.4-mini, gpt-5.3-codex. Buen default si tiene ChatGPT.
- `openai` — API key de OpenAI. Modelos típicos: gpt-4.1, gpt-4o, gpt-4o-mini.
- `anthropic` — Claude. Modelos: claude-opus-4-8 (más capaz), claude-sonnet-4-6 (equilibrado), claude-haiku-4-5-20251001 (rápido y barato).
- Otros (openrouter, gemini, xai, glm, zai, minimax): según la key que tenga el cliente.

Regla: elegí el modelo según lo que el cliente YA tiene configurado. Si no hay provider configurado, primero hay que sellar la key con `set_credential` (riesgo alto → staged).
