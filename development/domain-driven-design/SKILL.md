---
name: domain-driven-design
description: Apply DDD tactical patterns (Entities, Value Objects, Aggregates, Domain Services, Repositories) and strategic design (Ubiquitous Language, Bounded Contexts). Use when modeling complex business logic.
---

# Domain-Driven Design (DDD) Skill

You are assisting with code that must follow Domain-Driven Design principles.

## Core Concept

**Focus on the Domain**: The heart of software is its domain model - the conceptual model of the problem domain that incorporates both behavior and data. DDD enables developers to translate complex problem domains into rich, expressive, and evolving software.

**When to Use DDD**:
- Complex business requirements that go beyond CRUD operations
- Business logic that cannot be adequately expressed through simple data structures
- Domains where standard architectural patterns feel insufficient
- Systems requiring deep domain understanding and continuous evolution

**When NOT to Use DDD**:
- Simple CRUD applications
- When business logic is minimal
- Projects with tight deadlines and simple requirements
- Team lacks OOP fundamentals and SOLID principles understanding

## Strategic Design

### Ubiquitous Language
The foundation of DDD is discovering and using shared terminology through conversations with domain experts. This common vocabulary ensures code reflects real-world business processes rather than arbitrary technical abstractions.

**Principles**:
- Use the same terms in code as domain experts use
- No translation layer between business and code
- Class names, method names, variables match domain vocabulary
- The language evolves as understanding deepens

**For Norwegian admission system**:
- Use Norwegian domain terms: `Opptakskrav`, `Karakterpoeng`, `Kvote`
- Or agreed English equivalents: `AdmissionRequirement`, `GradePoints`, `Quota`
- Avoid generic terms: `Rule`, `Data`, `Manager`, `Processor`, `Handler`

### Bounded Contexts
Separate domain models into distinct boundaries based on different meanings of the same terms.

**Example for admission system**:
- **Admission Context**: Rules, evaluation, quotas
- **Student Context**: Personal data, grades, applications
- **Reporting Context**: Statistics, analytics, exports

Each context has its own model, even if terms overlap.

### Context Mapping
Define relationships between bounded contexts:
- **Shared Kernel**: Common domain model
- **Customer-Supplier**: One context depends on another
- **Anti-Corruption Layer**: Translate between contexts
- **Published Language**: Standard interchange format

## Tactical Design Patterns

### 1. Entities
Objects defined by identity, not attributes.

**Characteristics**:
- Has unique identifier
- Mutable
- Identity persists through changes
- Lifecycle matters

```python
class Student:
    """Entity: Student identity matters, attributes can change."""
    def __init__(self, student_id: StudentId, name: str):
        self._id = student_id  # Identity
        self._name = name      # Can change
        self._grades: List[Grade] = []

    @property
    def id(self) -> StudentId:
        return self._id

    def add_grade(self, grade: Grade) -> None:
        self._grades.append(grade)
```

### 2. Value Objects
Objects defined by attributes, not identity.

**Characteristics**:
- No unique identifier
- Immutable
- Equality by value comparison
- Can be shared

```python
@dataclass(frozen=True)
class Grade:
    """Value Object: Two grades with same values are identical."""
    subject: str
    score: int

    def __post_init__(self):
        if not 1 <= self.score <= 6:
            raise ValueError("Grade must be between 1 and 6")

@dataclass(frozen=True)
class CompetencePoints:
    """Value Object: Immutable, defined by value."""
    value: Decimal

    def add(self, other: 'CompetencePoints') -> 'CompetencePoints':
        return CompetencePoints(self.value + other.value)
```

### 3. Aggregates
Cluster of entities and value objects with defined boundaries. Aggregates are crucial for maintaining consistency and controlling access to the domain model.

**Rules**:
- One entity is the Aggregate Root (the entry point)
- External objects can only reference the root (never internal entities)
- Root enforces all invariants across the aggregate
- Transaction boundaries align with aggregates
- Keep aggregates as small as possible for performance
- External references point only to roots, preventing external manipulation of internal state

```python
class AdmissionApplication:
    """Aggregate Root: Controls access to internal entities."""
    def __init__(self, application_id: ApplicationId, student: Student):
        self._id = application_id
        self._student = student
        self._program_choices: List[ProgramChoice] = []
        self._status = ApplicationStatus.DRAFT

    def add_program_choice(self, program: Program, priority: int) -> None:
        """Root controls modification of internal entities."""
        if len(self._program_choices) >= 10:
            raise DomainError("Maximum 10 program choices allowed")

        choice = ProgramChoice(program, priority)
        self._program_choices.append(choice)

    def submit(self) -> None:
        """Root enforces invariants."""
        if not self._program_choices:
            raise DomainError("Cannot submit without program choices")
        self._status = ApplicationStatus.SUBMITTED
```

### 4. Domain Services
Stateless operations that handle domain logic which doesn't naturally belong to any single entity or value object. Domain services often orchestrate multiple aggregates.

**Use when**:
- Operation involves multiple domain objects
- Operation is a significant domain concept in itself
- Operation is stateless (no instance variables)
- Forcing the behavior into an entity would feel unnatural

**Avoid when**:
- The behavior naturally belongs to a specific entity
- It would create an anemic domain model by extracting entity behavior

```python
class AdmissionEvaluationService:
    """Domain Service: Evaluates admission across multiple entities."""

    def evaluate_application(
        self,
        application: AdmissionApplication,
        rules: List[AdmissionRule]
    ) -> EvaluationResult:
        """Service coordinates between multiple domain objects."""
        results = []
        for rule in rules:
            result = rule.evaluate(application.student)
            results.append(result)

        return EvaluationResult.from_rule_results(results)
```

### 5. Domain Events
Objects representing significant business occurrences that domain experts care about. Domain events decouple and coordinate complex workflows across subdomains.

**Characteristics**:
- Past tense naming (describes what happened)
- Immutable (events cannot be changed)
- Contains all relevant data for the event
- Timestamped
- Represent facts that have occurred in the domain

**Benefits**:
- Loose coupling between bounded contexts
- Audit trail of domain changes
- Enable event-driven architectures
- Support eventual consistency patterns

```python
@dataclass(frozen=True)
class StudentAdmitted:
    """Domain Event: Something significant happened."""
    student_id: StudentId
    program_id: ProgramId
    admitted_at: datetime
    admission_basis: str

@dataclass(frozen=True)
class QuotaFilled:
    """Domain Event: Quota reached capacity."""
    quota_id: QuotaId
    filled_at: datetime
    capacity: int
```

### 6. Repositories
Data access abstractions that provide the illusion of an in-memory collection of aggregates. Repositories enable persistence ignorance, allowing you to switch storage technologies without affecting domain logic.

**Responsibilities**:
- Add/remove aggregates
- Find aggregates by criteria
- Reconstitute aggregates from storage
- Work exclusively with aggregate roots, not individual entities

**Key Benefits**:
- Domain layer stays independent of infrastructure
- Easier to test with in-memory implementations
- Can swap persistence strategies (SQL, NoSQL, file system) transparently

```python
class AdmissionRuleRepository(Protocol):
    """Repository interface in domain layer."""

    def find_by_program(self, program_id: ProgramId) -> List[AdmissionRule]:
        """Find all rules for a program."""
        ...

    def find_by_id(self, rule_id: RuleId) -> Optional[AdmissionRule]:
        """Find specific rule."""
        ...

    def save(self, rule: AdmissionRule) -> None:
        """Persist rule."""
        ...
```

### 7. Factories
Encapsulate complex object creation.

```python
class AdmissionRuleFactory:
    """Factory: Creates complex admission rules."""

    @staticmethod
    def create_minimum_grade_rule(
        subject: str,
        minimum_grade: int
    ) -> MinimumGradeRule:
        """Create validated rule."""
        if not 1 <= minimum_grade <= 6:
            raise ValueError("Invalid grade")
        return MinimumGradeRule(subject, minimum_grade)

    @staticmethod
    def create_from_config(config: dict) -> AdmissionRule:
        """Create rule from configuration."""
        rule_type = config['type']
        if rule_type == 'minimum_grade':
            return MinimumGradeRule(config['subject'], config['grade'])
        elif rule_type == 'quota':
            return QuotaRule(config['quota_name'], config['capacity'])
        # ... more types
```

## Domain Model Patterns

### Specification Pattern
Encapsulate business rules that can be combined.

```python
class AdmissionSpecification(ABC):
    """Specification: Reusable business rule."""

    @abstractmethod
    def is_satisfied_by(self, student: Student) -> bool:
        pass

    def and_(self, other: 'AdmissionSpecification') -> 'AdmissionSpecification':
        return AndSpecification(self, other)

class MinimumGradeSpecification(AdmissionSpecification):
    def __init__(self, subject: str, minimum: int):
        self._subject = subject
        self._minimum = minimum

    def is_satisfied_by(self, student: Student) -> bool:
        grade = student.get_grade(self._subject)
        return grade is not None and grade.score >= self._minimum
```

### Policy Pattern
Encapsulate complex business rules and decisions.

```python
class QuotaAssignmentPolicy:
    """Policy: Encapsulates quota assignment logic."""

    def assign_quota(
        self,
        student: Student,
        program: Program
    ) -> Optional[Quota]:
        """Determine which quota the student qualifies for."""
        if student.has_special_competence():
            return program.get_quota('special_competence')
        elif student.is_first_time_applicant():
            return program.get_quota('ordinary')
        else:
            return program.get_quota('supplementary')
```

## Protecting Invariants

Business rules that must always be true.

```python
class Quota:
    """Entity with invariant: filled <= capacity."""

    def __init__(self, name: str, capacity: int):
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")
        self._name = name
        self._capacity = capacity
        self._filled = 0

    def fill_spot(self) -> None:
        """Invariant protected: cannot overfill."""
        if self._filled >= self._capacity:
            raise DomainError(f"Quota {self._name} is full")
        self._filled += 1

    @property
    def available_spots(self) -> int:
        """Derived value from invariant."""
        return self._capacity - self._filled
```

## Rich Domain Model vs Anemic Domain Model

A **rich domain model** encapsulates business rules and logic within cohesive objects, protecting business concerns from infrastructure details. An **anemic domain model** separates data from behavior, resulting in procedural code disguised as objects.

### Anemic (BAD - Avoid)
```python
# Just data, no behavior - violates OOP principles
class Student:
    def __init__(self):
        self.name = ""
        self.grades = []

# Logic scattered in services
def calculate_points(student):
    total = 0
    for grade in student.grades:
        total += grade.score * 4
    return total
```

**Problems with Anemic Models**:
- Business logic scattered across service classes
- Data structures exposed and vulnerable to invalid states
- Difficult to maintain consistency and enforce invariants
- Loses benefits of encapsulation and OOP
- Cognitive load increases as codebase grows

### Rich (GOOD - Prefer)
```python
# Data + behavior together - proper encapsulation
class Student:
    def __init__(self, name: str):
        self._name = name
        self._grades: List[Grade] = []

    def add_grade(self, grade: Grade) -> None:
        """Domain logic with the data."""
        if grade in self._grades:
            raise DomainError("Grade already exists")
        self._grades.append(grade)

    def calculate_competence_points(self) -> CompetencePoints:
        """Behavior lives with data."""
        total = sum(grade.to_points() for grade in self._grades)
        return CompetencePoints(total)
```

**Benefits of Rich Models**:
- Encapsulation: Business logic isolated from infrastructure
- Testability: Pure domain logic is easier to test
- Maintainability: Clear mental models reduce cognitive load
- Scalability: As complexity grows, structure prevents degradation

## Why DDD Matters: Cognitive Load and Mental Models

**The Central Problem**: As codebases grow, cognitive load increases. Understanding how changes impact the system becomes difficult.

**DDD's Solution**: Create clear mental models that:
- Reduce cognitive load through well-defined boundaries
- Improve as the system grows (rather than degrade)
- Make the codebase easier to reason about over time
- Enable faster onboarding and safer changes

**Key Insight**: Without DDD structure, complexity overwhelms developers as systems scale. With DDD, the architecture provides a mental framework that remains comprehensible even as features multiply.

## Code Review Checklist

- [ ] Does code use ubiquitous language from domain?
- [ ] Are entities and value objects properly distinguished?
- [ ] Are aggregates properly bounded?
- [ ] Are invariants protected?
- [ ] Is the domain model rich (not anemic)?
- [ ] Are domain services used appropriately?
- [ ] Are domain events captured for significant happenings?
- [ ] Do repositories work with aggregate roots?
- [ ] Are bounded contexts clearly separated?
- [ ] Does the code reduce cognitive load through clear structure?
- [ ] Will this design scale as complexity grows?

## Practical Application for Admission Rules

### Entities
- `Student` (identity: student number)
- `Program` (identity: program code)
- `AdmissionRule` (identity: rule ID)

### Value Objects
- `Grade(subject, score)`
- `CompetencePoints(value)`
- `QuotaName(name)`
- `StudentId(value)`

### Aggregates
- `AdmissionApplication` (root) containing `ProgramChoice` entities
- `Program` (root) containing `Quota` entities

### Domain Services
- `AdmissionEvaluationService`
- `CompetencePointsCalculationService`

### Domain Events
- `StudentAdmitted`
- `StudentRejected`
- `QuotaFilled`
- `ApplicationSubmitted`

### Repositories
- `AdmissionRuleRepository`
- `StudentRepository`
- `ProgramRepository`

## Prerequisites for DDD Success

Before adopting DDD patterns, developers should understand:
- Object-oriented programming fundamentals
- SOLID principles (especially Single Responsibility and Dependency Inversion)
- Design patterns (Strategy, Factory, Specification)
- Separation of concerns
- Interface-based design

**Start Simple**: Don't apply all DDD patterns immediately. Begin with:
1. Ubiquitous language
2. Rich domain models (avoid anemic models)
3. Clear entity vs value object distinction
4. Then gradually adopt aggregates, domain events, specifications

## Managing DDD Complexity

**Progressive Enhancement**:
- Start with basic entities and value objects
- Add aggregates when consistency boundaries become clear
- Introduce domain events when decoupling is needed
- Apply specifications when rule combinations emerge

**Avoid Over-Engineering**:
- Not every class needs to be an aggregate
- Not every operation needs a domain service
- Not every change needs a domain event
- Keep it simple until complexity demands structure

## Response Format

When applying DDD:
1. Identify domain concepts from requirements
2. Classify as entity, value object, aggregate, or service
3. Define ubiquitous language terms
4. Protect invariants within aggregates
5. Use rich domain models with behavior
6. Capture domain events for significant changes
7. Start simple and add patterns as complexity grows
