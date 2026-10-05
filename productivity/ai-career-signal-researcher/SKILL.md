---
name: ai-career-signal-researcher
description: "Use when the user wants an AI Systems Engineering Signal Radar: researching AI systems engineering trends, AI infrastructure, agent infrastructure, production AI and LLM application engineering, agent/RAG/evals/MCP/workflow automation trends, YouTube/podcast/blog/GitHub/hiring-market signals, career skill demand for AI systems engineers, or Medium/LinkedIn/GitHub portfolio content opportunities. Optimized for a backend engineer with strong Python production experience transitioning into AI systems engineering and AI infrastructure engineering."
---

# AI Career Signal Researcher

## Purpose

Use this skill to research practical career and market signals for AI systems engineering. Treat YouTube as one evidence source, not the whole research surface.

Optimize analysis for a backend engineer with strong Python production experience who is moving toward production-grade AI systems, LLM applications, agentic workflows, RAG, evaluations, observability, data pipelines, and backend infrastructure. Prefer practical demand, implementation difficulty, engineering depth, and portfolio relevance over hype.

## Quick Usage

Use this skill for prompts such as:

1. "Research the latest AI agent infrastructure signals and tell me what I should learn next."
2. "Analyze YouTube and blog signals around MCP and whether it is worth learning deeply."
3. "Find career signals for AI systems engineers in Singapore and China mainland."
4. "Compare market demand for RAG, agents, evals, and AI observability."
5. "Find content opportunities for my Medium/LinkedIn based on current AI engineering trends."
6. "Analyze whether agent runtime is becoming a real infrastructure category."

## Signal Sources

Collect from the sources available for the task:

- YouTube: technical talks, AI engineering channels, conference videos, founder/engineer interviews, tutorials, and product demos.
- GitHub: trending repositories, repo activity, release cadence, issue/discussion friction, contributor shape, and production-adoption clues. Do not overweight stars.
- Blogs and engineering posts: OpenAI, Anthropic, Google DeepMind, Meta AI, AWS, Microsoft, Databricks, LangChain, LlamaIndex, Modal, Temporal, Vercel, Cloudflare, and other AI infrastructure companies.
- Job-market signals: job descriptions, skill requirements, salary ranges when available, region differences, and keyword stuffing. Pay special attention to China mainland, Hong Kong, Singapore, Japan, and remote roles when relevant.
- Community signals: Hacker News, Reddit, X/Twitter, Discord/forum discussions when available, and technical newsletters.

When external browsing or current market data matters, verify live sources before synthesizing. Cite sources in the final answer when browsing was used.

## YouTube Source Collector

The existing helper script remains a YouTube-specific collector for search, channel inspection, and transcripts. Use it when YouTube evidence is useful, especially for technical talks, demos, interviews, or claim extraction.

Run these commands from this skill directory:

```bash
python scripts/youtube_research.py --help
```

Common commands:

```bash
python scripts/youtube_research.py search "AI agent infrastructure MCP evals" --limit 10 --json

python scripts/youtube_research.py search "production RAG evaluation observability" --limit 8 --transcripts 5 --excerpt-chars 900 --json

python scripts/youtube_research.py channel "@ycombinator" --limit 12 --with-transcripts 3 --json

python scripts/youtube_research.py transcript "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --lang en
```

Use `--json` when results will be synthesized in chat. Use `--no-cache` for fast-moving topics where freshness matters. Keep transcript fetching targeted; use transcripts for actual claims, not broad popularity scans.

## Research Themes

Prefer these themes when the user does not specify a narrower target:

- AI agents, agent runtime, agent orchestration, agent memory, MCP, tool use, and browser automation
- RAG, retrieval infrastructure, vector databases, embedding pipelines, and data pipelines for AI systems
- Evals, evaluation harnesses, LLM observability, prompt/version management, guardrails, and human-in-the-loop systems
- AI gateways, model routing, inference cost optimization, latency optimization, streaming systems, and production deployment patterns
- Multimodal AI applications, AI coding agents, Codex/Claude Code/Cursor/Devin-like workflows, AI workflow automation, and AI infra startups
- Backend engineering skills that remain valuable in AI systems

## Workflow

1. Clarify the research target only if the request is too broad to produce useful recommendations.
2. Collect signals from available sources; use the YouTube collector only when YouTube is relevant.
3. Normalize findings into structured signal categories.
4. Filter out shallow hype and popularity-only evidence.
5. Map findings to backend engineering, AI systems engineering, and production constraints.
6. Recommend learning, portfolio, and writing actions.
7. Produce a concise, evidence-aware report.

## Analysis Dimensions

Classify findings with these dimensions:

- Signal type: Hype signal, Hiring signal, Infrastructure signal, Product adoption signal, Open-source activity signal, Developer pain signal, Content opportunity signal, Portfolio opportunity signal.
- Engineering depth: Surface-level tool usage, Application integration, Production system design, Infrastructure/platform engineering, Research-heavy/model-level work.
- Career relevance: Immediately useful for current backend + AI transition, Useful within 3-6 months, Long-term strategic bet, Interesting but not urgent, Mostly hype/low ROI.
- Evidence strength: Strong when multiple independent sources agree, Medium when credible but limited, Weak when mostly social hype or one-off claims.
- Recommended action: Learn, Build portfolio project, Write Medium/LinkedIn post, Track further, Ignore for now, Use at work if relevant.

## Output Format

Usually structure the final answer as:

```markdown
# AI Career Signal Report

## Executive Summary
Concise summary of what changed, what matters, and what the user should do.

## Top Signals
For each signal:
- Signal
- Why it matters
- Evidence
- Engineering depth
- Career relevance
- Confidence
- Recommended action

## Skill Demand Map
- Core backend skills that remain valuable
- AI application engineering skills
- AI infrastructure skills
- Agentic system skills
- Evaluation / observability skills
- Optional / speculative skills

## Market Interpretation
Distinguish real engineering demand, buzzword-driven demand, startup demo demand, enterprise implementation demand, and research-lab demand.

## Portfolio Opportunities
For each project: project idea, target skills demonstrated, market relevance, expected difficulty, and possible GitHub / Medium / LinkedIn output.

## Content Opportunities
For each idea: title, target audience, why now, unique angle, and whether it should be a short post, long article, or GitHub-backed case study.

## Watchlist
Topics to keep monitoring.

## Ignore / Deprioritize
Topics that look overhyped or low-ROI for the user right now.
```

For small requests, use a shorter version of the same structure.

## Constraints

- Do not overfit to YouTube metrics such as views, thumbnails, or title packaging.
- Do not treat popularity as proof of importance.
- Prefer engineering adoption, hiring demand, production usage, repeated pain points, and credible implementation evidence.
- Be explicit when evidence is weak.
- Separate "interesting trend" from "worth my time."
- Prefer practical recommendations over generic summaries.
- Avoid generic career advice and vague claims like "AI is growing rapidly."
- Always connect findings back to backend engineering, AI systems engineering, and production constraints.

## Portability Notes

- Specific to the author's current workflow: analysis defaults to a backend engineer with strong Python production experience moving into AI systems engineering, with extra attention to Asia-region market signals when relevant.
- Reusable: the evidence-first signal collection, hype filtering, career relevance scoring, and portfolio/content mapping workflow.
- Adapt before reuse: replace the career profile, target regions, preferred publishing surfaces, and available collectors or API keys with the adopting user's context.

## References

- `references/source-evaluation.md` for evaluating external evidence and avoiding popularity traps.
- `references/api-notes.md` for the YouTube collector's SerpApi and Supadata endpoint notes.
- `references/sample-ai-career-signal-report.md` for a compact example report shape.
