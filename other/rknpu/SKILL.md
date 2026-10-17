---
name: rknpu
description: >
  RK1 NPU pool — rkllama server con RKLLM models en RK3588 NPU de los nodos TuringPi 2.
  Gotchas de device exclusivo, tokenizador HF, modelos compatibles, límites de memoria,
  test CPU vs NPU con Gemma 3.
tags: [kubernetes, ai, rk3588, npu, rkllm, rkllama, arm64, inference, gemma]
---

# RK1 NPU Pool — rkllama en RK3588

## Arquitectura

4 nodos TuringPi 2 (RK3588S, 32 GB LPDDR4X) corriendo `ghcr.io/notpunchnox/rkllama:main`.
Cada nodo tiene su propio Deployment + PVC + Service en namespace `ai`.

```
LiteLLM proxy → gemma-npu / rk1-npu-0X services (port 8080)
                    ↓
             rkllama (Flask, Ollama-compatible API)
                    ↓
             RKLLM runtime (librkllmrt.so)
                    ↓
             /dev/dri/renderD129  ← RKNN kernel driver
                    ↓
             RK3588 NPU (3 cores, 6 TOPS)
```

- Role: `roles/install-rknpu-pool/`
- Namespace: `ai`
- Port: 8080 (Ollama-compatible API)
- Deploy: `ansible-playbook bootstrap.yml --tags ai-npu-pool`

## Device RKNN en RK3588

```
/dev/dri/renderD128  ← Mali GPU (ARM GPU)
/dev/dri/renderD129  ← RKNN NPU (Rockchip NPU, DRIVER=RKNPU)
```

El kernel 6.1 vendor de TuringPi 2 expone el NPU como DRI device.
`librkllmrt.so` escanea `/dev/dri/` al arrancar y auto-selecciona `renderD129`
(el que tiene DRIVER=RKNPU). El pod necesita:
```yaml
securityContext:
  privileged: true
volumes:
  - name: dev-dri
    hostPath:
      path: /dev/dri
```

## CRÍTICO: el NPU es exclusivo — UN proceso a la vez

**El RKNN driver NO soporta acceso concurrente desde múltiples procesos.**
Si dos pods intentan usar `/dev/dri/renderD129` en el mismo nodo:
```
E RKNN: failed to allocate handle, ret: -1, errno: 14, errstr: Bad Address
E RKNN: failed to malloc npu memory, size: XXXXXXX, flags: 0x2
E RKNN: load model file error!
E rkllm: rkllm_init failed
```
`errno: 14 = EFAULT` — no es "sin memoria", es que el driver no puede mapear
el bloque DMA porque otro proceso ya tiene el device abierto.

**Regla:** un solo pod rkllama por nodo RK1. Nunca desplegar dos deployments NPU
en el mismo nodo. Antes de testear, escalar a 0 el pod existente:
```bash
kubectl scale deployment rk1-npu-04 -n ai --replicas=0
# testear...
kubectl scale deployment rk1-npu-04 -n ai --replicas=1
```

## Límites de memoria NPU

RK3588S tiene 32 GB LPDDR4X compartida CPU+GPU+NPU. El NPU aloca memoria DMA contigua.
Si la memoria DMA está fragmentada o agotada, el RKLLM falla con EFAULT (ver arriba).

| Modelo | Cuantización | Tamaño en disco | Memoria NPU |
|---|---|---|---|
| Gemma 3 270M IT | w8a8 | 629 MB | ~270 MB — funciona |
| Gemma 3 1B IT | w8a8 | 1.7 GB | ~954 MB — puede fallar si el nodo tuvo Llama-3.1-8B antes |
| Llama 3.1 8B | w8a8 | 8.63 GB | ~8-13 GB — el modelo por defecto del pool |

Si el modelo 1B falla con EFAULT después de haber corrido Llama-3.1-8B en el mismo nodo,
la causa es fragmentación DMA residual del driver. Solución: reiniciar el nodo
o usar el modelo 270M que tiene menor footprint.

## Modelos RKLLM disponibles para RK3588

Formato `.rkllm` compilado con rkllm-toolkit. **NO son GGUF**.
Fuente: `jamescallander` en HuggingFace — modelos convertidos para RK3588:

| Repo HF | Paráms | Cuantización | Tamaño |
|---|---|---|---|
| `jamescallander/gemma-3-270m-it_w8a8_g128_rk3588.rkllm` | 270M | w8a8 | 629 MB |
| `jamescallander/gemma-3-1b-it_w8a8_g128_rk3588.rkllm` | 1B | w8a8 | 1.7 GB |
| `jamescallander/gemma-3-4b-it_w8a8_g128_rk3588.rkllm` | 4B | w8a8 | ~4 GB |
| `jamescallander/Llama-3.1-8B-Instruct_w8a8_g128_rk3588.rkllm` | 8B | w8a8 | 8.63 GB |

Los repos `jamescallander/*.rkllm` SOLO contienen el archivo `.rkllm`, NO el tokenizador.

## Tokenizador — GOTCHA CRÍTICO

rkllama descarga el tokenizador desde HuggingFace en el primer `generate` usando el
campo `HUGGINGFACE_PATH` del Modelfile. Si ese repo no tiene tokenizador → `NoneType`
crash. Si el repo es gated → 401 error.

**Reglas:**
- NO usar el repo `.rkllm` de jamescallander como HUGGINGFACE_PATH (solo tiene el .rkllm)
- NO usar `google/gemma-*` (gated — requiere auth en HF)
- **SÍ usar unsloth**: `unsloth/gemma-3-1b-it` para todos los modelos Gemma 3
- Para Llama 3.1: `unsloth/llama-3.1-8b-instruct` (ya confirmado funcionando)

Modelfile correcto para Gemma 3 (cualquier tamaño):
```
FROM=gemma-3-270m-it_w8a8_g128_rk3588.rkllm
HUGGINGFACE_PATH=unsloth/gemma-3-1b-it
```

El tokenizador se cachea en `/opt/venv/lib/python3.12/site-packages/rkllama/config/data/`
(dentro de la imagen, se pierde al reiniciar el pod). Se re-descarga en cada boot.

## Descarga de modelos — init container

Patrón estándar (igual que el pool existente):
```yaml
initContainers:
  - name: model-downloader
    image: ghcr.io/notpunchnox/rkllama:main   # tiene Python + huggingface_hub
    imagePullPolicy: IfNotPresent
    command:
      - /bin/sh
      - -c
      - |
        MODEL_DIR="/opt/rkllama/models/gemma-3-270m-it"
        MODEL_FILE="${MODEL_DIR}/gemma-3-270m-it_w8a8_g128_rk3588.rkllm"
        mkdir -p "${MODEL_DIR}"
        if [ -f "${MODEL_FILE}" ]; then
          echo "Already present: $(du -sh $MODEL_FILE)"; exit 0
        fi
        /opt/venv/bin/python3 -c "
        from huggingface_hub import hf_hub_url
        import requests, os
        repo = 'jamescallander/gemma-3-270m-it_w8a8_g128_rk3588.rkllm'
        filename = 'gemma-3-270m-it_w8a8_g128_rk3588.rkllm'
        dest = '${MODEL_FILE}'
        url = hf_hub_url(repo_id=repo, filename=filename)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            done = 0
            with open(dest + '.tmp', 'wb') as f:
                for chunk in r.iter_content(chunk_size=8*1024*1024):
                    if chunk:
                        f.write(chunk)
                        done += len(chunk)
                        if total:
                            print(f'{int(done*100/total)}% ({done//1024//1024}/{total//1024//1024} MB)', flush=True)
        os.rename(dest + '.tmp', dest)
        print('Done.', flush=True)
        "
    volumeMounts:
      - name: model-storage
        mountPath: /opt/rkllama/models
```

## Queries desde terminal

```bash
# Desde dentro del cluster
kubectl exec -n test-gemma deploy/gemma-npu -- \
  curl -s -X POST http://localhost:8080/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma-3-270m-it","prompt":"Tu pregunta","stream":false}'

# Via port-forward desde workstation
kubectl port-forward -n test-gemma svc/gemma-npu 8080:8080 &
curl -s -X POST http://localhost:8080/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma-3-270m-it","prompt":"What is 2+2?","stream":false}' | jq .response

# Ver modelos cargados
kubectl exec -n test-gemma deploy/gemma-npu -- \
  curl -s http://localhost:8080/api/tags | jq .

# OpenAI-compatible (también funciona)
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma-3-270m-it","messages":[{"role":"user","content":"Hola"}]}'
```

## Performance medida (Gemma 3 270M, RK3588 NPU, w8a8)

```
load_duration:       100 ms  (carga modelo en NPU)
prompt_eval_duration: 58 ms  (21 tokens de prompt)
eval_duration:       484 ms  (8 tokens generados)
total_duration:      550 ms  (end-to-end)
tokens/s:            ~16 t/s
```

Para comparar, la misma pregunta en CPU (RK1, 4 cores big) con llama.cpp tarda ~5-15s.
El NPU da ~10-30x speedup vs CPU para modelos pequeños en RK3588.

## Test CPU vs NPU en namespace test-gemma

Manifests en `tests/gemma-rk1/manifest.yaml`:
- `gemma-cpu` (Ollama + GGUF Gemma 3 1B, srv-rk1-nvme-03, port 8080)
- `gemma-npu` (rkllama + RKLLM Gemma 3 270M, srv-rk1-nvme-04, port 8080)

```bash
kubectl get pods -n test-gemma
kubectl port-forward -n test-gemma svc/gemma-npu 8080:8080 &
kubectl port-forward -n test-gemma svc/gemma-cpu 8081:8080 &
```

## ¿Vale la pena el NPU? Mi opinión

El NPU RK3588 es una herramienta de nicho. Vale para latencia local baja y privacidad;
no vale para calidad de conversación. El error común es usarlo como sustituto de un LLM
grande — no lo es. Es mejor pensarlo como un co-procesador de clasificación/filtrado que
corre en paralelo con el stack LLM principal (LiteLLM + OpenRouter).

**El caso de uso que justifica los 4 nodos NPU en este cluster**: un pipeline de voz
100% local donde Whisper (CPU RK1) transcribe y Gemma NPU clasifica la intención antes
de rutear al LLM correcto. Zero latencia de red, zero costo, funciona offline. Eso es
suficiente para justificar el hardware ya existente.

**Lo que NO justifica**: reemplazar claude-sonnet para conversación general. Gemma 270M
da respuestas de 5-20 palabras con calidad irregular. No hay ROI en usar el NPU para
razonamiento complejo cuando LiteLLM + modelos :free son gratuitos y de alta calidad.

## Casos de uso donde el NPU vale la pena

### Vale la pena ✅

1. **Clasificación de intención en tiempo real** — clasificar mensajes de Telegram/usuario
   en <100ms sin tocar OpenRouter. Gemma 3 270M w8a8 lo hace en 550ms total.
   Útil para routing en OpenClaw antes de llamar al LLM grande.

2. **Extracción de entidades locales** — NER sobre logs, alertas, mensajes internos.
   Datos que no deben salir del cluster. 270ms por query, sin latencia de red.

3. **Filtrado/moderación de contenido** — pre-filtrar requests antes de mandar a modelos
   caros. Si el NPU dice "irrelevante" → no gastar tokens en OpenRouter.

4. **Embeddings ligeros / resumen de chunks** — preparar contexto antes de pasar
   a un modelo más grande. Pipeline local completo.

5. **Whisper STT → Gemma NPU → respuesta** — pipeline de voz 100% in-cluster:
   transcribir audio (whisper-stt, CPU RK1) → procesar con Gemma (NPU RK1)
   → responder. Zero costo, ~1-2s latencia total.

6. **Guardia de privacidad** — para datos sensibles (salud, finanzas), el NPU
   es la única opción viable (no se puede mandar a cloud).

### No vale la pena ❌

1. **Conversación general de calidad** — Gemma 270M/1B es limitada. Para chat
   general, usar claude-sonnet/gemini-flash via LiteLLM. El NPU no compite en calidad.

2. **Context largo (>2048 tokens)** — los modelos RKLLM compilados tienen max_context_limit
   hardcodeado (4096 tokens en los modelos de jamescallander). Para textos largos usar CPU.

3. **Fine-tuning o RAG pesado** — el NPU no sirve para entrenamiento. Para RAG con
   muchos documentos, el embedding model necesita CPU o GPU dedicada.

4. **Modelos grandes (>4B)** — Llama 3.1 8B en NPU tarda ~800s en cargar y consume
   casi toda la LPDDR4X. Para inferencia pesada, usar el t7910 con GPU.

## Uso desde OpenCode / LiteLLM

El pool está expuesto como `rk1-npu-local` en LiteLLM (4× entradas en round-robin).
Acceso desde OpenCode:

```bash
# Desde cualquier directorio (provider 'litellm' en ~/.config/opencode/config.json)
opencode run --model litellm/rk1-npu-local "pregunta"

# Desde el repo infra (provider 'litellm-cluster' en opencode.local.json)
opencode run --model litellm-cluster/rk1-npu-local "pregunta"
```

Config en `opencode.json` / `opencode.local.json`:
```json
"rk1-npu-local": { "name": "Llama 3.1 8B NPU", "tools": false }
```
`"tools": false` es obligatorio — enviar tool definitions sube el request a ~62K tokens,
excediendo el límite de 4K de rkllama y activando el fallback chain de LiteLLM.

## Fix de streaming SSE (rkllama bug — 2026-06-17)

**Bug**: rkllama llamaba `ollama_chat_stream_to_openai_chat_completions_chunks([chunk])`
una vez por chunk SSE. Cada llamada generaba un UUID nuevo → el streaming parser de
`@ai-sdk` descarta texto cuando los IDs difieren entre chunks.

**Fix**: initContainer `patch-streaming` en cada pod que parchea `format_utils.py`
al arrancar: genera un solo `_cid` por stream y lo pasa a todos los chunks.

Archivo parchado: `/opt/rkllama/build/lib/rkllama/api/format_utils.py`
Verificar que el patch se aplicó:
```bash
kubectl logs -n ai deploy/rk1-npu-01 -c patch-streaming
# debe mostrar: "Patch applied"
```

Si rkllama actualiza su imagen y rompe el pattern match:
```bash
# Copiar format_utils.py actual del pod para ver el nuevo código
kubectl exec -n ai deploy/rk1-npu-01 -- \
  cat /opt/rkllama/build/lib/rkllama/api/format_utils.py
```
Luego actualizar el `old =` string en el initContainer del template `rk1-npu-pool.yaml.j2`.

## Gotchas operacionales

- **`imagePullPolicy: Always` en init containers** → re-pull en cada boot, lento.
  Siempre usar `IfNotPresent`.
- **PVC debe ser RWO individual por pod** — `longhorn-nvme` es RWO. Un PVC compartido
  entre pods en distintos nodos no funciona. Un PVC por variante/nodo.
- **`ollama/ollama` no tiene `curl`** — el startup script del container Ollama debe
  usar `ollama list` para esperar que el server arranque, no `curl`.
- **El tokenizador tarda ~1-2s en descargarse** en el primer generate. La segunda
  llamada es instantánea (cacheada en memoria del proceso).
- **hostPID no está activado** por defecto en los pods rkllama — `fuser /dev/dri/*`
  desde dentro del pod solo ve procesos del container, no del host.
  Para diagnosticar quién tiene el device, usar `kubectl debug node/` o agregar
  `hostPID: true` al pod spec.
