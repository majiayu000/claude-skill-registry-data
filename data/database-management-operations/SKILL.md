---
name: database-management-operations
description: Specialized database operations for Chuukese language data including dictionary management, phrase collections, translation pairs, and linguistic metadata. Use when working with Chuukese language databases, managing translation data, or performing database operations on linguistic datasets.
---

# Database Management Operations

## Overview
A specialized skill for managing database operations specific to Chuukese language data, including dictionary entries, phrase collections, translation pairs, and linguistic metadata. Designed to handle the unique requirements of low-resource language data management with proper accent character support and cultural context preservation.

## Capabilities
- **Dictionary Data Management**: CRUD operations for Chuukese-English dictionary entries
- **Phrase Collection Management**: Handle grouped phrases and contextual expressions
- **Translation Pair Operations**: Manage bidirectional translation relationships
- **Linguistic Metadata Handling**: Store and retrieve grammatical, cultural, and phonetic information
- **Unicode Support**: Proper handling of Chuukese accented characters in database operations
- **Search and Filtering**: Advanced search capabilities with fuzzy matching and cultural context

## Core Components

### 1. Database Schema Design for Chuukese Data

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class DictionaryEntry(Base):
    __tablename__ = 'dictionary_entries'
    
    id = Column(Integer, primary_key=True)
    chuukese_word = Column(String(200), nullable=False, index=True)
    english_definition = Column(Text, nullable=False)
    pronunciation = Column(String(300))  # IPA or phonetic guide
    part_of_speech = Column(String(50))
    cultural_context = Column(Text)
    difficulty_level = Column(String(20))  # beginner, intermediate, advanced
    usage_frequency = Column(Float)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    phrases = relationship("PhraseEntry", back_populates="dictionary_entry")
    translations = relationship("TranslationPair", foreign_keys="TranslationPair.chuukese_entry_id")

class PhraseEntry(Base):
    __tablename__ = 'phrase_entries'
    
    id = Column(Integer, primary_key=True)
    chuukese_phrase = Column(Text, nullable=False)
    english_translation = Column(Text, nullable=False)
    context_category = Column(String(100))  # family, formal, casual, traditional
    cultural_significance = Column(Text)
    usage_notes = Column(Text)
    dictionary_entry_id = Column(Integer, ForeignKey('dictionary_entries.id'))
    
    # Relationships
    dictionary_entry = relationship("DictionaryEntry", back_populates="phrases")

class TranslationPair(Base):
    __tablename__ = 'translation_pairs'
    
    id = Column(Integer, primary_key=True)
    chuukese_text = Column(Text, nullable=False)
    english_text = Column(Text, nullable=False)
    quality_score = Column(Float)  # Translation quality assessment
    cultural_preservation_score = Column(Float)
    linguistic_accuracy_score = Column(Float)
    human_validated = Column(Boolean, default=False)
    validator_notes = Column(Text)
    chuukese_entry_id = Column(Integer, ForeignKey('dictionary_entries.id'))
    
class CulturalContext(Base):
    __tablename__ = 'cultural_contexts'
    
    id = Column(Integer, primary_key=True)
    term = Column(String(200), nullable=False)
    category = Column(String(100))  # family, respect, traditional, spatial, temporal
    description = Column(Text, nullable=False)
    usage_examples = Column(Text)
    related_terms = Column(Text)  # JSON array of related term IDs
```

### 2. Database Operations Manager

```python
from sqlalchemy import create_engine, or_, and_, func
from sqlalchemy.orm import sessionmaker
import json
import re
from difflib import get_close_matches

class ChuukeseDatabaseManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Initialize text normalization for searches
        self.accent_variants = {
            'a': ['á', 'à', 'ā', 'â', 'ă'],
            'e': ['é', 'è', 'ē', 'ê', 'ĕ'],
            'i': ['í', 'ì', 'ī', 'î', 'ĭ'],
            'o': ['ó', 'ò', 'ō', 'ô', 'ŏ'],
            'u': ['ú', 'ù', 'ū', 'û', 'ŭ']
        }
    
    def normalize_for_search(self, text):
        """Normalize text for accent-insensitive searching"""
        normalized = text.lower()
        for base_char, variants in self.accent_variants.items():
            for variant in variants:
                normalized = normalized.replace(variant, base_char)
        return normalized
    
    def create_search_pattern(self, search_term):
        """Create fuzzy search pattern that handles accent variations"""
        pattern = ""
        for char in search_term.lower():
            if char in self.accent_variants:
                # Create character class for accent variations
                variants = ''.join(self.accent_variants[char])
                pattern += f"[{char}{variants}]"
            else:
                pattern += char
        return pattern

    # Dictionary Entry Operations
    def add_dictionary_entry(self, chuukese_word, english_definition, **kwargs):
        """Add new dictionary entry with optional metadata"""
        entry = DictionaryEntry(
            chuukese_word=chuukese_word,
            english_definition=english_definition,
            pronunciation=kwargs.get('pronunciation'),
            part_of_speech=kwargs.get('part_of_speech'),
            cultural_context=kwargs.get('cultural_context'),
            difficulty_level=kwargs.get('difficulty_level', 'intermediate'),
            usage_frequency=kwargs.get('usage_frequency', 0.5)
        )
        
        self.session.add(entry)
        self.session.commit()
        return entry.id
    
    def search_dictionary_entries(self, search_term, search_type='fuzzy', limit=10):
        """Search dictionary entries with accent-aware fuzzy matching"""
        if search_type == 'exact':
            results = self.session.query(DictionaryEntry).filter(
                or_(
                    DictionaryEntry.chuukese_word == search_term,
                    DictionaryEntry.english_definition.contains(search_term)
                )
            ).limit(limit).all()
        
        elif search_type == 'fuzzy':
            # Create accent-insensitive pattern
            pattern = self.create_search_pattern(search_term)
            results = self.session.query(DictionaryEntry).filter(
                or_(
                    DictionaryEntry.chuukese_word.op('~*')(pattern),
                    DictionaryEntry.english_definition.op('~*')(pattern)
                )
            ).limit(limit).all()
        
        elif search_type == 'partial':
            results = self.session.query(DictionaryEntry).filter(
                or_(
                    DictionaryEntry.chuukese_word.contains(search_term),
                    DictionaryEntry.english_definition.contains(search_term)
                )
            ).limit(limit).all()
        
        return results
    
    def get_entries_by_cultural_context(self, context_category):
        """Get entries filtered by cultural context"""
        return self.session.query(DictionaryEntry).filter(
            DictionaryEntry.cultural_context.contains(context_category)
        ).all()

    # Phrase Operations
    def add_phrase_entry(self, chuukese_phrase, english_translation, context_category=None, **kwargs):
        """Add phrase entry with cultural context"""
        phrase = PhraseEntry(
            chuukese_phrase=chuukese_phrase,
            english_translation=english_translation,
            context_category=context_category,
            cultural_significance=kwargs.get('cultural_significance'),
            usage_notes=kwargs.get('usage_notes'),
            dictionary_entry_id=kwargs.get('dictionary_entry_id')
        )
        
        self.session.add(phrase)
        self.session.commit()
        return phrase.id
    
    def search_phrases(self, search_term, context_filter=None):
        """Search phrases with optional context filtering"""
        query = self.session.query(PhraseEntry)
        
        # Apply text search
        pattern = self.create_search_pattern(search_term)
        query = query.filter(
            or_(
                PhraseEntry.chuukese_phrase.op('~*')(pattern),
                PhraseEntry.english_translation.op('~*')(pattern)
            )
        )
        
        # Apply context filter if provided
        if context_filter:
            query = query.filter(PhraseEntry.context_category == context_filter)
        
        return query.all()

    # Translation Pair Operations
    def add_translation_pair(self, chuukese_text, english_text, quality_scores=None, **kwargs):
        """Add translation pair with quality metrics"""
        translation = TranslationPair(
            chuukese_text=chuukese_text,
            english_text=english_text,
            quality_score=quality_scores.get('overall_score', 0.0) if quality_scores else 0.0,
            cultural_preservation_score=quality_scores.get('cultural_score', 0.0) if quality_scores else 0.0,
            linguistic_accuracy_score=quality_scores.get('linguistic_score', 0.0) if quality_scores else 0.0,
            human_validated=kwargs.get('human_validated', False),
            validator_notes=kwargs.get('validator_notes'),
            chuukese_entry_id=kwargs.get('chuukese_entry_id')
        )
        
        self.session.add(translation)
        self.session.commit()
        return translation.id
    
    def get_high_quality_translations(self, min_quality_score=0.8):
        """Get translations above quality threshold"""
        return self.session.query(TranslationPair).filter(
            TranslationPair.quality_score >= min_quality_score
        ).all()
    
    def get_translations_for_validation(self, limit=50):
        """Get translations that need human validation"""
        return self.session.query(TranslationPair).filter(
            and_(
                TranslationPair.human_validated == False,
                TranslationPair.quality_score > 0.5  # Basic quality threshold
            )
        ).limit(limit).all()

    # Advanced Search and Analytics
    def get_vocabulary_statistics(self):
        """Get comprehensive vocabulary statistics"""
        stats = {}
        
        # Total counts
        stats['total_dictionary_entries'] = self.session.query(DictionaryEntry).count()
        stats['total_phrases'] = self.session.query(PhraseEntry).count()
        stats['total_translation_pairs'] = self.session.query(TranslationPair).count()
        
        # Part of speech distribution
        pos_counts = self.session.query(
            DictionaryEntry.part_of_speech,
            func.count(DictionaryEntry.id)
        ).group_by(DictionaryEntry.part_of_speech).all()
        stats['part_of_speech_distribution'] = {pos: count for pos, count in pos_counts}
        
        # Difficulty level distribution
        difficulty_counts = self.session.query(
            DictionaryEntry.difficulty_level,
            func.count(DictionaryEntry.id)
        ).group_by(DictionaryEntry.difficulty_level).all()
        stats['difficulty_distribution'] = {level: count for level, count in difficulty_counts}
        
        # Cultural context categories
        context_counts = self.session.query(
            PhraseEntry.context_category,
            func.count(PhraseEntry.id)
        ).group_by(PhraseEntry.context_category).all()
        stats['cultural_context_distribution'] = {ctx: count for ctx, count in context_counts if ctx}
        
        # Quality metrics
        avg_quality = self.session.query(func.avg(TranslationPair.quality_score)).scalar()
        stats['average_translation_quality'] = float(avg_quality) if avg_quality else 0.0
        
        validated_count = self.session.query(TranslationPair).filter(
            TranslationPair.human_validated == True
        ).count()
        stats['human_validated_translations'] = validated_count
        
        return stats
    
    def find_missing_translations(self):
        """Identify dictionary entries without corresponding translation pairs"""
        entries_with_translations = self.session.query(TranslationPair.chuukese_entry_id).distinct()
        missing = self.session.query(DictionaryEntry).filter(
            ~DictionaryEntry.id.in_(entries_with_translations)
        ).all()
        
        return missing
    
    def get_cultural_term_coverage(self):
        """Analyze coverage of culturally significant terms"""
        cultural_entries = self.session.query(DictionaryEntry).filter(
            DictionaryEntry.cultural_context.isnot(None)
        ).all()
        
        coverage_report = {
            'total_cultural_terms': len(cultural_entries),
            'categories': {},
            'high_importance_missing': []
        }
        
        # Analyze by cultural categories (this would be expanded based on actual categories)
        for entry in cultural_entries:
            # Extract categories from cultural_context (assuming JSON or comma-separated)
            context = entry.cultural_context or ""
            categories = [cat.strip() for cat in context.split(',')]
            
            for category in categories:
                if category:
                    if category not in coverage_report['categories']:
                        coverage_report['categories'][category] = 0
                    coverage_report['categories'][category] += 1
        
        return coverage_report

    # Batch Operations
    def import_dictionary_batch(self, entries_data):
        """Import multiple dictionary entries from structured data"""
        import_results = {
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        for entry_data in entries_data:
            try:
                self.add_dictionary_entry(
                    chuukese_word=entry_data['chuukese_word'],
                    english_definition=entry_data['english_definition'],
                    pronunciation=entry_data.get('pronunciation'),
                    part_of_speech=entry_data.get('part_of_speech'),
                    cultural_context=entry_data.get('cultural_context'),
                    difficulty_level=entry_data.get('difficulty_level', 'intermediate')
                )
                import_results['successful'] += 1
                
            except Exception as e:
                import_results['failed'] += 1
                import_results['errors'].append({
                    'entry': entry_data,
                    'error': str(e)
                })
        
        return import_results
    
    def export_dictionary_data(self, format_type='json', filters=None):
        """Export dictionary data in specified format"""
        query = self.session.query(DictionaryEntry)
        
        # Apply filters if provided
        if filters:
            if 'part_of_speech' in filters:
                query = query.filter(DictionaryEntry.part_of_speech == filters['part_of_speech'])
            if 'difficulty_level' in filters:
                query = query.filter(DictionaryEntry.difficulty_level == filters['difficulty_level'])
            if 'cultural_context' in filters:
                query = query.filter(DictionaryEntry.cultural_context.contains(filters['cultural_context']))
        
        entries = query.all()
        
        if format_type == 'json':
            return [
                {
                    'id': entry.id,
                    'chuukese_word': entry.chuukese_word,
                    'english_definition': entry.english_definition,
                    'pronunciation': entry.pronunciation,
                    'part_of_speech': entry.part_of_speech,
                    'cultural_context': entry.cultural_context,
                    'difficulty_level': entry.difficulty_level,
                    'usage_frequency': entry.usage_frequency
                }
                for entry in entries
            ]
        
        elif format_type == 'tsv':
            output = "chuukese_word\tenglish_definition\tpronunciation\tpart_of_speech\tcultural_context\tdifficulty_level\n"
            for entry in entries:
                output += f"{entry.chuukese_word}\t{entry.english_definition}\t{entry.pronunciation or ''}\t{entry.part_of_speech or ''}\t{entry.cultural_context or ''}\t{entry.difficulty_level}\n"
            return output
        
        return entries

    # Database Maintenance
    def cleanup_duplicates(self):
        """Remove duplicate entries based on Chuukese word"""
        # Find duplicates
        duplicates = self.session.query(
            DictionaryEntry.chuukese_word,
            func.count(DictionaryEntry.id)
        ).group_by(DictionaryEntry.chuukese_word).having(
            func.count(DictionaryEntry.id) > 1
        ).all()
        
        removed_count = 0
        for word, count in duplicates:
            entries = self.session.query(DictionaryEntry).filter(
                DictionaryEntry.chuukese_word == word
            ).order_by(DictionaryEntry.created_at.desc()).all()
            
            # Keep the newest, remove others
            for entry in entries[1:]:
                self.session.delete(entry)
                removed_count += 1
        
        self.session.commit()
        return removed_count
    
    def update_usage_frequencies(self, usage_data):
        """Update usage frequency scores based on corpus analysis"""
        updated_count = 0
        
        for word, frequency in usage_data.items():
            entry = self.session.query(DictionaryEntry).filter(
                DictionaryEntry.chuukese_word == word
            ).first()
            
            if entry:
                entry.usage_frequency = frequency
                updated_count += 1
        
        self.session.commit()
        return updated_count
    
    def __del__(self):
        """Cleanup database connection"""
        if hasattr(self, 'session'):
            self.session.close()
```

## Usage Examples

### Basic Database Operations
```python
# Initialize database manager
db = ChuukeseDatabaseManager('sqlite:///chuukese_dictionary.db')

# Add dictionary entry
entry_id = db.add_dictionary_entry(
    chuukese_word="chomong",
    english_definition="to help, assist",
    pronunciation="tʃomoŋ",
    part_of_speech="verb",
    cultural_context="community cooperation, traditional value",
    difficulty_level="beginner"
)

# Search with accent handling
results = db.search_dictionary_entries("chomong", search_type='fuzzy')
```

### Advanced Search Operations
```python
# Search by cultural context
cultural_terms = db.get_entries_by_cultural_context("traditional")

# Find high-quality translations
quality_translations = db.get_high_quality_translations(min_quality_score=0.85)

# Get comprehensive statistics
stats = db.get_vocabulary_statistics()
print(f"Total entries: {stats['total_dictionary_entries']}")
```

### Batch Import and Export
```python
# Import from structured data
dictionary_data = [
    {
        'chuukese_word': 'ngang',
        'english_definition': 'fish',
        'part_of_speech': 'noun',
        'difficulty_level': 'beginner'
    },
    # ... more entries
]

import_results = db.import_dictionary_batch(dictionary_data)
print(f"Imported {import_results['successful']} entries")

# Export filtered data
exported_data = db.export_dictionary_data(
    format_type='json',
    filters={'part_of_speech': 'noun'}
)
```

## Best Practices

### Database Design
1. **Unicode support**: Ensure proper UTF-8 encoding for accented characters
2. **Indexing strategy**: Index frequently searched fields (words, categories)
3. **Normalization**: Balance between normalization and query performance
4. **Backup strategy**: Regular backups of linguistic data

### Search and Retrieval
1. **Accent handling**: Implement fuzzy search for accent variations
2. **Cultural context**: Index and search by cultural significance
3. **Performance optimization**: Use appropriate indexes and query optimization
4. **Flexible searching**: Support multiple search strategies (exact, partial, fuzzy)

### Data Quality
1. **Validation rules**: Implement data validation for consistency
2. **Duplicate detection**: Regular cleanup of duplicate entries
3. **Quality metrics**: Track and maintain translation quality scores
4. **Human validation**: Workflow for community review and validation

## Dependencies
- `sqlalchemy`: Database ORM and operations
- `re`: Regular expression pattern matching
- `difflib`: Fuzzy string matching
- `json`: Data serialization
- `datetime`: Timestamp management

## Validation Criteria
A successful implementation should:
- ✅ Handle Chuukese accented characters correctly in all operations
- ✅ Provide efficient search with cultural context awareness
- ✅ Support batch import/export operations
- ✅ Include comprehensive quality metrics and analytics
- ✅ Handle duplicate detection and cleanup
- ✅ Support multiple data export formats
- ✅ Provide database maintenance and optimization features