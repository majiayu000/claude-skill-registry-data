---
name: writing
description: >-
  Draft or revise a technical blog post, paper, tutorial, changelog, X thread, Reddit, Xiaohongshu
  or WeChat piece. When adapting release notes or other material for a new readership, find the
  point worth publishing, follow the channel's conventions and remove stock AI phrasing. Not for
  contract-bound-deliverables.
metadata:
  revision: "8"
  areas: "work-management,self-management"
  targets: "runtime-agnostic"
  summary: "draft and verify publishable prose for its audience and channel; use style measurements as diagnostics, not quotas"
  summary_zh: "按读者与渠道撰写和核验可发布文章；风格指标用于诊断，不作统一配额"
  kind: "entry"
---


# Writing for publication

Start with the reader's question and the point the piece can support. Ask once about destination
and audience when choosing the wrong form would change the draft. The publication's current
requirements and the user's editorial brief take precedence over these defaults.

| Destination | Read |
|---|---|
| Technical blog | [Blog](references/blog.md) |
| Academic paper | [Academic](references/academic.md) |
| X post or thread | [X](references/x-thread.md) |
| Reddit post | [Reddit](references/reddit.md) |
| Xiaohongshu | [Xiaohongshu](references/xiaohongshu.md) |
| WeChat Official Account | [WeChat](references/wechat-mp.md) |
| Tutorial or docs | [Tutorial](references/tutorial.md) |
| Changelog or release notes | [Changelog](references/changelog.md) |
| Story-led learning notes | [A Little Book](references/a-little-book.md) |

1. **Find the substance.** Identify what the reader will learn, decide, or be able to do. Anchor
   it in actual observations, a worked example, an executable step, or a defensible comparison.
   Flag thin material before polishing it. Split independent claims when each earns its own
   piece. Test candidate titles against the passages that deliver their promise.
2. **Choose the rewrite input.** For restructuring, use the old draft as a fact lead and keep
   what works. For a fresh draft, withhold the old prose; supply verified facts, exact quotes or
   code, and a new outline. Review unexpected reuse rather than enforcing overlap percentages.
3. **Verify facts.** Recheck inherited numbers, quotations, links, and claims against original
   records. Resolve gaps or mark them honestly. Treat operational metrics as evidence only when
   they help the reader. Use `uv run scripts/fact_check.py <draft.md> --corpus <source>` to surface
   untraced numbers; inspect matches for meaning, not just string equality.
4. **Read for voice and meaning.** Cut stock introductions, empty emphasis, repeated rhetorical
   moves, and certainty the material cannot support. Keep the author's useful vocabulary and
   the genre's necessary structure. When style intent is unclear, ask what the author wants the
   passage to do before rewriting it. Sentence length, repetition, and reuse are diagnostics,
   not universal limits; obey only limits in the brief or verified platform requirements.
   When revising an existing draft or checking it for AI phrasing, use
   [AI tells](references/ai-tells.md) for false positives, protected spans and edit scope.
5. **Deliver.** Use the requested language and publication format. For long pieces, put the
   draft in the task workspace and give its path. Publication is a separate authorized action.

For measured style comparison, use [style benchmarking](references/style-benchmarking.md).
For optional Chinese draft diagnostics and a site publication checklist, see
[blog editing](references/blog.md).
Only if a script command fails (for example `uv` is not found), read
[references/troubleshooting.md](references/troubleshooting.md).
