---
name: Embedding Pipeline
description: Implement reusable embedding functions using Gemini embedding models via LangChain with proper error handling and batching for sitemap-crawled content.
---

# Embedding Pipeline

## Instructions

1. Create embedding module at `app/services/embedding/embedding.py`:
   - Provide embed_text(text: str) -> list[float] function
   - Include batch embedding embed_texts() for multiple texts
   - Implement retry logic with exponential backoff for API failures
   - Add proper error handling and logging

2. Configure Gemini embeddings via LangChain:
   - Use GoogleGenerativeAIEmbeddings from langchain_google_genai
   - Model: "models/gemini-embedding-001" (768 dimensions)
   - Handle API key via GOOGLE_API_KEY environment variable
   - Include rate limiting (60 requests/minute for free tier)

3. Implement batching functionality:
   - Process multiple texts efficiently (max 100 texts per batch)
   - Handle large batches by splitting into sub-batches
   - Include progress tracking with tqdm
   - Add memory management for large inputs

4. Support sitemap-crawled content:
   - Accept chunk objects with text and metadata
   - Preserve metadata association with embeddings
   - Return embeddings ready for Qdrant upload
   - Handle HTML-to-text cleaned content

5. Add utility functions:
   - Similarity calculation between embeddings (cosine)
   - Token counting for chunk size validation
   - Caching mechanism for repeated embeddings (optional)
   - Input validation for max text length (8192 tokens)

6. Follow Context7 MCP standards:
   - Use Gemini embeddings only (no OpenAI)
   - Follow LangChain GoogleGenerativeAIEmbeddings API
   - Include proper error handling
   - Document all configuration options

## Examples

Input: "Create embedding pipeline with Gemini for sitemap content"
Output: Creates embedding.py with:
```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from typing import List, Dict, Any
from tenacity import retry, wait_exponential, stop_after_attempt
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.batch_size = 100
        self.dimension = 768

    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(3))
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        return self.embeddings.embed_query(text)

    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(3))
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts with batching."""
        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            embeddings = self.embeddings.embed_documents(batch)
            all_embeddings.extend(embeddings)
        return all_embeddings

    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed chunks with metadata preserved for Qdrant upload."""
        texts = [chunk["content"] for chunk in chunks]
        embeddings = self.embed_texts(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk["vector"] = embedding

        return chunks
```
