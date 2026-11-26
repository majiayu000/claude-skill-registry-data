---
name: company-intel
description: Build or load a cached prep brief for a specific target company covering its interview process and rounds, OA format, the LeetCode questions and topics most frequently reported for it (recent and all-time), what its resume screen values, its stated values or leadership principles, and system design and HR focus. Every cracked skill uses this when the candidate names a company. Use when the user says they're preparing for a specific company ("I have a Google interview", "prep me for Amazon", "Flipkart OA next week"), asks what a company asks, or wants company-wise questions.
---

# Company intel

When a candidate names a company, every cracked skill gets sharper: the OA uses that company's reported questions, the HR round asks about its values, and the resume roast checks against its bar. This skill builds that knowledge **once**, caches it, and hands it to whichever skill asked.

**No company named? Don't ask.** Skills work fine without one: a generic product-company style is the default. Only build a brief when the user names a company or the profile's `target_companies` lists one and the calling skill wants it.

## 0. Load or build

1. Call the Skill tool with "cracked-profile".
2. Normalise the company name (e.g. "goog" → "Google"), then read `$CRACKED_DIR/companies/<company-slug>.md`.
   - If it exists and its `updated:` date is under 30 days old, use it. Say one line ("Loaded Google brief, updated 2026-10-30") and hand back.
   - If it's older, or missing, build it (below). If the calling skill only needs questions, you can do just §1.

## 1. Reported questions (always, if online)

Run the bundled script. It fetches the community-maintained company-wise LeetCode dataset ([liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems), 470+ companies, frequency-ranked) and caches it in `$CRACKED_DIR/cache/`. Every output ends with a freshness line (`cached <date> · dataset last updated upstream <date>`): quote it, and if the upstream date is more than ~3 months old, tell the user the data may be stale.

```bash
python3 <this-skill-dir>/scripts/questions.py list <query>                 # find the exact company name
python3 <this-skill-dir>/scripts/questions.py topics "<Company>"            # topic + difficulty mix (last 6 months)
python3 <this-skill-dir>/scripts/questions.py get "<Company>" --window 3m --limit 30
python3 <this-skill-dir>/scripts/questions.py get "<Company>" --difficulty medium,hard --topic graph
```

`<this-skill-dir>` is this skill's base directory (most harnesses print it when the skill loads). If you can't see it, locate the script with:
`find ~/.claude ~/.codex ~/.agents ~/.cursor ~/.gemini ~/.config "$PWD" -path '*company-intel/scripts/questions.py' 2>/dev/null | head -1`.
Other skills that need questions use the same script path. Tell them the absolute path when you hand back.

Windows: `30d`, `3m`, `6m` (default), `older`, `all`. Use `--format json` when another skill needs to pick problems programmatically.

- Names match case- and punctuation-insensitively, with aliases for common long forms ("Tata Consultancy Services" → `tcs`, "Facebook" → Meta, "AWS" → Amazon). If there's still no match, it suggests close names: confirm with the user.
- An empty window widens automatically (30d → 3m → 6m → all) and prints `window widened from X to Y`. Say which window you actually used.
- If you hit GitHub's rate limit on a shared network, set `GITHUB_TOKEN`.
- If the company isn't in the dataset (common for small startups, and for some service companies), say so, then fall back to the closest archetype in [ARCHETYPES.md](ARCHETYPES.md).
- If you're offline, use the cache. If there's no cache, use the archetype and say so.
- **Provenance**: always label these as "frequently reported by candidates (community dataset)", never as the company's official or leaked question bank.

## 2. Process, values and resume bar (web, if available)

If you have a web search or fetch tool, research these from **public** sources, and keep each source's URL:
- The official careers page and "how we hire" or interview-prep pages. Many large companies publish them.
- Public interview experiences: LeetCode Discuss (company tag), GeeksforGeeks interview experiences, Glassdoor interview reviews, Reddit (r/cscareerquestions, r/developersIndia), and company engineering blogs.
- The company's published values or leadership principles (for example, Amazon publishes its Leadership Principles).

Extract: the round sequence (OA → technical × N → system design → HR or hiring manager), OA platform, duration and question count, interview language rules, what's emphasised, recent changes (dated), and the role and level the experiences refer to. Prefer the last 12 months. Note conflicts between sources rather than picking one silently.

**If you have no web tool**: say so, fill §2 from the archetype, and mark it `unverified: no web access`. Never present general knowledge as current fact. Hiring processes change.

## 3. Write the brief

Save `$CRACKED_DIR/companies/<company-slug>.md` in this shape. Keep it under ~120 lines, since other skills read it:

```markdown
# <Company> prep brief
updated: <YYYY-MM-DD> · role focus: <e.g. SDE-1 / new grad> · archetype: <from ARCHETYPES.md>

## Process (reported)
1. <round> · <format> · <duration> · <what's assessed>
…
Sources: <urls>

## OA
<platform, count, difficulty mix, time, language rules, typical topics>

## DSA focus (community dataset, window: <w>)
Difficulty mix: …
Top topics: …
Top 15 recent questions: | Difficulty | Title | Topics | Link |

## System design
<expected at this level? HLD or LLD? typical prompts reported>

## Values / behavioral
<published values or principles, and the behavioral themes interviewers probe>

## Resume screen
<what this company's screen is reported or known to value; must-have keywords for the role>

## Gotchas
<e.g. "bar raiser round", "no IDE, shared doc only", "CGPA cutoff reported for campus drives">
```

## 4. Hand back

Give the calling skill (and the user) a 3–5 line summary: process, top 5 topics, the OA shape, and one gotcha. Then continue with the calling skill. If the user invoked this directly, offer next steps: `/oa-sim <company>`, `/mock-interview <company>`, `/resume-blueprint <company>`, `/hr-round <company>`.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
