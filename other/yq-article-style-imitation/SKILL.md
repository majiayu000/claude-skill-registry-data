---
name: yq-article-style-imitation
description: Use when asked to study any writer or author, imitate article style, directly mimic a living or historical writer's prose style when requested, revise an imitation draft, or adapt Chinese articles for WeChat or Xiaohongshu.
---

# YQ Article Style Imitation

## Core Principle

Build a reusable article-writing skill, not a project agent. The skill's job is:

1. collect reference writing,
2. deconstruct the writer's expression DNA,
3. draft or repair an imitation article,
4. adapt the repaired draft for WeChat or Xiaohongshu.

Do not let evidence-register language, risk-gate language, or workflow labels leak into the article.
Do not draft from vibe memory, author profiles, interviews about the author, book pages, encyclopedia pages, or generic genre labels.
Do not treat search results as sources. A result becomes a source only after the page is opened, readable text is available, and the usable text is saved or otherwise recorded in the run.

When the user explicitly requests direct style imitation, use direct imitation mode for any named writer or author. The target can be living, historical, Chinese, non-Chinese, professional, literary, journalistic, online-native, or self-provided. Chai Jing, Mao Ni, and He Caitou are examples, not limits.

Borrowing from the Nuwa-style distillation pattern, treat the task as "distill how this writer writes," not "repeat what this writer said." Extract the writer's observable expression DNA: narrative mechanics, tonal temperature, paragraph rhythm, sentence functions, question movement, evidence handling, judgment timing, image system, humor or restraint, and ending shape.

Do not downgrade direct imitation into generic "mechanism transfer" unless the user asks for mechanism transfer. The boundaries below prevent plagiarism, false attribution, and process leakage; they are not a ban on direct style imitation.

If older project artifacts conflict with this skill, treat only those lower-priority artifacts as stale. Current system, developer, platform, legal, and user instructions always take precedence; this skill must never reclassify a higher-priority rule as stale. Within those boundaries, direct imitation is allowed when the user explicitly requests it.

## Required Workflow

1. **Source fetch log**: search, open, and record candidate pages before they enter the corpus. Mark inaccessible, 404, login-blocked, snippet-only, or off-target pages as rejected.
2. **Reference corpus**: collect title, author, URL/source, date, source role, source grade, access status, text availability, local text path, authorship evidence, accepted use, and selection reason. Keep URLs in the corpus only.
3. **Author-source validity gate**: before style teardown, prove that each primary style source is readable text written by the target writer. If there are not enough author-written primary sources, stop and report the source gap instead of drafting.
4. **Style-source / fact-source separation**: style sources do not need to match the article topic. Fact sources must support the topic's claims. Do not reject a valid target-writer text because it is about a different topic.
5. **Expression-DNA teardown**: analyze opening, scene density, paragraph rhythm, sentence functions, question movement, image system, humor/restraint, evidence handling, judgment timing, ending, and taboo patterns. Every style claim must cite valid primary source IDs and the local text used.
6. **Evidence ledger**: collect facts, sources, uncertainty, and verification paths. Keep links and formal labels here.
7. **Mode selection gate**: default to essay, commentary, reflective narrative, or other form implied by the reference sources. Use documentary reportage or pseudo-documentary/literary reportage only when the user asks for it or provides interview/case material.
8. **Evidence-to-prose translation**: turn evidence into natural narrative sentences before drafting.
9. **Imitation draft**: write in the requested reference style. If the user named a writer and asked to imitate, directly imitate that writer's style, including for living writers. Use new facts and new wording.
10. **Point-of-view continuity gate**: keep the article inside the subject's world; do not switch into "how to write/investigate this article" meta-commentary.
11. **Imitation repair gate**: check the draft for source leakage, AI/report language, fake interviews, meta-writing leakage, style decay, and weak ending.
12. **Platform pattern check**: before WeChat/Xiaohongshu adaptation, read `references/platform-patterns.md` and identify what evidence level supports the platform rules being used.
13. **Platform adaptation**: only after the imitation draft passes the repair gate and platform pattern check, adapt to WeChat and/or Xiaohongshu.
14. **Independent review swarm**: before release, spawn independent reviewer agents. The drafting agent cannot approve its own source quality, style fidelity, or publication readiness.
15. **Final release audit**: run the review artifact validator. If any independent reviewer returns `REVISE` or `BLOCK`, stop, repair the run package, and repeat the relevant review.

## Independent Review Swarm

Use Nuwa's review pattern: Python scripts catch mechanical failures; independent agents catch judgment failures. Do not replace reviewer agents with the drafting agent's own checklist.

Before publishing or platform adaptation, create `reviews/` inside the run directory and ask independent agents to write separate review files. Give each reviewer only the run package and the criteria below, not the drafting conversation. If subagent tooling is unavailable, run separate zero-context review passes and save their outputs in the same files.

Required reviewers:

| Reviewer | Output file | Review focus | Must inspect |
|---|---|---|---|
| Source auditor | `reviews/01-source-audit.md` | Whether accepted style sources are author-written, readable, substantial, and correctly graded | `source-fetch-log.md`, `style-reference-corpus.md`, `raw-sources/` |
| Style auditor | `reviews/02-style-audit.md` | Whether the teardown actually supports the draft, and whether the draft decays into generic reportage, AI language, or platform copy | `style-mechanism-breakdown.md`, `imitation-draft.md`, accepted raw sources |
| Fact auditor | `reviews/03-fact-audit.md` | Whether factual claims in the draft are supported, overclaimed, or missing uncertainty | `evidence-ledger.md`, `imitation-draft.md` |
| Platform auditor | `reviews/04-platform-audit.md` | Required only when WeChat/Xiaohongshu drafts exist; checks platform adaptation against sourced platform patterns rather than generic memory | `references/platform-patterns.md`, platform drafts, platform notes |

Each review file must include:

- `reviewer_role`: one of `source-auditor`, `style-auditor`, `fact-auditor`, `platform-auditor`
- `verdict`: `PASS`, `REVISE`, or `BLOCK`
- `checked_files`: concrete files inspected
- `critical_findings`: concrete issues or `none`
- `required_changes`: exact changes required before release, or `none`
- `independence_note`: confirm this was a separate review pass, not approval by the drafting agent

Reviewer standards:

- `PASS`: no blocking issue; minor notes may remain.
- `REVISE`: article can be repaired without rebuilding the corpus.
- `BLOCK`: source corpus, teardown, evidence base, or platform basis is invalid; drafting must stop until the upstream package is fixed.

The main agent must summarize reviewer disagreements and resolve them by evidence, not by majority vote. One `BLOCK` is enough to stop release.

## Author-Source Validity Gate

Direct imitation requires primary style sources. A primary style source is a complete or substantial text written by the target writer: article, essay, column, book excerpt, novel chapter, speech transcript authored by the writer, or an authorized/reposted text with a clear byline and provenance.

These may support background only, never style imitation:

- encyclopedia pages, author profiles, book pages, bibliography pages;
- news reports about the writer;
- interviews where the writer is the subject but not the author;
- reviews, summaries, biographies, introductions, or platform metadata;
- short quotes detached from the surrounding article.

For each target writer, collect at least two primary style sources before drafting unless the user explicitly approves a smaller corpus. If no valid primary style source is available, stop with a source-gap note. Do not fill the gap with "reportage style," "novel style," or memory of the writer.

Reposts can be valid style sources. Do not reject a page merely because it is hosted by a third-party site such as a medical, media, blog, or archive site. Judge it by access, readable text, byline/provenance, and whether the text itself is substantial.

Use source grades:

- `A`: first-party source, official archive, official account, or formal publication excerpt.
- `B`: third-party repost with clear byline/provenance and readable substantial text.
- `C`: search result, snippet-only page, unstable page, unclear byline, or incomplete text.
- `D`: background-only page such as encyclopedia, author profile, book metadata, interview about the writer, review, or summary.

Only `A` and `B` can be accepted for style. `C` and `D` can never justify style teardown.

Corpus rows must include:

- `source_id`
- `target_writer`
- `role`: `primary-style-source` or `background-only`
- `source_grade`: `A`, `B`, `C`, or `D`
- `access_status`: `ok`, `blocked`, `404`, `login-required`, `snippet-only`, or equivalent
- `text_available`: `yes` or `no`
- `local_text_path`: path to the saved readable text used for teardown
- title
- byline / author
- URL or local path
- date if available
- authorship evidence
- `accepted_for`: `style`, `background`, `fact`, or `rejected`
- why selected
- what style behavior it can teach

If a source is reposted, state why the authorship is still credible. If authorship is unclear, mark it `background-only`.

## Teardown Traceability Gate

Do not write generic teardown bullets such as "纪实观察向" or "长篇叙事向" unless each point is anchored to primary source IDs.

Every style observation must name:

- the supported behavior;
- the source IDs supporting it;
- where it appears in the text: opening, transition, paragraph rhythm, evidence move, judgment timing, or ending;
- one taboo: what not to copy or overdo.

If the teardown cannot point back to author-written texts, the imitation draft is not allowed.

Before drafting, run:

```powershell
python "<skill>/scripts/validate_style_run.py" <run-directory> --target-writer <writer-name>
```

Fix any failures before writing the imitation draft.
Then run the source auditor. Do not let the drafting agent certify its own corpus.

## Form And Interview Mode

A writer's style is not synonymous with one genre. Many writers work across essays, columns, talks, interviews, fiction, newsletters, posts, book chapters, and reportage. Match the form implied by the selected primary sources and the user's request.

Default:

- If the user asks only for "仿[某作家]文风", do not assume first-person reportage, fiction, commentary, or any other single genre.
- Do not invent real interviews, real observed scenes, or first-person reporting claims.
- Avoid lines like `我问他`, `他说`, `后来他告诉我`, or `他对我说` unless they come from user-provided case notes, real interviews, or explicit pseudo-documentary mode.

Allowed when explicit:

- If the user asks for `纪实`, use real interview/case/source material only.
- If the user asks for `伪纪实文学` or `伪纪实`, a composite fictional scene is allowed, but do not imply it is a real interview or real reported event.
- In pseudo-documentary mode, prefer third-person composite narration over fake first-person reporting.

## Hard Boundaries For Published Drafts

Article drafts must not contain:

- naked URLs, markdown links, or `来源:` inline source labels;
- workflow labels such as `已知事实`, `候选假设`, `验证路径`, `风险门`, `质量评分`;
- audit/report endings such as `这也是这篇文章目前能走到的边界`;
- generic AI phrases such as `根因`, `写死`, `清楚、可查、负责任`, `在患者的经验里`;
- meta-writing or investigation-method commentary such as `所以，写...`, `这篇文章`, `本文`, `如果要把它查清楚`, `不能从...这个大词开始`, `最危险的是`;
- fake interview/reportage signals such as `我问他`, `后来他告诉我`, or unsourced direct quotes when no interview/case source exists;
- a final section named `Safe Publication Notes`, `Quality Score`, or similar process metadata.

Keep these in companion files, not the publishable article:

- source URLs;
- fact labels;
- uncertainty notes;
- medical/legal/compliance caveats;
- quality scores;
- publishing risk notes.

## Evidence-To-Prose Rule

Evidence must enter the article as narration, not citation scaffolding.

Bad:

> 国家医保局说... 来源: https://...

Better:

> 后来我查到一段官方表述。它没有说医院不能再用原研药。它说的是，协议之外，医疗机构仍然可以选择非中选产品。

Bad:

> 已知事实是...

Better:

> 到这里，能确认的事情其实不多。政策不是一句话，医院也不是一个窗口。

## Point-Of-View Continuity Rule

The publishable article must stay inside the article's object-level world: people, scenes, institutions, products, decisions, and consequences.

Do not switch into the writer's backstage view:

- how to write this topic;
- how to investigate this topic;
- what this article can or cannot prove;
- what a reporter should verify next.

Bad:

> 所以，写"消失的进口药"，最危险的不是提出疑问。

Better:

> 可那个站在窗口前的人，并不是在问一个品类。他问的是这一盒药，今天为什么不在这里。

Bad:

> 如果要把它查清楚，不能从"进口药"这个大词开始。

Better:

> 问题一旦落到这一盒药上，就变小了，也变清楚了：哪一个药名，哪一个厂牌，哪一个规格，哪一家医院，哪一天。

Verification paths belong in the evidence ledger. In the article, turn them into scene-bound questions a person in the story would naturally ask.

## Imitation Repair Gate

Before platform adaptation, run:

```powershell
python "<skill>/scripts/lint_article_style.py" <article-draft.md>
```

If it reports issues, revise the imitation draft first. Do not proceed to WeChat/Xiaohongshu adaptation until the draft is clean or each issue is explicitly justified.

Then manually check:

- Does the first half and second half sound like the same writer?
- Did policy/data paragraphs remain narrative?
- Is the ending earned by the scene, not pasted from a report?
- Does the article hide its scaffolding?
- Does every paragraph stay inside the subject's world rather than explaining the author's writing or investigation method?

After this self-check, run the style auditor and fact auditor. The self-check is only a preparation step; it is not release approval.

For final release, run:

```powershell
python "<skill>/scripts/review_style_run.py" <run-directory>
```

If platform drafts are included, require platform review:

```powershell
python "<skill>/scripts/review_style_run.py" <run-directory> --require-platform-review
```

This script only validates that independent review artifacts exist and that no `REVISE` or `BLOCK` verdict remains. It cannot judge literary quality by itself; the independent reviewer agents do that work.

## Platform Adaptation

Read `references/platform-patterns.md` and `references/platform-adaptation.md` only after the imitation draft passes the repair gate.

If current platform examples or accessible source material are insufficient, state the source gap in the platform draft notes instead of inventing platform rules.

Default:

- WeChat: deeper, complete, restrained, credibility-first.
- Xiaohongshu: shorter, visual, scenario-led, still not traffic-style.

## References

- `references/style-workflow.md`: detailed collection, teardown, drafting, and repair workflow.
- `references/platform-patterns.md`: evidence-backed platform differences and source caveats.
- `references/platform-adaptation.md`: WeChat and Xiaohongshu conversion rules.
- `scripts/validate_style_run.py`: mechanical check for separate output files, source access fields, local source text, valid primary author-written sources, source-ID traceability, and fake interview signals.
- `scripts/lint_article_style.py`: mechanical scan for URLs and AI/report-language leakage.
- `scripts/review_style_run.py`: mechanical check that independent source, style, fact, and optional platform reviews exist, use explicit verdicts, and contain no unresolved release blockers.
