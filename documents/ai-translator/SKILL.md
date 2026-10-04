---
name: ai-translator
description: "Advanced AI translation with context awareness, terminology management, and quality scoring. Supports 100+ languages."
triggers:
  - "translate text"
  - "翻译"
  - "多语言翻译"
  - "localization"
  - "国际化"
---

# AI Translator

Context-aware translation with quality scoring.

## Features

- 🌍 **100+ Languages** — Major and rare languages
- 🧠 **Context Aware** — Understands domain context
- 📚 **Terminology** — Custom glossary support
- ✅ **Quality Score** — Confidence rating
- 🔄 **Batch Translate** — Multiple files at once

## Supported Formats

| Format | Input | Output |
|--------|-------|--------|
| Text | ✅ | ✅ |
| Markdown | ✅ | ✅ |
| JSON | ✅ | ✅ |
| HTML | ✅ | ✅ |
| Subtitles | ✅ | ✅ |
| Documents | ✅ | ✅ |

## Usage

### Text Translation

```bash
# Simple translation
hermes translate "Hello world" --to zh

# With context
hermes translate "Apple is great" --to zh --context technology

# Multiple languages
hermes translate "Welcome" --to zh,ja,ko,es
```

### File Translation

```bash
# Translate document
hermes translate file README.md --to zh

# Translate JSON (i18n)
hermes translate file en.json --to zh,ja,ko

# Batch translate directory
hermes translate dir ./docs/ --to zh
```

### Subtitle Translation

```bash
# Translate SRT file
hermes translate subtitles video.srt --to zh

# With timing preservation
hermes translate subtitles video.srt --to zh --preserve-timing
```

## Quality Scoring

Each translation gets a quality score:

| Score | Quality | Recommendation |
|-------|---------|----------------|
| 95-100 | Excellent | Use directly |
| 85-94 | Good | Minor review |
| 70-84 | Fair | Review needed |
| <70 | Poor | Rewrite recommended |

## Terminology Management

### Custom Glossary

```yaml
# glossary.yml
terms:
  - source: "machine learning"
    target_zh: "机器学习"
    target_ja: "機械学習"
    context: technology
  
  - source: "cloud computing"
    target_zh: "云计算"
    context: technology
```

### Usage

```bash
# Translate with glossary
hermes translate file doc.md --to zh --glossary glossary.yml

# Update glossary from translations
hermes translate learn --from translated.md --glossary glossary.yml
```

## Localization Workflow

```bash
# Initialize i18n
hermes translate init --framework nextjs

# Extract strings
hermes translate extract ./src/

# Translate all
hermes translate all --to zh,ja,ko

# Verify translations
hermes translate verify ./locales/
```

## Integration

### React/Next.js

```typescript
// useTranslation hook
import { useTranslation } from 'hermes-i18n';

function Component() {
  const { t } = useTranslation();
  return <h1>{t('welcome')}</h1>;
}
```

### API

```python
from hermes import Translator

translator = Translator(api_key="...")

result = translator.translate(
    text="Hello world",
    target_lang="zh",
    context="greeting"
)

print(result.translation)  # "你好世界"
print(result.quality)       # 98
```

## Pitfalls

1. **Context Matters** — Always provide context for accurate translation
2. **Review Critical Content** — Machine translation for legal/medical needs human review
3. **Glossary Maintenance** — Keep glossary updated for consistency
4. **Character Limits** — Some languages expand (German) or contract (Chinese)
5. **Cultural Adaptation** — Direct translation may not convey same meaning
