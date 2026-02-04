---
name: vlex
description: Interacts with vLex legal APIs for document search, anonymization, citation extraction, and classification. Use when needing international legal documents, PII removal, or legal text analysis. Requires VLEX_API_KEY environment variable.
---

# vLex API Skill

Use this skill to interact with the vLex legal document APIs.

## Setup

Before using this skill, ensure the following environment variables are set:
- `VLEX_API_KEY` - Your vLex subscription key from the Developer Portal

## Available Operations

### 1. Anonymise Text
Remove personally identifiable information (PII) from legal text.

```bash
curl -X POST "https://api.vlex.com/anonymisation/analyse" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: $VLEX_API_KEY" \
  -d '{
    "text": "The contract between John Smith and Acme Corp was signed on January 15, 2024."
  }'
```

### 2. Search Legal Documents
Search the vLex legal document database.

```bash
curl -X GET "https://api.vlex.com/search" \
  -H "Ocp-Apim-Subscription-Key: $VLEX_API_KEY" \
  -G \
  --data-urlencode "query=class action COVID-19" \
  --data-urlencode "jurisdiction=US" \
  --data-urlencode "document_type=statute"
```

### 3. Get Document by ID
Retrieve a specific legal document.

```bash
curl -X GET "https://api.vlex.com/documents/{document_id}" \
  -H "Ocp-Apim-Subscription-Key: $VLEX_API_KEY"
```

### 4. Extract Citations
Extract legal citations from text.

```bash
curl -X POST "https://api.vlex.com/citations/extract" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: $VLEX_API_KEY" \
  -d '{
    "text": "As established in Brown v. Board of Education, 347 U.S. 483 (1954)..."
  }'
```

### 5. Classify Document
Classify a legal document by type and jurisdiction.

```bash
curl -X POST "https://api.vlex.com/classification/analyse" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: $VLEX_API_KEY" \
  -d '{
    "text": "Your legal document text here..."
  }'
```

### 6. Extract Key Phrases
Extract key legal phrases and concepts from text.

```bash
curl -X POST "https://api.vlex.com/keyphrases/extract" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: $VLEX_API_KEY" \
  -d '{
    "text": "Your legal document text here..."
  }'
```

## Response Format

All APIs return JSON responses. Example anonymisation response:

```json
{
  "original_text": "The contract between John Smith and Acme Corp...",
  "anonymised_text": "The contract between [PERSON] and [ORGANIZATION]...",
  "entities": [
    {"type": "PERSON", "value": "John Smith", "start": 21, "end": 31},
    {"type": "ORGANIZATION", "value": "Acme Corp", "start": 36, "end": 45}
  ]
}
```

## Notes

- API base URL: `https://api.vlex.com`
- Authentication: Uses `Ocp-Apim-Subscription-Key` header (Azure API Management style)
- Get your API key from: https://developer.vlex.com
- Rate limits and quotas depend on your subscription tier
- Supported output formats: JSON, XML, LDML

## Reference

- Developer Portal: https://developer.vlex.com
- API Documentation: https://developer.vlex.com/apis
- Support: https://support.vlex.com
