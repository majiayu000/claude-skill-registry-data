---
name: datalab
description: Convert documents (PDF, EPUB, PPTX, DOCX, XLSX, HTML, images) to Markdown using Datalab cloud API. Use when user wants to use Datalab API for document conversion, or prefers cloud-based processing over local marker CLI.
---

# Datalab Document Converter

Convert PDF, EPUB, PPTX, DOCX, XLSX, HTML, and image files to Markdown using the Datalab cloud API.

## Prerequisites

```bash
# Install Datalab Python SDK
uv pip install datalab-python-sdk

# Set API key (get from https://www.datalab.to)
export DATALAB_API_KEY="your_api_key_here"
```

## Python SDK Usage

### Basic Conversion

```python
from datalab_sdk import DatalabClient

client = DatalabClient()  # Uses DATALAB_API_KEY env var

# Convert document to markdown
result = client.convert("document.pdf")
print(result.markdown)

# Save output
result = client.convert(
    "document.pdf",
    save_output="./output/document"
)
# Creates: output/document.md, output/document_meta.json, output/*.png
```

### With Options

```python
from datalab_sdk import DatalabClient, ConvertOptions

client = DatalabClient()

options = ConvertOptions(
    output_format="markdown",  # markdown, json, html, chunks
    force_ocr=False,           # Force OCR on all pages
    paginate=True,             # Add page separators
    use_llm=True,              # Use LLM for better accuracy
    disable_image_extraction=True,  # Plain text only
    page_range="0,5-10,20"     # Specific pages
)

result = client.convert("document.pdf", options=options)
```

### Async Client (Better Performance)

```python
import asyncio
from datalab_sdk import AsyncDatalabClient, ConvertOptions

async def convert_document():
    async with AsyncDatalabClient() as client:
        result = await client.convert(
            "document.pdf",
            options=ConvertOptions(output_format="markdown")
        )
        return result.markdown

markdown = asyncio.run(convert_document())
print(markdown)
```

### OCR Only

```python
from datalab_sdk import DatalabClient

client = DatalabClient()

# OCR a document
ocr_result = client.ocr("document.pdf")
print(ocr_result.pages)  # Get all text
```

## REST API Usage

### Submit Document for Conversion

```python
import requests

url = "https://www.datalab.to/api/v1/marker"
headers = {"X-API-Key": "YOUR_API_KEY"}

with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    data = {
        "output_format": (None, "markdown"),
        "force_ocr": (None, "false"),
        "use_llm": (None, "false"),
        "disable_image_extraction": (None, "true")
    }
    response = requests.post(url, headers=headers, files=files, data=data)

result = response.json()
print(f"Request ID: {result['request_id']}")
print(f"Check URL: {result['request_check_url']}")
```

### Poll for Results

```python
import requests
import time

check_url = result['request_check_url']
headers = {"X-API-Key": "YOUR_API_KEY"}

while True:
    response = requests.get(check_url, headers=headers)
    status = response.json()

    if status.get('status') == 'complete':
        print(status['markdown'])
        break
    elif status.get('status') == 'failed':
        print(f"Error: {status.get('error')}")
        break

    time.sleep(2)  # Poll every 2 seconds
```

### Using curl

```bash
# Submit document
curl -X POST "https://www.datalab.to/api/v1/marker" \
  -H "X-API-Key: $DATALAB_API_KEY" \
  -F "file=@document.pdf" \
  -F "output_format=markdown" \
  -F "disable_image_extraction=true"

# Check status
curl "https://www.datalab.to/api/v1/marker/{request_id}" \
  -H "X-API-Key: $DATALAB_API_KEY"
```

## API Options

| Parameter                  | Type    | Description                          |
| -------------------------- | ------- | ------------------------------------ |
| `output_format`            | string  | `markdown`, `json`, `html`, `chunks` |
| `force_ocr`                | boolean | Force OCR on all pages               |
| `paginate`                 | boolean | Add page separators                  |
| `use_llm`                  | boolean | Use LLM for better accuracy          |
| `strip_existing_ocr`       | boolean | Remove existing OCR and re-process   |
| `disable_image_extraction` | boolean | Plain text only                      |
| `page_range`               | string  | Specific pages, e.g., `"0,5-10,20"`  |
| `max_pages`                | integer | Maximum pages to convert             |

## Batch Processing

```python
import asyncio
from pathlib import Path
from datalab_sdk import AsyncDatalabClient, ConvertOptions

async def batch_convert(files: list[Path], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    options = ConvertOptions(
        output_format="markdown",
        disable_image_extraction=True
    )

    async with AsyncDatalabClient() as client:
        tasks = [
            client.convert(
                file_path=f,
                options=options,
                save_output=output_dir / f.stem
            )
            for f in files
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for f, result in zip(files, results):
        if isinstance(result, Exception):
            print(f"✗ {f.name}: {result}")
        elif result.success:
            print(f"✓ {f.name}: {result.page_count} pages")
        else:
            print(f"✗ {f.name}: {result.error}")

# Usage
files = list(Path("documents").glob("*.pdf"))
asyncio.run(batch_convert(files, Path("output")))
```

## Error Handling

```python
from datalab_sdk import (
    DatalabClient,
    DatalabAPIError,
    DatalabTimeoutError,
    DatalabFileError
)

client = DatalabClient()

try:
    result = client.convert("document.pdf", max_polls=60, poll_interval=2)

    if result.success:
        print(result.markdown)
    else:
        print(f"Conversion failed: {result.error}")

except DatalabAPIError as e:
    if e.status_code == 401:
        print("Authentication failed - check API key")
    elif e.status_code == 429:
        print("Rate limit exceeded - wait before retrying")
    else:
        print(f"API Error: {e}")

except DatalabTimeoutError:
    print("Operation timed out - try increasing max_polls")

except DatalabFileError as e:
    print(f"File error: {e}")
```

## Datalab vs Marker CLI

| Feature      | Datalab API        | Marker CLI          |
| ------------ | ------------------ | ------------------- |
| Processing   | Cloud-based        | Local               |
| GPU Required | No                 | Yes (recommended)   |
| Setup        | API key only       | Python + PyTorch    |
| Speed        | Fast (cloud GPU)   | Depends on hardware |
| Privacy      | Data sent to cloud | Local processing    |
| Cost         | API credits        | Free                |

## Instructions

1. Confirm the input file path exists
2. Check if `$DATALAB_API_KEY` environment variable is set
3. **Use AskUserQuestion tool** to ask user preferences:

   **Question 1 - Processing Method**:
   - Header: "Method"
   - Question: "使用哪种方式调用 Datalab API？"
   - Options:
     - "Python SDK (Recommended)": 使用 datalab-python-sdk，更简洁
     - "REST API": 使用 requests 直接调用 API
     - "curl": 使用命令行 curl

   **Question 2 - Image Extraction**:
   - Header: "Images"
   - Question: "是否需要提取文档中的图片？"
   - Options:
     - "No (Recommended)": 仅提取文本，生成纯 Markdown
     - "Yes": 提取图片并保存

4. Generate and run the appropriate code based on user's choice
5. Report the output file location and any extraction notes
