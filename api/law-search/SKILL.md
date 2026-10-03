---
name: law-search
description: Korean law/case search via law.go.kr + data.go.kr APIs. Use for legal questions, statute lookup, court cases, and everyday legal info.
version: 2.1.0
author: chumjibot
created: 2026-02-13
updated: 2026-02-14
tags: [law, legal, korea, openapi, data.go.kr, law.go.kr]
connectors: [~~law, ~~docs, ~~notify]
---

# Law & Case Search Skill

Korea Legislation Research Institute (MOLEG) law search, statute detail, case search.
Inspired by Cowork Legal plugin architecture.

## Overview

| Key | Value |
|-----|-------|
| Provider | MOLEG (Ministry of Government Legislation) |
| API Source | law.go.kr (primary) + data.go.kr (fallback) |
| Auth (law.go.kr) | `~/.config/law-go-kr/credentials.json` → OC code |
| Auth (data.go.kr) | `~/.config/data-go-kr/api_key` |
| Daily limit | 10,000 calls |
| Playbook | `playbook.md` |

## Scripts

```
scripts/
├── law_search.sh   → Search laws by keyword
├── law_detail.sh   → Statute text by law ID
├── case_search.sh  → Court case search
└── life_law.sh     → Everyday legal info search
```

## Workflow

### Step 1: Analyze question
- Extract legal keywords from user question
- Match against `playbook.md` interest areas
- Decide strategy: statute-focused? case-focused? combined?

### Step 2: Search statutes
- `law_search.sh "keyword"` → list of relevant laws

### Step 3: Fetch statute text (if needed)
- `law_detail.sh [law_id]` → specific articles

### Step 4: Search cases
- `case_search.sh "keyword"` → relevant court decisions

### Step 5: Everyday legal info (optional)
- `life_law.sh "keyword"` → plain-language legal guide

### Step 6: Structured response using template

## Output Template

Action-first structure: lead with what to DO, then back it up with law.

```markdown
## ⚖️ [Topic]

### 📋 Core Answer
[1-2 sentence conclusion — what the user needs to know]

### 🚶 What To Do (practical steps)
1. [Concrete action step] — with conditions/branches if needed
2. [Next step]
3. [Final step]
※ [Situation-specific branch: "If X, then A; if Y, then B"]

### 📖 Legal Basis
**[Law Name]** Art. X (Effective YYYY.MM.DD)
> ① Original text...
> → Plain language: [simplified explanation]

**[Related Law]** Art. Y (if applicable)
> ...

### ⚖️ Related Case (if relevant)
**[Case Number]** ([Court], YYYY.MM.DD)
> Key point: [one-line holding]

### 🔗 References
- [Statute](https://www.law.go.kr/...)

⚠️ Reference only — not legal advice. Consult an attorney for important decisions.
```

**Principles:**
1. User's action = main content; statutes = supporting evidence
2. Branch by situation (listed vs unlisted company, etc.)
3. Cite specific articles, not just law names
4. Ask follow-up if context is needed for better advice

## API Endpoints

### law.go.kr (Primary)
| Target | Description | URL |
|--------|-------------|-----|
| law | Statute search/detail | `https://www.law.go.kr/DRF/lawSearch.do?OC={oc}&target=law&type=JSON` |
| prec | Court cases | `...&target=prec&type=JSON` |
| detc | Interpretation examples | `...&target=detc&type=JSON` |
| admrul | Administrative rules | `...&target=admrul&type=JSON` |

### data.go.kr (Fallback)
| API | Data ID | Endpoint |
|-----|---------|----------|
| Statute search | 15000115 | `http://apis.data.go.kr/1170000/law/lawSearchList.do` |
| Everyday law | 15000215 | `http://apis.data.go.kr/1170000/lifeLawSearch/lifeLawSearchList.do` |
| Case text | 15057123 | (linked to law.go.kr) |

## Connectors

| Placeholder | Purpose | Current Tool |
|-------------|---------|-------------|
| `~~law` | Law/case API | law.go.kr, data.go.kr |
| `~~docs` | Save results | Notion |
| `~~notify` | Alerts | Telegram |
| `~~search` | Supplementary search | Brave Search |

## Notes
1. **Disclaimer**: API info is reference only. Not legal advice.
2. **Currency**: Based on current law, but recent amendments may have delay.
3. **Format**: law.go.kr returns JSON; data.go.kr returns XML → each needs parser.
4. **Priority**: law.go.kr JSON first → fallback to data.go.kr XML.
5. **Encoding**: URL-encode query parameters.

---
*Cowork Legal architecture v2.1 — 🦞 chumjibot (2026-02-14)*

## 🔧 Setup

### 법제처 국가법령정보 API (주 API)
1. [open.law.go.kr](https://open.law.go.kr) 회원가입
2. OC 코드 발급 (이메일 @ 앞부분)
3. `mkdir -p ~/.config/law-go-kr && echo '{"oc":"YOUR_OC"}' > ~/.config/law-go-kr/credentials.json`

### data.go.kr 판례 API (보조)
1. [data.go.kr](https://www.data.go.kr) 회원가입 → 인증키 복사
2. `mkdir -p ~/.config/data-go-kr && echo "YOUR_KEY" > ~/.config/data-go-kr/api_key`

> 법제처 API 미등록 시에도 `web_search` 폴백으로 법령 기본 검색 가능합니다.
