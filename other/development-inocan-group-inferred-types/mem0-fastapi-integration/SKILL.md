---
name: mem0-fastapi-integration
description: Memory layer integration patterns for FastAPI with Mem0 including client setup, memory service patterns, user tracking, conversation persistence, and background task integration. Use when implementing AI memory, adding Mem0 to FastAPI, building chat with memory, or when user mentions Mem0, conversation history, user context, or memory layer.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Mem0 FastAPI Integration Patterns

**Purpose:** Provide complete Mem0 integration templates, memory service patterns, user tracking implementations, and conversation persistence strategies for building FastAPI applications with intelligent AI memory.

**Activation Triggers:**
- Integrating Mem0 memory layer into FastAPI
- Building chat applications with conversation history
- Implementing user context and personalization
- Adding memory to AI agents
- Creating stateful AI interactions
- User preference management

**Key Resources:**
- `templates/memory_service.py` - Complete Mem0 service implementation
- `templates/memory_middleware.py` - Request-scoped memory middleware
- `templates/memory_client.py` - Mem0 client configuration
- `templates/memory_routes.py` - API routes for memory operations
- `scripts/setup-mem0.sh` - Mem0 installation and configuration
- `scripts/test-memory.sh` - Memory service testing utility
- `examples/chat_with_memory.py` - Complete chat implementation
- `examples/user_preferences.py` - User preference management

## Core Mem0 Integration

### 1. Client Configuration

**Template:** `templates/memory_client.py`

**Workflow:**
```python
from mem0 import Memory, AsyncMemory, MemoryClient
from mem0.configs.base import MemoryConfig

# Hosted Mem0 Platform
client = MemoryClient(api_key=settings.MEM0_API_KEY)

# Self-Hosted Configuration
config = MemoryConfig(
    vector_store={
        "provider": "qdrant",
        "config": {
            "host": settings.QDRANT_HOST,
            "port": settings.QDRANT_PORT,
            "api_key": settings.QDRANT_API_KEY
        }
    },
    llm={
        "provider": "openai",
        "config": {
            "model": "gpt-4",
            "api_key": settings.OPENAI_API_KEY
        }
    },
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": settings.OPENAI_API_KEY
        }
    }
)
memory = AsyncMemory(config)
```

### 2. Memory Service Pattern

**Template:** `templates/memory_service.py`

**Key Operations:**
```python
class MemoryService:
    async def add_conversation(
        user_id: str,
        messages: List[Dict[str, str]],
        metadata: Optional[Dict] = None
    ) -> Dict

    async def search_memories(
        query: str,
        user_id: str,
        limit: int = 5
    ) -> List[Dict]

    async def get_user_summary(user_id: str) -> Dict

    async def add_user_preference(
        user_id: str,
        preference: str,
        category: str = "general"
    ) -> bool
```

**Initialization:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    memory_service = MemoryService()
    app.state.memory_service = memory_service
    yield
    # Shutdown
```

## Memory Patterns

### 1. Conversation Persistence

**When to use:** Chat applications, conversational AI

**Template:** `templates/memory_service.py#add_conversation`

```python
async def add_conversation(
    self,
    user_id: str,
    messages: List[Dict[str, str]],
    metadata: Optional[Dict[str, Any]] = None
) -> Optional[Dict]:
    enhanced_metadata = {
        "timestamp": datetime.now().isoformat(),
        "conversation_type": "chat",
        **(metadata or {})
    }

    if self.client:
        result = self.client.add(
            messages=messages,
            user_id=user_id,
            metadata=enhanced_metadata
        )
    elif self.memory:
        result = await self.memory.add(
            messages=messages,
            user_id=user_id,
            metadata=enhanced_metadata
        )

    return result
```

**Best for:** Chat history, conversation context, multi-turn interactions

### 2. Semantic Memory Search

**When to use:** Context retrieval, relevant history lookup

**Template:** `templates/memory_service.py#search_memories`

```python
async def search_memories(
    self,
    query: str,
    user_id: str,
    limit: int = 5,
    filters: Optional[Dict] = None
) -> List[Dict]:
    if self.client:
        result = self.client.search(
            query=query,
            user_id=user_id,
            limit=limit
        )
    elif self.memory:
        result = await self.memory.search(
            query=query,
            user_id=user_id,
            limit=limit
        )

    memories = result.get('results', [])
    return memories
```

**Best for:** Finding relevant past conversations, context-aware responses

### 3. User Preference Storage

**When to use:** Personalization, user settings, behavioral tracking

**Template:** `templates/memory_service.py#add_user_preference`

```python
async def add_user_preference(
    self,
    user_id: str,
    preference: str,
    category: str = "general"
) -> bool:
    preference_message = {
        "role": "system",
        "content": f"User preference ({category}): {preference}"
    }

    metadata = {
        "type": "preference",
        "category": category,
        "timestamp": datetime.now().isoformat()
    }

    if self.client:
        self.client.add(
            messages=[preference_message],
            user_id=user_id,
            metadata=metadata
        )
    elif self.memory:
        await self.memory.add(
            messages=[preference_message],
            user_id=user_id,
            metadata=metadata
        )

    return True
```

**Best for:** User customization, learning user behavior, preference management

## API Routes Integration

### 1. Memory Management Endpoints

**Template:** `templates/memory_routes.py`

```python
from fastapi import APIRouter, Depends, BackgroundTasks
from app.api.deps import get_current_user, get_memory_service
from app.services.memory_service import MemoryService

router = APIRouter()

@router.post("/conversation")
async def add_conversation(
    request: ConversationRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service)
):
    # Add to memory in background
    background_tasks.add_task(
        memory_service.add_conversation,
        user_id,
        request.messages,
        request.metadata
    )

    return {
        "status": "success",
        "message": "Conversation added to memory"
    }

@router.post("/search")
async def search_memories(
    request: SearchRequest,
    user_id: str = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service)
):
    memories = await memory_service.search_memories(
        query=request.query,
        user_id=user_id,
        limit=request.limit
    )

    return {
        "query": request.query,
        "results": memories,
        "count": len(memories)
    }

@router.get("/summary")
async def get_memory_summary(
    user_id: str = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service)
):
    summary = await memory_service.get_user_summary(user_id)
    return {"user_id": user_id, "summary": summary}
```

### 2. Request Models

**Template:** `templates/memory_routes.py#models`

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ConversationRequest(BaseModel):
    messages: List[Dict[str, str]] = Field(..., description="Conversation messages")
    session_id: Optional[str] = Field(None, description="Session identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(5, ge=1, le=20, description="Number of results")
    filters: Optional[Dict[str, Any]] = Field(None, description="Search filters")

class PreferenceRequest(BaseModel):
    preference: str = Field(..., description="User preference")
    category: str = Field("general", description="Preference category")
```

## Background Task Integration

### 1. Async Memory Storage

**Pattern:**
```python
from fastapi import BackgroundTasks

@router.post("/chat")
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    memory_service: MemoryService = Depends(get_memory_service)
):
    # Generate AI response
    response = await ai_service.generate(request.message)

    # Store conversation in background
    background_tasks.add_task(
        memory_service.add_conversation,
        user_id=request.user_id,
        messages=[
            {"role": "user", "content": request.message},
            {"role": "assistant", "content": response}
        ]
    )

    return {"response": response}
```

**Benefits:**
- Non-blocking memory operations
- Faster response times
- Graceful failure handling

### 2. Batch Memory Updates

**Pattern:**
```python
async def batch_update_memories(
    conversations: List[Conversation],
    memory_service: MemoryService
):
    tasks = [
        memory_service.add_conversation(
            user_id=conv.user_id,
            messages=conv.messages
        )
        for conv in conversations
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## Dependency Injection Pattern

### 1. Memory Service Dependency

**Template:** `templates/memory_middleware.py#deps`

```python
from fastapi import Request

def get_memory_service(request: Request) -> MemoryService:
    """Get memory service from app state"""
    return request.app.state.memory_service

# Usage in routes
@router.get("/")
async def endpoint(
    memory_service: MemoryService = Depends(get_memory_service)
):
    memories = await memory_service.search_memories(...)
    return memories
```

### 2. User Context Injection

**Pattern:**
```python
async def get_user_context(
    user_id: str = Depends(get_current_user),
    memory_service: MemoryService = Depends(get_memory_service)
) -> Dict[str, Any]:
    """Get enriched user context from memory"""
    summary = await memory_service.get_user_summary(user_id)
    return {
        "user_id": user_id,
        "preferences": summary.get("user_preferences", []),
        "total_conversations": summary.get("total_memories", 0)
    }

# Usage
@router.post("/personalized-response")
async def personalized(
    request: QueryRequest,
    context: Dict = Depends(get_user_context)
):
    # Use context for personalized AI response
    pass
```

## Implementation Workflow

### Step 1: Setup Mem0

```bash
# Install and configure Mem0
./scripts/setup-mem0.sh
```

**Creates:**
- Mem0 configuration file
- Environment variable template
- Vector database setup (if self-hosted)

### Step 2: Configure Memory Service

**Decision tree:**
- **Hosted Mem0**: Use MemoryClient with API key (simple, managed)
- **Self-Hosted**: Use AsyncMemory with config (full control, cost-effective)
- **Hybrid**: Support both with fallback logic

### Step 3: Integrate with FastAPI Lifespan

**Pattern:**
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    memory_service = MemoryService()
    app.state.memory_service = memory_service
    logger.info("Memory service initialized")

    yield

    # Shutdown
    logger.info("Shutting down memory service")
```

### Step 4: Add Memory Routes

**Use template:** `templates/memory_routes.py`

**Register:**
```python
app.include_router(
    memory.router,
    prefix=f"{settings.API_V1_STR}/memory",
    tags=["memory"]
)
```

### Step 5: Test Memory Service

```bash
# Run memory service tests
./scripts/test-memory.sh
```

**Tests:**
- Add conversation
- Search memories
- Get user summary
- Add preferences
- Error handling

## Optimization Strategies

### 1. Memory Caching

**Pattern:**
```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedMemoryService(MemoryService):
    def __init__(self):
        super().__init__()
        self._cache = {}
        self._cache_ttl = timedelta(minutes=5)

    async def search_memories(self, query: str, user_id: str, limit: int = 5):
        cache_key = f"{user_id}:{query}:{limit}"

        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if datetime.now() - cached_time < self._cache_ttl:
                return cached_result

        result = await super().search_memories(query, user_id, limit)
        self._cache[cache_key] = (datetime.now(), result)
        return result
```

### 2. Batch Operations

**Pattern:**
```python
async def batch_add_conversations(
    conversations: List[Tuple[str, List[Dict]]],
    memory_service: MemoryService
):
    """Add multiple conversations efficiently"""
    tasks = [
        memory_service.add_conversation(user_id, messages)
        for user_id, messages in conversations
    ]
    return await asyncio.gather(*tasks)
```

### 3. Error Handling with Fallback

**Pattern:**
```python
async def resilient_memory_add(
    user_id: str,
    messages: List[Dict],
    memory_service: MemoryService
):
    try:
        return await memory_service.add_conversation(user_id, messages)
    except Exception as e:
        logger.error(f"Memory add failed: {e}")
        # Fallback: Queue for retry or log to backup storage
        await backup_storage.save(user_id, messages)
        return None
```

## Production Best Practices

### 1. Environment Configuration

**Template:** `.env` variables
```bash
# Hosted Mem0
MEM0_API_KEY=your_mem0_api_key

# Self-Hosted Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=your_qdrant_key
OPENAI_API_KEY=your_openai_key

# Memory Settings
MEMORY_CACHE_TTL_SECONDS=300
MEMORY_SEARCH_LIMIT_DEFAULT=5
MEMORY_SEARCH_LIMIT_MAX=20
```

### 2. Monitoring and Logging

**Pattern:**
```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MonitoredMemoryService(MemoryService):
    async def add_conversation(self, user_id: str, messages: List[Dict], metadata=None):
        start_time = datetime.now()
        try:
            result = await super().add_conversation(user_id, messages, metadata)
            latency = (datetime.now() - start_time).total_seconds()
            logger.info(f"Memory add success: user={user_id}, latency={latency}s")
            return result
        except Exception as e:
            logger.error(f"Memory add failed: user={user_id}, error={e}")
            raise
```

### 3. Rate Limiting

**Pattern:**
```python
from fastapi import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/search")
@limiter.limit("10/minute")
async def search_memories(request: Request, ...):
    # Rate-limited memory search
    pass
```

## Common Memory Patterns

### 1. Chat with Memory

**Example:** `examples/chat_with_memory.py`

Complete chat implementation with conversation history and context retrieval

**Features:**
- Automatic conversation storage
- Context-aware responses
- Session management
- Memory search integration

### 2. User Preference Management

**Example:** `examples/user_preferences.py`

User preference tracking and personalization

**Features:**
- Preference categorization
- Preference retrieval
- Behavioral learning
- Personalized AI responses

### 3. Multi-User Memory Isolation

**Pattern:**
```python
async def get_user_memories_isolated(
    user_id: str,
    memory_service: MemoryService
):
    """Ensure memory isolation between users"""
    # All memory operations scoped to user_id
    memories = await memory_service.search_memories(
        query="...",
        user_id=user_id  # Always scoped
    )
    return memories
```

## Vector Database Support

### Supported Vector Databases

**1. Qdrant (Recommended for Self-Hosted)**
```python
vector_store={
    "provider": "qdrant",
    "config": {
        "host": "localhost",
        "port": 6333,
        "api_key": settings.QDRANT_API_KEY
    }
}
```

**2. Pinecone (Fully Managed)**
```python
vector_store={
    "provider": "pinecone",
    "config": {
        "api_key": settings.PINECONE_API_KEY,
        "environment": "us-west1-gcp"
    }
}
```

**3. Chroma (Local Development)**
```python
vector_store={
    "provider": "chroma",
    "config": {
        "host": "localhost",
        "port": 8000
    }
}
```

## Resources

**Scripts:**
- `setup-mem0.sh` - Install and configure Mem0
- `test-memory.sh` - Test memory service functionality

**Templates:**
- `memory_service.py` - Complete MemoryService implementation
- `memory_client.py` - Mem0 client configuration
- `memory_middleware.py` - Middleware and dependencies
- `memory_routes.py` - FastAPI routes for memory operations

**Examples:**
- `chat_with_memory.py` - Complete chat with memory
- `user_preferences.py` - User preference management
- `memory_analytics.py` - Memory usage analytics

---

**Supported Configurations:** Hosted Mem0, Self-Hosted (Qdrant, Pinecone, Chroma)
**FastAPI Version:** 0.100+
**Mem0 Version:** 0.1.0+
**Python Version:** 3.9+

**Best Practice:** Start with hosted Mem0 for simplicity, migrate to self-hosted for cost optimization
