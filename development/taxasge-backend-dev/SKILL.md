---
name: TaxasGE Backend Dev
description: Patterns backend FastAPI architecture 3-tiers, complète DEV_AGENT avec best practices backend
version: 2.0.0
---

# TaxasGE Backend Dev Skill

## Overview

Ce skill **complète le DEV_AGENT** avec des patterns spécifiques backend FastAPI. Il ne remplace PAS le workflow de développement mais fournit des références techniques et templates pour l'implémentation backend.

**Principe fondamental** : Guide technique, pas workflow (le workflow est dans DEV_AGENT.md et DEV_WORKFLOW.md).

---

## When to Use This Skill

Claude invoquera automatiquement ce skill quand :
- DEV_AGENT implémente tâche backend
- Besoin patterns FastAPI
- Questions architecture 3-tiers
- Référence technique backend

**Ne PAS utiliser pour** :
- Workflow développement (voir DEV_WORKFLOW.md)
- Validation (voir Go/No-Go Validator)
- Orchestration (voir Orchestrator)

---

## Core Responsibilities

### 1. Architecture 3-Tiers Stricte

**Séparation obligatoire** :
```
Routes (API Layer)        ← Validation input, Response format, RBAC
    ↓
Services (Business Logic) ← Logique métier, Orchestration
    ↓
Repositories (Data)       ← CRUD, Queries SQL, Transactions
```

**Règles absolues** :
- ❌ Jamais de business logic dans routes
- ❌ Jamais de SQL direct dans services
- ❌ Jamais de validation métier dans repositories

### 2. Référence Documentation Backend

**Source unique de vérité** : `.github/docs-internal/Documentations/Backend/`

Structure :
```
.github/docs-internal/Documentations/Backend/
├── API_REFERENCE.md              ← Endpoints documentés
├── ARCHITECTURE.md               ← Architecture globale
├── DATABASE_SCHEMA.md            ← Schéma DB
├── ERROR_HANDLING.md             ← Gestion erreurs RFC 7807
├── AUTHENTICATION.md             ← JWT + RBAC
└── DEPLOYMENT.md                 ← Déploiement Cloud Run
```

**Important** : Toujours référencer cette documentation, ne PAS dupliquer.

### 3. Templates Code

**Templates disponibles** :
- `templates/endpoint_template.py` - Structure route FastAPI
- `templates/service_template.py` - Structure service métier
- `templates/repository_template.py` - Structure repository DB

**Usage** : Copie template → Adapte au use case → Implémente

---

## Patterns Backend

### Pattern 1 : Route FastAPI Standard

**Template** : `templates/endpoint_template.py`

**Structure** :
```python
from fastapi import APIRouter, Depends, HTTPException
from app.services.{module}_service import {Module}Service
from app.core.auth import require_role
from app.schemas.{module} import {Module}Create, {Module}Response

router = APIRouter(prefix="/{module}", tags=["{Module}"])

@router.post("/", response_model={Module}Response, status_code=201)
@require_role("citizen")
async def create_{module}(
    data: {Module}Create,
    service: {Module}Service = Depends()
):
    """
    Créer {module}.
    
    **Source** : .github/docs-internal/Documentations/Backend/API_REFERENCE.md
    
    **Validation** :
    - Pydantic {Module}Create automatique
    - RBAC : Rôle "citizen" requis
    
    **Errors** :
    - 400 : Validation error
    - 401 : Non authentifié
    - 403 : Non autorisé
    """
    return await service.create(data)
```

**Points clés** :
1. **Prefix + Tags** : Organisation Swagger
2. **Response model** : Type-safety sortie
3. **RBAC decorator** : `@require_role()` AVANT handler
4. **Dependency injection** : Service via `Depends()`
5. **Docstring complète** : Source + Validation + Errors

---

### Pattern 2 : Service Métier

**Template** : `templates/service_template.py`

**Structure** :
```python
from app.database.repositories.{module}_repository import {Module}Repository
from app.core.errors import ValidationError, ResourceNotFoundError

class {Module}Service:
    """
    Service {module}.
    
    **Source** : .github/docs-internal/Documentations/Backend/ARCHITECTURE.md
    """
    
    def __init__(self):
        self.repo = {Module}Repository()
    
    async def create(self, data: {Module}Create) -> {Module}:
        """
        Créer {module} avec validations métier.
        
        **Business Rules** :
        1. {Règle métier 1}
        2. {Règle métier 2}
        
        **Source** : .github/docs-internal/Documentations/Backend/API_REFERENCE.md
        """
        # Validations métier
        await self._validate_business_rules(data)
        
        # Créer via repository
        result = await self.repo.create(data)
        
        # Actions post-création (emails, notifications, etc.)
        await self._post_creation_actions(result)
        
        return result
    
    async def _validate_business_rules(self, data: {Module}Create):
        """
        Validations métier spécifiques.
        
        Raises:
            ValidationError: Si validation échoue
        """
        # Exemple : Vérifier unicité
        existing = await self.repo.get_by_field(data.unique_field)
        if existing:
            raise ValidationError(
                field="unique_field",
                message="Already exists",
                value=data.unique_field
            )
    
    async def _post_creation_actions(self, entity):
        """Actions après création (async, non-bloquantes)."""
        # Exemple : Envoyer email confirmation
        pass
```

**Points clés** :
1. **Injection repository** : Dans `__init__`
2. **Business logic SEULEMENT** : Pas de SQL
3. **Méthodes privées** : `_validate_*`, `_post_*`
4. **Exceptions custom** : `ValidationError`, `ResourceNotFoundError`
5. **Docstrings avec source** : Traçabilité

---

### Pattern 3 : Repository DB

**Template** : `templates/repository_template.py`

**Structure** :
```python
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.{module} import {Module}
from app.database.connection import get_db
from app.core.errors import ResourceNotFoundError
from fastapi import Depends

class {Module}Repository:
    """
    Repository {module}.
    
    **Source** : database/schema.sql
    """
    
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def create(self, data: {Module}Create) -> {Module}:
        """
        Créer {module} en DB.
        
        **Source** : database/schema.sql ligne {X}
        """
        entity = {Module}(**data.dict())
        self.db.add(entity)
        await self.db.flush()  # Get ID
        await self.db.refresh(entity)
        return entity
    
    async def get_by_id(self, id: int) -> {Module}:
        """
        Récupérer {module} par ID.
        
        Raises:
            ResourceNotFoundError: Si non trouvé
        """
        query = select({Module}).where({Module}.id == id)
        result = await self.db.execute(query)
        entity = result.scalar_one_or_none()
        
        if not entity:
            raise ResourceNotFoundError(
                resource="{Module}",
                identifier=str(id)
            )
        
        return entity
    
    async def list(
        self, 
        filters: dict = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[{Module}]:
        """
        Lister {module}s avec pagination.
        
        **Source** : .github/docs-internal/Documentations/Backend/API_REFERENCE.md
        """
        query = select({Module})
        
        # Filtres dynamiques
        if filters:
            for key, value in filters.items():
                if hasattr({Module}, key):
                    query = query.where(getattr({Module}, key) == value)
        
        # Pagination
        query = query.limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update(self, id: int, data: {Module}Update) -> {Module}:
        """Mettre à jour {module}."""
        entity = await self.get_by_id(id)
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(entity, key, value)
        
        await self.db.flush()
        await self.db.refresh(entity)
        return entity
    
    async def delete(self, id: int) -> bool:
        """Supprimer {module}."""
        entity = await self.get_by_id(id)
        await self.db.delete(entity)
        return True
```

**Points clés** :
1. **Injection DB session** : Via `Depends(get_db)`
2. **Queries SQL SEULEMENT** : Pas de business logic
3. **Gestion erreurs** : `ResourceNotFoundError` si non trouvé
4. **Pagination** : `limit` + `offset`
5. **Source schema.sql** : Référence ligne exacte

---

## Checklist Implémentation Backend

Avant de considérer tâche backend terminée :

### Code
- [ ] **Architecture 3-tiers** respectée (Routes → Services → Repositories)
- [ ] **Pydantic models** avec validation complète
- [ ] **Error handling** RFC 7807 implémenté
- [ ] **RBAC** configuré (`@require_role`)
- [ ] **Docstrings** complètes avec sources

### Sources (Règle 0)
- [ ] **Schema DB** vérifié (`database/schema.sql`)
- [ ] **Documentation backend** consultée (`.github/docs-internal/Documentations/Backend/`)
- [ ] **Code existant** respecté (patterns cohérents)

### Tests
- [ ] **Tests unitaires** services écrits (>85% coverage)
- [ ] **Tests endpoints** écrits (>85% coverage)
- [ ] **Tests repositories** écrits (>90% coverage)
- [ ] **Tests passent** (100%)

### Qualité
- [ ] **Lint** : 0 erreurs flake8
- [ ] **Type check** : 0 erreurs mypy
- [ ] **Build** : Réussi

### Documentation
- [ ] **Swagger** endpoints documentés
- [ ] **README module** créé/mis à jour

---

## Integration avec DEV_AGENT

### Workflow Complet

```
1. DEV_AGENT reçoit tâche (ex: TASK-P2-007)
   ↓
2. DEV_AGENT lit DEV_WORKFLOW.md (9 étapes)
   ↓
3. DEV_AGENT invoque Backend Dev Skill (ce skill)
   ↓
4. Backend Dev Skill fournit :
   - Patterns 3-tiers
   - Templates code
   - Références documentation
   ↓
5. DEV_AGENT implémente selon patterns
   ↓
6. DEV_AGENT génère rapport (.agent/Reports/PHASE_X/)
   ↓
7. Go/No-Go Validator valide (invoque TEST_AGENT)
```

**Ce skill ne fait PAS** :
- ❌ Workflow développement (c'est DEV_WORKFLOW.md)
- ❌ Git operations (c'est DEV_WORKFLOW.md)
- ❌ Génération rapports (c'est DEV_AGENT)
- ❌ Validation (c'est Go/No-Go Validator)

**Ce skill fait** :
- ✅ Fournit patterns techniques
- ✅ Référence documentation
- ✅ Templates code
- ✅ Best practices backend

---

## References

### Agents & Workflows
- `.claude/.agent/Tasks/DEV_AGENT.md` - Agent développement
- `.claude/.agent/SOP/DEV_WORKFLOW.md` - Workflow 9 étapes
- `.claude/.agent/SOP/CODE_STANDARDS.md` - Standards code
- `.claude/.agent/SOP/TEST_WORKFLOW.md` - Tests

### Documentation Backend
- `.github/docs-internal/Documentations/Backend/API_REFERENCE.md`
- `.github/docs-internal/Documentations/Backend/ARCHITECTURE.md`
- `.github/docs-internal/Documentations/Backend/DATABASE_SCHEMA.md`
- `.github/docs-internal/Documentations/Backend/ERROR_HANDLING.md`
- `.github/docs-internal/Documentations/Backend/AUTHENTICATION.md`

### Templates
- `templates/endpoint_template.py` - Route FastAPI
- `templates/service_template.py` - Service métier
- `templates/repository_template.py` - Repository DB

### Sources (Règle 0)
1. `database/schema.sql` - Schéma DB
2. `packages/backend/.env` - Configuration
3. `.github/docs-internal/Documentations/Backend/` - Documentation
4. `packages/backend/app/` - Code existant

---

## Success Criteria

Une implémentation backend est réussie si :
- ✅ Architecture 3-tiers strictement respectée
- ✅ Pydantic validation complète
- ✅ Error handling RFC 7807
- ✅ RBAC implémenté
- ✅ Tests coverage >85%
- ✅ 0 erreurs lint/type
- ✅ Documentation Swagger complète
- ✅ Sources (Règle 0) vérifiées

---

## Example Usage

**Scenario** : DEV_AGENT implémente TASK-P2-007 (Endpoint création déclaration)

**DEV_AGENT actions** :
1. Lit TASK-P2-007 définition
2. Invoque Backend Dev Skill
3. Backend Dev Skill retourne :
   - Pattern Route (template endpoint)
   - Pattern Service (template service)
   - Pattern Repository (template repository)
   - Référence `.github/docs-internal/Documentations/Backend/API_REFERENCE.md`
4. DEV_AGENT implémente selon patterns :
   - `app/api/v1/declarations.py` (route)
   - `app/services/declaration_service.py` (service)
   - `app/database/repositories/declaration_repository.py` (repository)
5. DEV_AGENT écrit tests (>85% coverage)
6. DEV_AGENT génère rapport

**Backend Dev Skill n'a PAS** :
- ❌ Créé fichiers (c'est DEV_AGENT)
- ❌ Exécuté tests (c'est TEST_AGENT via Go/No-Go)
- ❌ Généré rapport (c'est DEV_AGENT)

**Backend Dev Skill a** :
- ✅ Fourni patterns/templates
- ✅ Référencé documentation
- ✅ Guidé architecture

---

**Skill created by:** TaxasGE Backend Team  
**Date:** 2025-10-31  
**Version:** 2.0.0  
**Status:** ✅ READY FOR USE
