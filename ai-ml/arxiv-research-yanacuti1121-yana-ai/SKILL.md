---
name: arxiv-research
description: "Use when asked to search for academic papers, find related work, look up research on a topic, or retrieve papers from arXiv. Triggers on: 'search papers', 'find papers about', 'arxiv search', 'academic search', 'find related work', 'research papers on', 'literature search', 'find studies on', 'tìm bài báo', 'tìm nghiên cứu', 'tìm paper về', 'tìm tài liệu học thuật'."
---

# arXiv Research Skill
# Source: NousResearch/hermes-agent (MIT) — arXiv API integration pattern adapted for YAMTAM
# Tier: TIER 3 — PRODUCTIVITY

Tìm kiếm bài báo khoa học trên arXiv qua API công khai, không cần API key.
Rate limit: 1 request / 3 giây. XML response → parse thủ công.

## Khi nào dùng

- Tìm paper theo keyword, tác giả, hoặc category (cs.AI, cs.LG, stat.ML...)
- Lấy abstract + BibTeX để cite trong tài liệu
- Kiểm tra related work trước khi implement feature mới
- Tìm sota cho một task cụ thể

**Do NOT use for:** non-arXiv sources (dùng semantic-scholar), full-text PDF parsing (dùng fetch URL trực tiếp).

---

## API Reference

```
Base URL: https://export.arxiv.org/api/query
Format:   Atom XML (parse với grep/sed hoặc python xml.etree)
Auth:     Không cần
Limit:    1 req/3s — KHÔNG flood
```

### Search operators

```
ti:keyword       — tìm trong title
au:AuthorName    — tìm theo tác giả
abs:keyword      — tìm trong abstract
cat:cs.AI        — filter theo category
AND / OR / ANDNOT — boolean operators
```

---

## Pipeline

### Step 1 — Build query URL

```bash
# Tìm paper theo keyword
QUERY="ti:retrieval+augmented+generation+AND+cat:cs.AI"
URL="https://export.arxiv.org/api/query?search_query=${QUERY}&start=0&max_results=5&sortBy=relevance&sortOrder=descending"

# Tìm theo tác giả
QUERY="au:Vaswani+AND+ti:attention"

# Tìm theo category + date range
QUERY="cat:cs.LG+AND+abs:reinforcement+learning"
```

### Step 2 — Fetch results

```bash
# Rate limit: sleep 3 between calls
curl -s "$URL" -o /tmp/arxiv_results.xml
sleep 3  # bắt buộc — rate limit
```

### Step 3 — Parse XML

```python
import xml.etree.ElementTree as ET

tree = ET.parse('/tmp/arxiv_results.xml')
root = tree.getroot()
ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom'
}

results = []
for entry in root.findall('atom:entry', ns):
    arxiv_id = entry.find('atom:id', ns).text.split('/abs/')[-1]
    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
    abstract = entry.find('atom:summary', ns).text.strip()[:300]
    authors = [a.find('atom:name', ns).text
               for a in entry.findall('atom:author', ns)]
    published = entry.find('atom:published', ns).text[:10]

    results.append({
        'id': arxiv_id,
        'title': title,
        'authors': authors[:3],  # first 3 authors
        'published': published,
        'abstract': abstract,
        'url': f'https://arxiv.org/abs/{arxiv_id}',
        'pdf': f'https://arxiv.org/pdf/{arxiv_id}'
    })

for r in results:
    print(f"[{r['id']}] {r['title']}")
    print(f"  Authors: {', '.join(r['authors'])}")
    print(f"  Date: {r['published']}")
    print(f"  URL: {r['url']}")
    print(f"  Abstract: {r['abstract']}...")
    print()
```

### Step 4 — Generate BibTeX (optional)

```python
def to_bibtex(paper):
    first_author_last = paper['authors'][0].split()[-1] if paper['authors'] else 'Unknown'
    year = paper['published'][:4]
    key = f"{first_author_last}{year}{paper['id'].replace('/', '_')}"
    title_words = paper['title'].split()[:3]
    key = f"{first_author_last}{year}{''.join(title_words)}"

    return f"""@article{{{key},
  title = {{{paper['title']}}},
  author = {{{' and '.join(paper['authors'])}}},
  year = {{{year}}},
  journal = {{arXiv preprint arXiv:{paper['id']}}},
  url = {{{paper['url']}}}
}}"""

for r in results:
    print(to_bibtex(r))
```

---

## Common Categories

```
cs.AI   — Artificial Intelligence
cs.LG   — Machine Learning
cs.CL   — Computation and Language (NLP)
cs.CV   — Computer Vision
cs.IR   — Information Retrieval
stat.ML — Statistics / Machine Learning
cs.CR   — Cryptography and Security
cs.SE   — Software Engineering
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu dùng API mà không sleep 3s giữa các request
❌ FAIL nếu parse XML bằng regex thay vì xml.etree
❌ FAIL nếu hiển thị kết quả mà không có arxiv ID (không thể verify)
❌ FAIL nếu search query không encode spaces thành +
✅ PASS khi: kết quả có id + title + authors + URL đầy đủ và verify được trên arxiv.org
```

## See also
- `semantic-scholar` — citation count, references, impact metrics
- `research-analyst` — tổng hợp nhiều paper thành insight
