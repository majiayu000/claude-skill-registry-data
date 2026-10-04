---
name: qwen-prompting
description: Use when changing how suspects are prompted or sampled - Ollama parameters (temperature, num_ctx, keepAlive, maxTokens), system prompt wording, nudges or retries in AIConversationManager/PromptBuilder, or switching to a smaller or different model.
---

# Prompts y parámetros de qwen2.5:7b-instruct

Ningún parámetro de Ollama ni frase del prompt cambia sin un A/B medido (ver la skill `calibration-run`). La capa de proveedores no se toca; solo los parámetros, y con datos.

## Valores actuales y su porqué

| Valor | Dónde | Por qué |
|---|---|---|
| temperature **0.6** | `AIConversationManager.DefaultTemperature` **y** `Game.unity` (la escena manda) | Frente a 0.4: 9/12 frente a 6/12 pistas, 73 % frente a 68 % de detección y más variedad. A 0.4 resume y pierde detalles. Por encima de 0.6 no hay medida. |
| num_ctx **8192** | `OllamaProvider`, el mismo en la precarga y en cada petición | Si no coinciden, Ollama recarga el modelo. |
| keepAlive **"60m"** | `OllamaProvider` | Sin unidad da HTTP 400. |
| maxTokens 250, historial 16 mensajes | `AIConversationManager` | ~1219 tokens de ficha más historial. |
| Reintento de hora a **0.3** (`CoolTimeRetry`) | | 10/11 frente a 5/9 arreglados, misma latencia |
| `StrictTimeNudge` **apagado** | | A/B no concluyente (3 → 1 aviso en 347 respuestas) |

## Reglas

- Lo que cambia (día, prueba mostrada) va **al final** del prompt de sistema. Ollama reutiliza el prefijo: 271 ms la primera vez, 10 ms después.
- Un reintento por tipo de fallo (repetición, idioma, primer contacto, hora), como mucho 2 llamadas extra. Al encadenarlos se conserva el empujón de variedad.
- Un modelo más pequeño no sustituye al 7B sin medirlo antes con la sonda de premisas y la calibración de pistas:

  | Modelo | Premisas falsas aceptadas | Pistas |
  |---|---|---|
  | 1.5B | 72 % | 15/48 |
  | 3B | 18 % | 22/48 |
  | 7B | 2-5 % | 36-39/48 |

- La misma temperatura llega también a `AnthropicProvider`.

## Si te piden subir la temperatura para que hablen "más creativos"

1. Mide antes: ClueCalibrator con la temperatura nueva contra la de 0.6, y el bot con la misma semilla.
2. Con +0.25, un reintento a 0.9 llega al tope de 1.0.
3. A más temperatura suben el chino, las horas inventadas y bajan las pistas.
4. Propón antes un cambio de `speech` o `speechExample`.
