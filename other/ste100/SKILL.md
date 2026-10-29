---
name: ste100
description: The ASD-STE100 rules for the Claude files (CLAUDE.md, .claude/, the memory files) and for agent prompts and reports, with the checker that the hooks run. Use it when you write a Claude file, a prompt for a subagent or a report from a subagent.
---

# ASD-STE100 (Simplified Technical English)

The Claude files and the messages between agents use ASD-STE100. The Claude files are CLAUDE.md, the Markdown files in
`.claude/` and the memory files. The messages are the prompts to subagents and the final reports of subagents. A
reader must understand each sentence one time, with one meaning for each word.

`check.py` finds the rule breaks that a program can find. Hooks in `.claude/settings.json` run it:

- An edit to a Claude file stops when a changed paragraph breaks a rule.
- A prompt to a subagent stops when it breaks a rule.
- A subagent writes its final report again when the report breaks a rule (three times at most).
- The ctest `claude_ste100` checks all the Claude files of the repository.

The checker cannot check the dictionary. You must use the approved words with their approved meanings.

## Words

- Use the words of the STE dictionary, with the meaning that the dictionary gives. Use one word for one meaning.
- You can use a technical name or a technical verb. Examples are a file name, a symbol, a register, a Vulkan term
  and a command. Put code, paths and commands in code spans. A code span counts as one word.
- Do not use the -ing form of a verb. Use a noun, the infinitive or a clause with a verb. You can use a technical name
  that ends in -ing (a binding, a setting). Add it to `terms.txt`.
- Do not use contractions. Write "do not", "cannot" and "it is".
- `words.txt` lists the words that STE does not approve and the words to use in their place. Add to it when you find
  more.
- Do not use more than three nouns in a noun cluster. Use a preposition to divide a longer cluster.

## Verbs

- Use the active voice. Say who or what does the action: "the build deploys the runtime", not `the runtime is
  deployed`.
- Use the simple present, the simple past or the simple future. Do not use `has done` or `had done`.
- Use the past participle only as an adjective: "the changed file".
- Use "must" for a rule, and "can" for a possibility. Do not use `have to`.

## Sentences

- An instruction has 20 words at most. A description has 25 words at most.
- Write one instruction in each sentence. Write the instruction as a command: "Run the test."
- Do not leave out words to make a sentence shorter. Keep "the", "a" and "that".
- Do not use a semicolon. Write two sentences or a list.
- Use a vertical list for a sequence of steps or for items that are alike.

## Paragraphs

- A paragraph has 6 sentences at most, and one topic.
- Put the most important information first.
- Put a warning or a caution before the step that it is for.

## Prompts and reports

- A prompt to a subagent follows these rules. Give the goal, the files and the facts in short sentences and lists.
- A report from a subagent follows these rules. Give the result first, then the evidence.
- Quoted code, logs and disassembly are not text. Put them in code blocks, which the checker does not read.

## Check

```sh
python3 .claude/skills/ste100/check.py FILE...      # the rule breaks in each file
python3 .claude/skills/ste100/check.py --all        # every Claude file of the repository
python3 .claude/skills/ste100/check.py --text < F   # a prompt or a report
```

Each line of output gives the line, the rule and the text. Write the sentence again. Do not change the checker to
let a sentence through. A false positive is a bug in the checker. Fix the checker, and add a test case to `test/`.
