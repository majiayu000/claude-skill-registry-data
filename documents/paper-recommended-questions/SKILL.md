---
name: "paper-recommended-questions"
description: "Extracts text from PDF files and generates 3 thought-provoking questions that explore the study in depth. Supports direct PDF file processing and integration with OpenClaw."
version: "1.0.1"
---

# paper-recommended-questions

## 功能说明
This skill extracts text from PDF files and generates 3 thought-provoking questions that explore the study in depth. Each question focuses on technical details, applications, comparisons with existing methods, or future directions.

## 使用方法
@openclaw paper-recommended-questions [PDF_FILE_PATH]

### 必选参数
- **PDF_FILE_PATH**: 待处理的PDF文件路径（支持绝对路径和相对路径）

### 示例
@openclaw paper-recommended-questions /path/to/research-paper.pdf

## Input Requirements
- 提供有效的PDF文件路径
- 确保PDF文件可访问和可读
- 支持标准学术论文格式的PDF文件

## Output Format
The skill will generate 3 recommended questions in markdown format:

```markdown
### Recommended Questions
1. [Question 1]
2. [Question 2]
3. [Question 3]
```

### 输出示例
```markdown
### Recommended Questions
1. How does the sparse attention mechanism reduce computational costs compared to GPT-4?
2. Can this method maintain robustness when applied to medical diagnosis scenarios?
3. What hardware limitations must be overcome for real-time deployment on edge devices?
```

## Implementation Details

### Text Extraction
The skill uses `PyMuPDF==1.26.1` (fitz) library to extract text from PDF files. This library provides efficient text extraction capabilities from PDF documents with excellent performance and quality.

### Question Generation
The skill uses an embedded structured prompt template that guides the model to generate exactly 3 questions meeting the following criteria:
1. **Technical relevance** - Focus on technical details, applications, comparisons, or future directions
2. **Word count** - Between 10 and 20 words
3. **Format** - Ends with a question mark (?)
4. **Clarity** - Concise, clear, and logically sound

### Model Requirements
This skill requires access to a language model that supports:
- Text generation from structured prompts
- Processing of long text inputs (up to ~150,000 characters)
- Generation of markdown-formatted output

## Embedded Prompt Template
The skill includes the following embedded prompt template:
```
You are an Artificial Intelligence Assistant. You are fluent in both Chinese and English and always provide answers that are safe, helpful, accurate, and free from any content involving terrorism, racism, pornography, violence, or other harmful topics.

Your task is to perform a thorough analysis of the provided academic content (e.g., research paper excerpt). Based on this analysis, please generate exactly 3 thought-provoking questions that explore the study in depth.

Each question must:

Be related to technical details, applications, comparisons with existing methods, or future directions
Contain between 10 and 20 words
End with a question mark (?)
Be concise, clear, and logically sound
Please output your response using the following Markdown format:

Recommended Questions
1. [Question 1]
2. [Question 2]
3. [Question 3]
Do not include any additional text, explanations, or formatting beyond the list of questions.

Now, begin your analysis based on the following content:

{{ paper_text }}

for example, you can output like this:
### Recommended Questions
1. How does the sparse attention mechanism reduce computational costs compared to GPT-4?
2. Can this method maintain robustness when applied to medical diagnosis scenarios?
3. What hardware limitations must be overcome for real-time deployment on edge devices?
```

## Dependencies
- `PyMuPDF==1.26.1` for PDF text extraction
- Jinja2 for prompt template processing
- OpenClaw compatible language model

## Limitations
- The skill works best with well-structured research papers
- Results may vary for poorly formatted or scanned PDF documents
- Very long papers (over 150,000 characters) may be truncated
