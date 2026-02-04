---
name: skill-ollama-deepseek-ocr-tool
description: Batch OCR processing with DeepSeek-OCR via Ollama
---

# When to use

- Convert textbook/lecture images to markdown notes
- Batch OCR processing of scanned documents
- Extract text from image sequences (iPhone photos, screenshots)
- Create searchable markdown from visual content
- Process documents privately without cloud services

# ollama-deepseek-ocr-tool Skill

## Purpose

This skill provides access to `ollama-deepseek-ocr-tool`, a CLI tool for fast, private batch OCR processing using DeepSeek-OCR via Ollama. Converts sequences of images (textbook pages, slides, scans) into a single coherent markdown document.

**Key capabilities:**
- ⚡ Fast processing (~3s per image on M4)
- 🔒 Private - runs entirely locally
- 📝 Clean markdown output (tables, headings, lists)
- 🔄 Natural sorting (IMG_1 < IMG_2 < IMG_10)
- 💰 Free - no API costs or rate limits

## When to Use This Skill

**Use this skill when:**
- Converting textbook chapters to Obsidian notes
- Processing lecture slides or handouts to markdown
- Extracting text from scanned documents
- Creating searchable study materials from images
- Need comprehensive examples and troubleshooting

**Do NOT use this skill for:**
- Cloud-based OCR (this is local-only)
- Describing image content (extracts text only)
- Handwritten text recognition (printed text only)
- Real-time streaming OCR (batch processing only)

## CLI Tool: ollama-deepseek-ocr-tool

The `ollama-deepseek-ocr-tool` processes multiple images in sequence and creates a single markdown document with extracted text. Images are sorted naturally and text is appended sequentially for coherent reading.

### Installation

```bash
# Clone and install
git clone https://github.com/dnvriend/ollama-deepseek-ocr-tool.git
cd ollama-deepseek-ocr-tool
uv tool install .
```

### Prerequisites

1. **Ollama** - Local LLM runtime
   ```bash
   brew install ollama
   ollama serve
   ```

2. **DeepSeek-OCR model** (~6GB download)
   ```bash
   ollama pull deepseek-ocr
   ```

3. **Python 3.14+** and **uv package manager**

### Quick Start

```bash
# Example 1: Process textbook chapter from iPhone photos
ollama-deepseek-ocr-tool "IMG_*.png" chapter-3-notes.md

# Example 2: Convert lecture slides to markdown
ollama-deepseek-ocr-tool "lecture-week5/*.jpg" week5-summary.md

# Example 3: With verbose logging to debug issues
ollama-deepseek-ocr-tool "*.png" output.md -vv
```

### Main Command - Batch OCR Processing

Process images matching a glob pattern and create a markdown document.

**Usage:**
```bash
ollama-deepseek-ocr-tool GLOB_PATTERN OUTPUT_FILE [OPTIONS]
```

**Arguments:**
- `GLOB_PATTERN`: Pattern to match images (e.g., "*.png", "dir/*.jpg")
- `OUTPUT_FILE`: Path to output markdown file (will be overwritten)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)
- `--help`: Show comprehensive help with examples
- `--version`: Show version

**Examples:**
```bash
# Basic: Process all PNGs in current directory
ollama-deepseek-ocr-tool "*.png" output.md

# Process specific directory
ollama-deepseek-ocr-tool "textbook-ch3/*.jpg" chapter-3.md

# With verbose logging
ollama-deepseek-ocr-tool "*.png" output.md -vv

# Preview help (shows all examples)
ollama-deepseek-ocr-tool --help
```

**Output Format:**
```markdown
<!-- Source: IMG_4170.png -->

[extracted text from image 1]

---

<!-- Source: IMG_4171.png -->

[extracted text from image 2]
```

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

<!-- TODO: Add advanced features documentation -->

### Multi-Level Verbosity Logging

Control logging detail with progressive verbosity levels. All logs output to stderr.

**Logging Levels:**

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals | Deep debugging |

**Examples:**
```bash
# INFO level - see operations
ollama-deepseek-ocr-tool command -v

# DEBUG level - see detailed info
ollama-deepseek-ocr-tool command -vv

# TRACE level - see all internals
ollama-deepseek-ocr-tool command -vvv
```

---

### What Can Be Extracted

**Text & Formatting:**
- ✅ Headings (H1, H2, H3)
- ✅ Body text with bold/italic
- ✅ Bulleted and numbered lists
- ✅ Multi-column layouts

**Tables:**
- ✅ Clean markdown table format
- ✅ Headers and structure preserved
- ✅ Merged cells handled

**Diagrams & Figures:**
- ✅ Text labels extracted
- ✅ Figure captions captured
- ❌ Visual content not described
- ❌ Flowchart arrows not preserved

### Performance Characteristics

- **Speed**: ~3 seconds per image (M4 MacBook)
- **Memory**: ~6GB (DeepSeek-OCR model)
- **Throughput**: ~20 images per minute
- **Scalability**: Sequential processing (no parallel batching)

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: "No files match pattern"**
```bash
# Check your glob pattern and current directory
ls *.png  # Verify files exist

# Use absolute or relative paths correctly
ollama-deepseek-ocr-tool "./images/*.png" output.md
```

**Issue: "Connection refused" / "OCR extraction failed"**
```bash
# Ensure Ollama is running
ollama serve

# Verify model is installed
ollama list | grep deepseek-ocr

# Pull model if missing
ollama pull deepseek-ocr
```

**Issue: Poor quality extraction**
- Use `-vv` flag to see word counts and verify extraction
- Check image quality (resolution, clarity)
- For complex layouts, results may vary
- Tables and diagrams work best with clear text

**Issue: Slow processing**
- Expected: ~3 seconds per image on M4
- Check if Ollama is using GPU acceleration
- Sequential processing is by design (6GB model)

### Getting Help

```bash
# Show comprehensive help with examples
ollama-deepseek-ocr-tool --help

# Use verbose logging to debug
ollama-deepseek-ocr-tool "*.png" output.md -vv
```

</details>

## Exit Codes

- `0`: Success - all images processed
- `1`: Validation error - no files match pattern or invalid arguments
- `2`: Runtime error - Ollama connection failed or model not found

## Best Practices

1. **Organize images before processing**: Name files sequentially (IMG_001, IMG_002) for natural sorting
2. **Use descriptive output names**: `chapter-3-entrepreneurship.md` not `output.md`
3. **Start with small batches**: Test with 2-3 images first to verify quality
4. **Enable verbose logging for debugging**: Use `-vv` to see extraction progress and word counts
5. **Review output after processing**: OCR may miss formatting or misread complex layouts
6. **Keep images at good resolution**: Higher quality = better extraction
7. **Process similar content together**: Keep textbook pages separate from diagrams

## Resources

- **GitHub**: https://github.com/dnvriend/ollama-deepseek-ocr-tool
- **Python Package Index**: https://pypi.org/project/ollama-deepseek-ocr-tool/
- **Documentation**: <!-- TODO: Add documentation URL if available -->
