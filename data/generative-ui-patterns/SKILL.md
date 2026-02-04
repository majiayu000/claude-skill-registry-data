---
name: generative-ui-patterns
description: Generative UI implementation patterns for AI SDK RSC including server-side streaming components, dynamic UI generation, and client-server coordination. Use when implementing generative UI, building AI SDK RSC, creating streaming components, or when user mentions generative UI, React Server Components, dynamic UI, AI-generated interfaces, or server-side streaming.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Generative UI Patterns

**Purpose:** Provide reusable templates, patterns, and validation scripts for implementing Generative UI with Vercel AI SDK RSC (React Server Components).

**Activation Triggers:**
- Building generative UI interfaces
- Implementing AI SDK RSC patterns
- Creating server-side streaming components
- Dynamic UI generation based on AI responses
- Client-server component coordination
- Next.js App Router RSC integration

**Key Resources:**
- `templates/server-action-pattern.tsx` - Server action template for AI RSC
- `templates/streaming-component.tsx` - Streaming component pattern
- `templates/client-wrapper.tsx` - Client component wrapper pattern
- `templates/route-handler.ts` - API route handler for streaming UI
- `scripts/validate-rsc-setup.sh` - Validate Next.js RSC configuration
- `scripts/generate-ui-component.sh` - Generate UI component from schema
- `examples/` - Real-world generative UI implementations

## Core Patterns

### 1. Server Action Pattern (AI SDK RSC)

**When to use:** Next.js App Router with React Server Components

**Template:** `templates/server-action-pattern.tsx`

**Pattern:**
```typescript
'use server'
import { streamUI } from 'ai/rsc'
import { openai } from '@ai-sdk/openai'

export async function generateUI(prompt: string) {
  const result = await streamUI({
    model: openai('gpt-4')
    prompt
    text: ({ content }) => <p>{content}</p>
    tools: {
      // Tool definitions for dynamic UI generation
    }
  })

  return result.value
}
```

**Key features:**
- Server-side only execution (security)
- Streaming UI components to client
- Tool-based dynamic component selection
- Type-safe component generation

### 2. Streaming Component Pattern

**When to use:** Need real-time UI updates during AI generation

**Template:** `templates/streaming-component.tsx`

**Pattern:**
- Server component streams UI chunks
- Client component receives and renders
- Suspense boundaries for loading states
- Error boundaries for failure handling

### 3. Client-Server Coordination

**When to use:** Complex interactions between client and server components

**Template:** `templates/client-wrapper.tsx`

**Pattern:**
- Client components handle interactivity
- Server components handle AI calls
- Proper hydration boundaries
- State management across boundary

## Implementation Workflow

### Step 1: Validate Next.js Setup

```bash
# Check Next.js version and App Router setup
./scripts/validate-rsc-setup.sh
```

**Checks:**
- Next.js 13.4+ (App Router required)
- React 18+ (Server Components support)
- `app/` directory exists
- TypeScript configuration for RSC

### Step 2: Choose Component Pattern

**Decision tree:**
- Simple text streaming → Use basic streamUI with text callback
- Dynamic UI (charts, cards, forms) → Use tools with component mapping
- Complex multi-step → Use workflow with multiple streamUI calls
- Interactive elements → Use client wrapper pattern

### Step 3: Generate Component Template

```bash
# Generate component from pattern
./scripts/generate-ui-component.sh <pattern-type> <component-name>

# Examples:
./scripts/generate-ui-component.sh stream-text MessageCard
./scripts/generate-ui-component.sh dynamic-tool ChartGenerator
./scripts/generate-ui-component.sh workflow MultiStepForm
```

### Step 4: Implement Server Action

**Use template:** `templates/server-action-pattern.tsx`

**Customize:**
1. Define tools for dynamic component selection
2. Map tool outputs to React components
3. Add error handling and fallbacks
4. Configure streaming options

### Step 5: Add Client Wrapper (if needed)

**Use template:** `templates/client-wrapper.tsx`

**For:**
- User interactions (buttons, forms)
- Client-side state management
- Browser APIs (localStorage, etc.)
- Animations and transitions

## Component Mapping Strategy

### Tool-Based Dynamic UI

**Pattern:**
```typescript
const tools = {
  showChart: tool({
    description: 'Display data as chart'
    parameters: z.object({
      data: z.array(z.number())
      type: z.enum(['bar', 'line', 'pie'])
    })
    generate: async ({ data, type }) => {
      return <ChartComponent data={data} type={type} />
    }
  })
  showTable: tool({
    description: 'Display data as table'
    parameters: z.object({
      rows: z.array(z.record(z.string()))
    })
    generate: async ({ rows }) => {
      return <TableComponent rows={rows} />
    }
  })
}
```

**Key principle:** Let AI choose appropriate UI component based on data

## Error Handling & Fallbacks

### Pattern: Graceful Degradation

```typescript
const result = await streamUI({
  // ... config
  onError: (error) => {
    return <ErrorBoundary error={error} />
  }
  fallback: <LoadingSpinner />
})
```

**Best practices:**
- Always provide fallback component
- Handle streaming interruptions
- Validate tool parameters
- Sanitize AI-generated content

## Performance Optimization

### 1. Component Code Splitting

Use dynamic imports for heavy components:
```typescript
const HeavyChart = dynamic(() => import('./HeavyChart'))
```

### 2. Streaming Chunks

Control chunk size for optimal UX:
```typescript
const result = await streamUI({
  // ... config
  experimental_streamChunking: true
})
```

### 3. Caching Strategy

Cache static UI components:
```typescript
export const revalidate = 3600 // 1 hour
```

## Security Considerations

### Server-Only Code

**Critical:** Never expose server actions to client

```typescript
// ✅ Good: server action
'use server'
export async function generateUI() { /* ... */ }

// ❌ Bad: client-accessible
export async function generateUI() { /* ... */ }
```

### Content Sanitization

Always sanitize AI-generated content:
```typescript
import DOMPurify from 'isomorphic-dompurify'

const sanitized = DOMPurify.sanitize(aiContent)
```

## Framework Integration

### Next.js App Router

**File structure:**
```
app/
  actions/
    generate-ui.ts       # Server actions
  components/
    ui/
      generated/         # Generated UI components
    client-wrapper.tsx   # Client components
  api/
    stream-ui/
      route.ts           # Alternative API route pattern
```

### TypeScript Configuration

**Required:** Proper RSC types

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "jsx": "preserve"
    "lib": ["dom", "dom.iterable", "esnext"]
    "module": "esnext"
    "moduleResolution": "bundler"
  }
}
```

## Testing Strategy

### Unit Testing Server Actions

```typescript
import { generateUI } from './actions'

test('generates UI from prompt', async () => {
  const ui = await generateUI('Show weather chart')
  expect(ui).toMatchSnapshot()
})
```

### Integration Testing Streaming

Use testing-patterns skill for comprehensive streaming tests

## Common Patterns

### 1. Multi-Step Form Generation

**Use case:** AI generates form fields dynamically

**Template:** `examples/multi-step-form.tsx`

### 2. Data Visualization

**Use case:** AI selects appropriate chart type

**Template:** `examples/chart-generator.tsx`

### 3. Dashboard Generation

**Use case:** AI creates dashboard widgets

**Template:** `examples/dashboard-generator.tsx`

### 4. Content Cards

**Use case:** AI generates content in card layouts

**Template:** `examples/content-cards.tsx`

## Resources

**Scripts:**
- `validate-rsc-setup.sh` - Verify Next.js and RSC configuration
- `generate-ui-component.sh` - Scaffold component from pattern

**Templates:**
- `server-action-pattern.tsx` - Complete server action template
- `streaming-component.tsx` - Streaming component pattern
- `client-wrapper.tsx` - Client component wrapper
- `route-handler.ts` - API route alternative pattern

**Examples:**
- `multi-step-form.tsx` - Complete multi-step form implementation
- `chart-generator.tsx` - Dynamic chart generation
- `dashboard-generator.tsx` - Full dashboard example
- `content-cards.tsx` - Card-based content layout

---

**Supported Frameworks:** Next.js 13.4+ (App Router only)
**SDK Version:** Vercel AI SDK 5+ with RSC support
**React Version:** React 18+ (Server Components)

**Best Practice:** Always start with `validate-rsc-setup.sh` to ensure environment compatibility
