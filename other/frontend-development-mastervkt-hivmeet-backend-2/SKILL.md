---
name: frontend-development
description: 'Develop and modify HIVMeet frontend features in Flutter/Dart with Clean Architecture and BLoC. Use when implementing UI/pages/widgets, state management, API integration, i18n FR/EN, or mobile platform changes (Android/iOS). Includes hypothesis-first file targeting, spec compliance, privacy checks, and non-regression validation.'
argument-hint: 'Describe the frontend task, target module, and expected outcome.'
user-invocable: true
---

# Frontend Development (Flutter/Dart & Mobile)

## Purpose
Deliver production-ready HIVMeet frontend changes with a repeatable workflow that enforces:
- Clean Architecture boundaries
- Exact backend contract compliance
- Mandatory FR/EN internationalization
- Privacy and sensitivity safeguards
- Non-regression checks before completion

This skill is project-scoped and intentionally specific to HIVMeet.

## Use When
- Building or editing pages, widgets, navigation, and state management
- Implementing or fixing Discovery, Auth, Messaging, Profile, or Premium modules
- Integrating backend endpoints in frontend services/repositories
- Updating Android or iOS integration details linked to Flutter features

## Mandatory Workflow

### 1. Understand The Task
- Define the exact requirement or bug
- Define expected output and user-visible behavior
- Define success criteria and acceptance checks

### 2. Hypothesis-First File Targeting
- Do not scan the entire project initially
- Build a short list of likely files first, then validate
- If hypothesis is wrong, run focused search and update the file list

Suggested hypothesis template for Discovery/filter work:
- lib/presentation/pages/discovery/discovery_page.dart
- lib/presentation/pages/discovery/filters_page.dart
- lib/presentation/blocs/discovery/discovery_bloc.dart
- lib/presentation/blocs/discovery/discovery_state.dart
- lib/presentation/blocs/discovery/discovery_event.dart
- lib/domain/entities/profile.dart
- lib/domain/usecases/match/update_filters.dart
- lib/data/repositories/match_repository_impl.dart
- lib/data/models/profile_model.dart
- lib/core/config/constants.dart

### 3. Consult Specifications Before Coding
- Read docs/Plan de Développement Frontend Détaillé - HIVMeet.txt
- For API details, read API_DOCUMENTATION.md first
- Optionally cross-check guides/ENDPOINTS_COMPLETE_DOCUMENTATION.md

### 4. Analyze Dependencies And Impact
- Identify affected layers and dependent modules
- Detect potential breaking changes
- Decide whether backend adaptation is required

### 5. Plan Implementation
- List edits by file and layer
- Define test and validation strategy
- Include rollback-safe ordering for risky changes

### 6. Implement With Architecture Compliance
- Respect layer boundaries:
  - Presentation: UI + events only
  - Domain: entities, repository interfaces, use cases
  - Data: models, data sources, repository implementations
- Never call data layer directly from presentation
- Use repository interfaces from domain

### 7. Enforce i18n, Security, and Domain Sensitivity
- i18n:
  - No hardcoded user-facing text
  - Use intl/ARB keys for FR and EN
- Security:
  - Store tokens with flutter_secure_storage
  - Never log PII (email, token, user id, phone, exact location)
- HIVMeet domain sensitivity:
  - Use respectful, inclusive, non-stigmatizing wording
  - Preserve privacy-centered defaults

### 8. Validate Non-Regression
- Verify primary feature behavior
- Verify related flows impacted by the change
- Run static checks and formatting
- Confirm no new analyzer errors caused by the change

### 9. Completion Output Contract
For each completed task, include:
1. Exact files modified
2. Complete functional code changes
3. Specification compliance confirmation
4. Non-regression validation summary
5. Frontend/backend impact notes
6. Concise summary and next steps

## Architecture Reference
Expected structure:
- lib/core
- lib/data
- lib/domain
- lib/presentation

## Validation Commands
- flutter analyze
- dart format lib/
- flutter build apk --debug
- flutter build apk --release

## Quality Checklist
- Task understood and success criteria defined
- Likely files identified first (hypothesis)
- Relevant specs consulted
- Dependencies and impact analyzed
- i18n FR/EN respected
- Security/privacy constraints respected
- Tests/validation executed
- Response prepared in French

## Notes
- Prefer minimal, targeted changes over broad refactors
- If backend contract gaps are discovered, provide a precise backend change request with endpoint, payloads, status codes, and error shape
