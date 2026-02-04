---
name: Knack Exporter
description: Creates shareable and compliant stakeholder reports in multiple formats (PDF, CSV, JSON, Excel, HTML). Supports NCDIT submissions, board presentati...
allowed-tools: Read, Edit
---

# Knack Exporter

## Purpose
Creates shareable and compliant stakeholder reports in multiple formats (PDF, CSV, JSON, Excel, HTML). Supports NCDIT submissions, board presentations, and donor communications.

## Core Functions

### export_pdf
**Purpose**: Generate branded PDF reports for formal submissions

**Parameters**:
- `report` (object, required): Report data structure
- `filename` (string, required): Output filename
- `template` (string, optional): "ncdit_compliance" | "board_summary" | "donor_impact"
- `branding` (boolean, optional): Apply HTI colors/logo (default: true)

**Example**:
```javascript
const pdf = await export_pdf({
  report: await generate_quarterly_report("Q1", "2025"),
  filename: "HTI_Q1_2025_Report.pdf",
  template: "ncdit_compliance",
  branding: true
});
```

**PDF Generation Libraries**:
```javascript
// Option 1: Puppeteer (HTML → PDF)
import puppeteer from 'puppeteer';

async function generate_pdf_from_html(html, filename) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html);
  await page.pdf({
    path: filename,
    format: 'Letter',
    margin: { top: '0.5in', bottom: '0.5in', left: '0.5in', right: '0.5in' },
    printBackground: true
  });
  await browser.close();
}

// Option 2: jsPDF (programmatic)
import jsPDF from 'jspdf';

function generate_pdf_programmatic(data, filename) {
  const doc = new jsPDF();

  // Add HTI branding
  doc.setFontSize(20);
  doc.setTextColor('#0E2240'); // Navy Blue
  doc.text('HUBZone Technology Initiative', 20, 20);

  // Add content
  doc.setFontSize(12);
  doc.text(`Q1 2025 Quarterly Report`, 20, 40);
  doc.text(`Laptops Acquired: ${data.acquired}`, 20, 50);
  doc.text(`Devices Converted: ${data.converted}`, 20, 60);

  doc.save(filename);
}
```

### export_csv
**Purpose**: Export raw data for Excel analysis or data pipelines

**Parameters**:
- `records` (array, required): Array of record objects
- `filename` (string, required): Output filename
- `columns` (array, optional): Which fields to include (default: all)
- `delimiter` (string, optional): "," | ";" | "\t" (default: ",")

**Example**:
```javascript
const csv = await export_csv({
  records: await fetch_all_pages("object_1"),
  filename: "HTI_All_Devices_2025.csv",
  columns: ["id", "serial_number", "donor", "status", "county", "acquisition_date"],
  delimiter: ","
});
```

**Implementation**:
```javascript
import { stringify } from 'csv-stringify/sync';

function export_csv({ records, filename, columns, delimiter = ',' }) {
  const csv_data = stringify(records, {
    header: true,
    columns: columns || Object.keys(records[0]),
    delimiter: delimiter
  });

  fs.writeFileSync(filename, csv_data);
  return { filename, rows: records.length };
}
```

### export_json
**Purpose**: Export structured data for API consumption or archival

**Parameters**:
- `dataset` (object, required): Data to export
- `filename` (string, optional): Save to file (default: return string)
- `pretty` (boolean, optional): Human-readable formatting (default: true)

**Example**:
```javascript
const json = await export_json({
  dataset: {
    metadata: { quarter: "Q1", year: "2025" },
    metrics: await generate_metrics({ fields: ["acquired", "converted"] }),
    records: await fetch_all_pages("object_1")
  },
  filename: "HTI_Q1_2025_Data.json",
  pretty: true
});
```

**Implementation**:
```javascript
function export_json({ dataset, filename, pretty = true }) {
  const json_string = JSON.stringify(dataset, null, pretty ? 2 : 0);

  if (filename) {
    fs.writeFileSync(filename, json_string);
    return { filename, size_kb: (json_string.length / 1024).toFixed(2) };
  }

  return json_string;
}
```

### export_excel
**Purpose**: Generate Excel workbooks with multiple sheets and formatting

**Parameters**:
- `workbook` (object, required): Multi-sheet workbook structure
- `filename` (string, required): Output filename (.xlsx)
- `formatting` (object, optional): Cell styles, colors, formulas

**Example**:
```javascript
const excel = await export_excel({
  workbook: {
    sheets: [
      {
        name: "Summary",
        data: [
          ["Metric", "Value"],
          ["Laptops Acquired", 875],
          ["Devices Converted", 623],
          ["Conversion Rate", "71.2%"]
        ]
      },
      {
        name: "All Devices",
        data: await fetch_all_pages("object_1")
      },
      {
        name: "By County",
        data: await county_breakdown()
      }
    ]
  },
  filename: "HTI_Q1_2025_Workbook.xlsx",
  formatting: {
    header_style: {
      fill: { fgColor: { rgb: "0E2240" } },
      font: { color: { rgb: "FFFFFF" }, bold: true }
    }
  }
});
```

**Implementation**:
```javascript
import ExcelJS from 'exceljs';

async function export_excel({ workbook, filename, formatting }) {
  const wb = new ExcelJS.Workbook();

  workbook.sheets.forEach(sheet_def => {
    const sheet = wb.addWorksheet(sheet_def.name);

    // Add data
    sheet.addRows(sheet_def.data);

    // Apply header formatting
    const header_row = sheet.getRow(1);
    header_row.font = { bold: true, color: { argb: 'FFFFFFFF' } };
    header_row.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'FF0E2240' } // HTI Navy
    };

    // Auto-size columns
    sheet.columns.forEach(column => {
      column.width = 15;
    });
  });

  await wb.xlsx.writeFile(filename);
  return { filename, sheets: workbook.sheets.length };
}
```

### export_html
**Purpose**: Generate HTML reports for emails or web embedding

**Parameters**:
- `report` (object, required): Report data
- `template` (string, required): HTML template name
- `inline_css` (boolean, optional): Embed CSS (for email) (default: true)

**Example**:
```javascript
const html = await export_html({
  report: await generate_quarterly_report("Q1", "2025"),
  template: "donor_impact_email",
  inline_css: true
});

// Send via email
await sendEmail({
  to: "major_donors@list.com",
  subject: "HTI Q1 2025 Impact Report",
  html: html
});
```

**Template Example**:
```javascript
function render_donor_impact_email(data) {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body { font-family: Arial, sans-serif; color: #0E2240; }
        .header { background: #0E2240; color: white; padding: 20px; }
        .metric { font-size: 48px; color: #6FC3DF; font-weight: bold; }
        .label { font-size: 14px; color: #666; }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Your Impact This Quarter</h1>
      </div>
      <div style="padding: 20px;">
        <p>Thanks to your generous donation, HTI was able to:</p>

        <div style="text-align: center; margin: 30px 0;">
          <div class="metric">${data.acquired}</div>
          <div class="label">Laptops Acquired</div>
        </div>

        <div style="text-align: center; margin: 30px 0;">
          <div class="metric">${data.converted}</div>
          <div class="label">Chromebooks Created</div>
        </div>

        <div style="text-align: center; margin: 30px 0;">
          <div class="metric">${data.train_hours}</div>
          <div class="label">Training Hours Delivered</div>
        </div>

        <p><strong>Every device makes a difference.</strong> Thank you for being part of HTI's mission to bridge the digital divide.</p>
      </div>
    </body>
    </html>
  `;
}
```

## Report Templates

### NCDIT Compliance Template (PDF)
```javascript
const ncdit_template = {
  sections: [
    {
      title: "Grant Information",
      fields: ["grant_id", "organization", "reporting_period"]
    },
    {
      title: "Device Acquisition & Conversion",
      fields: ["acquired", "converted", "conversion_rate"],
      chart: "acquisition_trend"
    },
    {
      title: "Geographic Distribution",
      fields: ["counties_served", "county_breakdown"],
      chart: "county_bar_chart"
    },
    {
      title: "Training & Education",
      fields: ["train_hours", "participants", "sessions"]
    },
    {
      title: "Progress Toward Goals",
      fields: ["goal_comparison"],
      chart: "progress_bars"
    }
  ],
  branding: {
    header_color: "#0E2240",
    accent_color: "#6FC3DF",
    logo: "hti_logo.png",
    footer: "HUBZone Technology Initiative | NCDIT Digital Champion Grantee"
  }
};
```

### Board Summary Template (PDF)
```javascript
const board_template = {
  sections: [
    { title: "Executive Summary", type: "text" },
    { title: "Key Metrics", type: "kpi_grid" },
    { title: "Operational Highlights", type: "bullet_list" },
    { title: "Financial Summary", type: "table" },
    { title: "Challenges & Risks", type: "callout" },
    { title: "Next Quarter Priorities", type: "numbered_list" }
  ],
  branding: {
    full_hti_branding: true,
    page_numbers: true,
    confidential_watermark: false
  }
};
```

### Donor Impact Template (HTML Email)
```javascript
const donor_email_template = {
  layout: "single_column",
  sections: [
    { type: "hero_image", content: "devices_in_action.jpg" },
    { type: "thank_you_message", tone: "warm" },
    { type: "impact_metrics", style: "large_numbers" },
    { type: "success_story", format: "quote" },
    { type: "call_to_action", button: "View Full Report" }
  ],
  branding: {
    colors: ["#0E2240", "#6FC3DF"],
    inline_css: true, // For email clients
    mobile_responsive: true
  }
};
```

## Multi-Format Export

### Generate All Formats
```javascript
async function export_all_formats(quarter, year) {
  const report_data = await generate_quarterly_report(quarter, year);

  return {
    pdf: await export_pdf({
      report: report_data,
      filename: `HTI_${quarter}_${year}_Report.pdf`,
      template: "ncdit_compliance"
    }),

    excel: await export_excel({
      workbook: {
        sheets: [
          { name: "Summary", data: report_data.metrics },
          { name: "Devices", data: report_data.devices },
          { name: "Training", data: report_data.training }
        ]
      },
      filename: `HTI_${quarter}_${year}_Data.xlsx`
    }),

    csv: await export_csv({
      records: report_data.devices,
      filename: `HTI_${quarter}_${year}_Devices.csv`
    }),

    json: await export_json({
      dataset: report_data,
      filename: `HTI_${quarter}_${year}_Full.json`
    })
  };
}
```

## Cloud Storage Integration

### Upload to Vercel Blob Storage
```javascript
import { put } from '@vercel/blob';

async function export_and_upload(report, filename) {
  const pdf_buffer = await generate_pdf_buffer(report);

  const blob = await put(filename, pdf_buffer, {
    access: 'public',
    contentType: 'application/pdf'
  });

  return {
    url: blob.url,
    filename: filename,
    size: blob.size
  };
}
```

### Upload to S3
```javascript
import AWS from 'aws-sdk';

const s3 = new AWS.S3();

async function export_to_s3(report, filename) {
  const pdf_buffer = await generate_pdf_buffer(report);

  await s3.putObject({
    Bucket: 'hti-reports',
    Key: `quarterly/${filename}`,
    Body: pdf_buffer,
    ContentType: 'application/pdf',
    ACL: 'private'
  }).promise();

  const signed_url = s3.getSignedUrl('getObject', {
    Bucket: 'hti-reports',
    Key: `quarterly/${filename}`,
    Expires: 604800 // 7 days
  });

  return { url: signed_url };
}
```

## Automated Export Workflows

### Quarterly Report Auto-Export
```javascript
// Generate and distribute quarterly reports automatically
cron.schedule('0 8 5 1,4,7,10 *', async () => {
  const quarter = getCurrentQuarter();
  const year = getCurrentYear();

  // Generate all formats
  const exports = await export_all_formats(quarter, year);

  // Upload to cloud storage
  const pdf_url = await export_and_upload(exports.pdf, exports.pdf.filename);

  // Notify stakeholders
  await sendEmail({
    to: "board@hubzonetech.org",
    subject: `${quarter} ${year} Quarterly Report Available`,
    body: `Download: ${pdf_url.url}`
  });

  await sendEmail({
    to: "ncdit-reporting@nc.gov",
    subject: `HTI ${quarter} ${year} Grant Report`,
    body: `Attached quarterly report for review.`,
    attachments: [exports.pdf.filename]
  });
});
```

## Integration Points

- **knack_reporting_sync**: Generate report data for export
- **knack_dashboard_ai**: Render charts and visualizations
- **knack_data_cleaner**: Ensure data quality before export
- **knack_goal_tracker**: Include progress metrics
- **knack_cache_optimizer**: Cache generated reports

## Best Practices

1. **Version exports**: Include timestamp in filename
2. **Test all formats**: Verify output before distribution
3. **Compress large files**: Zip multi-file exports
4. **Secure sensitive data**: Use signed URLs, not public links
5. **Archive exports**: Retain copies of all official reports

## Grant Compliance

### NCDIT Submission Requirements
- PDF for official record
- Excel for data validation
- All files <25MB (portal limit)
- Naming convention: `HTI_Q#_YYYY_Type.ext`
- Retention: 5 years post-grant completion
