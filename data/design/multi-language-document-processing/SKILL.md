---
name: multi-language-document-processing
description: Process documents in multiple languages with focus on low-resource languages, accented character systems, and cross-linguistic content analysis. Use when working with minority languages, mixed-language documents, or documents with special characters and diacritical marks.
---

# Multi-Language Document Processing

## Overview

A specialized skill for processing documents in multiple languages, with particular focus on low-resource languages, accented character systems, and cross-linguistic content analysis. Designed to handle the unique challenges of processing minority languages alongside major languages.

## Capabilities

- **Low-Resource Language Support**: Optimized for languages with limited digital resources
- **Accent Character Handling**: Proper processing of diacritical marks and special characters
- **Cross-Linguistic Analysis**: Identify and separate content in different languages
- **Cultural Context Preservation**: Maintain cultural and linguistic nuances
- **Mixed-Language Processing**: Handle documents with multiple languages
- **Character Encoding Management**: Robust handling of various text encodings

## Core Components

### 1. Language Detection and Separation

Identify and categorize content by language within mixed-language documents.

**Detection Methods**:

- **Character pattern analysis**: Accented characters, script systems
- **Word frequency analysis**: Common words in each language
- **Grammatical pattern recognition**: Language-specific structures
- **Dictionary-based lookup**: Known vocabulary matching

**Implementation**:

```python
class MultiLanguageDetector:
    def __init__(self):
        self.language_patterns = {
            'chuukese': re.compile(r'[áéíóúàèìòùāēīōūâêîôû]'),
            'english': re.compile(r'^[a-zA-Z\s\-\']+$'),
            'spanish': re.compile(r'[ñáéíóúüÁÉÍÓÚÜ]'),
            'french': re.compile(r'[àâäéèêëïîôöùûüÿç]')
        }
    
    def detect_language(self, text):
        """Detect primary language of text segment"""
        scores = {}
        for lang, pattern in self.language_patterns.items():
            matches = len(pattern.findall(text))
            scores[lang] = matches / max(len(text.split()), 1)
        
        return max(scores, key=scores.get)
```

### 2. Processing Strategies

#### Segmented Processing

```python
def process_multilingual_document(document):
    # Detect language segments
    segments = detect_language_segments(document.text)
    
    processed_segments = []
    for segment in segments:
        if segment.language == 'chuukese':
            processed = process_chuukese_segment(segment)
        elif segment.language == 'english':
            processed = process_english_segment(segment)
        else:
            processed = process_general_segment(segment)
        
        processed_segments.append(processed)
    
    return combine_processed_segments(processed_segments)
```

#### Unicode Normalization

```python
import unicodedata

def normalize_text(text, form='NFC'):
    normalized = unicodedata.normalize(form, text)
    return normalize_chuukese_accents(normalized)

def normalize_chuukese_accents(text):
    # Convert common accent variations to standard form
    accent_mappings = {
        'á': 'á',  # Ensure consistent acute accent
        'ā': 'ā',  # Ensure consistent macron
    }
    
    for variant, standard in accent_mappings.items():
        text = text.replace(variant, standard)
    
    return text
```

## Best Practices

1. **Encoding consistency**: Always use UTF-8 for internal processing
2. **Normalization**: Apply Unicode normalization early in the pipeline
3. **Validation**: Multiple validation methods for language detection
4. **Context preservation**: Maintain cultural context in processing
5. **Fallback strategies**: Graceful degradation for unrecognized content

## Dependencies

- `unicodedata`: Unicode text normalization
- `chardet`: Character encoding detection
- `langdetect`: Language identification support
- `regex`: Enhanced regular expression support for Unicode
