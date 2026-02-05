---
name: fhir-migration
description: Migration du stockage Patient/Practitioner vers HAPI FHIR. Utiliser quand l'utilisateur demande d'implémenter l'architecture hybride FHIR, créer des mappers FHIR, ou intégrer avec HAPI FHIR.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(poetry:*), Bash(git:*)
---

# Migration HAPI FHIR - core-africare-identity

Ce skill guide la migration du service core-africare-identity vers une architecture hybride avec HAPI FHIR comme source de vérité pour les données démographiques.

## Architecture Cible

```
Client → API (Pydantic) → Service Layer → HAPI FHIR (Patient/Practitioner)
                               ↓
                      PostgreSQL (métadonnées GDPR)
```

- **HAPI FHIR**: Source de vérité pour données démographiques (Patient, Practitioner)
- **PostgreSQL**: Métadonnées GDPR locales (soft_deleted_at, correlation_hash, etc.)
- **Keycloak**: Authentification et gestion des utilisateurs

## Composants à Implémenter

### 1. Infrastructure FHIR

| Fichier | Description |
|---------|-------------|
| `app/infrastructure/fhir/__init__.py` | Exports du module |
| `app/infrastructure/fhir/client.py` | Client HTTP async pour HAPI FHIR |
| `app/infrastructure/fhir/config.py` | Configuration FHIR (URL, timeout) |
| `app/infrastructure/fhir/identifiers.py` | Systèmes d'identifiants FHIR |
| `app/infrastructure/fhir/exceptions.py` | Exceptions FHIR typées |

Voir [CLIENT-SETUP.md](CLIENT-SETUP.md) pour les détails d'implémentation.

### 2. Mappers Pydantic ↔ FHIR

| Fichier | Description |
|---------|-------------|
| `app/infrastructure/fhir/mappers/__init__.py` | Exports des mappers |
| `app/infrastructure/fhir/mappers/patient_mapper.py` | PatientCreate ↔ FHIR Patient |
| `app/infrastructure/fhir/mappers/professional_mapper.py` | ProfessionalCreate ↔ FHIR Practitioner |

Voir [MAPPERS.md](MAPPERS.md) pour les templates de mappers.

### 3. Modèles GDPR Locaux

| Fichier | Description |
|---------|-------------|
| `app/models/gdpr_metadata.py` | PatientGdprMetadata, ProfessionalGdprMetadata |

Voir [GDPR-MODELS.md](GDPR-MODELS.md) pour les modèles SQLAlchemy.

### 4. Service Layer Orchestration

Modifier les services existants pour orchestrer HAPI FHIR + PostgreSQL.

Voir [SERVICE-LAYER.md](SERVICE-LAYER.md) pour le pattern d'orchestration.

## Workflow de Migration

### Phase 1: Infrastructure (Prérequis)

```bash
# 1. Ajouter dépendances
poetry add "fhir.resources>=7.0.0" "httpx>=0.27.0"

# 2. Créer structure répertoires
mkdir -p app/infrastructure/fhir/mappers
touch app/infrastructure/fhir/__init__.py
touch app/infrastructure/fhir/mappers/__init__.py
```

### Phase 2: Client FHIR

1. Créer `app/infrastructure/fhir/config.py` - Configuration
2. Créer `app/infrastructure/fhir/identifiers.py` - Systèmes d'identifiants
3. Créer `app/infrastructure/fhir/exceptions.py` - Exceptions
4. Créer `app/infrastructure/fhir/client.py` - Client HTTP async

### Phase 3: Mappers

1. Créer `app/infrastructure/fhir/mappers/patient_mapper.py`
2. Créer `app/infrastructure/fhir/mappers/professional_mapper.py`
3. Ajouter tests dans `tests/unit/test_fhir_mappers.py`

### Phase 4: Modèles GDPR

1. Créer `app/models/gdpr_metadata.py` avec PatientGdprMetadata
2. Créer migration Alembic: `make migrate MESSAGE="Add GDPR metadata tables"`
3. Appliquer migration: `make migrate-up`

### Phase 5: Orchestration Services

1. Modifier `app/services/patient_service.py` pour utiliser FHIR + PostgreSQL
2. Modifier `app/services/professional_service.py`
3. Mettre à jour les endpoints API

### Phase 6: Suppression Legacy

1. Marquer tables `patients`/`professionals` comme deprecated
2. Créer migration de suppression
3. Nettoyer les imports

## Variables d'Environnement

```bash
# HAPI FHIR
HAPI_FHIR_BASE_URL=http://localhost:8090/fhir
HAPI_FHIR_TIMEOUT=30

# Optionnel: Auth FHIR
HAPI_FHIR_AUTH_TOKEN=
```

## Tests

```bash
# Tests unitaires mappers
poetry run pytest tests/unit/test_fhir_mappers.py -v

# Tests intégration FHIR (nécessite HAPI FHIR local)
make test-services-up
poetry run pytest tests/integration/test_fhir_client.py -v
make test-services-down
```

## Ressources

- [Client Setup](CLIENT-SETUP.md) - Configuration client FHIR
- [Mappers](MAPPERS.md) - Templates de mappers Pydantic ↔ FHIR
- [GDPR Models](GDPR-MODELS.md) - Modèles SQLAlchemy pour métadonnées
- [Service Layer](SERVICE-LAYER.md) - Pattern d'orchestration
- [FHIR R4 Spec](https://hl7.org/fhir/R4/) - Spécification FHIR

## Checklist Migration

- [ ] Dépendances installées (fhir.resources, httpx)
- [ ] Client FHIR créé et testé
- [ ] Mappers Patient et Professional créés
- [ ] Modèles GDPR créés avec migration
- [ ] Services refactorisés pour orchestration
- [ ] Tests unitaires et intégration passent
- [ ] Tables legacy supprimées
- [ ] Documentation mise à jour
