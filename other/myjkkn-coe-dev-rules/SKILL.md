---
name: myjkkn-coe-dev-rules
description: Complete reference for MyJKKN API integration, institution filtering, role-based access control, and field mappings between MyJKKN and COE local database. This skill should be used when implementing MyJKKN data fetching, institution-based filtering, handling super_admin vs normal user access, or mapping field names between systems. Automatically triggers when user mentions 'MyJKKN mapping', 'field mapping', 'institution filter', 'super_admin access', 'global select', 'myjkkn_institution_ids', 'counselling_code', or asks about column name differences.
---

# MyJKKN-COE Dev Rules

Complete development rules for integrating MyJKKN API with COE local database, including institution filtering, role-based access, CRUD operations, and field mappings.

## Quick Reference

### Key Hooks
| Hook | Purpose | Location |
|------|---------|----------|
| `useInstitutionFilter` | Filter data by institution, UI visibility control | `hooks/use-institution-filter.ts` |
| `useInstitutionField` | Form field management (show/hide, auto-fill) | `hooks/use-institution-field.ts` |
| `useMyJKKNInstitutionFilter` | Fetch & filter MyJKKN data | `hooks/use-myjkkn-institution-filter.ts` |

### Key Properties
| Property | Description |
|----------|-------------|
| `mustSelectInstitution` | `true` when super_admin views "All Institutions" |
| `shouldFilter` | `true` when filtering should be applied |
| `myjkkn_institution_ids` | Array of MyJKKN UUIDs for direct API filtering |

---

## Part 1: Institution Filter Rules

### 1.1 User Role Behavior

#### super_admin Users

```typescript
// Properties
canSwitchInstitution = true

// When "All Institutions" selected (selectedInstitution = null)
shouldFilter = false          // Sees ALL data
institutionFilter = {}        // Empty filter
mustSelectInstitution = true  // Show institution UI

// When specific institution selected
shouldFilter = true           // Filtered data
institutionFilter = { institution_code: 'CAS', institutions_id: 'uuid' }
mustSelectInstitution = false // Hide institution UI
```

#### Normal Users (coe, deputy_coe, coe_office)

```typescript
// Properties
canSwitchInstitution = false
shouldFilter = true           // ALWAYS filtered
mustSelectInstitution = false // ALWAYS hidden

// Auto-filled from auth context
currentInstitution = user.institution_id
currentInstitutionCode = user.institution_code
```

### 1.2 UI Visibility Patterns

#### Institution Field in Forms

```tsx
// Show when:
// 1. super_admin viewing "All Institutions" (mustSelectInstitution = true)
// 2. User can switch institutions (!shouldFilter || !institutionId)
{mustSelectInstitution || !shouldFilter || !institutionId ? (
  <div className="space-y-2">
    <Label>Institution <span className="text-red-500">*</span></Label>
    <Select value={formData.institutions_id} onValueChange={handleChange}>
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

#### Institution Column in Tables

```tsx
<TableHeader>
  <TableRow>
    {/* Show only when "All Institutions" is selected */}
    {mustSelectInstitution && <TableHead>Institution</TableHead>}
    <TableHead>Code</TableHead>
    <TableHead>Name</TableHead>
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

#### Add Button Behavior

```tsx
// Add button should ALWAYS work - user selects institution in form
<Button onClick={() => { resetForm(); setSheetOpen(true) }}>
  <PlusCircle className="h-3 w-3 mr-1" />
  Add
</Button>

// In resetForm, auto-fill institution when possible
const resetForm = () => {
  setFormData({
    institutions_id: getInstitutionIdForCreate() || '',
    // ... other fields
  })
}
```

#### Colspan Adjustment

```tsx
// Adjust colspan based on institution column visibility
<TableRow>
  <TableCell
    colSpan={mustSelectInstitution ? 8 : 7}
    className="text-center"
  >
    {loading ? 'Loading...' : 'No data found'}
  </TableCell>
</TableRow>
```

### 1.3 Data Upload & Download Rules

#### Normal Users (coe, deputy_coe, coe_office)

| Operation | Behavior |
|-----------|----------|
| **Upload (Import)** | Can only upload data for **their own institution** |
| **Download (Export)** | Can only download data from **their own institution** |
| **Institution Field** | Hidden - auto-filled from auth context |
| **Data Scope** | Restricted to assigned institution only |

```typescript
// Normal user upload - institution auto-filled
const handleImport = async (data: ImportData[]) => {
  // Institution automatically attached from context
  const institutionId = getInstitutionIdForCreate() // Always returns user's institution

  const payload = data.map(row => ({
    ...row,
    institutions_id: institutionId  // Auto-attached
  }))

  await fetch('/api/entity/import', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

// Normal user download - auto-filtered
const handleExport = async () => {
  // API automatically filters by user's institution
  const url = appendToUrl('/api/entity/export')  // Adds institution params
  const response = await fetch(url)
  // Returns only their institution's data
}
```

#### super_admin Users

| Scenario | Behavior |
|----------|----------|
| **"All Institutions" selected** | Must select institution in form/dialog before upload |
| **Specific institution selected** | Same rules as normal user for that institution |
| **Download with "All Institutions"** | Downloads ALL institutions' data (merged) |
| **Download with specific institution** | Downloads only selected institution's data |

```typescript
// super_admin behavior depends on selection state
const { mustSelectInstitution, getInstitutionIdForCreate } = useInstitutionFilter()

// Upload handling
const handleImport = async (data: ImportData[], selectedInstitutionId?: string) => {
  let institutionId: string

  if (mustSelectInstitution) {
    // "All Institutions" mode - user MUST select in form
    if (!selectedInstitutionId) {
      toast({ title: 'Please select an institution', variant: 'destructive' })
      return
    }
    institutionId = selectedInstitutionId
  } else {
    // Specific institution selected - use it
    institutionId = getInstitutionIdForCreate()!
  }

  const payload = data.map(row => ({
    ...row,
    institutions_id: institutionId
  }))

  await fetch('/api/entity/import', { method: 'POST', body: JSON.stringify(payload) })
}

// Download handling
const handleExport = async () => {
  if (mustSelectInstitution) {
    // "All Institutions" - downloads ALL data
    const response = await fetch('/api/entity/export')  // No institution filter
    // Returns data from ALL institutions
  } else {
    // Specific institution - filtered download
    const url = appendToUrl('/api/entity/export')
    const response = await fetch(url)
    // Returns only selected institution's data
  }
}
```

#### Summary Table

| User Type | Selection State | Upload Behavior | Download Behavior |
|-----------|-----------------|-----------------|-------------------|
| Normal User | N/A (fixed) | Own institution only | Own institution only |
| super_admin | "All Institutions" | Must select institution in form | ALL institutions' data |
| super_admin | Specific institution | Selected institution only | Selected institution only |

#### Import Dialog Pattern for super_admin

```tsx
// Import dialog with institution selection for super_admin
<Dialog open={importOpen} onOpenChange={setImportOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Import Data</DialogTitle>
    </DialogHeader>

    {/* Show institution select ONLY when "All Institutions" is selected */}
    {mustSelectInstitution && (
      <div className="space-y-2">
        <Label>Institution <span className="text-red-500">*</span></Label>
        <Select
          value={importInstitutionId}
          onValueChange={setImportInstitutionId}
        >
          <SelectTrigger>
            <SelectValue placeholder="Select institution for import" />
          </SelectTrigger>
          <SelectContent>
            {institutions.map((inst) => (
              <SelectItem key={inst.id} value={inst.id}>
                {inst.institution_code} - {inst.institution_name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <p className="text-xs text-muted-foreground">
          All imported records will be assigned to this institution
        </p>
      </div>
    )}

    {/* File upload area */}
    <FileUpload onUpload={handleFileUpload} />

    <DialogFooter>
      <Button
        onClick={handleImport}
        disabled={mustSelectInstitution && !importInstitutionId}
      >
        Import
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### 1.4 CRUD Operations Rules (Insert/Update/Delete/View)

#### Complete CRUD Behavior Matrix

| Operation | Normal User | super_admin (All Institutions) | super_admin (Specific Institution) |
|-----------|-------------|-------------------------------|-----------------------------------|
| **View (List)** | Own institution only | ALL institutions | Selected institution only |
| **View (Detail)** | Own institution only | Any institution | Selected institution only |
| **Insert (Create)** | Own institution (auto-filled) | Must select institution in form | Selected institution (auto-filled) |
| **Update (Edit)** | Own institution records only | Any institution's records | Selected institution records only |
| **Delete** | Own institution records only | Any institution's records | Selected institution records only |

#### VIEW Operations

```typescript
// Fetch data for listing
const fetchData = async () => {
  // appendToUrl handles filtering based on user type and selection
  const url = appendToUrl('/api/entity')
  const response = await fetch(url)
  const data = await response.json()
  setItems(data)
}

// Result behavior:
// - Normal user: Returns only their institution's records
// - super_admin (All): Returns ALL records from ALL institutions
// - super_admin (Specific): Returns only selected institution's records
```

#### INSERT (Create) Operations

```typescript
// Create new record
const handleCreate = async () => {
  // Get institution ID based on user type and selection
  let institutionId: string | null

  if (mustSelectInstitution) {
    // super_admin with "All Institutions" - must select in form
    institutionId = formData.institutions_id
    if (!institutionId) {
      setErrors({ institutions_id: 'Institution is required' })
      return
    }
  } else {
    // Normal user OR super_admin with specific selection - auto-fill
    institutionId = getInstitutionIdForCreate()
  }

  const payload = {
    ...formData,
    institutions_id: institutionId
  }

  await fetch('/api/entity', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}
```

#### UPDATE Operations

```typescript
// Update existing record
const handleUpdate = async (id: string) => {
  // Institution ID comes from the record being edited
  // User can only edit records they have access to (enforced by API)
  const payload = {
    id,
    ...formData
    // institutions_id is NOT changed during update - keeps original
  }

  await fetch('/api/entity', {
    method: 'PUT',
    body: JSON.stringify(payload)
  })
}

// API-side validation (route.ts):
// - Normal user: Can only update records matching their institution_id
// - super_admin: Can update any record (no institution restriction)
```

#### DELETE Operations

```typescript
// Delete record
const handleDelete = async (id: string) => {
  await fetch(`/api/entity?id=${id}`, {
    method: 'DELETE'
  })
}

// API-side validation (route.ts):
// - Normal user: Can only delete records matching their institution_id
// - super_admin: Can delete any record (no institution restriction)
```

#### API Route Pattern for Institution-Based Access Control

```typescript
// app/api/entity/route.ts

// GET - List with institution filter
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const institutionCode = searchParams.get('institution_code')
  const institutionsId = searchParams.get('institutions_id')

  let query = supabase.from('entity').select('*')

  // Apply filter if provided (normal users always have filter, super_admin optional)
  if (institutionCode) {
    query = query.eq('institution_code', institutionCode)
  } else if (institutionsId) {
    query = query.eq('institutions_id', institutionsId)
  }
  // If no filter: super_admin viewing all - return everything

  const { data, error } = await query
  return NextResponse.json(data)
}

// POST - Create with institution assignment
export async function POST(request: Request) {
  const body = await request.json()

  // institutions_id is required and comes from client
  // Client ensures it's either:
  // - Auto-filled (normal user / super_admin with selection)
  // - User-selected (super_admin with "All Institutions")

  const { data, error } = await supabase
    .from('entity')
    .insert(body)
    .select()
    .single()

  return NextResponse.json(data)
}

// PUT - Update (institution_id preserved)
export async function PUT(request: Request) {
  const body = await request.json()
  const { id, ...updateData } = body

  // Note: Do NOT allow changing institutions_id during update
  delete updateData.institutions_id
  delete updateData.institution_code

  const { data, error } = await supabase
    .from('entity')
    .update(updateData)
    .eq('id', id)
    .select()
    .single()

  return NextResponse.json(data)
}

// DELETE - Remove record
export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  const { error } = await supabase
    .from('entity')
    .delete()
    .eq('id', id)

  return NextResponse.json({ success: true })
}
```

#### Form Reset Pattern with Institution Handling

```typescript
const resetForm = () => {
  // Get institution ID for new records
  const autoInstitutionId = getInstitutionIdForCreate() || ''

  setFormData({
    institutions_id: autoInstitutionId,  // Auto-fill when possible
    code: '',
    name: '',
    // ... other fields
  })
  setErrors({})
  setEditing(null)
}

// When editing existing record
const handleEdit = (item: Entity) => {
  setEditing(item)
  setFormData({
    institutions_id: item.institutions_id,  // Use record's institution
    code: item.code,
    name: item.name,
    // ... other fields
  })
  setSheetOpen(true)
}
```

#### Institution Field Visibility in Form (Complete Pattern)

```tsx
{/*
  Show institution field when:
  1. Creating new record AND "All Institutions" selected (mustSelectInstitution = true)
  2. OR user can switch institutions AND no institution is set

  Hide institution field when:
  1. Editing existing record (institution comes from record)
  2. Normal user (institution auto-filled from auth)
  3. super_admin with specific institution selected
*/}
{!editing && (mustSelectInstitution || !shouldFilter || !institutionId) ? (
  <div className="space-y-2">
    <Label>
      Institution <span className="text-red-500">*</span>
    </Label>
    <Select
      value={formData.institutions_id}
      onValueChange={(v) => {
        setFormData(prev => ({
          ...prev,
          institutions_id: v,
          // Clear dependent fields when institution changes
          program_code: '',
          regulation_code: ''
        }))
      }}
    >
      <SelectTrigger className={errors.institutions_id ? 'border-red-500' : ''}>
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
    {errors.institutions_id && (
      <p className="text-xs text-red-500">{errors.institutions_id}</p>
    )}
  </div>
) : null}

{/* Show read-only institution info when editing */}
{editing && (
  <div className="space-y-2">
    <Label>Institution</Label>
    <Input
      value={institutions.find(i => i.id === formData.institutions_id)?.institution_code || ''}
      disabled
      className="bg-muted"
    />
    <p className="text-xs text-muted-foreground">
      Institution cannot be changed after creation
    </p>
  </div>
)}
```

---

## Part 2: MyJKKN Integration Rules

### 2.1 Critical Constraints

| Rule | Description |
|------|-------------|
| **Use `myjkkn_institution_ids` directly** | No two-step lookup! COE institutions have array of MyJKKN UUIDs |
| **Client-side filter ALWAYS** | MyJKKN API may ignore server-side `institution_id` - always filter client-side |
| **Deduplicate by CODE** | Programs: `program_id`, Regulations: `regulation_code`, Others: `id` |
| **Handle multiple UUIDs** | One institution = multiple UUIDs (Aided + Self-financing) |
| **Response handling** | Always: `response.data || response || []` |

### 2.2 Data Fetching Pattern

```typescript
import { useMyJKKNInstitutionFilter } from '@/hooks/use-myjkkn-institution-filter'

const { fetchPrograms, fetchRegulations, fetchSemesters } = useMyJKKNInstitutionFilter()

// Get myjkkn_institution_ids from COE institution
const institution = institutions.find(i => i.id === institutionId)
const myjkknIds = institution?.myjkkn_institution_ids || []

// Use IDs directly - no lookup needed!
const programs = await fetchPrograms(myjkknIds)
const regulations = await fetchRegulations(myjkknIds)
```

### 2.3 Deduplication Rules

| Entity | Deduplicate By | Why |
|--------|---------------|-----|
| Programs | `program_id` (CODE like "BCA") | Same program exists in Aided + SF |
| Regulations | `regulation_code` | Same regulation across branches |
| Semesters | `id` | Unique per program |
| Batches | `id` | Unique per program |
| Learners | `id` | Unique per person |

```typescript
// Example: Deduplicate programs by program_id (CODE field)
const seenCodes = new Set<string>()
const uniquePrograms = []

for (const prog of allPrograms) {
  const code = prog.program_id || prog.program_code
  if (code && !seenCodes.has(code)) {
    seenCodes.add(code)
    uniquePrograms.push(prog)
  }
}
```

---

## Part 3: Field Name Mappings

### 3.1 Critical Differences (MyJKKN vs COE)

| Entity | MyJKKN Field | COE Local Field | Notes |
|--------|--------------|-----------------|-------|
| **Course** | `course_name` | `course_title` | **Different name!** |
| **Program** | `program_id` | `program_code` | MyJKKN `program_id` is CODE ("BCA"), NOT UUID |
| **Institution FK** | `institution_id` | `institutions_id` | COE uses **plural** form |
| **Duration** | `duration_years` | `program_duration_yrs` | Different name |

### 3.2 Institution Fields

| MyJKKN Field | COE Field | Notes |
|--------------|-----------|-------|
| `id` | `id` | UUID |
| `institution_code` | `institution_code` | Primary identifier |
| `counselling_code` | `counselling_code` | For MyJKKN API matching |
| `name` | `name`, `institution_name` | Display name |
| N/A | `myjkkn_institution_ids` | Array of MyJKKN UUIDs |

### 3.3 Program Fields

| MyJKKN Field | COE Field | Notes |
|--------------|-----------|-------|
| `id` | `id` | UUID (actual unique ID) |
| `program_id` | `program_code` | **CODE** ("BCA", "MCA") - NOT UUID! |
| `program_code` | `program_code` | Fallback CODE field |
| `program_name` | `program_name` | Full name |
| `name` | `program_name` | Fallback field |
| `duration_years` | `program_duration_yrs` | Duration in years |

### 3.4 Course Fields

| MyJKKN Field | COE Field | Notes |
|--------------|-----------|-------|
| `id` | `id` | UUID |
| `course_code` | `course_code` | Primary code |
| `course_name` | `course_title` | **Different!** MyJKKN = name, COE = title |
| `credit` | `credits` | Credit points |
| `institution_id` | `institutions_id` | Note: COE uses **plural** |

### 3.5 Regulation Fields

| MyJKKN Field | COE Field | Notes |
|--------------|-----------|-------|
| `id` | `id` | UUID |
| `regulation_code` | `regulation_code` | Primary code |
| `regulation_name` | `regulation_name` | Full name |
| `name` | `regulation_name` | Fallback field |
| `effective_year` | `regulation_year` | Year regulation takes effect |

### 3.6 Semester Fields

| MyJKKN Field | COE Field | Notes |
|--------------|-----------|-------|
| `id` | `id` | UUID |
| `semester_code` | `semester_code` | Code like "BCA-1" |
| `semester_name` | `semester_name` | Name like "Semester I" |
| `name` | `semester_name` | Fallback field |
| `semester_number` | `semester_number` | Numeric order (1-8) |

**Extracting semester_number:**
```typescript
let semesterNum = s.semester_number
// Fallback 1: Extract from code (e.g., "BCA-2" → 2)
if (!semesterNum && s.semester_code) {
  const match = s.semester_code.match(/-(\d+)$/)
  if (match) semesterNum = parseInt(match[1])
}
// Fallback 2: Extract from name (e.g., "Semester II" → 2)
if (!semesterNum && s.semester_name) {
  const romanMap = { 'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8 }
  const romanMatch = s.semester_name.match(/\b(I|II|III|IV|V|VI|VII|VIII)\b/)
  if (romanMatch) semesterNum = romanMap[romanMatch[1]]
}
```

### 3.7 Batch Fields

| MyJKKN Field | COE Field | Notes |
|--------------|-----------|-------|
| `id` | `id` | UUID |
| `batch_code` | `batch_code` | Primary code |
| `batch_name` | `batch_name` | Display name |
| `name` | `batch_name` | Fallback field |
| `start_year` | `start_year` | Start year |
| `end_year` | `end_year` | End year |

### 3.8 Learner Fields

| MyJKKN Field | COE Field | Notes |
|--------------|-----------|-------|
| `id` | `id` | UUID |
| `register_number` | `register_number` | Unique registration |
| `roll_number` | `roll_number` | Roll number |
| `first_name` | `first_name` | First name |
| `last_name` | `last_name` | Last name |
| `college_email` | `learner_email` | Primary email |
| `student_email` | `learner_email` | Fallback email |
| `email` | `learner_email` | Fallback email |
| `student_mobile` | `learner_mobile` | Primary phone |
| `phone` | `learner_mobile` | Fallback phone |
| `is_active` | `is_active`, `status` | Both used |
| `is_profile_complete` | `is_active` | Fallback for status |

**Email/Phone precedence:**
```typescript
const learnerEmail = l.college_email || l.student_email || l.email
const learnerMobile = l.student_mobile || l.phone
```

### 3.9 Status Fields

| MyJKKN | COE | Notes |
|--------|-----|-------|
| `is_active` | `is_active` | Boolean status |
| `is_active` | `status` | COE uses both interchangeably |
| `is_profile_complete` | N/A | Learner-specific fallback for is_active |

---

## Part 4: Complete Implementation Pattern

### 4.1 Page with Institution Filter + MyJKKN Data

```typescript
'use client'

import { useState, useEffect, useCallback } from 'react'
import { useInstitutionFilter } from '@/hooks/use-institution-filter'
import { useMyJKKNInstitutionFilter } from '@/hooks/use-myjkkn-institution-filter'

interface Institution {
  id: string
  institution_code: string
  institution_name: string
  myjkkn_institution_ids: string[] | null  // Required for MyJKKN!
}

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

  // MyJKKN data fetching
  const { fetchPrograms, fetchRegulations } = useMyJKKNInstitutionFilter()

  // State
  const [institutions, setInstitutions] = useState<Institution[]>([])
  const [programs, setPrograms] = useState<any[]>([])
  const [programsLoading, setProgramsLoading] = useState(false)

  // Fetch institutions (include myjkkn_institution_ids!)
  const fetchInstitutions = async () => {
    const res = await fetch('/api/master/institutions')
    if (res.ok) {
      const data = await res.json()
      setInstitutions(data.map((i: any) => ({
        id: i.id,
        institution_code: i.institution_code,
        institution_name: i.institution_name || i.name,
        myjkkn_institution_ids: i.myjkkn_institution_ids || []  // Critical!
      })))
    }
  }

  // Load programs from MyJKKN
  const loadPrograms = useCallback(async (instId: string) => {
    setProgramsLoading(true)
    setPrograms([])

    const institution = institutions.find(i => i.id === instId)
    const myjkknIds = institution?.myjkkn_institution_ids || []

    if (myjkknIds.length === 0) {
      console.warn('No MyJKKN institution IDs found')
      setProgramsLoading(false)
      return
    }

    // Use IDs directly - no lookup!
    const progs = await fetchPrograms(myjkknIds)
    setPrograms(progs)
    setProgramsLoading(false)
  }, [institutions, fetchPrograms])

  // Initial load
  useEffect(() => {
    if (isReady) {
      fetchInstitutions()
    }
  }, [isReady])

  // Form with institution field visibility
  return (
    <>
      {/* Institution field - show only when needed */}
      {mustSelectInstitution || !shouldFilter || !institutionId ? (
        <InstitutionSelect
          value={formData.institutions_id}
          onChange={(v) => {
            setFormData({ ...formData, institutions_id: v })
            loadPrograms(v)  // Load dependent data
          }}
          institutions={institutions}
        />
      ) : null}

      {/* Dependent dropdown */}
      <ProgramSelect
        value={formData.program_code}
        onChange={(v) => setFormData({ ...formData, program_code: v })}
        programs={programs}
        loading={programsLoading}
        disabled={!formData.institutions_id}
        placeholder={
          !formData.institutions_id
            ? "Select institution first"
            : programsLoading
              ? "Loading programs..."
              : "Select program"
        }
      />
    </>
  )
}
```

### 4.2 Dependent Dropdown Cascade

```typescript
// Institution → Programs, Regulations
useEffect(() => {
  if (formData.institutions_id) {
    loadPrograms(formData.institutions_id)
    loadRegulations(formData.institutions_id)
  } else {
    setPrograms([])
    setRegulations([])
  }
  // Clear dependent fields
  setFormData(prev => ({ ...prev, program_code: '', regulation_code: '' }))
}, [formData.institutions_id])

// Program → Semesters
useEffect(() => {
  if (formData.program_code && formData.institutions_id) {
    const program = programs.find(p => p.program_code === formData.program_code)
    if (program) {
      loadSemesters(formData.institutions_id, program.id)  // Use program UUID
    }
  } else {
    setSemesters([])
  }
  setFormData(prev => ({ ...prev, semester_id: '' }))
}, [formData.program_code])
```

---

## Part 5: Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Fetching before `isReady` | Always check `isReady` first |
| Not using `appendToUrl()` | Use it to add institution params to API calls |
| Blocking Add button | Add button always works - user selects in form |
| Hardcoding table colspan | Adjust based on `mustSelectInstitution` |
| Trusting MyJKKN server-side filtering | Always filter client-side by `institution_id` |
| Deduplicating by `id` | Deduplicate by CODE field (e.g., `program_code`) |
| Not clearing dependent fields | Clear when parent changes |
| Missing `myjkkn_institution_ids` | Always fetch with institutions |
| Using `counselling_code` lookup | Use `myjkkn_institution_ids` directly |
| Using `course_name` in COE | Use `course_title` (COE's field name) |
| Using `program_id` as UUID | It's a CODE field in MyJKKN! |

---

## Part 6: Reference Files

| Purpose | File |
|---------|------|
| Institution context | `context/institution-context.tsx` |
| Filter hook | `hooks/use-institution-filter.ts` |
| Form field hook | `hooks/use-institution-field.ts` |
| MyJKKN filtering | `hooks/use-myjkkn-institution-filter.ts` |
| MyJKKN types | `types/myjkkn.ts` |
| Adapter service | `services/myjkkn/myjkkn-adapter-service.ts` |
| Institution API | `app/api/master/institutions/route.ts` |
| Example page | `app/(coe)/master/degrees/page.tsx` |
