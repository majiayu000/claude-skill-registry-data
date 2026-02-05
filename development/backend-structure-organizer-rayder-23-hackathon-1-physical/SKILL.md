---
name: backend-structure-organizer
description: Organizes a flat backend directory structure into a clean, modular architecture with proper Python packages and updated import paths. Transforms a flat backend structure into a modular, organized architecture following Python best practices.
license: Complete terms in LICENSE.txt
---

# Backend Structure Organizer

Organizes a flat backend directory structure into a clean, modular architecture with proper Python packages and updated import paths.

## When to Use This Skill

This skill should be used when:
- Backend files are organized in a flat structure and need to be organized into logical modules
- Python backend code requires refactoring to follow package best practices
- Import statements need to be updated to reflect a new directory structure
- Documentation needs to be updated to reflect a new backend organization

## Prerequisites

- Backend directory exists with Python files in flat structure
- Project uses Python with import statements that may need updating
- Git repository is initialized (for tracking changes)

## Process Overview

### Phase 1: Analysis and Setup
1. Scan backend directory to identify all Python files
2. Identify current structure and file locations
3. Generate report of files to be moved and updated
4. Create new organized directory structure:
   - `agents/` - AI/ML agents and processing
   - `auth/` - Authentication modules
   - `chatkit/` - Chatkit integration components
   - `data/` - Data handling and storage utilities
   - `database/` - Database operations and management
   - `models/` - Database models and schema definitions
   - `services/` - Business logic and service layer
   - `utils/` - Utility functions and helpers
   - `scripts/` - Utility scripts
   - `tests/` - Test files

### Phase 2: File Movement
1. Move files to appropriate directories based on their purpose:
   - Agent-related files → `agents/`
   - Authentication files → `auth/`
   - Data processing files → `data/`
   - Database files → `database/`
   - Model files → `models/`
   - Service files → `services/`
   - Utility files → `utils/`
   - Scripts → `scripts/`
   - Tests → `tests/`

### Phase 3: Import Updates
1. Update import statements in all affected Python files to reflect new locations
2. Handle both absolute and relative import patterns
3. Verify all imports resolve correctly after updates

### Phase 4: Package Setup
1. Create `__init__.py` files in each new directory
2. Ensure proper Python package structure
3. Verify import resolution throughout codebase

### Phase 5: Documentation Update
1. Update README.md to include structure documentation
2. Update requirements.txt if needed
3. Update any configuration files referencing old paths

## Common Import Pattern Updates

### Main Application File (main.py) updates:
- `from database import` → `from database.database import`
- `from models import` → `from models.models import`
- `from agent import` → `from agents.agent import`
- `from vector_store import` → `from data.vector_store import`
- `from rate_limiting import` → `from utils.rate_limiting import`
- `from session_service import` → `from services.session_service import`

### Chatkit Components updates:
- `from models import` → `from models.models import`
- `from session_service import` → `from services.session_service import`
- `from agent import` → `from agents.agent import`
- `from vector_store import` → `from data.vector_store import`
- `from embeddings import` → `from data.embeddings import`

### Data Processing Files updates:
- `from database import` → `from database.database import`
- `from models import` → `from models.models import`
- `from vector_store import` → `from data.vector_store import`
- `from embeddings import` → `from data.embeddings import`

## Success Criteria

- All files organized into logical directories
- All import statements updated and resolving correctly
- `__init__.py` files created in each directory
- Application functionality preserved
- Structure documented in README.md

## Validation Steps

1. Verify all imports resolve without errors
2. Run application to ensure functionality preserved
3. Check that new directory structure is logical and maintainable
4. Confirm documentation reflects new structure

## Rollback Plan

If issues occur:
1. Restore from git backup before changes
2. Revert file movements
3. Revert import statement changes
4. Remove newly created directories