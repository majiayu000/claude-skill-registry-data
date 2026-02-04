---
name: gemini-ai
description: Integrates Gemini AI for content generation. Use when adding AI features, generating project descriptions, implementing rate limiting, or working with geminiService.ts. Includes prompting guidelines and error handling.
---

# Gemini AI Integration Skill

## Instructions

1. Server functions in `src/services/geminiService.ts`
2. Use `'use server'` directive
3. Return structured JSON via schema
4. Apply rate limiting (3/draft, 10/day)
5. Korean language with "Chef" persona

## Existing Functions

- `generateProjectContent(draft)` → `{ shortDescription, description, tags }`
- `refineDescription(rawDescription)` → refined markdown

## AI Rate Limits
- 3 generations per draft
- 10 generations per day per user
- 5-second cooldown between requests

## Prompting Style

- Role: "SideDish 플랫폼의 수석 에디터"
- Language: Korean (자연스러운 해요체)
- Culinary metaphors: subtle, not forced
- Banned: "최고의", "혁신적인", "획기적인"

## Usage in Components

```tsx
import { generateProjectContent } from '@/services/geminiService'
import { canGenerate, recordGeneration } from '@/lib/aiLimitService'

if (!canGenerate(draftId)) {
  toast.error('AI 생성 횟수를 초과했습니다.')
  return
}

const result = await generateProjectContent(draft)
recordGeneration(draftId)
```

For complete templates, error handling, and UI components, see [reference.md](reference.md).
