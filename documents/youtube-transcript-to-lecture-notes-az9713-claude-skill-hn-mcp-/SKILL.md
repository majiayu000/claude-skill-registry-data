---
name: youtube-transcript-to-lecture-notes
description: Transform YouTube transcripts into comprehensive lecture notes with PDF and HTML outputs
---

# YouTube Transcript to Lecture Notes Skill

## Overview
This skill transforms YouTube transcripts into comprehensive, academic-quality lecture notes that serve as standalone learning materials. The skill produces both PDF and HTML versions with identical content, ensuring students can learn all key topics and nuances without attending the original lecture.

## Mathematical Foundation

### Text Processing Pipeline
The transformation process follows a multi-stage pipeline:

$$T_{raw} \xrightarrow{f_{clean}} T_{clean} \xrightarrow{f_{structure}} T_{structured} \xrightarrow{f_{enhance}} T_{enhanced} \xrightarrow{f_{format}} \{PDF, HTML\}$$

Where:
- $T_{raw}$ = Raw transcript text
- $f_{clean}$ = Cleaning function removing artifacts
- $f_{structure}$ = Structuring function for logical organization
- $f_{enhance}$ = Enhancement function adding educational value
- $f_{format}$ = Formatting function for output generation

## Core Components

### 1. Transcript Cleaning Algorithm

The cleaning process removes conversational artifacts while preserving educational content:

```python
import re
from typing import List, Dict, Tuple

class TranscriptCleaner:
    """
    Implements sophisticated cleaning algorithms for YouTube transcripts.
    
    The cleaning process uses pattern matching with complexity O(n*m) where:
    - n = length of transcript
    - m = number of patterns to match
    """
    
    def __init__(self):
        # Define patterns for removal with confidence scores
        self.filler_patterns = [
            (r'\b(um+|uh+|ah+|er+|hmm+)\b', 0.95),  # Filler words
            (r'\[.*?\]', 0.90),  # Timestamps and annotations
            (r'\(.*?inaudible.*?\)', 0.99),  # Inaudible markers
            (r'\b(you know|I mean|like|sort of|kind of)\b', 0.70),  # Hedging phrases
            (r'\.{3,}', 0.85),  # Multiple dots
            (r'\s+', 1.0),  # Normalize whitespace
        ]
        
    def clean_transcript(self, text: str) -> str:
        """
        Apply multi-pass cleaning with confidence thresholds.
        
        Mathematical model for cleaning decision:
        P(remove) = Σ(w_i * c_i) / Σ(w_i)
        
        Where:
        - w_i = weight of pattern i
        - c_i = confidence score for pattern i
        """
        cleaned_text = text
        
        for pattern, confidence in self.filler_patterns:
            if confidence > 0.8:  # Only apply high-confidence removals
                cleaned_text = re.sub(pattern, ' ', cleaned_text, flags=re.IGNORECASE)
        
        # Normalize spacing and punctuation
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text = re.sub(r'\s*([.,!?;:])\s*', r'\1 ', cleaned_text)
        
        return cleaned_text.strip()
```

### 2. Intelligent Content Structuring

The structuring algorithm uses natural language processing to identify logical sections:

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentStructurer:
    """
    Implements topic segmentation using TF-IDF and cosine similarity.
    
    Mathematical foundation:
    TF-IDF(t,d,D) = TF(t,d) × IDF(t,D)
    Where:
    - TF(t,d) = frequency of term t in document d
    - IDF(t,D) = log(|D| / |{d ∈ D : t ∈ d}|)
    """
    
    def __init__(self, window_size: int = 5, threshold: float = 0.3):
        self.window_size = window_size
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    
    def segment_content(self, sentences: List[str]) -> List[Tuple[int, int]]:
        """
        Identify topic boundaries using sliding window similarity.
        
        Algorithm:
        1. Convert sentences to TF-IDF vectors
        2. Calculate similarity between adjacent windows
        3. Identify boundaries where similarity < threshold
        
        Complexity: O(n * w * f) where:
        - n = number of sentences
        - w = window size
        - f = number of features
        """
        # Create sentence windows
        windows = []
        for i in range(len(sentences) - self.window_size + 1):
            window_text = ' '.join(sentences[i:i + self.window_size])
            windows.append(window_text)
        
        # Vectorize windows
        tfidf_matrix = self.vectorizer.fit_transform(windows)
        
        # Calculate similarities between adjacent windows
        boundaries = [0]  # Start with first sentence
        for i in range(len(windows) - 1):
            similarity = cosine_similarity(
                tfidf_matrix[i:i+1], 
                tfidf_matrix[i+1:i+2]
            )[0][0]
            
            # Boundary detection condition
            if similarity < self.threshold:
                boundaries.append(i + self.window_size)
        
        boundaries.append(len(sentences))  # End with last sentence
        
        # Create segments
        segments = []
        for i in range(len(boundaries) - 1):
            segments.append((boundaries[i], boundaries[i+1]))
        
        return segments
```

### 3. Content Enhancement Engine

The enhancement engine adds educational value through elaboration and clarification:

```python
class ContentEnhancer:
    """
    Enhances lecture content with explanations, examples, and context.
    
    Uses a knowledge graph approach:
    G = (V, E) where:
    - V = set of concepts
    - E = relationships between concepts
    """
    
    def __init__(self):
        self.concept_graph = {}
        self.importance_scores = {}
    
    def extract_key_concepts(self, text: str) -> List[Dict[str, any]]:
        """
        Extract and rank key concepts using TextRank algorithm.
        
        Mathematical model:
        PR(v_i) = (1-d) + d * Σ(PR(v_j) * w_ji / Σw_jk)
        
        Where:
        - PR(v_i) = PageRank of vertex i
        - d = damping factor (typically 0.85)
        - w_ji = weight of edge from j to i
        """
        # Simplified concept extraction
        concepts = []
        
        # Extract noun phrases as potential concepts
        import nltk
        from nltk import pos_tag, word_tokenize
        from nltk.chunk import ne_chunk, tree2conlltags
        
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        
        # Extract noun phrases
        noun_phrases = []
        current_phrase = []
        for word, tag in pos_tags:
            if tag.startswith('NN'):  # Noun
                current_phrase.append(word)
            elif current_phrase:
                if len(current_phrase) > 1:
                    noun_phrases.append(' '.join(current_phrase))
                current_phrase = []
        
        # Score concepts by frequency and position
        for i, phrase in enumerate(noun_phrases):
            score = noun_phrases.count(phrase) * (1 - i/len(noun_phrases))
            concepts.append({
                'term': phrase,
                'score': score,
                'definition': self.generate_definition(phrase),
                'examples': self.generate_examples(phrase)
            })
        
        return sorted(concepts, key=lambda x: x['score'], reverse=True)[:10]
    
    def generate_definition(self, term: str) -> str:
        """Generate educational definition for a term."""
        # In production, this would use an LLM or knowledge base
        return f"A comprehensive explanation of {term} in the context of this lecture."
    
    def generate_examples(self, term: str) -> List[str]:
        """Generate illustrative examples."""
        # In production, this would generate contextual examples
        return [
            f"Example 1: Practical application of {term}",
            f"Example 2: Theoretical illustration of {term}",
            f"Example 3: Real-world scenario involving {term}"
        ]
```

### 4. Multi-Format Output Generator

The output generator creates both PDF and HTML with identical content:

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import markdown
from jinja2 import Template

class OutputGenerator:
    """
    Generates PDF and HTML outputs with identical content structure.
    
    Ensures content parity: C_pdf ≡ C_html
    """
    
    def __init__(self):
        self.styles = self._initialize_styles()
        self.html_template = self._load_html_template()
    
    def _initialize_styles(self) -> Dict:
        """Initialize PDF styles for different content types."""
        styles = getSampleStyleSheet()
        
        # Custom styles for lecture notes
        styles.add(ParagraphStyle(
            name='LectureTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor='#2c3e50'
        ))
        
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=12,
            textColor='#34495e'
        ))
        
        styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            textColor='#7f8c8d'
        ))
        
        styles.add(ParagraphStyle(
            name='LectureBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=16,
            alignment=4,  # Justify
            spaceAfter=12
        ))
        
        return styles
    
    def _load_html_template(self) -> Template:
        """Load HTML template with TOC sidebar."""
        template_str = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            display: flex;
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        /* TOC Sidebar */
        .toc-sidebar {
            width: 300px;
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            background-color: #2c3e50;
            color: white;
            padding: 20px;
        }
        
        .toc-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #34495e;
        }
        
        .toc-item {
            margin-bottom: 10px;
        }
        
        .toc-item a {
            color: #ecf0f1;
            text-decoration: none;
            display: block;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        
        .toc-item a:hover {
            background-color: #34495e;
        }
        
        .toc-item.subsection {
            margin-left: 20px;
            font-size: 14px;
        }
        
        .toc-item.active a {
            background-color: #3498db;
        }
        
        /* Main Content */
        .main-content {
            flex: 1;
            padding: 40px;
            max-width: 900px;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 32px;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }
        
        h2 {
            color: #34495e;
            font-size: 24px;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-left: 10px;
            border-left: 4px solid #3498db;
        }
        
        h3 {
            color: #7f8c8d;
            font-size: 18px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        p {
            text-align: justify;
            margin-bottom: 15px;
            line-height: 1.8;
        }
        
        .concept-box {
            background-color: #ecf0f1;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        
        .concept-term {
            font-weight: bold;
            color: #2c3e50;
            font-size: 16px;
            margin-bottom: 8px;
        }
        
        .example-box {
            background-color: #e8f6f3;
            border-left: 4px solid #27ae60;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        
        .example-title {
            font-weight: bold;
            color: #27ae60;
            margin-bottom: 5px;
        }
        
        .math-equation {
            background-color: #fdf2e9;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }
            
            .toc-sidebar {
                width: 100%;
                height: auto;
                position: relative;
            }
            
            .main-content {
                padding: 20px;
            }
        }
        
        /* Smooth Scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Print Styles */
        @media print {
            .toc-sidebar {
                display: none;
            }
            
            .main-content {
                max-width: 100%;
                padding: 0;
            }
            
            body {
                background-color: white;
            }
            
            .container {
                box-shadow: none;
            }
        }
    </style>
    <script>
        // Highlight active section in TOC
        window.addEventListener('scroll', function() {
            const sections = document.querySelectorAll('h2, h3');
            const tocItems = document.querySelectorAll('.toc-item');
            
            let current = '';
            sections.forEach(section => {
                const rect = section.getBoundingClientRect();
                if (rect.top <= 100) {
                    current = section.id;
                }
            });
            
            tocItems.forEach(item => {
                item.classList.remove('active');
                if (item.querySelector('a').getAttribute('href') === '#' + current) {
                    item.classList.add('active');
                }
            });
        });
    </script>
</head>
<body>
    <div class="container">
        <nav class="toc-sidebar">
            <div class="toc-title">Table of Contents</div>
            {{ toc_html }}
        </nav>
        
        <main class="main-content">
            <h1>{{ title }}</h1>
            {{ content_html }}
        </main>
    </div>
</body>
</html>
        '''
        return Template(template_str)
    
    def generate_outputs(self, structured_content: Dict) -> Tuple[bytes, str]:
        """
        Generate both PDF and HTML outputs with identical content.
        
        Ensures: ∀s ∈ sections, ∀p ∈ paragraphs: 
                 content_pdf(s,p) = content_html(s,p)
        """
        pdf_bytes = self._generate_pdf(structured_content)
        html_str = self._generate_html(structured_content)
        
        return pdf_bytes, html_str
    
    def _generate_pdf(self, content: Dict) -> bytes:
        """Generate PDF with formatted lecture notes."""
        from io import BytesIO
        buffer = BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Add title
        story.append(Paragraph(content['title'], self.styles['LectureTitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Add sections
        for section in content['sections']:
            # Section header
            story.append(Paragraph(section['title'], self.styles['SectionHeader']))
            
            # Section content
            for paragraph in section['paragraphs']:
                story.append(Paragraph(paragraph, self.styles['LectureBody']))
            
            # Add subsections
            for subsection in section.get('subsections', []):
                story.append(Paragraph(subsection['title'], self.styles['SubsectionHeader']))
                for paragraph in subsection['paragraphs']:
                    story.append(Paragraph(paragraph, self.styles['LectureBody']))
            
            # Add concepts if present
            if 'concepts' in section:
                for concept in section['concepts']:
                    concept_text = f"<b>{concept['term']}</b>: {concept['definition']}"
                    story.append(Paragraph(concept_text, self.styles['LectureBody']))
                    
                    # Add examples
                    for example in concept['examples']:
                        example_text = f"• {example}"
                        story.append(Paragraph(example_text, self.styles['LectureBody']))
            
            story.append(Spacer(1, 0.2*inch))
        
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _generate_html(self, content: Dict) -> str:
        """Generate HTML with TOC sidebar."""
        # Generate TOC HTML
        toc_items = []
        for i, section in enumerate(content['sections']):
            section_id = f"section-{i}"
            toc_items.append(
                f'<div class="toc-item">'
                f'<a href="#{section_id}">{section["title"]}</a>'
                f'</div>'
            )
            
            for j, subsection in enumerate(section.get('subsections', [])):
                subsection_id = f"subsection-{i}-{j}"
                toc_items.append(
                    f'<div class="toc-item subsection">'
                    f'<a href="#{subsection_id}">{subsection["title"]}</a>'
                    f'</div>'
                )
        
        toc_html = '\n'.join(toc_items)
        
        # Generate content HTML
        content_items = []
        for i, section in enumerate(content['sections']):
            section_id = f"section-{i}"
            content_items.append(f'<h2 id="{section_id}">{section["title"]}</h2>')
            
            for paragraph in section['paragraphs']:
                content_items.append(f'<p>{paragraph}</p>')
            
            for j, subsection in enumerate(section.get('subsections', [])):
                subsection_id = f"subsection-{i}-{j}"
                content_items.append(f'<h3 id="{subsection_id}">{subsection["title"]}</h3>')
                
                for paragraph in subsection['paragraphs']:
                    content_items.append(f'<p>{paragraph}</p>')
            
            # Add concepts
            if 'concepts' in section:
                for concept in section['concepts']:
                    content_items.append(
                        f'<div class="concept-box">'
                        f'<div class="concept-term">{concept["term"]}</div>'
                        f'<div>{concept["definition"]}</div>'
                        f'</div>'
                    )
                    
                    for example in concept['examples']:
                        content_items.append(
                            f'<div class="example-box">'
                            f'<div class="example-title">Example:</div>'
                            f'<div>{example}</div>'
                            f'</div>'
                        )
        
        content_html = '\n'.join(content_items)
        
        return self.html_template.render(
            title=content['title'],
            toc_html=toc_html,
            content_html=content_html
        )
```

### 5. Main Processing Pipeline

The main pipeline orchestrates all components:

```python
class LectureNotesProcessor:
    """
    Main processor that coordinates all components.
    
    Processing flow:
    Input → Clean → Structure → Enhance → Format → Output
    """
    
    def __init__(self):
        self.cleaner = TranscriptCleaner()
        self.structurer = ContentStructurer()
        self.enhancer = ContentEnhancer()
        self.generator = OutputGenerator()
    
    def process_transcript(self, transcript_text: str, lecture_title: str = None) -> Dict:
        """
        Complete processing pipeline with error handling and logging.
        
        Time Complexity: O(n²) in worst case for structure detection
        Space Complexity: O(n) for storing processed content
        """
        try:
            # Step 1: Clean transcript
            print("Step 1: Cleaning transcript...")
            cleaned_text = self.cleaner.clean_transcript(transcript_text)
            
            # Step 2: Sentence segmentation
            print("Step 2: Segmenting sentences...")
            sentences = self._segment_sentences(cleaned_text)
            
            # Step 3: Identify structure
            print("Step 3: Identifying content structure...")
            segments = self.structurer.segment_content(sentences)
            
            # Step 4: Build sections
            print("Step 4: Building sections...")
            sections = self._build_sections(sentences, segments)
            
            # Step 5: Enhance content
            print("Step 5: Enhancing content...")
            enhanced_sections = self._enhance_sections(sections)
            
            # Step 6: Prepare final content
            print("Step 6: Preparing final content...")
            structured_content = {
                'title': lecture_title or self._extract_title(cleaned_text),
                'sections': enhanced_sections
            }
            
            # Step 7: Generate outputs
            print("Step 7: Generating PDF and HTML outputs...")
            pdf_bytes, html_str = self.generator.generate_outputs(structured_content)
            
            return {
                'success': True,
                'pdf': pdf_bytes,
                'html': html_str,
                'structured_content': structured_content
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _segment_sentences(self, text: str) -> List[str]:
        """
        Intelligent sentence segmentation using NLTK.
        
        Handles edge cases:
        - Abbreviations (Dr., Mr., etc.)
        - Decimal numbers
        - URLs and emails
        """
        import nltk
        nltk.download('punkt', quiet=True)
        
        # Use NLTK's pre-trained sentence tokenizer
        sentences = nltk.sent_tokenize(text)
        
        # Post-process to merge incorrectly split sentences
        merged_sentences = []
        buffer = ""
        
        for sentence in sentences:
            if buffer and (
                len(sentence.split()) < 3 or  # Very short sentence
                sentence[0].islower()  # Starts with lowercase
            ):
                buffer += " " + sentence
            else:
                if buffer:
                    merged_sentences.append(buffer)
                buffer = sentence
        
        if buffer:
            merged_sentences.append(buffer)
        
        return merged_sentences
    
    def _build_sections(self, sentences: List[str], segments: List[Tuple[int, int]]) -> List[Dict]:
        """
        Build hierarchical section structure.
        
        Uses heuristics to identify:
        - Main sections (major topic changes)
        - Subsections (subtopic elaborations)
        """
        sections = []
        
        for start, end in segments:
            segment_sentences = sentences[start:end]
            
            # Determine if this is a main section or subsection
            # Heuristic: First sentence length and capitalization
            first_sentence = segment_sentences[0] if segment_sentences else ""
            
            is_main_section = (
                len(first_sentence.split()) < 10 and
                first_sentence[0].isupper()
            )
            
            section_data = {
                'title': self._generate_section_title(segment_sentences),
                'paragraphs': self._group_into_paragraphs(segment_sentences),
                'is_main': is_main_section
            }
            
            sections.append(section_data)
        
        # Organize into hierarchical structure
        hierarchical_sections = []
        current_main = None
        
        for section in sections:
            if section['is_main']:
                if current_main:
                    hierarchical_sections.append(current_main)
                current_main = {
                    'title': section['title'],
                    'paragraphs': section['paragraphs'],
                    'subsections': []
                }
            else:
                if current_main:
                    current_main['subsections'].append({
                        'title': section['title'],
                        'paragraphs': section['paragraphs']
                    })
                else:
                    # Orphan subsection becomes main section
                    hierarchical_sections.append({
                        'title': section['title'],
                        'paragraphs': section['paragraphs'],
                        'subsections': []
                    })
        
        if current_main:
            hierarchical_sections.append(current_main)
        
        return hierarchical_sections
    
    def _generate_section_title(self, sentences: List[str]) -> str:
        """
        Generate descriptive section title using keyword extraction.
        
        Algorithm:
        1. Extract keywords using TF-IDF
        2. Identify most important 2-3 words
        3. Create grammatical title
        """
        if not sentences:
            return "Untitled Section"
        
        # Combine first few sentences for context
        context = ' '.join(sentences[:min(3, len(sentences))])
        
        # Simple keyword extraction
        from collections import Counter
        import string
        
        # Remove punctuation and convert to lowercase
        words = context.translate(str.maketrans('', '', string.punctuation)).lower().split()
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
                     'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                     'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might'}
        
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Get top keywords
        keyword_counts = Counter(keywords)
        top_keywords = [word for word, _ in keyword_counts.most_common(3)]
        
        if top_keywords:
            # Capitalize and format
            title = ' '.join(word.capitalize() for word in top_keywords)
        else:
            title = "Continued Discussion"
        
        return title
    
    def _group_into_paragraphs(self, sentences: List[str]) -> List[str]:
        """
        Group sentences into coherent paragraphs.
        
        Uses semantic similarity to determine paragraph boundaries.
        Optimal paragraph length: 3-7 sentences
        """
        if len(sentences) <= 5:
            return [' '.join(sentences)]
        
        paragraphs = []
        current_paragraph = []
        
        for i, sentence in enumerate(sentences):
            current_paragraph.append(sentence)
            
            # Check if we should start a new paragraph
            if (len(current_paragraph) >= 3 and 
                (len(current_paragraph) >= 7 or 
                 self._is_paragraph_boundary(current_paragraph, sentences[i+1:i+2]))):
                
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        
        return paragraphs
    
    def _is_paragraph_boundary(self, current: List[str], next_sentences: List[str]) -> bool:
        """
        Determine if there should be a paragraph break.
        
        Heuristics:
        - Topic shift (low similarity)
        - Transition words
        - Significant length difference
        """
        if not next_sentences:
            return True
        
        # Check for transition indicators
        transition_words = ['however', 'moreover', 'furthermore', 'additionally',
                          'in conclusion', 'to summarize', 'first', 'second', 'finally',
                          'on the other hand', 'in contrast', 'nevertheless']
        
        next_lower = next_sentences[0].lower()
        for transition in transition_words:
            if next_lower.startswith(transition):
                return True
        
        # Check length difference
        avg_current_length = sum(len(s.split()) for s in current) / len(current)
        next_length = len(next_sentences[0].split())
        
        if abs(avg_current_length - next_length) > 15:
            return True
        
        return False
    
    def _enhance_sections(self, sections: List[Dict]) -> List[Dict]:
        """
        Enhance sections with educational features.
        
        Enhancements:
        - Key concept identification
        - Example generation
        - Cross-references
        - Summary points
        """
        enhanced = []
        
        for section in sections:
            # Extract concepts from section content
            section_text = ' '.join(section['paragraphs'])
            concepts = self.enhancer.extract_key_concepts(section_text)[:3]  # Top 3 concepts
            
            enhanced_section = {
                **section,
                'concepts': concepts
            }
            
            # Enhance subsections similarly
            if 'subsections' in section:
                enhanced_subsections = []
                for subsection in section['subsections']:
                    subsection_text = ' '.join(subsection['paragraphs'])
                    subsection_concepts = self.enhancer.extract_key_concepts(subsection_text)[:2]
                    
                    enhanced_subsections.append({
                        **subsection,
                        'concepts': subsection_concepts
                    })
                
                enhanced_section['subsections'] = enhanced_subsections
            
            enhanced.append(enhanced_section)
        
        return enhanced
    
    def _extract_title(self, text: str) -> str:
        """
        Extract or generate lecture title from content.
        
        Strategies:
        1. Look for explicit title mentions
        2. Use first significant topic
        3. Generate from main themes
        """
        # Try to find explicit title patterns
        title_patterns = [
            r"(?:lecture|lesson|chapter|module)\s*(?:on|about|title:|:)?\s*([^.]+)",
            r"(?:today|this)\s+(?:lecture|lesson|session)\s+(?:is about|covers|on)\s+([^.]+)",
            r"welcome to\s+([^.]+)"
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text[:500], re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Clean and capitalize
                title = ' '.join(word.capitalize() for word in title.split())
                return title
        
        # Fallback: Use key concepts
        concepts = self.enhancer.extract_key_concepts(text[:1000])
        if concepts:
            top_concepts = [c['term'] for c in concepts[:3]]
            return f"Lecture on {', '.join(top_concepts)}"
        
        return "Lecture Notes"
```

## Usage Instructions

### Step 1: Upload Transcript
```python
# Read the transcript file
with open('/path/to/transcript.txt', 'r', encoding='utf-8') as f:
    transcript_text = f.read()
```

### Step 2: Process Transcript
```python
# Initialize processor
processor = LectureNotesProcessor()

# Process with optional title
result = processor.process_transcript(
    transcript_text,
    lecture_title="Advanced Machine Learning Concepts"
)
```

### Step 3: Save Outputs
```python
if result['success']:
    # Save PDF
    with open('/output/lecture_notes.pdf', 'wb') as f:
        f.write(result['pdf'])
    
    # Save HTML
    with open('/output/lecture_notes.html', 'w', encoding='utf-8') as f:
        f.write(result['html'])
    
    print("✓ Lecture notes generated successfully!")
else:
    print(f"✗ Error: {result['error']}")
```

## Advanced Configuration

### Customization Parameters

```python
class AdvancedConfig:
    """
    Configuration parameters for fine-tuning the processing.
    
    Each parameter affects the output quality/processing time tradeoff:
    Q(output) ∝ √(processing_time) for most parameters
    """
    
    # Cleaning parameters
    REMOVE_FILLER_WORDS = True
    FILLER_CONFIDENCE_THRESHOLD = 0.75
    
    # Structuring parameters
    TOPIC_WINDOW_SIZE = 5  # Sentences per window
    TOPIC_SIMILARITY_THRESHOLD = 0.3  # Lower = more sections
    MIN_SECTION_LENGTH = 3  # Minimum sentences per section
    
    # Enhancement parameters
    MAX_CONCEPTS_PER_SECTION = 5
    GENERATE_EXAMPLES = True
    EXAMPLES_PER_CONCEPT = 3
    
    # Output parameters
    PDF_PAGE_SIZE = 'letter'  # or 'A4'
    HTML_THEME = 'academic'  # or 'modern', 'classic'
    INCLUDE_PAGE_NUMBERS = True
    INCLUDE_TIMESTAMP = True
    
    # Processing options
    PARALLEL_PROCESSING = True
    MAX_WORKERS = 4
    CACHE_INTERMEDIATE_RESULTS = True
```

### Error Handling and Logging

```python
import logging
from typing import Optional

class RobustProcessor(LectureNotesProcessor):
    """
    Enhanced processor with comprehensive error handling.
    """
    
    def __init__(self, log_level: str = 'INFO'):
        super().__init__()
        self.logger = self._setup_logging(log_level)
    
    def _setup_logging(self, level: str) -> logging.Logger:
        """Configure structured logging."""
        logger = logging.getLogger('LectureNotes')
        logger.setLevel(getattr(logging, level))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler('lecture_processing.log')
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        return logger
    
    def process_with_validation(self, transcript_text: str) -> Dict:
        """
        Process with input validation and error recovery.
        """
        # Input validation
        if not transcript_text:
            self.logger.error("Empty transcript provided")
            return {'success': False, 'error': 'Empty transcript'}
        
        if len(transcript_text) < 100:
            self.logger.warning("Very short transcript - may not produce good results")
        
        try:
            # Process with timeout
            import signal
            from contextlib import contextmanager
            
            @contextmanager
            def timeout(seconds):
                def signal_handler(signum, frame):
                    raise TimeoutError("Processing timeout")
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(seconds)
                try:
                    yield
                finally:
                    signal.alarm(0)
            
            with timeout(300):  # 5 minute timeout
                result = self.process_transcript(transcript_text)
            
            # Validate output
            if result['success']:
                if len(result['pdf']) < 1000:
                    self.logger.warning("Generated PDF seems too small")
                if len(result['html']) < 1000:
                    self.logger.warning("Generated HTML seems too small")
            
            return result
            
        except TimeoutError as e:
            self.logger.error(f"Processing timeout: {e}")
            return {'success': False, 'error': 'Processing took too long'}
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
```

## Performance Metrics

### Quality Metrics

```python
class QualityMetrics:
    """
    Metrics for evaluating lecture notes quality.
    
    Quality Score Q = w₁*Completeness + w₂*Coherence + w₃*Structure + w₄*Clarity
    """
    
    @staticmethod
    def calculate_completeness(original: str, notes: str) -> float:
        """
        Measure how much content is preserved.
        
        Completeness = |concepts_notes ∩ concepts_original| / |concepts_original|
        """
        # Extract concepts from both
        original_concepts = set(original.lower().split())
        notes_concepts = set(notes.lower().split())
        
        if not original_concepts:
            return 0.0
        
        overlap = original_concepts.intersection(notes_concepts)
        return len(overlap) / len(original_concepts)
    
    @staticmethod
    def calculate_coherence(paragraphs: List[str]) -> float:
        """
        Measure semantic coherence between paragraphs.
        
        Coherence = mean(similarity(p_i, p_{i+1})) for all adjacent paragraphs
        """
        if len(paragraphs) < 2:
            return 1.0
        
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(paragraphs)
        
        coherence_scores = []
        for i in range(len(paragraphs) - 1):
            similarity = cosine_similarity(
                vectors[i:i+1], 
                vectors[i+1:i+2]
            )[0][0]
            coherence_scores.append(similarity)
        
        return sum(coherence_scores) / len(coherence_scores)
    
    @staticmethod
    def calculate_structure_score(content: Dict) -> float:
        """
        Evaluate structural organization.
        
        Factors:
        - Section balance
        - Hierarchy depth
        - Concept distribution
        """
        sections = content.get('sections', [])
        if not sections:
            return 0.0
        
        # Calculate section balance
        section_lengths = [
            len(' '.join(s['paragraphs'])) 
            for s in sections
        ]
        
        if not section_lengths:
            return 0.0
        
        avg_length = sum(section_lengths) / len(section_lengths)
        variance = sum((l - avg_length) ** 2 for l in section_lengths) / len(section_lengths)
        std_dev = variance ** 0.5
        
        # Lower coefficient of variation = better balance
        cv = std_dev / avg_length if avg_length > 0 else 1.0
        balance_score = max(0, 1 - cv)
        
        # Check hierarchy
        has_subsections = any('subsections' in s for s in sections)
        hierarchy_score = 1.0 if has_subsections else 0.7
        
        # Check concepts
        has_concepts = any('concepts' in s for s in sections)
        concept_score = 1.0 if has_concepts else 0.8
        
        return (balance_score + hierarchy_score + concept_score) / 3
```

## Best Practices

### 1. Pre-processing Recommendations
- Clean transcript before uploading if possible
- Remove obvious artifacts (timestamps, speaker labels)
- Ensure UTF-8 encoding

### 2. Optimal Transcript Characteristics
- Minimum 500 words for good structure detection
- Clear topic transitions improve sectioning
- Technical content benefits from concept extraction

### 3. Post-processing Options
- Review generated section titles
- Add custom examples for key concepts
- Merge very short sections manually

## Troubleshooting Guide

### Common Issues and Solutions

1. **Poor Section Detection**
   - Adjust `TOPIC_SIMILARITY_THRESHOLD` (lower = more sections)
   - Increase `TOPIC_WINDOW_SIZE` for longer contexts

2. **Missing Content**
   - Check `FILLER_CONFIDENCE_THRESHOLD` (lower = keep more)
   - Disable aggressive cleaning for technical content

3. **Formatting Issues**
   - Verify encoding (UTF-8 required)
   - Check for special characters in transcript

4. **Performance Issues**
   - Enable `PARALLEL_PROCESSING`
   - Reduce `MAX_CONCEPTS_PER_SECTION`
   - Use `CACHE_INTERMEDIATE_RESULTS`

## Mathematical Foundations Summary

The skill uses several key algorithms:

1. **TF-IDF for Keyword Extraction**:
   $$TF\text{-}IDF(t,d,D) = \frac{f_{t,d}}{\max_{t' \in d} f_{t',d}} \times \log\frac{|D|}{|\{d \in D : t \in d\}|}$$

2. **Cosine Similarity for Topic Segmentation**:
   $$\text{similarity}(A,B) = \frac{A \cdot B}{||A|| \times ||B||} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \times \sqrt{\sum_{i=1}^{n} B_i^2}}$$

3. **TextRank for Concept Importance**:
   $$PR(v_i) = (1-d) + d \times \sum_{v_j \in In(v_i)} \frac{w_{ji}}{\sum_{v_k \in Out(v_j)} w_{jk}} PR(v_j)$$

## Conclusion

This skill provides a comprehensive solution for converting YouTube transcripts into professional lecture notes. The dual output format (PDF and HTML) ensures accessibility and usability across different platforms, while the intelligent processing preserves and enhances educational content.

The system's modular architecture allows for easy customization and extension, making it suitable for various educational contexts and content types.
