---
name: rag_skill
description: Build and integrate production-ready RAG (Retrieval-Augmented Generation) chatbots into documentation sites using OpenAI, Qdrant Cloud, and Neon Postgres. Handles complete stack from backend API to frontend UI integration.
version: 1.0.0
---

This skill provides comprehensive guidance for building intelligent chatbots that answer questions based on documentation content using RAG architecture. It includes backend API development (FastAPI + OpenAI + Qdrant), conversation management (PostgreSQL), and frontend UI components (React/TypeScript for Docusaurus).

## What This Skill Does

1. **Backend Setup** - Configure FastAPI with OpenAI, Qdrant, and Neon Postgres
2. **RAG Service Implementation** - Build embedding generation, vector search, and LLM response generation
3. **Document Indexing** - Extract, chunk, and embed documentation content
4. **Frontend Integration** - Create React chat components with text selection and source citations
5. **Session Management** - Implement conversation memory and persistence
6. **Testing & Deployment** - Validate functionality and deploy to production
7. **Performance Optimization** - Monitor costs, response times, and accuracy

## When to Use This Skill

- Add an AI-powered Q&A chatbot to documentation sites
- Implement semantic search over documentation content
- Build conversational interfaces with source citations
- Create context-aware chatbots with text selection features
- Integrate OpenAI, Qdrant, and PostgreSQL for RAG systems
- Deploy production-ready RAG applications with proper testing

## How This Skill Works

### Phase 1: Backend Setup

1. **Create project structure:**
   ```bash
   mkdir backend
   cd backend
   ```

2. **Install dependencies** (requirements.txt):
   ```
   fastapi==0.115.0
   uvicorn[standard]==0.32.0
   python-dotenv==1.0.1
   openai==1.54.0
   qdrant-client==1.12.0
   psycopg2-binary==2.9.10
   sqlalchemy==2.0.35
   pydantic==2.9.2
   pydantic-settings==2.6.0
   python-multipart==0.0.12
   markdown==3.7
   beautifulsoup4==4.12.3
   tiktoken==0.8.0
   ```

3. **Configure environment variables** (.env):
   - `OPENAI_API_KEY`: OpenAI API key from platform.openai.com
   - `QDRANT_URL`: Qdrant Cloud cluster URL (https://xxx.cloud.qdrant.io:6333)
   - `QDRANT_API_KEY`: Qdrant Cloud API key
   - `QDRANT_COLLECTION_NAME`: Collection name (e.g., "ai_native_book")
   - `DATABASE_URL`: Neon Postgres connection string
   - `CORS_ORIGINS`: Allowed origins (e.g., "http://localhost:3000")

4. **Implement core services:**
   - **RAG Service** (rag_service.py):
     - Embedding generation using OpenAI text-embedding-3-small
     - Vector similarity search in Qdrant
     - LLM response generation with GPT-4o-mini
     - Context building from retrieved documents

   - **Database Models** (models.py):
     - ChatSession (session_id, created_at, last_activity)
     - ChatMessage (session_id, role, content, timestamp)

   - **API Endpoints** (main.py):
     - `GET /api/health`: System status and service connectivity
     - `POST /api/chat`: Send message and get AI response
     - `GET /api/sessions/{session_id}/history`: Retrieve conversation history

5. **Create document indexing pipeline** (indexer.py):
   - Extract content from markdown/MDX files
   - Clean and preprocess text
   - Chunk documents (1000 words with 200-word overlap)
   - Generate embeddings using OpenAI
   - Store vectors in Qdrant with metadata (title, file_path, sidebar_position)

### Phase 2: Frontend Integration

1. **Create chat component** (book/src/components/RAGChatbot/):
   ```typescript
   // index.tsx - Main chat component
   - Message display with user/assistant roles
   - Loading states and typing animations
   - Source citation display
   - Error handling and retry logic
   - Session persistence
   ```

2. **Add styling** (styles.module.css):
   - Dark mode support
   - Responsive design
   - Smooth animations
   - Accessibility (ARIA labels, keyboard navigation)

3. **Implement text selection feature:**
   - Detect text selection on documentation page
   - Show yellow context indicator banner
   - Include selected text in API requests
   - Clear selection after use

4. **Create global integration** (book/src/theme/Root.tsx):
   - Wrap Docusaurus with chat component
   - Configure API endpoint URL
   - Enable CORS headers

### Phase 3: Testing & Deployment

1. **Run comprehensive test suite** (test_api.py):
   - **Health Check Test**: Verify all services connected
   - **Basic Q&A Test**: Test RAG retrieval and generation
   - **Context-Aware Test**: Test conversation memory
   - **Text Selection Test**: Test selected text integration
   - **Session Management Test**: Test database persistence

2. **Deploy backend:**
   - Deploy to Railway, Render, or AWS
   - Configure production environment variables
   - Enable HTTPS and proper CORS
   - Set up monitoring and logging

3. **Deploy frontend:**
   - Update API URL to production endpoint
   - Build and deploy Docusaurus site
   - Verify CORS and connectivity

4. **Verify deployment:**
   - Test health endpoint
   - Run smoke tests with sample queries
   - Monitor performance and errors
   - Check cost tracking

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **LLM Provider**: OpenAI (GPT-4o-mini for chat, text-embedding-3-small for embeddings)
- **Vector Database**: Qdrant Cloud (free tier: 1GB storage)
- **Relational Database**: Neon Serverless Postgres (free tier: 0.5GB storage, 100 hours compute)
- **Additional Libraries**: SQLAlchemy, Pydantic, python-dotenv, BeautifulSoup4, tiktoken

### Frontend
- **Framework**: React + TypeScript
- **Integration**: Docusaurus v3+
- **Styling**: CSS Modules with dark mode support
- **Features**: Text selection, session management, source citations

### Cloud Services Required

1. **OpenAI Account**
   - API key from platform.openai.com
   - Billing enabled
   - Cost: ~$5-10/month for moderate usage (1000 queries)

2. **Qdrant Cloud**
   - Free tier: 1GB storage
   - Create cluster at cloud.qdrant.io
   - Copy cluster URL and API key

3. **Neon Postgres**
   - Free tier: 0.5GB storage, 100 hours compute
   - Create database at neon.tech
   - Copy connection string

## Architecture Components

### Backend API Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI application with endpoints
│   ├── config.py            # Configuration and settings
│   ├── models.py            # Pydantic and SQLAlchemy models
│   ├── database.py          # Database connection and session management
│   ├── services/
│   │   ├── rag_service.py       # RAG logic (embeddings + retrieval + generation)
│   │   ├── conversation.py      # Conversation management
│   │   └── vector_store.py      # Qdrant vector operations
│   └── schemas/
│       └── chat.py              # Request/response schemas
├── scripts/
│   ├── index_docs.py        # Document indexing script
│   └── clear_and_reindex.py # Clear collection and reindex
├── tests/
│   └── test_api.py          # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
├── .env.example             # Environment variables template
├── Dockerfile               # Container configuration
└── docker-compose.yml       # Multi-service orchestration
```

### Core API Endpoints

**Health Check**: `GET /api/health`
- Returns system status and service connectivity
- Example response:
  ```json
  {
    "status": "healthy",
    "openai": "connected",
    "qdrant": "connected",
    "postgres": "connected"
  }
  ```

**Chat**: `POST /api/chat`
- Input:
  ```json
  {
    "message": "What is Physical AI?",
    "session_id": "uuid-optional",
    "selected_text": "optional selected context"
  }
  ```
- Output:
  ```json
  {
    "session_id": "uuid",
    "message": "AI response with context",
    "sources": [
      {
        "title": "Introduction to Physical AI",
        "file_path": "/docs/intro.md",
        "score": 0.85
      }
    ],
    "timestamp": "2025-12-02T10:30:00Z"
  }
  ```

**Session History**: `GET /api/sessions/{session_id}/history`
- Returns full conversation history for a session
- Example response:
  ```json
  {
    "session_id": "uuid",
    "messages": [
      {
        "role": "user",
        "content": "What is Physical AI?",
        "timestamp": "2025-12-02T10:30:00Z"
      },
      {
        "role": "assistant",
        "content": "Physical AI refers to...",
        "timestamp": "2025-12-02T10:30:02Z"
      }
    ]
  }
  ```

### Frontend Components Structure

```
book/src/
├── theme/
│   ├── components/
│   │   └── ChatWidget/
│   │       ├── index.tsx           # Main chat component
│   │       ├── ChatWindow.tsx      # Chat window UI
│   │       ├── MessageList.tsx     # Message display
│   │       ├── MessageInput.tsx    # Input field
│   │       ├── SourceCitation.tsx  # Source display
│   │       └── styles.module.css   # Component styles
│   └── Root.tsx                     # Global wrapper for chatbot
└── css/
    └── custom.css                   # Global styles
```

## Key Features Implementation

### 1. RAG-Powered Responses

**Semantic Search Pattern:**
```python
# Generate query embedding
query_embedding = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=user_query
).data[0].embedding

# Search in Qdrant
similar_docs = qdrant_client.search(
    collection_name="ai_native_book",
    query_vector=query_embedding,
    limit=5
)

# Build context from top results
context = "\n\n".join([
    f"[{doc.payload['title']}]\n{doc.payload['content']}"
    for doc in similar_docs
])
```

**Response Generation Pattern:**
```python
# Generate response with context
response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        *chat_history[-6:],  # Last 3 exchanges
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_query}"}
    ],
    temperature=0.7,
    max_tokens=1000
)
```

### 2. Text Selection Context

**Frontend Detection:**
```typescript
useEffect(() => {
  const handleSelection = () => {
    const selection = window.getSelection();
    const text = selection?.toString().trim();
    if (text && text.length > 10) {
      setSelectedText(text);
      setShowContextBanner(true);
    }
  };

  document.addEventListener('mouseup', handleSelection);
  return () => document.removeEventListener('mouseup', handleSelection);
}, []);
```

**Backend Integration:**
```python
# Include selected text in prompt if provided
if selected_text:
    user_message = f"Selected text: '{selected_text}'\n\n{user_message}"
```

### 3. Conversation Memory

**Database Storage:**
```python
# Store chat history in Postgres
new_message = ChatMessage(
    session_id=session.id,
    role="user",
    content=user_message,
    timestamp=datetime.utcnow()
)
db.add(new_message)
db.commit()

# Retrieve history
chat_history = db.query(ChatMessage).filter(
    ChatMessage.session_id == session.id
).order_by(ChatMessage.timestamp.desc()).limit(10).all()
```

**Context Building:**
```python
# Include in LLM context
history_messages = [
    {"role": msg.role, "content": msg.content}
    for msg in reversed(chat_history)
]
```

### 4. Source Citations

**Return Sources:**
```python
sources = [
    {
        "title": doc.payload["title"],
        "file_path": doc.payload["file_path"],
        "score": round(doc.score, 3)
    }
    for doc in similar_docs[:3]
]
```

**Frontend Display:**
```typescript
{sources.map((source, idx) => (
  <div key={idx} className={styles.source}>
    <a href={source.file_path}>{source.title}</a>
    <span className={styles.score}>
      {Math.round(source.score * 100)}% match
    </span>
  </div>
))}
```

## Document Indexing Strategy

### Chunking Parameters
- **Chunk Size**: 1000 words (configurable)
- **Overlap**: 200 words (maintains context continuity)
- **Metadata**: Title, file path, chunk index, sidebar position
- **Processing**: Clean HTML, remove code blocks, normalize whitespace

### Embedding Model
- **Model**: text-embedding-3-small (1536 dimensions)
- **Cost**: ~$0.00002 per 1K tokens
- **Performance**: ~100ms per embedding
- **Batch Size**: 100 documents per batch

### Vector Search Configuration
- **Distance Metric**: Cosine similarity
- **Results**: Top 5 most relevant chunks
- **Threshold**: Minimum 0.5 similarity score
- **Metadata Filtering**: Support filtering by file path, section

### Indexing Script Usage

```bash
# Index all documentation
cd backend
source venv/bin/activate
python scripts/index_docs.py

# Clear and reindex
python scripts/clear_and_reindex.py
```

## Performance Metrics

### Expected Response Times
- **Embedding Generation**: ~100ms
- **Vector Search**: ~50ms
- **LLM Generation**: ~1-2 seconds
- **Database Operations**: ~50ms
- **Total Response**: ~1.5-2.5 seconds (95th percentile < 3s)

### Accuracy Metrics
- **Relevance Scores**: 55-75% for top results
- **Context Retrieval**: 3-5 relevant chunks per query
- **Answer Quality**: High when relevant context is found
- **Source Attribution**: 90%+ accuracy

### Performance Targets
- **API Response Time**: < 3 seconds (95th percentile)
- **Vector Search**: < 100ms
- **Database Queries**: < 50ms
- **Frontend Render**: < 16ms (60fps)
- **Uptime**: 95%+

## Testing Strategy

### Test Coverage Areas

1. **Health Checks**: Verify all services connected
   ```python
   response = requests.get(f"{BASE_URL}/api/health")
   assert response.json()["status"] == "healthy"
   assert response.json()["openai"] == "connected"
   assert response.json()["qdrant"] == "connected"
   assert response.json()["postgres"] == "connected"
   ```

2. **Basic Q&A**: Test RAG retrieval and generation
   ```python
   response = requests.post(
       f"{BASE_URL}/api/chat",
       json={"message": "What is Physical AI?"}
   )
   assert "session_id" in response.json()
   assert len(response.json()["sources"]) > 0
   assert response.json()["message"]
   ```

3. **Context Awareness**: Test conversation memory
   ```python
   # First message
   response1 = requests.post(
       f"{BASE_URL}/api/chat",
       json={"message": "What is ROS 2?"}
   )
   session_id = response1.json()["session_id"]

   # Follow-up message
   response2 = requests.post(
       f"{BASE_URL}/api/chat",
       json={
           "message": "What are its main features?",
           "session_id": session_id
       }
   )
   assert "ROS 2" in response2.json()["message"]
   ```

4. **Text Selection**: Test selected text integration
   ```python
   response = requests.post(
       f"{BASE_URL}/api/chat",
       json={
           "message": "Explain this",
           "selected_text": "Physical AI combines artificial intelligence with physical robotics"
       }
   )
   assert response.status_code == 200
   ```

5. **Session Management**: Test database persistence
   ```python
   response = requests.get(
       f"{BASE_URL}/api/sessions/{session_id}/history"
   )
   assert len(response.json()["messages"]) >= 2
   ```

### Sample Test Script

```python
import requests

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed")

def test_basic_qa():
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={"message": "What is Physical AI?"}
    )
    assert "session_id" in response.json()
    assert len(response.json()["sources"]) > 0
    print("✅ Basic Q&A passed")

if __name__ == "__main__":
    test_health()
    test_basic_qa()
```

## Common Issues & Solutions

### Issue: "process is not defined" in browser
**Cause**: Using Node.js `process.env` in React browser code

**Solution**: Use hardcoded values or build-time environment variables
```typescript
// ❌ Wrong - process.env doesn't exist in browser
<RAGChatbot apiUrl={process.env.REACT_APP_API_URL} />

// ✅ Correct - hardcode or use Docusaurus config
<RAGChatbot apiUrl="http://localhost:8000" />
```

### Issue: OpenAI client initialization error
**Cause**: Outdated OpenAI SDK version

**Solution**: Upgrade to latest version
```bash
pip install --upgrade openai
```

### Issue: Empty search results
**Cause**: Documents not indexed in Qdrant

**Solution**: Run indexing script
```bash
cd backend
python scripts/index_docs.py
```

### Issue: CORS errors
**Cause**: CORS origins not configured properly

**Solution**: Configure CORS in backend
```python
# config.py
CORS_ORIGINS = "http://localhost:3000,https://your-domain.com"
```

### Issue: Qdrant connection failures
**Cause**: Incorrect cluster URL or API key

**Solution**: Verify configuration
- Cluster URL must include port: `https://xxx.cloud.qdrant.io:6333`
- API key must be valid
- Test with health endpoint

### Issue: Slow responses
**Cause**: Too many context chunks or slow LLM model

**Solution**: Optimize retrieval and model
- Reduce chunk retrieval limit (5 → 3)
- Use faster model (GPT-4o-mini)
- Implement caching
- Reduce context size

### Issue: Database connection errors
**Cause**: Invalid Neon connection string

**Solution**: Verify connection string format
```
postgresql://user:password@host/database?sslmode=require
```

## Deployment Checklist

### Pre-Deployment
- [ ] All environment variables configured
- [ ] Documents indexed in Qdrant
- [ ] Database tables created in Neon
- [ ] Test suite passing (5/5 tests)
- [ ] Local build successful
- [ ] No broken links or errors

### Backend Deployment
- [ ] Backend deployed to Railway/Render/AWS
- [ ] Production environment variables set
- [ ] HTTPS enabled
- [ ] CORS configured for production domain
- [ ] Health check endpoint returning success
- [ ] Monitoring/logging configured

### Frontend Deployment
- [ ] API URL updated to production endpoint
- [ ] Docusaurus site built successfully
- [ ] Chat widget visible and functional
- [ ] Text selection feature working
- [ ] Sources displaying correctly

### Post-Deployment
- [ ] Smoke tests passing
- [ ] Response times acceptable (< 3s)
- [ ] No CORS errors
- [ ] Conversation memory working
- [ ] Cost tracking enabled
- [ ] Error monitoring active

## Cost Estimation

**Monthly costs (moderate usage - 1000 queries):**
- **OpenAI Embeddings**: ~$0.50 (1000 queries × 1000 words × $0.00002 per 1K tokens)
- **OpenAI Chat**: ~$5-10 (1000 responses × ~1000 tokens × $0.15-0.60 per 1M tokens)
- **Qdrant Cloud**: $0 (free tier - 1GB storage)
- **Neon Postgres**: $0 (free tier - 0.5GB storage, 100 hours compute)
- **Hosting**: $5-10 (Railway/Render free tier or basic plan)
- **Total**: **$5-20/month**

**Cost optimization tips:**
- Use GPT-4o-mini instead of GPT-4o (10x cheaper)
- Cache embeddings for common queries
- Reduce chunk retrieval limit
- Monitor usage and set limits

## Success Criteria

A successful RAG chatbot implementation should achieve:

✅ **Functional Requirements**:
- User asks question → Gets relevant answer
- User selects text → Context indicator appears
- Follow-up questions → Conversation memory works
- Sources shown → User can verify information
- All tests passing (5/5)

✅ **Performance Requirements**:
- Response time < 3 seconds (95th percentile)
- Vector search < 100ms
- Database queries < 50ms
- Uptime 95%+

✅ **Quality Requirements**:
- Relevance score > 70% for top source
- Answer accuracy high when context available
- Source attribution accurate
- Error rate < 5%
- Positive user feedback

✅ **Cost Requirements**:
- Within budget ($5-20/month for moderate usage)
- Efficient token usage
- Optimized embedding calls

## Example Usage Workflow

1. **User opens documentation** → Chat button appears in bottom-right
2. **User clicks chat button** → Chat window opens
3. **User asks "What is Physical AI?"** → Backend searches Qdrant for relevant chunks
4. **System finds 5 relevant chunks** → Combines with query and chat history
5. **OpenAI generates answer** → Returns with 3 source citations
6. **User sees answer + sources** → Can click sources to verify information
7. **User selects text on page** → Yellow context banner appears
8. **User asks "Explain this"** → Context-aware response using selected text
9. **User asks follow-up** → Conversation memory maintained
10. **User closes chat** → Session persisted in database

## Quality Gates

Before deployment to production, verify:
- [ ] All tests pass (health, Q&A, context, selection, session)
- [ ] Local build completes without errors
- [ ] No broken links or missing resources
- [ ] Performance targets met (< 3s response)
- [ ] Accessibility standards verified (ARIA labels, keyboard navigation)
- [ ] Security: API keys in environment variables, CORS configured
- [ ] Monitoring and error tracking enabled
- [ ] Cost tracking and limits configured

## Next Steps After Implementation

1. **Monitor and optimize:**
   - Track usage patterns and costs
   - Monitor response times and error rates
   - Collect user feedback
   - Optimize chunk size and retrieval parameters

2. **Enhance features:**
   - Add multi-language support
   - Implement voice input/output
   - Add feedback buttons (thumbs up/down)
   - Create analytics dashboard

3. **Scale infrastructure:**
   - Move to paid tiers as needed
   - Implement caching layer
   - Add rate limiting
   - Set up load balancing

4. **Improve quality:**
   - Fine-tune prompts
   - Optimize chunking strategy
   - Add more sophisticated context ranking
   - Implement A/B testing

## Output Format

When using this skill, you should have:

**Input Requirements:**
- Documentation content location (e.g., `book/docs/`)
- Desired chat features (text selection, sources, memory)
- Cloud service credentials (OpenAI, Qdrant, Neon)
- Deployment target (Railway, Render, AWS, etc.)

**Skill Returns:**

1. **Backend Implementation:**
   - FastAPI application with health, chat, and history endpoints
   - RAG service with embedding generation and vector search
   - Database models and session management
   - Document indexing script
   - Comprehensive test suite

2. **Frontend Implementation:**
   - React chat component with TypeScript
   - Text selection feature
   - Source citation display
   - Dark mode styling
   - Global Docusaurus integration

3. **Configuration Files:**
   - `.env.example` with all required variables
   - `requirements.txt` with pinned dependencies
   - `docker-compose.yml` for local development
   - API documentation and usage examples

4. **Testing & Deployment:**
   - Test scripts with all 5 test cases
   - Deployment instructions for chosen platform
   - Health check verification
   - Performance monitoring setup

5. **Documentation:**
   - Setup guide with step-by-step instructions
   - API endpoint documentation
   - Troubleshooting guide
   - Cost estimation and optimization tips

---

**Version**: 1.0.0
**Last Updated**: 2025-12-02
**Tested With**: Docusaurus 3.9.2, OpenAI API 1.54.0, Qdrant 1.12.0, FastAPI 0.115.0
