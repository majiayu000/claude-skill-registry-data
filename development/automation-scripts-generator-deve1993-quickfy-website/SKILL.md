---
name: automation-scripts-generator
description: Generate automation scripts for component creation, bulk operations, code transformation, project scaffolding, and custom CLI tools for UI library development workflows
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Automation Scripts Generator

Expert skill for creating automation scripts and CLI tools for UI library development. Specializes in component generators, bulk operations, code transformers, project scaffolding, and custom development workflows.

## Core Capabilities

### 1. Component Generation Scripts
- **New Component**: Generate complete component with tests, styles, docs
- **Variant Generator**: Create component variants automatically
- **Bulk Creation**: Generate multiple components at once
- **Template Customization**: Configurable component templates
- **File Organization**: Auto-organize files in correct structure
- **Index Updates**: Auto-update barrel exports

### 2. Code Transformation
- **Refactoring Scripts**: Automated code refactoring
- **Migration Tools**: Migrate between patterns/libraries
- **Import Organizer**: Sort and clean imports
- **Props Transformer**: Convert prop patterns
- **Type Generator**: Generate TypeScript types from data
- **Style Converter**: Convert CSS to different formats

### 3. Bulk Operations
- **Mass Rename**: Rename files/components in bulk
- **Batch Update**: Update props across components
- **Global Replace**: Smart search and replace
- **Delete Unused**: Find and remove unused code
- **Add Feature**: Add feature to multiple components
- **Update Dependencies**: Batch dependency updates

### 4. Project Scaffolding
- **New Project**: Initialize complete UI library
- **Documentation Site**: Set up Storybook/docs site
- **Testing Setup**: Configure testing infrastructure
- **CI/CD Pipeline**: Set up GitHub Actions
- **Package Configuration**: Set up build and publish
- **Monorepo Setup**: Configure Turborepo/Nx

### 5. CLI Tools
- **Interactive Prompts**: User-friendly CLI interface
- **Command Framework**: Build custom commands
- **Configuration**: Load/save preferences
- **Validation**: Input validation and error handling
- **Progress Indicators**: Show progress for long operations
- **Logging**: Structured logging and debugging

### 6. Quality Automation
- **Linting Scripts**: Auto-fix lint issues
- **Format All**: Format entire codebase
- **Type Check**: Run TypeScript checks
- **Test Runner**: Execute test suites
- **Coverage Reports**: Generate coverage analysis
- **Performance Audit**: Analyze bundle sizes

## Workflow

### Phase 1: Script Planning
1. **Identify Task**
   - What needs automation?
   - How often is it done?
   - What's the manual process?
   - What can go wrong?

2. **Design Solution**
   - Command interface?
   - Input parameters?
   - Output format?
   - Error handling?

3. **Choose Tools**
   - Node.js script?
   - Shell script?
   - CLI framework?
   - Dependencies needed?

### Phase 2: Implementation
1. **Build Core Logic**
   - File operations
   - Code generation
   - Validation
   - Error handling

2. **Add CLI Interface**
   - Argument parsing
   - Interactive prompts
   - Progress indicators
   - Output formatting

3. **Test Thoroughly**
   - Happy path
   - Edge cases
   - Error scenarios
   - Dry run mode

### Phase 3: Integration
1. **Document Script**
   - Usage instructions
   - Examples
   - Options reference
   - Troubleshooting

2. **Add to Workflow**
   - npm scripts
   - package.json
   - CI/CD pipeline
   - Developer docs

3. **Optimize**
   - Performance
   - Error messages
   - User experience
   - Logging

## Script Templates

### Component Generator (Node.js)

```typescript
#!/usr/bin/env node
// scripts/generate-component.ts
import fs from 'fs/promises'
import path from 'path'
import { prompts } from 'prompts'
import chalk from 'chalk'

interface ComponentOptions {
  name: string
  type: 'basic' | 'compound' | 'polymorphic'
  withTests: boolean
  withStories: boolean
  withDocs: boolean
}

async function generateComponent(options: ComponentOptions) {
  const { name, type, withTests, withStories, withDocs } = options

  console.log(chalk.blue(`\n🚀 Generating ${type} component: ${name}\n`))

  const componentDir = path.join(process.cwd(), 'src', 'components', name)

  // Create directory
  await fs.mkdir(componentDir, { recursive: true })

  // Generate component file
  const componentCode = generateComponentCode(name, type)
  await fs.writeFile(path.join(componentDir, `${name}.tsx`), componentCode)
  console.log(chalk.green(`✓ Created ${name}.tsx`))

  // Generate types file
  const typesCode = generateTypesCode(name)
  await fs.writeFile(path.join(componentDir, `${name}.types.ts`), typesCode)
  console.log(chalk.green(`✓ Created ${name}.types.ts`))

  // Generate tests
  if (withTests) {
    const testCode = generateTestCode(name)
    await fs.writeFile(path.join(componentDir, `${name}.test.tsx`), testCode)
    console.log(chalk.green(`✓ Created ${name}.test.tsx`))
  }

  // Generate Storybook story
  if (withStories) {
    const storyCode = generateStoryCode(name)
    await fs.writeFile(path.join(componentDir, `${name}.stories.tsx`), storyCode)
    console.log(chalk.green(`✓ Created ${name}.stories.tsx`))
  }

  // Generate README
  if (withDocs) {
    const readmeCode = generateReadmeCode(name)
    await fs.writeFile(path.join(componentDir, 'README.md'), readmeCode)
    console.log(chalk.green(`✓ Created README.md`))
  }

  // Generate index file
  const indexCode = generateIndexCode(name)
  await fs.writeFile(path.join(componentDir, 'index.ts'), indexCode)
  console.log(chalk.green(`✓ Created index.ts`))

  // Update barrel export
  await updateBarrelExport(name)
  console.log(chalk.green(`✓ Updated src/components/index.ts`))

  console.log(chalk.green.bold(`\n✨ Component ${name} generated successfully!\n`))
}

function generateComponentCode(name: string, type: string): string {
  const templates = {
    basic: `import React from 'react'
import { ${name}Props } from './${name}.types'

export function ${name}({ children, ...props }: ${name}Props) {
  return (
    <div {...props}>
      {children}
    </div>
  )
}`,
    compound: `import React, { createContext, useContext } from 'react'
import { ${name}Props, ${name}ContextValue } from './${name}.types'

const ${name}Context = createContext<${name}ContextValue | undefined>(undefined)

export function ${name}({ children, ...props }: ${name}Props) {
  const value: ${name}ContextValue = {
    // Add context value here
  }

  return (
    <${name}Context.Provider value={value}>
      <div {...props}>{children}</div>
    </${name}Context.Provider>
  )
}

export function use${name}() {
  const context = useContext(${name}Context)
  if (!context) {
    throw new Error('use${name} must be used within ${name}')
  }
  return context
}

${name}.Item = function ${name}Item({ children }: { children: React.ReactNode }) {
  const context = use${name}()
  return <div>{children}</div>
}`,
    polymorphic: `import React from 'react'
import { ${name}Props } from './${name}.types'

export function ${name}<C extends React.ElementType = 'div'>({
  as,
  children,
  ...props
}: ${name}Props<C>) {
  const Component = as || 'div'
  return <Component {...props}>{children}</Component>
}`,
  }

  return templates[type] || templates.basic
}

function generateTypesCode(name: string): string {
  return `import React from 'react'

export interface ${name}Props extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode
  // Add your props here
}

export interface ${name}ContextValue {
  // Add context value types here
}`
}

function generateTestCode(name: string): string {
  return `import { render, screen } from '@testing-library/react'
import { ${name} } from './${name}'

describe('${name}', () => {
  it('renders children', () => {
    render(<${name}>Hello World</${name}>)
    expect(screen.getByText('Hello World')).toBeInTheDocument()
  })
})`
}

function generateStoryCode(name: string): string {
  return `import type { Meta, StoryObj } from '@storybook/react'
import { ${name} } from './${name}'

const meta: Meta<typeof ${name}> = {
  title: 'Components/${name}',
  component: ${name},
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof ${name}>

export const Default: Story = {
  args: {
    children: '${name} content',
  },
}`
}

function generateReadmeCode(name: string): string {
  return `# ${name}

## Usage

\`\`\`tsx
import { ${name} } from '@your-library/components'

function App() {
  return (
    <${name}>
      Content here
    </${name}>
  )
}
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | - | The content |

## Examples

### Basic Usage

\`\`\`tsx
<${name}>Hello World</${name}>
\`\`\`
`
}

function generateIndexCode(name: string): string {
  return `export { ${name} } from './${name}'
export type { ${name}Props } from './${name}.types'`
}

async function updateBarrelExport(name: string) {
  const indexPath = path.join(process.cwd(), 'src', 'components', 'index.ts')

  try {
    let content = await fs.readFile(indexPath, 'utf-8')
    const exportLine = `export * from './${name}'\n`

    // Check if export already exists
    if (!content.includes(exportLine)) {
      // Add export in alphabetical order
      const exports = content.split('\n').filter(line => line.startsWith('export'))
      exports.push(exportLine.trim())
      exports.sort()

      content = exports.join('\n') + '\n'
      await fs.writeFile(indexPath, content)
    }
  } catch (error) {
    // If index doesn't exist, create it
    await fs.writeFile(indexPath, `export * from './${name}'\n`)
  }
}

// CLI Interface
async function main() {
  console.log(chalk.cyan.bold('\n📦 Component Generator\n'))

  const response = await prompts([
    {
      type: 'text',
      name: 'name',
      message: 'Component name (PascalCase):',
      validate: (value) =>
        /^[A-Z][a-zA-Z0-9]*$/.test(value) || 'Must be PascalCase (e.g., Button)',
    },
    {
      type: 'select',
      name: 'type',
      message: 'Component type:',
      choices: [
        { title: 'Basic', value: 'basic' },
        { title: 'Compound', value: 'compound' },
        { title: 'Polymorphic', value: 'polymorphic' },
      ],
    },
    {
      type: 'confirm',
      name: 'withTests',
      message: 'Generate tests?',
      initial: true,
    },
    {
      type: 'confirm',
      name: 'withStories',
      message: 'Generate Storybook story?',
      initial: true,
    },
    {
      type: 'confirm',
      name: 'withDocs',
      message: 'Generate README?',
      initial: true,
    },
  ])

  if (!response.name) {
    console.log(chalk.red('\n❌ Cancelled\n'))
    process.exit(0)
  }

  try {
    await generateComponent(response as ComponentOptions)
  } catch (error) {
    console.error(chalk.red('\n❌ Error generating component:'), error)
    process.exit(1)
  }
}

main()
```

### Bulk Rename Script

```bash
#!/bin/bash
# scripts/bulk-rename.sh

# Bulk rename components
# Usage: ./scripts/bulk-rename.sh old-pattern new-pattern

set -e

OLD_PATTERN=$1
NEW_PATTERN=$2

if [ -z "$OLD_PATTERN" ] || [ -z "$NEW_PATTERN" ]; then
  echo "Usage: ./scripts/bulk-rename.sh old-pattern new-pattern"
  echo "Example: ./scripts/bulk-rename.sh UIButton Button"
  exit 1
fi

echo "🔄 Renaming $OLD_PATTERN → $NEW_PATTERN"
echo ""

# Find all files containing the old pattern
FILES=$(grep -rl "$OLD_PATTERN" src/)

if [ -z "$FILES" ]; then
  echo "❌ No files found containing '$OLD_PATTERN'"
  exit 0
fi

echo "Files to update:"
echo "$FILES"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "❌ Cancelled"
  exit 0
fi

# Replace in file contents
for file in $FILES; do
  sed -i "" "s/$OLD_PATTERN/$NEW_PATTERN/g" "$file"
  echo "✓ Updated $file"
done

# Rename files
find src/ -name "*$OLD_PATTERN*" | while read file; do
  new_file=$(echo "$file" | sed "s/$OLD_PATTERN/$NEW_PATTERN/g")
  mv "$file" "$new_file"
  echo "✓ Renamed $file → $new_file"
done

echo ""
echo "✨ Rename complete!"
```

### Code Formatter Script

```typescript
#!/usr/bin/env node
// scripts/format-all.ts
import { exec } from 'child_process'
import { promisify } from 'util'
import ora from 'ora'
import chalk from 'chalk'

const execAsync = promisify(exec)

interface FormatOptions {
  fix: boolean
  check: boolean
  staged: boolean
}

async function formatCode(options: FormatOptions) {
  const { fix, check, staged } = options

  console.log(chalk.cyan.bold('\n🎨 Code Formatter\n'))

  // Get files to format
  let files = 'src/**/*.{ts,tsx,js,jsx,css,scss,json,md}'

  if (staged) {
    const spinner = ora('Getting staged files...').start()
    try {
      const { stdout } = await execAsync('git diff --cached --name-only --diff-filter=ACMR')
      files = stdout
        .split('\n')
        .filter((f) => /\.(ts|tsx|js|jsx|css|scss|json|md)$/.test(f))
        .join(' ')

      if (!files) {
        spinner.succeed('No staged files to format')
        return
      }
      spinner.succeed(`Found ${files.split(' ').length} staged files`)
    } catch (error) {
      spinner.fail('Failed to get staged files')
      throw error
    }
  }

  // Run Prettier
  const prettierSpinner = ora('Running Prettier...').start()
  try {
    const prettierCmd = check
      ? `prettier --check ${files}`
      : `prettier --write ${files}`

    await execAsync(prettierCmd)
    prettierSpinner.succeed('Prettier complete')
  } catch (error) {
    prettierSpinner.fail('Prettier found issues')
    if (!fix) {
      console.log(chalk.yellow('\nRun with --fix to auto-fix issues'))
    }
    throw error
  }

  // Run ESLint
  const eslintSpinner = ora('Running ESLint...').start()
  try {
    const eslintCmd = fix
      ? `eslint ${files.replace(/\{.*\}/, '{ts,tsx,js,jsx}')} --fix`
      : `eslint ${files.replace(/\{.*\}/, '{ts,tsx,js,jsx}')}`

    await execAsync(eslintCmd)
    eslintSpinner.succeed('ESLint complete')
  } catch (error) {
    eslintSpinner.fail('ESLint found issues')
    if (!fix) {
      console.log(chalk.yellow('\nRun with --fix to auto-fix issues'))
    }
    throw error
  }

  console.log(chalk.green.bold('\n✨ Formatting complete!\n'))
}

// CLI
const args = process.argv.slice(2)
const options: FormatOptions = {
  fix: args.includes('--fix'),
  check: args.includes('--check'),
  staged: args.includes('--staged'),
}

formatCode(options).catch((error) => {
  console.error(chalk.red('\n❌ Formatting failed\n'))
  process.exit(1)
})
```

### Migration Script

```typescript
#!/usr/bin/env node
// scripts/migrate-to-tailwind.ts
import fs from 'fs/promises'
import path from 'path'
import { glob } from 'glob'
import chalk from 'chalk'

// CSS to Tailwind class mappings
const cssToTailwind: Record<string, string> = {
  'display: flex': 'flex',
  'flex-direction: column': 'flex-col',
  'justify-content: center': 'justify-center',
  'align-items: center': 'items-center',
  'padding: 1rem': 'p-4',
  'margin: 1rem': 'm-4',
  'background-color: #3b82f6': 'bg-blue-500',
  'color: white': 'text-white',
  'font-weight: bold': 'font-bold',
  'border-radius: 0.5rem': 'rounded-lg',
}

async function migrateToTailwind() {
  console.log(chalk.cyan.bold('\n🎨 Migrating to Tailwind CSS\n'))

  // Find all component files
  const files = await glob('src/components/**/*.tsx')

  let totalChanges = 0

  for (const file of files) {
    let content = await fs.readFile(file, 'utf-8')
    let changes = 0

    // Find style objects
    const styleRegex = /style=\{\{([^}]+)\}\}/g
    const matches = content.matchAll(styleRegex)

    for (const match of matches) {
      const styleContent = match[1]
      const classes: string[] = []

      // Convert each CSS property
      for (const [css, tailwind] of Object.entries(cssToTailwind)) {
        if (styleContent.includes(css)) {
          classes.push(tailwind)
          changes++
        }
      }

      if (classes.length > 0) {
        // Replace style with className
        const replacement = `className="${classes.join(' ')}"`
        content = content.replace(match[0], replacement)
      }
    }

    if (changes > 0) {
      await fs.writeFile(file, content)
      console.log(chalk.green(`✓ ${file} (${changes} changes)`))
      totalChanges += changes
    }
  }

  console.log(chalk.green.bold(`\n✨ Migration complete! (${totalChanges} total changes)\n`))
}

migrateToTailwind().catch((error) => {
  console.error(chalk.red('\n❌ Migration failed:'), error)
  process.exit(1)
})
```

## Best Practices

### Script Design
1. **Single Responsibility**: One script, one task
2. **Idempotent**: Safe to run multiple times
3. **Dry Run**: Preview changes before applying
4. **Validation**: Validate inputs and state
5. **Error Handling**: Graceful error messages

### CLI UX
1. **Clear Messages**: What's happening and why
2. **Progress Indicators**: Show progress for long tasks
3. **Confirmation Prompts**: Ask before destructive actions
4. **Colorized Output**: Use colors meaningfully
5. **Help Text**: Always provide --help

### Code Quality
1. **TypeScript**: Type-safe scripts
2. **Error Recovery**: Handle failures gracefully
3. **Logging**: Log important operations
4. **Testing**: Test scripts with various inputs
5. **Documentation**: Document usage and options

### Performance
1. **Parallel Operations**: Run independent tasks concurrently
2. **Caching**: Cache expensive operations
3. **Incremental**: Process only changed files
4. **Streaming**: Stream large file operations
5. **Debouncing**: Avoid duplicate operations

## When to Use This Skill

Activate this skill when you need to:
- Generate new components with boilerplate
- Create CLI tools for developers
- Automate repetitive tasks
- Migrate code between patterns
- Scaffold new projects
- Bulk update code across files
- Transform code automatically
- Set up automation workflows
- Build custom dev tools
- Optimize development workflow

## Output Format

When creating automation scripts, provide:
1. **Complete Script**: Production-ready code
2. **Installation Instructions**: Dependencies and setup
3. **Usage Guide**: How to run the script
4. **Options Reference**: All available flags/options
5. **Examples**: Common use cases
6. **Error Handling**: How errors are reported

Always build scripts that save time, prevent errors, and improve developer experience.
