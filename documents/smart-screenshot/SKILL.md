---
name: smart-screenshot
description: Intelligent screenshot and screen capture with OCR, markdown conversion, and annotation. Triggered by PrtSc key, captures screen regions, extracts text with OCR, converts to markdown using MarkItDown, saves with auto-formatting. Similar to Windows Snipping Tool with AI enhancements for text extraction and document processing.
---

# Smart Screenshot

Intelligent screen capture with OCR, markdown conversion, and smart formatting. Capture screen regions, extract text, convert images/PDFs to markdown, and save with automated formatting.

## Quick Start

**Trigger methods:**
1. **Keyboard shortcut:** Press `PrtSc` (customizable)
2. **Command line:** `python scripts/capture.py`
3. **Claude Code:** Ask Claude to "take a screenshot"

**Workflow:**
1. Press PrtSc → Capture mode activates
2. Choose: **Image** or **Text**
3. Select region/window
4. **If Image:** Save with annotation options
5. **If Text:** OCR → MarkItDown → Save markdown

## Prerequisites

### System Requirements
- Windows 10/11, macOS 10.14+, or Linux
- Python 3.8+
- Screen with display access

### Install Dependencies

**Core (required):**
```bash
# Screenshot and OCR
pip install pillow pyautogui mss pytesseract pyscreenshot --break-system-packages

# MarkItDown (Microsoft's converter)
pip install markitdown --break-system-packages

# Keyboard hooks
pip install keyboard pynput --break-system-packages

# GUI for dialogs
pip install tkinter --break-system-packages  # May be pre-installed
```

**OCR engine (Tesseract):**

**Windows:**
```bash
# Download installer from:
# https://github.com/UB-Mannheim/tesseract/wiki
# Install to: C:\Program Files\Tesseract-OCR\
# Add to PATH
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
# or
sudo dnf install tesseract
```

**Optional enhancements:**
```bash
# Better OCR (EasyOCR - slower but more accurate)
pip install easyocr --break-system-packages

# PDF handling
pip install pdf2image pypdf2 --break-system-packages

# Image enhancement
pip install opencv-python --break-system-packages

# Clipboard integration
pip install pyperclip --break-system-packages
```

See [reference/setup-guide.md](reference/setup-guide.md) for detailed installation.

## Features

### Capture Modes

**1. Region Selection**
- Click and drag to select area
- Real-time preview
- Pixel-perfect selection

**2. Window Capture**
- Automatically detect windows
- Capture specific application
- Includes/excludes borders

**3. Full Screen**
- Entire display
- Multi-monitor support
- All screens at once

**4. Scrolling Capture**
- Capture long web pages
- Auto-scroll and stitch
- Perfect for documentation

### Text Extraction

**OCR Engines:**
- **Tesseract** - Fast, free, 100+ languages
- **EasyOCR** - Slower, more accurate
- **Cloud OCR** - Azure/Google (highest accuracy)

**Smart text processing:**
- Automatic language detection
- Text cleanup and formatting
- Table recognition
- Layout preservation

### Markdown Conversion

**Using MarkItDown (Microsoft):**
- Images → Markdown with alt text
- PDFs → Clean markdown
- Screenshots → Formatted text
- Tables → Markdown tables
- Code blocks → Syntax highlighting

**Conversion features:**
- Smart heading detection
- List preservation
- Link extraction
- Code formatting
- Table structure recognition

## Core Operations

### Quick Capture

**Keyboard shortcut:**
```bash
# Run as background service
python scripts/screenshot_service.py

# Now press PrtSc anytime:
# 1. Screen freezes
# 2. Choose "Image" or "Text"
# 3. Select region
# 4. Auto-process and save
```

**Command line:**
```bash
# Capture with UI
python scripts/capture.py

# Capture full screen immediately
python scripts/capture.py --fullscreen --output screenshot.png

# Capture region with coordinates
python scripts/capture.py --region 100,100,800,600 --output region.png
```

### Text Mode (OCR → Markdown)

**Interactive:**
```bash
# Start capture
python scripts/capture.py --mode text

# Process:
# 1. Select region
# 2. OCR extracts text
# 3. MarkItDown formats
# 4. Save dialog opens
# 5. Save as .md file
```

**Automatic:**
```bash
# Capture and OCR
python scripts/capture_text.py --output extracted.md

# With specific language
python scripts/capture_text.py --lang eng+fra --output text.md

# With enhancement
python scripts/capture_text.py --enhance --output clean.md
```

### Image Mode

**Interactive:**
```bash
# Start capture
python scripts/capture.py --mode image

# Process:
# 1. Select region
# 2. Annotation tools appear
# 3. Add arrows, boxes, text
# 4. Save dialog opens
```

**With annotations:**
```bash
# Capture and annotate
python scripts/capture_annotate.py --output annotated.png

# Annotation tools:
# - Arrow
# - Rectangle
# - Circle
# - Text
# - Highlight
# - Blur (redact sensitive info)
```

### PDF to Markdown

**Convert PDF to markdown:**
```bash
# Using MarkItDown
python scripts/pdf_to_markdown.py --input document.pdf --output document.md

# With OCR for scanned PDFs
python scripts/pdf_to_markdown.py --input scanned.pdf --ocr --output text.md

# Batch convert folder
python scripts/batch_pdf_convert.py --input ./pdfs/ --output ./markdown/
```

### Screenshot from Image

**Process existing image:**
```bash
# Extract text to markdown
python scripts/image_to_markdown.py --input screenshot.png --output text.md

# Clean up image first
python scripts/enhance_and_extract.py --input noisy.png --output clean.md
```

## Configuration

**Settings file:** `config.yaml`

```yaml
# Keyboard shortcut
hotkey: "Print"  # or "ctrl+shift+s", "cmd+shift+5", etc.

# Default capture mode
default_mode: "prompt"  # "image", "text", or "prompt"

# OCR settings
ocr:
  engine: "tesseract"  # "tesseract", "easyocr", or "cloud"
  language: "eng"
  enhance: true  # Pre-process image for better OCR

# Output settings
output:
  directory: "~/Screenshots"
  filename_pattern: "Screenshot-{date}-{time}"
  auto_save: false  # true = skip save dialog
  clipboard: true   # Copy to clipboard

# Markdown settings
markdown:
  format_code_blocks: true
  detect_tables: true
  preserve_formatting: true
  
# Annotation defaults
annotation:
  arrow_color: "#FF0000"
  box_color: "#0000FF"
  text_color: "#000000"
  text_size: 12
  line_width: 2
```

## Common Workflows

### Workflow 1: Code Documentation

**Scenario:** Capture code from screen → Markdown documentation

```bash
# 1. Run screenshot service
python scripts/screenshot_service.py &

# 2. Press PrtSc on your keyboard

# 3. Select "Text" mode

# 4. Select code region on screen

# 5. OCR extracts code

# 6. MarkItDown formats as code block:
```python
def example_function():
    return "formatted code"
```

# 7. Save dialog opens → Save as code-snippet.md
```

### Workflow 2: Meeting Notes from Slides

**Scenario:** Capture presentation slides → Formatted notes

```bash
# Capture multiple slides
python scripts/capture_sequence.py \
  --count 5 \
  --delay 3 \
  --mode text \
  --output slides.md

# Result: All slides as markdown in one file
```

### Workflow 3: Email/Document Processing

**Scenario:** Screenshot email → Extract and format text

```bash
# Capture email
python scripts/capture.py --mode text --enhance

# Text extracted, formatted, and saved
# Perfect for archiving or processing
```

### Workflow 4: Research Paper Annotation

**Scenario:** Screenshot paper → Annotate → Save

```bash
# Capture and annotate
python scripts/capture_annotate.py --output paper-notes.png

# Add arrows, highlights, notes
# Save annotated version
```

### Workflow 5: Batch PDF Conversion

**Scenario:** Convert all PDFs to markdown

```bash
# Convert folder of PDFs
python scripts/batch_pdf_convert.py \
  --input ~/Documents/PDFs/ \
  --output ~/Documents/Markdown/ \
  --ocr  # Enable OCR for scanned docs
  
# Progress shown for each file
# All PDFs → Clean markdown
```

## MarkItDown Features

**Microsoft's MarkItDown converts:**

**Images:**
- Screenshots → Extracted text
- Diagrams → Alt text descriptions
- Charts → Data tables

**PDFs:**
- Native PDFs → Clean markdown
- Scanned PDFs → OCR + markdown
- Preserve structure and formatting

**Documents:**
- Word docs → Markdown
- PowerPoint → Slide content
- Excel → Markdown tables

**Code:**
- Syntax highlighted code blocks
- Language detection
- Proper indentation

**Tables:**
- Visual tables → Markdown tables
- Preserved alignment
- Header detection

## Keyboard Shortcuts

**During capture:**
- `Esc` - Cancel capture
- `Space` - Toggle crosshair/selection
- `Enter` - Confirm selection
- `Ctrl+Z` - Undo annotation
- `Ctrl+C` - Copy to clipboard
- `Ctrl+S` - Save

**Annotation mode:**
- `A` - Arrow tool
- `R` - Rectangle tool
- `C` - Circle tool
- `T` - Text tool
- `H` - Highlight tool
- `B` - Blur tool
- `Delete` - Remove last annotation

## OCR Accuracy Tips

**Better results:**
1. **Enhance image first** - Increase contrast, denoise
2. **Correct language** - Specify language(s)
3. **Proper DPI** - Higher resolution = better OCR
4. **Clean background** - Remove clutter
5. **Good lighting** - For camera captures
6. **Straight text** - Rotate if needed

**Pre-processing:**
```bash
# Enhance before OCR
python scripts/enhance_image.py \
  --input screenshot.png \
  --output enhanced.png \
  --operations "grayscale,contrast,denoise"

# Then OCR
python scripts/image_to_markdown.py --input enhanced.png
```

## Multi-Monitor Support

**Capture from specific monitor:**
```bash
# List monitors
python scripts/list_monitors.py

# Capture from monitor 2
python scripts/capture.py --monitor 2

# Capture all monitors
python scripts/capture.py --all-monitors
```

## Save Dialog Options

**When save dialog appears:**
- **Filename:** Auto-generated or custom
- **Location:** Last used or default directory
- **Format:** .md, .txt, .png, .jpg
- **Options:**
  - Copy to clipboard
  - Open in editor
  - Share

**Skip dialog (auto-save):**
```yaml
# config.yaml
output:
  auto_save: true
  directory: "~/Screenshots"
```

## Integration with Clipboard

**Copy to clipboard automatically:**
```bash
# Text mode - copies markdown
python scripts/capture.py --mode text --clipboard

# Image mode - copies image
python scripts/capture.py --mode image --clipboard

# Both
python scripts/capture.py --clipboard --save
```

**Paste from clipboard:**
```bash
# Process clipboard image
python scripts/process_clipboard.py --output result.md
```

## Running as Service

### Windows

**Install as Windows service:**
```bash
# Install
python scripts/install_windows_service.py

# Service runs on startup
# PrtSc always available
```

**Or use Task Scheduler:**
```
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At log on
4. Action: Start program
5. Program: python
6. Arguments: path\to\screenshot_service.py
```

### macOS

**LaunchAgent setup:**
```bash
# Install service
python scripts/install_macos_service.py

# Creates ~/Library/LaunchAgents/com.screenshot.service.plist
# Runs on login
```

**Manual:**
```bash
# Create LaunchAgent plist
# Load with launchctl
launchctl load ~/Library/LaunchAgents/com.screenshot.service.plist
```

### Linux

**Systemd service:**
```bash
# Install
python scripts/install_linux_service.py

# Creates ~/.config/systemd/user/screenshot.service
# Enable and start:
systemctl --user enable screenshot
systemctl --user start screenshot
```

**Or use autostart:**
```bash
# Copy desktop entry
cp screenshot.desktop ~/.config/autostart/
```

## Cloud OCR (Optional)

**For highest accuracy:**

**Azure Computer Vision:**
```bash
export AZURE_CV_KEY="your-key"
export AZURE_CV_ENDPOINT="https://your-region.api.cognitive.microsoft.com/"

python scripts/capture.py --mode text --ocr-engine azure
```

**Google Vision:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"

python scripts/capture.py --mode text --ocr-engine google
```

**Costs:**
- Azure: 1000 transactions/month free, then $1/1000
- Google: 1000 units/month free, then $1.50/1000

## Scripts Reference

**Capture:**
- `capture.py` - Main interactive capture
- `capture_text.py` - Text mode only
- `capture_annotate.py` - Image with annotations
- `capture_sequence.py` - Multiple captures

**Service:**
- `screenshot_service.py` - Background service
- `install_windows_service.py` - Windows installer
- `install_macos_service.py` - macOS installer
- `install_linux_service.py` - Linux installer

**Conversion:**
- `image_to_markdown.py` - Image → Markdown
- `pdf_to_markdown.py` - PDF → Markdown
- `batch_pdf_convert.py` - Batch conversion

**Processing:**
- `enhance_image.py` - Image enhancement
- `process_clipboard.py` - Clipboard processing
- `extract_tables.py` - Table extraction

**Utilities:**
- `list_monitors.py` - List displays
- `test_ocr.py` - Test OCR accuracy
- `configure.py` - Interactive config

## Best Practices

1. **Run as service** - Always available with hotkey
2. **Configure hotkey** - Choose comfortable shortcut
3. **Enable clipboard** - Quick copy-paste workflow
4. **Enhance first** - Better OCR results
5. **Use appropriate OCR** - Tesseract for speed, Cloud for accuracy
6. **Organize output** - Set default directory
7. **Backup settings** - Save config.yaml
8. **Test thoroughly** - Verify OCR accuracy for your use case

## Troubleshooting

**"Tesseract not found"**
```bash
# Install Tesseract
# Windows: Download installer
# macOS: brew install tesseract
# Linux: apt install tesseract-ocr

# Check installation
tesseract --version
```

**"Permission denied" (screenshot)**
```
Windows: Run as Administrator
macOS: System Preferences → Security → Privacy → Screen Recording
Linux: Check X11 permissions
```

**"Keyboard hook failed"**
```bash
# Requires administrator/root privileges
# Windows: Run as Administrator
# macOS: Grant Accessibility permissions
# Linux: Run with sudo or add user to input group
```

**"Poor OCR quality"**
```bash
# Enhance image first
python scripts/enhance_image.py --input screenshot.png

# Try different OCR engine
python scripts/capture.py --ocr-engine easyocr

# Specify language
python scripts/capture.py --lang eng+fra
```

**"MarkItDown not working"**
```bash
pip install --upgrade markitdown --break-system-packages

# Check version
python -c "import markitdown; print(markitdown.__version__)"
```

## Platform-Specific Notes

### Windows
- PrtSc key native support
- Windows Ink integration available
- OneDrive sync compatible
- Notification system integration

### macOS
- cmd+shift+5 alternative
- Quick Look preview
- iCloud Drive sync
- Notification Center integration

### Linux
- Wayland/X11 support
- Various hotkey daemons
- Desktop environment integration
- Screenshot directories vary

## Integration Examples

See [examples/](examples/) for complete workflows:
- [examples/documentation-workflow.md](examples/documentation-workflow.md) - Code docs
- [examples/research-notes.md](examples/research-notes.md) - Paper processing
- [examples/meeting-capture.md](examples/meeting-capture.md) - Meeting slides
- [examples/email-archival.md](examples/email-archival.md) - Email processing

## Reference Documentation

- [reference/setup-guide.md](reference/setup-guide.md) - Complete setup
- [reference/ocr-engines.md](reference/ocr-engines.md) - OCR comparison
- [reference/markitdown-guide.md](reference/markitdown-guide.md) - MarkItDown features
- [reference/hotkey-config.md](reference/hotkey-config.md) - Keyboard shortcuts
- [reference/service-install.md](reference/service-install.md) - Service setup
