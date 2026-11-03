---
name: NPU Optimizer
description: Skill para otimização de inferência de IA em hardware Áquila Edge (NPU 26 TOPS).
---

# NPU Optimizer (Flash-MoE Enhanced)

Extração máxima de performance para inferência soberana de baixa latência.

## Instruções de Uso
Ativar para otimizar modelos MoE, depurar latência de inferência ou gerir recursos da NPU.

## Capacidades
- **Flash-MoE Strategy**: Implementação de Async Weight Streaming e Expert Repacking.
- **Kernel Fusion**: Otimização de operações de dequantização e produto escalar na NPU.
- **I/O Profiling**: Medição de carregamento de pesos e uso de DMA.

## Regras Invioláveis (Zero-Bypass)
1. **Non-Blocking**: Proibido bloquear a Main Thread com carregamentos síncronos.
2. **Thermal Guard**: Monitorar temperatura e aplicar auto-throttling se exceder 75ºC.
3. **Local Weights**: Pesos de modelos devem estar em armazenamento local criptografado.

## Exemplos
"Otimize a inferência do modelo de reconhecimento facial para rodar na NPU com menos de 20ms de latência."
