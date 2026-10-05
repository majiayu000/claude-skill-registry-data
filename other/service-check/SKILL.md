---
name: service-check
description: Search for existing services before creating new infrastructure. Prevents duplicate services. TRIGGER when the user says "create a service", "new service", "add a service class", "build a service for", or discusses creating any new service, manager, or helper class in the Services/ directory.
argument-hint: <functionality description>
---

# Service Duplicate Prevention Check

**Desired functionality**: $ARGUMENTS

Before creating ANY new service, verify it doesn't already exist.

## Step 1: Search Existing Services

Search `Services/` directory for related functionality:

### Core Services
- `HouseholdService` — Household management, CloudKit sharing, member invitations
- `RecipeService` — Recipe CRUD
- `WeeklyListService` — Grocery list CRUD
- `MealPlanService` — Meal plan operations
- `IngredientTemplateService` — Template management, normalization, deduplication
- `IngredientParsingService` — PUBLIC API for ingredient parsing (3-tier hybrid)
- `RecipeImportService` — Recipe import orchestrator
- `OptimizedRecipeDataService` — Recipe queries
- `CloudKitSyncMonitor` — Real-time sync tracking
- `UserPreferencesService` — Settings

### Utility Services
- `RecipeScalingService` — 0.25x-4x scaling
- `QuantityMergeService` — Intelligent quantity consolidation
- `UnitConversionService` — cups/tbsp/tsp, lbs/oz
- `GroceryMergeService` — Duplicate grocery consolidation
- `IngredientAutocompleteService` — Search suggestions
- `ParsingTelemetryService` — Telemetry collection
- `KeychainHelper` — Secure storage
- `DuplicateDetectionService` — Import duplicate avoidance

### Import Services
- `RecipeJSONLDExtractor` — JSON-LD schema parsing
- `WKWebViewExtractor` — WKWebView DOM scraping
- `ImageOCRService` — Vision framework OCR
- `OCRLineClassifier` — Line classification
- `FoundationModelsExtractor` — LLM-based extraction

## Step 2: Can an Existing Service Be Extended?

For each potentially related service found, assess:
- Does it already handle the desired functionality?
- Can a new method be added to it?
- Would extending it violate single responsibility?

## Step 3: Report

```markdown
## Service Check: [Functionality]

### Existing Related Services
- [Service name]: [relevance to desired functionality]

### Recommendation
- [ ] **Extend existing service** — [which one, what to add]
- [ ] **Create new service** — [justification for why existing services can't cover it]

### If Creating New Service
Follow the service layer pattern in `docs/architecture/service-layer-pattern.md`:
- @MainActor class with @Published errorMessage and isLoading
- Intent-style methods with error handling
- Single context.save() per operation
```
