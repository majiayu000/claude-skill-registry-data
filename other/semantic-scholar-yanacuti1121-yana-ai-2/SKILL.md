---
name: semantic-scholar
description: "Use when asked about citation counts, paper impact, who cited a paper, research influence, finding references of a paper, author h-index, or publication metrics. Triggers on: 'citation count', 'who cited', 'how many citations', 'paper impact', 'semantic scholar', 'research influence', 'find references', 'author publications', 'h-index', 'số lần trích dẫn', 'tìm tài liệu tham khảo', 'bài báo có ảnh hưởng'."
---

# Semantic Scholar Skill
# Source: NousResearch/hermes-agent (MIT) — Semantic Scholar API pattern adapted for YAMTAM
# Tier: TIER 3 — PRODUCTIVITY

Tra cứu citation, impact, và references của paper khoa học qua Semantic Scholar API.
Rate limit: 1 request/giây không cần API key. Có JSON response, dễ parse hơn arXiv.

## Khi nào dùng

- Kiểm tra citation count của một paper cụ thể
- Tìm tất cả paper cite một công trình nào đó ("who builds on this?")
- Xem references list của một paper
- Tra thông tin tác giả: h-index, top papers, collaboration network
- So sánh impact của nhiều paper

**Do NOT use for:** tìm paper theo keyword (dùng arxiv-research), full-text (dùng arxiv PDF URL trực tiếp).

---

## API Reference

```
Base URL: https://api.semanticscholar.org/graph/v1/
Auth:     Không cần key cho rate ≤ 1 req/s
Headers:  User-Agent: yamtam-research/1.0 (optional nhưng tốt)
Limit:    1 req/s — sleep 1 between calls
```

---

## Pipeline

### Step 1 — Lookup paper by arXiv ID hoặc DOI

```bash
# Từ arXiv ID (e.g., 2303.08774)
ARXIV_ID="2303.08774"
FIELDS="title,authors,year,citationCount,referenceCount,citations,references,abstract"

curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:${ARXIV_ID}?fields=${FIELDS}" \
  -H "User-Agent: yamtam-research/1.0" \
  -o /tmp/s2_paper.json
sleep 1
```

```bash
# Từ DOI
DOI="10.48550/arXiv.2303.08774"
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:${DOI}?fields=${FIELDS}" \
  -o /tmp/s2_paper.json
sleep 1
```

```bash
# Search by title keyword (khi không có ID)
QUERY="attention+is+all+you+need"
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=${QUERY}&fields=title,year,citationCount,authors&limit=5" \
  -o /tmp/s2_search.json
sleep 1
```

### Step 2 — Parse paper info

```python
import json

with open('/tmp/s2_paper.json') as f:
    p = json.load(f)

print(f"Title: {p['title']}")
print(f"Year: {p.get('year', 'N/A')}")
print(f"Citations: {p.get('citationCount', 0)}")
print(f"References: {p.get('referenceCount', 0)}")
print(f"Authors: {', '.join(a['name'] for a in p.get('authors', [])[:5])}")
print(f"Abstract: {(p.get('abstract') or '')[:300]}...")
```

### Step 3 — Get citations (who cited this paper)

```python
# Từ response đã fetch ở Step 1
citations = p.get('citations', [])
print(f"\nTop citations ({len(citations)} total):")
for c in citations[:10]:
    print(f"  [{c.get('year', '?')}] {c['title']} — {c.get('citationCount', 0)} cites")
```

```bash
# Nếu cần paginate citations riêng
PAPER_ID="<semanticscholar_paper_id>"
curl -s "https://api.semanticscholar.org/graph/v1/paper/${PAPER_ID}/citations?fields=title,year,authors,citationCount&limit=20" \
  -o /tmp/s2_citations.json
sleep 1
```

### Step 4 — Author lookup

```bash
# Tìm author ID từ paper
AUTHOR_ID=$(python3 -c "import json; d=json.load(open('/tmp/s2_paper.json')); print(d['authors'][0]['authorId'])")

# Lấy profile tác giả
curl -s "https://api.semanticscholar.org/graph/v1/author/${AUTHOR_ID}?fields=name,hIndex,citationCount,paperCount,papers" \
  -o /tmp/s2_author.json
sleep 1

python3 -c "
import json
a = json.load(open('/tmp/s2_author.json'))
print(f'Name: {a[\"name\"]}')
print(f'h-index: {a.get(\"hIndex\", \"N/A\")}')
print(f'Total citations: {a.get(\"citationCount\", 0)}')
print(f'Papers: {a.get(\"paperCount\", 0)}')
"
```

---

## Output format chuẩn

```markdown
## Paper: [Title]

- **arXiv ID:** 2303.08774
- **Year:** 2023
- **Citations:** 1,247
- **Authors:** Author A, Author B, Author C
- **Abstract:** ...

### Top Citing Papers
| Year | Title | Citations |
|------|-------|-----------|
| 2024 | ...   | 89        |

### Key References
- [2017] Attention Is All You Need — 89,000 citations
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu không sleep 1s giữa các request (rate limit violation)
❌ FAIL nếu citationCount không hiển thị cụ thể (không verify được)
❌ FAIL nếu dùng paper ID từ arXiv mà không prefix "arXiv:" trong URL
❌ FAIL nếu author lookup không có authorId (authorId = required field)
✅ PASS khi: citation count + paper URL + author name đều verify được trên semanticscholar.org
```

## See also
- `arxiv-research` — tìm paper theo keyword/topic
- `research-analyst` — tổng hợp findings từ nhiều paper
