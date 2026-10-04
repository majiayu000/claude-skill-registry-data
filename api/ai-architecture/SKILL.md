---
name: ai-architecture
description: Arquitetura de plataformas AI, integracao de modelos, MLOps, edge AI. Usar quando o projeto envolve IA, modelos de linguagem, Gemma, fine-tuning, ou inferencia.
---

# Arquitetura AI -- Padrao DME

## Stack AI da DME

- Modelo local: Gemma 4 (no computador do Henrique)
- API: Claude API (Anthropic SDK)
- Embeddings: OpenAI ou local
- Vector DB: pgvector (Supabase) ou Pinecone
- Framework: LangChain ou direto com SDK

## Padroes de integracao

### Claude API (principal)
```typescript
import Anthropic from '@anthropic-ai/sdk';
const client = new Anthropic();
const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: prompt }]
});
```

### Gemma 4 (local, gratuito)
Usar para pre-processamento, resumo, classificacao -- tarefas que nao precisam do Claude.
Rodar via Ollama ou direto no Python.

## Decisoes de arquitetura AI

| Tarefa | Modelo | Por que |
|--------|--------|---------|
| Resumo de documentos | Gemma 4 (local) | Gratuito, rapido |
| Geracao de codigo | Claude Sonnet | Qualidade + velocidade |
| Decisoes complexas | Claude Opus | Raciocinio profundo |
| Embeddings | text-embedding-3-small | Barato, bom o suficiente |
| Classificacao simples | Gemma 4 (local) | Zero custo |

## Seguranca AI

- Nunca enviar PII para APIs externas sem anonimizar
- Rate limiting em endpoints AI
- Timeout em chamadas de inferencia (30s max)
- Fallback quando modelo esta indisponivel
- Logging de prompts sem dados sensiveis
