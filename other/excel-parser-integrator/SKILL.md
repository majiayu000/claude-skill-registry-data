---
name: excel-parser-integrator
description: Integrate Excel/CSV parsing into your backend application code using SheetJS and csv-parse. Use this skill ONLY when building server-side API endpoints that accept uploaded spreadsheet files and return parsed data — for example, a file upload route that extracts tabular data for charts or database import. Do NOT use for directly reading, editing, or creating .xlsx files locally (use the xlsx skill instead).
_meta_type: sdk
---

# Excel/CSV Parser SDK Integration Guide

## When to Use

This SDK wrapper is designed for backend services to parse uploaded Excel and CSV files, extracting tabular data for visualization chart generation.

**Best suited for:**
- Server-side data parsing after file upload
- Unified processing of Excel (xlsx/xls) and CSV files
- Data extraction and transformation for visualization
- Batch tabular data processing

**Not recommended for:**
- Browser-side parsing (use backend service instead)
- Real-time streaming data processing
- Very large files (>100MB, consider chunking)

## Installation

```bash
# SheetJS - Excel file parsing (install from official CDN)
npm i --save https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz

# csv-parse - CSV file parsing
npm install csv-parse
```

**Note:** The `xlsx` package must be installed from the SheetJS official CDN. The npm public registry version is outdated.

### Copy SDK Wrapper

Read `lib/excel-parser.ts` from this skill and copy it to the project, then use it directly.

## Configuration

This SDK requires no environment variables. It is a pure local file parsing tool.

## Quick Start

### Import and Use

```typescript
import { ExcelParser, createParser, ParsedData } from './lib/excel-parser';

// Create parser instance
const parser = createParser();

// Parse uploaded file Buffer
const result = await parser.parse(fileBuffer, {
  filename: 'data.xlsx',  // Used to determine file type
  sheet: 0,               // Parse first worksheet
  headers: true           // First row as headers
});

console.log(result.headers);  // ['Column1', 'Column2', 'Column3']
console.log(result.rows);     // [{Column1: 'a', Column2: 'b', Column3: 'c'}, ...]
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/excel.service.ts
import { createParser, ParsedData, ParseOptions } from '../lib/excel-parser';

export class ExcelService {
  private parser = createParser();

  /**
   * Parse uploaded file
   * Auto-detects xlsx/xls/csv formats
   */
  async parseUploadedFile(
    buffer: Buffer,
    filename: string,
    options?: Partial<ParseOptions>
  ): Promise<ParsedData> {
    return this.parser.parse(buffer, {
      filename,
      headers: true,
      ...options
    });
  }

  /**
   * Get all sheet names in file (Excel only)
   */
  async getSheetNames(buffer: Buffer, filename: string): Promise<string[]> {
    return this.parser.getSheetNames(buffer, filename);
  }

  /**
   * Parse to chart data format
   * Returns data structure compatible with ECharts/Chart.js
   */
  async parseForChart(
    buffer: Buffer,
    filename: string,
    xColumn: string,
    yColumns: string[]
  ): Promise<ChartData> {
    const { headers, rows } = await this.parseUploadedFile(buffer, filename);

    // Validate column names exist
    if (!headers.includes(xColumn)) {
      throw new Error(`X-axis column "${xColumn}" does not exist`);
    }
    for (const col of yColumns) {
      if (!headers.includes(col)) {
        throw new Error(`Y-axis column "${col}" does not exist`);
      }
    }

    return {
      labels: rows.map(row => row[xColumn]),
      datasets: yColumns.map(col => ({
        label: col,
        data: rows.map(row => {
          const val = row[col];
          return typeof val === 'number' ? val : parseFloat(val) || 0;
        })
      }))
    };
  }
}

interface ChartData {
  labels: (string | number)[];
  datasets: Array<{
    label: string;
    data: number[];
  }>;
}
```

### API Route Integration Example

```typescript
// src/routes/upload.ts
import { Router } from 'express';
import multer from 'multer';
import { ExcelService } from '../services/excel.service';

const router = Router();
const upload = multer({ 
  storage: multer.memoryStorage(),
  limits: { fileSize: 50 * 1024 * 1024 } // 50MB
});

const excelService = new ExcelService();

// Upload and parse file
router.post('/parse', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'Please upload a file' });
    }

    const { originalname, buffer } = req.file;
    const result = await excelService.parseUploadedFile(buffer, originalname);

    res.json({
      success: true,
      data: {
        headers: result.headers,
        rows: result.rows,
        rowCount: result.rows.length
      }
    });
  } catch (error) {
    res.status(400).json({ 
      error: error instanceof Error ? error.message : 'Parse failed' 
    });
  }
});

// Get chart data
router.post('/chart-data', upload.single('file'), async (req, res) => {
  try {
    const { xColumn, yColumns } = req.body;
    const { originalname, buffer } = req.file!;

    const chartData = await excelService.parseForChart(
      buffer,
      originalname,
      xColumn,
      JSON.parse(yColumns)
    );

    res.json({ success: true, data: chartData });
  } catch (error) {
    res.status(400).json({ 
      error: error instanceof Error ? error.message : 'Parse failed' 
    });
  }
});

export default router;
```

## Supported File Formats

| Format | Extension | Parser Library |
|--------|-----------|----------------|
| Excel 2007+ | .xlsx | SheetJS |
| Excel 97-2003 | .xls | SheetJS |
| CSV | .csv | csv-parse |
| TSV | .tsv | csv-parse |

## Security Best Practices

1. **File size limits**: Set multer's `limits.fileSize`
2. **File type validation**: Check extension and MIME type
3. **Memory management**: Consider streaming for large files
4. **Error handling**: Catch parsing exceptions, return friendly errors

## Troubleshooting

### Character Encoding Issues
- Ensure CSV files use UTF-8 encoding
- Excel files typically contain encoding info, no special handling needed

### Date Format Issues
- SheetJS converts dates to numbers by default, use `cellDates: true` option to generate Date objects
- Dates in CSV are strings, require manual parsing

### Empty Rows/Columns
- Use `skipEmptyRows: true` to skip empty rows
- For CSV use `skip_empty_lines: true`

## Support and Resources

- **SDK Wrapper**: `lib/excel-parser.ts`
- **SheetJS Docs**: https://docs.sheetjs.com
- **csv-parse Docs**: https://csv.js.org/parse

## Version Info

- **Wrapper Version**: 1.0.0
- **SheetJS**: xlsx@0.20.3
- **csv-parse**: latest
- **Node.js**: >=18.0.0
- **TypeScript**: ^5.0.0
