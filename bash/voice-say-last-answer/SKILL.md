---
name: voice-say-last-answer
description: Lee en voz (Mónica / español) la última respuesta completa del asistente usando un archivo temporal y scripts/voice-tts-file.sh. Usar cuando el usuario pida escuchar la última respuesta, TTS de la respuesta anterior, o “voice say last”.
---

# Voice — última respuesta del agente (macOS, voz Mónica)

## Cuándo usar

- El usuario quiere **oír en altavoz** lo que acaba de responder el asistente, o la **última respuesta completa** del agente en el hilo.
- Frases típicas: “léelo en voz”, “Monica voice last answer”, “speak the last response”, “npm voice last”, “lee la última respuesta”.

## Reglas obligatorias

1. **Fuente del texto:** usar la **última intervención completa del asistente** (mensaje `assistant`) **anterior** al mensaje actual del usuario que dispara esta acción. Si el usuario señala otra vuelta (“la respuesta de hace dos mensajes”), usar esa.
2. **No acortar** salvo que el usuario pida resumen; si es enorme, advertir y ofrecer leer entero o por partes.
3. **Formato para TTS:** convertir a texto hablable razonable:
   - Quitar o simplificar bloques de código (`` ``` ``): sustituir por “código omitido” o leer solo la primera línea si aporta.
   - Enlaces markdown `[texto](url)` → leer **solo “texto”**.
   - Quitar `**`, `#`, listas puede dejarse como frases separadas por punto y coma.
4. **Nunca** pasar el texto largo por argumento de shell: `npm run voice:say -- "..."` **rompe** con respuestas grandes. Siempre **archivo temporal + `voice-tts-file.sh`**.

## Procedimiento (ejecutar en el repo)

Desde la raíz de **Calculadora-BMC** (ajustar ruta si el workspace es otro):

Flujo sugerido en terminal (el agente rellena el archivo con el contenido real, no un placeholder):

```bash
TMP="$(mktemp /tmp/bmc-agent-tts-XXXXXX.txt)"
# El contenido de la última respuesta del asistente debe escribirse en $TMP (UTF-8).
bash scripts/voice-tts-file.sh "$TMP"
rm -f "$TMP"
```

En la práctica, el **agente** debe:

1. Reconstruir en el turno actual el contenido de la última respuesta (como la tiene en contexto).
2. Escribir ese contenido a `"$TMP"` con la herramienta de escritura de archivos **o** con un único `printf` / heredoc en terminal cuidando comillas (si el texto tiene `'` usar archivo vía herramienta Write).
3. Ejecutar: `bash scripts/voice-tts-file.sh "$TMP"`.
4. Borrar `"$TMP"` después de que termine `say` (o dejar que el usuario borre; `mktemp` en `/tmp` es aceptable).

**Recomendación:** usar la herramienta **Write** para escribir `/tmp/bmc-agent-tts-LAST.txt` con el texto plano, luego **Shell**:

`bash scripts/voice-tts-file.sh /tmp/bmc-agent-tts-LAST.txt && rm -f /tmp/bmc-agent-tts-LAST.txt`

## Voz Mónica

- macOS debe tener la voz **Mónica** (`es_ES`). Si no está: Ajustes → Accesibilidad → Contenido hablado → Gestionar voces → Spanish.
- `scripts/voice-tts-file.sh` intenta **Mónica** primero; si no existe, primera voz española; si no, voz por defecto.

## Comandos relacionados (ya en el repo)

| Comando | Uso |
|---------|-----|
| `npm run voice:say -- "frase corta"` | Texto corto por CLI |
| `npm run voice:tts-file -- /ruta/archivo.txt` | Cualquier longitud desde archivo |
| `scripts/voice-speak-es.sh` | stdin o argumentos; sin `-f` para archivos gigantes preferir `voice-tts-file` |

## Límites

- Solo **macOS** (`say`). En Linux/Windows este skill no aplica tal cual.
- El agente **no** puede leer el portapapeles del usuario salvo que el usuario lo pegue; la “última respuesta” sale del **contexto del chat**, no de APIs ocultas de Cursor.

## Disclaimer

No graba ni sube audio; todo es local con `say`.
