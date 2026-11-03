---
name: colab_offload
description: |
  Skill que abstrai a comunicação com o Google Colab rodando GPU NVIDIA (T4/A100).
  Foco exclusivo em processamento gráfico/visual acelerado por GPU.
  O Colab é tratado como um "funcionário GPU" gerenciado pelo Antigravity.
  
  O que roda no Colab (GPU):
    - Face Recognition (InsightFace/ArcFace — embeddings 512-dim)
    - Object Detection (YOLOv8 — pessoas, objetos)
    - Processamento de imagem (resize, sharpen, normalize, edges)
    - Benchmarks GPU (multiplicação de matrizes, TFLOPs)
  
  O que NÃO roda no Colab:
    - LLMs de chat (o Antigravity faz isso)
    - Geração de código (o Antigravity faz isso)
    - Gerência de tokens (o Antigravity faz isso)

inputs:
  - name: imageData
    type: Buffer
    description: Dados binários da imagem (JPEG/PNG) para processar na GPU.
  - name: taskType
    type: enum[face_embeddings, face_compare, face_batch, detect_objects, process_image, benchmark]
    description: Tipo de processamento gráfico a executar na GPU.
  - name: options
    type: object
    description: Opções específicas do tipo de tarefa (confidence, classes, operations, etc.)

outputs:
  - name: result
    type: object
    description: JSON com resultado do processamento (embeddings, detecções, imagem processada, etc.)

setup:
  colab_script: colab/aquila_sovereign_engine.py
  electron_bridge: apps/electron/src/main/services/ColabGpuBridge.ts

architecture: |
  ┌──────────────────┐       HTTPS (Cloudflare)      ┌──────────────────────┐
  │  Áquila Desktop  │ ─────────────────────────────► │  Google Colab (GPU)  │
  │  (Electron)      │                                │                      │
  │                  │ ◄───────────────────────────── │  InsightFace (faces) │
  │  ColabGpuBridge  │       JSON response            │  YOLOv8 (objetos)   │
  │  (TypeScript)    │                                │  OpenCV (imagem)     │
  └──────────────────┘                                └──────────────────────┘
  
  Divisão de trabalho:
    GPU (Colab)  = Tudo que é gráfico/visual/tensor
    CPU (Agent)  = Código, raciocínio, gerência, tokens

usage: |
  // No Electron:
  import { colabGpuBridge } from './services/ColabGpuBridge';
  
  // 1. Configurar URL (feito uma vez ao receber do Colab)
  colabGpuBridge.configure('https://xxx.trycloudflare.com');
  
  // 2. Extrair embeddings faciais
  const result = await colabGpuBridge.extractFaceEmbeddings(imageBuffer);
  // → { faces_detected: 2, faces: [{ embedding: [512 floats], ... }] }
  
  // 3. Detectar objetos
  const detections = await colabGpuBridge.detectObjects(frameBuffer, 0.5, "0");
  // → { detections: [{ class_name: "person", confidence: 0.92, bbox: [...] }] }
  
  // 4. Comparar rostos
  const match = await colabGpuBridge.compareFaces(photo1, photo2);
  // → { match: true, similarity: 0.87 }

example:
  taskType: "face_embeddings"
  imageData: "<Buffer JPEG>"
  options: {}
  result:
    faces_detected: 1
    faces:
      - embedding: [0.123, -0.456, ...]
        embedding_dim: 512
        bbox: [100, 50, 300, 350]
        det_score: 0.98
        age: 14
        gender: "M"
    processing_time_ms: 45.2
---
