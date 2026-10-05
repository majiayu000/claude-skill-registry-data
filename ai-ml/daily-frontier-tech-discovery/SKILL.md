---
name: daily-frontier-tech-discovery
description: Discover and send a daily frontier technology brief for AI, LLMs, agents, memory systems, trustworthy AI, data-centric ML, enterprise/private AI, GitHub developer tools, autonomous driving, world models, and embodied intelligence. Use this skill whenever the user asks for daily tech discovery, frontier AI research scanning, OpenReview/arXiv/GitHub trend monitoring, or sending a concise technical brief to a DingTalk group.
metadata:
  requires:
    bins:
      - python3
---

# Daily Frontier Tech Discovery

## Runtime paths

Resolve paths from the current user's home directory so the skill remains portable:

- Memory root: `${FRONTIER_MEMORY_ROOT:-$HOME/Documents/memory}`
- Report directory: `${FRONTIER_REPORT_DIR:-$FRONTIER_MEMORY_ROOT/tech/daily frontier report}`
- Skill directory: `$HOME/.agents/skills/daily-frontier-tech-discovery`

Use these resolved paths everywhere below. Never substitute another user's hard-coded home directory.

## Purpose

Produce a concise daily frontier technology brief for a technical audience.

The goal is not to summarize AI news. The goal is to find technically meaningful breakthroughs, implementations, papers, benchmarks, repos, engineering writeups, and product architecture signals that can inform Friday / PreSeen work, especially agent runtime, memory, feedback-native learning, enterprise AI workflow, data-centric ML, evaluation, alignment, trustworthy AI, and autonomous driving.

## Product Contract

The final output is a Friday artifact suitable for direct DingTalk group posting:

- Chinese
- Markdown
- Each item should be at most 150 Chinese characters and 100 English words, excluding URLs
- Maximum 8 items
- Items must be extremely fresh: default publication/update window is the last 72 hours, with priority for the last 48 hours
- Every item includes a Markdown URL
- Every item includes an internal relevance reason based on local meeting notes or project documents
- Every generated daily report is archived under the resolved report directory.
- The default selected set should be driven by curated sources and engineering/product signals, not by arXiv volume. Papers are eligible only when they have clear impact signals such as high citations, top-tier venue acceptance, unusually strong benchmark adoption, or repeated appearance in curated/trending sources.
- No conversational preface
- No process narration
- No generic market commentary
- No item without technical evidence

Preferred report shape:

```markdown
# 技术前沿洞察（YYYY.M.D）
趋势/热度：基于过去几天 archived reports 的连续主题做热度判断；说明哪些方向持续升温、哪些是当天新增技术信号、哪些只是低热但高相关的专项线索。不要把“近 72 小时”本身写成热度理由。

## 关键趋势与证据
- **趋势名**：72 小时内的新发现/新发布/新代码。荐因：优先写它对哪个人/角色有帮助、为什么值得对方点开；其次才写关联的项目或系统。[来源](url)

结论：...
```

Use the user's sample style: trend-oriented, compact, technical, suitable for a technical group chat. Do not write a dry metadata list. The internal relevance reason must appear in the DingTalk-facing text itself, preferably with `荐因：`.

Length counting rule:

- Strip URLs before counting.
- Count Chinese by CJK characters, not total string length.
- Count English by words/tokens, not characters.
- Mixed Chinese/English items pass when CJK characters are <=150 and English words are <=100.

Recommendation reasons should be people-oriented whenever possible:

- Prefer named people or roles from local meeting notes, such as Xiaomin张晓民, 周俊杰, 王静, 张毅倜(ET), 侯总, or the relevant owner role.
- When mentioning a person or emphasized role in the DingTalk-facing report, bold it with Markdown, for example `**小明**`, `**周俊杰**`, `**王静**`, or `**负责自动驾驶标注验证的同学**`.
- Explain the personal work benefit: what decision, implementation, test design, debugging, or experiment the person can make better after reading it.
- Avoid making the reason only a project mapping like "关联 Friday" or "关联 StarBench"; project names may appear, but the motivation should be human and actionable.

Trend/heat analysis rule:

- Before writing `趋势/热度`, inspect prior reports in the resolved report directory.
- Treat repeated topics across multiple archived reports as higher heat, such as agent runtime/tooling, skills/composability, memory/RAG, evaluation loops, safety/provenance, compression/private deployment, or world models.
- Distinguish long-running heat from the current day's fresh delta.
- Do not say a topic is hot merely because it was published in the last 72 hours.

After candidate analysis and ranking, archive the full local analysis first. Then produce a separate DingTalk-facing Markdown file from the selected ranked items and send only that DingTalk-facing file. After a successful DingTalk send, update the reported-item history so future runs can deduplicate and explain incremental updates.

## Report Archive Policy

Store every generated daily report under:

`${FRONTIER_REPORT_DIR:-$HOME/Documents/memory/tech/daily frontier report}`

Use these filename patterns:

- Full local archive: `YYYY-MM-DD-daily-frontier-report.md`
- DingTalk-facing text only: `YYYY-MM-DD-daily-frontier-report-dingtalk.md`

If multiple reports are generated on the same day, append a short suffix:

`YYYY-MM-DD-daily-frontier-report-2.md`
`YYYY-MM-DD-daily-frontier-report-2-dingtalk.md`

The full local archive must include every serious candidate that passed the first filter, including both selected and rejected candidates. It must be auditable and contain:

- candidate title
- canonical key
- URL
- channel/source, such as arXiv, OpenReview, GitHub, Hugging Face, Techmeme, DevURLs, first-party blog, technical blog, or search
- discovered_at / freshness date
- freshness evidence
- content summary
- technical novelty / delta
- dedup status and previous recommendation date if any
- local relevance evidence, prioritized by person, meeting, role/current task, then company strategy fallback
- recommendation reason
- score table and total score
- comments / reviewer notes
- final decision: selected, rejected, or track-only
- rejection reason when rejected

The DingTalk-facing file must contain only the final sorted selected items and must be directly copy/paste/sendable. It must not include raw scores, local file paths, process notes, rejected items, hidden YAML, credentials, or send status.

Use the full archive directory and reported-item history as the source for future deduplication and trend/heat analysis. Keep raw candidate analysis out of the DingTalk-facing file.

Candidate scoring rubric:

- `freshness_score` 0-5: freshness and verifiability of the update.
- `technical_depth_score` 0-5: concrete implementation, architecture, paper, benchmark, code, or reproducible method.
- `frontier_score` 0-5: whether it is genuinely early/frontier rather than generic commentary.
- `local_relevance_score` 0-5: strength of dynamic connection to local people, meetings, roles, or strategy.
- `actionability_score` 0-5: whether someone can read it and make a concrete implementation, test, eval, or product decision.
- `novelty_dedup_score` 0-5: new item or meaningful delta beyond prior reports.
- `signal_heat_score` 0-5: long-running heat from prior local daily reports and repeated external signals.

Sort candidates by total score. Use the sorted list to choose final DingTalk items. Do not choose lower-scored items unless the archive comment explains the editorial reason.

Maintain a lightweight history index in the same directory:

`${FRONTIER_REPORT_DIR:-$HOME/Documents/memory/tech/daily frontier report}/reported_items.jsonl`

Append one JSON object per successfully sent item:

```json
{"canonical_key":"github:owner/repo","title":"...","url":"https://...","reported_at":"YYYY-MM-DD","report_path":"$HOME/Documents/memory/tech/daily frontier report/YYYY-MM-DD-daily-frontier-report.md","novelty_delta":"...","internal_link":"...","recommendation_reason":"..."}
```

Use `reported_items.jsonl` first for fast lookup, then inspect archived Markdown reports when more context is needed.

## Freshness Policy

Freshness is a hard gate, not a nice-to-have.

Default rule:

- Only include items published, released, substantially updated, or first made discoverable within the last 72 hours.
- Prefer items from the last 48 hours.
- If the task is a daily report, do not include older evergreen papers, old GitHub repos, old surveys, or old benchmark pages just because they are technically relevant.

Allowed freshness evidence:

- publication date
- GitHub `created_at`, release date, or last meaningful push
- official blog publish date
- OpenReview revision date
- arXiv submission or replacement date
- Hugging Face paper trending entry with current date signal
- benchmark leaderboard update date

Older canonical items may appear only when the new information is fresh:

- new release in the last 72 hours
- new benchmark result in the last 72 hours
- new model/code/data release in the last 72 hours
- new official technical explanation in the last 72 hours
- new OpenReview/arXiv revision in the last 72 hours

In that case, the report must frame the item around the fresh delta, not the old project:

```markdown
- **项目名**：此前在 YYYY-MM-DD 推荐过；本次 72 小时内新增 X，关联内部项目 Y，推荐关注 Z。[来源](url)
```

If freshness cannot be verified, reject the item.

## Paper Influence Gate

Do not fill the report with newly posted papers just because they are recent and technically relevant. Treat papers as a higher-threshold source class than curated news, repos, releases, benchmarks, or first-party engineering writeups.

A paper can enter the first filter only if at least one influence signal is verifiable:

- Accepted by or clearly associated with a top-tier venue or high-signal workshop, such as ICLR, ICML, NeurIPS, COLM, CoRL, CVPR, ICCV, ECCV, ACL, EMNLP, NAACL, SIGGRAPH, SOSP, OSDI, NSDI, VLDB, SIGMOD, or an equivalent venue for the topic.
- Has high citation count for its age, or is from an established benchmark/project with visible adoption. For very new papers where citations are not yet meaningful, use other signals in this list.
- Appears in curated or trending sources such as Hugging Face Papers Trending, Papers with Code trending/leaderboards, Techmeme, DevURLs-linked discussions, GitHub trending repo/code release, or repeated independent technical discussions.
- Releases credible code, benchmark data, leaderboard, reproducible harness, or first-party implementation that materially changes engineering practice.
- Directly answers a strong recent AI听记 meeting trigger and has an external material date within the allowed support window; even then, it should be framed as support material and should not crowd out stronger curated-source candidates.

Reject or track-only papers that are merely fresh arXiv/OpenReview submissions with no venue, citation/adoption, code/benchmark, curated-source, or strong meeting-trigger signal. The archive should record this as `rejection reason: paper lacks verified influence signal`.

## Local Context Policy

Every final item must be connected back to local company context before it can be recommended.

Use local documents under the resolved memory root as the primary internal context source. Relevant local sources include:

- Meeting transcripts and summaries, especially `AI听记/`
- Friday product docs under `product/Friday/`
- Strategy, OKR, and management docs
- Product docs for StarBench, Hyperion, MorningStar, data compliance, and autonomous-driving research
- Existing graphify knowledge graph output under `graphify-out/`

When working inside the resolved memory root, follow the project graph rules:

- Read `graphify-out/GRAPH_REPORT.md` before architecture or codebase-style interpretation.
- If `graphify-out/wiki/index.md` exists, navigate it first.
- For cross-module relationships, prefer `graphify query "<question>"`, `graphify explain "<concept>"`, or `graphify path "<A>" "<B>"` when available.
- Use `rg` only as fallback or for targeted evidence lookup.

For each shortlisted external item, find at least one internal connection using this priority order:

1. Person: a named internal owner, stakeholder, meeting participant, or directly affected operator.
2. Meeting: a specific meeting note, discussion, decision, concern, or action item that already raised the same problem.
3. Role/current task: the team role or active workstream that would use the item when no named person is available.
4. Company strategy/project: Friday, StarBench, Hyperion, MorningStar, PreSeen, data annotation, autonomous-driving research, enterprise private deployment, or another strategic initiative. Use this only as fallback when no person or meeting connection is available.

The DingTalk-facing `荐因` should follow the same priority. Prefer "Xiaomin can use this to..." or "the 4/22 meeting raised..." over "关联 Friday". Project names can appear as context, but should not be the primary recommendation reason unless no person or meeting connection exists.

Each final recommendation must include:

- `internal_link`: the local person/meeting/role first; fallback to project/strategy only when needed
- `recommendation_reason`: why this item is worth sending to the team based on that internal connection
- `local_evidence`: local file path or graphify result used as evidence

If no internal connection can be found, do not include the item in the final DingTalk report, even if it is globally interesting.

## Tool Policy

Prefer Exa for discovery and content extraction:

- Use `web_search_exa` for web, GitHub, arXiv, OpenReview, Hugging Face Papers, technical blogs, and benchmark discovery.
- Use `web_fetch_exa` to read only shortlisted URLs.
- Use compact, targeted queries with source and time intent, such as:
  - `site:openreview.net agent memory LLM reasoning 2026`
  - `site:arxiv.org LLM agent evaluation long horizon 2026`
  - `site:github.com AI agent memory benchmark pushed recently`
  - `site:huggingface.co/papers agent memory evaluation 2026`

Fallback only when Exa is insufficient:

- Tavily or web search for missing webpage summaries.
- GitHub page fetch for README, recent releases, stars, and last push.
- arXiv/OpenReview/Hugging Face paper pages for abstract, code link, benchmark, and author context.

## Source Tiers

### Required Aggregators

Scan these first by title, URL, source, date if available, and short summary. They are not optional: the candidate pool should start here before arXiv/OpenReview expansion.

- [Techmeme](https://www.techmeme.com/)
- [Trendshift Python 7-day GitHub trends](https://trendshift.io/?trending-range=7&trending-language=python)
- [DevURLs](https://devurls.com/)

Curated-source handling:

- Techmeme: parse homepage news titles and links; prioritize first-party technical/product announcements over media commentary.
- Trendshift Python 7-day GitHub trends: parse project list and inspect only relevant repos for release date, recent commits, README, stars/velocity, and technical substance.
- DevURLs: parse aggregated Hacker News, Lobsters, and other developer links; prioritize links with engineering depth, first-party posts, open-source releases, or substantive technical discussion.
- A candidate sourced from these aggregators gets a stronger `signal_heat_score` than an isolated paper, provided the technical substance and freshness are verified.
- If daily time is limited, prefer fewer, better candidates from these curated sources over many arXiv abstracts.

### Research Frontiers

- [OpenReview](https://openreview.net/)
- [arXiv cs.AI](https://arxiv.org/list/cs.AI/recent)
- [arXiv cs.LG](https://arxiv.org/list/cs.LG/recent)
- [arXiv cs.CL](https://arxiv.org/list/cs.CL/recent)
- [arXiv cs.RO](https://arxiv.org/list/cs.RO/recent)
- [Hugging Face Papers Trending](https://huggingface.co/papers/trending)
- [Papers with Code](https://paperswithcode.com/)

Research-frontier sources are secondary expansion sources. Use them after the required aggregators, or when a recent AI听记 trigger requires technical support. Apply the Paper Influence Gate before promoting any paper into first filter.

### Conference and Workshop Frontiers

Prioritize OpenReview venues and workshops when relevant:

- [ICLR](https://openreview.net/group?id=ICLR.cc)
- [ICML](https://openreview.net/group?id=ICML.cc)
- [NeurIPS](https://openreview.net/group?id=NeurIPS.cc)
- [COLM](https://openreview.net/group?id=colmweb.org)
- [CoRL](https://openreview.net/group?id=robot-learning.org%2FCoRL)

High-signal workshop topics:

- LLM Reasoning
- World Models
- Reliable Autonomy
- Re-Align
- Trustworthy ML
- Agentic AI
- Embodied AI
- Evaluation and Datasets

### GitHub and Developer Tools

- [GitHub Trending Python](https://github.com/trending/python?since=daily)
- [GitHub Trending TypeScript](https://github.com/trending/typescript?since=daily)
- [GitHub Topics: llm](https://github.com/topics/llm)
- [GitHub Topics: ai-agents](https://github.com/topics/ai-agents)
- [GitHub Topics: rag](https://github.com/topics/rag)
- [GitHub Topics: autonomous-driving](https://github.com/topics/autonomous-driving)

### First-Party Technical Blogs

- [OpenAI News](https://openai.com/news/)
- [Anthropic Engineering](https://www.anthropic.com/engineering)
- [Google DeepMind Blog](https://deepmind.google/discover/blog/)
- [Meta AI Blog](https://ai.meta.com/blog/)
- [Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/)
- [NVIDIA Technical Blog](https://developer.nvidia.com/blog/)
- [Hugging Face Blog](https://huggingface.co/blog)
- [GitHub AI & ML Blog](https://github.blog/ai-and-ml/)
- [LangChain Blog](https://blog.langchain.com/)
- [LlamaIndex Blog](https://www.llamaindex.ai/blog)
- [Letta Blog](https://letta.com/blog)
- [Modal Blog](https://modal.com/blog)
- [Databricks Blog](https://www.databricks.com/blog)

### Benchmark and Eval Sources

- [SWE-bench](https://www.swebench.com/)
- [METR RE-Bench](https://openreview.net/forum?id=3rB0bVU6z6)
- [FrontierSWE](https://frontierswe.com/)
- [LMArena](https://lmarena.ai/)
- [HELM](https://crfm.stanford.edu/helm/)
- [OpenCompass](https://opencompass.org.cn/)
- [Agent Leaderboard](https://huggingface.co/spaces/galileo-ai/agent-leaderboard)

## Focus Areas

Filter strictly by technical relevance:

1. Model safety and trustworthy AI
   - Data attribution
   - Model provenance
   - Hallucination detection and mitigation
   - Evaluation, red teaming, guardrails, agent safety

2. Agents and alignment
   - Agent runtime, harness, sandbox
   - Long-running agents
   - Sub-agent workflow
   - Tool-use planning
   - RL for alignment
   - Human feedback, preference learning
   - Agent memory, task memory, execution memory

3. Memory and enterprise knowledge systems
   - Long-term memory
   - Workspace memory
   - Team memory
   - Continuous context
   - Graph memory
   - Knowledge rollup
   - Expert knowledge networks
   - Enterprise search plus agent execution

4. Model performance and reasoning
   - Advanced reasoning
   - CoT, ToT, planning optimization
   - Test-time compute
   - Inference optimization
   - Model routing and small-model orchestration

5. Data-driven AI
   - Data-centric ML
   - Synthetic data
   - Automated labeling
   - Knowledge distillation
   - Dataset quality
   - Eval data generation
   - RLHF/RLAIF data pipelines

6. Enterprise and private AI
   - Private LLM deployment
   - On-prem or VPC AI stack
   - Permission-aware retrieval
   - Enterprise workflow automation
   - Auditability and compliance for AI systems

7. GitHub and developer tooling
   - AI/LLM/agent repos
   - Agent frameworks
   - Eval frameworks
   - Memory frameworks
   - AI coding and workflow automation tools

8. Autonomous driving and embodied intelligence
   - World models
   - VLA and embodied agents
   - Simulation and synthetic scenario generation
   - Autonomous driving data engine
   - 3D/spatial intelligence, LiDAR, BEV

## Exclusions

Exclude by default:

- Financial reports
- Stock price movement
- Fundraising without technical detail
- Executive or personnel changes
- Generic product announcements
- Non-technical trend commentary
- Marketing-only posts
- Reposts with no original technical source
- Items already reported unless they contain a clear new technical delta

## Workflow

### 1. Source Scan

Scan required aggregators before research-frontier feeds. Capture only:

- title
- URL
- source
- date if available
- short summary
- suspected category

Order:

1. Techmeme homepage titles and links.
2. Trendshift Python 7-day GitHub project list.
3. DevURLs aggregated developer links and titles.
4. First-party technical blogs, GitHub releases/trending, benchmark and eval sources.
5. OpenReview/arXiv/Hugging Face/Papers with Code only after applying the Paper Influence Gate.

Do not let arXiv recency dominate the first-filter pool. If the day's curated sources provide enough technically strong candidates, use papers only for high-impact support or benchmark context.

Do not deep-read every source at this stage.

### 2. Candidate Normalize

For every candidate, create:

- `canonical_key`
- `item_type`: paper, repo, benchmark, technical_blog, product_technical_note, other
- `source_url`
- `primary_evidence_url`
- `suspected_category`
- `freshness_date`
- `freshness_evidence`

Canonical key examples:

- `paper:arxiv:2602.15112`
- `paper:openreview:3rB0bVU6z6`
- `github:letta-ai/letta-evals`
- `benchmark:frontierswe`
- `blog:anthropic:managed-agents`

### 3. Filter

Remove candidates that are:

- Not technical
- Purely commercial
- Missing a URL
- Missing technical evidence
- Older than 72 hours without a fresh technical delta
- Missing verifiable freshness evidence
- Papers without verified influence signal under the Paper Influence Gate
- Outside the focus areas

Do not perform historical deduplication here. This stage is for basic quality, relevance, and freshness.

### 4. Deduplicate

Deduplication happens after Filter and before Score.

Check reported-item history before scoring:

Primary lookup source:

- `${FRONTIER_REPORT_DIR:-$HOME/Documents/memory/tech/daily frontier report}/reported_items.jsonl`

Secondary lookup source:

- archived Markdown reports in the resolved report directory

1. URL deduplication
   - If the exact URL was already sent and there is no new technical delta, remove it.
   - If the exact URL now has a new technical delta, keep it and mark the previous recommendation date.

2. Canonical item deduplication
   - If the same paper, GitHub repo, benchmark, product technical release, or official blog post was already sent, remove it unless there is a new technical delta.
   - If kept, record when it was previously recommended and what changed this time.

3. Semantic deduplication
   - If the title differs but the content is only a repost, summary, or commentary of an already reported item, remove it.

4. Technical progress exception
   - Keep the candidate only if it has a non-empty `novelty_delta`, such as:
     - new paper version
     - new release
     - new benchmark result
     - new official technical blog
     - new open-source code
     - new architecture detail
     - new empirical result

Each kept candidate should have:

```yaml
canonical_key:
freshness_date:
freshness_evidence:
novelty_delta:
previous_recommended_at:
previous_report_path:
duplicate_decision: allow
```

Each removed candidate should have:

```yaml
canonical_key:
duplicate_decision: reject
duplicate_reason:
```

### 5. Score

Score only deduplicated candidates:

- Technical relevance: 0-5
- Technical novelty: 0-5
- Engineering usefulness: 0-5
- Friday relevance: 0-5
- Impact potential: 0-5

Prefer items that can inform Friday's agent, memory, recipe, artifact, eval, enterprise workflow, or private deployment roadmap.

### 6. Deep Dive

Deep-read only the top 5-10 candidates.

Extract:

- Core technical idea
- Why it matters
- Evidence URL
- Paper/repo/demo/benchmark availability
- Friday / PreSeen implication
- Whether it should be tracked long term

If the original source is unclear, search for official docs, paper, repo, benchmark, or first-party technical blog.

### 7. Local Context Match

For every deep-dived candidate, search local meeting notes and project documents before generating the recommendation.

Recommended query strategy:

1. Extract the candidate's core concepts, such as `agent memory`, `long-running agent`, `eval benchmark`, `world model`, `private deployment`, `graph memory`, `RLHF`, or `data attribution`.
2. Search local context for those concepts and adjacent internal project terms:
   - Friday / Memory / Recipe / Artifact / Task / Agent runtime
   - StarBench / eval / benchmark / VLM reasoning
   - Hyperion / Walmart / persona / private AI decision engine
   - MorningStar / data loop / dynamic training
   - autonomous driving / LiDAR / BEV / world model / synthetic data
3. Prefer graphify for relationship questions. Use `rg` for direct evidence lookup.
4. Identify the strongest internal connection:
   - Which person or team should care?
   - Which meeting already raised a related problem?
   - Which current task, decision, test, or implementation could this inform?
   - Which internal project or company strategy would benefit? Use this only as fallback.
   - What product or architecture decision could this inform?

Create this record before synthesis:

```yaml
canonical_key:
external_title:
external_url:
freshness_date:
freshness_evidence:
previous_recommended_at:
novelty_delta:
internal_link:
local_evidence:
recommendation_reason:
confidence: high|medium|low
```

Reject candidates with `confidence: low` unless the technical item is unusually important and the report explicitly states the internal connection is tentative.

### 8. Synthesis

Generate the final report in this format:

```markdown
## 每日前沿技术洞察

### Agent / Memory
- **技术点或项目名**：一句话说明技术突破；优先写关联人物或会议，再说明推荐理由。[来源](url)

### Eval / Trustworthy AI
- **技术点或项目名**：一句话说明技术价值；优先写关联人物或会议问题，再说明推荐理由。[来源](url)
```

If an item or canonical technology was recommended before but is allowed because of a new technical delta, mention that explicitly in the same bullet:

```markdown
- **项目名**：此前在 YYYY-MM-DD 推荐过；本次增量是新 release / 新 benchmark / 新论文版本 / 新架构细节。荐因优先写对哪个人或哪次会议问题有帮助；项目/战略只作 fallback。[来源](url)
```

Rules:

- Chinese
- Each item should be at most 150 Chinese characters and 100 English words, excluding URLs
- Maximum 8 items
- Every item includes a Markdown URL
- Every item is based on a verifiably fresh update from the last 72 hours
- Every item states the internal connection and recommendation reason
- Use category headings only when there are items under them
- No filler
- No "以下是"
- No process notes
- Do not include local file paths in the DingTalk-facing report unless the user explicitly asks; use local evidence for reasoning and memory writeback

### 9. Archive Report

Before sending to DingTalk, write two files:

1. Full local archive:
   `${FRONTIER_REPORT_DIR:-$HOME/Documents/memory/tech/daily frontier report}/YYYY-MM-DD-daily-frontier-report.md`

2. DingTalk-facing text only:
   `${FRONTIER_REPORT_DIR:-$HOME/Documents/memory/tech/daily frontier report}/YYYY-MM-DD-daily-frontier-report-dingtalk.md`

The full local archive must contain:

```markdown
# 每日前沿技术洞察 YYYY-MM-DD

## 趋势/热度分析
<based on historical reports and current candidate pool>

## 候选池总览
| Rank | Decision | Score | Title | Channel | Freshness | Dedup | Best local link | Comment |

## 候选详情
### 1. <Title>
- Decision:
- Score:
  - freshness:
  - technical_depth:
  - frontier:
  - local_relevance:
  - actionability:
  - novelty_dedup:
  - signal_heat:
- URL:
- Channel:
- Freshness evidence:
- Content summary:
- Technical novelty / delta:
- Dedup / previous recommendation:
- Local relevance evidence:
- Recommendation reason:
- Comments:

## 钉钉推送正文
<exact content of the -dingtalk.md file>
```

The DingTalk-facing file must be exact sendable Markdown only. Send this file, not the full archive.

Track sent-item metadata only in `reported_items.jsonl` after a successful DingTalk send.

### 10. DingTalk Send

Send the final report to the DingTalk group robot only after the report passes validation.

Use `scripts/send_dingtalk_markdown.py`.

Security:

- Read webhook and secret from the skill-scoped config file:
  `$HOME/.agents/skills/daily-frontier-tech-discovery/config/config.json`
- The config file must be local-only and mode `600`.
- Create it from `config/config.example.json`; the repository and sync scripts exclude `config.json`.
- Do not copy credentials into reports, automation prompts, logs, history files, or error summaries.
- If the config file is missing or incomplete, produce the report and explain that sending was skipped.

Message format:

- `msgtype`: `markdown`
- `title`: `每日前沿技术洞察`
- `text`: full Markdown report

Only after a successful send, update reported-item history.

### 11. Memory Writeback

After successful send, update the history store with:

```yaml
reported_items:
  - canonical_key:
    title:
    url:
    first_reported_at:
    last_reported_at:
    report_path:
    category:
    summary:
    internal_link:
    local_evidence:
    recommendation_reason:
    novelty_history:
      - date:
        novelty_delta:
        url:
```

If Friday memory tools are available, write this as memory. Otherwise, append to a local history file chosen by the user or the current project convention.
Always append successfully sent items to:

`${FRONTIER_REPORT_DIR:-$HOME/Documents/memory/tech/daily frontier report}/reported_items.jsonl`

## Local Script

Use the bundled sender:

```bash
python scripts/send_dingtalk_markdown.py --title "每日前沿技术洞察" --text-file report.md
```

Dry-run validation:

```bash
python scripts/send_dingtalk_markdown.py --title "每日前沿技术洞察" --text-file report.md --dry-run
```
