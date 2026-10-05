---
name: component-boundary-identifier
description: Identify natural module and component boundaries for microservice extraction, modularization, or monolith decomposition using coupling analysis, cohesion.
---

# Component Boundary Identifier

Analyze a codebase to identify natural boundaries where modules, services, or components can be cleanly separated. This skill applies coupling analysis, cohesion measurement, dependency graph construction, bounded context identification from Domain-Driven Design, and the strangler fig pattern to guide systematic modularization or microservice extraction.

## When to Use This Skill

Use this skill when you need to:

- Decompose a monolith into microservices or modular components
- Identify which parts of a codebase should be extracted into separate packages or libraries
- Reduce coupling between modules to improve maintainability
- Plan a migration from monolithic to service-oriented architecture
- Identify bounded contexts in a domain model for DDD implementation
- Evaluate whether a proposed module boundary is clean or will create excessive cross-cutting concerns
- Analyze a codebase before a large-scale refactoring effort
- Apply the strangler fig pattern to incrementally migrate functionality

**Trigger phrases**: "find module boundaries", "component boundaries", "service extraction", "decompose monolith", "coupling analysis", "cohesion analysis", "bounded context", "strangler fig", "modularization", "microservice boundaries"

## What This Skill Does

### Core Capabilities

- **Coupling Analysis**: Measure how tightly connected different parts of the codebase are
- **Cohesion Measurement**: Evaluate how well each module's internal components belong together
- **Dependency Graph Construction**: Build and visualize the dependency relationships between modules
- **Bounded Context Identification**: Apply DDD principles to find natural domain boundaries
- **Change Coupling Detection**: Identify files that always change together (indicating hidden coupling)
- **Data Flow Analysis**: Trace how data flows between components to find natural seams
- **Strangler Fig Planning**: Design an incremental extraction strategy for identified boundaries

### Boundary Quality Indicators

| Indicator | Good Boundary | Poor Boundary |
|-----------|---------------|---------------|
| Coupling | Few, well-defined interfaces | Many cross-boundary calls |
| Cohesion | Related functionality grouped | Unrelated concerns mixed |
| Data ownership | Each module owns its data | Shared mutable state |
| Change frequency | Modules change independently | Changes cascade across modules |
| Team alignment | One team owns one module | Multiple teams edit same module |
| API surface | Narrow, stable interface | Wide, frequently changing interface |

## Instructions

### Phase 1: Build the Dependency Graph

**Step 1.1: Extract import/dependency relationships**

JavaScript/TypeScript:

```bash
# Generate dependency graph using madge
npx madge --json src/ > dependency-graph.json

# Visualize as a dot graph
npx madge --image dependency-graph.svg src/

# Find circular dependencies (strong coupling indicator)
npx madge --circular src/
```

Python:

```bash
# Using pydeps for dependency visualization
pip install pydeps
pydeps src/mypackage --max-bacon=4 --cluster -o deps.svg

# Using import-linter for architecture enforcement
pip install import-linter
# Configure in setup.cfg or pyproject.toml
```

Java:

```bash
# Using jdeps for module dependencies
jdeps --multi-release 17 -summary target/app.jar

# Using Structure101 or ArchUnit for architecture analysis
# ArchUnit test example is shown below
```

Go:

```bash
# Module dependency graph
go mod graph

# Package-level import analysis
go list -m -json all
```

**Step 1.2: Parse and structure the dependency data**

```python
import json
from collections import defaultdict
from dataclasses import dataclass, field

@dataclass
class Module:
    name: str
    files: list[str] = field(default_factory=list)
    imports_from: set[str] = field(default_factory=set)    # Modules this depends on
    imported_by: set[str] = field(default_factory=set)      # Modules that depend on this

def build_module_graph(dependency_json: dict, module_prefix_depth: int = 2) -> dict[str, Module]:
    """Build a module-level dependency graph from file-level dependencies."""
    modules: dict[str, Module] = defaultdict(lambda: Module(name=""))

    for file_path, dependencies in dependency_json.items():
        # Derive module name from directory structure
        # e.g., "src/services/user/handler.ts" -> "services/user"
        parts = file_path.split("/")
        module_name = "/".join(parts[1:module_prefix_depth + 1])

        if module_name not in modules:
            modules[module_name] = Module(name=module_name)
        modules[module_name].files.append(file_path)

        for dep in dependencies:
            dep_parts = dep.split("/")
            dep_module = "/".join(dep_parts[1:module_prefix_depth + 1])

            if dep_module != module_name:  # Ignore intra-module dependencies
                modules[module_name].imports_from.add(dep_module)
                if dep_module not in modules:
                    modules[dep_module] = Module(name=dep_module)
                modules[dep_module].imported_by.add(module_name)

    return dict(modules)
```

### Phase 2: Measure Coupling

**Step 2.1: Calculate afferent and efferent coupling**

```python
def calculate_coupling_metrics(modules: dict[str, Module]) -> list[dict]:
    """Calculate coupling metrics for each module."""
    results = []

    for name, module in modules.items():
        ca = len(module.imported_by)   # Afferent coupling (incoming dependencies)
        ce = len(module.imports_from)  # Efferent coupling (outgoing dependencies)

        # Instability: Ce / (Ca + Ce)
        # 0 = maximally stable (many dependents, no dependencies)
        # 1 = maximally unstable (no dependents, many dependencies)
        instability = ce / (ca + ce) if (ca + ce) > 0 else 0

        results.append({
            "module": name,
            "afferent_coupling": ca,
            "efferent_coupling": ce,
            "instability": round(instability, 2),
            "total_coupling": ca + ce,
            "imports_from": sorted(module.imports_from),
            "imported_by": sorted(module.imported_by),
        })

    return sorted(results, key=lambda x: x["total_coupling"], reverse=True)
```

**Step 2.2: Detect change coupling from version control**

Files that frequently change together indicate hidden coupling, even if there are no direct import dependencies:

```bash
# Find files that frequently change together in the last 6 months
git log --since="6 months ago" --name-only --pretty=format: | \
  sort | uniq -c | sort -rn | head -50

# Find pairs of files that change in the same commit
git log --since="6 months ago" --name-only --pretty=format:"---" | \
  python3 -c "
import sys
from collections import Counter
from itertools import combinations

commits = []
current = []
for line in sys.stdin:
    line = line.strip()
    if line == '---':
        if current:
            commits.append(current)
        current = []
    elif line:
        current.append(line)
if current:
    commits.append(current)

pairs = Counter()
for commit_files in commits:
    for a, b in combinations(sorted(set(commit_files)), 2):
        pairs[(a, b)] += 1

for (a, b), count in pairs.most_common(30):
    if count >= 3:
        print(f'{count:4d}  {a}  <->  {b}')
"
```

**Step 2.3: Identify coupling hotspots**

```python
def identify_coupling_hotspots(modules: list[dict], threshold: int = 5) -> list[dict]:
    """Identify modules with excessive coupling that are candidates for boundary review."""
    hotspots = []

    for module in modules:
        issues = []
        if module["total_coupling"] > threshold:
            issues.append(f"High total coupling ({module['total_coupling']})")
        if module["efferent_coupling"] > threshold:
            issues.append(f"Depends on too many modules ({module['efferent_coupling']})")
        if module["afferent_coupling"] > threshold:
            issues.append(f"Too many modules depend on this ({module['afferent_coupling']})")

        if issues:
            hotspots.append({
                "module": module["module"],
                "issues": issues,
                "recommendation": (
                    "Split into smaller modules" if module["efferent_coupling"] > threshold
                    else "Extract stable interface" if module["afferent_coupling"] > threshold
                    else "Review boundary placement"
                ),
            })

    return hotspots
```

### Phase 3: Measure Cohesion

**Step 3.1: Assess functional cohesion**

A cohesive module has files that work together toward a single purpose:

```python
def assess_cohesion(module_name: str, files: list[str], dependencies: dict) -> dict:
    """Assess the cohesion of a module by analyzing internal connectivity."""
    internal_connections = 0
    possible_connections = 0

    for file_a in files:
        for file_b in files:
            if file_a != file_b:
                possible_connections += 1
                # Check if file_a imports file_b
                if file_b in dependencies.get(file_a, []):
                    internal_connections += 1

    # LCOM (Lack of Cohesion in Methods) adapted for modules
    # 0 = fully connected (high cohesion)
    # 1 = no internal connections (low cohesion)
    if possible_connections == 0:
        cohesion_score = 1.0
    else:
        cohesion_score = internal_connections / possible_connections

    return {
        "module": module_name,
        "file_count": len(files),
        "internal_connections": internal_connections,
        "possible_connections": possible_connections,
        "cohesion_score": round(cohesion_score, 2),
        "assessment": (
            "HIGH" if cohesion_score > 0.5
            else "MEDIUM" if cohesion_score > 0.2
            else "LOW"
        ),
    }
```

**Step 3.2: Identify mixed concerns**

```python
def detect_mixed_concerns(module_name: str, files: list[str]) -> list[str]:
    """Detect files in a module that may belong to different concerns."""
    concern_patterns = {
        "api": ["controller", "handler", "route", "endpoint"],
        "data": ["repository", "dao", "model", "entity", "schema"],
        "business": ["service", "usecase", "domain", "logic"],
        "infrastructure": ["adapter", "client", "provider", "connector"],
        "presentation": ["view", "component", "template", "page"],
        "configuration": ["config", "settings", "constants"],
        "utility": ["util", "helper", "common", "shared"],
    }

    file_concerns = {}
    for file_path in files:
        filename = file_path.lower().split("/")[-1]
        for concern, keywords in concern_patterns.items():
            if any(kw in filename for kw in keywords):
                file_concerns[file_path] = concern
                break
        else:
            file_concerns[file_path] = "unknown"

    concerns_found = set(file_concerns.values()) - {"unknown"}

    if len(concerns_found) > 2:
        return [
            f"Module '{module_name}' contains {len(concerns_found)} different concerns: {', '.join(sorted(concerns_found))}",
            "Consider splitting into separate modules by concern",
        ]
    return []
```

### Phase 4: Identify Bounded Contexts

Apply Domain-Driven Design principles to find natural domain boundaries.

**Step 4.1: Map domain concepts to code**

```yaml
# Domain concept inventory
domain_concepts:
  user_management:
    entities: [User, Role, Permission, Session]
    operations: [register, authenticate, authorize, updateProfile]
    data_stores: [users_table, roles_table, sessions_table]
    code_modules: [src/services/user, src/services/auth, src/models/user]

  order_processing:
    entities: [Order, OrderItem, Invoice, Payment]
    operations: [createOrder, processPayment, generateInvoice, shipOrder]
    data_stores: [orders_table, payments_table, invoices_table]
    code_modules: [src/services/order, src/services/payment, src/models/order]

  product_catalog:
    entities: [Product, Category, Price, Inventory]
    operations: [listProducts, searchProducts, updateInventory, setPrice]
    data_stores: [products_table, categories_table, inventory_table]
    code_modules: [src/services/product, src/services/inventory, src/models/product]
```

**Step 4.2: Identify context boundaries**

```python
def identify_bounded_contexts(domain_concepts: dict, module_graph: dict) -> list[dict]:
    """Identify bounded contexts based on domain concept clustering."""
    contexts = []

    for context_name, concept in domain_concepts.items():
        # Analyze cross-context dependencies
        external_deps = set()
        for module in concept["code_modules"]:
            if module in module_graph:
                for dep in module_graph[module].imports_from:
                    # Check if dependency belongs to a different context
                    dep_context = find_context_for_module(dep, domain_concepts)
                    if dep_context and dep_context != context_name:
                        external_deps.add((dep_context, dep))

        contexts.append({
            "name": context_name,
            "entities": concept["entities"],
            "modules": concept["code_modules"],
            "external_dependencies": [
                {"context": ctx, "module": mod} for ctx, mod in external_deps
            ],
            "boundary_quality": (
                "CLEAN" if len(external_deps) <= 2
                else "ACCEPTABLE" if len(external_deps) <= 5
                else "TANGLED"
            ),
        })

    return contexts
```

**Step 4.3: Identify shared kernel and anti-corruption layers**

```markdown
## Context Map

```
+-------------------+       +---------------------+
| User Management   |       | Order Processing    |
|                   |  ACL  |                     |
| - User            |<----->| - Customer (value)  |
| - Authentication  |       | - Order             |
| - Authorization   |       | - Payment           |
+-------------------+       +---------------------+
         |                           |
         | Shared Kernel             | ACL
         |                           |
+-------------------+       +---------------------+
| Shared Identity   |       | Product Catalog     |
| - UserId          |       | - Product           |
| - TenantId        |       | - Inventory         |
+-------------------+       +---------------------+
```

### Anti-Corruption Layer Example
The Order Processing context references users, but should not depend
on the full User Management model. Instead, it maintains a lightweight
Customer value object and an ACL that translates between the two.
```

### Phase 5: Design the Extraction Strategy

**Step 5.1: Rank candidates for extraction**

```python
def rank_extraction_candidates(
    modules: list[dict],
    cohesion_scores: list[dict],
    contexts: list[dict],
) -> list[dict]:
    """Rank modules by their suitability for extraction."""
    candidates = []

    for context in contexts:
        # Score based on multiple factors
        score = 0

        # High cohesion = good candidate
        avg_cohesion = sum(
            c["cohesion_score"] for c in cohesion_scores
            if c["module"] in context["modules"]
        ) / max(len(context["modules"]), 1)
        score += avg_cohesion * 30

        # Low external coupling = good candidate
        ext_dep_count = len(context["external_dependencies"])
        score += max(0, 30 - ext_dep_count * 5)

        # Clear domain alignment = good candidate
        if context["boundary_quality"] == "CLEAN":
            score += 40
        elif context["boundary_quality"] == "ACCEPTABLE":
            score += 20

        candidates.append({
            "context": context["name"],
            "modules": context["modules"],
            "extraction_score": round(score, 1),
            "effort_estimate": (
                "LOW" if ext_dep_count <= 2
                else "MEDIUM" if ext_dep_count <= 5
                else "HIGH"
            ),
            "prerequisites": [
                f"Decouple from {dep['context']} ({dep['module']})"
                for dep in context["external_dependencies"]
            ],
        })

    return sorted(candidates, key=lambda x: x["extraction_score"], reverse=True)
```

**Step 5.2: Plan the strangler fig migration**

The strangler fig pattern incrementally replaces functionality in the monolith with new service implementations:

```yaml
# Strangler fig migration plan
migration_phases:
  - phase: 1
    name: "Extract Product Catalog"
    extraction_score: 85
    effort: LOW
    steps:
      - "Define the API contract for the Product service"
      - "Create the new Product service with its own database"
      - "Implement the anti-corruption layer in the monolith"
      - "Route product read traffic to the new service"
      - "Migrate product write operations"
      - "Remove product code from the monolith"
      - "Verify with integration tests"

  - phase: 2
    name: "Extract Order Processing"
    extraction_score: 65
    effort: MEDIUM
    steps:
      - "Define event contracts for order lifecycle"
      - "Implement event bus for order-related events"
      - "Create Order service with event-driven communication"
      - "Implement saga pattern for distributed transactions"
      - "Route order traffic through the API gateway"
      - "Migrate order data to the new service database"
      - "Remove order code from the monolith"
```

**Step 5.3: Define the interface between components**

```typescript
// Define a clean interface at the boundary
// This interface becomes the contract between the monolith and the extracted service

// product-service/src/api/product.interface.ts
export interface ProductService {
  getProduct(id: string): Promise<Product>;
  listProducts(filters: ProductFilters): Promise<PaginatedResult<Product>>;
  searchProducts(query: string): Promise<Product[]>;
  updateInventory(productId: string, delta: number): Promise<void>;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: Money;
  inventory: number;
  category: string;
}

export interface ProductFilters {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  inStock?: boolean;
  page?: number;
  pageSize?: number;
}
```

### Phase 6: Validate Boundaries with Architecture Tests

**Step 6.1: ArchUnit tests (Java)**

```java
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

public class BoundaryArchitectureTest {

    @Test
    void orderModuleShouldNotDependOnUserInternals() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..order..")
            .should().dependOnClassesThat()
            .resideInAPackage("..user.internal..");

        rule.check(new ClassFileImporter().importPackages("com.example"));
    }

    @Test
    void modulesShouldOnlyCommunicateThroughInterfaces() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..service.impl..")
            .should().beAccessedByClassesThat()
            .resideOutsideOfPackage("..service..");

        rule.check(new ClassFileImporter().importPackages("com.example"));
    }
}
```

**Step 6.2: import-linter rules (Python)**

```ini
# setup.cfg or .importlinter
[importlinter]
root_package = myapp

[importlinter:contract:1]
name = Order module cannot import user internals
type = forbidden
source_modules =
    myapp.order
forbidden_modules =
    myapp.user.models
    myapp.user.repositories

[importlinter:contract:2]
name = Independence of bounded contexts
type = independence
modules =
    myapp.product
    myapp.order
    myapp.user
```

**Step 6.3: ESLint boundaries (TypeScript)**

```json
{
  "plugins": ["boundaries"],
  "settings": {
    "boundaries/elements": [
      { "type": "user", "pattern": "src/modules/user/**" },
      { "type": "order", "pattern": "src/modules/order/**" },
      { "type": "product", "pattern": "src/modules/product/**" },
      { "type": "shared", "pattern": "src/shared/**" }
    ],
    "boundaries/ignore": ["**/*.test.ts"]
  },
  "rules": {
    "boundaries/element-types": [2, {
      "default": "disallow",
      "rules": [
        { "from": "order", "allow": ["shared"] },
        { "from": "user", "allow": ["shared"] },
        { "from": "product", "allow": ["shared"] }
      ]
    }]
  }
}
```

## Best Practices

- Start with dependency graph analysis before making any boundary decisions; let the data guide the design, not assumptions
- Prefer high cohesion within a boundary over low coupling between boundaries; a module that does one thing well is easier to extract than one with scattered responsibilities
- Use change coupling (co-change analysis from version control) as a complement to static dependency analysis; files that change together often belong together
- Define the interface at the boundary before extracting the implementation; a well-defined API contract makes extraction reversible
- Apply the strangler fig pattern for incremental extraction rather than big-bang rewrites; migrate one boundary at a time
- Validate boundaries with automated architecture tests (ArchUnit, import-linter, ESLint boundaries) to prevent boundary violations from creeping back in
- Align component boundaries with team boundaries (Conway's Law); a boundary that crosses team ownership creates coordination overhead
- Keep shared kernels minimal; every shared component is a coupling point that constrains independent evolution
- Plan for data ownership at the boundary level; a service that shares a database with another service is not truly independent
- Revisit boundaries periodically as the domain evolves; boundaries that were correct six months ago may need adjustment as requirements change

## Common Pitfalls

- **Drawing boundaries too early**: Extracting services before the domain is well understood leads to wrong boundaries that are expensive to fix. Let the monolith grow until natural seams emerge.
- **Ignoring data coupling**: Two modules may have no code dependencies but share a database table. This hidden coupling makes extraction impossible without data migration.
- **Creating too many small services**: Over-decomposition creates distributed monolith problems (network latency, distributed transactions, deployment complexity). Start with a few coarse-grained services.
- **Extracting shared utilities first**: Shared libraries (logging, validation, HTTP clients) seem like easy extraction targets, but they create coupling in the opposite direction. Extract domain modules first.
- **Ignoring cross-cutting concerns**: Authentication, logging, and monitoring span all boundaries. Plan how these concerns will work in a distributed context before extracting services.
- **Breaking transactional boundaries without a plan**: If two operations that currently run in the same database transaction are split across services, you need a saga or eventual consistency pattern. Plan this before extraction.
- **Not measuring before and after**: Without baseline metrics (coupling scores, deployment frequency, lead time), you cannot demonstrate that the extraction improved anything.
- **Copying the monolith structure into services**: If you extract a "service" that mirrors the monolith's internal layering (controller, service, repository), you may have just created a smaller monolith. Design each service around its domain model.
- **Ignoring the human factor**: Boundary decisions are also organizational decisions. A boundary that places related functionality in different teams will create handoff friction.
- **Treating extraction as a one-time project**: Boundaries need ongoing maintenance. Without architecture tests and regular review, coupling will gradually increase across boundaries.
