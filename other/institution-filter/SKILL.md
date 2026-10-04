---
name: institution-filter
description: Complete guide for implementing institution-based data filtering in JKKN COE pages. This skill should be used when creating or updating pages that need to filter data by institution, implementing institution dropdowns in forms, or integrating with MyJKKN API with institution context. Automatically triggers when user mentions 'institution filter', 'filter by institution', 'institution dropdown', 'multi-tenant', or asks about institution-scoped data.
---

# Institution Filter Skill

This skill provides patterns for implementing institution-based data filtering across the JKKN COE application.

## Overview

The COE application is multi-tenant - users see only data belonging to their institution unless they are `super_admin`. This skill covers:

1. **Index Pages** - Filtering data lists by institution
2. **Add/Edit Forms** - Institution field visibility (show/hide based on context)
3. **Table Columns** - Institution column visibility
4. **MyJKKN Integration** - Direct UUID lookup using `myjkkn_institution_ids`
5. **Dependent Dropdowns** - Cascading dropdowns that depend on institution selection

## Core Hooks

### 1. `useInstitutionFilter` - For Index Pages & Forms

Location: `hooks/use-institution-filter.ts`

Provides filtering logic for data fetching and UI visibility control.

```typescript
import { useInstitutionFilter } from '@/hooks/use-institution-filter'

const {
  filter,                    // { institution_code?: string, institutions_id?: string }
  isReady,                   // true when context is initialized
  appendToUrl,               // (url) => url with query params
  getInstitutionIdForCreate, // () => institution_id for new records
  mustSelectInstitution,     // true when "All Institutions" is selected globally
  shouldFilter,              // true if filtering is active
  institutionId              // current institution id or null
} = useInstitutionFilter()
```

**Key Properties:**

| Property | Description |
|----------|-------------|
| `filter` | Object with `institution_code` and `institutions_id` to pass to API |
| `isReady` | Boolean - wait for this before fetching data |
| `appendToUrl(url)` | Appends institution query params to URL |
| `getInstitutionIdForCreate()` | Returns institution ID for new records (auto-fills form) |
| `mustSelectInstitution` | `true` when "All Institutions" selected (show institution dropdown/column) |
| `shouldFilter` | `true` when filtering should be applied |
| `institutionId` | Current institution ID or null |

### 2. `useInstitutionField` - For Form Field Management

Location: `hooks/use-institution-field.ts`

Higher-level hook for managing institution dropdown in forms.

```typescript
import { useInstitutionField } from '@/hooks/use-institution-field'

const {
  shouldShowField,           // true when dropdown should be visible
  defaultInstitutionCode,    // auto-fill value when field is hidden
  defaultInstitutionId,      // auto-fill ID value
  availableInstitutions,     // list of institutions for dropdown
  isLoading                  // loading state
} = useInstitutionField()
```

### 3. `useMyJKKNInstitutionFilter` - For MyJKKN API Integration

Location: `hooks/use-myjkkn-institution-filter.ts`

**NEW PATTERN:** Uses `myjkkn_institution_ids` array directly from COE institutions table - no two-step lookup required!

**Critical Constraints:**
1. COE institutions have `myjkkn_institution_ids: string[]` field with MyJKKN UUIDs
2. MyJKKN API may ignore server-side `institution_id` filtering - **always filter client-side**
3. Deduplicate by CODE field (e.g., `regulation_code`, `program_id`), **NOT by `id`**
4. MyJKKN uses `program_id` as the CODE field (like "BCA"), NOT as a UUID

```typescript
import { useMyJKKNInstitutionFilter } from '@/hooks/use-myjkkn-institution-filter'

const {
  fetchRegulations,       // (myjkknInstitutionIds) => Promise<RegulationOption[]>
  fetchLearnerProfiles,   // (myjkknInstitutionIds, options) => Promise<LearnerProfileOption[]>
  fetchPrograms,          // (myjkknInstitutionIds, options) => Promise<ProgramOption[]>
  fetchSemesters,         // (myjkknInstitutionIds, options) => Promise<SemesterOption[]>
  fetchBatches,           // (myjkknInstitutionIds, options) => Promise<BatchOption[]>
  fetchFilteredData       // Generic function for any endpoint
} = useMyJKKNInstitutionFilter()
```

### 4. `useMyJKKNPrograms` - For Programs from MyJKKN

Location: `hooks/myjkkn/use-myjkkn-data.ts`

Declarative hook for fetching programs with auto-refresh on options change.

```typescript
import { useMyJKKNPrograms } from '@/hooks/myjkkn/use-myjkkn-data'

const { data: programs, loading, error, refetch } = useMyJKKNPrograms({
  is_active: true,
  institution_code: institutionCode,  // Optional - filter by institution
})
```

## Database Schema: myjkkn_institution_ids

The COE `institutions` table has a `myjkkn_institution_ids` column:

```sql
-- institutions table
myjkkn_institution_ids TEXT[] -- Array of MyJKKN institution UUIDs
```

**Example data:**
| institution_code | counselling_code | myjkkn_institution_ids |
|------------------|------------------|------------------------|
| CAS | CAS | `["a33138b6-4eea-4675-941f-1071bf88b127","b0b8a724-7c65-4f07-8047-2a38e8100ad5"]` |
| CET | CET | `["uuid-1","uuid-2"]` |

The array contains multiple UUIDs because MyJKKN has separate records for:
- Aided institution
- Self-financing (SF) institution

Both share the same `counselling_code` but have different `id` values.

## UI Visibility Patterns

### Pattern 1: Institution Field in Forms

Show institution dropdown when:
1. "All Institutions" is selected globally (`mustSelectInstitution = true`)
2. User can switch institutions (`!shouldFilter || !institutionId`)

Hide when a specific institution is already selected (auto-fill from context).

```tsx
{/* Show institution field when needed */}
{mustSelectInstitution || !shouldFilter || !institutionId ? (
  <div className="space-y-2">
    <Label>Institution <span className="text-red-500">*</span></Label>
    <Select
      value={formData.institutions_id}
      onValueChange={(v) => setFormData({ ...formData, institutions_id: v })}
    >
      <SelectTrigger>
        <SelectValue placeholder="Select institution" />
      </SelectTrigger>
      <SelectContent>
        {institutions.map((inst) => (
          <SelectItem key={inst.id} value={inst.id}>
            {inst.institution_code} - {inst.institution_name}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  </div>
) : null}
```

### Pattern 2: Institution Column in Tables

Show Institution column only when "All Institutions" is selected globally.

```tsx
<TableHeader>
  <TableRow>
    {/* Show Institution column only when "All Institutions" is selected */}
    {mustSelectInstitution && (
      <TableHead>Institution</TableHead>
    )}
    <TableHead>Code</TableHead>
    <TableHead>Name</TableHead>
    {/* ... other columns */}
  </TableRow>
</TableHeader>

<TableBody>
  {items.map((item) => (
    <TableRow key={item.id}>
      {mustSelectInstitution && (
        <TableCell>
          {institutions.find(i => i.id === item.institutions_id)?.institution_code || '-'}
        </TableCell>
      )}
      <TableCell>{item.code}</TableCell>
      <TableCell>{item.name}</TableCell>
    </TableRow>
  ))}
</TableBody>
```

### Pattern 3: Add Button Behavior

Add button should ALWAYS work - opens form directly without blocking.
- When `mustSelectInstitution = true`: user selects institution in the form
- When `mustSelectInstitution = false`: institution auto-fills from context

```tsx
<Button onClick={() => {
  resetForm()
  setSheetOpen(true)
}}>
  <PlusCircle className="h-3 w-3 mr-1" />
  Add
</Button>
```

## MyJKKN Integration Pattern (NEW)

### Pattern 4: Using myjkkn_institution_ids Directly

**This is the recommended pattern.** No two-step lookup required!

```typescript
// State for institutions (must include myjkkn_institution_ids)
const [institutions, setInstitutions] = useState<Array<{
  id: string
  institution_code: string
  institution_name: string
  myjkkn_institution_ids: string[] | null  // NEW: Direct UUIDs
}>>([])

// Hook for MyJKKN filtering
const { fetchPrograms } = useMyJKKNInstitutionFilter()

// Fetch programs when institution changes
const loadPrograms = async (institutionId: string) => {
  setProgramsLoading(true)
  setPrograms([])

  // Get the institution with its myjkkn_institution_ids
  const institution = institutions.find(i => i.id === institutionId)
  const myjkknIds = institution?.myjkkn_institution_ids || []

  if (myjkknIds.length === 0) {
    console.warn('No MyJKKN institution IDs found')
    setProgramsLoading(false)
    return
  }

  // Use IDs directly - no lookup needed!
  const progs = await fetchPrograms(myjkknIds)
  setPrograms(progs)
  setProgramsLoading(false)
}

// Effect: Refetch when institution changes
useEffect(() => {
  if (formData.institutions_id) {
    loadPrograms(formData.institutions_id)
  } else {
    setPrograms([])
  }
}, [formData.institutions_id])
```

### Pattern 5: Fetching Institutions with myjkkn_institution_ids

Always fetch `myjkkn_institution_ids` when loading institutions:

```typescript
const fetchInstitutions = async () => {
  try {
    const res = await fetch('/api/master/institutions')
    if (res.ok) {
      const data = await res.json()
      const mapped = Array.isArray(data)
        ? data.filter((i: any) => i?.institution_code).map((i: any) => ({
          id: i.id,
          institution_code: i.institution_code,
          institution_name: i.institution_name || i.name,
          myjkkn_institution_ids: i.myjkkn_institution_ids || []  // Include this!
        }))
        : []
      setInstitutions(mapped)
    }
  } catch (e) {
    console.error('Failed to load institutions:', e)
  }
}
```

### Pattern 6: Dependent Dropdowns (Programs, Regulations, Semesters)

From: `course-management/course-mapping/add/page.tsx`

```typescript
'use client'

import { useState, useEffect } from 'react'
import { useMyJKKNInstitutionFilter } from '@/hooks/use-myjkkn-institution-filter'

export default function CourseMappingAddPage() {
  const [institutions, setInstitutions] = useState<any[]>([])
  const [programs, setPrograms] = useState<any[]>([])
  const [regulations, setRegulations] = useState<any[]>([])
  const [semesters, setSemesters] = useState<any[]>([])

  const [programsLoading, setProgramsLoading] = useState(false)
  const [regulationsLoading, setRegulationsLoading] = useState(false)
  const [semestersLoading, setSemestersLoading] = useState(false)

  const [selectedInstitution, setSelectedInstitution] = useState('')
  const [selectedProgram, setSelectedProgram] = useState('')
  const [selectedRegulation, setSelectedRegulation] = useState('')

  // Hook for MyJKKN data fetching
  const { fetchPrograms, fetchRegulations, fetchSemesters } = useMyJKKNInstitutionFilter()

  // Fetch institutions on mount
  useEffect(() => {
    const loadInstitutions = async () => {
      const res = await fetch('/api/master/institutions')
      if (res.ok) {
        const data = await res.json()
        setInstitutions(data.map((i: any) => ({
          id: i.id,
          institution_code: i.institution_code,
          name: i.name,
          myjkkn_institution_ids: i.myjkkn_institution_ids || []
        })))
      }
    }
    loadInstitutions()
  }, [])

  // Fetch programs when institution changes
  useEffect(() => {
    if (!selectedInstitution) {
      setPrograms([])
      return
    }

    const loadPrograms = async () => {
      setProgramsLoading(true)
      const institution = institutions.find(i => i.institution_code === selectedInstitution)
      const myjkknIds = institution?.myjkkn_institution_ids || []

      if (myjkknIds.length === 0) {
        setPrograms([])
        setProgramsLoading(false)
        return
      }

      const progs = await fetchPrograms(myjkknIds)
      setPrograms(progs)
      setProgramsLoading(false)
    }

    loadPrograms()
    // Clear dependent selections
    setSelectedProgram('')
    setRegulations([])
    setSemesters([])
  }, [selectedInstitution, institutions, fetchPrograms])

  // Fetch regulations when institution changes
  useEffect(() => {
    if (!selectedInstitution) {
      setRegulations([])
      return
    }

    const loadRegulations = async () => {
      setRegulationsLoading(true)
      const institution = institutions.find(i => i.institution_code === selectedInstitution)
      const myjkknIds = institution?.myjkkn_institution_ids || []

      if (myjkknIds.length === 0) {
        setRegulations([])
        setRegulationsLoading(false)
        return
      }

      const regs = await fetchRegulations(myjkknIds)
      setRegulations(regs)
      setRegulationsLoading(false)
    }

    loadRegulations()
    setSelectedRegulation('')
  }, [selectedInstitution, institutions, fetchRegulations])

  // Fetch semesters when program changes
  useEffect(() => {
    if (!selectedProgram || !selectedInstitution) {
      setSemesters([])
      return
    }

    const loadSemesters = async () => {
      setSemestersLoading(true)
      const institution = institutions.find(i => i.institution_code === selectedInstitution)
      const myjkknIds = institution?.myjkkn_institution_ids || []

      // Find the selected program to get its UUID
      const program = programs.find(p => p.program_code === selectedProgram)
      const programId = program?.id

      const sems = await fetchSemesters(myjkknIds, { program_id: programId })
      setSemesters(sems)
      setSemestersLoading(false)
    }

    loadSemesters()
  }, [selectedProgram, selectedInstitution, institutions, programs, fetchSemesters])

  return (
    <div className="space-y-4">
      {/* Institution Select */}
      <Select value={selectedInstitution} onValueChange={setSelectedInstitution}>
        <SelectTrigger>
          <SelectValue placeholder="Select Institution" />
        </SelectTrigger>
        <SelectContent>
          {institutions.map((inst) => (
            <SelectItem key={inst.institution_code} value={inst.institution_code}>
              {inst.institution_code} - {inst.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      {/* Program Select - depends on institution */}
      <Select
        value={selectedProgram}
        onValueChange={setSelectedProgram}
        disabled={!selectedInstitution || programsLoading}
      >
        <SelectTrigger className={!selectedInstitution ? 'bg-muted' : ''}>
          <SelectValue placeholder={
            !selectedInstitution
              ? "Select institution first"
              : programsLoading
                ? "Loading programs..."
                : programs.length === 0
                  ? "No programs found"
                  : "Select program"
          } />
        </SelectTrigger>
        <SelectContent>
          {programs.map((prog) => (
            <SelectItem key={prog.id} value={prog.program_code}>
              {prog.program_code} - {prog.program_name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      {/* Regulation Select - depends on institution */}
      <Select
        value={selectedRegulation}
        onValueChange={setSelectedRegulation}
        disabled={!selectedInstitution || regulationsLoading}
      >
        <SelectTrigger className={!selectedInstitution ? 'bg-muted' : ''}>
          <SelectValue placeholder={
            !selectedInstitution
              ? "Select institution first"
              : regulationsLoading
                ? "Loading regulations..."
                : "Select regulation"
          } />
        </SelectTrigger>
        <SelectContent>
          {regulations.map((reg) => (
            <SelectItem key={reg.id} value={reg.regulation_code}>
              {reg.regulation_code} - {reg.regulation_name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
```

## MyJKKN Field Naming Conventions

**IMPORTANT:** MyJKKN uses different field names than you might expect:

| Field | Description | Example Value |
|-------|-------------|---------------|
| `id` | UUID (actual unique identifier) | `a33138b6-4eea-4675-941f-1071bf88b127` |
| `program_id` | Program CODE (NOT a UUID!) | `BCA`, `MCA`, `MBA` |
| `regulation_code` | Regulation CODE | `REG2020`, `REG2023` |
| `institution_id` | Institution UUID | `a33138b6-4eea-4675-941f-1071bf88b127` |

**Deduplication Rules:**
- Programs: Deduplicate by `program_id` (the CODE field)
- Regulations: Deduplicate by `regulation_code`
- Semesters: Deduplicate by `id` (actual UUID)
- Batches: Deduplicate by `id` (actual UUID)
- Learners: Deduplicate by `id` (actual UUID)

## Complete Page Pattern

```typescript
'use client'

import { useState, useEffect, useCallback } from 'react'
import { useInstitutionFilter } from '@/hooks/use-institution-filter'
import { useMyJKKNInstitutionFilter } from '@/hooks/use-myjkkn-institution-filter'

export default function EntityPage() {
  // Institution filter hook
  const {
    filter,
    isReady,
    appendToUrl,
    getInstitutionIdForCreate,
    mustSelectInstitution,
    shouldFilter,
    institutionId
  } = useInstitutionFilter()

  // MyJKKN integration
  const { fetchRegulations, fetchPrograms } = useMyJKKNInstitutionFilter()

  // State
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [sheetOpen, setSheetOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [institutions, setInstitutions] = useState<Array<{
    id: string
    institution_code: string
    institution_name: string
    myjkkn_institution_ids: string[] | null
  }>>([])
  const [regulations, setRegulations] = useState([])
  const [regulationsLoading, setRegulationsLoading] = useState(false)

  // Form state
  const [formData, setFormData] = useState({
    institutions_id: '',
    code: '',
    name: '',
    regulation_id: ''
  })
  const [errors, setErrors] = useState<Record<string, string>>({})

  // Fetch data with institution filter
  const fetchData = async () => {
    try {
      setLoading(true)
      const url = appendToUrl('/api/entity')
      const response = await fetch(url)
      if (response.ok) {
        const data = await response.json()
        setItems(data)
      }
    } finally {
      setLoading(false)
    }
  }

  // Fetch institutions (include myjkkn_institution_ids)
  const fetchInstitutions = async () => {
    try {
      const res = await fetch('/api/master/institutions')
      if (res.ok) {
        const data = await res.json()
        const mapped = Array.isArray(data)
          ? data.filter((i: any) => i?.institution_code).map((i: any) => ({
            id: i.id,
            institution_code: i.institution_code,
            institution_name: i.institution_name || i.name,
            myjkkn_institution_ids: i.myjkkn_institution_ids || []
          }))
          : []
        setInstitutions(mapped)
      }
    } catch (e) {
      console.error('Failed to load institutions:', e)
    }
  }

  // Fetch regulations from MyJKKN using myjkkn_institution_ids
  const loadRegulations = useCallback(async (instId?: string) => {
    try {
      setRegulationsLoading(true)
      setRegulations([])

      if (!instId) return

      const institution = institutions.find(i => i.id === instId)
      const myjkknIds = institution?.myjkkn_institution_ids || []

      if (myjkknIds.length === 0) {
        console.warn('No MyJKKN institution IDs for:', institution?.institution_code)
        return
      }

      // Use IDs directly - no lookup needed!
      const regs = await fetchRegulations(myjkknIds)
      setRegulations(regs.map(r => ({
        id: r.id,
        regulation_code: r.regulation_code,
        regulation_name: r.regulation_name || r.regulation_code
      })))
    } finally {
      setRegulationsLoading(false)
    }
  }, [institutions, fetchRegulations])

  // Load data when institution filter is ready
  useEffect(() => {
    if (isReady) {
      fetchData()
      fetchInstitutions()
    }
  }, [isReady, filter])

  // Fetch regulations when form institution changes
  useEffect(() => {
    if (formData.institutions_id) {
      loadRegulations(formData.institutions_id)
    } else {
      setRegulations([])
    }
  }, [formData.institutions_id, loadRegulations])

  // Reset form with auto-filled institution
  const resetForm = () => {
    const autoInstitutionId = getInstitutionIdForCreate() || ''
    setFormData({
      institutions_id: autoInstitutionId,
      code: '',
      name: '',
      regulation_id: ''
    })
    setErrors({})
    setEditing(null)
  }

  // Handle edit - populate form with existing data
  const handleEdit = (item) => {
    setEditing(item)
    setFormData({
      institutions_id: item.institutions_id,
      code: item.code,
      name: item.name,
      regulation_id: item.regulation_id || ''
    })
    setSheetOpen(true)
  }

  return (
    <>
      {/* Data Table */}
      <Table>
        <TableHeader>
          <TableRow>
            {mustSelectInstitution && <TableHead>Institution</TableHead>}
            <TableHead>Code</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {items.map((item) => (
            <TableRow key={item.id}>
              {mustSelectInstitution && (
                <TableCell>
                  {institutions.find(i => i.id === item.institutions_id)?.institution_code || '-'}
                </TableCell>
              )}
              <TableCell>{item.code}</TableCell>
              <TableCell>{item.name}</TableCell>
              <TableCell>
                <Button onClick={() => handleEdit(item)}>Edit</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* Add Button - Always works */}
      <Button onClick={() => { resetForm(); setSheetOpen(true) }}>Add</Button>

      {/* Form Sheet */}
      <Sheet open={sheetOpen} onOpenChange={(o) => { if (!o) resetForm(); setSheetOpen(o) }}>
        <SheetContent>
          <form>
            {/* Institution field - show only when needed */}
            {mustSelectInstitution || !shouldFilter || !institutionId ? (
              <div className="space-y-2">
                <Label>Institution <span className="text-red-500">*</span></Label>
                <Select
                  value={formData.institutions_id}
                  onValueChange={(v) => setFormData({
                    ...formData,
                    institutions_id: v,
                    regulation_id: '' // Clear dependent field
                  })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select institution" />
                  </SelectTrigger>
                  <SelectContent>
                    {institutions.map((inst) => (
                      <SelectItem key={inst.id} value={inst.id}>
                        {inst.institution_code} - {inst.institution_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            ) : null}

            {/* Dependent regulation dropdown */}
            <div className="space-y-2">
              <Label>Regulation</Label>
              <Select
                value={formData.regulation_id}
                onValueChange={(v) => setFormData({ ...formData, regulation_id: v })}
                disabled={!formData.institutions_id || regulationsLoading}
              >
                <SelectTrigger className={!formData.institutions_id ? 'bg-muted' : ''}>
                  <SelectValue placeholder={
                    !formData.institutions_id
                      ? "Select institution first"
                      : regulationsLoading
                        ? "Loading..."
                        : "Select regulation"
                  } />
                </SelectTrigger>
                <SelectContent>
                  {regulations.map((reg) => (
                    <SelectItem key={reg.id} value={reg.id}>
                      {reg.regulation_code}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Other form fields */}
            <Input
              value={formData.code}
              onChange={(e) => setFormData({ ...formData, code: e.target.value })}
            />
          </form>
        </SheetContent>
      </Sheet>
    </>
  )
}
```

## Validation Pattern

```typescript
const validate = () => {
  const e: Record<string, string> = {}

  // Institution is required
  if (!formData.institutions_id) {
    e.institutions_id = 'Institution is required'
  }

  // Other validations...
  if (!formData.code.trim()) {
    e.code = 'Code is required'
  }

  setErrors(e)
  return Object.keys(e).length === 0
}
```

## Colspan Adjustment for Tables

When Institution column visibility changes, adjust colspan for empty/loading states:

```tsx
<TableRow>
  <TableCell
    colSpan={mustSelectInstitution ? 8 : 7}
    className="text-center"
  >
    {loading ? 'Loading...' : 'No data'}
  </TableCell>
</TableRow>
```

## Common Mistakes to Avoid

1. **Fetching before filter is ready** - Always check `isReady` before fetching
2. **Not using `appendToUrl`** - Use this to add institution params to API calls
3. **Blocking Add button** - Add button should always work; institution selected in form
4. **Forgetting to reset form** - Use `getInstitutionIdForCreate()` in `resetForm()`
5. **Hardcoding column counts** - Adjust colspan based on `mustSelectInstitution`
6. **MyJKKN: Trusting server-side filtering** - Always filter client-side by `institution_id`
7. **MyJKKN: Deduplicating by `id`** - Deduplicate by code field (e.g., `regulation_code`, `program_id`)
8. **Not clearing dependent fields** - When institution changes, clear dependent dropdowns
9. **Not showing loading state** - Show "Loading..." in dependent dropdowns while fetching
10. **Not including `myjkkn_institution_ids`** - Always fetch this field with institutions
11. **Using `counselling_code` lookup** - Use `myjkkn_institution_ids` directly (no lookup needed!)

## Summary: When to Use Which Hook

| Use Case | Hook |
|----------|------|
| Filter index page data | `useInstitutionFilter` + `appendToUrl()` |
| Show/hide institution field in forms | `useInstitutionFilter` + `mustSelectInstitution` |
| Auto-fill institution for new records | `useInstitutionFilter` + `getInstitutionIdForCreate()` |
| Fetch MyJKKN data by institution | `useMyJKKNInstitutionFilter` + `myjkkn_institution_ids` |
| Fetch programs (declarative) | `useMyJKKNPrograms` + client-side filter |
| Generic MyJKKN data with filtering | `useMyJKKNInstitutionFilter` + specific fetch method |

## Migration from Old Pattern (counselling_code)

If you have code using the old two-step `counselling_code` lookup pattern:

**OLD (deprecated):**
```typescript
const { fetchRegulations } = useMyJKKNInstitutionFilter()

// Old: Pass counselling_code, hook does two-step lookup
const institution = institutions.find(i => i.id === institutionId)
const regs = await fetchRegulations(institution?.counselling_code)
```

**NEW (recommended):**
```typescript
const { fetchRegulations } = useMyJKKNInstitutionFilter()

// New: Pass myjkkn_institution_ids directly, no lookup needed!
const institution = institutions.find(i => i.id === institutionId)
const myjkknIds = institution?.myjkkn_institution_ids || []
const regs = await fetchRegulations(myjkknIds)
```

The new pattern is simpler and more efficient - it uses the pre-populated `myjkkn_institution_ids` array directly instead of making an extra API call to look up institution IDs by `counselling_code`.
