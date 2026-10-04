---
name: daily-papers
description: Review today's HuggingFace daily papers, pick the most relevant one, write a LaTeX summary report with follow-up research directions. Use when asked to check daily papers, do a paper review, or triggered by the scheduler.
---

# Daily Papers Review

## When to use

- User asks to check today's papers, do a daily paper review, or says "daily papers"
- Triggered by the scheduler (e.g., cron every weekday morning)
- User asks "any interesting papers today?"

## Research Topics

Default topics (pick the paper most relevant to any of these):
1. LLM efficiency (quantization, pruning, distillation, inference optimization)
2. Reinforcement learning (RLHF, RLAIF, reward modeling, policy optimization)
3. Continual learning for LLM agents (lifelong learning, memory, catastrophic forgetting)
4. Diffusion LLM (discrete diffusion, text generation via diffusion, hybrid architectures)
5. Time series forecasting (foundation models for time series, multivariate forecasting)

If the user specifies different topics (e.g., "focus on RL today"), use those instead.

## Papers Log

A log of previously reviewed papers is kept at `reports-repo/papers-log.json` to avoid re-reviewing.

Format:
```json
[
  {"arxiv_id": "2506.12345", "title": "Paper Title", "reviewed_on": "2026-03-04", "report": "2026-03-04-daily-papers.pdf"}
]
```

If the file doesn't exist, create it as an empty array `[]`.

## Workflow

### 1. Fetch today's papers

Use `mcp__hf_papers__get_today_papers` to get the day's trending papers.

### 2. Filter and select

- Read `reports-repo/papers-log.json` — collect all previously reviewed `arxiv_id` values
- Skip any paper whose arxiv ID is already in the log
- From the remaining papers, pick the **1 paper** most relevant to the research topics
- If the user overrode topics, use those instead of defaults
- If no papers match any topic, post to Slack: "No new papers matching your research topics today." and stop

### 3. Study the paper

- Use `mcp__arxiv__get_paper` to fetch the full paper metadata
- Download and read the PDF if possible using WebFetch
- Deeply analyze the paper:
  - What is the core problem and why does it matter?
  - What is the key technical contribution?
  - What are the main results (quantitative where possible)?
  - What are the limitations and assumptions?

### 4. Brainstorm follow-up research

Generate 2-3 concrete follow-up research directions:
- Each must be specific enough to start working on (not vague like "improve performance")
- For each direction include:
  - One-line description
  - What gap it addresses
  - Approach sketch (2-3 sentences)
  - Feasibility: easy (weeks) / moderate (months) / hard (6+ months)
- Prioritize by intersection of novelty and feasibility

### 5. Write LaTeX report

Write a report to `reports-repo/reports/YYYY-MM-DD-daily-papers.tex` with:
- `\section{Paper Summary}` — title, authors, core contribution, method, results, limitations. Include links:
  - arxiv: `https://arxiv.org/abs/{id}`
  - HF daily papers page: `https://huggingface.co/papers/{id}`
  - GitHub repo (if the paper has an open-source implementation — check the paper metadata or HF page for a repo link; omit if none exists)
- `\section{Follow-up Research Directions}` — the 2-3 directions with full detail
- `\section{Conclusion}` — key takeaway and recommended next step
- Proper `\bibliography` with BibTeX entries for the paper and any referenced work

Compile:
```bash
cd reports-repo/reports
pdflatex -interaction=nonstopmode YYYY-MM-DD-daily-papers.tex
bibtex YYYY-MM-DD-daily-papers
pdflatex -interaction=nonstopmode YYYY-MM-DD-daily-papers.tex
pdflatex -interaction=nonstopmode YYYY-MM-DD-daily-papers.tex
```

### 6. Publish

- From `reports-repo/`, commit the `.tex`, `.bib`, and `.pdf` files
- Push to GitHub
- Update `reports-repo/papers-log.json` — append the new entry, commit and push

### 7. Post to Slack

Post a concise summary (not the full report):
- Paper title with links: arxiv, HF daily papers page, GitHub repo (if exists)
- 2-3 sentence summary of what the paper does and why it matters
- Top follow-up research idea (1 sentence)
- Link to the PDF report: get the repo URL via `git -C reports-repo remote get-url origin`, then construct `<repo-url>/blob/main/reports/YYYY-MM-DD-daily-papers.pdf` (strip any `.git` suffix and auth prefix)
