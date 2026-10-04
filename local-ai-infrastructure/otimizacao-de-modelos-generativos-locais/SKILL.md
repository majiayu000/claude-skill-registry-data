---
name: otimizacao-de-modelos-generativos-locais
description: Otimiza engines de inferencia local (llama.cpp) com quantizacao Q4_K_M, KV cache e interface assincrona para latencia minima.
---
# otimizacao-de-modelos-generativos-locais

## Descrição
A skill `otimizacao-de-modelos-generativos-locais` especifica as técnicas de otimização de engines de inferência para modelos de linguagem generativos rodando diretamente no hardware do escritor (CPU/GPU do laptop ou desktop). Ela visa reduzir a pegada de memória VRAM, eliminar latências de contexto redundantes via caching e garantir que a interface do editor permaneça responsiva enquanto a IA processa sugestões em background.

## Quando usar
Gatilhos concretos e observáveis:
- A equipe de engenharia configura ou atualiza o motor local de inferência (llama.cpp, Triton) para o aplicativo desktop.
- O usuário ativa um novo modelo de linguagem no painel de configurações do assistente de IA.
- O sistema detecta latência de geração superior ao limite aceitável e aciona perfis de otimização.

Quando NÃO usar:
- Para modelos de IA que rodam exclusivamente na nuvem (aplicar otimizações de servidor remoto nesse contexto).
- Para fine-tuning ou treinamento de modelos (que são operações offline distintas da otimização de inferência).

## Pré-requisitos
- Biblioteca de inferência local compatível: llama.cpp (CPU/GPU) ou ONNX Runtime.
- Modelo de linguagem base em formato GGUF (quantização INT4/INT8).
- Suporte a Web Workers ou threads de background no aplicativo (para execução assíncrona).

## Processo (passo a passo executável)
1. **Quantização INT4 (Q4_K_M):**
   - Selecionar a variante quantizada Q4_K_M do modelo-alvo (ex: `Qwen-2.5-7B-Instruct-Q4_K_M.gguf`).
   - Verificar que a pegada de memória VRAM não excede `4.5 GB` para permitir execução em GPUs populares de 6 GB (ex: RTX 3060, RTX 4060).
2. **Ativação de Prompt Caching (KV Cache):**
   - Configurar o llama.cpp com a flag de cache de chave-valor KV (`--cache-type q8_0`) para manter os tensores de atenção do prompt de sistema (worldbuilding e fichas de personagens) processados em memória entre chamadas.
   - Definir o número de tokens de cache alocados: `n_ctx = 8192` (suficiente para manter o contexto de 3 a 5 capítulos).
3. **Configuração de Parâmetros de Decodificação Literária:**
   - Ajustar os parâmetros de sampling do modelo para maximizar a qualidade criativa literária:
     - `temperature = 0.80` (diversidade controlada; evitar < 0.5 que resulta em textos planos e repetitivos).
     - `top_p = 0.90` (núcleo de probabilidade — filtro de vocabulário).
     - `repeat_penalty = 1.10` (penalidade de repetição de tokens para evitar loops de frases idênticas).
4. **Interface Assíncrona de Exibição (Translúcida):**
   - Disparar a geração de texto em um Web Worker ou thread separada.
   - Enquanto o modelo gera tokens, exibir o texto sendo construído com opacidade reduzida (`0.40`) no painel de sugestão, indicando visualmente que está em processamento.
   - Ao concluir a geração completa, aplicar transição de opacidade para `1.0` e habilitar os botões de ação (Aceitar/Rejeitar/Refinar).

## Parâmetros e configuração
- `MODEL_QUANT_FORMAT`: Formato de quantização GGUF usado. Padrão: `"Q4_K_M"`.
- `KV_CACHE_TOKEN_LIMIT`: Tamanho máximo do contexto no cache KV em tokens. Padrão: `8192`.
- `GEN_TEMPERATURE`: Temperatura de amostragem do decodificador. Padrão: `0.80`.
- `GEN_REPEAT_PENALTY`: Penalidade de repetição de tokens consecutivos. Padrão: `1.10`.

## Armadilhas e como evitá-las
- **Armadilha:** Saturação de VRAM por Recálculo de Contexto: sem o prompt caching ativo, o modelo precisa re-processar os tensores de atenção do contexto inteiro (fichas de personagens, worldbuilding, capítulos anteriores) a cada nova chamada de geração de parágrafo. Isso eleva o TTFT para acima de 10 segundos, tornando a experiência de co-escrita inutilizável.
  **Mitigação:** Habilitar o caching de KV no llama.cpp desde a inicialização do motor. Manter o bloco de contexto de sistema (fichas, worldbuilding) sempre no início do prompt (prefixo estável) para que o sistema de caching possa reutilizá-lo eficientemente entre chamadas consecutivas (LiteraryBench, 2026).

## Critérios de validação (Definition of Done)
- [ ] O TTFT médio para geração de parágrafos com contexto literário completo é inferior a 300ms com o cache KV ativo.
- [ ] A pegada de memória VRAM do modelo quantizado em INT4 (Q4_K_M) não excede 4.5 GB, confirmada por monitoramento no painel de desempenho do aplicativo.

## Fundamentação científica
- Self-Refine (2023) - Self-Refine: Iterative Refinement with Self-Feedback - NeurIPS 2023
- LiteraryBench (2026) - LiteraryBench: A Benchmark for AI-Assisted Literary Writing - arXiv 2026

## Requisitos do projeto relacionados
- RF-81 (sugestões inline)
- RF-180 (reescrever com estilo)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A quantização Q4_K_M e o KV caching em llama.cpp são técnicas amplamente testadas e estáveis com retorno mensurável claro em latência e footprint de memória.*

## Exemplos
**Configuração do motor llama.cpp:**
```bash
./llama-server \
  --model Qwen-2.5-7B-Instruct-Q4_K_M.gguf \
  --n-gpu-layers 35 \
  --ctx-size 8192 \
  --cache-type q8_0 \
  --temp 0.80 \
  --repeat-penalty 1.10 \
  --top-p 0.90
```
**Resultado esperado:**
- VRAM utilizada: ~4.1 GB
- TTFT com KV cache quente: ~180ms
**Caso de falha conhecido:**
O usuário ativar o modelo sem a flag de cache KV e o sistema demorar 12 segundos para gerar o primeiro token de sugestão enquanto o autor tenta digitar.
