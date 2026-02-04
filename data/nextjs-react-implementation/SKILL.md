---
name: nextjs-react-implementation
description: Generate production-ready Next.js/React components from design specifications. Use this skill when you have a design specification document and need to create React/TypeScript components with Tailwind CSS styling, Vitest tests, and Storybook documentation.
---

# Next.js React Implementation Generator

## Overview

Transform design specification documents into production-ready Next.js/React components with complete TypeScript types, Tailwind CSS styling, comprehensive tests, and Storybook documentation. This skill focuses on accurate implementation following modern React patterns and best practices.

**Use this skill when:**
- Implementing components from design specifications
- Creating React components with TypeScript
- Generating Tailwind CSS styled components
- Writing Vitest browser mode tests
- Creating Storybook documentation
- Building component libraries

## Prerequisites

This skill expects a design specification document created by the `figma-design-analyzer` skill or a similar structured specification. The specification should include:

- Component name and atomic category
- Semantic HTML element
- Layout and spacing details
- Typography specifications
- Color and visual properties
- Variants and states
- Responsive behavior

## Core Workflow

### Step 1: Parse Design Specification

Read and understand the design specification document:

1. **Load the specification file:**
   - Read the `.design.md` file
   - Parse front matter metadata
   - Extract all design properties

2. **Identify key information:**
   - Component name (PascalCase)
   - Atomic category (Atom/Molecule/Organism)
   - Semantic root element
   - Variants and their options
   - States (hover, active, disabled, etc.)

3. **Validate specification:**
   - Ensure all required fields are present
   - Check for contradictions or ambiguities
   - Note any missing information

### Step 2: Determine Component Structure

Plan the component implementation:

1. **Determine component directory:**
   ```
   src/components/
     atoms/ComponentName/
     molecules/ComponentName/
     organisms/ComponentName/
   ```

2. **Plan file structure:**
   ```
   ComponentName/
   ├── index.ts              # Barrel export
   ├── ComponentName.tsx     # Component implementation
   ├── ComponentName.test.tsx # Vitest tests
   └── ComponentName.stories.tsx # Storybook stories
   ```

3. **Identify dependencies:**
   - Child components (for Molecules/Organisms)
   - Icons or assets
   - Utility functions

### Step 3: Generate TypeScript Props Interface

Create type-safe props based on the specification:

1. **Read variant information from spec:**
   ```markdown
   ## Variants
   - variant: primary | secondary | tertiary
   - size: small | medium | large
   ```

2. **Create props interface:**
   ```typescript
   export interface ButtonProps {
     /** Button variant style */
     variant?: 'primary' | 'secondary' | 'tertiary';
     /** Button size */
     size?: 'small' | 'medium' | 'large';
     /** Button content */
     children: React.ReactNode;
     /** Click handler */
     onClick?: () => void;
     /** Disabled state */
     disabled?: boolean;
     /** Additional CSS classes */
     className?: string;
   }
   ```

3. **Set default props:**
   - Define sensible defaults based on the "Default" state in spec
   - Use TypeScript default parameters

### Step 4: Generate Component Implementation

Use the component template to create the implementation:

1. **Read the component template:**
   ```
   assets/templates/component.tsx.template
   ```

2. **Fill in template placeholders:**
   - `{{COMPONENT_NAME}}`: Component name in PascalCase
   - `{{COMPONENT_DESCRIPTION}}`: Brief description from spec
   - `{{ATOMIC_CATEGORY}}`: Atoms, Molecules, or Organisms
   - `{{ROOT_ELEMENT}}`: Semantic HTML element
   - `{{TAILWIND_CLASSES}}`: Base Tailwind classes from spec

3. **Implement variant logic:**
   ```typescript
   const variantClasses = {
     primary: 'bg-blue-500 text-white hover:bg-blue-600',
     secondary: 'bg-white text-blue-500 border-blue-500 hover:bg-blue-50',
     tertiary: 'bg-transparent text-blue-500 hover:bg-blue-50'
   };

   const sizeClasses = {
     small: 'px-4 py-2 text-sm',
     medium: 'px-6 py-3 text-base',
     large: 'px-8 py-4 text-lg'
   };

   const className = cn(
     'inline-flex items-center justify-center rounded-lg font-semibold',
     'transition-colors duration-200',
     'disabled:opacity-50 disabled:cursor-not-allowed',
     variantClasses[variant],
     sizeClasses[size],
     props.className
   );
   ```

4. **Handle responsive behavior:**
   - Use Tailwind responsive prefixes from spec
   - Implement mobile-first approach
   ```typescript
   className = cn(
     'w-full md:w-auto',  // Full width on mobile, auto on tablet+
     'px-4 md:px-6 lg:px-8',  // Responsive padding
     // ... other classes
   );
   ```

5. **Implement accessibility:**
   - Add ARIA attributes as specified
   - Ensure keyboard navigation
   - Include focus states
   ```typescript
   <button
     className={className}
     disabled={disabled}
     onClick={onClick}
     aria-label={ariaLabel}
     {...props}
   >
     {children}
   </button>
   ```

### Step 5: Generate Vitest Browser Mode Tests

Create comprehensive tests using the test template:

1. **Read the test template:**
   ```
   assets/templates/test.tsx.template
   ```

2. **Set up test structure:**
   ```typescript
   import { describe, it, expect, vi } from 'vitest';
   import { page } from '@vitest/browser/context';
   import { render } from 'vitest-browser-react';
   import { Button } from './Button';

   describe('Button', () => {
     // Test cases here
   });
   ```

3. **Follow TDD principles with Arrange-Act-Assert:**
   ```typescript
   it('正しくレンダリングされること', async () => {
     // Arrange
     const props = { children: 'Click Me' };

     // Act
     await render(<Button {...props} />);

     // Assert
     const button = page.getByRole('button', { name: 'Click Me' });
     await expect.element(button).toBeVisible();
   });
   ```

4. **Test all variants:**
   ```typescript
   it.each([
     { variant: 'primary', expectedClass: 'bg-blue-500' },
     { variant: 'secondary', expectedClass: 'bg-white' },
     { variant: 'tertiary', expectedClass: 'bg-transparent' }
   ])('$variant バリアントが正しくレンダリングされること', async ({ variant, expectedClass }) => {
     // Arrange & Act
     await render(<Button variant={variant}>Button</Button>);

     // Assert
     const button = page.getByRole('button');
     await expect.element(button).toHaveClass(expectedClass);
   });
   ```

5. **Test all states:**
   ```typescript
   it('無効状態が正しく動作すること', async () => {
     // Arrange
     const handleClick = vi.fn();
     await render(
       <Button disabled onClick={handleClick}>
         Disabled
       </Button>
     );

     // Act
     const button = page.getByRole('button');
     await button.click();

     // Assert
     await expect.element(button).toBeDisabled();
     expect(handleClick).not.toHaveBeenCalled();
   });
   ```

6. **Test interactions:**
   ```typescript
   it('クリックイベントが動作すること', async () => {
     // Arrange
     const handleClick = vi.fn();
     await render(<Button onClick={handleClick}>Click Me</Button>);

     // Act
     const button = page.getByRole('button');
     await button.click();

     // Assert
     expect(handleClick).toHaveBeenCalledTimes(1);
   });
   ```

7. **Test accessibility:**
   ```typescript
   it('キーボード操作が動作すること', async () => {
     // Arrange
     const handleClick = vi.fn();
     await render(<Button onClick={handleClick}>Press Enter</Button>);

     // Act
     const button = page.getByRole('button');
     await button.focus();
     await page.keyboard.press('Enter');

     // Assert
     expect(handleClick).toHaveBeenCalled();
   });
   ```

### Step 6: Generate Storybook Stories

Create interactive documentation:

1. **Read the Storybook template:**
   ```
   assets/templates/storybook.tsx.template
   ```

2. **Set up story structure:**
   ```typescript
   import type { Meta, StoryObj } from '@storybook/react';
   import { Button } from './Button';

   const meta = {
     title: 'Atoms/Button',
     component: Button,
     parameters: {
       layout: 'centered',
     },
     tags: ['autodocs'],
     argTypes: {
       variant: {
         control: 'select',
         options: ['primary', 'secondary', 'tertiary']
       },
       size: {
         control: 'select',
         options: ['small', 'medium', 'large']
       }
     }
   } satisfies Meta<typeof Button>;

   export default meta;
   type Story = StoryObj<typeof meta>;
   ```

3. **Create stories for each variant:**
   ```typescript
   export const Primary: Story = {
     args: {
       variant: 'primary',
       children: 'Primary Button'
     }
   };

   export const Secondary: Story = {
     args: {
       variant: 'secondary',
       children: 'Secondary Button'
     }
   };

   export const Tertiary: Story = {
     args: {
       variant: 'tertiary',
       children: 'Tertiary Button'
     }
   };
   ```

4. **Create stories for different sizes:**
   ```typescript
   export const Small: Story = {
     args: {
       size: 'small',
       children: 'Small Button'
     }
   };

   export const Medium: Story = {
     args: {
       size: 'medium',
       children: 'Medium Button'
     }
   };

   export const Large: Story = {
     args: {
       size: 'large',
       children: 'Large Button'
     }
   };
   ```

5. **Create stories for states:**
   ```typescript
   export const Disabled: Story = {
     args: {
       disabled: true,
       children: 'Disabled Button'
     }
   };
   ```

6. **Create interactive playground:**
   ```typescript
   export const Playground: Story = {
     args: {
       variant: 'primary',
       size: 'medium',
       children: 'Playground Button'
     }
   };
   ```

### Step 7: Handle Complex Components

For Molecules and Organisms that use child components:

1. **Identify child components:**
   - Read component hierarchy from spec
   - Import child components

2. **Compose the component:**
   ```typescript
   import { Button } from '@/components/atoms/Button';
   import { Input } from '@/components/atoms/Input';

   export function SearchBar({ onSearch }: SearchBarProps) {
     return (
       <div className="flex gap-2">
         <Input placeholder="Search..." />
         <Button onClick={onSearch}>Search</Button>
       </div>
     );
   }
   ```

3. **Pass props to children:**
   - Map parent props to child props
   - Handle event delegation

### Step 8: Implement Responsive Behavior

Add responsive styles based on the specification:

1. **Read responsive behavior from spec:**
   ```markdown
   ## Responsive Behavior
   - Mobile (default): flex-col gap-4 text-sm
   - Tablet (md): md:flex-row md:gap-6 md:text-base
   - Desktop (lg): lg:gap-8 lg:text-lg
   ```

2. **Apply Tailwind responsive prefixes:**
   ```typescript
   className = cn(
     'flex flex-col gap-4 text-sm',      // Mobile (default)
     'md:flex-row md:gap-6 md:text-base', // Tablet
     'lg:gap-8 lg:text-lg',               // Desktop
     // ... other classes
   );
   ```

3. **Test responsive behavior:**
   - Test at different viewport sizes
   - Verify layout changes

### Step 9: Add Barrel Export

Create index.ts for clean imports:

```typescript
export { Button } from './Button';
export type { ButtonProps } from './Button';
```

### Step 10: Verify Implementation

Final checks before completion:

1. **Verify against specification:**
   - All variants implemented
   - All states handled
   - Responsive behavior correct
   - Accessibility requirements met

2. **Run tests:**
   ```bash
   npm run test
   ```

3. **Run Storybook:**
   ```bash
   npm run storybook
   ```

4. **Type check:**
   ```bash
   npm run type-check
   ```

5. **Lint:**
   ```bash
   npm run lint
   ```

## Using Context7 for Latest Documentation

Always use Context7 MCP to get up-to-date documentation:

1. **Resolve library IDs:**
   ```
   mcp__context7__resolve-library-id(libraryName: "react")
   mcp__context7__resolve-library-id(libraryName: "tailwindcss")
   mcp__context7__resolve-library-id(libraryName: "vitest")
   ```

2. **Get library documentation:**
   ```
   mcp__context7__get-library-docs(
     context7CompatibleLibraryID: "/facebook/react",
     topic: "hooks"
   )
   ```

3. **Check project versions:**
   - Read package.json to determine versions
   - Use exact version for Context7 if available

## Best Practices

1. **Type Safety:**
   - Use strict TypeScript
   - Define all props with proper types
   - Avoid `any` type

2. **Component Composition:**
   - Keep components focused and single-purpose
   - Use composition over inheritance
   - Extract reusable logic into hooks

3. **Styling:**
   - Use Tailwind CSS utility classes
   - Follow project's Tailwind configuration
   - Use `cn()` utility for conditional classes

4. **Testing:**
   - Write tests before implementation (TDD)
   - Test all variants and states
   - Test user interactions
   - Test accessibility

5. **Documentation:**
   - Add JSDoc comments to props
   - Create comprehensive Storybook stories
   - Include usage examples

6. **Accessibility:**
   - Use semantic HTML
   - Add ARIA attributes when needed
   - Ensure keyboard navigation
   - Test with screen readers

7. **Performance:**
   - Avoid unnecessary re-renders
   - Use React.memo when appropriate
   - Optimize large lists with virtualization

## Resources

This skill includes templates for code generation:

### assets/templates/

- **component.tsx.template**: React/TypeScript component structure
- **test.tsx.template**: Vitest browser mode test structure
- **storybook.tsx.template**: Storybook story structure

**Usage:** Use these templates as starting points. Fill in placeholders with values from the design specification.

## Common Pitfalls

1. **Ignoring the specification:**
   - Always implement exactly as specified
   - Don't make assumptions
   - Ask for clarification if ambiguous

2. **Incomplete variant handling:**
   - Implement all variants from spec
   - Don't skip edge cases

3. **Poor test coverage:**
   - Test all variants
   - Test all states
   - Test all interactions

4. **Accessibility oversights:**
   - Don't forget ARIA attributes
   - Ensure keyboard navigation
   - Test with assistive technologies

5. **Inconsistent naming:**
   - Follow project naming conventions
   - Use consistent prop names
   - Match Figma component names

6. **Hardcoded values:**
   - Use props and configuration
   - Avoid magic numbers
   - Use design tokens when available

## Example Implementation Flow

**Input:** Button.design.md specification

**Steps:**
1. Parse specification
2. Create directory: `src/components/atoms/Button/`
3. Generate `Button.tsx` with variants (primary, secondary, tertiary) and sizes (small, medium, large)
4. Generate `Button.test.tsx` with tests for all variants, sizes, and states
5. Generate `Button.stories.tsx` with interactive stories
6. Create `index.ts` barrel export
7. Verify implementation against specification
8. Run tests and Storybook

**Output:**
- Production-ready Button component
- Comprehensive test suite
- Interactive Storybook documentation

---

**This skill transforms design specifications into production-ready Next.js/React components with complete testing and documentation.**
