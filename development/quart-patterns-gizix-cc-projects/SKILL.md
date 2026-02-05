---
name: quart-patterns
description: Comprehensive guide to common Quart async patterns including app factory, blueprints, async sessions, background tasks, error handling, and WebSocket patterns. Activates when implementing Quart features or refactoring code.
allowed-tools: Read, Write
---

You are a Quart patterns specialist providing comprehensive guidance on common async web development patterns.

## When to Activate

Activate when you detect:
- Setting up new Quart application
- Implementing async patterns
- Questions about app structure
- Background task implementation
- Error handling setup
- WebSocket pattern questions
- User asks "how do I..." with Quart

## App Factory Pattern

The app factory pattern creates the application instance within a function, enabling multiple configurations:

```python
# src/app/__init__.py
from quart import Quart
from quart_schema import QuartSchema
from quart_cors import cors
from app.database import init_db
from app.config import config

def create_app(config_name='development'):
    """Create and configure Quart application."""
    app = Quart(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    QuartSchema(
        app,
        title=app.config.get('API_TITLE', 'Quart API'),
        version=app.config.get('API_VERSION', '1.0.0')
    )

    # CORS configuration
    app = cors(
        app,
        allow_origin=app.config.get('CORS_ORIGINS', '*'),
        allow_credentials=True,
        allow_headers=['Content-Type', 'Authorization']
    )

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp
    from app.routes.websocket import ws_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(ws_bp)

    # Initialize database
    init_db(app)

    # Global error handlers
    register_error_handlers(app)

    # Lifecycle hooks
    register_lifecycle_hooks(app)

    return app

def register_error_handlers(app: Quart):
    """Register global error handlers."""
    @app.errorhandler(404)
    async def not_found(error):
        return {'error': 'Not Found', 'message': str(error)}, 404

    @app.errorhandler(500)
    async def internal_error(error):
        app.logger.error(f'Internal error: {error}')
        return {'error': 'Internal Server Error'}, 500

    @app.errorhandler(ValidationError)
    async def validation_error(error):
        return {
            'error': 'Validation Error',
            'details': error.errors()
        }, 422

def register_lifecycle_hooks(app: Quart):
    """Register application lifecycle hooks."""
    @app.before_serving
    async def startup():
        """Run before server starts."""
        app.logger.info('Application starting up...')
        # Initialize caches, connections, etc.

    @app.after_serving
    async def shutdown():
        """Run after server stops."""
        app.logger.info('Application shutting down...')
        # Cleanup resources

    @app.before_request
    async def before_request():
        """Run before each request."""
        # Add request ID, start timer, etc.
        pass

    @app.after_request
    async def after_request(response):
        """Run after each request."""
        # Add security headers, log response, etc.
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

# Usage
app = create_app()  # Development
app = create_app('production')  # Production
app = create_app('testing')  # Testing
```

## Blueprint Organization

Organize routes by resource domain using blueprints:

```python
# src/app/routes/auth.py
from quart import Blueprint, request, jsonify
from quart_schema import validate_request, validate_response
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.security import verify_password, create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.before_request
async def before_request():
    """Run before each auth route."""
    # Add auth-specific middleware
    pass

@auth_bp.route('/login', methods=['POST'])
@validate_request(LoginRequest)
@validate_response(TokenResponse)
async def login(data: LoginRequest):
    """User login endpoint."""
    # Implementation
    pass

# src/app/routes/api.py
from quart import Blueprint
from quart_jwt_extended import jwt_required

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/users', methods=['GET'])
@jwt_required
async def list_users():
    """List all users."""
    pass

# src/app/routes/websocket.py
from quart import Blueprint, websocket

ws_bp = Blueprint('websocket', __name__, url_prefix='/ws')

@ws_bp.websocket('/chat')
async def chat():
    """WebSocket chat endpoint."""
    pass
```

## Async Session Management

Proper async database session lifecycle:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager

# Create engine (do this once at startup)
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

# Create session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session():
    """Context manager for database sessions."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Usage in routes
@app.route('/users/<int:user_id>')
async def get_user(user_id: int):
    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            return {'error': 'Not found'}, 404
        return user.to_dict()

# NEVER do this (session sharing):
# session = get_session()  # Created once
# @app.route('/users')
# async def users():
#     users = await session.execute(select(User))  # Race conditions!
```

## Background Task Patterns

Execute long-running tasks without blocking responses:

```python
import asyncio

# Method 1: Quart's add_background_task
@app.route('/send-email', methods=['POST'])
async def send_email():
    data = await request.get_json()

    async def send_email_task():
        await asyncio.sleep(2)  # Simulate sending
        # Send email logic
        pass

    app.add_background_task(send_email_task)

    return {'message': 'Email queued'}, 202

# Method 2: asyncio.create_task for fire-and-forget
@app.route('/process-data', methods=['POST'])
async def process_data():
    data = await request.get_json()

    async def process_task():
        try:
            # Long-running processing
            result = await expensive_operation(data)
            await save_result(result)
        except Exception as e:
            app.logger.error(f'Background task failed: {e}')

    asyncio.create_task(process_task())

    return {'message': 'Processing started'}, 202

# Method 3: Task queue (for production)
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def send_email_celery(email_data):
    # Celery task (runs in separate process)
    pass

@app.route('/send-email-celery', methods=['POST'])
async def send_email_endpoint():
    data = await request.get_json()
    send_email_celery.delay(data)
    return {'message': 'Email queued'}, 202
```

## Error Handling Patterns

Comprehensive error handling strategies:

```python
# Custom exceptions
class APIException(Exception):
    """Base API exception."""
    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class NotFoundException(APIException):
    """Resource not found."""
    def __init__(self, resource: str, resource_id: any):
        super().__init__(
            f'{resource} not found',
            404,
            {'resource': resource, 'id': resource_id}
        )

class UnauthorizedException(APIException):
    """Unauthorized access."""
    def __init__(self, message: str = 'Unauthorized'):
        super().__init__(message, 401)

class ValidationException(APIException):
    """Validation failed."""
    def __init__(self, errors: dict):
        super().__init__('Validation failed', 422, errors)

# Error handlers
@app.errorhandler(APIException)
async def handle_api_exception(error):
    return {
        'error': error.__class__.__name__,
        'message': error.message,
        'details': error.details
    }, error.status_code

@app.errorhandler(Exception)
async def handle_unexpected_error(error):
    app.logger.exception('Unexpected error occurred')
    return {
        'error': 'InternalServerError',
        'message': 'An unexpected error occurred'
    }, 500

# Usage in routes
@app.route('/users/<int:user_id>')
async def get_user(user_id: int):
    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            raise NotFoundException('User', user_id)
        return user.to_dict()

# With context manager for cleanup
from contextlib import asynccontextmanager

@asynccontextmanager
async def error_boundary(operation_name: str):
    """Context manager for error handling."""
    try:
        yield
    except APIException:
        raise  # Re-raise API exceptions
    except Exception as e:
        app.logger.exception(f'{operation_name} failed')
        raise APIException('Operation failed', 500)

# Usage
@app.route('/complex-operation')
async def complex_operation():
    async with error_boundary('complex_operation'):
        result = await do_something_complex()
        return result
```

## WebSocket Patterns

Common WebSocket implementation patterns:

```python
import asyncio
from collections import defaultdict

# Pattern 1: Simple echo
@app.websocket('/ws/echo')
async def echo():
    try:
        while True:
            message = await websocket.receive()
            await websocket.send(f'Echo: {message}')
    except asyncio.CancelledError:
        pass

# Pattern 2: Authenticated WebSocket
from app.auth import verify_jwt_token

@app.websocket('/ws/chat')
async def authenticated_chat():
    # Authenticate first
    token = request.args.get('token')
    if not token:
        await websocket.close(1008, 'Auth required')
        return

    try:
        payload = verify_jwt_token(token)
        user_id = payload['user_id']
    except Exception:
        await websocket.close(1008, 'Invalid token')
        return

    # Now safe to process messages
    try:
        while True:
            message = await websocket.receive()
            await process_user_message(user_id, message)
    except asyncio.CancelledError:
        pass

# Pattern 3: Broadcasting
connected_clients = set()

@app.websocket('/ws/broadcast')
async def broadcast():
    ws = websocket._get_current_object()
    connected_clients.add(ws)

    try:
        while True:
            message = await websocket.receive()

            # Broadcast to all
            for client in list(connected_clients):
                try:
                    await client.send(message)
                except:
                    connected_clients.discard(client)
    except asyncio.CancelledError:
        pass
    finally:
        connected_clients.discard(ws)

# Pattern 4: Pub/Sub with topics
subscriptions = defaultdict(set)

@app.websocket('/ws/pubsub')
async def pubsub():
    ws = websocket._get_current_object()
    user_topics = set()

    try:
        while True:
            data = await websocket.receive()
            message = json.loads(data)

            if message['type'] == 'subscribe':
                topic = message['topic']
                subscriptions[topic].add(ws)
                user_topics.add(topic)

            elif message['type'] == 'publish':
                topic = message['topic']
                for client in subscriptions[topic]:
                    try:
                        await client.send(json.dumps(message))
                    except:
                        subscriptions[topic].discard(client)
    except asyncio.CancelledError:
        pass
    finally:
        for topic in user_topics:
            subscriptions[topic].discard(ws)
```

## Request Validation Patterns

Using quart-schema for validation:

```python
from dataclasses import dataclass
from typing import Optional
from quart_schema import validate_request, validate_response

@dataclass
class CreateUserRequest:
    """Request schema for creating user."""
    username: str
    email: str
    password: str
    bio: Optional[str] = None

@dataclass
class UserResponse:
    """Response schema for user."""
    id: int
    username: str
    email: str
    bio: Optional[str]
    created_at: str

@app.route('/users', methods=['POST'])
@validate_request(CreateUserRequest)
@validate_response(UserResponse, 201)
async def create_user(data: CreateUserRequest):
    """Create new user with validation."""
    # data is validated CreateUserRequest instance
    async with get_session() as session:
        user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password),
            bio=data.bio
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        bio=user.bio,
        created_at=user.created_at.isoformat()
    ), 201
```

## Configuration Pattern

Environment-based configuration:

```python
# src/app/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Base configuration."""
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-change-me')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-me')
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql+asyncpg://localhost/quart_db')
    QUART_ENV: str = os.getenv('QUART_ENV', 'development')

    # API settings
    API_TITLE: str = 'Quart API'
    API_VERSION: str = '1.0.0'

    # CORS
    CORS_ORIGINS: str = os.getenv('CORS_ORIGINS', '*')

@dataclass
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG: bool = True
    TESTING: bool = False

@dataclass
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG: bool = False
    TESTING: bool = False

    def __post_init__(self):
        # Validate production settings
        if self.SECRET_KEY == 'dev-secret-change-me':
            raise ValueError('SECRET_KEY must be set in production')
        if self.CORS_ORIGINS == '*':
            raise ValueError('CORS_ORIGINS must be explicit in production')

@dataclass
class TestingConfig(Config):
    """Testing configuration."""
    TESTING: bool = True
    DATABASE_URL: str = 'postgresql+asyncpg://localhost/quart_test'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
```

## Testing Patterns

Async testing with pytest-asyncio:

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from app import create_app

@pytest.fixture(name='app')
def _app():
    app = create_app('testing')
    return app

@pytest_asyncio.fixture(name='client')
async def _client(app):
    return app.test_client()

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post('/users', json={
        'username': 'test',
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 201
    data = await response.get_json()
    assert data['username'] == 'test'
```

Use these patterns as templates for implementing Quart features!
