---
name: excel-report
description: Create an auditable Markdown report for any uploaded Microsoft Excel (.xlsx) or CSV files in an Openrind Shell sandbox.
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Bash, Glob, Write
argument-hint: [optional: path to .xlsx or .csv file(s)]
---

# Excel & CSV Reporting

**CRITICAL INSTRUCTION FOR CLAUDE**:
- This skill does **NOT** spawn background processes or background task IDs. There is **NO** task ID (never call `Task Output` or wait for `skill_run`).
- You (Claude) must directly and immediately execute the `Bash` command in Step 2 to generate the parsed data and then write the final report.
- Never claim data was analyzed until the parsing command succeeds.

## Core Rules

- **Zero External Dependencies**: Standard `python3` (built-in `zipfile`, `xml.etree.ElementTree`, `csv`, `math`, `statistics`, `json`, `datetime`) is used directly.
- **Never probe or search for tools**: Do NOT execute `which libreoffice`, `which csvkit`, `which unzip`, or `apt list`.
- **Never run network package installs**: Do NOT run `pip install`, `uv pip install`, or attempt downloading external packages. The built-in Python script parses `.xlsx` OpenXML and `.csv` natively, offline, and in milliseconds.
- **Bounded input**: Reject files over 10 MiB, ZIP expansion over 32 MiB, members over 8 MiB, more than 128 members, 10,000 rows, 256 columns, or 250,000 dense cells per sheet. Do not retry rejected files without splitting them first.
- **Privacy & Security Gate**: Strictly prohibit exposing secrets, credentials (tokens, passwords, API keys, private keys, database URLs), and unnecessary personal data (PII, SSNs, credit card numbers). Redact sensitive columns and values (`[REDACTED]`). Row-level samples must be redacted, and do not dump raw row-level data or full reports in chat when row-level or sensitive records are present.

## Step 1: Locate Target Files

Determine the inbox directory and find the target file(s):

```bash
if mountpoint -q /sandbox/work 2>/dev/null; then
  INBOX=/sandbox/work/inbox
elif [ -d "/sandbox/inbox" ]; then
  INBOX=/sandbox/inbox
else
  INBOX="."
fi
mkdir -p "$INBOX"
```

If specific file path(s) were given in the user prompt or skill argument, use those.
Otherwise, discover all workbooks dynamically:

```bash
find "$INBOX" /sandbox . -maxdepth 3 -type f \( -iname '*.xlsx' -o -iname '*.csv' \) 2>/dev/null | sort -u
```

## Step 2: Run The Self-Contained Parser

Create `/tmp/openrind-excel-parse.py` and run it against the target file(s) with `python3`:

```bash
cat << 'EOF' > /tmp/openrind-excel-parse.py
import sys, os, zipfile, csv, json, re, math, statistics, datetime, io
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import Counter

MAX_FILE = 10 * 1024 * 1024
MAX_ROWS, MAX_COLS, MAX_CELLS = 10000, 256, 250000
csv.field_size_limit(65536)

def check_file(path):
    if Path(path).stat().st_size > MAX_FILE:
        raise ValueError('Input exceeds the 10 MiB safety limit')

def check_shape(rows, cols):
    if rows > MAX_ROWS or cols > MAX_COLS or rows * cols > MAX_CELLS:
        raise ValueError('Sheet exceeds safe row, column, or cell limits')

def col_letter_to_index(col_str):
    idx = 0
    for char in col_str.upper():
        if 'A' <= char <= 'Z':
            idx = idx * 26 + (ord(char) - ord('A') + 1)
    return idx - 1

def index_to_col_letter(idx):
    res = []
    idx += 1
    while idx > 0:
        idx, rem = divmod(idx - 1, 26)
        res.append(chr(ord('A') + rem))
    return ''.join(reversed(res))

def parse_cell_ref(cell_ref):
    m = re.match(r'([A-Za-z]+)([0-9]+)', cell_ref)
    if m:
        return col_letter_to_index(m.group(1)), int(m.group(2))
    return None, None

def is_date_format_code(code):
    if not code:
        return False
    cleaned = re.sub(r'"[^"]*"', '', code)
    cleaned = re.sub(r'\[(?!\s*[hmsHMS]\s*\])[^\]]*\]', '', cleaned)
    cleaned = re.sub(r'\\.', '', cleaned)
    cleaned = re.sub(r'[_\*].', '', cleaned)
    cl = cleaned.lower()
    if re.search(r'[ydhs]|am/pm|a/p', cl):
        return True
    if re.search(r'(^|[^a-z0-9])m+($|[^a-z0-9])', cl):
        return True
    return False

def format_excel_date(serial, is_1904=False):
    if is_1904:
        base = datetime.datetime(1904, 1, 1)
        dt = base + datetime.timedelta(days=serial)
    else:
        base = datetime.datetime(1899, 12, 31) if serial < 60 else datetime.datetime(1899, 12, 30)
        dt = base + datetime.timedelta(days=serial)
    if dt.microsecond >= 500000:
        dt += datetime.timedelta(seconds=1)
    if serial < 1 and not is_1904:
        return dt.strftime('%H:%M:%S')
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
        return dt.strftime('%Y-%m-%d')
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def read_xlsx(file_path):
    check_file(file_path)
    sheets_data = {}
    with zipfile.ZipFile(file_path, 'r') as z:
        members = z.infolist()
        if (len(members) > 128 or sum(m.file_size for m in members) > 32 * 1024 * 1024
                or any(m.file_size > 8 * 1024 * 1024 or m.file_size > max(1, m.compress_size) * 200 for m in members)):
            raise ValueError('Workbook exceeds ZIP expansion safety limits')
        is_1904 = False
        if 'xl/workbook.xml' in z.namelist():
            wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
            wb_pr = wb_tree.find('.//{*}workbookPr')
            if wb_pr is not None and wb_pr.get('date1904') in ('1', 'true', 'True'):
                is_1904 = True

        custom_num_fmts = {}
        cell_xfs_num_fmt_ids = []
        if 'xl/styles.xml' in z.namelist():
            styles_tree = ET.fromstring(z.read('xl/styles.xml'))
            for num_fmt in styles_tree.findall('.//{*}numFmt'):
                fmt_id_str = num_fmt.get('numFmtId')
                fmt_code = num_fmt.get('formatCode')
                if fmt_id_str is not None and fmt_code is not None:
                    try:
                        custom_num_fmts[int(fmt_id_str)] = fmt_code
                    except ValueError:
                        pass
            for xf in styles_tree.findall('.//{*}cellXfs/{*}xf'):
                num_fmt_id_str = xf.get('numFmtId', '0')
                try:
                    cell_xfs_num_fmt_ids.append(int(num_fmt_id_str))
                except ValueError:
                    cell_xfs_num_fmt_ids.append(0)

        builtin_date_fmt_ids = {
            14, 15, 16, 17, 18, 19, 20, 21, 22,
            27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
            45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 57, 58
        }
        date_style_indices = set()
        for idx, fmt_id in enumerate(cell_xfs_num_fmt_ids):
            if fmt_id in builtin_date_fmt_ids:
                date_style_indices.add(idx)
            elif fmt_id in custom_num_fmts and is_date_format_code(custom_num_fmts[fmt_id]):
                date_style_indices.add(idx)

        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in tree.findall('.//{*}si'):
                texts = [t.text for t in si.findall('.//{*}t') if t.text is not None]
                shared_strings.append(''.join(texts))

        rel_map = {}
        if 'xl/_rels/workbook.xml.rels' in z.namelist():
            rels_tree = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
            for rel in rels_tree.findall('.//{*}Relationship'):
                r_id = rel.get('Id')
                target = rel.get('Target', '')
                if target.startswith('/'):
                    target = target[1:]
                if not target.startswith('xl/'):
                    target = 'xl/' + target
                rel_map[r_id] = target

        sheets = []
        if 'xl/workbook.xml' in z.namelist():
            wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
            for idx, sheet_el in enumerate(wb_tree.findall('.//{*}sheet')):
                name = sheet_el.get('name') or f'Sheet{idx+1}'
                r_id = (sheet_el.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                        or sheet_el.get('r:id') or sheet_el.get('id'))
                target = rel_map.get(r_id, f'xl/worksheets/sheet{idx+1}.xml')
                sheets.append({'name': name, 'path': target})

        if not sheets:
            for name in z.namelist():
                if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
                    sheets.append({'name': Path(name).stem, 'path': name})

        for s in sheets:
            path = s['path']
            if path not in z.namelist():
                alt = 'xl/' + path if not path.startswith('xl/') else path[3:]
                if alt in z.namelist():
                    path = alt
                else:
                    continue

            ws_tree = ET.fromstring(z.read(path))
            rows_data = []
            max_col = 0

            for row_el in ws_tree.findall('.//{*}row'):
                row_dict = {}
                for c_el in row_el.findall('.//{*}c'):
                    ref = c_el.get('r')
                    t = c_el.get('t', 'n')
                    style_attr = c_el.get('s')
                    style_idx = int(style_attr) if style_attr and style_attr.isdigit() else 0
                    is_date_cell = style_idx in date_style_indices
                    val = None

                    if t == 's':
                        v_el = c_el.find('.//{*}v')
                        if v_el is not None and v_el.text:
                            try:
                                s_idx = int(v_el.text)
                                if s_idx < len(shared_strings):
                                    val = shared_strings[s_idx]
                            except ValueError:
                                val = v_el.text
                    elif t == 'inlineStr':
                        texts = [t_el.text for t_el in c_el.findall('.//{*}t') if t_el.text is not None]
                        val = ''.join(texts) if texts else None
                    elif t == 'b':
                        v_el = c_el.find('.//{*}v')
                        val = (v_el.text == '1') if v_el is not None and v_el.text else False
                    elif t == 'd':
                        v_el = c_el.find('.//{*}v')
                        val = v_el.text if v_el is not None else None
                    elif t in ('str', 'e'):
                        v_el = c_el.find('.//{*}v')
                        val = v_el.text if v_el is not None else None
                    else:
                        v_el = c_el.find('.//{*}v')
                        if v_el is not None and v_el.text:
                            raw = v_el.text
                            try:
                                f_val = float(raw)
                                if is_date_cell:
                                    try:
                                        val = format_excel_date(f_val, is_1904)
                                    except Exception:
                                        val = int(f_val) if f_val.is_integer() else f_val
                                else:
                                    val = int(f_val) if f_val.is_integer() else f_val
                            except ValueError:
                                val = raw

                    col_idx = None
                    if ref:
                        col_idx, _ = parse_cell_ref(ref)
                    if col_idx is not None:
                        check_shape(len(rows_data) + 1, col_idx + 1)
                        row_dict[col_idx] = val
                        if col_idx + 1 > max_col:
                            max_col = col_idx + 1
                rows_data.append(row_dict)
                check_shape(len(rows_data), max_col)

            matrix = []
            for r in rows_data:
                row = [r.get(c, None) for c in range(max_col)]
                matrix.append(row)

            sheets_data[s['name']] = matrix

    return sheets_data

def read_csv(file_path):
    check_file(file_path)
    encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']
    raw_bytes = Path(file_path).read_bytes()
    text = None
    for enc in encodings:
        try:
            text = raw_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        text = raw_bytes.decode('utf-8', errors='replace')
    try:
        dialect = csv.Sniffer().sniff(text[:4096])
        delimiter = dialect.delimiter
    except Exception:
        delimiter = ','
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    matrix = []
    for row in reader:
        check_shape(len(matrix) + 1, len(row))
        converted = []
        for cell in row:
            val = cell.strip()
            converted.append(val if val != '' else None)
        matrix.append(converted)
    return {'CSV Data': matrix}

def is_sensitive_name(name):
    n = str(name).lower()
    patterns = ['password', 'secret', 'token', 'key', 'ssn', 'auth', 'credential', 'credit_card', 'card_number', 'api_key', 'private', 'bearer', 'cvv', 'pin']
    return any(p in n for p in patterns)

def analyze_matrix(matrix):
    if not matrix:
        return {'total_rows': 0, 'total_cols': 0, 'duplicate_rows': 0, 'headers': [], 'sample': [], 'columns': {}}
    raw_headers = [str(c) if c is not None and str(c).strip() != '' else f'Column_{i+1}' for i, c in enumerate(matrix[0])]
    data_rows = matrix[1:]
    total_rows = len(data_rows)
    total_cols = len(raw_headers)
    row_tuples = [tuple(r) for r in data_rows]
    dup_count = len(row_tuples) - len(set(row_tuples)) if total_rows > 0 else 0

    seen_header_counts = {}
    unique_keys = []
    for h in raw_headers:
        if h in seen_header_counts:
            seen_header_counts[h] += 1
            unique_keys.append(f"{h}_{seen_header_counts[h]}")
        else:
            seen_header_counts[h] = 1
            unique_keys.append(h)

    # Default-deny value disclosure: arbitrary notes, identifiers, and numeric
    # account/card values cannot be reliably classified using header names.
    sensitive_cols = set(range(len(raw_headers)))
    redacted_sample = []
    for r in data_rows[:5]:
        redacted_sample.append([('[REDACTED]' if c_idx in sensitive_cols else (r[c_idx] if c_idx < len(r) else None)) for c_idx in range(len(raw_headers))])
    columns_info = {}
    for col_idx, (col_name, col_key) in enumerate(zip(raw_headers, unique_keys)):
        values = [r[col_idx] if col_idx < len(r) else None for r in data_rows]
        non_null_values = [v for v in values if v is not None and v != '']
        null_count = total_rows - len(non_null_values)
        null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0.0
        unique_count = len(set(non_null_values))
        numeric_vals = []
        for v in non_null_values:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                numeric_vals.append(float(v))
            elif isinstance(v, str):
                try:
                    numeric_vals.append(float(v.strip().replace(',', '')))
                except ValueError:
                    pass
        is_numeric = len(numeric_vals) == len(non_null_values) and len(non_null_values) > 0
        col_info = {
            'header': col_name,
            'col_index': col_idx,
            'col_letter': index_to_col_letter(col_idx),
            'dtype': 'numeric' if is_numeric else 'text',
            'missing_count': null_count,
            'missing_pct': round(null_pct, 2),
            'unique_count': unique_count
        }
        if col_idx in sensitive_cols:
            col_info['values_withheld'] = True
        elif is_numeric and numeric_vals:
            numeric_vals.sort()
            n = len(numeric_vals)
            mean_val = statistics.mean(numeric_vals)
            std_val = statistics.stdev(numeric_vals) if n > 1 else 0.0
            def percentile(s, p):
                idx = (len(s) - 1) * p
                l, u = int(math.floor(idx)), int(math.ceil(idx))
                return s[l] if l == u else s[l] * (u - idx) + s[u] * (idx - l)
            q1, q3 = percentile(numeric_vals, 0.25), percentile(numeric_vals, 0.75)
            iqr = q3 - q1
            outliers = [v for v in numeric_vals if v < (q1 - 1.5*iqr) or v > (q3 + 1.5*iqr)]
            col_info['stats'] = {
                'count': n, 'sum': round(sum(numeric_vals), 2), 'mean': round(mean_val, 2), 'std': round(std_val, 2),
                'min': round(numeric_vals[0], 2), 'q1': round(q1, 2), 'median': round(statistics.median(numeric_vals), 2),
                'q3': round(q3, 2), 'max': round(numeric_vals[-1], 2), 'iqr': round(iqr, 2), 'outlier_count': len(outliers)
            }
        else:
            if col_idx in sensitive_cols:
                col_info['top_values'] = [{'value': '[REDACTED]', 'count': len(non_null_values), 'pct': 100.0}]
            else:
                counts = Counter([str(v) for v in non_null_values]).most_common(5)
                col_info['top_values'] = [{'value': k, 'count': c, 'pct': round(c/len(non_null_values)*100, 1) if non_null_values else 0} for k, c in counts]
        columns_info[col_key] = col_info
    return {'total_rows': total_rows, 'total_cols': total_cols, 'duplicate_rows': dup_count, 'headers': raw_headers, 'sample': redacted_sample, 'columns': columns_info}

def process_file(p):
    path = Path(p)
    if not path.exists(): return None
    sfx = path.suffix.lower()
    if sfx in ('.xlsx', '.xlsm', '.xltx'):
        sheets = read_xlsx(path); fmt = 'Excel Workbook'
    elif sfx in ('.csv', '.tsv', '.txt'):
        sheets = read_csv(path); fmt = 'CSV'
    else: return None
    return {'filename': path.name, 'path': str(path.absolute()), 'size_bytes': path.stat().st_size, 'format': fmt, 'sheets': {k: {'stats': analyze_matrix(v)} for k, v in sheets.items()}}

target_files = sys.argv[1:]
results = []
for f in target_files:
    res = process_file(f)
    if res is not None:
        results.append(res)
print(json.dumps(results, indent=2))
EOF
```

Run against the target file(s):

```bash
python3 /tmp/openrind-excel-parse.py "<path_to_file1>" ["<path_to_file2>" ...] > /tmp/parsed-excel.json
```

## Step 3: Write The Report Contract

Read `/tmp/parsed-excel.json` and generate `$INBOX/analysis-report.md` with:

1. **Executive Summary** — concise, factual overview of the files analyzed and critical findings.
2. **Data Scope** — table showing file names, worksheet names, dimensions (rows × columns), and duplicate rows.
3. **Key Metrics And Statistics** — tables with counts, means, medians, std dev, min, max, IQR outliers, and missing counts.
4. **Detailed Findings** — column diagnostics, data distributions, categorical frequencies, and redacted/opt-in data previews.
5. **Data-Quality Risks** — explicit itemization of missing values, duplicate records, and outliers tied to specific workbooks, sheets, and columns.
6. **Next Steps** — actionable recommendations and investigative questions for further analysis.

Tie each finding to a named workbook, sheet, and column. Distinguish observed facts
from inference. Ensure secrets, credentials, and unnecessary personal data are never printed in plaintext; redact sensitive columns and values. After writing the file, tell the user its exact path. Present an executive summary and high-level findings in chat; do not require or dump the full report in chat when it contains row-level data or sensitive details.
