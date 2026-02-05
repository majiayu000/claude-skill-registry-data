---
name: rag-cag-security
description: Security patterns for RAG and CAG systems with multi-tenant isolation. Use when building retrieval-augmented or cache-augmented generation systems that require tenant isolation, access control, and secure data handling.
---

# RAG/CAG Security Skill

This skill provides security patterns for RAG and CAG systems.

## Multi-Tenant Architecture

### Tenant Isolation Strategies

1. **Namespace Isolation** - Separate vector namespaces per tenant
2. **Metadata Filtering** - Filter by tenant_id at query time
3. **Separate Collections** - Isolated collections per tenant

```python
# Metadata filtering approach
results = vector_store.similarity_search(
    query,
    filter={"tenant_id": current_user.tenant_id}
)
```

## Access Control

### Document-Level Permissions
```python
@dataclass
class Document:
    id: str
    content: str
    tenant_id: str
    access_groups: list[str]
    classification: str  # public, internal, confidential

def can_access(user: User, doc: Document) -> bool:
    return (
        user.tenant_id == doc.tenant_id
        and any(g in doc.access_groups for g in user.groups)
        and user.clearance >= doc.classification
    )
```

## Prompt Injection Prevention

```python
def sanitize_retrieved_context(chunks: list[str]) -> str:
    """Sanitize retrieved chunks before including in prompt."""
    sanitized = []
    for chunk in chunks:
        # Remove potential instruction patterns
        cleaned = remove_instruction_patterns(chunk)
        # Escape special characters
        escaped = escape_prompt_chars(cleaned)
        sanitized.append(escaped)
    return "\n".join(sanitized)
```

## Data Classification

| Level | Description | Handling |
|-------|-------------|----------|
| Public | Open information | No restrictions |
| Internal | Company-only | Tenant isolation |
| Confidential | Sensitive | Encryption + audit |
| Restricted | Highly sensitive | Need-to-know basis |

## Security Checklist

- [ ] Tenant isolation implemented
- [ ] Document-level access control
- [ ] Retrieved content sanitized
- [ ] Audit logging enabled
- [ ] Data encryption at rest
- [ ] Secure API authentication
