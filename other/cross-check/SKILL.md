---
name: cross-check
description: This skill should be used when the user asks to "cross check", "verify this", "is this correct", "what needs verification", "검증해줘", "크로스체크", "이거 맞아?", or after any analysis to identify points that need human verification.
arguments:
  - name: target
    description: The analysis result or claim to cross-check.
    default: ""
tools:
  - Read
  - Bash
---

# Cross-Check

> Evaluate the reliability of AI analysis results and explicitly flag the points that a human must verify.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

Cross-check the most recent analysis result or the specified content.

---

## Workflow

### Step 1: Identify the analysis target
Locate the analysis result to be checked. If the preceding conversation contains one, use that.

### Step 2: Reliability assessment

For each claim / number, evaluate:

| Item | Criterion |
|------|-----------|
| **Data grounding** | Can it be verified directly from the source data? |
| **Reference lookup** | Was it compared against any workspace reference documents under `references/`? |
| **Logical consistency** | Is the cause → effect reasoning sound? |
| **Scope coverage** | Is the analysis period / range sufficient? |
| **Explicit assumptions** | Any hidden assumptions? |

### Step 3: Output

```
■ Cross-check Results

✅ Verified (confirmable from data)
- {item}: {evidence}

⚠️ Needs verification (human must confirm on site)
- {item}: {reason} → how to verify: {method}

❌ Caution (insufficient data or assumption-based)
- {item}: {reason}

📊 Confidence: {high / medium / low}
```

### Step 4: Recommendations

For each "needs verification" item, suggest a concrete way to confirm:
- Who to ask
- What additional data to pull
- What to check in the source system or workspace
