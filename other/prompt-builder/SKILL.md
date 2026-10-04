---
name: prompt-builder
description: "Interactive structured prompt generator for Claude based on the user's task description. Asks 7 questions and assembles a ready-to-use prompt from a universal template. EN triggers: 'create a prompt', 'write a prompt', 'prompt builder'. RU triggers: 'создай промпт', 'напиши промпт', 'prompt builder'."
version: 1.0.0
---

# Prompt Builder

An interactive generator that builds structured prompts for Claude based on the user's task description. The skill asks 7 questions, interprets loose or vague answers, clarifies details, and assembles a ready-to-use prompt from a universal template.

Suitable for anyone who needs to create a reusable, well-structured prompt for Claude — for code review, content writing, data analysis, or any other repeatable task.

## Language Detection

Detect the language of the user's first message:
- If the message is in **Russian** — conduct the entire interview and output the final prompt in Russian.
- If the message is in **English** — conduct the entire interview and output the final prompt in English.
- If the language is ambiguous, default to English.

All question texts, labels, and output section headers must match the detected language.

## Input

A natural-language description from the user of what they want the prompt to accomplish. Can be brief ("I need a prompt for code review") or detailed.

## Output

A structured prompt document with sections: Role, Context, Task, Input data, Output requirements, Constraints, and optionally Examples. Displayed in chat and optionally saved as a `.md` file.

## Instructions

### Step 1: Interactive interview

Ask questions in the order below. Wait for the user's answer after each question before proceeding.

**Rules:**
- User answers may be unstructured or vague — interpret the intent
- If an answer is unclear or incomplete, ask a clarifying question
- Do not move to the next item until you have enough information
- Collect answers into variables for final generation

---

#### Question 1: Claude's role

**EN:** "What role should Claude take on in this task? (E.g.: analyst, writer, tester, coder, etc.) Describe what it will do in general terms."

**RU:** "Какую роль должен взять на себя Claude в этой задаче? (Например: аналитик, писатель, тестировщик, кодер и т.д.) Опиши, что он будет делать в общих чертах."

**Action:** Interpret the answer, extract the role and core function. If the answer is too broad, ask: "If I understood correctly, Claude should act as [your interpretation]? Confirm or clarify?"

**Variable:** `ROLE`

---

#### Question 2: Context

**EN:** "What context does Claude need to understand the task? (Background: why this matters, conditions, prerequisites?)"

**RU:** "Какой контекст нужен Claude для понимания задачи? (Фоновая информация: почему это важно, в каких условиях, какие предпосылки?)"

**Action:** Interpret as background and prerequisites. If the user says "it's clear from the task", ask: "Are there specific conditions, constraints, or history that affect the task?"

**Variable:** `CONTEXT`

---

#### Question 3: Main task

**EN:** "Specifically, what should Claude produce? (Describe the exact result you need)"

**RU:** "Конкретно, что должен выполнить Claude? (Опиши точный результат, который нужен)"

**Action:** Interpret as the primary goal. If the answer is vague, reframe: "So you need [your interpretation]?"

**Variable:** `TASK`

---

#### Question 4: Input data

**EN:** "What data or information will be passed to Claude? (Text, table, list, description, nothing?)"

**RU:** "Какие данные/информация будут подаваться на вход Claude? (Текст, таблица, список, описание, ничего?)"

**Action:** Interpret the format and type of input. If "it depends", ask: "Give an example of a typical input."

**Variable:** `INPUT`

---

#### Question 5: Output requirements

**EN:** "What should the result look like? (Format: text, list, table, code, JSON, etc.) (Length: brief, detailed, specific number of items?) (Style: technical, plain language, with examples?)"

**RU:** "В каком виде должен быть результат? (Формат: текст, список, таблица, код, JSON и т.д.) (Объем: краткий, развёрнутый, конкретное количество пунктов?) (Стиль: технический, простой язык, с примерами?)"

**Action:** Interpret all three aspects. If only one is answered, ask about the others: "And the format? Length? Style?"

**Variable:** `OUTPUT`

---

#### Question 6: Constraints and tone

**EN:** "Are there any constraints or special requirements? (What to avoid, tone, taboos, formatting restrictions?)"

**RU:** "Есть ли ограничения или специальные требования? (Что нельзя делать, особый тон, табу, форматирование?)"

**Action:** Interpret as constraints and stylistic requirements. If "no constraints", ask: "Can Claude be creative? Is there a preferred style (formal/informal)?"

**Variable:** `CONSTRAINTS`

---

#### Question 7: Examples

**EN:** "Do you need input/output examples for clarity? (If yes, provide one: what goes in, what's expected out)"

**RU:** "Нужны ли примеры input/output для ясности? (Если да, приведи пример: что на входе, что ожидается на выходе)"

**Action:** If "yes" — ask for an example. If "no" — skip and proceed to generation.

**Variable:** `EXAMPLES` (optional)

---

### Step 2: Generate the prompt

After collecting all answers, assemble the final prompt using the appropriate template.

**EN template:**
```
## Role
[ROLE]

## Context
[CONTEXT]

## Task
[TASK]

## Input data
[INPUT]

## Output requirements
[OUTPUT]

## Constraints
[CONSTRAINTS]

[IF EXAMPLES COLLECTED:]
## Examples
[EXAMPLES]
```

**RU template:**
```
## Роль
[ROLE]

## Контекст
[CONTEXT]

## Задача
[TASK]

## Входные данные
[INPUT]

## Требования к выводу
[OUTPUT]

## Ограничения
[CONSTRAINTS]

[ЕСЛИ EXAMPLES СОБРАНЫ:]
## Примеры
[EXAMPLES]
```

---

### Step 3: Output and save

1. Display the final prompt in chat — clearly and structured
2. After the prompt, ask the user: "The prompt is ready. Do you want to save it as a `.md` file?" (in the detected language)
3. If "yes":
   - Suggest a filename (e.g.: `prompt-[short-description].md`)
   - Save the file and make it available for download or copying
4. If "no":
   - Ask: "Do you need any edits to the prompt?"
   - If edits — return to the relevant step, update the variable, regenerate

## Output Format

The generated prompt is a Markdown document with H2-level section headers. Each section contains only the user-provided content for that field, lightly formatted for readability. The document is self-contained and ready to paste directly into a new Claude conversation.

## Negative Cases

- **User provides a full, detailed description upfront** — still ask all 7 questions to confirm each field; prefill your interpretation and ask the user to confirm rather than skipping
- **User answers in a different language mid-interview** — switch to that language for remaining questions and the final output
- **User wants to skip a question** — accept "skip" or "not applicable" and use a reasonable default (e.g., "No specific constraints") rather than blocking
- **User asks to edit the generated prompt** — return to the relevant question(s), update variables, and regenerate the full prompt
- **User provides contradictory answers** — ask for clarification rather than guessing which answer to use
