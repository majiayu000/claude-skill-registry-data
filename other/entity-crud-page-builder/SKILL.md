---
name: entity-crud-page-builder
description: Complete workflow for building standardized entity CRUD pages in the JKKN COE Next.js application. This skill should be used when creating or updating entity management pages (like courses, degrees, departments, programs, students, etc.) that require full CRUD operations, data tables, import/export functionality, and comprehensive validation. Automatically triggers when user mentions creating entity pages, CRUD operations, or standardizing existing pages.
---

# Entity CRUD Page Builder

This skill provides a complete workflow for building standardized entity management pages in the JKKN COE application, following the proven patterns from [app/coe/degree/page.tsx](app/coe/degree/page.tsx).

## About This Skill

Entity CRUD pages in JKKN COE follow a standardized pattern that includes:
- **Data Table**: Sortable, searchable, paginated data display
- **Form Management**: Sheet-based forms with comprehensive validation
- **Import/Export**: Excel/JSON import with detailed error tracking
- **Template Generation**: Excel templates with reference sheets
- **Upload Summary**: Visual feedback with success/failure tracking
- **Toast Notifications**: Context-aware success/error messages
- **Foreign Key Handling**: Automatic ID resolution from codes

## When to Use This Skill

Use this skill when:
- Creating a new entity management page (e.g., courses, students, departments)
- Standardizing an existing CRUD page to match project patterns
- Adding import/export functionality to an entity page
- Implementing comprehensive validation and error handling
- Building data tables with sorting, filtering, and pagination

## Page Structure Overview

Every entity CRUD page consists of:

### 1. Core Components
- **Data Table**: Fixed-height scrollable table with sticky headers
- **Scorecard Section**: Summary metrics (total, active, inactive, new this month)
- **Action Bar**: Search, filters, refresh, template, download, upload, add buttons
- **Form Sheet**: Slide-out form for create/edit operations
- **Error Dialog**: Detailed upload error display with summary cards

### 2. State Management
```typescript
const [items, setItems] = useState<Entity[]>([])
const [loading, setLoading] = useState(true)
const [searchTerm, setSearchTerm] = useState("")
const [sortColumn, setSortColumn] = useState<string | null>(null)
const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc")
const [currentPage, setCurrentPage] = useState(1)
const itemsPerPage = 10

const [sheetOpen, setSheetOpen] = useState(false)
const [editing, setEditing] = useState<Entity | null>(null)
const [statusFilter, setStatusFilter] = useState("all")
const [errorPopupOpen, setErrorPopupOpen] = useState(false)

const [importErrors, setImportErrors] = useState<Array<{
  row: number
  [entity]_code: string
  [entity]_name: string
  errors: string[]
}>>([])

const [uploadSummary, setUploadSummary] = useState<{
  total: number
  success: number
  failed: number
}>({ total: 0, success: 0, failed: 0 })
```

### 3. Form Data Structure
```typescript
const [formData, setFormData] = useState({
  // Required fields (marked with * in UI)
  institution_code: "",
  [entity]_code: "",
  [entity]_name: "",

  // Optional fields
  display_name: "",
  description: "",

  // Status toggle
  is_active: true,
})
```

## Implementation Steps

### Step 1: Define Entity Type and State

1. **Create TypeScript Interface**
   ```typescript
   interface Entity {
     id: string
     institution_code: string
     [entity]_code: string
     [entity]_name: string
     display_name?: string
     description?: string
     is_active: boolean
     created_at: string
   }
   ```

2. **Initialize State Variables** (see State Management section above)

3. **Set Up Validation Hook** (see `references/validation-patterns.md`)

### Step 2: Implement Data Fetching

1. **API Fetch Function**
   ```typescript
   const fetchEntities = async () => {
     try {
       setLoading(true)
       const response = await fetch('/api/[entity]')
       if (!response.ok) throw new Error('Failed to fetch')
       const data = await response.json()
       setItems(data)
     } catch (error) {
       console.error('Error fetching:', error)
       setItems([])
     } finally {
       setLoading(false)
     }
   }
   ```

2. **Fetch Reference Data** (institutions, departments, etc.)

3. **useEffect Hook**
   ```typescript
   useEffect(() => {
     fetchEntities()
     fetchReferenceData()
   }, [])
   ```

### Step 3: Build Data Table Section

1. **Scorecard Metrics** (4 cards: Total, Active, Inactive, New This Month)
2. **Action Bar** (Status filter, Search, Refresh, Template, Download, Upload, Add)
3. **Data Table** with:
   - Fixed height: `style={{ height: "440px" }}`
   - Sticky header: `className="sticky top-0 z-10"`
   - Sortable columns with sort icons
   - Action buttons (Edit, Delete) in last column
4. **Pagination Controls** (Previous/Next with page info)

### Step 4: Implement Form Sheet

1. **Sheet Component** with gradient header and sections
2. **Form Sections**:
   - Basic Information (required fields with red asterisks)
   - Additional Details (optional fields)
   - Status Section (toggle switch)
3. **Form Validation** (see `references/validation-patterns.md`)
4. **Save Handler** with foreign key auto-mapping (see CLAUDE.md)

### Step 5: Add Import/Export Functionality

See `references/upload-patterns.md` for complete implementation:

1. **Template Export** with:
   - Sample data row
   - Mandatory fields marked with red headers and asterisks
   - Reference sheet for foreign key codes (e.g., Institution Codes)
   - Column width optimization

2. **Data Export** (Excel format with current data)

3. **Import Handler** with:
   - File parsing (JSON/CSV/Excel)
   - Row-by-row validation
   - Foreign key validation
   - Detailed error tracking
   - Upload summary tracking

4. **Error Dialog** with visual summary cards (see `references/upload-patterns.md`)

### Step 6: Implement CRUD Operations

1. **Create**: POST to `/api/[entity]` with validation
2. **Update**: PUT to `/api/[entity]` with validation
3. **Delete**: DELETE to `/api/[entity]?id={id}` with confirmation
4. **Error Handling**: Extract error messages from API response JSON

### Step 7: Add Toast Notifications

Use context-aware toast messages:
- ✅ **Success** (green): "Record Created/Updated/Deleted"
- ❌ **Error** (red): "Save Failed" with error message
- ⚠️ **Warning** (yellow): "Validation Error" or "Partial Upload Success"

## Key Patterns and Best Practices

### Foreign Key Auto-Mapping
Always validate and resolve foreign key references before insert:
```typescript
// Fetch institutions_id from institution_code
const selectedInstitution = institutions.find(inst =>
  inst.institution_code === formData.institution_code
)

if (!selectedInstitution) {
  toast({
    title: "❌ Error",
    description: "Selected institution not found",
    variant: "destructive",
  })
  return
}

const payload = {
  ...formData,
  institutions_id: selectedInstitution.id
}
```

### Upload Error Tracking
Track three metrics: total rows, successful saves, failed saves
```typescript
setUploadSummary({
  total: mapped.length,
  success: successCount,
  failed: errorCount
})
```

### Visual Error Display
Show 3-column summary cards (blue/green/red) in error dialog with detailed error list showing row numbers and specific validation failures.

### API Error Extraction
Always extract error messages from API response JSON:
```typescript
if (!response.ok) {
  const errorData = await response.json()
  throw new Error(errorData.error || 'Failed to save')
}
```

### Validation Pattern
See `references/validation-patterns.md` for comprehensive validation examples including:
- Required field validation
- Format validation (regex)
- Length constraints
- Numeric range validation
- Conditional validation
- URL validation
- Foreign key validation

## Reference Files

This skill includes detailed reference documentation:

1. **`references/validation-patterns.md`**: Comprehensive validation examples
2. **`references/upload-patterns.md`**: Import/export implementation details
3. **`references/form-patterns.md`**: Form design and layout patterns

## Common Customizations

### Adding Optional Fields
Add to formData state, form UI (without asterisk), and API payload.

### Adding Foreign Key Relationships
1. Add dropdown in form (use Select component)
2. Fetch reference data in useEffect
3. Implement auto-mapping in save handler
4. Validate in API route before insert

### Adjusting Table Columns
Modify TableHead and TableCell components to match entity fields.

### Custom Validation Rules
Add entity-specific validation in validate function (see validation-patterns.md).

## Testing Checklist

After implementation, verify:
- ✅ Create operation with validation
- ✅ Update operation with validation
- ✅ Delete operation with confirmation
- ✅ Sort by all columns
- ✅ Search across all text fields
- ✅ Status filter (All/Active/Inactive)
- ✅ Pagination (Previous/Next)
- ✅ Excel template export with reference sheet
- ✅ Excel data export
- ✅ Import with validation errors (verify error dialog)
- ✅ Import with foreign key errors
- ✅ Partial import success (some pass, some fail)
- ✅ Full import success
- ✅ Toast notifications for all operations
- ✅ Mobile responsive layout
- ✅ Dark mode support

## Notes

- All entity pages should maintain visual consistency (same spacing, colors, icons)
- Always use the same toast notification patterns for user feedback
- Foreign key validation must happen both client-side and server-side
- Upload error dialog must show row numbers matching Excel file (header row = row 1)
- Template exports must include a reference sheet for foreign key codes
- Status toggles should use the same green/red color scheme across all pages
