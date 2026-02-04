---
name: marker
description: Convert documents (PDF, EPUB, PPTX, DOCX, XLSX, HTML, images) to Markdown/JSON/HTML using marker-pdf with Claude Haiku LLM enhancement for accurate table, math, and form extraction. Use when user needs to extract content from documents, convert PDFs to markdown, or process document files.
---

# Marker Document Converter

Convert PDF, EPUB, PPTX, DOCX, XLSX, HTML, and image files to clean Markdown/JSON/HTML format using the marker-pdf tool with multimodal LLM enhancement.

## Prerequisites

```bash
# Install marker-pdf with full document support
uv tool install marker-pdf[full]
```

Requires Python 3.10+ and PyTorch.

## Basic Usage

```bash
marker_single "<file_path>" \
  --output_format markdown \
  --output_dir "<output_directory>" \
  --use_llm \
  --llm_service marker.services.claude.ClaudeService \
  --claude_model_name claude-haiku-4-5 \
  --claude_api_key $ANTHROPIC_API_KEY \
  --disable_image_extraction
```

**Note**: `--disable_image_extraction` generates plain text output. Remove this flag if images need to be preserved.

## Output Formats

| Format     | Description                                                                       | Use Case                    |
| ---------- | --------------------------------------------------------------------------------- | --------------------------- |
| `markdown` | Formatted text with tables, LaTeX equations ($$-fenced), code blocks, image links | General document conversion |
| `html`     | Semantic HTML with `<img>`, `<math>`, `<pre>` tags                                | Web display                 |
| `json`     | Hierarchical structure with block types, bounding boxes, section hierarchy        | Programmatic processing     |
| `chunks`   | Flattened JSON optimized for RAG                                                  | Vector database ingestion   |

## CLI Options

### Core Options

- `--output_format`: `markdown` (default), `html`, `json`, `chunks`
- `--output_dir`: Directory for output files
- `--page_range`: Specific pages, e.g., `"0,5-10,20"`

### LLM Enhancement

- `--use_llm`: Enable LLM for improved accuracy (tables, forms, math, handwriting)
- `--llm_service`: LLM service class (see LLM Services below)
- `--block_correction_prompt`: Custom prompt for output refinement

### OCR & Processing

- `--force_ocr`: Force OCR on entire document, converts inline math to LaTeX
- `--strip_existing_ocr`: Remove existing OCR and re-process
- `--redo_inline_math`: Highest quality inline math conversion (use with `--use_llm`)

### Image & Output Control

- `--disable_image_extraction`: Skip image extraction (plain text only)
- `--paginate_output`: Add page separators to output
- `--extract_images`: Enable image extraction (default: true)

### Advanced

- `--config_json`: Load configuration from JSON file
- `--debug`: Enable diagnostic logging
- `--force_layout_block`: Force layout type, e.g., `Table`
- `--converter_cls`: Custom converter class

## LLM Services

### Claude (Default)

```bash
marker_single document.pdf \
  --use_llm \
  --llm_service marker.services.claude.ClaudeService \
  --claude_api_key $ANTHROPIC_API_KEY \
  --claude_model_name claude-haiku-4-5
```

### OpenAI

```bash
marker_single document.pdf \
  --use_llm \
  --llm_service marker.services.openai.OpenAIService \
  --openai_api_key $OPENAI_API_KEY \
  --openai_model gpt-4o
```

### Ollama (Local)

```bash
marker_single document.pdf \
  --use_llm \
  --llm_service marker.services.ollama.OllamaService \
  --ollama_base_url "http://localhost:11434" \
  --ollama_model llama3.2-vision
```

### Google Gemini (Default if no service specified)

```bash
export GOOGLE_API_KEY="your-api-key"
marker_single document.pdf --use_llm
```

## Examples

### Convert PDF to Markdown (Plain Text)

```bash
marker_single "./docs/report.pdf" \
  --output_format markdown \
  --output_dir "./docs/" \
  --use_llm \
  --llm_service marker.services.claude.ClaudeService \
  --claude_model_name claude-haiku-4-5 \
  --claude_api_key $ANTHROPIC_API_KEY \
  --disable_image_extraction
```

### Convert with Images Preserved

```bash
marker_single "./docs/report.pdf" \
  --output_format markdown \
  --output_dir "./docs/" \
  --use_llm \
  --llm_service marker.services.claude.ClaudeService \
  --claude_model_name claude-haiku-4-5 \
  --claude_api_key $ANTHROPIC_API_KEY
```

### Extract Tables Only

```bash
marker_single "./docs/spreadsheet.pdf" \
  --use_llm \
  --force_layout_block Table \
  --converter_cls marker.converters.table.TableConverter \
  --output_format json
```

### Batch Convert Multiple Files

```bash
marker /path/to/input/folder --workers 4
```

### Using JSON Config File

```bash
cat > config.json << EOF
{
  "force_ocr": true,
  "use_llm": true,
  "output_format": "markdown",
  "disable_image_extraction": true,
  "strip_existing_ocr": true,
  "redo_inline_math": true
}
EOF

marker_single document.pdf --config_json config.json
```

## Output Structure

### Markdown Output

- Image links: `![](image_name.png)`
- Tables: Formatted as markdown tables
- Equations: Fenced with `$$...$$`
- Code: Fenced with ` ```language `
- Headings: `#` for sections

### JSON Output

```json
{
  "pages": [
    {
      "id": "page_0",
      "polygon": [[x1,y1], [x2,y2], ...],
      "children": [
        {
          "id": "block_0",
          "block_type": "Text|Table|Image|...",
          "html": "<p>content</p>",
          "polygon": [...],
          "section_hierarchy": {...}
        }
      ]
    }
  ],
  "metadata": {
    "table_of_contents": [...],
    "page_stats": [...]
  }
}
```

## Instructions

1. Confirm the input file path exists
2. Determine output directory (default: same as input file)
3. **Use AskUserQuestion tool** to ask user preferences (ask both questions together):

   **Question 1 - Image Extraction**:
   - Header: "Images"
   - Question: "是否需要提取文档中的图片？"
   - Options:
     - "No (Recommended)": 仅提取文本，生成纯 Markdown 文件
     - "Yes": 提取图片并保存，Markdown 中包含图片链接

   **Question 2 - LLM Service**:
   - Header: "LLM"
   - Question: "使用哪个 LLM 来识别图片和表格内容？"
   - Options:
     - "Claude Haiku (Recommended)": 快速、经济，需要 ANTHROPIC_API_KEY
     - "Claude Sonnet": 更高质量，需要 ANTHROPIC_API_KEY
     - "GPT-4o": OpenAI 模型，需要 OPENAI_API_KEY
     - "Ollama (Local)": 本地运行，无需 API Key

4. Based on user's answers, construct the command:
   - If "No" for images: add `--disable_image_extraction`
   - Set LLM service parameters according to selection:
     - Claude Haiku: `--llm_service marker.services.claude.ClaudeService --claude_model_name claude-haiku-4-5 --claude_api_key $ANTHROPIC_API_KEY`
     - Claude Sonnet: `--llm_service marker.services.claude.ClaudeService --claude_model_name claude-sonnet-4-20250514 --claude_api_key $ANTHROPIC_API_KEY`
     - GPT-4o: `--llm_service marker.services.openai.OpenAIService --openai_api_key $OPENAI_API_KEY --openai_model gpt-4o`
     - Ollama: `--llm_service marker.services.ollama.OllamaService --ollama_base_url "http://localhost:11434" --ollama_model llama3.2-vision`

5. Run the `marker_single` command with chosen options
6. Report the output file location and any extraction notes
