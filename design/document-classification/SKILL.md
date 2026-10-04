---
name: document-classification
description: Use when working on document classification — `classify_document` tool, OCR pipeline, document type taxonomy for insurance/pension documents.
---

# Document Classification skill

## When to invoke

- Touching `src/tools/classify-document.ts`
- Defining or extending document type taxonomy
- Designing OCR → classification flow
- Writing tests for the classifier

## Document taxonomy (initial)

| Type | Hebrew | Triggers |
|------|--------|----------|
| `id_card` | תעודת זהות | "תעודת זהות", ID number patterns |
| `pension_statement` | דוח פנסיה | קרן פנסיה, יתרה צבורה |
| `gemel_statement` | דוח גמל | גמל, השתלמות |
| `policy_document` | פוליסה | פוליסה, ביטוח מנהלים |
| `loan_document` | מסמך הלוואה | הלוואה |
| `severance_form` | טופס פיצויים | פיצויים, סיום עבודה |
| `salary_slip` | תלוש שכר | תלוש, שכר |
| `medical_form` | טופס רפואי | הצהרת בריאות |
| `power_of_attorney` | ייפוי כוח | ייפוי כוח |
| `unknown` | לא ידוע | (fallback) |

## Classification policy

- Use Claude Haiku (cheap, fast) — model `claude-haiku-4-5-20251001`
- **Confidence threshold**: if classifier confidence < 0.75 → return `unknown` + flag for human
- Always preserve original file path
- Log every classification decision (input snippet, output type, confidence, model)
- Never throw away the original — store classification metadata alongside

## Output schema

```ts
{
  document_type: DocumentType;
  confidence: number;            // 0-1
  reasoning: string;             // why this type
  hebrew_label: string;          // for UI/CRM
  requires_review: boolean;      // true if confidence < threshold
}
```
