---
name: answer-buzzkill
description: Write a short, fact-checked reply that answers a colleague's question in one meaning only, ready to copy and paste. The input is their pasted message. Check the claims against the code first, use the project glossary terms, and print only the reply in chat. Read-only — no writes to code, the issue tracker, GitHub, chat or any MCP. Use on "/cortex-communication:answer-buzzkill", "help me answer", "reply to this question", or when the user pastes a colleague's question and asks for an answer in the same manner.
---

# Answer Buzzkill

> "What's the word for душнила? Buzzkill?" — [Oleksandr Usyk](https://www.youtube.com/shorts/GFOxVAQeK3g)

The input is a message from a colleague, pasted as is. The output is one reply that the user can paste back to them without editing.

## Who the colleague is

The colleague is a highly skilled software engineer. They do not need basics explained. They often ask follow-up questions one after another, and the thread goes deeper each time without reaching a decision. The reply must end that loop: give them a closed answer that matches their intention, and leave no open end for a new question.

Their intention is one of two types. Find which one before you write:

- **To do.** They must decide or build something. Give the answer and the one fact that decides their action.
- **To understand.** They want to know how the system behaves. Give the behaviour as a complete, closed statement: what happens, and where it stops.

## Side effects

Read-only. You can read code, git history, the issue tracker and any MCP. You must not write to any of them: no file edits, no commits, no ticket comments, no PR comments, no messages. The reply goes into chat only.

## Steps

1. **Find the question.** The colleague often explains their context before they ask. Find the one question they want answered, and find their intention: what they will decide or do with the answer. Answer that question only. Ignore side points they say are "not the question".
2. **Check the facts in the code.** Find the code that runs for their case and read it to the end. Do not answer from memory, from a ticket, or from what their message claims. If their message states something about the system, check it. If the code disagrees, say so in one sentence.
3. **Use the glossary terms.** Read the project domain glossary (for example `CONCEPTS.md`, `GLOSSARY.md` or `CONTEXT.md` at the repo root). If there is no glossary, use the names the code uses. Use one term for each concept. If the colleague uses a raw status name or a code value (for example an enum value or a vendor status) and the concept term could be read in a different way, keep their word in backticks so the two of you agree on what it means.
4. **Write the reply.** Use the format below.
5. **Do a check for ambiguity.** Read each sentence as the colleague. If a sentence can have two meanings, rewrite it. If a sentence will make them ask a new question that does not help their decision, delete it.
6. **Close the loop.** Predict the next question they will ask. If that question is necessary for their intention, answer it in the reply now. If it is not necessary, make sure no sentence invites it: no "except", "in some cases", "it depends" or other open qualifiers unless you also state the full condition.

## Reply format

Short is kind. The colleague reads the reply between other tasks, so give them the minimum that answers the question, and nothing they already know.

- The first word answers the question: "Yes", "No", or the direct value. Limit the answer to their case in the same sentence.
- After that, give at most 3 bullets with only the facts they need to trust the answer or to act on it. If the first sentence is enough, give no bullets.
- Describe the behaviour, not the code. Add a code reference (a file or a method name) only when they cannot verify or act on the answer without it, and add a maximum of one.
- Do not repeat their question, their context or anything a senior engineer knows.
- Do not use "should", "might", "probably" or "usually". State what the code does. If the code cannot answer a part of the question, say so in one sentence, and say what will answer it (a config, an environment, a person).
- Keep the tone warm, but do not add a greeting, a summary or an offer to help. If their idea was right, say so in a few words ("Yes, you are right:"). If the code disagrees with them, state what the code does, not that they are wrong. Do not use "obviously", "as I said", "just" or "simply".
- Write in the practical depth of `/cortex-communication:simple-english`: short sentences, active voice, one word for one concept, and the glossary terms from step 3.

## Output

Print the reply as plain Markdown, and nothing else: no code fence, no delimiters, so it renders in chat and copies with its formatting and working links. If the facts in the code disagree with something the user said earlier in the session, add a horizontal rule after the reply and one line below it for the user only, not for the colleague.

## Example

The colleague asks if a background job that a deploy interrupts is retried, and explains that they think `stalled` and `failed` jobs need different handling.

```text
Yes, you are right: an interrupted job comes back as `stalled`, not `failed`.

- After its lock expires (30 seconds), a new worker runs it again from the start. Steps that finished before the deploy run again.
- Stalls do not count against the retry limit. After 2 stalls, the job moves to `failed`.
```
