---
name: fastapi-backend
description: FastAPI routes, services, auth JWT, streaming, error handling, OpenAI integration
---

# FastAPI Backend — CEI-001

## Architecture Pattern

```
Route Layer (FastAPI)
  ↓ (validates request)
Service Layer (business logic)
  ↓ (Pydantic schema validation)
Data Layer (SQLAlchemy ORM)
  ↓
Response (Pydantic schema)
```

## Route Patterns

### Basic CRUD Route
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.evaluation import EvaluationCreate, EvaluationResponse
from app.services.evaluation_service import EvaluationService
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])

@router.post("", response_model=EvaluationResponse, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    eval_data: EvaluationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
) -> EvaluationResponse:
    """
    Create new evaluation for user
    
    Example:
    ```
    POST /api/evaluations
    {
        "company_id": "123e4567-e89b-12d3-a456-426614174000",
        "project_type": "new_erp"
    }
    ```
    """
    service = EvaluationService(db)
    return await service.create(current_user.id, eval_data)

@router.get("/{eval_id}", response_model=EvaluationResponse)
async def get_evaluation(
    eval_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
) -> EvaluationResponse:
    """Get evaluation by ID"""
    service = EvaluationService(db)
    evaluation = await service.get(eval_id, current_user.id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

@router.get("", response_model=list[EvaluationResponse])
async def list_evaluations(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
) -> list[EvaluationResponse]:
    """List user's evaluations"""
    service = EvaluationService(db)
    return await service.list(current_user.id, skip, limit)

@router.put("/{eval_id}", response_model=EvaluationResponse)
async def update_evaluation(
    eval_id: str,
    eval_data: EvaluationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
) -> EvaluationResponse:
    """Update evaluation"""
    service = EvaluationService(db)
    evaluation = await service.update(eval_id, current_user.id, eval_data)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

@router.delete("/{eval_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_evaluation(
    eval_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete evaluation"""
    service = EvaluationService(db)
    success = await service.delete(eval_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Evaluation not found")
```

### Streaming Route (Chat)
```python
from fastapi.responses import StreamingResponse

@router.post("/api/chat/message")
async def send_message(
    message_data: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
) -> StreamingResponse:
    """
    Send message to chat agent, stream response
    
    Streams back JSON lines: {"type": "content", "data": "text"}
    """
    service = ChatService(db)
    
    async def generate():
        async for chunk in service.stream_response(
            conversation_id=message_data.conversation_id,
            user_id=current_user.id,
            message=message_data.content
        ):
            # Send as JSON line
            yield f"data: {json.dumps(chunk)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Admin Protected Route
```python
from app.api.deps import get_admin_user

@router.post("/api/admin/documents/{doc_id}/pipeline")
async def start_pipeline(
    doc_id: str,
    config: PipelineConfig,
    db: AsyncSession = Depends(get_db),
    admin_user = Depends(get_admin_user)
):
    """Start document pipeline (admin only)"""
    service = DocumentPipelineService(db)
    return await service.start(doc_id, config)
```

## Service Layer Pattern

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class EvaluationService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: str, eval_data: EvaluationCreate):
        """Create evaluation with validation"""
        # Validate user exists
        user = await self.db.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Create record
        evaluation = Evaluation(
            user_id=user_id,
            **eval_data.dict()
        )
        self.db.add(evaluation)
        await self.db.commit()
        await self.db.refresh(evaluation)
        return evaluation
    
    async def get(self, eval_id: str, user_id: str):
        """Get evaluation (owner only)"""
        stmt = select(Evaluation).where(
            (Evaluation.id == eval_id) &
            (Evaluation.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list(self, user_id: str, skip: int = 0, limit: int = 10):
        """List user evaluations"""
        stmt = select(Evaluation)\
            .where(Evaluation.user_id == user_id)\
            .offset(skip)\
            .limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
```

## Auth & Dependencies

```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.core.security import decode_access_token
from app.models.user import User

security = HTTPBearer()

async def get_db() -> AsyncSession:
    """Get async session"""
    async with get_session() as session:
        yield session

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get authenticated user"""
    token = credentials.credentials
    user_id = decode_access_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré"
        )
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_admin_user(
    current_user = Depends(get_current_user)
) -> User:
    """Get admin user (verify role)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
```

## OpenAI Integration

```python
from openai import AsyncOpenAI

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.rag_service = RAGService()
    
    async def stream_response(self, conversation_id: str, user_id: str, message: str):
        """Stream chat response with RAG context"""
        
        # Save user message
        user_msg = Message(
            conversation_id=conversation_id,
            role="user",
            content=message
        )
        self.db.add(user_msg)
        await self.db.commit()
        
        # Get RAG context
        context = await self.rag_service.search(message, limit=3)
        
        # Build prompt
        system_prompt = self._build_system_prompt(context)
        
        # Stream from OpenAI
        async with self.client.messages.stream(
            model="gpt-4-turbo-preview",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": message}
            ]
        ) as stream:
            full_response = ""
            async for text in stream.text_stream:
                full_response += text
                yield {"type": "content", "data": text}
        
        # Save assistant response
        assistant_msg = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_response,
            sources=context
        )
        self.db.add(assistant_msg)
        await self.db.commit()
        
        yield {"type": "done"}
    
    def _build_system_prompt(self, context: list) -> str:
        """Build system prompt with RAG context"""
        sources = "\n".join([f"- {c['title']}: {c['content'][:200]}..." for c in context])
        return f"""Tu es un expert ERP pour PME manufacturières.

Contexte de connaissances:
{sources}

Réponds aux questions de l'utilisateur en utilisant ce contexte.
Cite les sources quand tu utilises le contexte.
Sois concis et pratique."""
```

## Error Handling

```python
@router.post("/api/chat/message")
async def send_message(
    message_data: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Send message with proper error handling"""
    try:
        service = ChatService(db)
        async for chunk in service.stream_response(...):
            yield chunk
    except ValueError as e:
        yield {"type": "error", "message": str(e)}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Chat error: {e}")
        yield {"type": "error", "message": "Internal server error"}
```

## Conventions

- Routes start with `/api/`
- Use descriptive HTTP methods (POST create, PUT update, DELETE delete)
- Always return status codes (201 create, 200 ok, 404 not found, 422 validation, 500 error)
- Docstring required on all route functions
- Use Pydantic schemas for request/response validation
- Service layer handles business logic
- Type hints everywhere
- Use `async/await` for async operations
- Error handling explicit with HTTPException
- Log important operations
- Pagination: `skip` and `limit` parameters
