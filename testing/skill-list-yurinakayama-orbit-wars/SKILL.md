---
name: skill-list
description: Lists all Claude skills currently available in this repository and in the user's global skill directory, grouped by domain. Use this skill whenever the user asks things like "what skills can you use", "show me the available skills", "skill list", "list skills", "使えるスキルを教えて", "どんなスキルがある", "skill 一覧", or wants to narrow the list down to a specific area or purpose (e.g. "research", "python", "テスト", "デプロイ"). This skill accepts an optional filter argument (a domain name, keyword, or purpose) and returns only the skills whose name or description matches.
---

# skill-list

A discovery skill that enumerates locally installed Claude skills and presents them to the user, grouped by domain. It reads `name` and `description` from each `SKILL.md` frontmatter at invocation time, so the list is always up to date.

All user-facing output MUST be in Japanese, matching the convention of other skills in this repository. Internal reasoning stays in English.

## Execution steps

### 1. Collect skills

Scan the following directories for `*/SKILL.md` (silently skip any that do not exist):

- `.claude/skills/` — project-local skills for the current repo
- `~/.claude/skills/` — user-global skills

Use Glob to enumerate candidates, then Read the first ~20 lines of each `SKILL.md` to extract the YAML frontmatter. Only the `name` and `description` fields are needed. Batch the reads in parallel when there are many files.

If a skill also appears in the Skill tool's runtime list (provided by the harness in the system prompt), prefer that runtime list as the source of truth for what is actually invocable, and use the filesystem scan to enrich descriptions or catch skills the runtime list truncated. When both are available, deduplicate by skill name.

### 2. Classify by domain

Assign each skill to a category based on keywords in its name and description. Categories are not fixed — adapt them to the actual set of skills present, but keep the "grouped by domain" intent intact. A skill that does not clearly fit anywhere goes into **その他 (Other)**.

Suggested categories:

- **Research / 調査** — `research-*`, `find-skills`, and anything focused on information gathering
- **Python** — `python-*`, Python-flavored TDD, etc.
- **Frontend / Web** — `typescript-*`, `playwright`, `web-design-*`, `vercel-*`, frontend/UI design skills
- **Testing / QA** — `tdd`, `e2e-*`, `test-*`, `eval-*`, `verify`, `playwright`
- **Code Quality / Review** — `code-review`, `*-lint`, `*-review`, `simplify`, `remove-unused`
- **Git / Release / CI-CD** — `pr`, `release-*`, `ci-*`, `deploy`, `checkpoint`
- **Planning / Docs** — `plan`, `feature-plan`, `update-docs`, `update-codemaps`, `orchestrate`
- **Skill / Meta / Learning** — `skill-creator`, `find-skills`, `list-skills`, `learn`, `instinct-*`, `update-config`, `keybindings-help`
- **Automation / Scheduling** — `loop`, `schedule`
- **その他 (Other)**

A single skill should appear in only one category; pick the most specific fit.

### 3. Apply the optional filter argument

When the user invokes this skill with an argument (a domain, keyword, or purpose — e.g. `python`, `research`, `テスト`, `デプロイ`), filter to skills whose name or description contains the argument, case-insensitively.

If the argument is Japanese, expand it to semantically related English keywords before matching, because most skill metadata is in English. Rough mappings:

- 「テスト」「試験」 → `test`, `tdd`, `e2e`, `coverage`, `playwright`, `verify`
- 「デプロイ」「リリース」 → `deploy`, `release`, `ci`, `cd`
- 「調査」「リサーチ」 → `research`, `gather`, `retrieval`, `cluster`
- 「計画」「設計」 → `plan`, `feature`, `design`, `orchestrate`
- 「レビュー」 → `review`, `lint`, `quality`
- 「ドキュメント」 → `docs`, `codemap`, `readme`
- 「スキル」 → `skill`, `instinct`, `learn`

Feel free to extend this mapping based on context. If a match against the original argument succeeds, do not discard it — union the original-match and the expanded-match result sets.

If the filter yields zero results, tell the user so in Japanese, then show the full unfiltered list as a fallback so they can pick another keyword.

### 4. Output format (Japanese, table-based)

Render the result in Japanese Markdown using **one Markdown table per category**. Each category becomes an `##` heading followed by a table with these columns:

| Skill | 概要 | Scope |
| --- | --- | --- |

- **Skill** — skill name wrapped in backticks (e.g. `` `python-tdd` ``) for easy copy-paste.
- **概要** — a one-line Japanese summary derived from the English `description`. Translate/condense as needed. Keep it on a single line; truncate with `…` if it would otherwise be unreadably long (target ~60–90 characters).
- **Scope** — `project` or `global`. Omit this column entirely (header and cells) when all listed skills come from the same scope, to avoid visual noise.

Escape or replace any `|` characters inside descriptions so they do not break the table.

Template (scope column shown; drop it when not needed):

```
# 使用可能な Skill 一覧 [— フィルタ: "<arg>"]

合計: N 件

## Research / 調査

| Skill | 概要 | Scope |
| --- | --- | --- |
| `research-clustering` | リサーチ領域をクラスタリングして構造化する | project |
| `research-gather` | 指定ドメインの論文・特許・Web 情報などを収集する | project |

## Python

| Skill | 概要 | Scope |
| --- | --- | --- |
| `python-tdd` | Python の TDD ワークフロー（pytest → 実装 → カバレッジ確認） | project |
```

Close with one short line in Japanese inviting the user to ask for details on any specific skill, e.g. 「特定の skill の詳細を知りたい場合はスキル名を教えてください。」 Also mention that `list-skills <キーワード>` can be used to filter.

## Design notes (why this shape)

- **Dynamic scan, not a hardcoded list.** Skills are added and removed frequently. Embedding a static list inside this skill would rot immediately. Reading the filesystem at call time is the only reliable source.
- **Frontmatter only.** Using just `name` and `description` keeps the output compact and stable, and avoids pulling large SKILL.md bodies into context for a listing task.
- **Flexible categories.** Categorization rules are keyword-based rather than an exhaustive enum, so new skills slot in without requiring edits to this SKILL.md.
- **Filter fallback.** Showing the full list when a filter returns zero results turns a dead end into a useful menu, which is the real intent behind the filter argument anyway.
