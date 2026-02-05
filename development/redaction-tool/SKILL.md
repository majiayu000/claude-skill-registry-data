---
name: redaction-tool
description: |
  Development skill for CaseMark's Smart Redaction Tool - an intelligent document 
  redaction application with two-pass PII detection combining regex patterns and 
  AI-powered semantic analysis. Built with Next.js 14, pdf.js/pdf-lib, and Case.dev 
  LLMs. Use this skill when: (1) Working on the redaction-tool codebase, (2) Adding 
  or modifying regex patterns, (3) Implementing AI detection features, (4) Building 
  PDF export functionality, or (5) Adding new PII types.
---

# Redaction Tool Development Guide

An intelligent document redaction application with two-pass PII detection—regex patterns for standard formats plus AI semantic analysis for contextual data.

**Live site**: https://redaction-tool.casedev.app/

## Architecture

```
src/
├── app/
│   ├── page.tsx                    # Main application UI
│   └── api/
│       ├── detect-pii/             # Two-pass PII detection
│       ├── export-pdf/             # PDF generation
│       ├── detect/                 # Database-backed detection
│       ├── export/                 # Database-backed export
│       ├── jobs/                   # Job management
│       └── upload/                 # File upload
├── components/
│   ├── redaction/
│   │   ├── PatternSelector.tsx     # Redaction type selection
│   │   ├── EntityList.tsx          # Detected entities
│   │   └── DocumentPreview.tsx     # Preview with highlights
│   ├── upload/
│   │   └── DropZone.tsx            # File upload
│   └── ui/                         # shadcn components
└── lib/
    ├── redaction/
    │   ├── detector.ts             # Two-pass detection logic
    │   └── patterns.ts             # Regex patterns & presets
    ├── case-dev/
    │   └── client.ts               # Case.dev API client
    ├── db.ts                       # Database connection
    └── utils.ts                    # Utilities
```

## Core Workflow

```
Upload Doc → Extract Text → Pass 1: Regex → Pass 2: AI → Review → Export PDF
     ↓            ↓             ↓              ↓           ↓          ↓
  PDF/TXT      pdf.js       SSN, CC,       Names,      Toggle      Redacted
  images       extraction   phone, email   addresses   entities    document
                            patterns       context
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React, Tailwind CSS |
| UI | shadcn/ui |
| PDF Processing | pdf.js (extract), pdf-lib (generate) |
| AI Detection | Case.dev LLM (GPT-4o) |
| Database | PostgreSQL + Prisma (optional) |

## Key Features

| Feature | Description |
|---------|-------------|
| Two-Pass Detection | Regex + AI for comprehensive coverage |
| PII Types | SSN, bank accounts, credit cards, names, addresses, phone, email, DOB |
| Presets | Pre-configured redaction profiles |
| Entity Review | Toggle, edit masked values |
| PDF Export | Generate redacted documents |
| Audit Log | Track what was redacted |

## Two-Pass Detection

See [references/pii-detection.md](references/pii-detection.md) for patterns and AI prompts.

### Pass 1: Regex (Fast, High-Precision)
- SSN: `XXX-XX-XXXX` with validation
- Credit cards: Luhn-valid patterns
- Phone: US formats
- Email: Standard format
- Dates: Common formats

### Pass 2: AI/LLM (Semantic, Aggressive)
- Non-standard formats ("SSN: one two three...")
- Contextual references ("my social is...")
- Names and addresses
- OCR errors and typos
- Obfuscated data

## Redaction Presets

| Preset | Types Included |
|--------|----------------|
| SSNs and Financial | SSN, Account Numbers, Credit Cards |
| All Personal Information | All PII types |
| Contact Information Only | Phone, Email |
| Financial Only | Account Numbers, Credit Cards |

## Case.dev Integration

See [references/casedev-redaction-api.md](references/casedev-redaction-api.md) for API patterns.

### LLM Detection
```typescript
const aiEntities = await detectWithLLM(text, piiTypes);
```

### OCR for Images
```typescript
const text = await extractTextFromImage(imageUrl);
```

## Development

### Setup
```bash
npm install
cp .env.example .env
# Add CASEDEV_API_KEY
npm run dev
```

### Environment
```
CASEDEV_API_KEY=sk_case_...               # Required
DATABASE_URL=postgresql://...             # Optional for job persistence
```

### Database (Optional)
```bash
npx prisma migrate dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/detect-pii | Two-pass PII detection |
| POST | /api/export-pdf | Generate redacted PDF |
| POST | /api/upload | File upload |
| GET | /api/jobs | List jobs |
| GET | /api/jobs/:id | Get job status |

## Common Tasks

### Adding a New PII Type
1. Add regex pattern to `lib/redaction/patterns.ts`
2. Add to AI prompt in `lib/redaction/detector.ts`
3. Add UI toggle in `PatternSelector.tsx`
4. Add masking function

### Improving AI Detection
Modify the LLM prompt to be more/less aggressive or handle specific formats.

### Adding Export Format
1. Add generation function in `lib/export/`
2. Add endpoint in `api/export-[format]/`
3. Add UI option

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Regex missing PII | Check pattern, add variations |
| AI too aggressive | Adjust prompt confidence |
| PDF export fails | Verify pdf-lib compatibility |
| OCR errors | Use higher quality images |
