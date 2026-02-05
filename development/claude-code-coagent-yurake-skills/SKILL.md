---
name: claude-code-coagent
description: >
  Use claude_code MCP as a third-party co-agent to gather alternative opinions, unblock stalemates,
  or delegate scoped tasks (reviews, ideas, draft edits) while you remain the decision-maker.
  Trigger when seeking another perspective or backup executor: "他の意見", "別の人", "違う観点",
  "打開策ない?", "別LLMの見解", "claudeに頼んで".
---

# Claude Code Co-Agent

## What this skill is for
- Pull in claude_code as an external reviewer/ideator/executor while you (Codex) keep ownership.
- Typical asks: alternative solutions, risk review, unblock ideas, scoped edits/tests in bounded paths.
- Use when the main pair (user + Codex) is stuck or wants a second opinion or fast trial edit.

## Roles
- You (Codex): own context, guardrails, final decisions, and integration of any changes.
- claude_code: provides opinions, options, or scoped file edits; must work within explicit bounds.

## Workflow
1) Frame the ask
   - Goal and expected output format (e.g., 3 options ranked, risk bullets, patch for file X only).
   - Scope: allowed files/dirs, banned actions, time/complexity constraints.
   - Context: minimal code snippets/diffs needed to answer; avoid oversharing.
2) Invoke claude_code with a structured prompt (see templates below).
   - タイムアウトしたら1回リトライ。成功しない場合はユーザーへ報告。
3) Receive and digest
   - Summarize response in 2–3 bullets。
   - MUST: 返答内容を自分の結論・回答に反映する。統合しない場合は理由を明記。
   - Decide: adopt / partial / discard.
   - If edits returned, review diff → apply → run relevant checks/tests if riskful.
4) Follow-up if needed
   - Ask to narrow to one option, or request a patch limited to specific paths.
5) Record briefly
   - What was asked, key takeaways, what was applied (optional but recommended for continuity).

## Prompt templates
- Opinion/ideas: "目的: <goal>. 制約: <constraints>. 求める出力: 選択肢3件を重要度順で。禁止: <bans>."
- Review: "次のdiffを重大リスクがある点のみ箇条書きで。無害な指摘は不要。<diff/snippet>"
- Scoped patch: "ファイル限定: <paths>. 仕様: <spec>. 期待: 完全なパッチのみ。禁止: 依存追加/構造変更。"
- Unblocker: "今の案が行き詰まり。打開策3件、各1行で。前提: <brief>."

## Safety/guardrails
- Always state allowed paths and banned actions before asking for edits.
- Prefer getting reasoning or options first; request patches only after scoping.
- Verify diffs yourself; run focused tests when behavior can change.
- タイムアウト時は1回リトライし、成功した返答は必ず要約して結論に反映。統合しない場合は理由を明示。リトライ失敗時はユーザーへ報告。

## References
- Prompt examples: `references/prompts.md`
- Call checklist: `references/checklist.md`
