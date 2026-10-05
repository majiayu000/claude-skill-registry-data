---
name: llm-ops
description: LLM Operations -- RAG, embeddings, vector databases, fine-tuning, prompt engineering avancado, custos de LLM, evals de qualidade e arquiteturas de IA para producao. 
category: AI & Agents
source: antigravity
tags: [markdown, claude, ai, agent, llm, document, rag]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/llm-ops
---


# LLM-OPS -- IA de Producao

## Overview

LLM Operations -- RAG, embeddings, vector databases, fine-tuning, prompt engineering avancado, custos de LLM, evals de qualidade e arquiteturas de IA para producao. Ativar para: implementar RAG, criar pipeline de embeddings, Pinecone/Chroma/pgvector, fine-tuning, prompt engineering, reducao de custos de LLM, evals, cache semantico, streaming, agents.

## When to Use This Skill

- When you need specialized assistance with this domain

## Do Not Use This Skill When

- The task is unrelated to llm ops
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

> A diferenca entre um prototipo de IA e um produto de IA e operabilidade.
> LLM-Ops e a engenharia que torna IA confiavel, escalavel e economica.

---

## Arquitetura Rag Completa

[Documentos] -> [Chunking] -> [Embeddings] -> [Vector DB]
                                                      |
    [Query] -> [Embed query] -> [Semantic Search] -> [Top K chunks]
                                                          |
                                           [LLM + Context] -> [Resposta]

## Pipeline De Indexacao

from anthropic import Anthropic
    import chromadb

    client = Anthropic()
    chroma = chromadb.PersistentClient(path="./chroma_db")

    def chunk_text(text, chunk_size=500, overlap=50):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk: chunks.append(chunk)
        return chunks

    def index_document(doc_id, content_text, metadata=None):
        chunks = chunk_text(content_text)
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        collection.upsert(ids=ids, documents=chunks)
        return len(chunks)

## Pipeline De Query Com Rag

def rag_query(query, top_k=5, system=None):
        results = collection.query(
            query_texts=[query], n_results=top_k,
            include=["documents", "metadatas", "distances"])
        context_parts = []
        for doc, meta, dist in zip(results["documents"][0],
                                    results["metadatas"][0],
                                    results["distances"][0]):
            if dist < 1.5:
                src = meta.get("source", "doc")
                context_parts.append(f"[Fonte: {src}]
{doc}")
        context = "

---

".join(context_parts)
        response = client.messages.create(
            model="claude-opus-4-20250805", max_tokens=1024,
            system=system or "Responda baseado no contexto.",
            messages=[{"role": "user", "content": f"Contexto:
{context}

{query}"}])
        return response.content[0].text

---

## Escolha Do Vector Db

| DB | Melhor Para | Hosting | Custo |
|----|------------|---------|-------|
| Chroma | Desenvolvimento, local | Self-hosted | Gratis |
| pgvector | Ja usa PostgreSQL | Self/Cloud | Gratis |
| Pinecone | Producao gerenciada | Cloud | USD 70+/mes |
| Weaviate | Multi-modal | Self/Cloud | Gratis+ |
| Qdrant | Alta performance | Self/Cloud | Gratis+ |

## Pgvector

CREATE EXTENSION IF NOT EXISTS vector;
    CREATE TABLE knowledge_embeddings (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        content TEXT NOT NULL,
        embedding vector(1536),
        metadata JSONB,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    CREATE INDEX ON knowledge_embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
    SELECT content, 1 - (embedding <=> QUERY_VECTOR) AS similarity
    FROM knowledge_embeddings ORDER BY similarity DESC LIMIT 5;

---

## Estrutura De Prompt De Elite

Componentes do system prompt Auri:

- Identidade: Nome (Auri), Tom (Natural, caloroso, direto), Plataforma (Amazon Alexa)
- Regras: Maximo 3 paragrafos curtos, sem markdown, linguagem conversacional
- Capacidades: analise de negocios, conselho baseado em dados, criatividade
- Limitacoes: sem internet tempo real, sem transacoes financeiras
- Personalizacao: {user_name}, {user_preferences}, {relevant_history}

## Chain-Of-Thought

def cot_analysis(problem: str) -> str:
        steps = [
            "1. O que exatamente esta sendo pedido?",
            "2. Que informacoes sao criticas para resolver?",
            "3. Quais abordagens possiveis existem?",
            "4. Qual abordagem e melhor e por que?",
            "5. Quais riscos ou limitacoes existem?",
        ]
        prompt = f"Analise passo a passo:

PROBLEMA: {problem}

"
        prompt += "
".join(steps) + "

Resposta final (concisa, para voz):"
        return call_claude(prompt)

---

## Cache Semantico

class SemanticCache:
        def __init__(self, similarity_threshold=0.95):
            self.threshold = similarity_threshold
            self.cache = {}

        def get_cached(self, query, embedding):
            for cached_emb, (response, _) in self.cache.items():
            
