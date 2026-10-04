---
name: "academic-ref-inserter"
description: "Inserts, formats, and cross-references academic citations in docx. Invoke when user needs to insert references, fix citation order, add cross-reference hyperlinks, or reformat bibliography to Chinese (GB/T 7714) or international (IEEE/APA) standards."
---

# Academic Reference Inserter (学术参考文献插入器)

A comprehensive tool for inserting, formatting, and cross-referencing academic references in Word (.docx) documents. Supports Chinese national standard GB/T 7714-2015 and major international journal formats (IEEE, APA 7th).

---

## 1. When to Invoke

Invoke this skill when the user:
- Says "插入参考文献" / "insert references"
- Says "格式化参考文献" / "format bibliography"
- Says "添加交叉引用" / "add cross-references"
- Says "按GB/T 7714格式化" / "format by GB/T 7714"
- Says "按IEEE/APA格式" / "format in IEEE/APA style"
- Needs to reorder, validate, or fix citation numbering
- Submits a paper and needs reference checking before journal submission

## 2. Supported Citation Formats

| Format | Region | Common In | Ordering | In-text style |
|--------|--------|-----------|----------|---------------|
| **GB/T 7714-2015** | China (中文) | 计算机工程与应用, 自动化学报 | Sequential [1][2][3] | [N] |
| **IEEE** | International | Engineering, CS journals | Sequential [1][2][3] | [N] |
| **APA 7th** | International | Psychology, Education, Business | Alphabetical | (Author, Year) |

## 3. Complete Workflow

### Step 1: Analyze Document

Before making any changes, ALWAYS run the analysis script to understand the current state:

```bash
python scripts/insert_refs.py analyze --input <paper.docx>
```

This will output:
- Total paragraphs
- All in-text citation markers found (in order)
- All bibliography entries found
- Orphan citations (cited but not in bibliography)
- Uncited references (in bibliography but not cited)
- Current ordering analysis

### Step 2: Determine Format

Ask the user which format they need (if not already specified):
- **GB/T 7714-2015** (Chinese standard, 顺序编码制)
- **IEEE** (numbered references)
- **APA 7th** (author-year)
- **Vancouver** (numbered, medical)

If the document already has references, auto-detect the format.

### Step 3: Normalize and Reformat

Run the reformat command:

```bash
# GB/T 7714-2015
python scripts/insert_refs.py reformat --input <paper.docx> --format gbt7714

# IEEE
python scripts/insert_refs.py reformat --input <paper.docx> --format ieee

# APA 7th
python scripts/insert_refs.py reformat --input <paper.docx> --format apa7
```

### Step 4: Reorder References

If the format requires sequential numbering (GB/T 7714, IEEE), reorder references to match first citation order in text:

```bash
python scripts/insert_refs.py reorder --input <paper.docx>
```

### Step 5: Insert Cross-Reference Hyperlinks

Add bookmarks to each bibliography entry and convert all in-text citations to clickable hyperlinks:

```bash
python scripts/insert_refs.py hyperlink --input <paper.docx>
```

### Step 6: Validate

Run comprehensive validation:

```bash
python scripts/insert_refs.py validate --input <paper.docx> --format gbt7714
```

Checks performed:
- All citations have matching bibliography entries
- All bibliography entries are cited in text
- Sequential numbering is correct (no gaps/duplicates)
- Minimum reference count met (default 15)
- Author names formatted correctly
- Document type tags present ([J], [M], [C], etc.)
- Year format valid
- No orphan references

### Step 7: Report

Provide the user with a clear summary of:
- Number of references processed
- Changes made (insertions, renumbering, hyperlinks)
- Any warnings (uncited refs, missing tags, format issues)
- Backup file location

---

## 4. GB/T 7714-2015 Format Rules (中国国家标准)

### Journal Article [J]

```
[序号] 作者. 题名[J]. 刊名, 出版年, 卷(期): 起止页码.
```

**Rules:**
- Authors: `Lastname FirstInitial SecondInitial` (e.g., `Wang Y, Wu H`)
- Chinese authors: Keep Chinese names (e.g., `刘云`) in Chinese journals, use pinyin `Liu Y` in English journals
- 3 authors or fewer: list all; 4+: list first 3 then `, et al.`
- No quotes around title
- Journal name in full (not abbreviated) for Chinese journals
- DOI is optional but encouraged

**Examples:**
```
[1] Wang Y, Wu H, Dong J, et al. TimeXer: Empowering transformers for time series forecasting with exogenous variables[J]. Advances in Neural Information Processing Systems, 2024, 37: 469-498.

[2] 刘云, 胡涛, 张华, 等. 基于深度学习的空气质量预测综述[J]. 计算机工程与应用, 2024, 60(2): 1-15.
```

### Conference Paper [C]

```
[序号] 作者. 题名[C]//会议录名称. 出版地: 出版者, 出版年: 起止页码.
```

**Example:**
```
[3] Zeng A, Chen M, Zhang L, et al. Are transformers effective for time series forecasting?[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2023: 11121-11128.
```

### Book [M]

```
[序号] 作者. 书名[M]. 出版地: 出版者, 出版年.
```

**Example:**
```
[4] Box G E, Jenkins G M, Reinsel G C, et al. Time series analysis: forecasting and control[M]. John Wiley & Sons, 2015.
```

### Dissertation [D]

```
[序号] 作者. 题名[D]. 出版地: 出版单位, 出版年.
```

### Standard [S]

```
[序号] 发布机构. 标准编号 标准名称[S]. 出版地: 出版者, 出版年.
```

### Electronic Resource [EB/OL]

```
[序号] 作者. 题名[EB/OL]. (发布日期)[引用日期]. URL.
```

### Preprint / arXiv

Treat as [J] with journal name `arXiv preprint arXiv:XXXX`:

```
[5] Liu Y, Hu T, Zhang H, et al. iTransformer: Inverted transformers are effective for time series forecasting[J]. arXiv preprint arXiv:2310.06625, 2023.
```

### Type Tags Reference

| Tag | Document Type |
|-----|--------------|
| [J] | Journal article |
| [C] | Conference paper |
| [M] | Monograph (book) |
| [D] | Dissertation |
| [N] | Newspaper |
| [S] | Standard |
| [P] | Patent |
| [R] | Report |
| [EB/OL] | Electronic resource |

### GB/T 7714 Specific Rules

1. **Author names**: Chinese → keep original; English → `Last F M` format
2. **Capitalization**: Chinese → keep original; English → title case for title
3. **Punctuation**: Use `.` between fields, not `;`
4. **Periods**: End each entry with `.`
5. **Ordering**: Sequential by first citation in text

---

## 5. IEEE Format Rules

### Journal Article [J]

```
[1] A. Author, B. Author, and C. Author, "Title of article," Journal Name, vol. X, no. Y, pp. Z1-Z2, Month, Year.
```

**Rules:**
- Authors: `F. Lastname` (initial then last name)
- Use `,` between authors, `and` before last
- Title in double quotes, sentence case
- Journal name in italics
- `vol.`, `no.`, `pp.` abbreviations

### Conference [C]

```
[2] A. Author and B. Author, "Title," in Conference Proceedings, Year, pp. X-Y.
```

### Book [M]

```
[3] A. Author, Book Title, Xth ed. City, State: Publisher, Year.
```

---

## 6. APA 7th Format Rules

### Journal Article [J]

```
Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), page-page. https://doi.org/xxxx
```

**Rules:**
- Authors: `Last, F. M.` format
- Use `&` before last author
- Title in sentence case
- Journal name in italics
- DOI required

### Book [M]

```
Author, A. A. (Year). Title of work: Capital letter also for subtitle. Publisher.
```

---

## 7. Error Handling

### Common Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Missing type tag | `[J]` not found in ref | Auto-detect from source pattern |
| Author name format wrong | Name has incorrect capitalization or order | Normalize to target format |
| No matching citation | Ref in bib but never cited | Either remove ref or add citation with `[TODO: add citation context]` |
| No matching ref | Citation [N] in text but not in bib | Add placeholder ref entry |
| Duplicate citation numbers | Two refs with same number | Renumber sequentially |
| Gaps in numbering | [1], [2], [4] without [3] | Compact to sequential |

### Recovery

If any step fails:
1. Restore from the automatic backup (`_backup_refs.docx`)
2. Report the error to the user
3. Offer manual intervention for complex cases

---

## 8. Output Files

After running the full workflow:

| File | Description |
|------|-------------|
| `paper.docx` (original) | Updated with hyperlinks |
| `paper_backup_refs_YYYYMMDD_HHMMSS.docx` | Timestamped pre-modification backup |
| `paper_analysis.json` | Citation analysis report |

---

## 9. Validation Checklist

Before reporting completion, verify ALL of:

- [ ] Reference count ≥ 15 (for journal papers)
- [ ] ≥ 50% references from last 5 years
- [ ] All in-text citations have matching bibliography entries
- [ ] All bibliography entries are cited in text
- [ ] Sequential numbering matches citation order (GB/T, IEEE)
- [ ] Each entry has proper type tag [J]/[M]/[C]/[D]
- [ ] Author names formatted correctly for target style
- [ ] Cross-reference hyperlinks work (Ctrl+Click)
- [ ] Backup file created
