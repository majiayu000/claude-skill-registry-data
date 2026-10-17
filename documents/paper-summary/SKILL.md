---
name: "paper-summary"
description: "Extracts text from PDF files and generates structured paper summaries with Key Ideas, Main Contributions, and Experimental Results. Supports direct PDF file processing and integration with OpenClaw."
version: "1.0.1"
---

# paper-summary

## 功能说明
This skill extracts text from PDF files and generates structured paper summaries based on the given PDF content. It provides a comprehensive analysis including Key Ideas, Main Contributions, and Experimental Results using advanced natural language processing.

## 使用方法
@openclaw paper-summary [PDF_FILE_PATH]

### 必选参数
- **PDF_FILE_PATH**: 待处理的PDF文件路径（支持绝对路径和相对路径）

### 示例
@openclaw paper-summary /path/to/research-paper.pdf

## Input Requirements
- 提供有效的PDF文件路径
- 确保PDF文件可访问和可读
- 支持标准学术论文格式的PDF文件

## Output Format
The skill will generate a structured summary in markdown format with the following sections:

```markdown
### Key Ideas
<Concise statement of the paper's core idea in one sentence>

### Main Contribution
<Analysis of the paper's main contributions to its field>

### Experimental Results
<Summary of key experimental results presented in the paper>
```

### 输出示例
```markdown
### Key Ideas
The paper proposes a novel deep learning approach for efficient image classification.

### Main Contribution
This research introduces a new network architecture that reduces computational complexity by 50% while maintaining comparable accuracy.

### Experimental Results
Experimental results on ImageNet dataset show that the proposed method achieves 89.2% top-1 accuracy, outperforming state-of-the-art methods in efficiency metrics.
```

## Implementation Details

### Text Extraction
The skill uses `PyMuPDF==1.26.1` (fitz) library to extract text from PDF files. This library provides efficient text extraction capabilities from PDF documents with excellent performance and quality.

### Summary Generation
The skill uses an embedded structured prompt template that guides the model to focus on three core areas:
1. **Key Ideas** - The heart of the paper in one concise sentence
2. **Main Contribution** - The paper's contributions to its field
3. **Experimental Results** - Key results that support the contributions

### Model Requirements
This skill requires access to a language model that supports:
- Text generation from structured prompts
- Processing of long text inputs (up to ~150,000 characters)
- Generation of markdown-formatted output

## Embedded Prompt Template
The skill includes the following embedded prompt template:
```
You are an Artificial Intelligence Assistant, and you are better at conversations in Chinese and English. You will provide users with safe, helpful and accurate answers. At the same time, you will reject all answers to questions that involve terrorism, racism, yellow violence, etc.
Your task is to perform an in-depth analysis of the provided as following, focusing on the following three core areas: Key Ideas, Main Contribution, and Experimental Results. Please read the document carefully and provide a concise and in-depth analysis.
{{ paper_text }}

Key Ideas:
The key idea should be the heart of an essay, and it should be clear in one sentence. Describe the core concept of the article in one concise sentence, no more than 20 words.
Main Contribution:
Analyse and clearly articulate the main contribution of this research to its field. This may include new methodologies, theoretical breakthroughs, technological innovations, or new insights into existing problems. Explain how these contributions have advanced the field and the potential impact they may have. Assess the originality and significance of these contributions.
Experimental Results:
Summarise the key experimental results presented in the document. Focus on results that directly support the main contribution or validate key ideas. Include a brief description of the experimental setup (if critical to understanding the results) and how these results support the author's argument or hypothesis. If there are any particularly significant or unexpected findings, point them out specifically.
Keep the following points in mind in your analysis:
Use language that is accurate and professional but easy to understand.

Remain objective, focus on the content of the document, and avoid adding personal speculation.
If information in a section is incomplete or unclear, explain this in your analysis.
Keep the total word count to 300 words to ensure dense but concise information.
You can answer in Chinese or English, depending on the language of the PDF document provided by the user.
Remember, as an AI assistant, your analyses should always be safe, helpful, and accurate. Your goal is to provide the reader with an overview of the core content of the document, highlighting its most important and innovative aspects, while ensuring that your answers do not contain any inappropriate or harmful content. Now, please begin your analysis.
The returned content must in markdown format, and you must generate in English. You only need to generate key ideas, main contributions and experimental results, and you don't need to generate anything else beyond that.
You must follow the markdown format below:

### Key Ideas
xxxxxxxxxxxxxxxxxxx

### Main Contribution
xxxxxxxxxxxxxxxxxxx

### Experimental Results
xxxxxxxxxxxxxxxxxxx
```

## Dependencies
- `PyMuPDF==1.26.1` for PDF text extraction
- Jinja2 for prompt template processing
- OpenClaw compatible language model

## Limitations
- The skill works best with well-structured research papers
- Results may vary for poorly formatted or scanned PDF documents
- Very long papers (over 150,000 characters) may be truncated
