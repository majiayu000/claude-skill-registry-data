---
name: analytics-tracking
description: Guide for implementing analytics tracking in SuperTool. Use this when adding analytics events, tracking user actions, or ensuring privacy compliance.
license: MIT
---

# Analytics Tracking Guide

This skill ensures proper analytics implementation while maintaining user privacy.

## Core Principle: Privacy-First Analytics

**CRITICAL**: NEVER track personally identifiable information (PII).

### What NOT to Track

- ❌ User names, emails, IP addresses
- ❌ Actual file names or file contents
- ❌ Full URLs with potential sensitive data
- ❌ User input text/data
- ❌ Authentication tokens or credentials
- ❌ Specific error messages with user data

### What TO Track

- ✅ Tool usage counts
- ✅ Feature interactions (anonymized)
- ✅ File types (not names): "image/png", "text/csv"
- ✅ File sizes in ranges: "<1MB", "1-10MB", ">10MB"
- ✅ Success/failure rates (without details)
- ✅ Performance metrics (timing)
- ✅ Generic error types: "validation_error", "network_error"

## Analytics Function

```typescript
import { trackToolEvent } from '@/lib/analytics'

// Function signature
trackToolEvent(
  toolId: string,      // Tool identifier from tools.ts
  action: string,      // Action name (snake_case)
  metadata?: object    // Optional metadata (NO PII!)
)
```

## Implementation Pattern

### 1. Import the Function

```typescript
import { trackToolEvent } from '@/lib/analytics'
```

### 2. Track User Actions

```typescript
'use client'

export default function ToolPage() {
  const handleProcess = async () => {
    try {
      // Process user action
      const result = await processData(input)
      
      // ✅ Track success (anonymized metadata)
      trackToolEvent('tool-id', 'process_success', {
        fileType: file.type,
        fileSizeRange: getFileSizeRange(file.size),
        processingTime: Date.now() - startTime
      })
      
    } catch (error) {
      // ✅ Track error (generic type only)
      trackToolEvent('tool-id', 'process_error', {
        errorType: error instanceof ValidationError ? 'validation' : 'unknown'
      })
    }
  }
  
  return (
    // Component JSX
  )
}
```

## Common Event Patterns

### Tool Page View

```typescript
// Track when tool is loaded (in useEffect)
useEffect(() => {
  trackToolEvent('tool-id', 'page_view')
}, [])
```

### File Upload

```typescript
const handleFileUpload = (file: File) => {
  trackToolEvent('tool-id', 'file_uploaded', {
    fileType: file.type,
    fileSizeRange: getFileSizeRange(file.size),
    // ❌ DON'T: fileName: file.name
  })
}

// Helper to anonymize file size
function getFileSizeRange(bytes: number): string {
  if (bytes < 1024 * 1024) return '<1MB'
  if (bytes < 10 * 1024 * 1024) return '1-10MB'
  if (bytes < 50 * 1024 * 1024) return '10-50MB'
  return '>50MB'
}
```

### Form Submission

```typescript
const handleSubmit = async (formData: FormData) => {
  const startTime = Date.now()
  
  try {
    const result = await submitForm(formData)
    
    trackToolEvent('tool-id', 'form_submitted', {
      fieldCount: formData.entries().length,
      processingTime: Date.now() - startTime
      // ❌ DON'T: formValues: Object.fromEntries(formData)
    })
  } catch (error) {
    trackToolEvent('tool-id', 'form_submission_failed', {
      errorType: 'network_error'
    })
  }
}
```

### Export/Download

```typescript
const handleExport = (format: string) => {
  trackToolEvent('tool-id', 'export_initiated', {
    format: format,
    itemCount: data.length
    // ❌ DON'T: fileName: exportFileName
  })
}
```

### Feature Toggle

```typescript
const handleToggleFeature = (featureName: string, enabled: boolean) => {
  trackToolEvent('tool-id', 'feature_toggled', {
    feature: featureName,
    enabled: enabled
  })
}
```

### API Call

```typescript
const callAPI = async (endpoint: string) => {
  const startTime = Date.now()
  
  try {
    const response = await fetch(endpoint)
    
    trackToolEvent('tool-id', 'api_call_success', {
      endpoint: endpoint.replace(/\/[^/]+$/, '/:id'), // Anonymize IDs
      statusCode: response.status,
      responseTime: Date.now() - startTime
    })
  } catch (error) {
    trackToolEvent('tool-id', 'api_call_failed', {
      endpoint: endpoint.replace(/\/[^/]+$/, '/:id'),
      errorType: 'network_error'
    })
  }
}
```

### Copy to Clipboard

```typescript
const handleCopy = () => {
  navigator.clipboard.writeText(result)
  
  trackToolEvent('tool-id', 'copy_to_clipboard', {
    resultLength: result.length > 1000 ? 'large' : 'small'
    // ❌ DON'T: copiedText: result
  })
}
```

### Settings Change

```typescript
const handleSettingChange = (setting: string, value: unknown) => {
  trackToolEvent('tool-id', 'setting_changed', {
    setting: setting,
    valueType: typeof value
    // ❌ DON'T: value: value
  })
}
```

### Tab/Section Switch

```typescript
const handleTabChange = (tabName: string) => {
  trackToolEvent('tool-id', 'tab_changed', {
    tab: tabName
  })
}
```

### Search Query

```typescript
const handleSearch = (query: string) => {
  trackToolEvent('tool-id', 'search_performed', {
    queryLength: query.length,
    hasSpecialChars: /[^a-zA-Z0-9\s]/.test(query)
    // ❌ DON'T: query: query
  })
}
```

## Event Naming Conventions

Use **snake_case** for action names:

```typescript
// ✅ GOOD
'file_uploaded'
'export_initiated'
'form_submitted'
'process_success'
'api_call_failed'

// ❌ BAD
'fileUploaded'
'ExportInitiated'
'Form Submitted'
'processSuccess'
```

## Metadata Best Practices

### Structure Metadata Objects

```typescript
// ✅ GOOD - Structured, anonymized data
trackToolEvent('json-beautifier', 'format_success', {
  inputSize: '<1KB',
  outputFormat: 'indented',
  indentSize: 2,
  processingTime: 123
})

// ❌ BAD - Unstructured or contains PII
trackToolEvent('json-beautifier', 'format_success', {
  data: jsonData,  // Don't send actual data
  user: userId     // Don't send user identifiers
})
```

### Keep Metadata Concise

```typescript
// ✅ GOOD - Essential info only
trackToolEvent('image-optimizer', 'optimization_complete', {
  originalSize: '5-10MB',
  optimizedSize: '1-5MB',
  compressionRatio: 0.7,
  format: 'jpeg'
})

// ❌ BAD - Too verbose or sensitive
trackToolEvent('image-optimizer', 'optimization_complete', {
  originalFileName: file.name,
  originalPath: file.path,
  optimizedFileName: output.name,
  fullMetadata: image.metadata
})
```

## Performance Tracking

Track performance metrics to identify bottlenecks:

```typescript
const startTime = performance.now()

try {
  const result = await expensiveOperation()
  
  const duration = performance.now() - startTime
  
  trackToolEvent('tool-id', 'operation_complete', {
    duration: Math.round(duration),
    success: true
  })
} catch (error) {
  const duration = performance.now() - startTime
  
  trackToolEvent('tool-id', 'operation_complete', {
    duration: Math.round(duration),
    success: false,
    errorType: 'processing_error'
  })
}
```

## A/B Testing Support

Track which variant users see:

```typescript
const variant = getABTestVariant('feature-x')

trackToolEvent('tool-id', 'feature_viewed', {
  variant: variant, // 'control' or 'treatment'
  feature: 'feature-x'
})
```

## Error Categorization

Categorize errors generically:

```typescript
const categorizeError = (error: Error): string => {
  if (error instanceof ValidationError) return 'validation'
  if (error instanceof NetworkError) return 'network'
  if (error instanceof TimeoutError) return 'timeout'
  return 'unknown'
}

trackToolEvent('tool-id', 'error_occurred', {
  errorCategory: categorizeError(error),
  // ❌ DON'T: errorMessage: error.message
})
```

## Testing Analytics

Mock analytics in tests:

```typescript
import { describe, expect, it, vi } from 'vitest'
import { trackToolEvent } from '@/lib/analytics'

// Mock the analytics module
vi.mock('@/lib/analytics', () => ({
  trackToolEvent: vi.fn(),
}))

describe('Component', () => {
  it('tracks user action', async () => {
    const { trackToolEvent } = await import('@/lib/analytics')
    
    // Trigger action
    await user.click(button)
    
    // Verify tracking
    expect(trackToolEvent).toHaveBeenCalledWith(
      'tool-id',
      'action_name',
      expect.objectContaining({
        // Expected metadata
      })
    )
  })
  
  it('does not track PII', async () => {
    const { trackToolEvent } = await import('@/lib/analytics')
    
    await user.type(input, 'sensitive data')
    await user.click(button)
    
    // Verify no sensitive data in any call
    const calls = vi.mocked(trackToolEvent).mock.calls
    calls.forEach(call => {
      const metadata = call[2]
      expect(JSON.stringify(metadata)).not.toContain('sensitive data')
    })
  })
})
```

## Analytics Dashboard Metrics

Track metrics useful for dashboard:

```typescript
// Daily Active Tools
trackToolEvent('tool-id', 'page_view')

// Feature Adoption
trackToolEvent('tool-id', 'feature_used', { feature: 'export-pdf' })

// Conversion Rate
trackToolEvent('tool-id', 'conversion', { from: 'view', to: 'action' })

// User Engagement
trackToolEvent('tool-id', 'session_duration', { duration: sessionTime })

// Error Rate
trackToolEvent('tool-id', 'error_occurred', { errorType: 'validation' })
```

## Compliance Checklist

Before deploying analytics:

- [ ] No PII tracked (names, emails, IPs, etc.)
- [ ] File names anonymized or not tracked
- [ ] URLs sanitized (IDs/tokens removed)
- [ ] User input not tracked
- [ ] Error messages anonymized
- [ ] Metadata is concise and relevant
- [ ] Event names follow snake_case convention
- [ ] Tests verify no PII in tracking calls
- [ ] Analytics calls wrapped in try/catch
- [ ] Performance impact minimal (async tracking)

## Reference Implementation

See existing tools for examples:
- `app/tools/split-bill/page.tsx` - Comprehensive tracking
- `app/tools/qr-code/page.tsx` - File upload tracking
- `app/tools/json-beautifier/page.tsx` - Processing tracking

## Common Mistakes to Avoid

### ❌ Tracking User Input

```typescript
// DON'T
trackToolEvent('password-generator', 'generated', {
  password: generatedPassword  // Never track passwords!
})
```

### ❌ Tracking File Names

```typescript
// DON'T
trackToolEvent('file-converter', 'converted', {
  fileName: file.name  // File names might contain PII
})
```

### ❌ Tracking Full URLs

```typescript
// DON'T
trackToolEvent('url-shortener', 'shortened', {
  originalUrl: url  // URLs might contain tokens/sensitive data
})
```

### ❌ Detailed Error Messages

```typescript
// DON'T
trackToolEvent('tool-id', 'error', {
  errorMessage: error.message  // Might contain sensitive info
})
```

### ✅ Correct Alternatives

```typescript
// DO - Anonymized tracking
trackToolEvent('password-generator', 'generated', {
  length: password.length,
  hasSpecialChars: includesSpecialChars,
  strength: 'strong'
})

trackToolEvent('file-converter', 'converted', {
  fileType: file.type,
  fileSizeRange: getFileSizeRange(file.size)
})

trackToolEvent('url-shortener', 'shortened', {
  urlLength: url.length > 100 ? 'long' : 'short',
  protocol: new URL(url).protocol
})

trackToolEvent('tool-id', 'error', {
  errorType: categorizeError(error)
})
```

## Implementation in New Tools

When creating a new tool, add analytics for:

1. **Page view** - Track when tool loads
2. **Primary action** - Track main feature usage
3. **Success/failure** - Track operation outcomes
4. **Exports** - Track when users export/download
5. **Settings** - Track feature toggle/configuration changes
6. **Errors** - Track error types (anonymized)

## Summary

**Golden Rule**: If you wouldn't want it tracked about yourself, don't track it about users.

When in doubt, ask:
1. Is this PII? → Don't track it
2. Can this be anonymized? → Anonymize it
3. Is this useful for metrics? → Track it safely
