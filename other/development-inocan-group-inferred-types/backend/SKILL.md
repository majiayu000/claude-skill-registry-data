---
name: backend
description: FastAPI, SQLModel, async services for Pulse Radar backend development.
---

# Backend Development Skill

## Architecture (Hexagonal)
```
backend/app/
├── api/v1/          # 23 routers (~100 endpoints)
├── models/          # 21 SQLModel entities
├── services/        # 35 services (business logic)
├── tasks/           # TaskIQ workers
└── ws/              # WebSocket endpoint
```

## Layer Pattern
```
Router (API) → Service (logic) → CRUD (data)
     ↓              ↓                ↓
  Validation    Business rules    Database
```

## API Pattern
```python
@router.get("/atoms/{atom_id}")
async def get_atom(
    atom_id: UUID,
    service: AtomService = Depends()
) -> AtomRead:
    return await service.get_by_id(atom_id)
```

## Service Pattern
```python
class AtomService:
    def __init__(self, crud: AtomCRUD = Depends()):
        self.crud = crud

    async def get_by_id(self, atom_id: UUID) -> AtomRead:
        atom = await self.crud.get(atom_id)
        if not atom:
            raise HTTPException(404, "Atom not found")
        return AtomRead.model_validate(atom)
```

## Key Models
- **Message**: content, embedding (1536), importance_score, noise_classification
- **Topic**: name, icon, color, keywords
- **Atom**: type, title, content, confidence, user_approved
- **LLMProvider**: type (ollama/openai), api_key_encrypted, validation_status

## Key Enums
```python
AnalysisStatus: pending, analyzed, spam, noise
AtomType: problem, solution, decision, question, insight, pattern, requirement
ProviderType: ollama, openai
ValidationStatus: pending, validating, connected, error
```

## Verification
```bash
just typecheck  # mypy strict
just fmt        # ruff format
just test       # pytest suite
```

## References
- @references/models.md — All 21 models with fields
- @references/services.md — All 35 services
- @references/taskiq.md — Background task patterns