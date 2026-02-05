---
name: fastapi-patterns
description: FastAPI 0.121+ production patterns with async SQLAlchemy 2.0.44, Pydantic V2.12.4, dependency injection, and enterprise architecture. Use for REST API development.
triggers:
  keywords: ["fastapi", "router", "endpoint", "APIRouter", "dependency injection", "Depends", "async", "sqlalchemy", "pydantic"]
  file_patterns: ["**/api/**/*.py", "**/api/v1/**/*.py", "**/core/**/*.py", "**/services/**/*.py"]
  context: ["creating API endpoints", "fastapi routing", "dependency injection", "service layer", "api development"]
---

# FastAPI Patterns Skill

Production-ready patterns for FastAPI 0.121+ with async SQLAlchemy 2.0.44, Pydantic V2.12.4, and enterprise architecture.

## 🎯 When to Use This Skill

**Auto-activates when:**
- Keywords: `fastapi`, `APIRouter`, `Depends`, `router`, `endpoint`, `async def`, `service layer`
- Files: `backend/api/`, `backend/core/`, `backend/services/`, `backend/models/`
- Tasks: creating REST endpoints, dependency injection, service layer design, async database operations

**NOT for:**
- Frontend components → use `react-enterprise` skill
- Agent integration → use `deepagents-integration` skill
- Database models design → covered here, but focus on API patterns

## ⚡ Quick Reference

### Top 10 Essential Patterns

```python
# 1. Router with Type-Safe Dependencies (Pydantic V2)
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("", response_model=AgentResponse, status_code=201)
async def create_agent(
    agent: AgentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> AgentResponse:
    service = AgentService()
    return await service.create_agent(db, agent, current_user.id)

# 2. Database Session Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# 3. Current User Dependency
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id: int = payload.get("sub")
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# 4. Service Layer Pattern
class AgentService:
    async def create_agent(
        self,
        db: AsyncSession,
        agent_data: AgentCreate,
        user_id: int
    ) -> Agent:
        agent = Agent(**agent_data.model_dump(), created_by_id=user_id)
        db.add(agent)
        await db.commit()
        await db.refresh(agent)
        return agent

# 5. Async Query with SQLAlchemy 2.0
from sqlalchemy import select

async def get_agents(db: AsyncSession, user_id: int) -> list[Agent]:
    stmt = select(Agent).where(Agent.created_by_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

# 6. Error Handling
from fastapi import HTTPException, status

@router.get("/{agent_id}")
async def get_agent(agent_id: int, db: DatabaseDep) -> AgentResponse:
    agent = await db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent

# 7. Request Validation (Pydantic V2)
from pydantic import BaseModel, Field, field_validator

class AgentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    model_name: str = Field(pattern=r"^(claude|gpt)-.*$")
    temperature: float = Field(ge=0.0, le=2.0, default=0.7)
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v.strip() != v:
            raise ValueError("Name cannot have leading/trailing spaces")
        return v

# 8. Response Model with Relationships
class AgentResponse(BaseModel):
    id: int
    name: str
    model_name: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 9. WebSocket Connection
from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws/{agent_id}")
async def agent_websocket(websocket: WebSocket, agent_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Process and send response
            await websocket.send_json({"response": data})
    except WebSocketDisconnect:
        pass

# 10. Lifespan Events
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting application")
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

## 📁 Project Structure

```
backend/
├── main.py                        # FastAPI app entry point
├── core/                          # Core application components
│   ├── config.py                  # Pydantic Settings
│   ├── database.py                # SQLAlchemy async engine
│   ├── security.py                # JWT, password hashing
│   └── middleware.py              # Custom middleware
├── api/                           # API layer
│   ├── deps.py                    # Shared dependencies
│   └── v1/                        # API version 1
│       ├── __init__.py
│       ├── agents.py              # Agent endpoints
│       ├── users.py               # User endpoints
│       └── auth.py                # Authentication endpoints
├── services/                      # Business logic layer
│   ├── agent_service.py           # Agent operations
│   ├── auth_service.py            # Authentication logic
│   └── execution_service.py       # Execution management
├── models/                        # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── base.py                    # Base model class
│   ├── user.py                    # User model
│   └── agent.py                   # Agent model
├── schemas/                       # Pydantic schemas
│   ├── __init__.py
│   ├── user.py                    # User schemas
│   └── agent.py                   # Agent schemas
└── tests/                         # Test suite
    ├── conftest.py                # Pytest fixtures
    ├── test_api/                  # API endpoint tests
    └── test_services/             # Service layer tests
```

## 🔧 Core Patterns

### 1. Router Pattern (RESTful Endpoints)

```python
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, get_current_user
from schemas.agent import AgentCreate, AgentUpdate, AgentResponse
from services.agent_service import AgentService
from models.user import User

# Type aliases for cleaner code
DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/agents", tags=["agents"])

# ✅ CORRECT: Full CRUD with proper status codes
@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent: AgentCreate,
    db: DatabaseDep,
    current_user: CurrentUserDep
) -> AgentResponse:
    """Create new agent configuration."""
    service = AgentService()
    return await service.create_agent(db, agent, current_user.id)

@router.get("", response_model=list[AgentResponse])
async def list_agents(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
) -> list[AgentResponse]:
    """List user's agents with pagination."""
    service = AgentService()
    return await service.list_agents(db, current_user.id, skip, limit)

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    db: DatabaseDep,
    current_user: CurrentUserDep
) -> AgentResponse:
    """Get agent by ID."""
    service = AgentService()
    agent = await service.get_agent(db, agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    
    # 🔒 Security: Check ownership
    if agent.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this agent"
        )
    
    return agent

@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_update: AgentUpdate,
    db: DatabaseDep,
    current_user: CurrentUserDep
) -> AgentResponse:
    """Update agent configuration."""
    service = AgentService()
    agent = await service.update_agent(db, agent_id, agent_update, current_user.id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: int,
    db: DatabaseDep,
    current_user: CurrentUserDep
) -> None:
    """Soft delete agent."""
    service = AgentService()
    await service.delete_agent(db, agent_id, current_user.id)

# ❌ WRONG: Missing type hints, no dependency injection
@router.get("/bad")
def bad_endpoint(agent_id):  # No async, no types
    agent = Agent.query.filter_by(id=agent_id).first()  # Sync query!
    return agent
```

**Troubleshooting**:
- **422 Validation Error** → Check Pydantic schema fields match request body
- **Dependency not injected** → Ensure `Depends()` is used correctly
- **Database session errors** → Verify async session management in `get_db()`

---

### 2. Dependency Injection Pattern

```python
# api/deps.py
from typing import AsyncGenerator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import async_session_maker
from models.user import User

# OAuth2 scheme for JWT tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ✅ CORRECT: Database session with auto-commit/rollback
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency with automatic commit/rollback.
    
    Yields:
        AsyncSession: Database session
    
    Behavior:
        - Commits on success
        - Rolls back on exception
        - Always closes session
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# ✅ CORRECT: Current user from JWT token
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        token: JWT access token from Authorization header
        db: Database session
    
    Returns:
        User: Authenticated user
    
    Raises:
        HTTPException: 401 if token invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    
    return user

# ✅ CORRECT: Optional authentication
async def get_current_user_optional(
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
    db: Annotated[AsyncSession, Depends(get_db)] = None
) -> User | None:
    """Get current user if authenticated, None otherwise."""
    if not token:
        return None
    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None

# Type aliases for cleaner endpoint signatures
DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
OptionalUserDep = Annotated[User | None, Depends(get_current_user_optional)]
```

**Troubleshooting**:
- **Session not committing** → Check if exception is raised before commit
- **Token validation fails** → Verify `SECRET_KEY` matches between token creation/validation
- **Circular dependency** → Ensure dependencies don't depend on each other

---

### 3. Service Layer Pattern

```python
# services/agent_service.py
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.agent import Agent, AgentTool
from schemas.agent import AgentCreate, AgentUpdate

class AgentService:
    """Business logic for agent operations."""
    
    async def create_agent(
        self,
        db: AsyncSession,
        agent_data: AgentCreate,
        user_id: int
    ) -> Agent:
        """
        Create new agent.
        
        🔒 Security:
            - Validates user_id ownership
            - Sanitizes inputs via Pydantic
        """
        # Convert Pydantic model to dict
        agent_dict = agent_data.model_dump()
        
        # Create agent
        agent = Agent(**agent_dict, created_by_id=user_id, is_active=True)
        
        db.add(agent)
        await db.flush()  # Get ID without committing
        
        # Associate tools if provided
        if agent_data.tool_ids:
            for tool_id in agent_data.tool_ids:
                agent_tool = AgentTool(agent_id=agent.id, tool_id=tool_id)
                db.add(agent_tool)
        
        await db.commit()
        await db.refresh(agent)
        
        return agent
    
    async def get_agent(
        self,
        db: AsyncSession,
        agent_id: int
    ) -> Agent | None:
        """Get agent with eager-loaded relationships."""
        stmt = (
            select(Agent)
            .where(Agent.id == agent_id, Agent.is_active == True)
            .options(
                selectinload(Agent.agent_tools).selectinload(AgentTool.tool),
                selectinload(Agent.subagents)
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list_agents(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Agent]:
        """List user's agents with pagination."""
        stmt = (
            select(Agent)
            .where(Agent.created_by_id == user_id, Agent.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(Agent.created_at.desc())
        )
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def update_agent(
        self,
        db: AsyncSession,
        agent_id: int,
        agent_update: AgentUpdate,
        user_id: int
    ) -> Agent | None:
        """Update agent configuration."""
        agent = await self.get_agent(db, agent_id)
        
        if not agent or agent.created_by_id != user_id:
            return None
        
        # Update fields (exclude_unset to allow partial updates)
        update_data = agent_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        await db.commit()
        await db.refresh(agent)
        return agent
    
    async def delete_agent(
        self,
        db: AsyncSession,
        agent_id: int,
        user_id: int
    ) -> bool:
        """Soft delete agent."""
        agent = await self.get_agent(db, agent_id)
        
        if not agent or agent.created_by_id != user_id:
            return False
        
        agent.is_active = False
        await db.commit()
        return True
```

---

### 4. WebSocket Pattern

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import json

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: int):
        self.active_connections.pop(client_id, None)
    
    async def send_personal_message(self, message: dict, client_id: int):
        websocket = self.active_connections.get(client_id)
        if websocket:
            await websocket.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/executions/{execution_id}")
async def execution_websocket(
    websocket: WebSocket,
    execution_id: int,
    db: DatabaseDep
):
    """Stream execution progress via WebSocket."""
    await manager.connect(websocket, execution_id)
    
    try:
        while True:
            # Receive client messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process and send updates
            await manager.send_personal_message(
                {"type": "progress", "data": message},
                execution_id
            )
    except WebSocketDisconnect:
        manager.disconnect(execution_id)
```

---

## 🔒 Security Best Practices

### Authentication & Authorization

```python
# Inline in endpoints
@router.post("/{agent_id}/execute")
async def execute_agent(
    agent_id: int,
    db: DatabaseDep,
    current_user: CurrentUserDep  # 🔒 Requires authentication
):
    agent = await db.get(Agent, agent_id)
    
    # 🔒 Check ownership
    if agent.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Continue execution...
```

### Input Validation

```python
# Inline with Pydantic
class AgentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    
    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        # 🔒 Remove potentially dangerous characters
        return v.strip()
```

---

## 📚 See Also

- **reference.md** - Complete FastAPI API reference
- **examples.md** - Full working examples
- **deepagents-integration** - Agent integration patterns
- **react-enterprise** - Frontend integration
