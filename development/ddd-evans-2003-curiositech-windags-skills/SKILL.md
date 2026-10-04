---
license: Apache-2.0
name: ddd-evans-2003
description: Domain-Driven Design methodology using bounded contexts, ubiquitous language, and strategic/tactical patterns
category: Research & Academic
tags:
  - domain-driven-design
  - ddd
  - software-architecture
  - bounded-contexts
  - ubiquitous-language
---

# Domain-Driven Design (Eric Evans)

Strategic and tactical patterns for building software systems that remain aligned with business reality as complexity grows.

## Decision Points

### Language & Naming Conflicts
```
Is the same word used differently across teams/systems?
├── Yes → Explicit Bounded Context boundary needed
│   ├── Teams can coordinate? → Shared Kernel or Customer/Supplier
│   └── Teams independent? → Anti-Corruption Layer
└── No → Can use single Ubiquitous Language
    ├── Code names ≠ domain expert names? → Rename code to match domain
    └── Names match → Continue with current language
```

### Object Identity & Boundaries
```
Does the business care which specific instance this is?
├── Yes → Entity
│   ├── Multiple entities modified together for consistency? → Same Aggregate
│   └── Independent lifecycle? → Separate Aggregates  
└── No → Value Object
    ├── Immutable attributes only? → Pure Value Object
    └── Contains behavior? → Value Object with methods
```

### Strategic Investment
```
Is this subdomain where we create competitive advantage?
├── Yes → Core Domain
│   ├── Complex business rules? → Deep modeling with tactical patterns
│   └── Simple CRUD? → May not be truly Core
└── No → Generic/Supporting Subdomain
    ├── Commodity problem? → Buy or use off-shelf solution
    └── Organization-specific? → Minimal custom solution
```

## Failure Modes

### **Anemic Domain Model**
- **Symptom:** Business logic lives in service classes; domain objects are property bags with getters/setters
- **Diagnosis:** Conflating domain objects with data transfer objects; OOP structure without OOP behavior
- **Fix:** Move business rules into domain objects; make services coordinate entities, not contain business logic

### **Translation Tunnel**
- **Symptom:** Same concept has different names at every layer (database: CUST_REC, ORM: CustomerRecord, domain: Client)
- **Diagnosis:** Each layer "protecting" itself with its own vocabulary instead of using Ubiquitous Language
- **Fix:** Use domain terms consistently from UI to database; eliminate gratuitous translation layers

### **God Aggregate**
- **Symptom:** Aggregates requiring joins across 10+ tables; concurrent modification failures; slow loading
- **Diagnosis:** Conflating "what user sees together" with "what must change together for consistency"
- **Fix:** Split aggregates by true consistency boundaries; use eventual consistency between aggregates

### **Shallow Metaphor Lock-in**
- **Symptom:** Model works for obvious cases but fights every edge case; constant special-case handling
- **Diagnosis:** Surface metaphor captured initial understanding but doesn't reflect how domain actually works
- **Fix:** Look for breakthrough refactoring; the model is missing a core concept that would unlock complexity

### **One Model Delusion**
- **Symptom:** Permanent committee meetings to agree on shared terms; integration constantly breaks; forced compromises
- **Diagnosis:** Attempting single canonical model across contexts with legitimately different needs
- **Fix:** Draw explicit bounded context boundaries; choose integration patterns (ACL, Conformist, etc.)

## Worked Examples

### E-Commerce Context Splitting
**Scenario:** Single "Product" concept causing integration pain between catalog and inventory teams.

**Analysis Walk-through:**
1. **Identify the conflict:** Catalog team needs rich attributes (descriptions, categories, SEO); Inventory team needs quantities, locations, reservations
2. **Map current usage:** Same `Product` class being modified by both teams for different reasons
3. **Decision point:** Is this one concept or two? Business says "it's the same product" but they mean different things
4. **Context boundary:** Catalog Context (ProductDetails) vs Inventory Context (StockItem)
5. **Integration choice:** Customer/Supplier relationship - Inventory subscribes to catalog events for new products

**Expert insight:** Novice focuses on avoiding duplication; expert focuses on model integrity within each context.

### Payment Processing Aggregate Design
**Scenario:** Designing order processing where payment, shipping, and inventory must stay consistent.

**Analysis Walk-through:**
1. **Identity question:** Does business care about specific Order instance? Yes → Entity
2. **Consistency boundary:** Payment + OrderLines must change together (inventory reserved when payment succeeds)
3. **Aggregate scope:** Order (root) + OrderLines + Payment attempt, but NOT inventory records (different lifecycle)
4. **Repository design:** OrderRepository loads entire aggregate; InventoryService handles stock via domain events
5. **Concurrency:** Optimistic locking on Order aggregate; inventory conflicts handled via compensating actions

**Expert insight:** Novice includes everything "related"; expert includes only what needs transactional consistency.

## Quality Gates

- [ ] **Language audit:** Same terms used by domain experts appear in code identically
- [ ] **Context map exists:** Explicit boundaries drawn between models with integration strategies defined
- [ ] **Aggregate boundaries validated:** Each aggregate has single reason to change; no cross-aggregate transactions
- [ ] **Entity/Value classification clear:** Each object's identity semantics match business requirements
- [ ] **Strategic allocation verified:** Core Domain gets deep modeling; Generic Subdomains get minimal custom code
- [ ] **Supple design test:** Adding common new features requires changing <3 classes
- [ ] **Anti-corruption barriers:** External systems don't leak their models into our domain
- [ ] **Repository isolation:** Domain layer has zero infrastructure dependencies
- [ ] **Ubiquitous language consistency:** Technical team can explain features using domain expert vocabulary
- [ ] **Invariants in code:** Business rules enforced by object structure, not developer discipline

## NOT-FOR Boundaries

**Don't use DDD for:**
- Pure technical problems (performance optimization, algorithms, infrastructure)
- Simple CRUD applications without complex business rules
- Systems where domain model is not the primary complexity

**Delegate to other skills:**
- **For data modeling without behavior** → use relational-database-design
- **For API integration patterns** → use api-design-patterns  
- **For event-driven architecture** → use event-sourcing-cqrs
- **For microservice boundaries** → use service-decomposition-patterns
- **For performance optimization** → use system-performance-optimization

**Context boundaries:**
- Apply full DDD tactical patterns only in Core Domain
- Use lightweight approaches for Supporting/Generic subdomains
- Don't force single model across organizational boundaries