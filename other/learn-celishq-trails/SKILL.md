---
name: learn
description: Drafts patterns from a source, such as past chats, a skill file, a folder or a URL, and keeps the ones the person agrees to. Use when the person runs /celis:learn <source>, or asks celis to learn from their history, a document or a repo.
---

The text after `/celis:learn` names the source. You read it, draft what later work should keep, and
the person keeps or drops each draft. Add it as one ask, as the card says, and write nothing before the
person says yes.

1. Read the source. For past chats, read the agent's history files the person names, such as
   `~/.claude/projects/<project>/*.jsonl`, and look at the person's own prompts: corrections, the
   words "always" and "never", picks, and reactions to a result. For a skill file, a folder or a URL,
   read its text and the files it shows as examples.
   For a URL or a web page, when you can open it in a browser, also save in a folder for this ask what
   its text cannot show: a screenshot of each part that shows a taste, such as the hero or a card, and a
   short recording, a gif or an mp4, of each motion, such as a hover or a page load. Read each motion's
   timing and easing from its CSS or script, because a recording shows the motion but not its values.
   When you cannot open a browser, say so, and draft from the text alone.
2. Read the index that `celis patterns` gives, open with `celis patterns <id>` each pattern that may say
   the same as a draft, and leave out each draft that a live pattern already says.
3. Draft each point as a pattern in the five lines the card shows, as its Learn move says: a must, such
   as "always" or "never", a taste, and a choice the source explains are each a pattern that guides,
   with each file, step or URL the source gives as a good or a bad example, and each screenshot or
   recording you saved as a good example of the pattern it shows. A pattern needs
   no example: its forces and its reason carry it. A skill's process, such as "plan, then build", is a
   pattern of the order of the work. Draft the patterns as a graph: a larger one first, such as the
   whole page, then each smaller one it holds, such as the hero, linked with `--within <its id>`. Say a
   motion by its role in the `Do`, such as "a short lift that settles", and write its exact timing and
   easing as a pattern of its own. Name a secret by where it lives, never by its value.
4. Show the person the drafts, numbered, each with where in the source it came from and its example
   files, and ask which to keep: a list of numbers, all, or none. Write each kept draft with `pattern`, its `--path` the module
   or the kind of file where it holds, never one file, `--within` the id of its larger pattern once that one is written, and `--scope me`
   when it holds for that kind of work in any project.
5. Close the ask. In the end, give how many drafts you made and how many the person kept, and each id.
