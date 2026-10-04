---
name: marketing-genius
description: Generate buyer psychology + ad copy. Use when user wants marketing insights, ad copy, or value propositions.
---

# Marketing Genius

Generate buyer psychology + ad copy for any product.

## Usage

Tell OpenClaw:
```
用marketing-genius分析 [产品]，受众是[受众]
```

## What it does

1. Analyze product (URL or description)
2. Generate 3 cognitive shortcuts (heuristics)
3. Generate 5 ad copy variations

## API

POST https://1agent.fyi/api

```json
{
  "product": "Your product",
  "audience": "Target audience",
  "lang": "en" or "zh",
  "copyCount": 5
}
```

## Output

```json
{
  "heuristics": [
    {"shortcut": "...", "explanation": "...", "applicationExample": "..."}
  ],
  "messaging": {...},
  "adCopy": [...]
}
```
