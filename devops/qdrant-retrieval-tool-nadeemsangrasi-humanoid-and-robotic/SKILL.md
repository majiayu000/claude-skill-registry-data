---
name: Qdrant Retrieval Tool
description: Generate JSON schemas and Python handlers for Qdrant-based retrieval tools used by the RAG agent to search sitemap-crawled textbook content with URL citations.
---

# Qdrant Retrieval Tool

## Instructions

1. Create tool definitions for retrieval functionality in app/services/tools/retrieval_tools.py:
   - Define retrieve_passages({ query: string, k: int }) tool
   - Define lookup_metadata({ id: string }) tool
   - Create proper JSON schemas following OpenAI Agent SDK specification
   - Include proper parameter validation

2. Implement Qdrant client integration:
   - Initialize Qdrant client with cloud configuration
   - Connect to the "book_chunks" collection (768 dimensions, cosine distance)
   - Implement vector search using Gemini embeddings
   - Handle connection errors and retries

3. Create retrieval handlers with URL-based metadata:
   - Implement retrieve_passages function that performs semantic search
   - Return results with full metadata including source URL for citations
   - Implement lookup_metadata function for getting document metadata
   - Include proper error handling and logging

4. Metadata schema for retrieved passages:
   ```python
   {
       "id": "hash_of_url_and_chunk_index",
       "content": "The actual text content...",
       "score": 0.95,
       "metadata": {
           "url": "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/module-1-ros2/03-ros2-communication-patterns/",
           "module": "module-1-ros2",
           "chapter": "03-ros2-communication-patterns",
           "title": "ROS2 Communication Patterns",
           "chunk_index": 0,
           "content_type": "text",
           "heading": "Topic Subscriptions"
       }
   }
   ```

5. Follow Context7 MCP conventions:
   - Match OpenAI Agent SDK tool specification exactly
   - Produce deterministic JSON schemas
   - Integrate with Gemini embeddings for query encoding
   - Follow proper error handling patterns

6. Add proper configuration management:
   - QDRANT_URL: Qdrant Cloud cluster URL
   - QDRANT_API_KEY: API key for authentication
   - GOOGLE_API_KEY: For query embedding generation
   - Support both local and cloud Qdrant instances

## Examples

Input: "Create Qdrant retrieval tools with URL citations"
Output: Creates retrieval_tools.py with:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Dict, Any, Optional
import os
import hashlib

# Initialize clients
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

COLLECTION_NAME = "book_chunks"

def retrieve_passages(query: str, k: int = 5, module_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve relevant passages from the textbook using semantic search.

    Returns passages with source URLs for citation.
    """
    # Generate query embedding
    query_vector = embeddings.embed_query(query)

    # Build filter if module specified
    search_filter = None
    if module_filter:
        search_filter = Filter(
            must=[FieldCondition(key="module", match=MatchValue(value=module_filter))]
        )

    # Perform vector search
    search_results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k,
        query_filter=search_filter,
        with_payload=True
    )

    passages = []
    for result in search_results:
        passages.append({
            "id": result.id,
            "content": result.payload.get("content", ""),
            "score": result.score,
            "metadata": {
                "url": result.payload.get("url", ""),
                "module": result.payload.get("module", ""),
                "chapter": result.payload.get("chapter", ""),
                "title": result.payload.get("title", ""),
                "chunk_index": result.payload.get("chunk_index", 0),
                "heading": result.payload.get("heading", "")
            }
        })

    return passages

def lookup_metadata(doc_id: str) -> Dict[str, Any]:
    """Lookup metadata for a specific document chunk by ID."""
    records = qdrant_client.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[doc_id],
        with_payload=True
    )

    if records:
        payload = records[0].payload
        return {
            "url": payload.get("url", ""),
            "module": payload.get("module", ""),
            "chapter": payload.get("chapter", ""),
            "title": payload.get("title", ""),
            "chunk_index": payload.get("chunk_index", 0),
            "heading": payload.get("heading", "")
        }
    return {}

# Tool schemas for OpenAI Agent SDK
retrieval_tools = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_passages",
            "description": "Retrieve relevant passages from the Physical AI & Humanoid Robotics textbook based on semantic search. Returns passages with source URLs for citations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant passages about robotics, ROS2, simulation, etc."
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of passages to retrieve (default: 5, max: 10)",
                        "default": 5
                    },
                    "module_filter": {
                        "type": "string",
                        "description": "Optional filter by module (e.g., 'module-1-ros2', 'module-2-gazebo-unity')",
                        "enum": ["module-1-ros2", "module-2-gazebo-unity", "module-3-nvidia-isaac", "module-4-vla", "capstone"]
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_metadata",
            "description": "Lookup metadata for a specific document chunk by ID to get source URL and context",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The document chunk ID to lookup metadata for"
                    }
                },
                "required": ["id"]
            }
        }
    }
]
```
