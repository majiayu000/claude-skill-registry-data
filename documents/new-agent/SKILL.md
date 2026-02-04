---
name: new-agent
description: Create a new underwriting agent (assets, credit, collateral) following established patterns. Use when implementing new agents, extending the system with new document analysis capabilities, or understanding how agents work.
---

# Create New Underwriting Agent

## Purpose
Create new agents for assets, credit, or collateral analysis following the income agent pattern.

## Agent Interface

All agents must implement this interface from `internal/agent/agent.go`:

```go
type Agent interface {
    Type() AgentType
    Name() string
    RequiredDocuments() []model.DocumentType
    OptionalDocuments() []model.DocumentType
    Dependencies() []AgentType
    Analyze(ctx context.Context, input *AnalysisInput) (*model.AnalysisResult, error)
    CanProceed(docs []*model.Document) (bool, []model.DocumentType)
}
```

## Agent Types

```go
const (
    AgentTypeIncome     AgentType = "income"
    AgentTypeAssets     AgentType = "assets"
    AgentTypeCredit     AgentType = "credit"
    AgentTypeCollateral AgentType = "collateral"
)
```

## Step-by-Step Guide

### 1. Create Directory Structure
```bash
mkdir -p internal/agent/<agentname>
```

### 2. Create Agent File

Use this template based on `internal/agent/income/income.go`:

```go
package <agentname>

import (
    "context"
    "encoding/json"
    "fmt"
    "strings"
    "time"

    "github.com/nimag/fast/internal/agent"
    "github.com/nimag/fast/internal/gemini"
    "github.com/nimag/fast/internal/guidelines"
    "github.com/nimag/fast/internal/model"
)

type Agent struct {
    gemini     *gemini.Client
    guidelines string
}

type Config struct {
    GuidelinesPath string
}

func New(geminiClient *gemini.Client) *Agent {
    return &Agent{gemini: geminiClient}
}

func NewWithConfig(geminiClient *gemini.Client, cfg Config) *Agent {
    a := &Agent{gemini: geminiClient}

    if cfg.GuidelinesPath != "" {
        loader := guidelines.NewLoader(cfg.GuidelinesPath)
        // Load appropriate section: "assets", "credit", or "collateral"
        if content, err := loader.LoadSection("<section>"); err == nil {
            a.guidelines = content
        }
    }
    return a
}

func (a *Agent) Type() agent.AgentType {
    return agent.AgentType<Name>
}

func (a *Agent) Name() string {
    return "<Name> Verification Agent"
}

func (a *Agent) RequiredDocuments() []model.DocumentType {
    return []model.DocumentType{
        // Add required document types
    }
}

func (a *Agent) OptionalDocuments() []model.DocumentType {
    return []model.DocumentType{
        // Add optional document types
    }
}

func (a *Agent) Dependencies() []agent.AgentType {
    return nil // Or list dependent agents
}

func (a *Agent) CanProceed(docs []*model.Document) (bool, []model.DocumentType) {
    required := a.RequiredDocuments()
    // Check if required docs are present
    // Return (true, nil) if can proceed
    // Return (false, missingTypes) if cannot
}

func (a *Agent) Analyze(ctx context.Context, input *agent.AnalysisInput) (*model.AnalysisResult, error) {
    // 1. Filter documents for this agent
    // 2. Build prompts
    // 3. Call Gemini
    // 4. Parse response
    // 5. Return AnalysisResult
}
```

### 3. Document Types by Agent

**Assets Agent:**
```go
Required: DocTypeBankStatement
Optional: DocTypeAssetStatement, DocTypeRetirementStmt, DocTypeGiftLetter
```

**Credit Agent:**
```go
Required: DocTypeCreditReport
Optional: DocTypeDebtPayoff
```

**Collateral Agent:**
```go
Required: DocTypeAppraisal
Optional: DocTypePurchaseContract, DocTypeTitleReport, DocTypePropertyInsurance
```

### 4. Guidelines Section Mapping

```go
// Load the correct section for your agent
loader.LoadSection("assets")     // For assets agent
loader.LoadSection("credit")     // For credit agent
loader.LoadSection("collateral") // For collateral agent
```

### 5. Streaming Output Format

For streaming analysis with real-time progress display, prompts should output markers that `StreamFormatter` detects. See the **streaming-output** skill for the full specification.

Key markers:
```
**📋 GUIDELINE: [Section ID] - [Title]**
Status: ✅ COMPLIANT | ⚠️ ISSUE | ❌ NON-COMPLIANT

**🔍 CROSS-CHECK: [Doc1] vs [Doc2]**
Result: MATCH | MISMATCH

**🧮 INCOME CALCULATION**
Base annual salary: $X,XXX.XX
Total qualifying monthly income: $X,XXX.XX

**✅ FINAL DETERMINATION**
Status: APPROVED | DENIED | NEEDS REVIEW
```

### 6. System Prompt Pattern

```go
func (a *Agent) buildSystemPrompt() string {
    // Load guidelines - they contain the analysis instructions
    // Don't duplicate guideline content in the prompt
    if a.guidelines != "" {
        return "## Fannie Mae Guidelines\n\n" + a.guidelines
    }
    return ""
}
```

### 7. Response Parsing

Request JSON output and parse into `model.AnalysisResult`:

```go
type analysisResponse struct {
    Status           string    `json:"status"`
    Confidence       float64   `json:"confidence"`
    Summary          string    `json:"summary"`
    Findings         []finding `json:"findings"`
    Risks            []risk    `json:"risks"`
    MissingDocuments []string  `json:"missing_documents"`
}
```

### 8. Register in Main

Update `cmd/underwriter/main.go`:

```go
import "<agentname>" // Add import

// Create agent
newAgent := <agentname>.NewWithConfig(geminiClient, <agentname>.Config{
    GuidelinesPath: *guidelinesDir,
})

// Add to agents slice
agents := []agent.Agent{incomeAgent, newAgent}
```

## Reference Implementation

Study `internal/agent/income/income.go` for:
- Complete Analyze() implementation
- Prompt building patterns
- JSON response parsing
- Error handling
- Document filtering

## Related Files
- `internal/agent/agent.go` - Interface definition
- `internal/agent/income/income.go` - Reference implementation
- `internal/model/document.go` - Document types
- `internal/model/analysis.go` - Result structures
- `internal/guidelines/loader.go` - Guideline loading
- `configs/guidelines/` - Guideline files by section
