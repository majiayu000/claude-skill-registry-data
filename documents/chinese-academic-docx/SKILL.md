---
name: chinese-academic-docx
description: Fill Chinese academic DOCX templates (课程论文, 毕业论文) with proper formatting. Covers template structure detection, python-docx paragraph replacement, lxml XML insertion for extra content, Chinese font/indent/spacing configuration, JSON bridge pattern for encoding-safe Chinese content, and GB/T 7714-2015 citation format.
---

# Chinese Academic DOCX Template Filling

## When to Use
- User provides a `.docx` template for a Chinese academic paper (课程论文/毕业论文)
- Template has placeholder text like "标题（小二号宋体居中加粗）" or "正文（小四号宋体）"
- Need to fill content while preserving template formatting or adding new paragraphs
- Need GB/T 7714-2015 formatted references

## Workflow

### Phase 1: Extract Template Structure
```bash
python3 -c "
import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile('template.docx') as z:
    z.extractall('/tmp/tpl')
tree = ET.parse('/tmp/tpl/word/document.xml')
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = [t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]
    if texts: print(''.join(texts))
"
```

### Phase 2: Identify Paragraphs by Content
```python
import docx
doc = docx.Document("template.docx")
para_texts = [p.text.strip() for p in doc.paragraphs]

# Match slots by known placeholder text
title_idx = next(i for i,t in enumerate(para_texts) if '小二号' in t)
body_indices = [i for i,t in enumerate(para_texts) if '正文' in t and '小四号' in t]
ref_start = next(i for i,t in enumerate(para_texts) if t.startswith('[1]'))
```

### Phase 3: Write Content as JSON (Avoids Chinese Quote Mangling)
```bash
cat > /tmp/content.json << 'JSONEOF'
{
  "title": "论文标题",
  "body": ["段落1内容...", "段落2内容..."],
  "references": ["[1] 作者. 书名[M]. 出版地: 出版社, 年份."]
}
JSONEOF
```

### Phase 4: Fill Template
```python
import json
with open('/tmp/content.json') as f:
    data = json.load(f)

def set_para_text(para, new_text, bold=None, alignment=None, font_size=None):
    """Replace paragraph text, set 宋体 font, optional formatting."""
    from docx.shared import Pt
    from docx.oxml.ns import qn
    for run in para.runs:
        run.text = ""
    run = para.runs[0] if para.runs else para.add_run("")
    run.text = new_text
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn('w:eastAsia'), "宋体")
    if font_size:
        run.font.size = font_size
    if bold is not None:
        run.bold = bold
    if alignment is not None:
        para.alignment = alignment

# Replace existing paragraphs
set_para_text(paragraphs[title_idx], data['title'], bold=True, alignment=CENTER, font_size=Pt(18))
```

### Phase 5: Insert New Paragraphs (lxml)
When the template has fewer slots than needed, inject XML paragraphs:

```python
from lxml import etree
from docx.oxml.ns import qn

# Find insertion point (e.g., before references label)
ref_para = paragraphs[ref_label_idx]._element
parent = ref_para.getparent()
ref_idx = list(parent).index(ref_para)

for i, text in enumerate(extra_paragraphs):
    new_p = etree.Element(qn('w:p'))
    parent.insert(ref_idx + i, new_p)  # ✅ forward order

    pPr = etree.SubElement(new_p, qn('w:pPr'))
    # 1.5x line spacing
    etree.SubElement(pPr, qn('w:spacing')).set(qn('w:line'), '360')
    etree.SubElement(pPr, qn('w:spacing')).set(qn('w:lineRule'), 'auto')
    # 2-char first-line indent
    etree.SubElement(pPr, qn('w:ind')).set(qn('w:firstLine'), '480')

    r = etree.SubElement(new_p, qn('w:r'))
    rPr = etree.SubElement(r, qn('w:rPr'))
    rf = etree.SubElement(rPr, qn('w:rFonts'))
    rf.set(qn('w:ascii'), '宋体')
    rf.set(qn('w:eastAsia'), '宋体')
    rf.set(qn('w:hAnsi'), '宋体')
    etree.SubElement(rPr, qn('w:sz')).set(qn('w:val'), '24')  # 12pt

    t = etree.SubElement(r, qn('w:t'))
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
```

## ⚠️ Key Pitfall: lxml addprevious() Reverses Order
`element.addprevious(new)` inserts `new` immediately before `element`. In a loop, each subsequent insertion also goes right before `element`, pushing earlier insertions down — resulting in **reversed order**. Always use `parent.insert(ref_idx + i, new_p)` instead.

## ⚠️ Pitfall: Don't Use `para.runs` for Blank Filling

`python-docx`'s `para.runs` order does NOT reliably reflect visual/text order of the paragraph — runs can be nested inside hyperlinks, fields, or split mid-word by Word's XML structure. For filling blanks in templates (especially 任务书/实训报告 with mixed code and Chinese text), use **raw XML parsing** instead:

```python
import zipfile, re
from xml.etree import ElementTree as ET
NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

with zipfile.ZipFile('template.docx') as z:
    root = ET.fromstring(z.read('word/document.xml'))

# Find ALL <w:t> elements with blanks, in TRUE document order
blanks = [t for t in root.iter(f'{{{NS}}}t')
          if t.text and re.search(r'_{3,}', t.text)]

# Replace one blank at a time from an ordered answer list
ans_idx = 0
for t_elem in blanks:
    text = t_elem.text
    n = len(re.findall(r'_{3,}', text))
    for _ in range(n):
        if ans_idx < len(answers) and answers[ans_idx] is not None:
            text = re.sub(r'_{3,}', str(answers[ans_idx]), text, count=1)
        ans_idx += 1
    t_elem.text = text

# Save
output_xml = ET.tostring(root, encoding='unicode')
with zipfile.ZipFile('template.docx') as zin:
    with zipfile.ZipFile('filled.docx', 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            zout.writestr(item, output_xml
                if item.filename == 'word/document.xml'
                else zin.read(item.filename))
```

## ⚠️ Pitfall: 任务书填充习惯 (User-Specific)

以下为当前用户（冯周杰）的填充偏好，每次填任务书/实训报告时必须遵守：

1. **组别不填**：个人信息表格中的「组别」字段始终留空（保持 `__________`），不要填任何数字。
2. **多选一只填选中的**：模板中如有「选择一项完成」的多项目并列（如 Project A/B/C），只填充用户选定的那一个项目，其余项目保留空白 `___`。
3. **问答组必须填满**：模板中有几组 Q&A 槽位就填几组，不要只填一组。每组都必须匹配内容。

## ⚠️ Pitfall: Q: 前缀与空白在不同 Run 中

任务书中的问答槽位常见格式：`Q: ` 在一个 `<w:r>` 中，`________________________` 在另一个 `<w:r>` 中。用 `replace_run_text` 匹配完整字符串 `"Q: ________________________"` 会失败，因为没有一个单独的 run 包含全部文字。

**正确做法**：先打印每个 paragraph 的 run 结构确认边界，然后用 `p.runs[1].text = answer` 直接赋值空白 run：

```python
# 1. 诊断：打印段落 run 结构
for i in [77, 78, 80, 81]:
    p = doc.paragraphs[i]
    for j, r in enumerate(p.runs):
        print(f"  run[{j}]: \"{r.text}\"")
# 输出示例: run[0]: "Q: " / run[1]: "________________________"

# 2. 直接替换空白 run
doc.paragraphs[77].runs[1].text = "如果目标丢失了怎么办？"
doc.paragraphs[78].runs[1].text = "系统切换到 SCANNING 状态..."
```

## ⚠️ Pitfall: Code Dunders Confused with Blanks

When templates contain Python code examples (e.g., `paddle.__version__`, `__name__`), regex `_{2,}` will match the double underscores as blanks, injecting answers into code and breaking the fill. **Always use `_{3,}` (3+ underscores)** to distinguish real fill-in blanks from dunder names.

Before filling, scan the template for this issue:
```python
# Audit: print all <w:t> elements that would be matched
for t in root.iter(f'{{{NS}}}t'):
    if t.text and re.search(r'_{3,}', t.text):
        print(f'  [{t.text[:80]}]')
# Manually count blanks per element, build answers list
```

## Chinese Font Size Table
| 字号 | pt | DOCX half-pts |
|------|-----|---------------|
| 小二号 | 18 | 36 |
| 小四号 | 12 | 24 |
| 五号 | 10.5 | 21 |

## GB/T 7714-2015 Citation Format (Quick Reference)
- **专著 [M]**: `作者. 书名[M]. 出版地: 出版社, 年份[: 页码].`
- **期刊 [J]**: `作者. 题名[J]. 刊名, 年份, 卷(期): 页码.`
- **学位论文 [D]**: `作者. 题名[D]. 出版地: 学校, 年份.`
- **电子资源**: add `[J/OL]` or `[M/OL]`, include URL and DOI if available
- Use 顺序编码制: `[1]` `[2]` in reference list, referenced in text by same numbers

## Chinese Business Document Template

For formal Chinese business/consulting documents (方案, 报告, 规划) with docx-js, see `references/chinese-business-docx-template.md` — proven pattern with cover page, styled headings, tables, headers/footers, and section numbering. Complements the academic template above.

## Chinese PDF Reading Fallback

When `pdftotext` or `pypdf` fail to extract Chinese text from a PDF (common with scanned/image-based PDFs):
```bash
# Convert to JPEG images
pdftoppm -jpeg -r 200 input.pdf /tmp/page_prefix
# Then read each page with mmx vision
mmx vision describe --image /tmp/page_prefix-01.jpg --prompt "逐字描述所有文字..." --output json --quiet
```
Note: `pdftoppm` requires `poppler-utils`. The `-r 200` sets 200 DPI for readability.

## Installation
```bash
# CN network — use Tsinghua mirror
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --python <venv>/bin/python python-docx lxml
```
