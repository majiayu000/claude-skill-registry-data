---
name: gemini-file-api
description: Work with Gemini File API for document caching and efficient multi-query workflows. Use when discussing file uploads, caching strategies, token optimization, or comparing File API vs inline document approaches.
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Gemini File API Integration

## Purpose
Understand and work with Gemini's File API for efficient document processing.

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│  Document Upload                            │
│  UploadFile() -> Gemini File API           │
│  Returns: URI with 48hr TTL                │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  FileCache (in-memory)                      │
│  Prevents re-uploads within session        │
│  Key: file path, Value: FileReference      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  GenerateContent()                          │
│  References files by URI (not bytes)       │
│  Reuse same URI for multiple queries       │
└─────────────────────────────────────────────┘
```

## Client Usage

### Creating a Client
```go
// Reads GEMINI_API_KEY from environment
client, err := gemini.NewClient(ctx)
if err != nil {
    return err
}
defer client.Close()
```

### Uploading Files

**Single file:**
```go
ref, err := client.UploadFile(ctx, "/path/to/doc.pdf", "application/pdf")
// ref.URI is reusable for 48 hours
```

**Multiple files (parallel upload):**
```go
paths := []string{"/path/to/w2.pdf", "/path/to/paystub.pdf"}
mimeTypes := map[string]string{
    "/path/to/w2.pdf": "application/pdf",
    "/path/to/paystub.pdf": "application/pdf",
}
refs, err := client.UploadFiles(ctx, paths, mimeTypes)
// refs is map[string]*FileReference
```

### Generating Content

**With File API (recommended for multiple queries):**
```go
resp, err := client.GenerateContent(ctx, &gemini.GenerateRequest{
    Model:        gemini.ModelFlash,
    Prompt:       "Analyze this W2 for annual income",
    SystemPrompt: "You are a mortgage underwriter...",
    FileURIs:     []string{ref.URI},
    FileMIMEs:    map[string]string{ref.URI: "application/pdf"},
})
```

**With Inline bytes (simpler for single queries):**
```go
resp, err := client.GenerateContent(ctx, &gemini.GenerateRequest{
    Model:  gemini.ModelFlash,
    Prompt: "Analyze this document",
    InlineFiles: []gemini.InlineFile{{
        Data:     fileBytes,
        MimeType: "application/pdf",
    }},
})
```

## Data Structures

### FileReference
```go
type FileReference struct {
    Name      string    // Gemini-assigned name
    URI       string    // Reusable URI for requests
    MimeType  string
    State     string    // Processing state
    CreatedAt time.Time
    ExpiresAt time.Time // 48 hours from creation
    SizeBytes int64
}
```

### GenerateRequest
```go
type GenerateRequest struct {
    Model        string              // ModelFlash or ModelPro
    Prompt       string              // User prompt
    SystemPrompt string              // System instructions
    FileURIs     []string            // Gemini file URIs
    FileMIMEs    map[string]string   // URI -> MIME type
    InlineFiles  []InlineFile        // Direct bytes (alternative)
    Temperature  *float32
    MaxTokens    *int32
}
```

### GenerateResponse
```go
type GenerateResponse struct {
    Text           string
    FinishReason   string
    TokensUsed     int64
    ModelUsed      string
    ProcessingTime time.Duration
}
```

## Model Selection

| Model | Constant | Use Case |
|-------|----------|----------|
| Gemini Flash | `gemini.ModelFlash` | Fast, cheaper, most tasks |
| Gemini Pro | `gemini.ModelPro` | Complex reasoning, escalation |

## File API vs Inline Comparison

| Aspect | File API | Inline |
|--------|----------|--------|
| Upload | Once (cached 48hr) | Every request |
| Best for | Multiple queries, same docs | Single query |
| Token cost | Lower per query | Higher per query |
| Latency | Higher first query | Consistent |
| Break-even | ~7 queries | N/A |

## FileCache Details

Located in `internal/gemini/cache.go`:
- **Thread-safe**: Uses RWMutex
- **Expiry-aware**: Checks 48hr TTL before returning
- **Methods**: Get, Set, Delete, Cleanup, GetAllURIs

## Troubleshooting

### "GEMINI_API_KEY not set"
```bash
export GEMINI_API_KEY="your-key"
```

### Upload failures
- Check file exists and is readable
- Verify MIME type matches content
- Check file size limits

### Rate limits
Add delays between requests:
```go
time.Sleep(500 * time.Millisecond)
```

## Related Files
- `internal/gemini/client.go` - Main client implementation
- `internal/gemini/cache.go` - FileCache implementation
- `cmd/benchmark/main.go` - Performance comparison tool
