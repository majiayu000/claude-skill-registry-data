---
name: new-tool-development
description: Guide for creating new tools in the SuperTool application. Use this when asked to add a new tool, create a tool page, or implement tool functionality.
license: MIT
---

# New Tool Development Guide

This skill guides you through creating a new tool in the SuperTool application following the project's architecture and standards.

## Prerequisites

Before starting, ensure you understand:
- Next.js 15 App Router with React 19
- Panda CSS for styling (NOT Tailwind for tool pages)
- Vitest browser testing requirements
- The project requires **>= 95% test coverage**

## Step-by-Step Tool Creation Process

### 1. Define Tool Metadata

First, add your tool to `lib/tools.ts`:

```typescript
{
  id: 'your-tool-id',
  name: 'Your Tool Name',
  category: 'appropriate-category', // Utilities, Converters, Generators, Productivity, etc.
  description: 'Brief description (50-80 chars)',
  icon: AppropriateIcon, // From lucide-react
  path: '/tools/your-tool-id',
  featured: false,
  new: true, // Remove after a few weeks
  keywords: ['keyword1', 'keyword2', 'keyword3']
}
```

### 2. Create Tool Directory Structure

```bash
mkdir -p app/tools/your-tool-id
mkdir -p app/tools/your-tool-id/__tests__
```

### 3. Create the Tool Page Component

File: `app/tools/your-tool-id/page.tsx`

**CRITICAL**: Must use Panda CSS, NOT Tailwind utilities.

```typescript
'use client'

import { useState } from 'react'
import { css } from '@/styled-system/css'
import { Button } from '@/components/ui/button'
import { trackToolEvent } from '@/lib/analytics'

export default function YourToolPage() {
  const [state, setState] = useState<YourStateType>({})

  // Handle user actions
  const handleAction = () => {
    try {
      // Your logic here
      
      // REQUIRED: Track analytics (anonymize PII)
      trackToolEvent('your-tool-id', 'action_name', {
        // metadata (NO PII!)
      })
    } catch (error) {
      console.error('Error:', error)
      // Show user-friendly error
    }
  }

  return (
    <main className={css({
      mx: 'auto',
      maxW: '7xl',
      w: 'full',
      px: { base: '4', sm: '6', md: '8' },
      py: { base: '6', sm: '8', md: '10' },
      spaceY: { base: '6', sm: '8', md: '10' }
    })}>
      {/* Tool Header */}
      <div className={css({ textAlign: 'center', spaceY: '4' })}>
        <h1 className={css({
          fontSize: { base: '3xl', sm: '4xl', md: '5xl' },
          fontWeight: 'bold',
          bgGradient: 'to-r',
          gradientFrom: 'purple.400',
          gradientTo: 'pink.600',
          bgClip: 'text'
        })}>
          Your Tool Name
        </h1>
        <p className={css({
          fontSize: { base: 'md', sm: 'lg' },
          color: 'gray.400'
        })}>
          Your tool description
        </p>
      </div>

      {/* Tool Content - Use glassmorphism card */}
      <div className={css({
        bg: 'rgba(255, 255, 255, 0.05)',
        backdropFilter: 'blur(10px)',
        borderRadius: 'xl',
        border: '1px solid',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        p: { base: '6', sm: '8' },
        spaceY: '6'
      })}>
        {/* Your tool UI here */}
      </div>
    </main>
  )
}
```

### 4. Create Metadata File

File: `app/tools/your-tool-id/metadata.ts`

```typescript
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Your Tool Name - SuperTool',
  description: 'Detailed description for SEO (150-160 chars)',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  openGraph: {
    title: 'Your Tool Name',
    description: 'Your description',
    type: 'website',
  },
}
```

### 5. Create Comprehensive Tests

File: `app/tools/your-tool-id/__tests__/page.test.tsx`

**CRITICAL**: Must achieve >= 95% coverage.

```typescript
import { describe, expect, it, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import YourToolPage from '../page'

// Mock analytics
vi.mock('@/lib/analytics', () => ({
  trackToolEvent: vi.fn(),
}))

describe('YourToolPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the tool page', () => {
    render(<YourToolPage />)
    expect(screen.getByText('Your Tool Name')).toBeInTheDocument()
  })

  it('handles user input', async () => {
    const user = userEvent.setup()
    render(<YourToolPage />)
    
    const input = screen.getByRole('textbox')
    await user.type(input, 'test input')
    
    expect(input).toHaveValue('test input')
  })

  it('processes action successfully', async () => {
    const user = userEvent.setup()
    render(<YourToolPage />)
    
    // Trigger action
    const button = screen.getByRole('button', { name: /action/i })
    await user.click(button)
    
    // Verify results
    await waitFor(() => {
      expect(screen.getByText(/expected result/i)).toBeInTheDocument()
    })
  })

  it('handles errors gracefully', async () => {
    // Test error scenarios
  })

  it('tracks analytics events', async () => {
    const { trackToolEvent } = await import('@/lib/analytics')
    const user = userEvent.setup()
    render(<YourToolPage />)
    
    const button = screen.getByRole('button')
    await user.click(button)
    
    expect(trackToolEvent).toHaveBeenCalledWith('your-tool-id', 'action_name', expect.any(Object))
  })
})
```

### 6. Update Documentation

Create: `docs/YOUR_TOOL_IMPLEMENTATION.md`

Document:
- Tool purpose and features
- Implementation details
- API endpoints (if any)
- Testing approach
- Known limitations

### 7. Run Quality Checks

```bash
# Format and lint
pnpm lint

# Type check
pnpm exec tsc --noEmit

# Run tests with coverage
CI=true pnpm test run --coverage

# Verify >= 95% coverage for your new files
# Build to verify no issues
pnpm build
```

## Critical Patterns to Follow

### Styling Requirements

1. **MUST use Panda CSS** - Use `css()` from `@/styled-system/css`
2. **Glassmorphism** - Use backdrop-blur and transparent backgrounds
3. **Responsive** - Always use responsive values: `{ base: 'sm', md: 'lg' }`
4. **Mobile-first** - Touch targets >= 44px, stack vertically on mobile
5. **Grid layouts** - Use valid values: `gridTemplateColumns: { base: '1fr', sm: 'repeat(2, 1fr)' }`

### Analytics Requirements

1. Track ALL user interactions with `trackToolEvent()`
2. NEVER track PII - anonymize file names, URLs, user data
3. Use consistent event naming: `tool-id`, `action_name`, `{metadata}`

### Testing Requirements

1. **>= 95% coverage** is MANDATORY (CI will fail otherwise)
2. Test all user interactions
3. Test error scenarios
4. Mock external dependencies (fetch, Supabase, OpenAI, etc.)
5. Use `beforeEach()` to clear mocks

### Error Handling

1. Always wrap async operations in try/catch
2. Show user-friendly error messages (toast notifications)
3. Log errors to console for debugging
4. Return proper HTTP status codes for API routes (400, 404, 409, 500)

## API Routes (if needed)

If your tool needs a backend API:

File: `app/api/your-endpoint/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate input
    if (!body.requiredField) {
      return NextResponse.json(
        { error: 'Missing required field' },
        { status: 400 }
      )
    }
    
    // Process request
    const result = await processData(body)
    
    return NextResponse.json({ data: result })
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

And create comprehensive API tests:

```typescript
// app/api/your-endpoint/__tests__/route.test.ts
import { describe, expect, it, vi } from 'vitest'
import { POST } from '../route'

describe('POST /api/your-endpoint', () => {
  it('returns 400 for missing fields', async () => {
    const request = new Request('http://localhost/api/your-endpoint', {
      method: 'POST',
      body: JSON.stringify({}),
    })
    
    const response = await POST(request as any)
    expect(response.status).toBe(400)
  })
  
  // Test all scenarios...
})
```

## Reference Examples

- **Canonical styling**: `app/tools/unit-converter/page.tsx`
- **API with tests**: `app/api/shorten/route.ts` and tests
- **Full guidelines**: `.github/copilot-instructions.md`

## Checklist Before Submitting

- [ ] Tool added to `lib/tools.ts`
- [ ] Page component uses Panda CSS (NOT Tailwind)
- [ ] Analytics tracking implemented (no PII)
- [ ] Comprehensive tests written
- [ ] Test coverage >= 95%
- [ ] Type checking passes (`tsc --noEmit`)
- [ ] Linting passes (`pnpm lint`)
- [ ] Build succeeds (`pnpm build`)
- [ ] Documentation created
- [ ] Mobile responsive design verified
- [ ] Glassmorphism styling applied
- [ ] Error handling implemented
- [ ] Accessibility considered (ARIA labels, keyboard nav)
