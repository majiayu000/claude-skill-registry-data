---
name: musubix-code-generation
description: Guide for generating code from design specifications using MUSUBIX. Use this when asked to generate code, implement features, or create components following design documents.
license: MIT
---

# MUSUBIX Code Generation Skill

This skill guides you through generating code from design specifications following MUSUBIX methodology.

## Prerequisites

Before generating code:

1. Verify design document exists (`DES-*`)
2. Verify requirements are traceable (`REQ-*`)
3. Check `steering/tech.ja.md` for technology stack

## Supported Languages

| Language | Extension | Features |
|----------|-----------|----------|
| TypeScript | `.ts` | Full support with types |
| JavaScript | `.js` | ES6+ modules |
| Python | `.py` | Type hints support |
| Java | `.java` | Interface/Class generation |
| Go | `.go` | Struct/Interface generation |
| Rust | `.rs` | Trait/Struct generation |
| C# | `.cs` | Interface/Class generation |

## Code Generation Workflow

### Step 1: Read Design Document

```bash
# Generate code from design
npx musubix codegen generate <design-file>
```

### Step 2: Generate with Traceability

Always include requirement references:

```typescript
/**
 * UserService - Handles user operations
 * 
 * @see REQ-INT-001 - Neuro-Symbolic Integration
 * @see DES-INT-001 - Integration Layer Design
 */
export class UserService {
  // Implementation
}
```

### Step 3: Follow Test-First (Article III)

1. **Write test first**:
```typescript
describe('UserService', () => {
  it('should create user', async () => {
    const service = new UserService();
    const user = await service.create({ name: 'Test' });
    expect(user.id).toBeDefined();
  });
});
```

2. **Implement minimal code**:
```typescript
export class UserService {
  async create(data: CreateUserDto): Promise<User> {
    return { id: generateId(), ...data };
  }
}
```

3. **Refactor**

## Design Pattern Templates

### Singleton Pattern
```typescript
/**
 * @see REQ-DES-001 - Pattern Detection
 * @pattern Singleton
 */
export class ConfigManager {
  private static instance: ConfigManager;
  
  private constructor() {}
  
  static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }
}
```

### Factory Pattern
```typescript
/**
 * @see REQ-DES-001 - Pattern Detection
 * @pattern Factory
 */
export interface ServiceFactory {
  create(type: string): Service;
}

export class DefaultServiceFactory implements ServiceFactory {
  create(type: string): Service {
    switch (type) {
      case 'auth': return new AuthService();
      case 'user': return new UserService();
      default: throw new Error(`Unknown service: ${type}`);
    }
  }
}
```

### Repository Pattern
```typescript
/**
 * @see REQ-COD-001 - Code Generation
 * @pattern Repository
 */
export interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}

export class UserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    // Implementation
  }
  // ... other methods
}
```

## CLI Commands

```bash
# Generate code from design
npx musubix codegen generate <design-file>

# Analyze existing code
npx musubix codegen analyze <file>

# Security scan
npx musubix codegen security <path>
```

## Quality Checks (Article IX)

Before committing code:

- [ ] **Type Safety**: No `any` types (TypeScript)
- [ ] **Traceability**: All classes/functions have `@see` references
- [ ] **Tests**: Test coverage ≥ 80%
- [ ] **Linting**: `npm run lint` passes
- [ ] **Build**: `npm run build` succeeds

## Neuro-Symbolic Integration (REQ-INT-002)

When generating code that involves decision-making:

```typescript
/**
 * @see REQ-INT-002 - Confidence Evaluation
 */
async function integrateResults(
  neuralResult: NeuralResult,
  symbolicResult: SymbolicResult
): Promise<FinalResult> {
  // Decision rules from REQ-INT-002
  if (symbolicResult.status === 'invalid') {
    return rejectNeural(neuralResult);
  }
  
  if (neuralResult.confidence >= 0.8) {
    return adoptNeural(neuralResult);
  }
  
  return prioritizeSymbolic(symbolicResult);
}
```

## File Structure Convention

```
packages/
├── core/
│   └── src/
│       ├── [feature]/
│       │   ├── index.ts        # Public exports
│       │   ├── [feature].ts    # Main implementation
│       │   ├── types.ts        # Type definitions
│       │   └── __tests__/      # Tests
│       └── index.ts            # Package exports
```

## Error Handling Pattern

```typescript
/**
 * @see REQ-ERR-001 - Graceful Degradation
 */
export class MuSubixError extends Error {
  constructor(
    message: string,
    public code: string,
    public recoverable: boolean = true
  ) {
    super(message);
    this.name = 'MuSubixError';
  }
}

// Usage
throw new MuSubixError(
  'Failed to connect to YATA',
  'YATA_CONNECTION_ERROR',
  true // Can retry
);
```
