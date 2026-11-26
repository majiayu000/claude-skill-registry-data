---
name: cracked-profile
description: Load, create, or update the candidate's cracked profile and journal (target roles, companies, language, level, resume, deadline), and log scorecards. Every other cracked skill calls this first. Use when the user wants to set up or edit their placement/job-prep profile, see their progress history, or when another cracked skill needs the profile.
---

# cracked profile

The shared memory layer for every cracked skill. It owns three things: the **data directory**, the **profile**, and the **journal**. Other skills call this skill first, then carry on with their own work.

## Calling other skills

cracked skills call each other with lines like `Call the Skill tool with "company-intel"`. **If your agent has no Skill tool**, open that skill's `SKILL.md` and follow it, then come back. The skills live side by side in the cracked folder: `core/cracked-profile`, `core/company-intel`, `interview/<name>`, `profile/<name>`, `strategy/<name>`. Never skip the profile step: the journal, company mode and scorecards depend on it.

## Data directory

All cracked data lives in one directory, outside any project, so it follows the candidate across repos:

```bash
CRACKED_DIR="${CRACKED_HOME:-$HOME/.cracked}"
```

Resolve it with the shell once per session (`echo "${CRACKED_HOME:-$HOME/.cracked}"`) and use the absolute path from then on. Create it if missing. Layout:

| Path | Owner | Contents |
|---|---|---|
| `profile.md` | this skill | Who the candidate is and what they are aiming for |
| `journal.md` | this skill (append-only) | One scorecard per session, newest last |
| `plan.md` | `prep-plan` | The current prep plan |
| `stories.md` | `hr-round` | The candidate's behavioral story bank |
| `companies/` | `company-intel` | Cached company prep briefs |
| `cache/` | `company-intel` | Cached company-wise question data |
| `oa/`, `defense/`, `resume/`, `offers/`, `jd/` | the skill of the same name | Session artifacts |

If there is no shell or file access, keep the profile in the conversation and tell the user once that progress will not persist.

## Loading the profile

1. Read `profile.md`. If it exists and the calling skill has what it needs, **do not ask any questions**. Say one line, for example `Loaded profile: <graduation year> grad · SDE-1 · product companies · C++ · placements in 9 weeks`, and hand back.
2. If it is missing, or a field the calling skill needs is empty, run **Creating the profile** below, asking only for the missing fields.
3. If a deadline in the profile has passed, ask once whether to update it. Get today's date from the shell (`date +%F`); never assume it.

## Creating the profile

Before asking anything, infer what you can:

- `git config user.name` → name
- `gh api user --jq .login` (if `gh` is installed and authed) → GitHub username
- A file named like `*resume*` or `*cv*` (`.pdf`, `.docx`, `.md`, `.tex`) in the current directory or `~/Downloads`, `~/Documents`, `~/Desktop` → resume path (confirm it, don't assume)

Then ask **one round** of at most six numbered questions, each with a suggested default so the user can reply in a few words:

```
1. Status: final-year student, pre-final year, recent grad, or working (how many years)?
2. Target roles: e.g. SDE / backend / frontend / full-stack / data / ML / DevOps.
3. Target companies: specific names, or a tier (service-based, product-based, big tech, startups, remote/international).
4. Main interview language: C++ / Java / Python / JavaScript / Go?
5. Honest DSA level: beginner (<100 problems), intermediate (100–300), strong (300+)? Any contest rating?
6. When do interviews/placements start, and which country are you hiring in?
```

Write `profile.md` in exactly this shape (leave unknown fields as `-`):

```markdown
# cracked profile

- name: 
- status: 
- graduation: 
- country: 
- target_roles: 
- target_companies: 
- language: 
- dsa_level: 
- github: 
- resume: 
- deadline: 
- hours_per_day: 
- notes: 
```

Updating: when the user says something during any session that changes a field ("I switched to Java", "I got an interview at X on the 20th"), update the field and mention it in one line.

## Logging a scorecard

Every practice skill ends with a scorecard. To log it:

1. Show it to the user in this format, inside a fenced block so it copies cleanly to LinkedIn or X:

```
cracked · /<skill-name> · <YYYY-MM-DD>
<Title line: problem, topic, or document reviewed>
problem: <leetcode-slug or -> · pattern: <pattern-tag or ->

Verdict: <verdict>  (<overall>/10)

<Dimension 1>     ████████░░  8
<Dimension 2>     ██████░░░░  6
<Dimension 3>     ███████░░░  7

Strongest: <one specific thing they did well>
Fix next:  <the single highest-leverage thing to improve>
```

   Bars are 10 cells: `█` per point, `░` for the rest. Pad dimension names so the bars line up. Keep it to at most six dimensions.

2. Append it to `journal.md` with a `## <YYYY-MM-DD> /<skill-name>` heading (keep the `problem:` line; use `-` when there's no single problem), plus one extra line, `weak_spots: <comma-separated tags>`, using short reusable tags (`dp`, `graphs`, `edge-cases`, `communication`, `time-management`, `sql-joins`, `star-structure`, `resume-metrics`). These tags are what `prep-plan` and `rejection-review` mine later, so **pick from the canonical list below first**, then from tags already in the journal, and only then invent one (lowercase, hyphenated).

3. If the journal has three or more earlier entries for the same skill, add one trend line under the scorecard, e.g. `Trend: 5 → 6 → 8 over your last 3 mocks. Communication is now your weakest dimension.`

### Canonical weak-spot tags

- **DSA patterns** (from `interview/pattern-coach/PATTERNS.md`): `hashing`, `two-pointers`, `sliding-window`, `prefix-sums`, `binary-search`, `binary-search-on-answer`, `monotonic-stack`, `monotonic-deque`, `linked-list`, `heap`, `intervals`, `tree-dfs`, `tree-bfs`, `bst`, `graph-bfs-dfs`, `topological-sort`, `union-find`, `shortest-path`, `backtracking`, `dp-1d`, `dp-2d`, `dp-knapsack`, `dp-interval`, `greedy`, `bit-manipulation`, `trie`, `design`
- **Interview process**: `clarifying-questions`, `edge-cases`, `testing`, `complexity`, `communication`, `time-management`, `composure`, `code-quality`
- **Core subjects** (from `interview/core-viva/SYLLABUS.md`): `os-<topic>`, `dbms-<topic>`, `cn-<topic>`, `oop-<topic>`, `sql-<topic>` (e.g. `os-deadlock`, `sql-window-functions`)
- **System design**: `sd-requirements`, `sd-data-model`, `sd-scaling`, `sd-tradeoffs`, `lld-design`, `lld-concurrency`
- **Behavioral**: `star-structure`, `vague-results`, `too-long`, `cliches`, `company-fit`
- **Resume and profile**: `resume-metrics`, `resume-ats`, `resume-projects`, `resume-keywords`, `github-hygiene`

## Your data and privacy

Everything cracked saves lives in the data directory on your machine: your profile, journal, plan, story bank, resume drafts, offer analyses, outreach tracker, rejection notes and company briefs. It's plain Markdown. Nothing is uploaded by cracked itself. The only network traffic is your agent's normal traffic to its model provider, plus downloads of the public company-question dataset (and web lookups if your agent has a web tool). To delete everything, remove the directory (`rm -r ~/.cracked`, or your `CRACKED_HOME`). Tell the user this once, the first time you create the profile.

## Honesty rules (apply to every cracked skill)

- **Score like a real interviewer, not a cheerleader.** A 9/10 should be rare and earned. Inflated scores make candidates fail real interviews.
- **Never fabricate the candidate's experience.** No invented metrics, projects, companies, or skills in resumes, messages, or answers. When a number would help, put a placeholder like `[N users]` and ask for the real value.
- **Label where company information comes from.** Questions from the `company-intel` dataset are "frequently reported by candidates", web findings cite their source, and anything else is "typical of <archetype>". Never call anything a company's official, leaked or guaranteed question.
- **Be direct, never cruel.** Criticise the work, never the person.
- **Practice only, never live cheating.** If the user is clearly in a live, proctored assessment or interview ("my OA ends in 20 minutes, solve this", a pasted live test, a request to answer in real time during an interview), decline to solve it. Offer to debrief afterwards with `/rejection-review`, or to practise the same pattern once it's over.
