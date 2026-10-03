---
name: lawclaw
description: Drop a contract, get answers. lawclaw rips through PDFs, spots risky clauses, diffs redlines, checks citations, and searches thousands of discovery docs—locally, so nothing leaves your machine. Built for attorneys and paralegals who bill by the hour and can't waste one.
homepage: https://github.com/legal-tools/lawclaw
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":["pdftotext","diff","grep","pandoc"]},"install":[{"id":"brew-poppler","kind":"brew","formula":"poppler","bins":["pdftotext"],"label":"Install pdftotext (brew)"},{"id":"brew-pandoc","kind":"brew","formula":"pandoc","bins":["pandoc"],"label":"Install pandoc (brew)"}]}}
---

# lawclaw

Drop a contract, get answers.

lawclaw tears through legal documents the way you wish your associates would—fast, thorough, and without missing the indemnification clause buried on page 47. It extracts text from PDFs, flags key clauses, generates redline comparisons, validates citations, and searches entire discovery sets for the one sentence that wins your case.

Everything runs locally on your machine. No uploads, no third-party servers, no risk to attorney-client privilege. Just you, your terminal, and a very sharp claw.

**Who it's for:** Attorneys, paralegals, and legal ops teams doing contract review, litigation support, due diligence, e-discovery, or brief-writing.

**What it replaces:** Hours of Ctrl+F across dozens of PDFs.

## Core Capabilities

**Document Analysis**
- Extract text from legal PDFs: `pdftotext <file.pdf> <output.txt>`
- Search for specific clauses: `grep -i "indemnification\|liability\|warranty" contract.txt`
- Word count for billing: `wc -w document.txt`
- Extract metadata: `pdfinfo <file.pdf>`

**Contract Clause Extraction**
Use grep with regex to find common clauses:
- Indemnification: `grep -i "indemnif\|hold harmless" contract.txt`
- Termination: `grep -i "terminat\|cancellation" contract.txt -A 3`
- Confidentiality: `grep -i "confidential\|proprietary\|NDA" contract.txt -A 3`
- Force majeure: `grep -i "force majeure\|act of god" contract.txt -A 3`
- Jurisdiction: `grep -i "jurisdiction\|venue\|governing law" contract.txt -A 2`
- Arbitration: `grep -i "arbitration\|dispute resolution" contract.txt -A 3`
- Non-compete: `grep -i "non-compete\|noncompete\|restrictive covenant" contract.txt -A 3`
- Assignment: `grep -i "assign\|transfer\|delegate" contract.txt -A 2`

**Redline / Comparison**
- Compare two versions: `diff -u original.txt revised.txt > redline.diff`
- Side-by-side view: `diff -y original.txt revised.txt | less`
- Word-level diff: `wdiff original.txt revised.txt > changes.txt`
- Convert Word to text first: `pandoc contract.docx -t plain -o contract.txt`

**Citation and Reference Checking**
- Find case citations: `grep -E "[0-9]+ [A-Z]\.[A-Za-z0-9.]+ [0-9]+" brief.txt`
- Find U.S. Code refs: `grep -E "[0-9]+ U\.S\.C\. § [0-9]+" document.txt`
- Find CFR refs: `grep -E "[0-9]+ C\.F\.R\. § [0-9]+" document.txt`
- Extract footnotes: `grep -E "\[[0-9]+\]" brief.txt`
- Find Bluebook short cites: `grep -E "[A-Z][a-z]+, [0-9]+ [A-Z]\." brief.txt`

**Document Organization**
- Find specific file types: `find . -name "*.pdf" -type f`
- Search within discovery docs: `grep -r "key term" ./discovery/`
- List recent modifications: `find . -name "*.pdf" -mtime -7 -ls`
- Batch rename exhibits: `for f in *.pdf; do mv "$f" "Exhibit_${f}"; done`

**Discovery Support**
- Count pages in PDF: `pdfinfo document.pdf | grep Pages`
- Batch convert PDFs: `for f in *.pdf; do pdftotext "$f" "${f%.pdf}.txt"; done`
- Create production log: `ls -lh *.pdf > production_log.txt`
- Search Bates numbers: `grep -r "PROD[0-9]\{6\}" ./documents/`

**Due Diligence**
- Scan for key terms: `grep -i "material adverse\|intellectual property\|pending litigation" diligence/*.txt`
- Extract dates: `grep -E "[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}" contract.txt`
- Find monetary amounts: `grep -E "\$[0-9,]+(\.[0-9]{2})?" agreement.txt`
- Identify parties: `grep -E "WHEREAS|Party|Seller|Buyer|Lessor|Lessee" contract.txt`

**Deposition / Transcript Analysis**
- Search testimony: `grep -i "Q\." deposition.txt | grep -i "keyword"`
- Extract witness answers: `grep "A\." deposition.txt -A 2`
- Count pages/lines: `wc -l transcript.txt`

**Privilege Log Support**
- Generate file list: `find ./documents -type f -exec ls -lh {} \; > privilege_log.csv`
- Search for privileged terms: `grep -ri "attorney-client\|work product" ./emails/`
- Tag privileged docs: `grep -rli "attorney-client" ./emails/ > privileged_files.txt`

## Common Workflows

**Contract Review Checklist**
1. Extract text: `pdftotext contract.pdf contract.txt`
2. Scan key clauses:
   - `grep -i "limitation of liability" contract.txt`
   - `grep -i "indemnification" contract.txt`
   - `grep -i "termination" contract.txt`
   - `grep -i "confidentiality" contract.txt`
   - `grep -i "governing law" contract.txt`
3. Extract monetary terms: `grep -E "\$[0-9,]+" contract.txt`
4. Flag deadlines: `grep -i "within [0-9]+ days\|business days\|calendar days" contract.txt`

**Redline Workflow**
1. Convert both versions: `pandoc original.docx -t plain -o original.txt && pandoc revised.docx -t plain -o revised.txt`
2. Generate diff: `diff -u original.txt revised.txt > changes.diff`
3. Side-by-side: `diff -y original.txt revised.txt | less`

**Discovery Review**
1. Extract all PDFs: `for pdf in discovery/*.pdf; do pdftotext "$pdf" "${pdf%.pdf}.txt"; done`
2. Search across all docs: `grep -ri "responsive term" discovery/*.txt`
3. Generate document index: `ls -lh discovery/*.pdf > document_index.txt`

**Due Diligence Package Review**
1. Extract all docs: `find diligence/ -name "*.pdf" -exec pdftotext {} \;`
2. Search for red flags: `grep -ri "litigation\|breach\|default\|bankruptcy" diligence/*.txt`
3. Extract unique dates: `grep -Eroh "[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}" diligence/*.txt | sort -u`

**Brief / Motion Citation Check**
1. Extract citations: `grep -E "[0-9]+ [A-Z]\.[A-Za-z0-9.]+ [0-9]+" brief.txt`
2. Cross-reference ToA: `diff <(grep -oE "[0-9]+ [A-Z]\.\S+ [0-9]+" brief.txt | sort -u) <(sort toa.txt)`

## Notes

- All processing runs locally—no cloud uploads—so client confidentiality is preserved
- Convert proprietary formats (DOCX, DOC) to plain text via `pandoc` before analysis
- Use `wdiff` for word-level comparison: install via `brew install wdiff`
- Combine with `gog` skill for Google Workspace integration (Drive, Gmail, Sheets)
- Confirm with supervising attorney before automated batch operations on case files
- For OCR on scanned PDFs, install `tesseract`: `brew install tesseract`

## Security & Ethics Reminders

- Verify all OCR-extracted text for accuracy before relying on it in filings
- Maintain privilege logs when processing communications
- Use redaction tools for PII before document production
- Comply with court e-discovery orders, ESI protocols, and local rules
- Keep audit trails of all document processing for chain-of-custody challenges
- Never transmit client data to external services without written consent
