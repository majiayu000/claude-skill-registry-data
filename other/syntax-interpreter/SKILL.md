---
name: syntax-interpreter
description: Performs paragraph-by-paragraph translation and deep linguistic analysis. Explains English syntax, grammar, and sentence structure in Chinese. References assets from the raw source directory.
---

# Syntax Interpreter

The core linguistic engine for bilingual analysis.

## Core Workflow
1. **Paragraph Processing**: 
   - Provide the **Original English Text**.
   - Provide the **Chinese Translation** (accurate and idiomatic).
   - Do NOT use labels like "English:" or "中文:".
2. **Deep Linguistic Analysis (深度解析)**:
   - **词汇**: 重点单词的中文定义、词性及英文例句。
   - **短语**: 核心短语/固定搭配的含义及用法。
   - **语法**: 涉及的时态、从句、非谓语动词等语法点。
   - **语态**: 主动语态或被动语态的运用及其作用。
   - **句法**: 倒装、省略、强调等句法手段的分析。
   - **句子结构与组成成分**: 拆解主谓宾、定状补等核心成分，分析长难句的逻辑层次。
3. **Cross-Reference**:
   - Save the output to `wiki/synthesis/article/[Category]/[Article_Title]/index.md`.
   - Reference assets using relative paths: `../../../../../raw/article/[Category]/[Article_Title]/assets/`.

## Guidelines
- All analysis must be in Chinese.
- Every paragraph must address all 6 points if applicable; if a point is not prominent, briefly state its role.
- Focus on representative or challenging sentence structures.
- Ensure the reference to raw assets is correct and functional.
