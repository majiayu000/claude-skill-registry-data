---
name: strict-triage
description: This skill should be used when triaging an inbound GitHub issue from a maintainer perspective — applying a 9-item checklist to decide a verdict (READY / NEEDS_INFO / DUP / CLOSE), surfacing classification disagreements with existing labels, and producing a draft response plus gh command suggestions. Parallel to strict-review but for issues, not code.
---

<!-- mkdocs-include-start -->

# Strict Triage

**Owner Agent**: Soyo (Reviewer)
**Consumers**: [`/maigo:triage-issue`](https://github.com/Lee-W/maigo/blob/main/commands/triage-issue.md) step 3

## Core stance: default NEEDS_INFO

**Verdict starts at NEEDS_INFO.** Maintainer time is the scarce resource.
An issue with missing info or unclear scope wastes the next contributor who
picks it up. "Looks reasonable at a glance" must not become "wasted three
contributors before we realized scope was wrong" — the checklist is the
guardrail.

These do **not** count as enough to upgrade to READY:

- "感覺像是 bug 吧" — without repro steps, you can't tell
- "之前有人問過類似的" — without the prior issue # linked, the next contributor will re-investigate
- "我猜作者意思是 X" — issue body is the source of truth; if it's ambiguous, ask

## The 9-item triage checklist

Every triage must walk through every item. Output explicitly marks `[x]` or `[ ]` per item.

1. **Specific title** — Title points at a concrete behaviour or feature, not "doesn't work" / "請新增功能" / "壞了"
2. **Repro steps (bug only)** — If classified as bug: numbered or bulleted steps a maintainer can run. Skip with `[—]` if not bug.
3. **Expected vs actual (bug only)** — Both sides stated; "it crashes" without "what should have happened instead" doesn't count. Skip with `[—]` if not bug.
4. **Environment info (bug only)** — Version / OS / runtime / relevant config. Skip with `[—]` if not bug.
5. **No obvious duplicate** — Raana's grep / linked-issue scan did not surface a same-bug / same-request issue. If one was found, must reference its `#N`.
6. **In project scope** — Belongs in this repo, not an upstream dep / unrelated tool / fork-only concern.
7. **Has actionable next step** — A maintainer could write a 1-line response that moves it forward (ask X, label as Y, assign to Z, close as W). "Interesting thought" with no path forward fails this.
8. **Follows issue template** — If `.github/ISSUE_TEMPLATE/` exists in the repo, the relevant sections are filled. Missing template → `[ ]` and call out which sections are blank.
9. **Signal not buried** — Discussion / "+1" / "me too" comments do not overwhelm the original report. If they do, summarise the core in your draft response so future readers don't have to dig.

Any `[ ]` blocks READY — verdict downgrades to NEEDS_INFO / DUP / CLOSE per the table below.

## Classification (parallel to checklist, always required)

Tomori's triage rubric (`.maigo/issue/<id>/rubric.md`, one per issue) includes
a `## Category` line — one of
`bug` / `feature` / `question` / `documentation` / `other`. Soyo's output **always
echoes Tomori's classification** and adds a `disagreement` line if existing
GitHub labels point at a different category:

```
## Classification
- Tomori's call: bug
- Existing labels: [enhancement]
- Disagreement: ⚠️ labels say enhancement but body describes a regression after upgrade — recommend re-label as bug
```

If no existing labels → just print `- Existing labels: (none)`.
If Tomori's call matches labels → just print `- Aligned with existing labels` and move on.

Classification is **not** part of the 9-item checklist — it is an orthogonal
output axis. An issue can be `[x]` on all 9 items and still have a label
disagreement worth surfacing.

## Verdict semantics

| Verdict | When | Required output additions |
|---|---|---|
| **READY** | All 9 `[x]` (or `[—]` for items 2–4 if not bug) AND no classification disagreement | Suggested labels to **add** (good-first-issue if applicable); suggested assignee if you can infer one from CODEOWNERS or recent contributors |
| **NEEDS_INFO** | Items 1–4 partial | Specific bullet list of what's missing; **polite** draft asking for it (don't dump 9 questions — pick the 2–3 that unlock the rest) |
| **DUP** | Item 5 fails OR Tomori flagged a likely dup in rubric | Link the original `#N`; draft `close as duplicate of #N` with a one-line note on which one survives |
| **CLOSE** | Items 6 or 7 fail (out of scope / not actionable) | Draft close reason naming the specific item that failed; if `question` category, suggest moving to Discussions instead of close |

**Don't combine verdicts.** An issue cannot be "NEEDS_INFO and also a DUP" — pick the most actionable one (DUP wins, because asking for info is wasted work if the answer is "see #N").

## Draft response rules

- **One paragraph max.** Maintainer pastes this, doesn't edit it down.
- **Cite line numbers / sections of the issue body** so the author knows you read it.
- **No "thanks for filing!"** opening fluff. Skip straight to the substance.
- **End with a concrete ask or a concrete next step** — never an open question with no scaffolding.
- **Polite but not soft** — same stance as `strict-review`'s reviewer voice (calm, polite, doesn't retreat on the standard).

## gh command suggestions

For each verdict, provide one or more `gh` commands the maintainer can paste:

| Verdict | 建議操作 |
|---|---|
| READY | `gh issue edit <N> --add-label <X>`（每個 suggested label 一條） |
| NEEDS_INFO | issue 連結 + 純內文回覆 block（見下）；`gh issue edit <N> --add-label needs-info`（若有此 label） |
| DUP | issue 連結 + 純內文回覆 block；`gh issue close <N> --reason "not planned"` |
| CLOSE | issue 連結 + 純內文回覆 block（close reason）；`gh issue close <N> --reason "not planned"`（或 `--reason "completed"`） |

**Reply 慣例（NEEDS_INFO / DUP / CLOSE 的回覆部分）**：不用 `gh issue comment --body-file -`——改給 **issue 連結 + 純內文 fenced code block**，maintainer 在 GitHub 網頁直接貼上送出：

```markdown
https://github.com/<owner>/<repo>/issues/<N>

````
<draft response above>
````
```

**Label / close 操作（READY / DUP / CLOSE 的 label 與 close 部分）**：這些沒有純文字等價物，仍用 `gh` 指令草稿（maintainer 自己貼到 terminal 執行）。

**Skill does not run these commands.** Suggest them; maintainer pastes them.
Reply 走「連結 + 純內文 block」慣例；label / close 走 gh 指令——對齊
[`/maigo:address-comments`](https://github.com/Lee-W/maigo/blob/main/commands/address-comments.md) 的新分流。

## Output format

```markdown
## Verdict
READY | NEEDS_INFO | DUP | CLOSE

## Classification
- Tomori's call: <bug | feature | question | documentation | other>
- Existing labels: <list, or "(none)">
- <"Aligned with existing labels" | "Disagreement: ⚠️ <one-line reason>">

## Checklist
- [x] specific title
- [ ] repro steps — missing: 沒寫怎麼觸發
- [—] expected vs actual — skipped (not bug)
- [—] environment info — skipped (not bug)
- [x] no obvious duplicate — Raana grep cleared
- [x] in project scope
- [ ] actionable next step — author 提了想法但沒提怎麼驗收
- [x] follows issue template
- [x] signal not buried

## Suggested labels
- Add: `needs-info`, `question`
- Remove: `bug` (Tomori reclassified as question)

## Draft response
作者的描述提到 X 不如預期，但沒看到怎麼觸發——能補一段 minimal repro 嗎？
具體想看：(1) 哪個指令 / API 呼叫，(2) 跑出來實際 output 與你期待 output 的差。
有的話可以直接進開發；沒有的話我們會先標 needs-info 等補上再回來看。

## Reply
https://github.com/<owner>/<repo>/issues/<N>

````
<draft response above>
````

## Suggested gh commands
```bash
gh issue edit <N> --add-label needs-info --remove-label bug
```

## What's good (optional)
- 作者引用了相關 PR #123 的 commit hash，幫忙縮小了範圍
```

## Re-triage (when issue updated)

When the author replies with more info or a new comment lands:

- Walk through the previous round's `[ ]` items one by one
- New info clearing a `[ ]` → check it off; if all 9 now pass → verdict can upgrade
- Verdict can downgrade too (new comment reveals scope creep → CLOSE)
- "I think they answered it" without quoting the specific reply doesn't clear an item — quote it

## What this skill does NOT cover

- Running the actual gh commands (skill produces drafts, maintainer pastes)
- Code-level review of any attached patches (that's [`strict-review`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/SKILL.md))
- Reproducing bugs (no Taki in triage flow — if maintainer decides "yes worth pursuing", switch to `/maigo:go`)
- Classifying issues that are clearly spam or off-topic — just close, no checklist needed
