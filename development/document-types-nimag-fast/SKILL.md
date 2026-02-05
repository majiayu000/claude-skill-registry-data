---
name: document-types
description: Understand and work with mortgage document types and classification. Use when asking about document types, adding new document support, debugging classification, or understanding what DocType constants mean.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Mortgage Document Types

## Purpose
Work with document classification in the mortgage underwriting system.

## Document Type Constants

Located in `internal/model/document.go`:

### Income Documents
| Constant | Description | Filename Patterns |
|----------|-------------|-------------------|
| `DocTypeW2` | W-2 wage statements | `*w2*`, `*w-2*` |
| `DocType1099` | 1099 contractor income | `*1099*` |
| `DocTypePaystub` | Pay stubs/earnings | `*paystub*`, `*pay_stub*`, `*pay-stub*`, `*earnings*` |
| `DocTypeTaxReturn` | Tax returns (1040) | `*tax*`, `*1040*` |
| `DocTypeProfitLoss` | P&L statements | `*profit*`, `*p&l*`, `*pnl*` |
| `DocTypeEmploymentLetter` | Employment verification | `*employment*`, `*verification*` |

### Asset Documents
| Constant | Description | Filename Patterns |
|----------|-------------|-------------------|
| `DocTypeBankStatement` | Bank statements | `*bank*` |
| `DocTypeAssetStatement` | General assets | `*asset*` |
| `DocTypeRetirementStmt` | 401k/IRA statements | `*retirement*`, `*401k*`, `*ira*` |
| `DocTypeGiftLetter` | Gift fund letters | `*gift*` |

### Credit Documents
| Constant | Description | Filename Patterns |
|----------|-------------|-------------------|
| `DocTypeCreditReport` | Credit bureau reports | `*credit*` |
| `DocTypeDebtPayoff` | Debt payoff letters | `*payoff*`, `*debt*` |

### Collateral Documents
| Constant | Description | Filename Patterns |
|----------|-------------|-------------------|
| `DocTypeAppraisal` | Property appraisals | `*appraisal*` |
| `DocTypePurchaseContract` | Purchase agreements | `*purchase*`, `*contract*` |
| `DocTypeTitleReport` | Title reports | `*title*` |
| `DocTypePropertyInsurance` | Hazard insurance | `*insurance*`, `*hazard*`, `*homeowner*` |

## Type Inference Logic

Located in `internal/document/store.go`:

```go
// Files are classified by checking if filename contains pattern
lower := strings.ToLower(filepath.Base(path))
for pattern, docType := range patterns {
    if strings.Contains(lower, pattern) {
        return docType
    }
}
```

## Adding a New Document Type

### Step 1: Add constant to `internal/model/document.go`
```go
const (
    // ... existing types ...
    DocTypeNewType DocumentType = "new_type"
)
```

### Step 2: Add pattern to `internal/document/store.go`
```go
patterns := map[string]model.DocumentType{
    // ... existing patterns ...
    "new_pattern": model.DocTypeNewType,
}
```

### Step 3: Add to agent's document lists
In the relevant agent (e.g., `internal/agent/income/income.go`):
```go
func (a *Agent) RequiredDocuments() []model.DocumentType {
    return []model.DocumentType{
        model.DocTypeW2,
        model.DocTypeNewType,  // Add here
    }
}
```

### Step 4: Update prompts
Update the agent's prompt to describe how to handle the new document type.

## Document Structure

```go
type Document struct {
    ID            string            // Hash-based unique ID
    ApplicationID string            // Loan application ID
    Type          DocumentType      // One of the DocType* constants
    FileName      string            // Original filename
    MimeType      string            // application/pdf, image/png, etc.
    FilePath      string            // Local filesystem path
    GeminiURI     string            // Cached Gemini File API URI
    UploadedAt    time.Time
    BorrowerID    string
    Year          int               // Tax year for tax docs
    Period        string            // Pay period for paystubs
    Metadata      map[string]string // Additional metadata
}
```

## Supported MIME Types

From `internal/document/store.go:MimeTypeFromExtension`:
- `.pdf` -> `application/pdf`
- `.png` -> `image/png`
- `.jpg`, `.jpeg` -> `image/jpeg`
- `.gif` -> `image/gif`
- `.webp` -> `image/webp`

## Related Files
- `internal/model/document.go` - Type definitions
- `internal/document/store.go` - Loading and type inference
- `cmd/underwriter/main.go` - CLI type inference
