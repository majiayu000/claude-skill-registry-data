---
name: python-expert
description: 'Python expert for writing clean, well-structured, and idiomatic code. Use for: code organization, PEP 8 compliance, type hints, design patterns, best practices, refactoring, testing, and modern Python features. Covers async/await, decorators, context managers, and pythonic idioms.'
argument-hint: 'Describe the Python task (e.g., write clean function, refactor code, add type hints)'
---

# Python Expert

Expert guidance for writing clean, maintainable, and idiomatic Python code following best practices and modern Python standards.

## When to Use

- Writing new Python functions, classes, or modules
- Refactoring existing code for better structure
- Applying design patterns and best practices
- Adding type hints and documentation
- Improving code readability and maintainability
- Implementing error handling and logging
- Writing tests and test fixtures
- Using async/await and concurrent programming
- Optimizing Python code performance

## Core Principles

### 1. Code Structure and Organization

**Module Organization:**
```python
"""
Module docstring describing purpose and usage.

This module handles user authentication and session management.
"""

# Standard library imports
import os
import sys
from datetime import datetime
from typing import Optional, List, Dict

# Third-party imports
import requests
from sqlalchemy import create_engine

# Local application imports
from .models import User
from .exceptions import AuthenticationError

# Constants
MAX_LOGIN_ATTEMPTS = 3
SESSION_TIMEOUT = 3600

# Module-level code
logger = logging.getLogger(__name__)
```

**Class Structure:**
```python
class UserManager:
    """Manage user operations with clean, single-responsibility methods.
    
    Attributes:
        db_connection: Database connection instance
        cache: Optional cache for user data
    """
    
    def __init__(self, db_connection, cache=None):
        """Initialize the UserManager.
        
        Args:
            db_connection: Active database connection
            cache: Optional cache instance for performance
        """
        self.db_connection = db_connection
        self.cache = cache
        self._session = None
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID with caching support."""
        if self.cache:
            cached_user = self.cache.get(f"user:{user_id}")
            if cached_user:
                return cached_user
        
        user = self.db_connection.query(User).filter_by(id=user_id).first()
        
        if user and self.cache:
            self.cache.set(f"user:{user_id}", user, timeout=300)
        
        return user
    
    def __repr__(self):
        return f"UserManager(cache={'enabled' if self.cache else 'disabled'})"
```

### 2. Type Hints and Annotations

Use type hints for better code clarity and IDE support:

```python
from typing import List, Dict, Optional, Union, Tuple, Callable, TypeVar, Generic

# Function signatures
def process_data(
    items: List[str],
    threshold: int = 10,
    callback: Optional[Callable[[str], None]] = None
) -> Dict[str, int]:
    """Process items and return frequency count."""
    result: Dict[str, int] = {}
    
    for item in items:
        result[item] = result.get(item, 0) + 1
        if callback:
            callback(item)
    
    return result

# Complex types
UserData = Dict[str, Union[str, int, List[str]]]

def get_user_data(user_id: int) -> Optional[UserData]:
    """Fetch user data with structured typing."""
    pass

# Generic types
T = TypeVar('T')

class Repository(Generic[T]):
    """Generic repository pattern."""
    
    def find_by_id(self, id: int) -> Optional[T]:
        """Find entity by ID."""
        pass
    
    def save(self, entity: T) -> T:
        """Save entity to repository."""
        pass
```

### 3. Python Idioms and Best Practices

**List Comprehensions:**
```python
# Good - clear and efficient
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Dictionary comprehensions
word_lengths = {word: len(word) for word in words}

# Set comprehensions
unique_lengths = {len(word) for word in words}
```

**Context Managers:**
```python
# File handling
with open('data.txt', 'r') as f:
    data = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def database_transaction(connection):
    """Ensure transaction is committed or rolled back."""
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    
# Usage
with database_transaction(db_conn) as conn:
    conn.execute("INSERT INTO users VALUES (...)")
```

**Generators for Memory Efficiency:**
```python
def read_large_file(file_path: str):
    """Read large file line by line without loading into memory."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

def fibonacci(n: int):
    """Generate Fibonacci sequence up to n terms."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Usage
for num in fibonacci(10):
    print(num)
```

**Unpacking and Multiple Assignment:**
```python
# Tuple unpacking
first, *middle, last = [1, 2, 3, 4, 5]

# Dictionary unpacking
defaults = {'timeout': 30, 'retries': 3}
config = {'timeout': 60, 'endpoint': '/api'}
final_config = {**defaults, **config}

# Function arguments
def process(name, age, city='Unknown'):
    pass

user_data = {'name': 'Alice', 'age': 30, 'city': 'NYC'}
process(**user_data)
```

### 4. Error Handling

**Specific Exception Handling:**
```python
def safe_divide(a: float, b: float) -> Optional[float]:
    """Safely divide two numbers with proper error handling."""
    try:
        result = a / b
    except ZeroDivisionError:
        logger.error(f"Cannot divide {a} by zero")
        return None
    except TypeError as e:
        logger.error(f"Invalid types for division: {e}")
        raise
    else:
        return result
    finally:
        logger.debug("Division operation completed")

# Custom exceptions
class ValidationError(Exception):
    """Raised when data validation fails."""
    pass

class DataNotFoundError(Exception):
    """Raised when requested data doesn't exist."""
    
    def __init__(self, entity_type: str, entity_id: int):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with ID {entity_id} not found")

# Usage
def get_user(user_id: int) -> User:
    user = db.query(User).get(user_id)
    if not user:
        raise DataNotFoundError("User", user_id)
    return user
```

### 5. Decorators and Higher-Order Functions

**Common Decorator Patterns:**
```python
from functools import wraps
import time

def timer(func):
    """Measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

def validate_types(**type_hints):
    """Validate function argument types."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Bind arguments to parameter names
            bound = inspect.signature(func).bind(*args, **kwargs)
            bound.apply_defaults()
            
            for param_name, expected_type in type_hints.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{param_name} must be {expected_type.__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@timer
@retry(max_attempts=3, delay=2.0)
def fetch_data(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### 6. Data Classes and Named Tuples

**Modern Data Structures:**
```python
from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class User:
    """User data structure with automatic methods."""
    id: int
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate data after initialization."""
        if '@' not in self.email:
            raise ValueError(f"Invalid email: {self.email}")

# Frozen dataclass (immutable)
@dataclass(frozen=True)
class Point:
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

# Named tuples for simple structures
from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])
location = Coordinate(40.7128, -74.0060)
```

### 7. Async/Await for Concurrent Operations

**Asynchronous Programming:**
```python
import asyncio
from typing import List

async def fetch_url(session, url: str) -> str:
    """Fetch single URL asynchronously."""
    async with session.get(url) as response:
        return await response.text()

async def fetch_all_urls(urls: List[str]) -> List[str]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def process_with_timeout(coro, timeout: float):
    """Execute coroutine with timeout."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        logger.error(f"Operation timed out after {timeout}s")
        return None

# Async context manager
class AsyncDatabaseConnection:
    async def __aenter__(self):
        self.conn = await get_connection()
        return self.conn
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()
```

### 8. Clean Code Practices

**SOLID Principles:**

**Single Responsibility:**
```python
# Bad - multiple responsibilities
class UserManager:
    def get_user(self, user_id): pass
    def save_user(self, user): pass
    def send_email(self, user, message): pass
    def log_activity(self, action): pass

# Good - focused responsibility
class UserRepository:
    def get(self, user_id): pass
    def save(self, user): pass

class EmailService:
    def send(self, recipient, message): pass

class ActivityLogger:
    def log(self, action): pass
```

**Dependency Injection:**
```python
# Good - dependencies injected
class OrderProcessor:
    def __init__(
        self,
        payment_gateway,
        inventory_service,
        notification_service
    ):
        self.payment = payment_gateway
        self.inventory = inventory_service
        self.notifications = notification_service
    
    def process_order(self, order):
        self.payment.charge(order.total)
        self.inventory.reserve(order.items)
        self.notifications.send_confirmation(order.customer)
```

**Small, Focused Functions:**
```python
def process_user_registration(data: Dict) -> User:
    """Process new user registration with clear steps."""
    validated_data = validate_registration_data(data)
    user = create_user_account(validated_data)
    send_welcome_email(user)
    log_registration_event(user)
    return user

def validate_registration_data(data: Dict) -> Dict:
    """Validate and sanitize registration data."""
    if not data.get('email'):
        raise ValidationError("Email is required")
    
    if len(data.get('password', '')) < 8:
        raise ValidationError("Password must be at least 8 characters")
    
    return {
        'email': data['email'].lower().strip(),
        'username': data['username'].strip(),
        'password': hash_password(data['password'])
    }
```

### 9. Testing Best Practices

**Unit Tests with pytest:**
```python
import pytest
from unittest.mock import Mock, patch

class TestUserManager:
    @pytest.fixture
    def mock_db(self):
        """Provide mock database connection."""
        return Mock()
    
    @pytest.fixture
    def user_manager(self, mock_db):
        """Provide UserManager instance with mock db."""
        return UserManager(mock_db)
    
    def test_get_user_success(self, user_manager, mock_db):
        """Test successful user retrieval."""
        # Arrange
        expected_user = User(id=1, name="Alice")
        mock_db.query.return_value.filter_by.return_value.first.return_value = expected_user
        
        # Act
        result = user_manager.get_user(1)
        
        # Assert
        assert result == expected_user
        mock_db.query.assert_called_once()
    
    def test_get_user_not_found(self, user_manager, mock_db):
        """Test user not found scenario."""
        mock_db.query.return_value.filter_by.return_value.first.return_value = None
        
        result = user_manager.get_user(999)
        
        assert result is None
    
    @pytest.mark.parametrize("user_id,expected", [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Charlie"),
    ])
    def test_multiple_users(self, user_manager, user_id, expected):
        """Test multiple user scenarios."""
        pass
```

### 10. Documentation Standards

**Comprehensive Docstrings:**
```python
def calculate_discount(
    price: float,
    discount_percent: float,
    min_price: float = 0.0
) -> float:
    """Calculate final price after applying discount.
    
    Applies a percentage discount to the given price, ensuring
    the final price doesn't fall below the minimum threshold.
    
    Args:
        price: Original price of the item
        discount_percent: Discount percentage (0-100)
        min_price: Minimum allowed price after discount (default: 0.0)
    
    Returns:
        Final price after discount, not less than min_price
    
    Raises:
        ValueError: If discount_percent is not between 0 and 100
        ValueError: If price is negative
    
    Examples:
        >>> calculate_discount(100.0, 20.0)
        80.0
        
        >>> calculate_discount(50.0, 50.0, min_price=30.0)
        30.0
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    if price < 0:
        raise ValueError("Price cannot be negative")
    
    discounted_price = price * (1 - discount_percent / 100)
    return max(discounted_price, min_price)
```

## Code Organization Patterns

### Project Structure
```
project/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── requirements.txt
├── setup.py
└── README.md
```

### Configuration Management
```python
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class Config:
    """Application configuration."""
    database_url: str
    api_key: str
    debug: bool = False
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables."""
        return cls(
            database_url=os.getenv("DATABASE_URL", "sqlite:///app.db"),
            api_key=os.getenv("API_KEY", ""),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )
```

## Performance Optimization

**Efficient Data Processing:**
```python
# Use generators for large datasets
def process_large_file(file_path: str):
    with open(file_path) as f:
        for line in f:
            yield process_line(line)

# Use sets for membership testing
valid_ids = {1, 2, 3, 4, 5}  # O(1) lookup
if user_id in valid_ids:
    pass

# Cache expensive computations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(n: int) -> int:
    """Cached computation for repeated calls."""
    return sum(i**2 for i in range(n))

# Use list comprehensions over loops
# Good
squares = [x**2 for x in range(1000)]

# Less efficient
squares = []
for x in range(1000):
    squares.append(x**2)
```

## Output Guidelines

When providing Python solutions:

1. **Follow PEP 8** - Consistent formatting, naming conventions, line length
2. **Use type hints** - Clear function signatures with return types
3. **Write docstrings** - Explain purpose, parameters, returns, and exceptions
4. **Handle errors gracefully** - Specific exceptions with meaningful messages
5. **Keep functions small** - Single responsibility, easy to test
6. **Use Python idioms** - List comprehensions, context managers, generators
7. **Consider performance** - Efficient data structures and algorithms
8. **Write testable code** - Dependency injection, mocked external dependencies
9. **Document assumptions** - Comments for complex logic or business rules
10. **Provide examples** - Show usage patterns when helpful

## Common Anti-Patterns to Avoid

- **Mutable default arguments**: `def func(items=[]):` → Use `items=None`
- **Bare except clauses**: `except:` → Use specific exceptions
- **String concatenation in loops**: Use `join()` or f-strings
- **Not using `with` for resources**: Always use context managers for files/connections
- **Overusing classes**: Not everything needs to be a class - functions are fine
- **God objects**: Classes that do too much - split responsibilities
- **Magic numbers**: Use named constants instead of hardcoded values

## Modern Python Features

**Pattern Matching (Python 3.10+):**
```python
def handle_response(response):
    match response.status:
        case 200:
            return response.json()
        case 404:
            raise NotFoundError()
        case 500 | 502 | 503:
            raise ServerError()
        case _:
            raise UnexpectedError(response.status)
```

**Walrus Operator (Python 3.8+):**
```python
# Assign and use in one expression
if (n := len(data)) > 10:
    print(f"Processing {n} items")

# In list comprehensions
filtered = [y for x in data if (y := transform(x)) is not None]
```

**Type Unions (Python 3.10+):**
```python
def process(value: int | str | None) -> str:
    """Process various input types."""
    pass
```
