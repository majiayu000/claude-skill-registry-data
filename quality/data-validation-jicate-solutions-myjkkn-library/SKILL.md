---
name: data-validation
description: Complete data validation patterns for JKKN COE Next.js application. This skill should be used when implementing form validation, import validation, or API-level validation. Automatically triggers when user mentions 'validation', 'validate', 'required fields', 'error messages', 'form errors', 'input validation', or 'data quality'.
---

# Data Validation Skill

This skill provides comprehensive validation patterns for the JKKN COE application, covering client-side form validation, import data validation, and server-side API validation.

## When to Use This Skill

Use this skill when:
- Implementing form validation for CRUD operations
- Validating imported Excel/CSV/JSON data
- Creating API-level validation in route handlers
- Standardizing error messages across the application
- Handling foreign key validation

## File Locations (Following project-structure)

```
lib/utils/
├── [entity]-validation.ts      # Entity-specific validation
├── validation-helpers.ts       # Shared validation utilities
```

## Validation Function Pattern

### 1. Entity Validation Function

Create a dedicated validation file for each entity:

**File: `lib/utils/[entity]-validation.ts`**

```typescript
export function validate[Entity]Data(
  data: Record<string, unknown>,
  rowIndex?: number
): string[] {
  const errors: string[] = []
  const prefix = rowIndex ? `Row ${rowIndex}: ` : ''

  // Required field validations
  if (!data.[entity]_code || String(data.[entity]_code).trim() === '') {
    errors.push(`${prefix}Entity Code is required`)
  } else if (String(data.[entity]_code).length > 50) {
    errors.push(`${prefix}Entity Code must be 50 characters or less`)
  }

  if (!data.[entity]_name || String(data.[entity]_name).trim() === '') {
    errors.push(`${prefix}Entity Name is required`)
  } else if (String(data.[entity]_name).length > 200) {
    errors.push(`${prefix}Entity Name must be 200 characters or less`)
  }

  // Format validations (see patterns below)
  // ...

  return errors
}
```

## Validation Patterns

### Required Field Validation

```typescript
// Simple required check
if (!data.field_name || String(data.field_name).trim() === '') {
  errors.push('Field Name is required')
}

// With length constraint
if (!data.field_name || String(data.field_name).trim() === '') {
  errors.push('Field Name is required')
} else if (String(data.field_name).length > 100) {
  errors.push('Field Name must be 100 characters or less')
}
```

### Email Validation

```typescript
if (data.email && String(data.email).trim() !== '') {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(String(data.email))) {
    errors.push('Email format is invalid')
  } else if (String(data.email).length > 100) {
    errors.push('Email must be 100 characters or less')
  }
}
```

### Phone Validation

```typescript
if (data.phone && String(data.phone).trim() !== '') {
  const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,15}$/
  if (!phoneRegex.test(String(data.phone))) {
    errors.push('Phone number format is invalid (10-15 digits)')
  }
}
```

### URL/Website Validation

```typescript
if (data.website && String(data.website).trim() !== '') {
  try {
    new URL(String(data.website))
  } catch {
    errors.push('Website URL format is invalid')
  }
  if (String(data.website).length > 255) {
    errors.push('Website URL must be 255 characters or less')
  }
}
```

### PIN Code Validation (India)

```typescript
if (data.pin_code && String(data.pin_code).trim() !== '') {
  const pinRegex = /^[0-9]{6}$/
  if (!pinRegex.test(String(data.pin_code))) {
    errors.push('PIN Code must be exactly 6 digits')
  }
}
```

### Enum/Allowed Values Validation

```typescript
if (data.entity_type && String(data.entity_type).trim() !== '') {
  const validTypes = ['type1', 'type2', 'type3']
  if (!validTypes.includes(String(data.entity_type))) {
    errors.push(`Entity Type must be one of: ${validTypes.join(', ')}`)
  }
}
```

### Numeric Range Validation

```typescript
if (data.credits !== undefined && data.credits !== '') {
  const credits = Number(data.credits)
  if (isNaN(credits) || credits < 0 || credits > 10) {
    errors.push('Credits must be between 0 and 10')
  }
}
```

### Boolean/Status Validation

```typescript
if (data.is_active !== undefined && data.is_active !== null) {
  if (typeof data.is_active !== 'boolean') {
    const statusValue = String(data.is_active).toLowerCase()
    if (!['true', 'false', 'active', 'inactive'].includes(statusValue)) {
      errors.push('Status must be true/false or Active/Inactive')
    }
  }
}
```

### Conditional Validation

```typescript
// Theory credit required when split credit is enabled
if (data.split_credit) {
  if (!data.theory_credit || Number(data.theory_credit) === 0) {
    errors.push('Theory credit is required when split credit is enabled')
  }
  if (!data.practical_credit || Number(data.practical_credit) === 0) {
    errors.push('Practical credit is required when split credit is enabled')
  }
}
```

### Code Format Validation

```typescript
// Alphanumeric with hyphens and underscores
if (data.course_code && !/^[A-Za-z0-9\-_]+$/.test(String(data.course_code))) {
  errors.push('Course code can only contain letters, numbers, hyphens, and underscores')
}
```

### String Length Batch Validation

```typescript
const stringFields = [
  { field: 'address_line1', maxLength: 255, name: 'Address Line 1' },
  { field: 'address_line2', maxLength: 255, name: 'Address Line 2' },
  { field: 'city', maxLength: 100, name: 'City' },
  { field: 'state', maxLength: 100, name: 'State' },
  { field: 'country', maxLength: 100, name: 'Country' },
]

stringFields.forEach(({ field, maxLength, name }) => {
  if (data[field] && String(data[field]).length > maxLength) {
    errors.push(`${name} must be ${maxLength} characters or less`)
  }
})
```

## Form Validation Pattern

### In-Page Validation Hook

```typescript
const [errors, setErrors] = useState<Record<string, string>>({})

const validate = (): boolean => {
  const e: Record<string, string> = {}

  if (!formData.institution_code.trim()) {
    e.institution_code = 'Institution is required'
  }
  if (!formData.[entity]_code.trim()) {
    e.[entity]_code = 'Entity Code is required'
  }
  if (!formData.[entity]_name.trim()) {
    e.[entity]_name = 'Entity Name is required'
  }

  // Additional validations...

  setErrors(e)
  return Object.keys(e).length === 0
}
```

### Form Field with Error Display

```tsx
<div className="space-y-2">
  <Label htmlFor="[entity]_code">
    Entity Code <span className="text-red-500">*</span>
  </Label>
  <Input
    id="[entity]_code"
    value={formData.[entity]_code}
    onChange={(e) => setFormData({ ...formData, [entity]_code: e.target.value })}
    className={errors.[entity]_code ? 'border-red-500' : ''}
    placeholder="Enter entity code"
  />
  {errors.[entity]_code && (
    <p className="text-sm text-red-500">{errors.[entity]_code}</p>
  )}
</div>
```

### Form Submission with Validation

```typescript
const handleSubmit = async () => {
  if (!validate()) {
    toast({
      title: 'Validation Error',
      description: 'Please fix all validation errors before submitting.',
      variant: 'destructive'
    })
    return
  }

  try {
    setLoading(true)
    const response = await fetch('/api/[entity]', {
      method: editing ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Failed to save')
    }

    // Success handling...
  } catch (error) {
    const errorMessage = error instanceof Error
      ? error.message
      : 'Failed to save. Please try again.'

    toast({
      title: 'Save Failed',
      description: errorMessage,
      variant: 'destructive'
    })
  } finally {
    setLoading(false)
  }
}
```

## API-Level Validation

### Server-Side Validation in Route Handler

```typescript
// app/api/[entity]/route.ts
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()

    // Required field validation
    if (!body.[entity]_code?.trim()) {
      return NextResponse.json(
        { error: 'Entity Code is required' },
        { status: 400 }
      )
    }

    if (!body.[entity]_name?.trim()) {
      return NextResponse.json(
        { error: 'Entity Name is required' },
        { status: 400 }
      )
    }

    // Foreign key validation
    const { data: institutionData, error: institutionError } = await supabase
      .from('institutions')
      .select('id')
      .eq('institution_code', body.institution_code)
      .single()

    if (institutionError || !institutionData) {
      return NextResponse.json(
        { error: `Institution "${body.institution_code}" not found` },
        { status: 400 }
      )
    }

    // Insert with validated data...

  } catch (error) {
    console.error('API error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### PostgreSQL Error Code Handling

```typescript
if (error) {
  console.error('Database error:', error)

  // Duplicate key constraint (23505)
  if (error.code === '23505') {
    return NextResponse.json(
      { error: 'Record already exists. Please use different values.' },
      { status: 400 }
    )
  }

  // Foreign key constraint (23503)
  if (error.code === '23503') {
    return NextResponse.json(
      { error: 'Invalid reference. Please select a valid option.' },
      { status: 400 }
    )
  }

  // Check constraint (23514)
  if (error.code === '23514') {
    return NextResponse.json(
      { error: 'Invalid value. Please check your input.' },
      { status: 400 }
    )
  }

  // Not-null constraint (23502)
  if (error.code === '23502') {
    return NextResponse.json(
      { error: 'Missing required field.' },
      { status: 400 }
    )
  }

  return NextResponse.json(
    { error: 'Failed to save record' },
    { status: 500 }
  )
}
```

## Import Validation Pattern

```typescript
// Validate each row during import
for (let i = 0; i < rows.length; i++) {
  const row = rows[i]
  const rowNumber = i + 2 // +2 for header row in Excel

  const validationErrors = validate[Entity]Data(row, rowNumber)

  if (validationErrors.length > 0) {
    uploadErrors.push({
      row: rowNumber,
      [entity]_code: row.[entity]_code || 'N/A',
      [entity]_name: row.[entity]_name || 'N/A',
      errors: validationErrors
    })
    continue
  }

  // Proceed with API save...
}
```

## Complete Example: Institution Validation

See `references/institution-validation-example.md` for a complete implementation.

## Testing Checklist

- [ ] Required fields show errors when empty
- [ ] Email format validation works
- [ ] Phone format validation works
- [ ] URL format validation works
- [ ] Length constraints are enforced
- [ ] Enum values are validated
- [ ] Numeric ranges are validated
- [ ] Conditional validation works
- [ ] Error messages are user-friendly
- [ ] API returns proper error codes
- [ ] Import validation shows row numbers
