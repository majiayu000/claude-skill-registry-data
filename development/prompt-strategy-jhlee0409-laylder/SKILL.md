---
name: prompt-strategy
description: Develop and optimize AI prompt strategies for code generation. Use when creating new AI model strategies, optimizing prompts for Claude/GPT/Gemini/DeepSeek/Grok, or improving prompt quality. Includes model-specific optimization techniques.
allowed-tools: Read, Glob, Grep
---

# AI Prompt Strategy Skill

Visual Layout Builder의 AI 프롬프트 전략 개발을 위한 전문 스킬입니다. Claude, GPT, Gemini, DeepSeek, Grok 등 다양한 AI 모델에 최적화된 프롬프트를 생성합니다.

## When to Use

- 새로운 AI 모델 전략 클래스 추가
- 기존 프롬프트 품질 개선
- `lib/prompt-strategies/` 작업
- `lib/prompt-generator.ts` 수정
- `lib/prompt-templates.ts` 업데이트
- 프롬프트 검증 로직 개선
- AI 모델별 최적화 작업

## Supported AI Models

| Provider | Models | Strategy Class |
|----------|--------|----------------|
| **Anthropic** | Claude Sonnet 4.5, Sonnet 4, Opus 4, Haiku 3.5 | `ClaudeStrategy` |
| **OpenAI** | GPT-4.1, GPT-4 Turbo, GPT-4 | `GPTStrategy` |
| **Google** | Gemini 2.5 Pro, 2.0 Pro, 2.0 Flash | `GeminiStrategy` |
| **DeepSeek** | R1, V3, Coder V2 | `DeepSeekStrategy` |
| **xAI** | Grok 3, Grok 2 | `GrokStrategy` |

## Strategy Architecture

### Directory Structure

```
lib/prompt-strategies/
├── base-strategy.ts      # 기본 전략 클래스
├── claude-strategy.ts    # Claude 최적화
├── gpt-strategy.ts       # GPT 최적화
├── gemini-strategy.ts    # Gemini 최적화
├── deepseek-strategy.ts  # DeepSeek 최적화
├── grok-strategy.ts      # Grok 최적화
├── strategy-factory.ts   # Factory pattern
└── index.ts              # Public exports
```

### Base Strategy Class

```typescript
// lib/prompt-strategies/base-strategy.ts
export abstract class BasePromptStrategy {
  protected modelId: string
  protected modelCapabilities: ModelCapabilities

  abstract generatePrompt(
    schema: LaydlerSchema,
    framework: string,
    cssSolution: string,
    options?: PromptOptions
  ): GenerationResult

  protected buildSystemPrompt(): string {
    // Common system prompt structure
  }

  protected buildComponentSection(components: Component[]): string {
    // Component specification format
  }

  protected buildLayoutSection(
    components: Component[],
    breakpoints: Breakpoint[],
    layouts: Record<string, LayoutConfig>
  ): string {
    // Layout specification with canvas grid info
  }

  protected estimateTokens(prompt: string): number {
    // Token estimation algorithm
  }
}
```

## Creating a New Model Strategy

### Step 1: Create Strategy Class

```typescript
// lib/prompt-strategies/new-model-strategy.ts
import { BasePromptStrategy } from './base-strategy'
import type { LaydlerSchema, GenerationResult, PromptOptions } from '@/types'

export class NewModelStrategy extends BasePromptStrategy {
  constructor(modelId: string) {
    super()
    this.modelId = modelId
    this.modelCapabilities = this.getModelCapabilities(modelId)
  }

  generatePrompt(
    schema: LaydlerSchema,
    framework: string,
    cssSolution: string,
    options?: PromptOptions
  ): GenerationResult {
    const sections: string[] = []

    // 1. System prompt (model-specific optimization)
    sections.push(this.buildSystemPrompt(options))

    // 2. Component specifications
    sections.push(this.buildComponentSection(schema.components))

    // 3. Layout with canvas grid info
    sections.push(this.buildLayoutSection(
      schema.components,
      schema.breakpoints,
      schema.layouts
    ))

    // 4. Model-specific instructions
    sections.push(this.buildModelSpecificInstructions(options))

    const prompt = sections.join('\n\n---\n\n')

    return {
      success: true,
      prompt,
      estimatedTokens: this.estimateTokens(prompt)
    }
  }

  private buildModelSpecificInstructions(options?: PromptOptions): string {
    // Model-specific optimizations
    if (this.modelCapabilities.supportsChainOfThought && options?.chainOfThought) {
      return `
## Reasoning Process

Think through each component step by step:
1. Analyze the semantic tag and its purpose
2. Consider the positioning strategy
3. Plan the layout implementation
4. Generate the code

Show your reasoning before providing the final code.
`
    }
    return ''
  }
}
```

### Step 2: Register in Factory

```typescript
// lib/prompt-strategies/strategy-factory.ts
import { NewModelStrategy } from './new-model-strategy'

export function createPromptStrategy(modelId: string): BasePromptStrategy {
  const provider = getProviderFromModelId(modelId)

  switch (provider) {
    case 'claude':
      return new ClaudeStrategy(modelId)
    case 'gpt':
      return new GPTStrategy(modelId)
    case 'gemini':
      return new GeminiStrategy(modelId)
    case 'deepseek':
      return new DeepSeekStrategy(modelId)
    case 'grok':
      return new GrokStrategy(modelId)
    case 'new-model':  // Add new model
      return new NewModelStrategy(modelId)
    default:
      return new BasePromptStrategy(modelId)
  }
}
```

### Step 3: Add Model Registry Entry

```typescript
// lib/ai-model-registry.ts
export const AI_MODELS: AIModelInfo[] = [
  // ... existing models
  {
    id: 'new-model-v1',
    name: 'New Model V1',
    provider: 'new-provider',
    contextWindow: 128000,
    maxOutput: 8192,
    capabilities: {
      supportsChainOfThought: true,
      supportsExtendedThinking: false,
      codeSpecialization: 'general',
      costTier: 'medium'
    }
  }
]
```

## Model-Specific Optimizations

### Claude Optimization

```typescript
// Extended thinking support for complex layouts
if (options?.optimizationLevel === 'quality') {
  systemPrompt += `
<thinking>
Before generating code, analyze:
1. Component hierarchy and relationships
2. Responsive behavior across breakpoints
3. CSS Grid vs Flexbox decision points
4. Accessibility requirements
</thinking>
`
}
```

### GPT Optimization

```typescript
// O1 reasoning model support
if (modelId.includes('o1')) {
  // No system prompt for o1 models
  // Use user message with clear structure
  return this.buildUserOnlyPrompt(schema, framework, cssSolution)
}
```

### Gemini Optimization

```typescript
// Structured output preference
instructions += `
## Output Format

Return the code in a structured format:
\`\`\`json
{
  "components": [
    {
      "name": "ComponentName",
      "code": "// React component code"
    }
  ],
  "layout": "// Main layout component"
}
\`\`\`
`
```

### DeepSeek Optimization

```typescript
// Code-focused models (Coder V2)
if (modelId.includes('coder')) {
  systemPrompt = `You are an expert React/TypeScript developer.
Generate production-ready code following these specifications exactly.
Prioritize code correctness and TypeScript type safety.`
}
```

## Prompt Quality Guidelines

### DO Include

```markdown
## Component Specifications

For each component, specify:
- **Semantic Tag**: The HTML5 semantic element
- **Positioning**: CSS positioning strategy
- **Layout**: Internal layout (flex/grid/container)
- **Canvas Position**: Grid coordinates for visual layout

## Visual Layout (Canvas Grid)

The canvas represents the visual arrangement:
- Grid: 12 columns × 8 rows (desktop)
- Each component has x, y, width, height in grid units
- Use CSS Grid for 2D positioning
- Respect the visual arrangement in generated code
```

### DO NOT Include

```markdown
❌ DO NOT Generate:
- Theme colors (bg-blue, bg-purple, text-white, gradients)
- Shadows (shadow-sm, shadow-md, shadow-lg)
- Rounded corners (rounded-lg, rounded-xl)
- Demo content or placeholder text with specific styling
```

### Layout-Only Philosophy

```markdown
## Layout-Only Output

Generate pure structural code:
✅ Layout classes (flex, grid, container)
✅ Positioning classes (fixed, sticky, static)
✅ Spacing utilities (p-4, gap-6, m-auto)
✅ Border for structure (border-b, border-gray-300)
✅ Responsive utilities (hidden lg:block)

❌ NO theme colors, shadows, or decorative styling
```

## Canvas Grid to CSS Grid Conversion

```typescript
// lib/canvas-to-grid.ts
export function canvasToGridPositions(
  components: Component[],
  breakpoint: string,
  gridCols: number,
  gridRows: number
): GridPosition[] {
  return components
    .filter(c => hasCanvasLayout(c, breakpoint))
    .map(c => {
      const layout = getCanvasLayoutForBreakpoint(c, breakpoint)!
      return {
        componentId: c.id,
        // CSS Grid uses 1-based indexing
        gridColumn: `${layout.x + 1} / ${layout.x + layout.width + 1}`,
        gridRow: `${layout.y + 1} / ${layout.y + layout.height + 1}`,
        gridArea: `${layout.y + 1} / ${layout.x + 1} / ${layout.y + layout.height + 1} / ${layout.x + layout.width + 1}`
      }
    })
}
```

## Visual Layout Description

```typescript
// lib/visual-layout-descriptor.ts
export function describeVisualLayout(
  components: Component[],
  breakpoint: string,
  gridCols: number,
  gridRows: number
): VisualLayoutDescription {
  return {
    summary: `${gridCols}-column × ${gridRows}-row grid system with ${components.length} components`,
    rowByRow: generateRowByRowDescription(components, breakpoint),
    spatialRelationships: analyzeSpatialRelationships(components, breakpoint),
    implementationHints: generateImplementationHints(components, breakpoint)
  }
}
```

## Prompt Validation

### Required Validations

```typescript
// lib/prompt-bp-validator.ts
export function validatePromptBreakpoints(
  prompt: string,
  schema: LaydlerSchema
): ValidationResult {
  const issues: ValidationIssue[] = []

  // 1. Check all breakpoints are mentioned
  for (const bp of schema.breakpoints) {
    if (!prompt.includes(bp.name)) {
      issues.push({
        code: 'MISSING_BREAKPOINT_IN_PROMPT',
        message: `Breakpoint "${bp.name}" not mentioned in prompt`
      })
    }
  }

  // 2. Check canvas layout info included
  if (!prompt.includes('grid') && !prompt.includes('Grid')) {
    issues.push({
      code: 'MISSING_GRID_INFO',
      message: 'Canvas grid layout information not included'
    })
  }

  return {
    valid: issues.length === 0,
    issues
  }
}
```

## Usage Example

```typescript
import { createPromptStrategy } from '@/lib/prompt-strategies'
import { generatePrompt } from '@/lib/prompt-generator'

// Method 1: Using strategy directly
const strategy = createPromptStrategy('claude-sonnet-4.5')
const result = strategy.generatePrompt(schema, 'react', 'tailwind', {
  optimizationLevel: 'quality',
  chainOfThought: true,
  verbosity: 'detailed'
})

// Method 2: Using main generator with links
const result = generatePrompt(
  schema,
  'react',
  'tailwind',
  componentLinks  // Optional cross-breakpoint links
)
```

## Testing New Strategies

```typescript
// scripts/test-new-model-strategy.ts
import { createPromptStrategy } from '@/lib/prompt-strategies'
import { sampleSchemas } from '@/lib/sample-data'

const strategy = createPromptStrategy('new-model-v1')

for (const [name, schema] of Object.entries(sampleSchemas)) {
  console.log(`Testing ${name}...`)
  const result = strategy.generatePrompt(schema, 'react', 'tailwind')

  if (result.success) {
    console.log(`✅ ${name}: ${result.estimatedTokens} tokens`)
  } else {
    console.log(`❌ ${name}: ${result.errors?.join(', ')}`)
  }
}
```

## Reference Files

- `lib/prompt-strategies/` - 모든 전략 클래스
- `lib/prompt-generator.ts` - 메인 생성기
- `lib/prompt-templates.ts` - 템플릿 정의
- `lib/ai-model-registry.ts` - 모델 메타데이터
- `lib/canvas-to-grid.ts` - Canvas→CSS Grid 변환
- `lib/visual-layout-descriptor.ts` - 자연어 설명 생성
- `docs/AI_MODELS_GUIDE.md` - AI 모델 가이드
