---
name: stuck
description: "Diagnoses a broken course setup by reading the folder, so the student never has to describe the problem in English. Takes no argument. Reports which class they are on and which files are filled, then names one blocker and one fix: Claude Code opened at the wrong level, .claude/skills/ missing, skills not loading because the trust question was never answered, a file whose scaffolding was deleted before it was filled, work going into an answer-key .example.md, an unfilled YOUR TURN, a skill run before the files it reads were filled, or a hunt for a file no skill creates. When it cannot tell, it writes the group-chat message for the student. Use whenever a student says they are stuck, confused, blocked, or that something is not working."
---

The student typed `/stuck` and nothing else. That is the whole input, and it is deliberate.

Do not ask them what is wrong. Do not ask them to describe the problem, paste an error, or say which step they are on. Most of this room reads and writes English as a second language, and having to explain a broken setup in English is the thing that stops people asking for help at all. So you look at the folder, work it out, and tell them what you found.

Create no file. This skill writes nothing to disk unless the fix itself is a file change and the student says yes to it first.

## The one rule

**Name one blocker and one fix. Then stop.**

A student running this is already lost. A list of eight possibilities asks them to triage, and triage is the thing they cannot do right now. So walk the chain below in order, stop at the first check that fires, and say only that.

Once they tell you it is fixed, run the chain again from the top and give them the next one.

## Step 1. Read before you speak

Look at all of this before you write a single sentence:

1. Which folder you are open in. Does it hold `CLAUDE.md`, `principles/`, `projects/`, `skills/` and `career-vault/`? Or does it hold `context.md` and `claude-contract.md`, which means you are inside one project folder.
2. Whether `.claude/skills/` exists at the course-folder root, and how many command folders sit inside it.
3. Which folder inside `projects/` is theirs. A folder that is not `edubridge` and not `_new-client` is theirs. If there is none, EduBridge is their project, which is a normal choice.
4. Every headline file in the class table in `CLAUDE.md`, and for each one whether it is still course scaffolding or the student's own writing.
5. Whether any `*.example.md` file has been edited, and whether a student file matches the `.example.md` beside it closely enough to be a copy.

A file is **still scaffolding** if any of these is true:

- A `YOUR TURN` heading is there with the prompts still sitting in HTML comments under it.
- It still holds `COURSE SCAFFOLDING`, `COURSE NOTE for the student`, `DELETE EVERYTHING ABOVE`, or `DELETE EVERYTHING EXCEPT`.
- The only filled part is the labelled EXAMPLE section, which is the instructor's.

A file is **damaged** if the frontmatter, the headings, or the `YOUR TURN` block are gone and no student writing replaced them. That happens when the scaffolding gets deleted before the answers get written, and the file is now shorter than it started.

Read `CLAUDE.md` for the class table. Do not restate that table here or in your answer; it changes, and a second copy of it goes stale.

## Step 2. Say where you think they are

Open with four short lines, in this shape:

> I read your folder. Here is what I see.
>
> **Class:** 4, Claude as Critic. **Your project:** `projects/edubridge/`.
> **Filled:** `principles/claude-contract.md`, `projects/edubridge/context.md`, `projects/edubridge/brief-v3-interrogated.md`.
> **Still blank:** `principles/design-taste.md`, `principles/anti-ai-slop.md`, `projects/edubridge/critique-notes.md`.
> **This week's file:** `projects/edubridge/critique-notes.md`.

Name real paths. Never say "some files" or "your context files". The paths are the part they can check against their own screen, and checking is what makes the rest of your answer believable.

If the file evidence is mixed, say which reading you went with in one sentence, then carry on. Do not stop to ask.

## Step 3. Walk the chain, stop at the first hit

### Check 1. Which level is Claude Code open at

Two levels are both correct, for different work. Root is for anything about the student: their contract, their taste rules, their career vault. The project folder is for client work.

It is only a fault when the level cannot reach this week's file.

- You are inside a project folder, and this week's file lives at root, or the skill this week needs `principles/`. Then say it.
- You are at root doing client work. That is fine. Say nothing.

What to say:

> You are open at `projects/edubridge/`, one folder down. From here I cannot see `principles/`, so every critique I write comes out generic no matter how good your prompt is.
>
> **Fix:** close this session. Open Claude Code again and pick the folder that holds `CLAUDE.md`, one level up. Then type `/stuck` again and I will check the next thing.

Also check for a doubled folder, like `claude-for-designers/claude-for-designers/`. Unzipping produces that, and the outer one is empty. The fix is the same: reopen at the inner folder, the one with `CLAUDE.md` in it.

### Check 2. Do the commands exist on disk

Look for `.claude/skills/` at the course-folder root, with one folder per command and a `SKILL.md` inside each.

**The folder shipped without `.claude/` for a while.** If it is missing, nothing the student did caused it, and say that out loud. They have zero slash commands and typing `/` shows nothing.

They can still reach you two ways, so tell them the shorter one:

> `.claude/skills/` is not in your folder, so you have no slash commands at all. The download shipped without it. Nothing you did caused this.
>
> **Fix:** paste this and I will build them from the files already in `skills/`:
>
> ```text
> Create .claude/skills/ at the root of this folder. For every .md file in
> skills/ except README.md, make a folder named after the file and put the
> file inside it as SKILL.md, with a name and description at the top.
> Then list the folders you made.
> ```
>
> Close Claude Code and open it again. Type `/` and the names appear.

If the student got here by pasting this file's text instead of typing `/stuck`, this check is the likely answer and you should reach it fast.

### Check 3. Do the commands load

`.claude/skills/` is on disk and looks right, but nothing appears when they type `/`.

You cannot see the trust dialog, so ask one closed question. One word answers it:

> Your `.claude/skills/` folder is there and there is a folder inside it for every command, so the files are fine. Did you type `/stuck`, or did you paste the text of a file? One word is enough.

Paste means the commands are not loading. Then:

> **Fix:** the first time Claude Code opens a folder it asks whether you trust the files in it. Skills stay switched off until you say yes. Close Claude Code, open the same folder again, and accept the question it asks before you type anything else.

Typing it means the commands load, so move to Check 4 and say nothing more about this.

### Check 4. Is a file damaged

The file exists but the frontmatter, the headings or the `YOUR TURN` block are gone, and nothing the student wrote replaced them. Every fillable file ends with a comment telling them to delete the scaffolding once their answers are in, and sometimes the delete lands first. The file is now shorter than it shipped, and there is no shape left to fill.

This check runs before the two below it, because a file with no headings cannot be filled and cannot be compared to anything.

> `principles/design-taste.md` has lost its headings, and there is nothing under them. The delete came before the writing, so the file has no shape left to fill.
>
> **Fix:** say yes and I will put the five headings back, empty, with your own lines untouched. Then we fill one heading at a time.

Wait for the yes. Never restore a file without it.

### Check 5. Are they in an answer key

Any file ending `.example.md` is the instructor's worked version.

**A blank `.md` sitting beside a filled `.example.md` is how the folder shipped. Never report that as a fault.** Every class works that way: the template is empty and the answer sits next to it. Calling that broken tells a student on track that they are behind, which is the worst thing this skill could do.

Two states are real. First, their file reads as a copy of the example:

> Your `context.md` matches `context.example.md` almost line for line. That is my EduBridge answer, not yours, and the assignment grades your decisions.
>
> **Fix:** keep the shape and change the facts. Tell me your client, your users and your one hard constraint, and I will ask you three questions instead of writing it for you.

Second, the `.example.md` is the file they have been writing in:

> You have been working in `context.example.md`. That one is my filled version, so it is not what gets marked, and `context.md` beside it is still empty.
>
> **Fix:** say yes and I will move your writing into `context.md` and put the example back as it was. Nothing you wrote gets lost.

You cannot always tell which file they are in. If the folder gives you nothing on this, skip the check rather than asking. Check 6 usually answers the same question anyway.

### Check 6. Is this week's file filled

Headings are there, prompts are still in comments, nothing written.

This is not a blocker. It is the assignment, so treat it as the assignment:

> Nothing is broken. `projects/edubridge/critique-notes.md` is the file for tonight and it is still the blank template, which is exactly where you should be.
>
> **Fix:** I ask you the first question, you answer in one line, I write your words into the file. Ready?

Then ask one question and stop. Never fill a `YOUR TURN` section for them.

### Check 7. Do the files this week's skill reads exist

A skill run on empty inputs returns output that fits any project ever made, and the student reads that as the skill being weak. It is the most common wrong turn in the whole course.

Check the class's dependency files before you blame the skill:

- `/design-review`, `/heuristic-evaluation`, `/persona-acid-test` read `principles/design-taste.md` and `principles/anti-ai-slop.md`.
- `/frontend-design` reads `projects/<theirs>/tokens.md` and the interrogated brief.
- Every skill reads `principles/claude-contract.md`.

> Your critique came back saying things like "improve the visual hierarchy", which would fit any screen ever made. `principles/design-taste.md` and `principles/anti-ai-slop.md` are both still the blank template, so the skill had nothing of yours to judge against.
>
> **Fix:** three lines in `design-taste.md` first. Not ten. Then run the critique again on the same screen and read the difference.

### Check 8. Are they looking for a file no skill creates

Most skills write no file. They hand back text in the session, and that text goes into a file that already exists.

Class 6 is the exception. `/information-architecture` writes `ia-map.md` and `ia-map.html`, and `/brief-to-tasks` writes `tasks.md`.

Outside Class 6 there is no `design-brief.md`, no `ia.md`, no `review.md`, no `grill-me-output.md`. A student spent hours in the group chat asking whether their `/grill-me` output had become a new file. It had not.

> Nothing is missing. `/grill-me` on a brief hands you a Requirements Handshake as text and creates no file. It goes into `projects/edubridge/brief-v3-interrogated.md`, which is already in your folder waiting for it.
>
> **Fix:** scroll up to the handshake, copy all three sections, and paste them under `## YOUR TURN` in that file. Whole thing, not a summary. Say when it is in and I will read it back.

## Step 4. When you cannot work it out

Some things are invisible from inside the folder. Say so plainly rather than guessing, and never invent a cause to look useful.

The clearest example is Windows. Claude Code needs Git installed as a background requirement, and the setup guide used to say no Git was needed. A student who followed the guide exactly gets a Code tab that opens nothing. That student cannot reach you at all, so if you are being read, that is not their problem.

When the chain finds nothing, write the group-chat message **for them**. This is the output that matters most, because a student who cannot describe the fault in English gets a message they can send anyway.

Fill in everything you already know from the folder. Leave them one blank at most.

> I cannot see the cause from here, so this one needs a human. Copy this into the group chat exactly as it is:
>
> ```text
> Class 4, EduBridge. Windows.
> I opened the course folder root in the Code tab and ran /design-review on
> projects/edubridge/booking-screen.html.
> It ran, but nothing appeared in critique-notes.md and I do not know why.
> Filled: principles/claude-contract.md, principles/design-taste.md,
> projects/edubridge/context.md, brief-v3-interrogated.md.
> Blank: principles/anti-ai-slop.md, projects/edubridge/critique-notes.md.
> ```
>
> Send that and stop working on it tonight. Somebody can answer it in one line.

Two rules for that block. Keep it under about eight lines, because a wall of text gets scrolled past in a group chat. And put the class and the platform first, since those two decide who can answer.

## How you talk in all of this

- **Never say they did something wrong.** No "you should have", no "the mistake was". Name what the folder shows and name the next move. A student who feels caught out stops asking.
- **Short sentences. Concrete nouns.** Real paths, real command names, real file names. A sentence they have to read twice has failed.
- **One fix, and make it a size, not a lecture.** "Three lines in `design-taste.md`" tells them whether tonight is enough time. "Improve your taste file" does not.
- **Show your working.** Say what you checked and what you found, in that order, so they can see the reasoning instead of receiving a verdict. When you were unsure, say which way you read it.
- **Never say the folder or the course is broken** when you have not checked. Say what you checked, and if you have run out of checks, use Step 4.
- No em dashes. No marketing words. No praise before the answer.
