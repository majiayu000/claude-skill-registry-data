---
name: evo-ocr-preprocess-extract
description: Preprocesses receipt images and extracts text using Tesseract OCR with optimal settings for receipt layouts.
---

# evo-ocr-preprocess-extract

Preprocesses receipt images using Pillow (grayscale, upscaling, contrast enhancement, binarization) and extracts raw text using pytesseract with optimal PSM configuration for receipt layouts.

## Key Functions

- `get_sorted_image_files(directory_path)` - Returns sorted list of (filename, full_path) tuples
- `preprocess_image(image_path, scale_factor=2, contrast_factor=2.0, threshold=140)` - Preprocesses image for OCR
- `extract_text_from_image(image_path, psm=4, oem=3, ...)` - Extracts text with preprocessing + Tesseract
- `extract_text_multi_config(image_path)` - Tries multiple configs for best result

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-ocr-preprocess-extract/scripts')
from utils import get_sorted_image_files, extract_text_from_image

files = get_sorted_image_files('/path/to/images')
for filename, filepath in files:
    text = extract_text_from_image(filepath)
```

## Pipeline
1. Grayscale conversion (handles RGBA/RGB)
2. 2x upscale with LANCZOS resampling
3. Contrast enhancement (factor 2.0)
4. Median filter denoising
5. Binarization (threshold 140)
6. Tesseract OCR with PSM 4 (single column)
