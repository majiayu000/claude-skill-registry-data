---
name: Vision Worker Expert
description: Especialista em depuração e melhoria dos workers de Visão Computacional (Python/Node).
---

# Vision Worker Expert

Esta skill é essencial para manter a integridade dos sensores visuais do Áquila Pro, garantindo detecção de alta precisão e baixa latência.

## Instruções de Uso
Ativar para depurar `aquila_camera_worker`, `aquila_face_worker` ou implementar novos modelos de detecção.

## Capacidades
- **NPU Architecture**: Configuração de threads dedicadas para cada stream (Multi-Camera School).
- **Real-time Analytics**: Implementação de detecção de intrusão, heatmaps e Re-ID.
- **Intelligence Targets**: Detecção de armas, bagagem suspeita e reconhecimento facial.
- **IPC Optimization**: Gestão de `SharedArrayBuffer` para troca de frames entre Python e Electron.

## Regras Invioláveis (Zero-Bypass)
1. **Local Inference**: Nunca sugerir o uso de APIs de visão na nuvem. Toda inferência deve ser local (TensorRT/OpenVINO).
2. **Memory Safety**: Monitorar frames órfãos em memória compartilhada para evitar vazamentos.
3. **Timestamp Sync**: Garantir sincronia absoluta de timestamps entre câmeras para rastreamento multi-sensor.

## Exemplos
"Antigravity, depure o worker de face e verifique por que o FPS caiu para 5 no sensor da entrada."
