---
name: bulletproof-react-auditor
version: 0.2.0
description: Use PROACTIVELY when users ask about React project structure, Bulletproof React patterns, or need architecture guidance. Covers structure setup, codebase auditing, anti-pattern detection, and feature-based migration planning. Triggers on "bulletproof react", "React structure help", "organize React app", or "audit my architecture".
---

# Bulletproof React Auditor

Audits React/TypeScript codebases against Bulletproof React architecture with migration planning.

## When to Use

**Natural Language Triggers** (semantic matching, not keywords):
- Questions about React project structure or organization
- Mentions of "bulletproof react" or feature-based architecture
- Requests to audit, review, or improve React codebase
- Planning migrations or refactoring React applications
- Seeking guidance on component patterns or folder structure

**Use Cases**:
- Setting up new React project structure
- Reorganizing existing flat codebase
- Auditing architecture against Bulletproof standards
- Planning migration to feature-based patterns
- Code review for structural anti-patterns
- Generating refactoring guidance and ADRs

## Bulletproof Structure Target

```
src/
├── app/           # Routes, providers
├── components/    # Shared components ONLY
├── config/        # Global config
├── features/      # Feature modules (most code)
│   └── feature/
│       ├── api/
│       ├── components/
│       ├── hooks/
│       ├── stores/
│       └── types/
├── hooks/         # Shared hooks
├── lib/           # Third-party configs
├── stores/        # Global state
├── testing/       # Test utilities
├── types/         # Shared types
└── utils/         # Shared utilities
```

## Audit Categories

| Category | Key Checks |
|----------|------------|
| Structure | Feature folders, cross-feature imports, boundaries |
| Components | Size (<300 LOC), props (<10), composition |
| State | Appropriate categories, localization, server cache |
| API Layer | Centralized client, types, React Query/SWR |
| Testing | Trophy (70/20/10), semantic queries, behavior |
| Styling | Consistent approach, component library |
| Errors | Boundaries, interceptors, tracking |
| Performance | Code splitting, memoization, bundle size |
| Security | JWT cookies, RBAC, XSS prevention |
| Standards | ESLint, Prettier, TS strict, Husky |

## Usage Examples

```
# Basic audit
Audit this React codebase using bulletproof-react-auditor.

# Structure focus
Run structure audit against Bulletproof React patterns.

# Migration plan
Generate migration plan to Bulletproof architecture.

# Custom scope
Audit focusing on structure, components, and state management.
```

## Output Formats

1. **Markdown Report** - ASCII diagrams, code examples
2. **JSON Report** - Machine-readable for CI/CD
3. **Migration Plan** - Roadmap with effort estimates

## Priority Levels

| Priority | Examples | Timeline |
|----------|----------|----------|
| P0 Critical | Security vulns, breaking issues | Immediate |
| P1 High | Feature folder creation, reorg | This sprint |
| P2 Medium | State refactor, API layer | Next quarter |
| P3 Low | Styling, docs, polish | Backlog |

## Connor's Standards Enforced

- TypeScript strict mode (no `any`)
- 80%+ test coverage
- Testing trophy: 70% integration, 20% unit, 10% E2E
- No console.log in production
- Semantic queries (getByRole preferred)

## Best Practices

1. Fix folder organization before component refactoring
2. Extract features before other changes
3. Maintain test coverage during migration
4. Incremental migration, not all at once
5. Document decisions with ADRs

## Limitations

- Static analysis only
- Requires React 16.8+ (hooks)
- Best for SPA/SSG (Next.js differs)
- Large codebases need scoped analysis

## Resources

- [Bulletproof React Guide](https://github.com/alan2207/bulletproof-react)
- [Project Structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md)
- [Sample App](https://github.com/alan2207/bulletproof-react/tree/master/apps/react-vite)

## References

See `reference/` for:
- Complete Bulletproof principles guide
- Detailed audit criteria checklist
- Migration patterns and examples
- ADR templates
