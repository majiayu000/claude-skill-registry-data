---
name: excel-import-export
description: Complete workflow for implementing Excel/JSON import and export functionality in JKKN COE Next.js application. This skill should be used when adding file import, export, or template generation features to entity pages. Automatically triggers when user mentions 'import', 'export', 'upload', 'download', 'template', 'Excel', 'XLSX', 'CSV', or 'JSON file handling'.
---

# Excel Import/Export Skill

This skill provides comprehensive patterns for implementing import/export functionality in the JKKN COE application, following project standards.

## When to Use This Skill

Use this skill when:
- Adding import/export functionality to entity pages
- Creating Excel/CSV/JSON file parsing logic
- Generating downloadable templates with sample data
- Implementing bulk upload with validation
- Creating export functionality for filtered data
- Building upload error tracking and display

## File Locations (Following project-structure)

When implementing import/export, create files in these locations:

```
lib/utils/
├── [entity]-validation.ts      # Validation functions
├── [entity]-export-import.ts   # Export/Import utilities
```

## Core Implementation Patterns

### 1. Export Utility Functions

Create a dedicated utility file for each entity:

**File: `lib/utils/[entity]-export-import.ts`**

```typescript
import XLSX from '@/lib/utils/excel-compat'
import type { Entity } from '@/types/[entity]'

// Export to JSON
export function exportToJSON(items: Entity[]): void {
  const exportData = items.map(item => ({
    [entity]_code: item.[entity]_code,
    [entity]_name: item.[entity]_name,
    // Map all fields
    is_active: item.is_active,
    created_at: item.created_at
  }))

  const json = JSON.stringify(exportData, null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `[entity]s_${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// Export to Excel
export async function exportToExcel(items: Entity[]): Promise<void> {
  const excelData = items.map((r) => ({
    'Entity Code': r.[entity]_code,
    'Entity Name': r.[entity]_name,
    // Map fields to human-readable column names
    'Status': r.is_active ? 'Active' : 'Inactive',
    'Created': new Date(r.created_at).toISOString().split('T')[0],
  }))

  const ws = XLSX.utils.json_to_sheet(excelData)

  // Set column widths
  const colWidths = [
    { wch: 20 }, // Entity Code
    { wch: 30 }, // Entity Name
    { wch: 10 }, // Status
    { wch: 12 }, // Created
  ]
  ws['!cols'] = colWidths

  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Data')
  await XLSX.writeFile(wb, `[entity]s_export_${new Date().toISOString().split('T')[0]}.xlsx`)
}
```

---

## Template Export with Dropdown Lists & Invalid Value Highlighting

The excel-compat layer supports **both dropdown validation AND conditional formatting** for highlighting invalid values in red. This is the **RECOMMENDED PATTERN** for all template exports.

### How It Works

1. **Dropdown Lists** (if values fit < 255 chars): Shows a dropdown menu in Excel
2. **Conditional Formatting** (ALWAYS applied): Invalid values get red background + red text
3. **Hidden `_ValidCodes` Sheet**: Stores valid values for long lists (>255 chars)
4. **Reference Codes Sheet**: Human-readable documentation for users

### Critical: 255 Character Limit

Excel has a **255 character limit** for inline dropdown formulas. The excel-compat layer handles this:

- **Short lists** (< 255 chars total): Uses inline formula `"Value1,Value2,Value3"` with dropdown
- **Long lists** (>= 255 chars): Uses hidden sheet reference `'_ValidCodes'!$A$1:$A$50` + conditional formatting

### Complete Template Export Pattern

**Reference Implementation: `app/(coe)/master/boards/page.tsx`**

```typescript
// Template Export with Reference Sheets and Dropdown Validation
const handleTemplateExport = async () => {
  const wb = XLSX.utils.book_new()

  // ═══════════════════════════════════════════════════════════════
  // Sheet 1: Template with empty row for user to fill
  // Note: Use * to mark required fields in headers
  // ═══════════════════════════════════════════════════════════════
  const sample = [{
    'Institution Code *': '',
    'Board Code *': '',
    'Board Name *': '',
    'Display Name': '',
    'Board Type': '',
    'Board Order': '',
    'Status': 'Active'
  }]

  const ws = XLSX.utils.json_to_sheet(sample)

  // Set column widths for readability
  const colWidths = [
    { wch: 20 }, // Institution Code
    { wch: 20 }, // Board Code
    { wch: 40 }, // Board Name
    { wch: 30 }, // Display Name
    { wch: 20 }, // Board Type
    { wch: 15 }, // Board Order
    { wch: 12 }, // Status
  ]
  ws['!cols'] = colWidths

  // ═══════════════════════════════════════════════════════════════
  // ADD DATA VALIDATIONS (DROPDOWN LISTS + CONDITIONAL FORMATTING)
  // excel-compat handles the 255 char limit automatically:
  // - Short lists: inline dropdown + conditional formatting
  // - Long lists: hidden sheet reference + conditional formatting
  // ═══════════════════════════════════════════════════════════════
  const validations: any[] = []

  // Column A: Institution Code dropdown
  // IMPORTANT: Always include showDropDown: true for dropdown to appear
  const instCodes = institutions.map(i => i.institution_code).filter(Boolean)
  if (instCodes.length > 0) {
    validations.push({
      type: 'list',
      sqref: 'A2:A1000',
      formula1: `"${instCodes.join(',')}"`,
      showDropDown: true,  // CRITICAL: Required for dropdown to appear
      showErrorMessage: true,
      errorTitle: 'Invalid Institution',
      error: 'Please select from the dropdown list',
    })
  }

  // Column E: Board Type dropdown (enum values)
  const boardTypes = ['National', 'State', 'International', 'Private', 'University']
  validations.push({
    type: 'list',
    sqref: 'E2:E1000',
    formula1: `"${boardTypes.join(',')}"`,
    showDropDown: true,
    showErrorMessage: true,
    errorTitle: 'Invalid Board Type',
    error: 'Select: National, State, International, Private, or University',
  })

  // Column G: Status dropdown (always short, fits inline)
  validations.push({
    type: 'list',
    sqref: 'G2:G1000',
    formula1: '"Active,Inactive"',
    showDropDown: true,
    showErrorMessage: true,
    errorTitle: 'Invalid Status',
    error: 'Select: Active or Inactive',
  })

  // Attach validations to worksheet
  // excel-compat will process these and:
  // 1. Create dropdowns (if < 255 chars) or use hidden sheet reference
  // 2. ALWAYS add conditional formatting to highlight invalid values in red
  ws['!dataValidation'] = validations

  XLSX.utils.book_append_sheet(wb, ws, 'Template')

  // ═══════════════════════════════════════════════════════════════
  // Sheet 2: Reference Codes (for user documentation)
  // Use section separators with ═══ for visual grouping
  // ═══════════════════════════════════════════════════════════════
  const referenceData: any[] = []

  // Institution codes section
  referenceData.push({ 'Type': '═══ INSTITUTION CODES ═══', 'Code': '', 'Name/Description': '' })
  institutions.forEach(inst => {
    referenceData.push({
      'Type': 'Institution',
      'Code': inst.institution_code,
      'Name/Description': inst.institution_name || 'N/A'
    })
  })

  // Board types section
  referenceData.push({ 'Type': '═══ BOARD TYPES ═══', 'Code': '', 'Name/Description': '' })
  boardTypes.forEach(type => {
    referenceData.push({ 'Type': 'Board Type', 'Code': type, 'Name/Description': type })
  })

  // Status values section
  referenceData.push({ 'Type': '═══ STATUS VALUES ═══', 'Code': '', 'Name/Description': '' })
  ;['Active', 'Inactive'].forEach(status => {
    referenceData.push({
      'Type': 'Status',
      'Code': status,
      'Name/Description': status === 'Active' ? 'Board is active' : 'Board is inactive'
    })
  })

  const wsRef = XLSX.utils.json_to_sheet(referenceData)
  wsRef['!cols'] = [{ wch: 25 }, { wch: 20 }, { wch: 40 }]
  XLSX.utils.book_append_sheet(wb, wsRef, 'Reference Codes')

  // IMPORTANT: await is required - XLSX.writeFile is async (ExcelJS)
  await XLSX.writeFile(wb, `boards_template_${new Date().toISOString().split('T')[0]}.xlsx`)
}
```

### Data Validation Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `type` | `'list'` | Validation type (always 'list' for dropdowns) |
| `sqref` | `string` | Cell range (e.g., `'A2:A1000'`, `'B2:B100'`) |
| `formula1` | `string` | Valid values: `'"Value1,Value2,Value3"'` (with quotes) |
| `showDropDown` | `boolean` | **CRITICAL**: Must be `true` for dropdown to appear |
| `showErrorMessage` | `boolean` | Show error popup for invalid input |
| `errorTitle` | `string` | Error popup title |
| `error` | `string` | Error popup message |

### How excel-compat Handles Validation

The `lib/utils/excel-compat.ts` file processes `!dataValidation` array:

```typescript
// Inside excel-compat.ts writeFile function:
if (wsCompat['!dataValidation'] && wsCompat['!dataValidation'].length > 0) {
  // Create hidden sheet for valid values
  const validationSheet = workbook.addWorksheet('_ValidCodes')
  validationSheet.state = 'hidden'

  let colIndex = 1
  wsCompat['!dataValidation'].forEach(validation => {
    // Parse values from formula1
    let values = validation.formula1.replace(/^"|"$/g, '').split(',')

    // Write values to hidden sheet column
    values.forEach((value, rowIdx) => {
      validationSheet.getCell(rowIdx + 1, colIndex).value = value
    })

    // Check 255 character limit for inline formula
    const inlineFormula = `"${values.join(',')}"`
    const canUseInlineDropdown = inlineFormula.length <= 255

    // Apply data validation (dropdown)
    const sheetRef = `'_ValidCodes'!$${colLetter}$1:$${colLetter}$${values.length}`
    for (let row = startRow; row <= endRow; row++) {
      cell.dataValidation = {
        type: 'list',
        allowBlank: true,
        formulae: canUseInlineDropdown ? [inlineFormula] : [sheetRef],
        showErrorMessage: true,
        errorStyle: 'warning'
      }
    }

    // ALWAYS add conditional formatting for invalid values (red highlight)
    worksheet.addConditionalFormatting({
      ref: `${targetCol}${startRow}:${targetCol}${endRow}`,
      rules: [{
        type: 'expression',
        formulae: [`AND(${targetCol}${startRow}<>"",COUNTIF(${validRange},${targetCol}${startRow})=0)`],
        style: {
          fill: { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFC7CE' } },
          font: { color: { argb: 'FF9C0006' } }
        },
        priority: 1
      }]
    })

    colIndex++
  })
}
```

### How It Looks in Excel

| Institution Code * | Board Code * | Board Name * | Board Type | Status |
|-------------------|--------------|--------------|------------|--------|
| **AHS** (valid - normal, dropdown available) | CBSE | Central Board | National | Active |
| **INVALID** (red background + red text) | STATE | State Board | State | Active |
| **CAS** (valid - normal) | UNIV | University | **WRONG** (red) | Active |

### Template Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ Sheet 1: Template                                                │
├─────────────────────────────────────────────────────────────────┤
│ Institution Code * │ Board Code * │ Board Name * │ Status        │
│ ──────────────────┼──────────────┼──────────────┼───────────────│
│ [dropdown + red   │              │              │ [dropdown]     │
│  highlight if     │              │              │                │
│  invalid]         │              │              │                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Sheet 2: Reference Codes                                         │
├─────────────────────────────────────────────────────────────────┤
│ Type              │ Code         │ Name/Description              │
│ ══════════════════│══════════════│═══════════════════════════════│
│ INSTITUTION CODES │              │                               │
│ Institution       │ AHS          │ Allied Health Sciences        │
│ Institution       │ CAS          │ Arts & Science                │
│ ══════════════════│══════════════│═══════════════════════════════│
│ STATUS VALUES     │              │                               │
│ Status            │ Active       │ Record is active              │
│ Status            │ Inactive     │ Record is inactive            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Sheet 3: _ValidCodes (HIDDEN - auto-created by excel-compat)     │
├─────────────────────────────────────────────────────────────────┤
│ A (Institution)  │ B (Board Type) │ C (Status)                   │
│ AHS              │ National       │ Active                       │
│ CAS              │ State          │ Inactive                     │
│ COE              │ International  │                              │
│ ...              │ Private        │                              │
│                  │ University     │                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Import Handler Pattern

Implement the import handler in your page component:

```typescript
// State for import errors dialog
const [errorPopupOpen, setErrorPopupOpen] = useState(false)
const [importErrors, setImportErrors] = useState<Array<{
  row: number
  entity_code: string
  entity_name: string
  errors: string[]
}>>([])
const [uploadSummary, setUploadSummary] = useState<{
  total: number
  success: number
  failed: number
}>({ total: 0, success: 0, failed: 0 })

// Import with Detailed Error Tracking
const handleImport = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json,.csv,.xlsx,.xls'
  input.onchange = async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0]
    if (!file) return

    try {
      let rows: Partial<Entity>[] = []

      // Parse file based on type (JSON/CSV/Excel)
      if (file.name.endsWith('.json')) {
        const text = await file.text()
        rows = JSON.parse(text)
      } else if (file.name.endsWith('.csv')) {
        const text = await file.text()
        const lines = text.split('\n').filter(line => line.trim())
        if (lines.length < 2) {
          toast({
            title: "❌ Invalid CSV File",
            description: "CSV must have header row and at least one data row",
            variant: "destructive"
          })
          return
        }

        const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''))
        rows = lines.slice(1).map(line => {
          const values = line.split(',').map(v => v.trim().replace(/"/g, ''))
          const row: Record<string, string> = {}
          headers.forEach((header, index) => {
            row[header] = values[index] || ''
          })
          return mapRowToEntity(row)
        })
      } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
        const data = new Uint8Array(await file.arrayBuffer())
        const wb = await XLSX.read(data, { type: 'array' })
        const ws = wb.Sheets[wb.SheetNames[0]]
        const json = XLSX.utils.sheet_to_json(ws) as Record<string, unknown>[]
        rows = json.map(mapRowToEntity)
      }

      await processImportedRows(rows)
    } catch (err) {
      console.error('Import error:', err)
      setLoading(false)
      toast({
        title: "❌ Import Error",
        description: "Import failed. Please check your file format.",
        variant: "destructive"
      })
    }
  }
  input.click()
}

// Map Excel columns to entity fields
// IMPORTANT: Handle both "Field Name *" and "field_name" formats
function mapRowToEntity(row: Record<string, unknown>): Partial<Entity> {
  return {
    institution_code: String(row['Institution Code *'] || row['Institution Code'] || row['institution_code'] || ''),
    entity_code: String(row['Entity Code *'] || row['Entity Code'] || row['entity_code'] || ''),
    entity_name: String(row['Entity Name *'] || row['Entity Name'] || row['entity_name'] || ''),
    description: String(row['Description'] || row['description'] || ''),
    is_active: String(row['Status'] || row['is_active'] || '').toLowerCase() === 'active'
  }
}
```

### Row Processing with Error Tracking

```typescript
async function processImportedRows(rows: Partial<Entity>[]) {
  setLoading(true)
  const validationErrors: ImportError[] = []

  // Step 1: Client-side validation for ALL rows first
  const mapped = rows.map((r, index) => {
    const itemData = {
      // ... map fields
    }

    const errors = validateEntityData(itemData, index + 2)
    if (errors.length > 0) {
      validationErrors.push({
        row: index + 2,  // +2 for header row in Excel
        entity_code: itemData.entity_code || 'N/A',
        entity_name: itemData.entity_name || 'N/A',
        errors: errors
      })
    }

    return itemData
  }).filter(r => r.entity_code && r.entity_name)

  // Step 2: If validation errors, show popup and stop
  if (validationErrors.length > 0) {
    setImportErrors(validationErrors)
    setUploadSummary({
      total: rows.length,
      success: 0,
      failed: validationErrors.length
    })
    setErrorPopupOpen(true)
    return
  }

  // Step 3: Save valid rows to database
  let successCount = 0
  let errorCount = 0
  const uploadErrors: ImportError[] = []

  for (let i = 0; i < mapped.length; i++) {
    const item = mapped[i]
    const rowNumber = i + 2

    try {
      const response = await fetch('/api/[entity]', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item)
      })

      if (response.ok) {
        const saved = await response.json()
        setItems(prev => [saved, ...prev])
        successCount++
      } else {
        const errorData = await response.json()
        errorCount++
        uploadErrors.push({
          row: rowNumber,
          entity_code: item.entity_code || 'N/A',
          entity_name: item.entity_name || 'N/A',
          errors: [errorData.error || 'Failed to save']
        })
      }
    } catch (error) {
      errorCount++
      uploadErrors.push({
        row: rowNumber,
        entity_code: item.entity_code || 'N/A',
        entity_name: item.entity_name || 'N/A',
        errors: [error instanceof Error ? error.message : 'Network error']
      })
    }
  }

  setLoading(false)

  // Update summary
  setUploadSummary({
    total: mapped.length,
    success: successCount,
    failed: errorCount
  })

  // Show error dialog if needed
  if (uploadErrors.length > 0) {
    setImportErrors(uploadErrors)
    setErrorPopupOpen(true)
  }

  // Show toast
  showUploadToast(mapped.length, successCount, errorCount)
}
```

### Validation Function Pattern

```typescript
// Validation function for imported data
const validateEntityData = (data: any, rowIndex: number): string[] => {
  const errors: string[] = []

  // Required field validations
  if (!data.institution_code || data.institution_code.trim() === '') {
    errors.push('Institution code is required')
  }

  if (!data.entity_code || data.entity_code.trim() === '') {
    errors.push('Entity code is required')
  } else if (data.entity_code.length > 50) {
    errors.push('Entity code must be 50 characters or less')
  }

  if (!data.entity_name || data.entity_name.trim() === '') {
    errors.push('Entity name is required')
  } else if (data.entity_name.length > 255) {
    errors.push('Entity name must be 255 characters or less')
  }

  // Status validation
  if (data.is_active !== undefined && data.is_active !== null) {
    if (typeof data.is_active !== 'boolean') {
      const statusValue = String(data.is_active).toLowerCase()
      if (!['true', 'false', 'active', 'inactive'].includes(statusValue)) {
        errors.push('Status must be true/false or Active/Inactive')
      }
    }
  }

  return errors
}
```

### Toast Notification Pattern

```typescript
function showUploadToast(total: number, success: number, failed: number) {
  if (success > 0 && failed === 0) {
    toast({
      title: "✅ Upload Complete",
      description: `Successfully uploaded all ${success} row${success > 1 ? 's' : ''}.`,
      className: "bg-green-50 border-green-200 text-green-800 dark:bg-green-900/20 dark:border-green-800 dark:text-green-200",
      duration: 5000,
    })
  } else if (success > 0 && failed > 0) {
    toast({
      title: "⚠️ Partial Upload Success",
      description: `${success} successful, ${failed} failed. View error details.`,
      className: "bg-yellow-50 border-yellow-200 text-yellow-800 dark:bg-yellow-900/20 dark:border-yellow-800 dark:text-yellow-200",
      duration: 6000,
    })
  } else if (failed > 0) {
    toast({
      title: "❌ Upload Failed",
      description: `${failed} row${failed > 1 ? 's' : ''} failed. View error details.`,
      variant: "destructive",
      className: "bg-red-50 border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-800 dark:text-red-200",
      duration: 6000,
    })
  }
}
```

---

## Error Dialog Component

**Reference: `app/(coe)/master/boards/page.tsx` lines 1291-1404**

```tsx
{/* Error Dialog */}
<AlertDialog open={errorPopupOpen} onOpenChange={setErrorPopupOpen}>
  <AlertDialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
    <AlertDialogHeader>
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-full bg-red-100 dark:bg-red-900/20 flex items-center justify-center">
          <XCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
        </div>
        <div>
          <AlertDialogTitle className="text-xl font-bold text-red-600 dark:text-red-400">
            Data Validation Errors
          </AlertDialogTitle>
          <AlertDialogDescription className="text-sm text-muted-foreground mt-1">
            Please fix the following errors before importing the data
          </AlertDialogDescription>
        </div>
      </div>
    </AlertDialogHeader>

    <div className="space-y-4">
      {/* Upload Summary Cards */}
      {uploadSummary.total > 0 && (
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-blue-50 dark:bg-blue-900/10 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
            <div className="text-xs text-blue-600 dark:text-blue-400 font-medium mb-1">Total Rows</div>
            <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">{uploadSummary.total}</div>
          </div>
          <div className="bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800 rounded-lg p-3">
            <div className="text-xs text-green-600 dark:text-green-400 font-medium mb-1">Successful</div>
            <div className="text-2xl font-bold text-green-700 dark:text-green-300">{uploadSummary.success}</div>
          </div>
          <div className="bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 rounded-lg p-3">
            <div className="text-xs text-red-600 dark:text-red-400 font-medium mb-1">Failed</div>
            <div className="text-2xl font-bold text-red-700 dark:text-red-300">{uploadSummary.failed}</div>
          </div>
        </div>
      )}

      {/* Error Summary */}
      <div className="bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 rounded-lg p-4">
        <div className="flex items-center gap-2 mb-2">
          <AlertTriangle className="h-4 w-4 text-red-600 dark:text-red-400" />
          <span className="font-semibold text-red-800 dark:text-red-200">
            {importErrors.length} row{importErrors.length > 1 ? 's' : ''} failed validation
          </span>
        </div>
        <p className="text-sm text-red-700 dark:text-red-300">
          Please correct these errors in your Excel file and try uploading again.
        </p>
      </div>

      {/* Detailed Error List */}
      <div className="space-y-3">
        {importErrors.map((error, index) => (
          <div key={index} className="border border-red-200 dark:border-red-800 rounded-lg p-4 bg-red-50/50 dark:bg-red-900/5">
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="text-xs bg-red-100 text-red-800 border-red-300">
                  Row {error.row}
                </Badge>
                <span className="font-medium text-sm">
                  {error.entity_code} - {error.entity_name}
                </span>
              </div>
            </div>

            <div className="space-y-1">
              {error.errors.map((err, errIndex) => (
                <div key={errIndex} className="flex items-start gap-2 text-sm">
                  <XCircle className="h-3 w-3 text-red-500 mt-0.5 flex-shrink-0" />
                  <span className="text-red-700 dark:text-red-300">{err}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Common Fixes */}
      <div className="bg-blue-50 dark:bg-blue-900/10 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h4 className="font-semibold text-blue-800 dark:text-blue-200 text-sm mb-1">Common Fixes:</h4>
        <ul className="text-xs text-blue-700 dark:text-blue-300 space-y-1">
          <li>• Ensure institution_code references an existing institution</li>
          <li>• Entity code must be unique within the institution</li>
          <li>• Check field length constraints (code ≤ 50 chars, name ≤ 255 chars)</li>
          <li>• Status: true/false or Active/Inactive</li>
        </ul>
      </div>
    </div>

    <AlertDialogFooter>
      <AlertDialogCancel>Close</AlertDialogCancel>
      <Button onClick={() => { setErrorPopupOpen(false); setImportErrors([]) }}>
        Try Again
      </Button>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

---

## Action Buttons UI Pattern

```tsx
<div className="flex gap-1 flex-wrap">
  <Button variant="outline" size="sm" className="text-xs px-2 h-8" onClick={fetchData} disabled={loading}>
    <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
    Refresh
  </Button>
  <Button variant="outline" size="sm" className="text-xs px-2 h-8" onClick={handleTemplateExport}>
    <FileSpreadsheet className="h-3 w-3 mr-1" />
    Template
  </Button>
  <Button variant="outline" size="sm" className="text-xs px-2 h-8" onClick={handleDownload}>
    Json
  </Button>
  <Button variant="outline" size="sm" className="text-xs px-2 h-8" onClick={handleExport}>
    Download
  </Button>
  <Button variant="outline" size="sm" className="text-xs px-2 h-8" onClick={handleImport}>
    Upload
  </Button>
  <Button size="sm" className="text-xs px-2 h-8" onClick={() => setSheetOpen(true)}>
    <PlusCircle className="h-3 w-3 mr-1" />
    Add
  </Button>
</div>
```

---

## Required Imports

```typescript
import XLSX from '@/lib/utils/excel-compat'
import { Download, Upload, FileSpreadsheet, FileJson, RefreshCw, XCircle, AlertTriangle, PlusCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog'
import { useToast } from '@/hooks/common/use-toast'
```

## State Types

```typescript
interface ImportError {
  row: number
  entity_code: string
  entity_name: string
  errors: string[]
}

interface UploadSummary {
  total: number
  success: number
  failed: number
}
```

---

## Key Implementation Details

| Feature | Implementation |
|---------|----------------|
| **Dropdown + Red Highlight** | Use `!dataValidation` array with `showDropDown: true` |
| **255 char limit handling** | excel-compat auto-uses hidden sheet reference for long lists |
| **Conditional formatting** | ALWAYS applied - invalid values get red bg + text |
| **Reference sheet** | Use `═══` separators for visual grouping |
| **Async writeFile** | Always use `await XLSX.writeFile()` |
| **Row number in errors** | Use `index + 2` (header = row 1) |
| **Status mapping** | Accept both `Active/Inactive` and `true/false` |
| **Header mapping** | Handle `Field Name *` and `field_name` formats |

---

## Checklist for New Entity

1. ☐ Create utility file `lib/utils/[entity-name]/export-import.ts`
2. ☐ Add export functions: `exportToJSON`, `exportToExcel`, `exportTemplate`
3. ☐ **Identify ALL reference data sources:**
   - Entity lookups (institutions, courses, sessions, etc.)
   - MyJKKN data (programs, semesters, batches, regulations)
   - Dropdown/enum values (exam_type, status, grade_type, etc.)
   - Boolean fields (is_active → Active/Inactive)
4. ☐ Add import error state to page component
5. ☐ Add button group in page header
6. ☐ Implement `handleImport` with file parsing
7. ☐ **Add data validations with `showDropDown: true`**
8. ☐ Implement validation function for import
9. ☐ Add Error Dialog component
10. ☐ Test with JSON, CSV, and Excel files
11. ☐ **Verify invalid values show RED highlight**
12. ☐ **Use `await` with XLSX.writeFile()** (ExcelJS is async)

## Testing Checklist

- [ ] JSON export works for filtered data
- [ ] Excel export includes all visible columns
- [ ] Template has empty row with `*` markers for required fields
- [ ] **Dropdown appears for short value lists (<255 chars)**
- [ ] **Invalid values are highlighted in RED**
- [ ] **Long value lists still get red highlighting (via hidden sheet)**
- [ ] Reference Codes sheet has all valid values with separators
- [ ] JSON import parses correctly
- [ ] CSV import handles quoted values
- [ ] Excel import reads first sheet
- [ ] Validation errors show row numbers
- [ ] API errors are captured and displayed
- [ ] Upload summary shows correct counts
- [ ] Toast notifications appear for all cases
- [ ] Error dialog is scrollable for many errors
