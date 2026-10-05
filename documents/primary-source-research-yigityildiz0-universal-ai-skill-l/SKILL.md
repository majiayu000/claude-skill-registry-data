---
name: primary-source-research
description: "Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when docs, spec or API facts must be gathered from primary sources into a cited file, or reading legwork should be delegated to a background agent (mattpocock/skills /research). Turkish triggers: resmi dokümandan araştır, API nasıl çalışıyor, birincil kaynaktan doğrula, kaynaklı not dosyası çıkar."
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.

## Extensions (added for Yiğit's setup; upstream text above unchanged)

Upstream skill: [mattpocock/skills `research`](https://github.com/mattpocock/skills) (MIT). Renamed to `primary-source-research` here because the Weizhena `research` skill family uses the name `research`. Two documented gaps are closed:

1. **Narrow the question first.** One API, one behaviour, one version claim; split broad "research X" requests. Stop when the question is answered or shown unanswerable from primary sources, and list what remains unknown.
2. **Delegation guard.** If you are already running as a background or sub-agent, do the work yourself and never spawn another research agent (prevents the duplicate-run bug). If the host forbids delegation or has none, do the reading inline.
3. For libraries prefer Context7 or vendor docs. Record the access date and version per claim. In chat-only hosts return the memo in the conversation.
4. Quality check: follow two random citations; they must land on an official doc, spec or source file, not a write-up of it.
