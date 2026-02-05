---
name: translate
description: Translates text between languages using Google Translate. Use when you need to translate text from one language to another.
allowed-tools: Bash
---

# Translate Skill

This skill translates text between different languages using Claude's native translation capabilities or direct API calls.

## Instructions

To translate text:
1. Accept the text to translate, source language, and target language as parameters
2. Use Claude's multilingual understanding to translate the text directly
3. Return the translated text accurately

## Supported Languages

Common language codes:
- `en` - English
- `fr` - French
- `es` - Spanish
- `he` - Hebrew (עברית)
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `zh-CN` - Chinese (Simplified)
- `ja` - Japanese
- `ar` - Arabic

## Implementation

Use Claude's native multilingual capabilities to:
- Read the input text in the source language
- Understand its semantic meaning
- Generate an accurate translation in the target language
- Preserve the meaning while adapting to target language conventions

## Usage Example

Input: "The quick brown fox jumps over the lazy dog"
Source: English (en)
Target: French (fr)
Output: "Le rapide renard brun saute par-dessus le chien paresseux"

## Notes

- Translation quality leverages Claude's multilingual training
- Very long texts may need to be handled carefully
- Some languages may have different conventions for formatting
- Handle right-to-left languages (Hebrew, Arabic) with proper encoding
- **NO PYTHON CODE** - Use Claude's native translation capabilities only
