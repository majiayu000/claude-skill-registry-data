---
name: questpdf
description: QuestPDF report generation with fluent C# API. Use when generating PDF documents, designing report layouts, creating invoices/data tables, implementing page structures with headers/footers, or building reusable document components.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(dotnet:*), WebFetch
---

# QuestPDF Report Generation

## Overview

QuestPDF is a modern C# library for PDF document generation with a dedicated layout engine optimized for PDF creation. It uses a component-based, fluent API architecture where simple elements are composed into sophisticated documents.

### Key Benefits

| Feature | Description |
|---------|-------------|
| **Native C# API** | No HTML-to-PDF conversion - direct PDF generation |
| **Component-Based** | Reusable IComponent pattern for modular documents |
| **Automatic Pagination** | Content flows naturally across pages |
| **Type-Safe** | Compile-time checked document structure |
| **Fluent API** | Intuitive chaining syntax for layout definition |

## Installation

```bash
dotnet add package QuestPDF
```

**License:** Free for individuals, non-profits, and businesses < $1M annual revenue.

## Quick Start

```csharp
using QuestPDF.Fluent;
using QuestPDF.Infrastructure;
using QuestPDF.Helpers;

Document.Create(container =>
{
    container.Page(page =>
    {
        page.Size(PageSizes.A4);
        page.Margin(50);

        page.Header().Text("My Report").FontSize(24).Bold();

        page.Content().Column(column =>
        {
            column.Spacing(10);
            column.Item().Text("Hello, QuestPDF!");
            column.Item().Text($"Generated: {DateTime.Now:g}");
        });

        page.Footer().AlignCenter().Text(text =>
        {
            text.Span("Page ");
            text.CurrentPageNumber();
            text.Span(" of ");
            text.TotalPages();
        });
    });
}).GeneratePdf("report.pdf");
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Constraint conflicts | Ensure parent containers provide sufficient space for width/height constraints |
| Header/Footer height | Combined header + footer must leave space for content |
| Image loading | Load images once and reuse for performance |
| Text overflow | Use `.ClampLines()` or ensure adequate width |
| DateTime metadata | Use `DateTimeOffset.Now` instead of `DateTime.Now` |

## Additional Resources

For detailed guidance, see:
- [Document Architecture](document-architecture.md) - IDocument pattern, models, three-layer architecture
- [Layout Components](layout-components.md) - Column, Row, Table, Inlined, Layers, Decoration
- [Text & Styling](text-styling.md) - Fonts, typography, colors, DefaultTextStyle
- [Tables](tables.md) - Table structure, headers, footers, cell spanning, styling
- [Images & Media](images-media.md) - Loading, scaling, SVG, optimization
- [Page Flow](page-flow.md) - Page breaks, sections, navigation, conditional rendering
- [Report Patterns](report-patterns.md) - Invoices, data tables, reusable components

## API Reference

For complete API documentation, see: https://www.questpdf.com/api-reference/
