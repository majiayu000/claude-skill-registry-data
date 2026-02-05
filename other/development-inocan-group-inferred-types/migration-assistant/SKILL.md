---
name: migration-assistant
description: Expert in code migrations, version upgrades, breaking change handling, automated codemods, deprecation warnings, and migration testing
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Migration Assistant

Expert skill for handling code migrations and version upgrades. Specializes in codemods, breaking change detection, automated migrations, and upgrade strategies.

## Core Capabilities

### 1. Version Migrations
- **React Upgrades**: v16 → v17 → v18
- **Dependency Updates**: Major version changes
- **Breaking Changes**: Identify and fix
- **Deprecation Warnings**: Replace deprecated APIs
- **Migration Guides**: Step-by-step instructions

### 2. Codemods
- **jscodeshift**: AST transformations
- **Custom Transforms**: Project-specific migrations
- **Batch Updates**: Update multiple files
- **Safe Migrations**: Test before apply
- **Rollback**: Undo if needed

### 3. Pattern Migrations
- **Component Patterns**: Class → Function
- **State Management**: Context → Zustand/Redux
- **Styling**: CSS → Tailwind/CSS-in-JS
- **Build Tools**: Webpack → Vite
- **Testing**: Enzyme → Testing Library

### 4. Breaking Change Detection
- **API Changes**: Detect usage of changed APIs
- **Prop Changes**: Component API updates
- **Import Changes**: Module resolution
- **Type Changes**: TypeScript migrations

## React 18 Migration

```typescript
// React 18 Codemod
// Class component → Function component with hooks

// Before (React 16/17)
class Counter extends React.Component {
  state = { count: 0 }

  increment = () => {
    this.setState({ count: this.state.count + 1 })
  }

  render() {
    return (
      <div>
        <p>{this.state.count}</p>
        <button onClick={this.increment}>+</button>
      </div>
    )
  }
}

// After (React 18)
function Counter() {
  const [count, setCount] = useState(0)

  const increment = () => {
    setCount(count + 1)
  }

  return (
    <div>
      <p>{count}</p>
      <button onClick={increment}>+</button>
    </div>
  )
}

// React 18 Root API
// Before
import ReactDOM from 'react-dom'
ReactDOM.render(<App />, document.getElementById('root'))

// After
import { createRoot } from 'react-dom/client'
const root = createRoot(document.getElementById('root')!)
root.render(<App />)
```

## Codemod Example

```typescript
// codemod/class-to-function.ts
import { Transform } from 'jscodeshift'

const transform: Transform = (file, api) => {
  const j = api.jscodeshift
  const root = j(file.source)

  // Find class components
  root.find(j.ClassDeclaration).forEach(path => {
    const className = path.value.id.name

    // Convert to function component
    const functionComponent = j.functionDeclaration(
      j.identifier(className),
      [],
      j.blockStatement([
        // Add hooks based on state and lifecycle
        // ... transformation logic
      ])
    )

    j(path).replaceWith(functionComponent)
  })

  return root.toSource()
}

export default transform

// Run codemod
// npx jscodeshift -t codemod/class-to-function.ts src/
```

## Migration Checklist

```markdown
# React 18 Migration Checklist

## Pre-migration
- [ ] Audit current React version
- [ ] Read React 18 migration guide
- [ ] Update TypeScript to 4.5+
- [ ] Backup codebase
- [ ] Run current tests

## Dependencies
- [ ] Update react to 18.x
- [ ] Update react-dom to 18.x
- [ ] Update @types/react
- [ ] Update testing library
- [ ] Check all dependencies compatibility

## Code Changes
- [ ] Update root rendering API
- [ ] Replace deprecated APIs
- [ ] Add types for new features
- [ ] Update tests
- [ ] Fix TypeScript errors

## Testing
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Manual QA testing
- [ ] Performance testing

## Post-migration
- [ ] Update documentation
- [ ] Train team on new features
- [ ] Monitor production
- [ ] Clean up deprecated code
```

## Deprecation Warning System

```typescript
// utils/deprecation.ts
export function deprecationWarning(
  oldAPI: string,
  newAPI: string,
  version: string
) {
  if (process.env.NODE_ENV === 'development') {
    console.warn(
      `[Deprecation] ${oldAPI} is deprecated and will be removed in v${version}. ` +
      `Please use ${newAPI} instead.`
    )
  }
}

// Usage
function OldComponent(props: Props) {
  deprecationWarning('OldComponent', 'NewComponent', '2.0.0')
  return <div>{/* ... */}</div>
}
```

## Breaking Change Detection

```typescript
// scripts/detect-breaking-changes.ts
import { Project } from 'ts-morph'

const project = new Project()
project.addSourceFilesAtPaths('src/**/*.{ts,tsx}')

const breakingChanges = []

// Detect usage of deprecated APIs
project.getSourceFiles().forEach(sourceFile => {
  const deprecatedAPIs = sourceFile
    .getDescendantsOfKind(ts.SyntaxKind.CallExpression)
    .filter(call => {
      const name = call.getExpression().getText()
      return DEPRECATED_APIS.includes(name)
    })

  if (deprecatedAPIs.length > 0) {
    breakingChanges.push({
      file: sourceFile.getFilePath(),
      apis: deprecatedAPIs.map(api => api.getText()),
    })
  }
})

console.log('Breaking changes found:', breakingChanges)
```

## Best Practices

- Read migration guides thoroughly
- Test migrations on a branch
- Update dependencies incrementally
- Use codemods for repetitive changes
- Keep comprehensive test coverage
- Document breaking changes
- Communicate with team
- Monitor after migration

## When to Use This Skill

Use when you need to:
- Upgrade React or dependencies
- Migrate between libraries
- Handle breaking changes
- Create codemods
- Automate code transformations
- Deprecate old APIs
- Guide team through migrations

## Output Format

Provide:
1. **Migration Plan**: Step-by-step guide
2. **Codemods**: Automated transformations
3. **Breaking Changes**: What changed
4. **Testing Strategy**: Ensure nothing breaks
5. **Documentation**: Update guides
6. **Rollback Plan**: If things go wrong
