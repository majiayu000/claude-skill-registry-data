---
name: skill-markdown-quiz-exporter-tool
description: Export quiz markdown to Anki, Flashcard Hero, HTML
---

# When to use
- Export quiz markdown to flashcard formats (Anki, Flashcard Hero)
- Generate interactive HTML quiz pages
- Convert study materials to multiple formats

# markdown-quiz-exporter-tool Skill

## Purpose

The `markdown-quiz-exporter-tool` is a CLI tool that exports quiz markdown files to multiple formats including Anki CSV, Flashcard Hero TSV, and interactive HTML quiz pages. It supports single-choice and multiple-choice questions with explanations.

## When to Use This Skill

**Use this skill when:**
- Converting quiz markdown to flashcard applications (Anki, Flashcard Hero)
- Generating self-contained HTML quiz pages with interactive features
- Exporting study materials to different formats for students
- Creating quiz applications with dark/light mode support
- Building responsive mobile-friendly quiz interfaces

**Do NOT use this skill for:**
- Creating the original quiz markdown content (use a text editor)
- Importing flashcards back to markdown format
- Modifying existing quiz content (edit the markdown directly)

## CLI Tool: markdown-quiz-exporter-tool

A command-line utility for exporting quiz markdown files to multiple formats with comprehensive validation and error handling.

### Installation

```bash
# Clone repository
git clone https://github.com/dnvriend/markdown-quiz-exporter-tool.git
cd markdown-quiz-exporter-tool

# Install with uv
uv tool install .

# Verify installation
markdown-quiz-exporter-tool --version
```

### Prerequisites

- Python 3.14+
- uv package manager
- Quiz markdown files in the correct format

### Quick Start

```bash
# Export to Flashcard Hero
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv

# Export to Anki (quiz format)
markdown-quiz-exporter-tool anki quiz.md cards.csv

# Generate HTML quiz
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "My Quiz"
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### flashhero - Export to Flashcard Hero

Export quiz markdown to Flashcard Hero TSV format with tab-separated question/answer pairs.

**Usage:**
```bash
markdown-quiz-exporter-tool flashhero INPUT_FILE OUTPUT_FILE [OPTIONS]
```

**Arguments:**
- `INPUT_FILE`: Path to quiz markdown file (*.md)
- `OUTPUT_FILE`: Path where TSV file will be written (*.tsv)
- `--force` / `-f`: Overwrite output file if it exists
- `-v/-vv/-vvv`: Verbosity levels (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Basic export
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv

# Overwrite existing file
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv --force

# With verbose output for debugging
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv -vv
```

**Output Format:**
```
Question<TAB>Answer
Question<TAB>Answer1; Answer2; Answer3
```

For questions with multiple correct answers, they are joined with "; " separator.

---

### anki - Export to Anki

Export quiz markdown to Anki CSV format supporting two note types: AllInOne (quiz) and Basic (recall).

**Usage:**
```bash
markdown-quiz-exporter-tool anki INPUT_FILE OUTPUT_FILE [OPTIONS]
```

**Arguments:**
- `INPUT_FILE`: Path to quiz markdown file (*.md)
- `OUTPUT_FILE`: Path where CSV file will be written (*.csv)
- `--quiz`: Export as AllInOne quiz format (default)
- `--recall`: Export as Basic recall format
- `--force` / `-f`: Overwrite output file if it exists
- `-v/-vv/-vvv`: Verbosity levels (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Export as quiz format (default)
markdown-quiz-exporter-tool anki quiz.md quiz-cards.csv

# Export as recall format
markdown-quiz-exporter-tool anki quiz.md recall-cards.csv --recall

# Overwrite existing file
markdown-quiz-exporter-tool anki quiz.md cards.csv --force

# With verbose output
markdown-quiz-exporter-tool anki quiz.md cards.csv -vv
```

**Output Formats:**

**AllInOne (--quiz):**
```
Question;Title;QType;Q_1;Q_2;Q_3;Q_4;Q_5;Answers;Sources;Extra1;Tags
```

**Basic (--recall):**
```
Front;Back;Tags
```

**Note:** AllInOne format supports maximum 5 answer options. Questions with more than 5 options will have only the first 5 included.

---

### quiz-html - Generate Interactive HTML Quiz

Generate self-contained HTML quiz page with embedded CSS, JavaScript, and quiz data.

**Usage:**
```bash
markdown-quiz-exporter-tool quiz-html INPUT_FILE OUTPUT_FILE --title "TITLE" [OPTIONS]
```

**Arguments:**
- `INPUT_FILE`: Path to quiz markdown file (*.md)
- `OUTPUT_FILE`: Path where HTML file will be written (*.html)
- `--title "TITLE"`: Quiz title displayed on intro page (required)
- `--force` / `-f`: Overwrite output file if exists
- `-v/-vv/-vvv`: Verbosity levels (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Generate quiz HTML
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "My Quiz"

# Overwrite existing file
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "Quiz" --force

# With verbose output
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "Quiz" -vv
```

**Features:**
- Dark/light mode with system preference detection and manual toggle
- Configurable question/answer shuffling on intro page
- Progress tracking with visual progress bar
- Timer tracking elapsed time
- Statistics page with score percentage and per-question review
- Review mode for detailed answer inspection
- Session storage for progress persistence across page refreshes
- Mobile-responsive design using Tailwind CSS
- Markdown rendering in explanation text
- Always-visible "Volgende" (Next) button for easy navigation
- Single self-contained HTML file (no external dependencies except Tailwind CDN)

**Output:**
Self-contained HTML file (typically 30-50 KB) containing:
- Embedded quiz data (JSON)
- Embedded JavaScript quiz application
- Embedded CSS styling
- Tailwind CSS via CDN
- Marked.js for markdown rendering

</details>

<details>
<summary><strong>📝 Quiz Markdown Format (Click to expand)</strong></summary>

### Format Specification

Quiz markdown files must follow this format:

```markdown
Question text here?

- (X) Correct answer
- ( ) Wrong answer 1
- ( ) Wrong answer 2

# reason
Explanation text here with markdown support.
Can include **bold**, *italic*, and other markdown features.

---

Another question?

- [X] Correct answer 1
- [X] Correct answer 2
- [ ] Wrong answer

# reason
Explanation for multiple choice question.

---
```

### Format Rules

1. **Question Text**: Plain text (no `##` header needed)
2. **Single Choice Answers**: Use `( )` for incorrect, `(X)` for correct (radio buttons)
3. **Multiple Choice Answers**: Use `[ ]` for incorrect, `[X]` for correct (checkboxes)
4. **Explanation**: Use `# reason` header followed by explanation text
5. **Separator**: Use `---` between questions
6. **Question Types**:
   - Single choice: Use `( )` and `(X)` notation
   - Multiple choice: Use `[ ]` and `[X]` notation

### Category Extraction

Questions can include category prefixes (used by HTML quiz for badges):

```markdown
CATEGORY: Question text?
```

This will:
- Extract "CATEGORY" as the category
- Display "Question text?" as the clean question text
- Show category badge in HTML quiz

Example:
```markdown
S3: What is the max size of an S3 object in GB?

- ( ) 1000
- (X) 5000
- ( ) 10000

# reason
The maximum size is 5TB or 5000GB.

---
```

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

### HTML Quiz Interactive Features

**Configuration Page:**
- Shuffle questions checkbox
- Shuffle answers checkbox
- Auto-advance option (disabled by default)
- Auto-advance delay setting (1-10 seconds)

**Question Page:**
- Progress bar showing current question/total
- Category badge (if present)
- Radio buttons (single choice) or checkboxes (multiple choice)
- "Controleren" (Check) button
- "Volgende" (Next) button (always visible)
- "Vorige" (Previous) button (if not first question)
- Visual feedback: green for correct, red for incorrect
- Markdown-rendered explanation after checking

**Statistics Page:**
- Circular score percentage indicator
- Score fraction (correct/total)
- Time elapsed (MM:SS format)
- Status: Geslaagd (≥75%), Voldoende (≥50%), Onvoldoende (<50%)
- Clickable question list for review

**Review Mode:**
- Read-only view of questions
- All correct answers highlighted in green
- Incorrect selected answers highlighted in red
- Full explanation visible
- "Terug naar resultaten" (Back to results) button

**Dark/Light Mode:**
- Auto-detect system preference on load
- Manual toggle button (fixed top-right)
- Smooth transitions between modes
- Custom scrollbar styling for dark mode

**State Persistence:**
- Uses session storage (not local storage)
- Saves: current page, answers, checked status, config, timestamps
- Clears on browser close
- Persists on page refresh

### Verbosity Levels

Control output detail with `-v` flags:

```bash
# Default: Warnings only
markdown-quiz-exporter-tool anki quiz.md output.csv

# INFO: High-level operations
markdown-quiz-exporter-tool anki quiz.md output.csv -v

# DEBUG: Detailed debugging
markdown-quiz-exporter-tool anki quiz.md output.csv -vv

# TRACE: Library internals
markdown-quiz-exporter-tool anki quiz.md output.csv -vvv
```

### Force Overwrite

By default, commands fail if output file exists:

```bash
# Fails if output.csv exists
markdown-quiz-exporter-tool anki quiz.md output.csv

# Overwrites without confirmation
markdown-quiz-exporter-tool anki quiz.md output.csv --force
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: "Error: Quiz file not found"**
```bash
Error: Quiz file not found: quiz.md
```

**Solution:**
- Verify file path is correct
- Use absolute path if relative path fails
- Check file exists: `ls -la quiz.md`

---

**Issue: "Error parsing quiz file"**
```bash
Error parsing quiz file: Invalid question format
```

**Solution:**
- Verify markdown format follows specification
- Check for missing `##` question headers
- Ensure answers use `- [ ]` or `- [x]` format
- Verify `---` separators between questions
- Use `-vv` for detailed parse errors

---

**Issue: "Output file already exists"**
```bash
Error: Output file 'output.csv' already exists. Use --force to overwrite.
```

**Solution:**
- Add `--force` flag to overwrite
- Or delete existing file first
- Or use different output filename

---

**Issue: "Questions exceed 5-option limit"**
```bash
Warning: 3 question(s) have more than 5 answer options.
Only the first 5 will be included in AllInOne format.
```

**Solution:**
- This is expected for Anki AllInOne format (5 option limit)
- Options: 
  1. Use Basic format: `--recall`
  2. Reduce answers to 5 per question
  3. Accept that only first 5 are exported

---

**Issue: "HTML quiz not displaying correctly"**

**Symptoms:**
- Layout broken
- Dark mode not working
- JavaScript errors

**Solution:**
- Verify file opened in modern browser (Chrome 90+, Firefox 88+, Safari 14+)
- Check browser console for JavaScript errors
- Ensure internet connection (Tailwind CDN required)
- Clear browser cache and reload
- Try opening in different browser

---

**Issue: "Markdown not rendering in quiz explanation"**

**Solution:**
- Verify `marked.js` loaded (check browser console)
- Ensure markdown syntax is correct
- Try basic markdown first (bold, italic)
- Check browser supports ES6+ JavaScript

### Getting Help

```bash
# Main help
markdown-quiz-exporter-tool --help

# Command-specific help
markdown-quiz-exporter-tool flashhero --help
markdown-quiz-exporter-tool anki --help
markdown-quiz-exporter-tool quiz-html --help

# Version information
markdown-quiz-exporter-tool --version

# Shell completion
markdown-quiz-exporter-tool completion bash
markdown-quiz-exporter-tool completion zsh
```

</details>

## Exit Codes

- `0`: Success
- `1`: Error (file not found, parse error, write error, etc.)

## Output Formats

**Flashcard Hero TSV:**
- Tab-separated values
- Two columns: Question, Answer
- Multiple correct answers joined with "; "

**Anki AllInOne CSV:**
- Semicolon-separated values
- 12 columns with question, answer options, correct answers
- Maximum 5 answer options per question

**Anki Basic CSV:**
- Semicolon-separated values
- 3 columns: Front, Back, Tags
- Simple question/answer format

**HTML Quiz:**
- Self-contained HTML5 file
- Embedded JSON quiz data
- Embedded JavaScript application
- Tailwind CSS via CDN
- Marked.js for markdown rendering
- Typically 30-50 KB file size

## Best Practices

1. **Validate Quiz Format**: Always check your markdown follows the format specification before exporting
2. **Use Verbosity**: Add `-vv` when debugging to see detailed error messages
3. **Keep Backups**: Use `--force` carefully to avoid overwriting important files
4. **Test HTML Quiz**: Open generated HTML in browser to verify all features work correctly
5. **Limit Answer Options**: For Anki AllInOne format, keep questions to 5 or fewer options
6. **Use Categories**: Add category prefixes (e.g., "S3:", "IAM:") for better organization in HTML quiz
7. **Write Clear Explanations**: Use markdown formatting in explanations for better readability
8. **Mobile Testing**: Test HTML quiz on mobile devices for responsive design verification

## Resources

- **GitHub**: https://github.com/dnvriend/markdown-quiz-exporter-tool
- **Documentation**: See README.md in repository
- **Quiz Format**: See example-quiz.md for format reference
- **HTML Example**: See example-quiz.html for generated output example
