---
name: pdf-ocr-skill
description: 支持双引擎的PDF OCR识别技能，可从影印版PDF文件和图片文件中提取中英文文字内容 | PDF OCR Skill with dual-engine support, capable of extracting Chinese and English text from scanned PDF files and image files
version: 2.3.0
author: yejinlei
license: MIT
tags:
  - ocr
  - pdf
  - image
  - text-extraction
  - chinese
  - english
  - siliconflow
  - deepseek
  - rapidocr
  - local-ocr
---

# PDF OCR Skill

## 中文版本

PDF OCR技能用于从影印版PDF文件和图片文件中提取文字内容。该技能支持两种OCR引擎：
- **RapidOCR**（本地引擎）：无需API密钥，免费使用，识别速度快
- **硅基流动大模型**（云端引擎）：使用AI大模型进行高精度OCR识别

### 功能特性

- 支持影印版PDF文件的文字提取
- 支持多种图片格式的文字识别（JPG、PNG、BMP、GIF、TIFF、WEBP）
- **双引擎支持**：RapidOCR（本地）和硅基流动API（云端）
- 支持中文和英文文字识别
- 保持文字的顺序和结构
- 自动将PDF页面转换为图片进行识别
- 智能引擎切换：当RapidOCR初始化失败时自动切换到硅基流动API

### 安装

#### 依赖要求

```bash
pip install pymupdf pillow requests python-dotenv
```

#### 可选依赖（推荐）

安装RapidOCR以获得本地识别能力：

```bash
pip install rapidocr_onnxruntime
```

### 环境变量配置

1. 复制 `.env.example` 文件并重命名为 `.env`
2. 根据需要配置以下选项：

```env
# OCR引擎选择
# - "rapid": 使用RapidOCR本地引擎（默认，无需API密钥）
# - "siliconflow": 使用硅基流动API引擎（需要API密钥）
OCR_ENGINE=rapid

# 如果使用硅基流动API引擎，需要配置以下选项：
SILICON_FLOW_API_KEY=your_api_key_here
SILICON_FLOW_OCR_MODEL=deepseek-ai/DeepSeek-OCR
```

### 快速开始

#### 使用默认引擎（RapidOCR本地识别）

```python
# 导入OCR处理器
from scripts.pdf_ocr_processor import PDFOCRProcessor

# 创建处理器实例（默认使用RapidOCR）
processor = PDFOCRProcessor()

# 执行PDF OCR识别
result = processor.ocr_pdf('path/to/your/scanned.pdf')

# 获取识别结果
print(f"识别完成，共 {result['page_count']} 页")
print(f"使用引擎: {result['engine']}")
print(result['text'])
```

#### 使用硅基流动API引擎

```python
# 导入OCR处理器
from scripts.pdf_ocr_processor import PDFOCRProcessor

# 创建处理器实例，指定使用硅基流动API
processor = PDFOCRProcessor(engine="siliconflow")

# 执行PDF OCR识别
result = processor.ocr_pdf('path/to/your/scanned.pdf')

# 获取识别结果
print(f"识别完成，共 {result['page_count']} 页")
print(result['text'])
```

#### 识别图片文件

```python
# 导入OCR处理器
from scripts.pdf_ocr_processor import PDFOCRProcessor

# 创建处理器实例
processor = PDFOCRProcessor()  # 或 PDFOCRProcessor(engine="siliconflow")

# 执行图片OCR识别
result = processor.ocr_image_file('path/to/your/image.jpg')

# 获取识别结果
print(f"识别结果: {result['text']}")
```

### 命令行使用

```bash
# 使用默认RapidOCR引擎
python pdf_ocr_processor.py your_document.pdf

# 使用硅基流动API引擎
python pdf_ocr_processor.py your_document.pdf siliconflow
```

### 进阶使用示例

#### 批量处理多个PDF文件

```python
import os
from scripts.pdf_ocr_processor import PDFOCRProcessor

# 创建处理器实例
processor = PDFOCRProcessor()

# 批量处理目录中的所有PDF文件
pdf_dir = "path/to/pdf/files"
output_dir = "path/to/output"
os.makedirs(output_dir, exist_ok=True)

for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}.txt")
        
        print(f"处理文件: {pdf_file}")
        try:
            result = processor.ocr_pdf(pdf_path)
            
            # 保存识别结果到文本文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"=== PDF OCR 识别结果 ===\n")
                f.write(f"文件名: {pdf_file}\n")
                f.write(f"页数: {result['page_count']}\n")
                f.write(f"使用引擎: {result['engine']}\n\n")
                f.write(result['text'])
            
            print(f"处理完成，结果已保存到: {output_path}")
        except Exception as e:
            print(f"处理失败: {e}")
```

#### 混合使用两种引擎

```python
from scripts.pdf_ocr_processor import PDFOCRProcessor

def process_with_best_engine(pdf_path):
    """尝试使用RapidOCR，如果效果不佳则使用硅基流动API"""
    # 首先使用RapidOCR本地引擎
    rapid_processor = PDFOCRProcessor(engine="rapid")
    rapid_result = rapid_processor.ocr_pdf(pdf_path)
    
    # 简单评估识别效果（例如：检查识别出的文本长度）
    text_length = len(rapid_result['text'])
    
    if text_length < 100:  # 如果识别出的文本太短，可能效果不佳
        print("RapidOCR识别效果可能不佳，尝试使用硅基流动API...")
        silicon_processor = PDFOCRProcessor(engine="siliconflow")
        silicon_result = silicon_processor.ocr_pdf(pdf_path)
        return silicon_result
    else:
        return rapid_result

# 使用示例
result = process_with_best_engine('path/to/your/document.pdf')
print(f"识别完成，使用引擎: {result['engine']}")
print(result['text'])
```

### 支持的文件格式

- **PDF文件**: .pdf
- **图片文件**: .jpg, .jpeg, .png, .bmp, .gif, .tiff, .webp

### 输出格式

```python
{
    "text": "识别的完整文本内容",
    "page_count": 页数,  # 图片文件始终为1
    "engine": "rapid" | "siliconflow"  # 使用的OCR引擎
}
```

### 使用场景

- 处理扫描版合同、协议等文档
- 提取影印版书籍、报告中的文字
- 处理无法直接复制文字的PDF文件
- 批量处理扫描版PDF文档
- 识别截图、扫描件等图片中的文字
- 处理手写体或印刷体图片文字识别

### 注意事项

1. **RapidOCR引擎**：
   - 完全免费，无需网络连接
   - 首次使用会自动下载模型文件
   - 识别速度取决于CPU性能

2. **硅基流动API引擎**：
   - 需要有效的API密钥
   - 可能会产生费用
   - 识别速度取决于文件页数、图片大小和网络状况

3. 对于复杂的扫描版PDF或图片，识别准确率可能会有所不同
4. 建议使用高清晰度的扫描版PDF或图片以获得更好的识别效果

### 触发使用不同引擎的提示词

在与 AI IDE 中的助手交互时，您可以使用以下提示词来指定使用不同的 OCR 引擎：

#### 📍 触发 RapidOCR（本地引擎）的提示词
- "使用本地 OCR 引擎处理这个 PDF"
- "用 RapidOCR 识别这个文件"
- "本地处理，不需要 API"
- "快速识别这个文档"
- "离线处理这个 PDF"
- "不使用硅基流动 API，用本地引擎"

#### 📍 触发硅基流动 API（云端引擎）的提示词
- "使用硅基流动 API 处理这个 PDF"
- "用大模型 OCR 识别这个文件"
- "高精度识别这个文档"
- "处理复杂的扫描件"
- "用云端 OCR 引擎"
- "使用 AI 大模型识别"

#### 📍 示例对话

**示例 1：使用本地引擎**
```
用户：帮我处理这个扫描版 PDF，用本地 OCR 引擎快速识别
助手：好的，我将使用 RapidOCR 本地引擎为您处理。请提供 PDF 文件路径。
```

**示例 2：使用云端引擎**
```
用户：这个 PDF 包含手写体，需要高精度识别，用硅基流动 API
助手：理解，我将使用硅基流动 API 大模型为您处理。请提供 PDF 文件路径和您的 API 密钥（如果尚未配置）。
```

**示例 3：自动选择**
```
用户：帮我识别这个 PDF，选择最合适的引擎
助手：我将默认使用 RapidOCR 本地引擎为您处理。如果识别效果不理想，我们可以尝试使用硅基流动 API。
```

### 🔧 技术实现

当 AI 助手接收到这些提示词时，会：

1. 解析用户意图，确定要使用的引擎
2. 调用 PDFOCRProcessor(engine="rapid") 或 PDFOCRProcessor(engine="siliconflow")
3. 执行 OCR 识别并返回结果

### 🎯 最佳实践

- **明确指定引擎**：如果您对引擎有特定要求，最好在提示词中明确说明
- **提供上下文**：说明文档类型（如手写体、复杂格式等）有助于助手选择合适的引擎
- **测试不同引擎**：对于重要文档，可以尝试两种引擎并比较结果

通过使用这些提示词，您可以在与 AI IDE 交互时灵活控制 OCR 引擎的选择，获得最佳的识别效果

### 故障排除

#### 常见问题及解决方案

1. **RapidOCR初始化失败**
   - 问题：`ModuleNotFoundError: No module named 'rapidocr_onnxruntime'`
   - 解决方案：安装RapidOCR依赖：`pip install rapidocr_onnxruntime`

2. **硅基流动API 401错误**
   - 问题：`Unauthorized: 401 Client Error`
   - 解决方案：检查API密钥是否正确配置在`.env`文件中

3. **PDF转图片失败**
   - 问题：`ImportError: No module named 'fitz'`
   - 解决方案：安装PyMuPDF依赖：`pip install pymupdf`

4. **识别结果为空**
   - 问题：识别结果文本长度为0
   - 解决方案：
     - 检查PDF是否为扫描版（非文本PDF）
     - 尝试使用硅基流动API引擎
     - 确保PDF或图片清晰可读

## English Version

### PDF OCR Skill

PDF OCR Skill is used to extract text content from scanned PDF files and image files. This skill supports two OCR engines:
- **RapidOCR** (local engine): No API key required, free to use, fast recognition speed
- **SiliconFlow Large Model** (cloud engine): Uses AI large model for high-precision OCR recognition

### Features

- Support text extraction from scanned PDF files
- Support text recognition from multiple image formats (JPG, PNG, BMP, GIF, TIFF, WEBP)
- **Dual-engine support**: RapidOCR (local) and SiliconFlow API (cloud)
- Support Chinese and English text recognition
- Maintain text order and structure
- Automatically convert PDF pages to images for recognition
- Intelligent engine switching: automatically switch to SiliconFlow API when RapidOCR initialization fails

### Installation

#### Dependencies

```bash
pip install pymupdf pillow requests python-dotenv
```

#### Optional Dependencies (Recommended)

Install RapidOCR for local recognition capability:

```bash
pip install rapidocr_onnxruntime
```

### Environment Configuration

1. Copy `.env.example` file and rename it to `.env`
2. Configure the following options as needed:

```env
# OCR engine selection
# - "rapid": Use RapidOCR local engine (default, no API key required)
# - "siliconflow": Use SiliconFlow API engine (API key required)
OCR_ENGINE=rapid

# If using SiliconFlow API engine, configure the following options:
SILICON_FLOW_API_KEY=your_api_key_here
SILICON_FLOW_OCR_MODEL=deepseek-ai/DeepSeek-OCR
```

### Quick Start

#### Using Default Engine (RapidOCR Local Recognition)

```python
# Import OCR processor
from scripts.pdf_ocr_processor import PDFOCRProcessor

# Create processor instance (default uses RapidOCR)
processor = PDFOCRProcessor()

# Perform PDF OCR recognition
result = processor.ocr_pdf('path/to/your/scanned.pdf')

# Get recognition result
print(f"Recognition completed, total {result['page_count']} pages")
print(f"Engine used: {result['engine']}")
print(result['text'])
```

#### Using SiliconFlow API Engine

```python
# Import OCR processor
from scripts.pdf_ocr_processor import PDFOCRProcessor

# Create processor instance, specify to use SiliconFlow API
processor = PDFOCRProcessor(engine="siliconflow")

# Perform PDF OCR recognition
result = processor.ocr_pdf('path/to/your/scanned.pdf')

# Get recognition result
print(f"Recognition completed, total {result['page_count']} pages")
print(result['text'])
```

#### Recognizing Image Files

```python
# Import OCR processor
from scripts.pdf_ocr_processor import PDFOCRProcessor

# Create processor instance
processor = PDFOCRProcessor()  # or PDFOCRProcessor(engine="siliconflow")

# Perform image OCR recognition
result = processor.ocr_image_file('path/to/your/image.jpg')

# Get recognition result
print(f"Recognition result: {result['text']}")
```

### Command Line Usage

```bash
# Use default RapidOCR engine
python pdf_ocr_processor.py your_document.pdf

# Use SiliconFlow API engine
python pdf_ocr_processor.py your_document.pdf siliconflow
```

### Advanced Usage Examples

#### Batch Processing Multiple PDF Files

```python
import os
from scripts.pdf_ocr_processor import PDFOCRProcessor

# Create processor instance
processor = PDFOCRProcessor()

# Batch process all PDF files in directory
pdf_dir = "path/to/pdf/files"
output_dir = "path/to/output"
os.makedirs(output_dir, exist_ok=True)

for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}.txt")
        
        print(f"Processing file: {pdf_file}")
        try:
            result = processor.ocr_pdf(pdf_path)
            
            # Save recognition result to text file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"=== PDF OCR Recognition Result ===\n")
                f.write(f"File name: {pdf_file}\n")
                f.write(f"Pages: {result['page_count']}\n")
                f.write(f"Engine used: {result['engine']}\n\n")
                f.write(result['text'])
            
            print(f"Processing completed, result saved to: {output_path}")
        except Exception as e:
            print(f"Processing failed: {e}")
```

#### Using Both Engines

```python
from scripts.pdf_ocr_processor import PDFOCRProcessor

def process_with_best_engine(pdf_path):
    """Try using RapidOCR, if not good enough then use SiliconFlow API"""
    # First use RapidOCR local engine
    rapid_processor = PDFOCRProcessor(engine="rapid")
    rapid_result = rapid_processor.ocr_pdf(pdf_path)
    
    # Simple evaluation of recognition effect (e.g., check recognized text length)
    text_length = len(rapid_result['text'])
    
    if text_length < 100:  # If recognized text is too short, may not be good enough
        print("RapidOCR recognition effect may not be good enough, trying SiliconFlow API...")
        silicon_processor = PDFOCRProcessor(engine="siliconflow")
        silicon_result = silicon_processor.ocr_pdf(pdf_path)
        return silicon_result
    else:
        return rapid_result

# Usage example
result = process_with_best_engine('path/to/your/document.pdf')
print(f"Recognition completed, engine used: {result['engine']}")
print(result['text'])
```

### Supported File Formats

- **PDF files**: .pdf
- **Image files**: .jpg, .jpeg, .png, .bmp, .gif, .tiff, .webp

### Output Format

```python
{
    "text": "Recognized full text content",
    "page_count": number_of_pages,  # Always 1 for image files
    "engine": "rapid" | "siliconflow"  # OCR engine used
}
```

### Use Cases

- Processing scanned contracts, agreements and other documents
- Extracting text from photocopied books and reports
- Processing PDF files with non-copyable text
- Batch processing scanned PDF documents
- Recognizing text in screenshots and scanned images
- Processing handwritten or printed text in images

### Notes

1. **RapidOCR Engine**:
   - Completely free, no network connection required
   - Model files will be automatically downloaded on first use
   - Recognition speed depends on CPU performance

2. **SiliconFlow API Engine**:
   - Requires a valid API key
   - May incur costs
   - Recognition speed depends on number of pages, image size, and network conditions

3. Recognition accuracy may vary for complex scanned PDFs or images
4. It is recommended to use high-resolution scanned PDFs or images for better recognition results

### Prompt Words for Different Engines

When interacting with assistants in AI IDEs, you can use the following prompt words to specify different OCR engines:

#### 📍 Prompt Words for RapidOCR (Local Engine)
- "Use local OCR engine to process this PDF"
- "Recognize this file with RapidOCR"
- "Local processing, no API needed"
- "Quickly recognize this document"
- "Process this PDF offline"
- "Don't use SiliconFlow API, use local engine"

#### 📍 Prompt Words for SiliconFlow API (Cloud Engine)
- "Use SiliconFlow API to process this PDF"
- "Recognize this file with large model OCR"
- "High-precision recognition for this document"
- "Process complex scanned documents"
- "Use cloud OCR engine"
- "Use AI large model for recognition"

#### 📍 Example Conversations

**Example 1: Using Local Engine**
```
User: Help me process this scanned PDF, use local OCR engine for quick recognition
Assistant: Sure, I'll use the RapidOCR local engine for you. Please provide the PDF file path.
```

**Example 2: Using Cloud Engine**
```
User: This PDF contains handwritten text, need high-precision recognition, use SiliconFlow API
Assistant: Understood, I'll use the SiliconFlow API large model for you. Please provide the PDF file path and your API key (if not already configured).
```

**Example 3: Automatic Selection**
```
User: Help me recognize this PDF, choose the most suitable engine
Assistant: I'll default to using the RapidOCR local engine for you. If the recognition effect is not ideal, we can try using SiliconFlow API.
```

### 🔧 Technical Implementation

When the AI assistant receives these prompt words, it will:

1. Parse the user's intent to determine the engine to use
2. Call PDFOCRProcessor(engine="rapid") or PDFOCRProcessor(engine="siliconflow")
3. Execute OCR recognition and return the result

### 🎯 Best Practices

- **Clearly specify the engine**: If you have specific requirements for the engine, it's best to clearly state it in the prompt
- **Provide context**: Explaining the document type (e.g., handwritten, complex format) helps the assistant choose the appropriate engine
- **Test different engines**: For important documents, you can try both engines and compare the results

By using these prompt words, you can flexibly control the OCR engine selection when interacting with AI IDEs to get the best recognition results

### Troubleshooting

#### Common Issues and Solutions

1. **RapidOCR Initialization Failure**
   - Issue: `ModuleNotFoundError: No module named 'rapidocr_onnxruntime'`
   - Solution: Install RapidOCR dependency: `pip install rapidocr_onnxruntime`

2. **SiliconFlow API 401 Error**
   - Issue: `Unauthorized: 401 Client Error`
   - Solution: Check if the API key is correctly configured in the `.env` file

3. **PDF to Image Conversion Failure**
   - Issue: `ImportError: No module named 'fitz'`
   - Solution: Install PyMuPDF dependency: `pip install pymupdf`

4. **Empty Recognition Result**
   - Issue: Recognition result text length is 0
   - Solution:
     - Check if the PDF is a scanned version (non-text PDF)
     - Try using SiliconFlow API engine
     - Ensure the PDF or image is clear and readable

## License

MIT License - See [LICENSE.txt](LICENSE.txt)
