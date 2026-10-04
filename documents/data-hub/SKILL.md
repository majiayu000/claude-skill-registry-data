---
name: "data-hub"
description: "5 document and data format skills for Claude Code: read, write, and manipulate DOCX, PDF, PPTX, XLSX files, and perform financial analysis."
version: 1.0.0
author: walva
license: MIT
tags:
  - documents
  - data
  - office
  - finance
  - pdf
agents:
  - claude-code
---

# Data Hub

5 skills for working with documents, spreadsheets, presentations, and financial data.

## Skills

| Skill | Purpose |
|-------|---------|
| docx | Read and write Microsoft Word documents |
| pdf | Parse, extract, and generate PDF files |
| pptx | Create and modify PowerPoint presentations |
| xlsx | Read, write, and analyze Excel spreadsheets |
| finance | Financial analysis: DCF valuation, SaaS metrics, budgeting, forecasting |

## Usage

To load a specific skill, read its SKILL.md:
```
/read _DATA_HUB/pdf/SKILL.md
/read _DATA_HUB/xlsx/SKILL.md
/read _DATA_HUB/finance/SKILL.md
```
