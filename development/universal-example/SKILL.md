---
name: universal-example
version: 1.0.0
description: An example of universal Skill using template engine for multi-platform support
---

# Universal Example Skill

This Skill demonstrates how to write platform-agnostic content using the template engine.

## Platform Information

<!-- @if platform=claude -->

**Platform**: Claude Code

This is the full-featured version with detailed documentation and extensive examples.
You're seeing this because you're using Claude Code, which supports longer descriptions
and more comprehensive Skill content.

<!-- @endif -->

<!-- @if platform=codex -->

**Platform**: Codex

This is the optimized version for Codex with concise documentation.
Codex has a 500-character description limit, so this version is streamlined.

<!-- @endif -->

<!-- @if platform=claude,codex -->

## Common Features

These features work on both platforms:

### Feature 1: Code Generation

```typescript
function generateCode() {
  return 'Generated code works everywhere!'
}
```

### Feature 2: Template Support

Both platforms support the same template structure.

### Feature 3: Resource Management

Assets and references work consistently across platforms.

<!-- @endif -->

## Platform-Specific Content

<!-- @if platform=claude -->

### Claude-Only Features

Claude Code supports these advanced features:

#### Detailed Documentation

You can include extensive documentation in Claude Skills without worrying
about length limits. This allows for comprehensive guides, multiple examples,
and in-depth explanations.

#### Rich Examples

```typescript
// Example 1: Complex scenario
class AdvancedFeature {
  constructor(private config: Config) {}

  async process(data: Data): Promise<Result> {
    // Detailed implementation
    const validated = await this.validate(data)
    const transformed = this.transform(validated)
    return this.output(transformed)
  }
}

// Example 2: Integration
const feature = new AdvancedFeature(config)
const result = await feature.process(inputData)
console.log(result)
```

#### Reference Materials

- [Advanced Topics](references/advanced.md)
- [Best Practices](references/best-practices.md)
- [API Reference](references/api.md)
<!-- @endif -->

<!-- @if platform=codex -->

### Codex-Optimized Content

Quick reference for Codex users:

#### Key Points

- Feature A: Brief explanation
- Feature B: Quick example
- Feature C: Core usage

#### Quick Example

```typescript
// Essential code only
const result = quickProcess(data)
```

<!-- @endif -->

## Variables

This Skill is named **{{name}}** and is at version **{{version}}**.

<!-- @unless platform=codex -->

## Additional Resources

For more information:

- Check the examples directory
- Read the comprehensive guide
- Review the API documentation
<!-- @endunless -->

## Conclusion

<!-- @if platform=claude -->

Thank you for using this universal Skill! This example demonstrates how to
write content that adapts to different platforms while maintaining a single
source of truth. By using conditional blocks, you can provide rich content
for Claude and optimized content for Codex from the same SKILL.md file.

<!-- @endif -->

<!-- @if platform=codex -->

Thanks for using this universal Skill! This example shows platform-adaptive content.

<!-- @endif -->
