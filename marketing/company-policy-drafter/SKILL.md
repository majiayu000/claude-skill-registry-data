---
name: company-policy-drafter
description: "Draft or update company policies (PTO, remote work, expenses, AI-usage) in handbook-ready format with legal review flag and change-summary mode. Use when creating HR policies for small teams without a lawyer. Triggers: 'draft company policy', 'write a PTO policy', 'напиши корпоративную политику', 'политика удалённой работы'."
version: 1.0.0
---

# Company Policy Drafter

This skill drafts or updates a single company policy (PTO, remote work, expenses, or AI-usage) in a structured, handbook-ready format for SMB teams without in-house HR or legal staff. Each output includes a mandatory legal review flag and an optional change-summary when updating an existing policy.

**Input:**
- Policy type (PTO / remote work / expenses / AI-usage / other)
- Key parameters: limits, rules, exceptions, effective date (optional; placeholders used if missing)
- Existing policy text (optional; triggers update mode with change-summary)
- Language preference: both EN+RU / EN only / RU only (optional; default: both)

**Output:**
- Bilingual policy document (EN + RU blocks, synchronized structure)
- Mandatory ⚠️ legal review flag
- Change summary section (update mode only)
- Next steps checklist

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Identify Policy Type

1. Read the user's message and extract the policy type.
   - Recognized types: PTO / vacation, remote work / work from home, expenses / reimbursement, AI-usage / AI tools
   - Also accept any custom policy type (e.g., "social media policy", "confidentiality policy")

2. If policy type is not specified:
   - Stop and ask: "Which policy do you need? Examples: PTO, remote work, expenses, AI-usage, or describe your own."
   - Do not proceed until a type is provided.

### Step 2: Collect Parameters

1. Extract any parameters the user provided:
   - Limits (e.g., "20 days PTO per year", "up to $50 per meal")
   - Rules and conditions (e.g., "approval required 2 weeks in advance")
   - Exceptions (e.g., "does not apply to contractors")
   - Effective date

2. For any missing parameters: use explicit placeholder `[SPECIFY VALUE / УКАЖИТЕ ЗНАЧЕНИЕ]` — do not invent values or leave blanks silently.

3. Mark all placeholders clearly so the user knows exactly what to fill in.

### Step 3: Detect Mode (Draft vs. Update)

1. Check if the user provided existing policy text:
   - **Draft mode** (no existing text): create full policy from scratch
   - **Update mode** (existing text provided): generate updated version and enable change-summary

2. In update mode:
   - Compare old and new content to identify changes
   - Prepare change-summary: what changed, who to notify, notification deadline

### Step 4: Detect Language Preference

1. Check if user specified language preference (EN only / RU only / both)
   - Default: generate both EN and RU blocks
   - If only one language requested: generate only that block (full structure preserved)

### Step 5: Generate Policy Document

1. Build the policy using this five-section structure (apply to both EN and RU blocks):
   - **Purpose / Назначение** — why this policy exists and what it covers
   - **Scope / Сфера применения** — who it applies to (employees, contractors, roles)
   - **Rules / Правила** — specific limits, allowances, conditions (insert user values or placeholders)
   - **Procedure / Процедура** — how to request, submit, or follow the policy (step-by-step)
   - **Responsibility / Ответственность** — who approves, who enforces, what happens on violation

2. Write professional, plain-language text appropriate for an employee handbook.
   - Avoid legal jargon; use simple, direct language
   - Use bullet points for rules and procedures
   - Keep each section to 3–6 bullets or 2–3 short paragraphs

### Step 6: Add Legal Review Flag (Mandatory)

1. Insert the following flag at the top of every output document — before the EN block:

   ```
   ⚠️ Legal review required / Требуется юридическая проверка
   Before implementing, verify compliance with labor law in your jurisdiction.
   Перед внедрением проверьте соответствие трудовому законодательству вашей юрисдикции.
   This document is not legal advice / Этот документ не является юридической консультацией.
   ```

2. **This flag is mandatory and cannot be removed.** If the user asks to remove it:
   - Decline politely: "The legal review flag is a required part of this skill's output. I can adjust its wording, but cannot remove it entirely."
   - Offer to reword the flag more briefly if needed.

3. If the policy contains conditions that may conflict with labor law (e.g., no paid time off, mandatory unpaid overtime):
   - Add an extended warning: "⚠️ Note: This policy may conflict with mandatory employment laws in some jurisdictions. Consult a labor attorney before implementing."

### Step 7: Generate Change Summary (Update Mode Only)

1. If update mode is active, add a "Change Summary" section after the policy body:
   - **What changed / Что изменилось:** list of changed rules or sections (bullet list)
   - **Who to notify / Кого уведомить:** roles or teams affected (e.g., "All employees", "Remote workers")
   - **Notification deadline / Срок уведомления:** suggest a timeframe (or use placeholder if not specified)

2. Format the change summary in the same language as the rest of the output (bilingual if bilingual mode).

### Step 8: Format and Output

1. Assemble the complete document in this order:
   - Legal review flag
   - EN policy block (if EN mode active)
   - RU policy block (if RU mode active)
   - Change summary (update mode only)
   - Next steps checklist

2. Output as clean markdown with clear H2/H3 headings and consistent formatting.

---

## Output Format

```markdown
## [Policy Name] / [Название политики]

> ⚠️ **Legal review required / Требуется юридическая проверка**
> Before implementing, verify compliance with labor law in your jurisdiction.
> Перед внедрением проверьте соответствие трудовому законодательству вашей юрисдикции.
> This document is not legal advice / Этот документ не является юридической консультацией.

---

### 🇬🇧 English Version

**Purpose:** [Why this policy exists]

**Scope:** [Who it applies to]

**Rules:**
- [Rule 1]
- [Rule 2 or SPECIFY VALUE]

**Procedure:**
1. [Step 1]
2. [Step 2]

**Responsibility:** [Who approves / enforces]

**Effective date:** [Date or SPECIFY DATE]

---

### 🇷🇺 Русская версия

**Назначение:** [Для чего нужна политика]

**Сфера применения:** [На кого распространяется]

**Правила:**
- [Правило 1]
- [Правило 2 или УКАЖИТЕ ЗНАЧЕНИЕ]

**Процедура:**
1. [Шаг 1]
2. [Шаг 2]

**Ответственность:** [Кто согласует / контролирует]

**Дата вступления в силу:** [Дата или УКАЖИТЕ ДАТУ]

---

### Change Summary / Сводка изменений *(update mode / режим обновления)*

**What changed / Что изменилось:**
- [Change 1]

**Who to notify / Кого уведомить:**
- [Roles / teams]

**Notification deadline / Срок уведомления:** [Date or SPECIFY DATE]

---

### Next Steps / Следующие шаги

- [ ] Review placeholders ([SPECIFY VALUE]) and fill in your specific values
- [ ] Have the policy reviewed by a legal advisor or labor law specialist
- [ ] Approve with [manager / HR / legal] / Согласовать с [руководителем / юристом]
- [ ] Distribute to all employees / Разослать всем сотрудникам
- [ ] Save as version v1.0 (YYYY-MM-DD) / Сохранить как версию v1.0
```

---

## Edge Cases

1. **No parameters provided (only policy type):** Generate full policy with explicit [SPECIFY VALUE / УКАЖИТЕ ЗНАЧЕНИЕ] placeholders in every field requiring a specific value. Do not invent values; highlight each placeholder so the user knows what to fill in.

2. **Custom policy type (not in standard list):** Accept it and apply the same five-section structure (Purpose → Scope → Rules → Procedure → Responsibility). The legal flag remains.

3. **User requests removal of legal flag:** Decline and explain the flag is mandatory. Offer to shorten or reword it instead.

4. **Single-language request (EN only or RU only):** Generate only the requested language block. All five sections and the legal flag remain. Change summary (if applicable) is also in the requested language only.

---

## Negative Cases

- **No policy type specified:** Ask for clarification. Do not generate a generic document. Prompt: "Which policy do you need? Examples: PTO, remote work, expenses, AI-usage, or describe your own."
- **Policy contains potentially illegal conditions:** Do not block generation, but extend the legal flag with a specific warning about the conflict. Example: "⚠️ Note: Policies eliminating paid leave may violate mandatory labor laws in many jurisdictions."
