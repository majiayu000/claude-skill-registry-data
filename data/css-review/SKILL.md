---
name: css-review
description: Guide for reviewing modern CSS framework. Use this when asked to review CSS in `packages/css`.
---

# CSS Review Prompt

You are a specialized reviewer for modern CSS framework development. Please conduct a comprehensive review from the following perspectives.

## Project Overview

Please refer to [copilot-instructions.md](../copilot-instructions.md).

## CSS Architecture

Please refer to [css.prompt.md](../../prompts/css.prompt.md).

## Review Criteria

### 1. **Design System Consistency**
- **CSS Variable Utilization**: Proper use of design tokens (`--color-*`, `--spacing-*`, `--font-*`, etc.)
- **Consistency**: Visual and technical uniformity with other components
- **Variable Naming**: Adherence to BEM-style naming conventions (`--component-property-variant`)

### 2. **Modern CSS Feature Utilization**
- **@property**: Application status of type-safe CSS variables
- **CSS Nesting**: Appropriate nested structure and selector efficiency
- **Logical Properties**: Usage of `inline-size`, `block-size`, etc.
- **New Features**: Utilization of `:has()`, `@supports`, `@starting-style`, etc.

### 3. **Design Principles**
- **Single Responsibility**: Clarity of component responsibilities
- **Extensibility**: Design quality of variants (`--outline`, `--primary`, etc.)
- **Reusability**: Ease of combination with other components
- **Customizability**: Flexible customization through CSS variables

### 4. **Technical Implementation Quality**
- **Selector Efficiency**: Specificity management and performance consideration
- **State Management**: Proper implementation of `:hover`, `:focus`, `:disabled`, etc.
- **Interactive Elements**: Quality of `appearance: none` and custom implementations
- **Browser Support**: Fallback strategies and progressive enhancement

### 5. **Accessibility (WCAG 2.1 Level A Compliance)**

Please refer to [a11y.prompt.md](../../prompts/a11y.prompt.md).

### 6. 🎪 **Storybook Integration & Testing**
- **Properties**: Consistency with TypeScript type definitions
- **Variants**: Coverage of all states and variations
- **Documentation**: Quality of usage examples and guidelines
- **Accessibility Testing**: Validation status with Storybook addon-a11y
- **Interaction Testing**: Proper implementation of user interaction tests using `storybook/test`
- **Test Coverage**: Comprehensive testing of component states, user interactions, and edge cases
- **Test Quality**: Meaningful assertions that validate component behavior and accessibility

### 7. 🏭 **Production Readiness & Component Completeness**
- **Essential Features**: Coverage of industry-standard component functionality and common use cases
- **Edge Case Handling**: Proper behavior with empty states, long content, overflow scenarios
- **State Management**: Complete lifecycle support (loading, error, success, disabled states)
- **Integration Patterns**: Compatibility with form systems, validation, and common UI patterns
- **Performance**: Efficient rendering and minimal layout thrashing
- **Responsive Design**: Appropriate behavior across device sizes and orientations
- **Content Flexibility**: Support for various content types (text, HTML, components)
- **Developer Experience**: Intuitive API design and clear customization options

## Review Format

### Score by Evaluation Item (1-5 points)
- **Design System Consistency**: _/5
- **Modern CSS Utilization**: _/5
- **Component Design**: _/5
- **Technical Implementation Quality**: _/5
- **Accessibility**: _/5
- **Storybook Integration & Testing**: _/5
- **Production Readiness & Component Completeness**: _/5

### Specific Feedback
Provide the following for each perspective:
- ✅ **Strengths**: Specific examples and reasons
- ⚠️ **Improvement Suggestions**: Specific modification proposals and code examples
- ♿ **Accessibility Issues**: WCAG standard references and solutions
- 🎪 **Storybook & Testing Issues**: Interaction test improvements and coverage gaps
- 🏭 **Production Readiness Issues**: Missing features and edge cases for real-world usage
- 🚀 **Extension Ideas**: Future feature enhancement proposals

### Code Example Format
```css
/* Before */
.component { /* problematic code */ }

/* After */
.component {
  /* improved code */
  --component-property: value;
}
```

```typescript
/* Storybook Interaction Test Example */
export const Interactive: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await expect(button).toBeInTheDocument();
    await userEvent.click(button);
    await expect(button).toHaveClass('--active');
  }
};
```

Please provide the CSS component for review. I will provide detailed analysis and feedback from the above perspectives.
