---
name: word-tracker
description: Comprehensive word counting and tracking system for authors - track word counts across documents, monitor writing progress, and generate detailed analytics for markdown-based writing projects.
---

# Overview
A comprehensive word counting and tracking system for managing writing projects, particularly designed for authors working with markdown files. This skill provides tools for tracking word counts across multiple documents, monitoring writing progress over time, and generating detailed analytics.

## Quick Start

### Minimal Working Example
```python
#!/usr/bin/env python3
import re
from pathlib import Path
from datetime import datetime

def quick_count(directory="drafts"):
    """Quick word count for all markdown files."""
    total = 0
    for md_file in Path(directory).glob("*.md"):
        text = md_file.read_text(errors='ignore')
        words = len(re.findall(r"\b\w+\b", text))
        print(f"{md_file.name}: {words:,} words")
        total += words
    print(f"\nTotal: {total:,} words")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    quick_count()
```

### Using the Provided Scripts
```bash
# Standalone script (simplest)
python scripts/word_tracker_standalone.py --drafts drafts

# Full package version (most features)
python -m scripts.wordcount_tracker.cli --drafts drafts --csv tracker.csv

# With options
python scripts/word_tracker_standalone.py --recursive --report --goal 70000
```

## When to Use This Skill
- Tracking word counts for novels, stories, or any writing project
- Monitoring daily writing progress
- Managing multiple writing projects simultaneously
- Generating word count reports and statistics
- Tracking revisions and edits over time
- Meeting word count goals and deadlines

## Core Capabilities
- Count words in individual markdown files
- Count words across multiple files in a directory
- Support for recursive directory scanning
- Handle various text encodings gracefully

### 1. Basic Word Counting
- Track word counts over time with CSV storage
- Monitor daily/weekly/monthly writing progress
- Track creation dates and update dates
- Identify new vs updated files

### 2. Progress Tracking
- Generate writing statistics and trends
- Calculate daily writing averages
- Track progress toward word count goals
- Create visual reports (when combined with data visualization tools)

### 3. Analytics & Reporting

## File Structure

```
word-tracker/
├── SKILL.md          # Main instructions (this file)
├── REFERENCE.md      # Detailed API reference
├── README.md         # Quick start guide
└── scripts/
    ├── word_tracker_standalone.py     # Single-file solution
    └── wordcount_tracker/             # Full package
        ├── __init__.py
        ├── cli.py                     # Command-line interface
        ├── scanner.py                 # File discovery
        ├── counter.py                 # Word counting
        ├── dates.py                   # Date handling
        ├── tracker.py                 # CSV management
        └── analytics.py               # Reports & statistics
```

For detailed API documentation and advanced usage, see REFERENCE.md.

## Implementation Options

### Option 1: Use the Standalone Script (Simplest)

```bash
# Basic usage
python scripts/word_tracker_standalone.py

# With options
python scripts/word_tracker_standalone.py --drafts manuscripts --recursive --report
```

**Advantages:**
- Single file, easy to deploy
- No dependencies or installation
- Perfect for quick start

### Option 2: Use the Full Package (Most Features)

```bash
# From the skill directory
python -m scripts.wordcount_tracker.cli --drafts drafts --csv tracker.csv

# With advanced features
python -m scripts.wordcount_tracker.cli --recursive --advanced --report --backup
```

**Advantages:**
- Modular design for extensibility
- Advanced analytics and reporting
- Professional structure for team projects
- Full API for integration

## Key Components

### Scanner Module
```python
def find_markdown_files(root: Path, recursive: bool = False) -> Iterable[Path]:
    """Find all markdown files in specified directory."""
    pattern = "**/*.md" if recursive else "*.md"
    return (p for p in root.glob(pattern) if p.is_file())
```

### Counter Module
```python
def count_words(text: str) -> int:
    """Count words using configurable regex patterns."""
    # Simple word boundary approach
    return len(re.findall(r"\b\w+\b", text))
    
def count_words_advanced(text: str, exclude_frontmatter: bool = True) -> int:
    """Advanced counting with frontmatter exclusion."""
    if exclude_frontmatter and text.startswith("---"):
        # Skip YAML frontmatter
        _, _, text = text.split("---", 2)
    return count_words(text)
```

### Tracker Module
```python
@dataclass
class WordCountEntry:
    filename: str
    word_count: int
    date_created: str
    date_updated: str = ""
    
def update_tracker(csv_path: Path, entries: List[WordCountEntry]) -> None:
    """Update CSV tracker with new word counts."""
    # Load existing data
    # Merge with new entries
    # Save back to CSV
```

## CSV Schema

The tracker uses this CSV format:

| Column | Type | Description |
|--------|------|-------------|
| Filename | String | Relative path to file |
| Word Count | Integer | Current word count |
| Date Created | Date | YYYY-MM-DD format |
| Date Updated | Date | YYYY-MM-DD or blank for new |

## Usage Examples

### Basic Usage
```bash
# Count words in drafts folder
python -m wordcount_tracker.cli --drafts drafts --csv word_count_tracker.csv

# Include subfolders
python -m wordcount_tracker.cli --drafts drafts --csv word_count_tracker.csv --recursive

# Specify custom paths
python -m wordcount_tracker.cli --drafts /path/to/manuscripts --csv /path/to/tracking.csv
```

### Advanced Features
```bash
# Generate weekly report
python -m wordcount_tracker.cli --report weekly

# Set word count goal
python -m wordcount_tracker.cli --goal 50000 --deadline 2024-12-31

# Track multiple projects
python -m wordcount_tracker.cli --project novel --drafts novel/drafts
python -m wordcount_tracker.cli --project stories --drafts short_stories
```

## Extension Points

### Custom Word Counting Algorithms
```python
# For screenplay format
def count_screenplay_words(text: str) -> int:
    # Custom logic for dialogue, action, etc.
    
# For academic papers
def count_academic_words(text: str) -> int:
    # Exclude citations, footnotes, etc.
```

### Front Matter Integration
```python
def extract_frontmatter_date(text: str) -> Optional[str]:
    """Extract creation date from YAML frontmatter."""
    if text.startswith("---"):
        frontmatter = yaml.safe_load(text.split("---")[1])
        return frontmatter.get("created", None)
```

### Multi-Format Support
```python
SUPPORTED_FORMATS = {
    ".md": count_markdown,
    ".txt": count_plaintext,
    ".docx": count_docx,  # Requires python-docx
    ".html": count_html,  # Strip tags first
}
```

## Best Practices

### 1. Git Integration
- Keep CSV tracker in version control
- Use consistent date formats for clean diffs
- Sort entries alphabetically for stable diffs

### 2. Performance Optimization
- Cache file reads for large projects
- Use generators for memory efficiency
- Implement incremental updates (only scan changed files)

### 3. Data Integrity
- Always backup before major updates
- Validate CSV structure before operations
- Handle encoding errors gracefully

### 4. Project Organization
```
project/
  drafts/           # Active writing
    chapter_01.md
    chapter_02.md
  archive/          # Completed/old versions
  reports/          # Generated analytics
  word_count_tracker.csv
  config.yaml       # Project settings
```

## Configuration Options

Create a `wordtracker.yaml` for project-specific settings:

```yaml
# wordtracker.yaml
drafts_dir: drafts
csv_path: word_count_tracker.csv
recursive: true
exclude_patterns:
  - "*.backup.md"
  - "notes/*"
word_count:
  method: standard  # or 'academic', 'screenplay'
  exclude_frontmatter: true
  exclude_code_blocks: false
reporting:
  weekly_goal: 5000
  project_goal: 70000
  deadline: 2024-12-31
```

## Troubleshooting

### Common Issues

1. **Encoding Errors**
   - Solution: Use `errors='ignore'` or 'replace' when reading files
   
2. **Date Detection Issues**
   - macOS: Uses st_birthtime (accurate)
   - Windows: Uses st_ctime (creation time)
   - Linux: Falls back to st_ctime (change time)
   
3. **Large File Performance**
   - Implement chunked reading for files > 10MB
   - Use multiprocessing for directories with 1000+ files

## Integration with Writing Tools

### Your First Draft (YFD)
- Export word counts to YFD-compatible format
- Track chapter-by-chapter progress
- Monitor revision statistics

### Pro Writing Aid
- Generate reports compatible with PWA imports
- Track editing progress post-PWA analysis

### Scrivener
- Parse Scrivener project files (with caution)
- Export statistics to Scrivener-compatible formats

## Sample Analytics Output

```
=== Writing Progress Report ===
Period: 2024-10-14 to 2024-10-21

Total Words Written: 12,450
Daily Average: 1,779 words
Best Day: Monday (2,341 words)

Projects:
- Novel: 8,200 words (5 chapters updated)
- Short Stories: 4,250 words (2 new stories)

Progress to Goal: 45,230 / 80,000 (56.5%)
Projected Completion: December 5, 2024
```

## Error Handling

```python
def safe_word_count(path: Path) -> Optional[int]:
    """Safely count words with comprehensive error handling."""
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
        return count_words(text)
    except PermissionError:
        print(f"Permission denied: {path}")
    except IsADirectoryError:
        print(f"Is a directory: {path}")
    except Exception as e:
        print(f"Unexpected error with {path}: {e}")
    return None
```

## Future Enhancements

1. **Real-time Monitoring**
   - File system watchers for automatic updates
   - Desktop notifications for goal achievements

2. **Cloud Sync**
   - Backup tracking data to cloud services
   - Multi-device synchronization

3. **AI Integration**
   - Writing pace predictions
   - Automated progress reports
   - Goal recommendations based on history

4. **Visualization**
   - Generate charts and graphs
   - Create writing calendars
   - Export to dashboard tools

## Quick Start Code

Here's a minimal working example to get started immediately:

```python
#!/usr/bin/env python3
import re
from pathlib import Path
from datetime import datetime

def quick_count(directory="drafts"):
    \"\"\"Quick word count for all markdown files.\"\"\"
    total = 0
    for md_file in Path(directory).glob("*.md"):
        text = md_file.read_text(errors='ignore')
        words = len(re.findall(r"\b\w+\b", text))
        print(f"{md_file.name}: {words:,} words")
        total += words
    print(f"\nTotal: {total:,} words")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    quick_count()
```

## Support for Authors

This skill is specifically designed with fiction authors in mind:

- Handles manuscript formatting conventions
- Tracks revision history for editorial process
- Supports multi-book series tracking
- Compatible with industry-standard word count methods
- Respects creative workflow (non-intrusive tracking)

## Version History

- v1.0: Basic word counting and CSV tracking
- v1.1: Added recursive scanning and date tracking
- v1.2: Frontmatter support and advanced analytics
- v1.3: Multi-project support and configuration files
- v2.0: Package structure with modular components

---

This skill provides a professional-grade word tracking solution that scales from simple single-file counts to complex multi-project manuscript management systems.
