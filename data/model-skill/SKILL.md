---
name: model-skill
description: Create Pydantic v2 data models with validation, type hints, and proper configuration. Use when designing data structures or schemas.
allowed-tools: Write, Read
---

# Model Skill

## Purpose
Design robust Pydantic v2 data models with full validation and type safety.

## Instructions

### Basic Model Structure
```python
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class Priority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TodoStatus(str, Enum):
    """Task status values."""
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class RecurrenceType(str, Enum):
    """Task recurrence options."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
```

### Full Model Example
```python
class TodoTask(BaseModel):
    """A todo task with full validation."""
    
    id: int = Field(default=0, description="Unique task identifier")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list)
    status: TodoStatus = Field(default=TodoStatus.PENDING)
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    recurrence: RecurrenceType = Field(default=RecurrenceType.NONE)
    
    @field_validator('title')
    @classmethod
    def strip_title(cls, v: str) -> str:
        """Strip whitespace from title."""
        return v.strip()
    
    @field_validator('tags')
    @classmethod
    def normalize_tags(cls, v: List[str]) -> List[str]:
        """Normalize tags to lowercase."""
        return [tag.lower().strip() for tag in v if tag.strip()]
    
    @model_validator(mode='after')
    def check_overdue(self) -> 'TodoTask':
        """Auto-set overdue status if past due date."""
        if (self.due_date and 
            self.due_date < datetime.now() and 
            self.status == TodoStatus.PENDING):
            self.status = TodoStatus.OVERDUE
        return self
    
    model_config = {
        "use_enum_values": True,
        "validate_assignment": True,
        "json_encoders": {datetime: lambda v: v.isoformat()},
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries",
                "priority": "medium",
                "tags": ["shopping"]
            }
        }
    }
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return self.model_dump(mode='json')
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TodoTask':
        """Create from dictionary."""
        return cls.model_validate(data)
```

## Validation Patterns

### Custom Field Validators
```python
@field_validator('email')
@classmethod
def validate_email(cls, v: str) -> str:
    if '@' not in v:
        raise ValueError('Invalid email format')
    return v.lower()
```

### Cross-field Validation
```python
@model_validator(mode='after')
def validate_dates(self) -> 'Model':
    if self.end_date and self.start_date > self.end_date:
        raise ValueError('end_date must be after start_date')
    return self
```

## Best Practices

- Always use type hints
- Provide descriptions for all fields
- Use Enums for constrained choices
- Add validators for data integrity
- Include examples in schema
- Use `model_dump()` for serialization
- Use `model_validate()` for deserialization
