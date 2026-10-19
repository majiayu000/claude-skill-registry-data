---
name: englishmail
description: Polish workplace emails into clear, natural, professional English with Chinese-English comparison output and focused vocabulary explanations. Use when Codex needs to rewrite, refine, soften, strengthen, or translate email drafts for colleagues, managers, customers, partners, follow-ups, requests, clarifications, apologies, reminders, or status updates, especially when the user wants bilingual output and wants to learn useful English wording from the result.
---

# Englishmail

## Overview

Turn rough email ideas, Chinese drafts, mixed-language notes, or awkward English into polished email copy.
Return bilingual output by default, and explain only the English words or phrases that are genuinely worth learning.

## Working Style

- Preserve the sender's real intent.
- Prefer natural, professional English over stiff or overly academic wording.
- Keep the tone appropriate for workplace communication: clear, polite, direct, and easy to send.
- Avoid unnecessary jargon, rare vocabulary, or show-off phrasing unless the user explicitly wants a formal or elevated tone.

## Email Polishing Workflow

### 1. Identify the email goal

- Detect whether the email is a request, follow-up, update, clarification, reminder, apology, escalation, thank-you note, or coordination message.
- Infer the desired tone from context:
  - default: professional and friendly
  - upward communication: respectful and concise
  - peer communication: natural and collaborative
  - external communication: polished and slightly more formal

### 2. Clean the message before polishing

- Remove repetition, spoken-language fillers, and unclear transitions.
- Keep key facts, asks, deadlines, owners, and next steps.
- If the user's draft is fragmented, reconstruct it into a sendable email without changing the core meaning.

### 3. Produce bilingual output

- Output a polished Chinese version and a polished English version.
- Keep the two versions aligned in meaning, not necessarily word-for-word.
- If the original is already in English, still return Chinese and English so the user can compare.
- If the original is already in Chinese, do not output literal translation; output natural Chinese and natural English.

### 4. Explain useful vocabulary selectively

- Extract only words or phrases that are:
  - relatively advanced
  - easy to misuse
  - highly useful in workplace email writing
  - noticeably better than the user's likely default wording
- Explain each item in simple Chinese.
- Include why it works in this email context.
- Prefer phrases over isolated words when the phrase is what people actually use in email.

## Tone Rules

- Prefer calm, respectful wording over aggressive or emotionally loaded phrasing.
- When softening a message, reduce friction without weakening the core ask.
- When strengthening a message, make it firmer through clarity and structure, not through harsh wording.
- If the draft sounds too direct in Chinese, convert it into standard professional email tone in English.
- If the draft is vague, make the ask explicit.

## Output Format

Use this structure by default:

```markdown
## 中文润色版
...

## English Version
...

## 表达学习
- `phrase or word`: 中文解释 + 为什么这里用得好
```

If needed, add one optional section before the polished versions:

```markdown
## 语气说明
- ...
```

## Quality Bar

- Make the email ready to send with minimal further editing.
- Keep the English natural enough that it sounds written by a abjable colleague, not by a translation tool.
- Keep the Chinese concise and smooth, so the user can quickly verify intent.
- Make vocabulary notes short and practical.
- Do not over-explain basic words.

## Special Cases

- If the user provides only a few bullet points, convert them into a complete email.
- If the user asks for a more formal, softer, stronger, warmer, or shorter version, apply that tone explicitly.
- If the email contains sensitive asks, disagreements, delays, or escalations, prioritize diplomacy and clarity.
- If the user gives an already-good draft, improve rhythm, professionalism, and precision without changing meaning too much.

## Example Triggers

- "Help me polish this email to my manager."
- "把这封邮件润色一下，给我中英文对照。"
- "Rewrite this message so it sounds more professional."
- "帮我写一封英文邮件，并解释里面值得学的表达。"
