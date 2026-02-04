---
name: obsidian-reading-guardrails
description: "Garantiza lectura real, control de limites, registro en cache y validacion de citas/wikilinks en Obsidian."
---
# Obsidian Reading Guardrails

## Cuando usar
- Tengo que leer notas para responder, resumir o editar.
- Necesito trazabilidad y citas verificables.
- Quiero evitar alucinaciones por lecturas incompletas.

## Guardrails
- Si no puedo leer una fuente necesaria, digo "no consta en la boveda".
- No cito nada que no haya leido completo.
- Mantengo un registro de lecturas con hash y tamano.

## Procedimiento
1. **Definir objetivos**
   - Identifico las rutas objetivo y el alcance (nota principal + enlaces de primer nivel).
2. **Lectura completa o limitada**
   - Si el archivo supera `limite_lectura_suave_kb` (128 KB por defecto), leo secciones objetivo.
   - Si supera `limite_lectura_duras_kb` (512 KB por defecto), pido confirmacion para leer completo.
3. **Seguir enlaces de primer nivel**
   - Wikilinks `[[...]]`, transclusiones `![[...]]`.
   - Enlaces Markdown a `.md/.txt/.pdf` cuando sean parseables.
4. **Registrar lecturas**
   - Escribo en `cache/lecturas.json` (o la ruta de cache del vault) con hash, tamano y enlaces seguidos.
5. **Anclado minimo**
   - Si necesito citar un bloque sin `^ancla`, propongo anadir una ancla solo con aprobacion.
6. **Validar wikilinks**
   - Verifico existencia de nota y seccion.
   - Si una seccion falla, degrado la cita a nivel de nota y lo marco.

## Formato de registro (ejemplo)
```json
{
  "ruta": "ruta/nota.md",
  "timestamp": "YYYY-MM-DDTHH:mm:ss",
  "tamano": 12345,
  "hash": "sha256:...",
  "origen": "filesystem",
  "enlaces_seguidos": ["ruta/enlace.md"]
}
```

## Entrega
- Incluyo una seccion **Fuentes internas** con wikilinks precisos.
- Si falta lectura, detengo la entrega y declaro "no consta en la boveda".

