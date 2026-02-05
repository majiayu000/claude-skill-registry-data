---
name: localization-urdu
description: Provide per-chapter Urdu translation toggle and manage translated content delivery. Use when translating chapters, caching translations, or implementing language toggles.
---

# Localization Urdu Skill

## Instructions

1. **Translation pipeline**
   - Extract sections by heading from source Markdown/MDX
   - Translate via OpenAI/ChatKit translation model
   - Keep glossary for robotics terms (JSON file)
   - Cache translations with checksum per section
   - Rerun only when source checksum changes

2. **Storage**
   - Option A: Markdown copies (`.ur.mdx`) alongside English
   - Option B: Neon table `translations(section_id, lang, content)`
   - Tag Qdrant payload with `lang` for bilingual RAG

3. **Frontend**
   - Add language toggle in Docusaurus layout
   - Load Urdu content when available, fallback to English
   - Ensure chat widget passes desired language to backend

4. **Quality**
   - Spot-check key technical terms
   - Allow glossary overrides via JSON config
   - Keep technical terms consistent across chapters

## Examples

```python
# Translation function
async def translate_section(content: str, glossary: dict) -> str:
    prompt = f"""Translate to Urdu. Keep technical terms from glossary.
    Glossary: {glossary}
    
    Content: {content}
    """
    # Call OpenAI
    return translated_content
```

```json
// glossary.json
{
  "Physical AI": "فزیکل اے آئی",
  "Humanoid Robot": "ہیومنائیڈ روبوٹ",
  "ROS 2": "ROS 2",
  "NVIDIA Isaac": "NVIDIA Isaac"
}
```

## Definition of Done

- Translation pipeline runs and caches results; reruns are incremental
- Urdu toggle renders translated sections for at least one sample chapter
- Backend can return Urdu-context answers when requested
