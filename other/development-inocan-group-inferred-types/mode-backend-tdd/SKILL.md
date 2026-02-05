---
name: MODE_Backend_TDD
description: Methodological skill for Test-Driven Development in NestJS backend. This skill should be used when strict quality requirements demand tests-first approach, refactoring critical services, or building MVPs with mandatory coverage. Complements nestjs-architect skill with TDD methodology.
---

# Backend TDD Mode

## Purpose

Transform backend development from waterfall (code → tests) to iterative TDD (test → code → refactor), where tests drive design decisions and Clean Architecture emerges from test requirements.

**Prerequisites:** This skill assumes familiarity with [nestjs-architect](../nestjs-architect/SKILL-LITE.md) for DDD, Clean Architecture, and NestJS integration patterns.

## Activation Triggers

- Flags: `--modo-backend-tdd`, `--tdd-clean-architecture`, `--strict-quality-mode`
- Verbal: "Start with unit tests", "Follow TDD rigorously", "Tests first"
- Context: PRD/TechSpec requires coverage ≥80%, refactoring critical services, MVP with mandatory quality gates

## Behavioral Changes

1. **Tests First** - Draft test specifications BEFORE any production code; never implement without failing test
2. **Dependency Inversion** - Define interfaces/contracts before implementations; inject via DI
3. **Continuous Refinement** - After each Red-Green cycle, eliminate coupling/duplication
4. **Visible Metrics** - Communicate coverage, complexity, execution time as part of decisions

## Core Process: Red-Green-Refactor (7 Steps)

Execute iteratively for each use case:

**Step 1: Confirm Context**

- Validate task objective, acceptance criteria, quality indicators (coverage ≥80%, complexity <10, execution <5s)

**Step 2: Model Contracts**

- Define interfaces (repositories, services) before implementations
- Follow [aggregates](../nestjs-architect/sections/aggregates.md) and [repositories](../nestjs-architect/sections/repositories.md) patterns

**Step 3: Write Tests (RED)**

- Create `.spec.ts` files in `__tests__` directories per [testing patterns](../nestjs-architect/sections/testing.md)
- Cover happy path + critical edge cases
- Use Arrange-Act-Assert pattern

**Step 4: Execute and Validate Failure (RED)**

- Run `npm run test` and confirm ALL new tests FAIL
- If tests pass without implementation, review test validity

**Step 5: Implement Minimum Code (GREEN)**

- Write minimal code to make tests pass
- Follow [architecture principles](../nestjs-architect/sections/architecture.md) for layer separation (domain/application/infrastructure)
- Apply TypeScript strictness (no `any`, strict mode enabled)
- Run `npm run test` and confirm GREEN

**Step 6: Refactor (REFACTOR)**

- Eliminate duplication and coupling while keeping tests green
- Verify Clean Architecture compliance (dependencies point inward)
- Run `npm run test` continuously during refactoring

**Step 7: Register Metrics**

- Execute `npm run test:cov` for coverage report
- Document: coverage %, complexity, execution time
- **Evaluate if more scenarios need coverage. If yes, return to Step 2 for next use case.**

## Expected Outcomes

Validate TDD application by verifying:

1. Test files created BEFORE production code (verify timestamps/commits)
2. Initial RED state documented (console logs showing failures)
3. Implementation organized per [architecture structure](../nestjs-architect/SKILL-LITE.md#2-estrutura-mínima) (core/domain, core/application, core/infra)
4. Interfaces and contracts explicit (repositories.interface.ts, use-cases.interface.ts)
5. Metrics documented: coverage ≥80%, complexity <10, execution <5s

## Quality Standards

**Mandatory criteria:**

1. **Tests First** - NO production code without failing test; commits show tests → implementation
2. **Segregated Layers** - Follow [architecture structure](../nestjs-architect/sections/architecture.md) (domain isolated, unidirectional dependencies)
3. **Testable Interfaces** - All external dependencies via interfaces with fakes/stubs per [repositories](../nestjs-architect/sections/repositories.md)
4. **Objective Metrics** - Run `npm run test:cov`, verify thresholds, document results
5. **Documentation** - Architectural decisions and metrics in `tasks.md` or `dev-log/`

## Example: Transformation

**Standard (Waterfall):**

```typescript
// 1. Implement service directly with Prisma
@Injectable()
export class PedidosService {
  constructor(private prisma: PrismaClient) {} // Tight coupling
  async listarPedidos() {
    return this.prisma.pedido.findMany();
  }
}
// 2. Write tests afterward
```

**TDD Mode:**

```typescript
// 1. Define interface (contract)
export interface IPedidosRepository {
  findAll(): Promise<Pedido[]>;
}

// 2. Write failing test with stub
it('should return all orders', async () => {
  repositoryStub.findAll.resolves(mockPedidos);
  const result = await useCase.execute();
  expect(result).toEqual(mockPedidos);
});

// 3. Implement use case (GREEN)
export class ListarPedidosUseCase {
  constructor(private readonly repo: IPedidosRepository) {}
  async execute(): Promise<Pedido[]> {
    return this.repo.findAll();
  }
}

// 4. Implement repository (concrete)
export class PedidosPrismaRepository implements IPedidosRepository {
  constructor(private prisma: PrismaService) {}
  async findAll(): Promise<Pedido[]> { /* ... */ }
}
```

**Result:** Decoupled design, testable with stubs, swappable implementations.

## Integration Points

- **With nestjs-architect:** Apply TDD methodology to [DDD/Clean Architecture patterns](../nestjs-architect/SKILL-LITE.md)
- **With backend-nestjs agent:** Agent executes this skill when TDD mode activated
- **With executar-tarefa workflow:** Modifies Sections 2 (modeling), 4 (implementation), 5 (validation)
- **With architecture guidelines:** References [testing](../nestjs-architect/sections/testing.md), [observability](../nestjs-architect/sections/infra-observability.md)

## References

- **Architectural patterns:** See [nestjs-architect](../nestjs-architect/SKILL-LITE.md)
- **Testing patterns:** See [testing section](../nestjs-architect/sections/testing.md)
- **Books:** "Test Driven Development: By Example" (Kent Beck), "Clean Architecture" (Robert C. Martin)
