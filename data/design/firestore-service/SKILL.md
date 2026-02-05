---
name: firestore-service
description: Guide for creating Firestore services with async operations, transactions, and proper error handling following this project's patterns.
---
# Firestore Service Creation

Use this skill when creating services that interact with Firestore using async operations.

For comprehensive coding guidelines, see `AGENTS.md` in the repository root.

## Service Structure

Create services in `app/services/` with the following structure:

```python
"""
Resource service with async Firestore operations.
"""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from google.cloud import firestore

from app.core.firebase import get_async_firestore_client
from app.exceptions import ResourceAlreadyExistsError, ResourceNotFoundError
from app.middleware import log_audit_event
from app.models.resource import RESOURCE_COLLECTION, Resource, ResourceCreate, ResourceUpdate
# Note: Models are organized in subdirectories:
# - app/models/resource/requests.py (ResourceCreate, ResourceUpdate)
# - app/models/resource/responses.py (Resource, RESOURCE_COLLECTION)

if TYPE_CHECKING:
    from google.cloud.firestore import AsyncClient, AsyncDocumentReference, AsyncTransaction


class ResourceService:
    """
    Service for resource CRUD operations using async Firestore.
    """

    def __init__(self) -> None:
        self.collection_name = RESOURCE_COLLECTION

    def _get_client(self) -> AsyncClient:
        return get_async_firestore_client()
```

## Transactional Operations

Use `@firestore.async_transactional` for atomic operations. Define transaction methods as static:

```python
@staticmethod
@firestore.async_transactional
async def _create_in_transaction(  # pragma: no cover
    transaction: AsyncTransaction,
    doc_ref: AsyncDocumentReference,
    data: dict,
) -> None:
    # Tested via E2E tests with Firebase emulators; unit tests mock this method
    snapshot = await doc_ref.get(transaction=transaction)
    if snapshot.exists:
        raise ResourceAlreadyExistsError("Resource already exists")
    transaction.set(doc_ref, data)
```

## CRUD Operations

### Create

```python
async def create_resource(self, user_id: str, resource_data: ResourceCreate) -> Resource:
    """
    Create a new resource for the given user.
    """
    client = self._get_client()
    doc_ref = client.collection(self.collection_name).document(user_id)

    now = datetime.now(UTC)
    resource_dict = {
        "id": user_id,
        **resource_data.model_dump(),
        "created_at": now,
        "updated_at": now,
    }

    transaction = client.transaction()
    await self._create_in_transaction(transaction, doc_ref, resource_dict)

    log_audit_event("create", user_id, "resource", user_id, "success")

    return Resource(**resource_dict)
```

### Read

```python
async def get_resource(self, user_id: str) -> Resource:
    """
    Get resource by user ID.

    Raises:
        ResourceNotFoundError: If resource does not exist.
    """
    client = self._get_client()
    doc_ref = client.collection(self.collection_name).document(user_id)
    snapshot = await doc_ref.get()

    if not snapshot.exists:
        raise ResourceNotFoundError("Resource not found")

    data = snapshot.to_dict()
    if not data:
        raise ResourceNotFoundError("Resource not found")

    return Resource(**data)
```

### Update

Use transactions to ensure atomicity and return merged data:

```python
@staticmethod
@firestore.async_transactional
async def _update_in_transaction(  # pragma: no cover
    transaction: AsyncTransaction,
    doc_ref: AsyncDocumentReference,
    updates: dict,
) -> dict | None:
    # Tested via E2E tests with Firebase emulators; unit tests mock this method
    snapshot = await doc_ref.get(transaction=transaction)
    if not snapshot.exists:
        return None
    existing_data = snapshot.to_dict() or {}
    transaction.update(doc_ref, updates)
    return {**existing_data, **updates}


async def update_resource(self, user_id: str, resource_data: ResourceUpdate) -> Resource:
    """
    Update an existing resource.

    Raises:
        ResourceNotFoundError: If resource does not exist.
    """
    client = self._get_client()
    doc_ref = client.collection(self.collection_name).document(user_id)

    update_dict = {k: v for k, v in resource_data.model_dump(exclude_unset=True).items() if v is not None}

    if not update_dict:
        return await self.get_resource(user_id)

    update_dict["updated_at"] = datetime.now(UTC)

    transaction = client.transaction()
    merged_data = await self._update_in_transaction(transaction, doc_ref, update_dict)

    if merged_data is None:
        raise ResourceNotFoundError("Resource not found")

    log_audit_event("update", user_id, "resource", user_id, "success")

    return Resource(**merged_data)
```

### Delete

```python
@staticmethod
@firestore.async_transactional
async def _delete_in_transaction(  # pragma: no cover
    transaction: AsyncTransaction,
    doc_ref: AsyncDocumentReference,
) -> dict | None:
    # Tested via E2E tests with Firebase emulators; unit tests mock this method
    snapshot = await doc_ref.get(transaction=transaction)
    if not snapshot.exists:
        return None
    data = snapshot.to_dict()
    transaction.delete(doc_ref)
    return data


async def delete_resource(self, user_id: str) -> Resource:
    """
    Delete a resource by user ID.

    Raises:
        ResourceNotFoundError: If resource does not exist.
    """
    client = self._get_client()
    doc_ref = client.collection(self.collection_name).document(user_id)

    transaction = client.transaction()
    deleted_data = await self._delete_in_transaction(transaction, doc_ref)

    if deleted_data is None:
        raise ResourceNotFoundError("Resource not found")

    log_audit_event("delete", user_id, "resource", user_id, "success")

    return Resource(**deleted_data)
```

## Audit Logging

Use `log_audit_event()` from `app.middleware` for security-relevant operations:

```python
from app.middleware import log_audit_event

# After successful operation
log_audit_event("create", user_id, "resource", resource_id, "success")
log_audit_event("update", user_id, "resource", resource_id, "success")
log_audit_event("delete", user_id, "resource", resource_id, "success", details={"reason": "user_request"})
```

## Dependency Registration

Register the service in `app/dependencies.py`:

```python
from typing import Annotated
from fastapi import Depends
from app.services.resource import ResourceService


def get_resource_service() -> ResourceService:
    """
    Dependency provider for ResourceService.
    """
    return ResourceService()


ResourceServiceDep = Annotated[ResourceService, Depends(get_resource_service)]
```

## Collection Constants

Define collection names in the response model file:

```python
# app/models/resource/responses.py
RESOURCE_COLLECTION = "resources"
```

Import in service:

```python
from app.models.resource import RESOURCE_COLLECTION
```

## Type Hints

Use `TYPE_CHECKING` for Firestore types to avoid import issues:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.cloud.firestore import AsyncClient, AsyncDocumentReference, AsyncTransaction
```

## Testing

Transaction methods are tested via E2E tests with Firebase emulators. Add `# pragma: no cover` comment and explanatory note:

```python
@staticmethod
@firestore.async_transactional
async def _create_in_transaction(  # pragma: no cover
    transaction: AsyncTransaction,
    doc_ref: AsyncDocumentReference,
    data: dict,
) -> None:
    # Tested via E2E tests with Firebase emulators; unit tests mock this method
    ...
```

Unit tests mock the transactional methods or the service itself:

```python
from unittest.mock import AsyncMock

mock_service = AsyncMock(spec=ResourceService)
mock_service.create_resource.return_value = make_resource()
```
