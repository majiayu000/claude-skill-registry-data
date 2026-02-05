---
name: docs-generator
description: Generate documentation from code, create API references, update README files, and maintain project documentation. Use when user says "document this", "generate docs", "update README", "create API docs", or when documentation is needed.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# Documentation Generator

## When to Use

Activate this skill when:
- User requests to "document this code" or "generate documentation"
- User says "update README" or "create README"
- User mentions "API docs" or "API reference"
- User asks to "add JSDoc" or "add comments"
- User wants to "document functions" or "document components"
- User requests "usage examples" or "code examples"
- User says "create documentation" or "write docs"
- New features need documentation
- User mentions "docstrings", "typedoc", or "jsdoc"

## Instructions

### Step 1: Identify Documentation Type

Determine what needs documentation:

1. **Code Documentation**: JSDoc/TSDoc comments in source files
2. **README**: Project overview, setup, usage
3. **API Reference**: Function/class documentation
4. **Component Docs**: React/Vue component props and usage
5. **Architecture Docs**: System design, data flow
6. **Tutorial/Guide**: Step-by-step instructions

### Step 2: Analyze Code to Document

1. Find files needing documentation:
```bash
# Find all source files
find src -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) \
  -not -path "*/node_modules/*"
```

2. Read and analyze code:
   - Function signatures
   - Parameters and return types
   - Component props
   - Class methods
   - Exported APIs

3. Identify existing documentation:
```bash
# Check for existing docs
ls -la README.md docs/ CONTRIBUTING.md API.md 2>/dev/null
```

### Step 3: Generate Appropriate Documentation

#### For Functions (JSDoc/TSDoc):

```typescript
/**
 * Calculates the sum of two numbers
 *
 * @param a - The first number
 * @param b - The second number
 * @returns The sum of a and b
 * @throws {Error} If parameters are not numbers
 *
 * @example
 * ```typescript
 * const result = add(2, 3);
 * console.log(result); // 5
 * ```
 */
function add(a: number, b: number): number {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Parameters must be numbers');
  }
  return a + b;
}
```

#### For React Components:

```typescript
/**
 * A reusable button component
 *
 * @component
 * @example
 * ```tsx
 * <Button onClick={handleClick} variant="primary">
 *   Click me
 * </Button>
 * ```
 */
interface ButtonProps {
  /** The button text or content */
  children: React.ReactNode;
  /** Click handler function */
  onClick?: () => void;
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'danger';
  /** Whether the button is disabled */
  disabled?: boolean;
}

export function Button({
  children,
  onClick,
  variant = 'primary',
  disabled = false
}: ButtonProps) {
  // Implementation
}
```

#### For Classes:

```typescript
/**
 * Manages user authentication and session
 *
 * @class UserManager
 * @example
 * ```typescript
 * const manager = new UserManager();
 * await manager.login('user@example.com', 'password');
 * const user = manager.getCurrentUser();
 * ```
 */
class UserManager {
  /**
   * Creates a new UserManager instance
   *
   * @param config - Configuration options
   */
  constructor(config?: UserManagerConfig) {
    // Implementation
  }

  /**
   * Authenticates a user with email and password
   *
   * @param email - User's email address
   * @param password - User's password
   * @returns Promise resolving to authenticated user
   * @throws {AuthError} If credentials are invalid
   */
  async login(email: string, password: string): Promise<User> {
    // Implementation
  }
}
```

### Step 4: Generate README (if needed)

Create comprehensive README.md:

```markdown
# Project Name

Brief description of what the project does and who it's for.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
npm install project-name
\`\`\`

## Usage

\`\`\`typescript
import { functionName } from 'project-name';

const result = functionName('example');
\`\`\`

## API Reference

### functionName(param: string): string

Description of what the function does.

**Parameters:**
- `param` (string): Description of parameter

**Returns:**
- (string): Description of return value

**Example:**
\`\`\`typescript
const result = functionName('test');
console.log(result); // Output
\`\`\`

## Development

\`\`\`bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
\`\`\`

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.
```

### Step 5: Generate API Documentation

Use documentation generators if available:

```bash
# TypeDoc for TypeScript
npx typedoc --out docs src/index.ts

# JSDoc for JavaScript
npx jsdoc -c jsdoc.json

# Storybook for React components
npm run storybook
```

### Step 6: Update Existing Documentation

1. Read current documentation:
```bash
cat README.md
```

2. Identify outdated sections
3. Update with current information
4. Maintain consistent formatting
5. Add new sections as needed

### Step 7: Verify Documentation

1. Check for:
   - Clarity and completeness
   - Code examples that work
   - Correct parameter types
   - Up-to-date API references
   - Working links

2. Test code examples:
```bash
# Extract and test code examples
# Ensure examples actually work
```

## Examples

### Example 1: Document a Utility Function

```typescript
// Before
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

// After
/**
 * Formats a Date object into ISO date string (YYYY-MM-DD)
 *
 * @param date - The date to format
 * @returns ISO formatted date string (YYYY-MM-DD)
 * @throws {TypeError} If date is not a valid Date object
 *
 * @example
 * ```typescript
 * const date = new Date('2024-01-15T10:30:00');
 * const formatted = formatDate(date);
 * console.log(formatted); // "2024-01-15"
 * ```
 */
function formatDate(date: Date): string {
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    throw new TypeError('Invalid date object');
  }
  return date.toISOString().split('T')[0];
}
```

### Example 2: Generate README for New Project

```bash
# Step 1: Analyze project structure
ls -la
cat package.json

# Step 2: Create README.md with Write tool
# Include: title, description, installation, usage, examples

# Step 3: Add badges
# Build status, coverage, version, license

# Step 4: Add screenshots/demos if applicable
```

### Example 3: Document React Component

```typescript
/**
 * Card component for displaying content in a contained box
 *
 * @component
 * @example
 * ```tsx
 * <Card title="Welcome" variant="outlined">
 *   <p>Card content goes here</p>
 * </Card>
 * ```
 */
interface CardProps {
  /** Card title displayed at the top */
  title?: string;
  /** Visual style variant */
  variant?: 'filled' | 'outlined' | 'elevated';
  /** Card content */
  children: React.ReactNode;
  /** Optional click handler */
  onClick?: () => void;
  /** Additional CSS classes */
  className?: string;
}

export function Card({
  title,
  variant = 'filled',
  children,
  onClick,
  className = ''
}: CardProps) {
  return (
    <div
      className={`card card-${variant} ${className}`}
      onClick={onClick}
    >
      {title && <h3 className="card-title">{title}</h3>}
      <div className="card-content">{children}</div>
    </div>
  );
}
```

### Example 4: Generate API Reference

```bash
# Step 1: Install TypeDoc
npm install --save-dev typedoc

# Step 2: Create typedoc.json
cat > typedoc.json << 'EOF'
{
  "entryPoints": ["src/index.ts"],
  "out": "docs",
  "excludePrivate": true,
  "excludeProtected": false,
  "readme": "README.md"
}
EOF

# Step 3: Generate docs
npx typedoc

# Step 4: Review generated docs
open docs/index.html
```

### Example 5: Update Existing README

```bash
# Step 1: Read current README
cat README.md

# Step 2: Identify changes needed
# - New features added
# - API changes
# - Updated dependencies
# - New installation steps

# Step 3: Update README with Edit tool
# Add new sections
# Update examples
# Fix broken links

# Step 4: Verify changes
cat README.md
```

## Best Practices

### ✅ DO:
- Write documentation as you code, not after
- Include working code examples
- Keep documentation in sync with code
- Use standard documentation formats (JSDoc, TSDoc)
- Document public APIs thoroughly
- Include parameter types and return types
- Add @example tags with real usage
- Write clear, concise descriptions
- Document edge cases and errors
- Use consistent formatting
- Include setup and installation instructions
- Add troubleshooting section for common issues

### ❌ DON'T:
- Don't document obvious code (self-explanatory)
- Don't write outdated documentation
- Don't copy-paste documentation without reviewing
- Don't forget to update docs when code changes
- Don't use vague descriptions like "does stuff"
- Don't document implementation details (document interface)
- Don't include code examples that don't work
- Don't forget to document error cases
- Don't use complex jargon without explanation

### JSDoc/TSDoc Tags:

Common tags to use:
- `@param` - Document parameters
- `@returns` - Document return value
- `@throws` - Document exceptions
- `@example` - Provide usage examples
- `@deprecated` - Mark deprecated features
- `@see` - Reference related items
- `@since` - When feature was added
- `@todo` - Future improvements
- `@remarks` - Additional notes
- `@beta` - Experimental features

### Documentation Structure:

1. **Summary**: One-line description
2. **Description**: Detailed explanation
3. **Parameters**: All parameters with types
4. **Returns**: Return value and type
5. **Throws**: Possible errors
6. **Examples**: Working code examples
7. **See Also**: Related functions/docs
8. **Remarks**: Additional context

### README Template Sections:

```markdown
# Project Title
## Badges (build, coverage, version)
## Description
## Features
## Screenshots/Demo
## Installation
## Quick Start
## Usage
## API Reference
## Examples
## Configuration
## Development
## Testing
## Deployment
## Contributing
## License
## Authors
## Acknowledgments
## FAQ
## Troubleshooting
## Changelog
```

## Documentation Checklist

Before writing documentation:
- [ ] Identified what needs documenting
- [ ] Analyzed code thoroughly
- [ ] Understood use cases
- [ ] Prepared examples
- [ ] Checked existing documentation

While writing documentation:
- [ ] Clear, concise descriptions
- [ ] All parameters documented
- [ ] Return types specified
- [ ] Error cases covered
- [ ] Working examples included
- [ ] Consistent formatting
- [ ] Proper grammar and spelling
- [ ] Code examples tested

After writing documentation:
- [ ] Examples actually work
- [ ] All links valid
- [ ] Consistent with project style
- [ ] No outdated information
- [ ] Covers common use cases
- [ ] Easy to understand for target audience
- [ ] Generated docs build without errors

## Troubleshooting

**Issue**: Generated docs have broken links
**Solution**: Check file paths, ensure all referenced files exist, use relative links correctly.

**Issue**: Code examples don't work
**Solution**: Test examples in isolation. Ensure imports are included. Check for missing dependencies.

**Issue**: Documentation out of sync with code
**Solution**: Set up automated doc generation in CI/CD. Add pre-commit hooks to check docs.

**Issue**: TypeDoc/JSDoc fails to generate
**Solution**: Check for syntax errors in comments. Ensure entry points are correct. Verify tsconfig.json settings.

**Issue**: Too much/too little documentation
**Solution**: Focus on public APIs. Document "why" not "how". Skip self-explanatory code.

**Issue**: Documentation unclear to users
**Solution**: Get feedback from target audience. Add more examples. Use simpler language.

## Documentation Tools

### TypeDoc (TypeScript)
```bash
npm install --save-dev typedoc

# Generate docs
npx typedoc --out docs src

# With config file
npx typedoc
```

### JSDoc (JavaScript)
```bash
npm install --save-dev jsdoc

# Generate docs
npx jsdoc -c jsdoc.json src
```

### Storybook (React Components)
```bash
npx sb init

# Run storybook
npm run storybook

# Build static docs
npm run build-storybook
```

### Docusaurus (Full Documentation Site)
```bash
npx create-docusaurus@latest docs classic

# Run dev server
cd docs
npm start

# Build
npm run build
```

### VitePress (Vue Documentation)
```bash
npm install -D vitepress

# Init docs
npx vitepress init

# Run dev server
npm run docs:dev
```

## Automation

### Generate docs on commit (package.json):
```json
{
  "scripts": {
    "docs": "typedoc",
    "docs:watch": "typedoc --watch",
    "predocs": "npm run lint"
  },
  "husky": {
    "hooks": {
      "pre-commit": "npm run docs"
    }
  }
}
```

### CI/CD Documentation Deployment:
```yaml
# GitHub Actions
- name: Generate documentation
  run: npm run docs

- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./docs
```

## Documentation Standards

### Function Documentation:
```typescript
/**
 * Brief one-line summary
 *
 * Longer description explaining what the function does,
 * when to use it, and any important notes.
 *
 * @param paramName - Parameter description
 * @returns Description of return value
 * @throws {ErrorType} When error occurs
 *
 * @example
 * ```typescript
 * const result = functionName('example');
 * ```
 *
 * @see relatedFunction
 * @since 1.0.0
 */
```

### Component Documentation:
```typescript
/**
 * Component summary
 *
 * @component
 * @example
 * ```tsx
 * <ComponentName prop="value">
 *   Content
 * </ComponentName>
 * ```
 */
```

### Class Documentation:
```typescript
/**
 * Class summary
 *
 * @class ClassName
 * @example
 * ```typescript
 * const instance = new ClassName();
 * instance.method();
 * ```
 */
```
