---
name: classify-repo-artifacts
description: Use when distinguishing core modules from support/generated/test/infrastructure code, separating signal from noise, or understanding which parts of a repo actually matter for analysis
---

## Announce at start: "Using codebase-analyzer to classify repo artifacts."

## Overview

Sort every module/file into categories: core, support, generated, test, infrastructure. Essential before deep analysis — don't waste tokens analyzing generated code.

**Prerequisite:** Reads `docs/analysis/provenance.md` and `docs/analysis/architecture.md`.

## Process

1. Load provenance map (which files are source vs derived)
2. Tag each top-level directory/module with category
3. Core: business logic, domain models, API handlers, data access
4. Support: utilities, helpers, shared libraries, middleware
5. Generated: build output, codegen, protobuf, graphql generated
6. Test: test files, fixtures, mocks, test utilities
7. Infrastructure: CI/CD, Docker, deployment scripts, config
8. Calculate signal-to-noise ratio: core / total

## Classification Heuristics

| Category | Indicators |
|----------|-----------|
| Core | Business logic, domain types, API handlers, data models |
| Support | utils/, helpers/, lib/, shared/, common/ |
| Generated | "DO NOT EDIT", codegen output, dist/ contents |
| Test | *.test.*, *.spec.*, __tests__/, test/, tests/ |
| Infra | Dockerfile, docker-compose, .github/, k8s/, terraform/ |

## Entropy Analysis

### Information Density Entropy

Files with abnormally high information density (many distinct operations per line) are either highly optimized or obfuscated. Files with abnormally low density are scaffolding or generated. This is a signal, not a verdict.

**How to measure:** Count distinct syntactic operations (function calls, assignments, control flow, operators) per line of executable code. Compare against the repository median. Files more than 2 standard deviations from the mean deserve scrutiny.

**High density (>2 sigma):**
- Hand-optimized algorithms, dense data transforms — likely core
- Minified or obfuscated code — likely generated or vendored
- Cryptographic routines, parser combinators — specialized core

**Low density (<2 sigma):**
- Boilerplate-heavy frameworks, config classes — likely support or infra
- Auto-generated CRUD scaffolding — likely generated
- Re-export barrels, type-only files — likely support

### Naming Entropy

Modules with many unique identifiers are business-logic-dense. Modules with repetitive naming (same prefixes everywhere) are boilerplate or generated. The naming pattern reveals the module's nature.

**How to measure:** Extract all identifiers (function names, variable names, type names, constants) from a module. Calculate the ratio of unique identifiers to total identifier tokens. High ratio = high naming entropy. Low ratio = repetitive.

**High naming entropy (many unique names):**
- Domain modules using business vocabulary specific to the project (e.g., `SubscriptionPlan`, `InvoiceTotal`, `PaymentGateway`) — core
- Complex orchestration with distinct step names — core

**Low naming entropy (repetitive names):**
- `UserHandler`, `OrderHandler`, `ProductHandler` — generated CRUD or boilerplate support
- `formatX`, `parseX`, `validateX` repeated patterns — utility support
- Identical structure across files with only entity names changed — codegen

## Identifying Domain Logic (Not Tautology)

Do not classify code as "domain-specific logic" without explaining HOW to identify domain. Domain logic = code that uses business vocabulary from the project's naming, not generic CS terms like "handler", "processor", "manager". A file called `OrderProcessor.java` is not automatically core — it is core only if it encodes business rules about orders that cannot be inferred from the name alone.

**Concrete test:** Remove the project-specific noun from each identifier. If the remaining structure is generic (CRUD, CRUD, validation, serialization), the module is support wearing domain clothing. If the remaining logic encodes rules, workflows, or constraints unique to the project's problem space, it is genuinely core.

Example: `calculateEarlyPaymentDiscount(invoice, paymentDate)` — removing "invoice" and "payment" leaves `calculateEarlyDiscount(...)`, which still encodes a business rule. This is core.
Example: `validateInvoiceFields(invoice)` — removing "invoice" leaves `validateFields(...)`, which is generic. This is support.

## Validation Checkpoint

After classification, verify against provenance:
- Does every "generated" file appear in the provenance map as derived?
- Are any "core" files actually generated but misidentified?
- Cross-reference entropy outliers: do high-density files classified as "core" contain genuine business rules, or are they minified vendored code?
- Do low-naming-entropy files classified as "core" pass the domain logic test above?

## Adversarial Lens

Generated code is a great place to hide things -- nobody reads it. If a module claims to be auto-generated but contains hand-crafted logic, that's suspicious. Check: do the generated files match what the generator would actually produce?

## Red Flags

- Classifying generated code as core (wastes downstream analysis tokens)
- Missing infrastructure-as-code files (Terraform, CloudFormation)
- Not validating classification against provenance map
- Files with high information density but no business vocabulary — likely vendored, not core
- Modules with repetitive naming classified as core without passing the domain logic test

## Output Contract

Write `docs/analysis/artifact-classification.md` using standard contract.
Include: category breakdown, signal-to-noise ratio, files per category, entropy outlier list, validation status.
