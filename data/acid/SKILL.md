---
name: acid
description: ACID database properties
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: databases
---

## What I do
- Explain ACID transaction properties
- Implement atomic operations
- Ensure data consistency
- Handle isolation levels

## When to use me
When working with database transactions.

## ACID Properties

### Atomicity
```python
class AtomicTransaction:
    """Implement atomic transactions"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.operations = []
    
    def add_operation(self, operation: Callable):
        self.operations.append(operation)
    
    def execute(self) -> bool:
        """Execute all operations atomically"""
        try:
            self.db.begin()
            
            for op in self.operations:
                op()
            
            self.db.commit()
            return True
        
        except Exception as e:
            self.db.rollback()
            raise e
```

### Consistency
```python
class ConsistencyValidator:
    """Ensure database consistency"""
    
    def __init__(self):
        self.constraints = []
    
    def add_constraint(self, constraint: dict):
        self.constraints.append(constraint)
    
    def validate(self, data: dict) -> bool:
        """Validate data against constraints"""
        for constraint in self.constraints:
            if not self._check_constraint(data, constraint):
                return False
        return True
    
    def _check_constraint(self, data: dict, 
                         constraint: dict) -> bool:
        if constraint["type"] == "unique":
            return self._check_unique(data, constraint)
        elif constraint["type"] == "check":
            return self._check_expression(data, constraint)
```

### Isolation
```python
class IsolationLevel:
    """Transaction isolation levels"""
    
    READ_UNCOMMITTED = "read_uncommitted"
    READ_COMMITTED = "read_committed"
    REPEATABLE_READ = "repeatable_read"
    SERIALIZABLE = "serializable"


class TransactionManager:
    """Manage transaction isolation"""
    
    def __init__(self):
        self.isolation_level = IsolationLevel.READ_COMMITTED
    
    def begin_transaction(self, level: str = None):
        """Begin transaction with isolation level"""
        level = level or self.isolation_level
        
        if level == IsolationLevel.SERIALIZABLE:
            return SerializableTransaction()
        elif level == IsolationLevel.REPEATABLE_READ:
            return RepeatableReadTransaction()
```

### Durability
```python
class DurableStorage:
    """Ensure durability"""
    
    def write(self, data: dict):
        """Write with durability guarantee"""
        # Write to WAL
        self.wal.write(data)
        
        # Sync to disk
        self.wal.sync()
        
        # Write to main storage
        self.storage.write(data)
        
        # Confirm write
        return {"status": "committed"}
```
