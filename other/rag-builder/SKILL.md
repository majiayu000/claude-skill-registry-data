---
name: rag-builder
description: Use when rAG pipeline design — document chunking, embedding strategies,
  retrieval optimization, and answer generation. Use when working with rag builder.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- builder
- infrastructure
- memory
- pipeline
- rag
- self-improvement
version: 1.0.0
category: core
---


## Overview

Retrieval-Augmented Generation (RAG) is the standard pattern for grounding LLMs in your data. This skill covers the full pipeline: document loading, chunking strategies, embedding, vector storage, retrieval, and answer synthesis.

## Capabilities

- Design document chunking strategies (fixed, semantic, recursive)
- Select and configure embedding models for your use case
- Implement hybrid search (vector + keyword) for better retrieval
- Build answer synthesis with source attribution
- Evaluate RAG quality with RAGAS metrics

## When to Use
**Trigger phrases:**
- "rag builder"
- "RAG pipeline design — document chunking, embedding strategies, retrieval optimiz"


- Building a chatbot over your documentation or knowledge base
- Need LLM answers grounded in factual, up-to-date data
- Document Q&A where hallucination is unacceptable
- Customer support automation over product docs

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Chunking Strategy
```python
def chunk_document(doc, strategy="recursive", chunk_size=512, overlap=50):
    if strategy == "fixed":
        return split_by_chars(doc, chunk_size, overlap)
    elif strategy == "recursive":
        return recursive_split(doc, separators=["\n\n", "\n", ". ", " "], chunk_size=chunk_size)
    elif strategy == "semantic":
        return semantic_split(doc, similarity_threshold=0.8)
```

### RAG Pipeline
```python
def rag_query(question, vector_store, llm):
    # 1. Retrieve relevant chunks
    chunks = vector_store.similarity_search(question, k=5)
    
    # 2. Re-rank by relevance
    ranked = rerank(chunks, question, top_k=3)
    
    # 3. Synthesize answer with sources
    context = "\n\n".join([c.text for c in ranked])
    prompt = f"""Answer based on context. Cite sources.

Context:
{context}

Question: {question}

Answer with citations:"""
    
    return llm.generate(prompt)
```

## Common Patterns

- **Recursive chunking**: Best default — splits by paragraphs, then sentences, then words
- **Overlap matters**: 10-20% overlap between chunks prevents context loss at boundaries
- **Hybrid search**: Combine vector similarity with BM25 keyword search for best results
- **Source attribution**: Always return which chunks informed the answer

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |