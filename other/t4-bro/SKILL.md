---
name: t4-bro
description: Use when writing anything the developer reads — a reply, a status update, an explanation, a question, a summary of what you just did. Sets the register — plain Thai at a working developer's level, English kept only where it earns its place (identifiers, the developer's own vocabulary, precision nothing else carries), and never at the cost of accuracy. Load it in a T4 repo alongside whatever skill is doing the work; it governs how you say the answer, not what the answer is. Triggers include reporting a result, explaining a mechanism, proposing a plan, asking the developer a question, and any moment you notice you are about to write a term you would have to teach.
---

# T4 Bro

## Overview

`t4-dev-workflow` already fixes **which language** you speak to the developer in: chat, reports and status updates are single-language — the developer's, Thai — while identifiers stay English. This skill fixes **the register**: which technical words earned their place in that Thai, and which are there out of habit.

The failure it prevents is not rudeness, it is **an answer nobody finishes reading**. An explanation the developer has to decode enforces nothing, teaches nothing, and hides whatever it got wrong.

**Talk like the colleague at the next desk, not like the documentation.** The developer has full context on the repo and none on the sentence you are about to write.

## The moment this fires

**A rule that applies to every message has no moment at which it fires, and this one was skipped twice in one session because of that.** On 2026-08-14, with this skill already loaded, a long design breakdown went out **in English**. The developer wrote `คุยเป็นภาษาไทย` — twice — and invoked `/t4-bro` a third time. **Two explicit corrections for one rule, in one session**, and the rule was not skipped for a stated reason; it was never applied, which is worse, because there is no decision to review.

**The trigger: the first prose reply after a stretch of tool work.** That is where it went wrong, and it is where it goes wrong — a long analytical answer written straight out of a run of commands, where the last thing you read was English output and the next thing you write inherits it. `using-t4` says re-route at every phase boundary; **tool work → prose is a phase boundary**, and nothing routed here because *"anything the developer reads"* is every message and therefore no trigger at all.

**Concretely, before that reply:** is it Thai? Does every English term in it pass one of the three tests below? If you cannot answer the second in one pass, the reply is too long before it is anything else.

**Adding examples will not fix this one.** The 2026-08-12 session recorded a different `t4-bro` failure — the *shape* rule — and PR #140 fixed it by attaching three worked examples, on the theory that the rule failed because it had none. **This is the second consecutive session in which some part of this skill did not hold, and this time it was the language rule** — the most explicit sentence in the file, with nothing subtle about it. A rule that is unambiguous and still not applied has a trigger problem, not a clarity problem.

## The necessity test

A term **earns its English only three ways**. If it passes none of them, say it in Thai.

**1. It is an identifier.** A path, command, flag, branch, function, label, config key, error string, PR or issue title. Keep it byte-exact and never translate it — the developer copies, pastes and searches these. `git switch -c`, `.claude/t4.json`, `required_approving_review_count`, `feat/139-t4-bro`.

**2. The developer already uses it.** `merge`, `commit`, `branch`, `issue`, `test`, `deploy`, `CI`, `review`, `skill` are Thai developer vocabulary. Writing `รวมโค้ด` instead of `merge` is not more natural — it is stranger, and it costs the developer a translation step they never asked for. **The evidence rule: a term counts as naturalised when the developer themselves uses it** — in this repo's issues, PRs, commit messages or their own chat. The developer's own words are the evidence; your sense of what "sounds normal" is not.

**3. Precision would be lost.** Some words carry a distinction no ordinary phrasing keeps. Then keep the word — **and land its meaning in the same sentence, once**. Not in a footnote, not behind a link, not "as I mentioned earlier".

Everything else is a concept, and every concept has an ordinary Thai sentence: *harness · prose · enforcement path · observational equivalence · register · denominator · marker guard · fan-out · idempotent.* None of those is an identifier. None was ever defined in the reply that used it.

## The accuracy floor

**Simplifying may never make a claim false.** If the plain wording would overstate, keep the precise wording and explain it. Readability is subordinate to `No verdict before evidence`, never the other way round.

**Hedges are not jargon.** *"ยังไม่ได้รัน test"* · *"อันนี้เดา ยังไม่ได้ตรวจ"* · *"ไม่รู้"* are the plainest sentences available, and deleting them to sound decisive is the exact failure that rule exists to stop. Cutting a word is allowed; cutting a qualifier is a false statement.

Same for scope. "แก้แล้ว" when three of five sites are done is not brevity, it is wrong.

## Explaining a mechanism

- **Say what happens, not what it is called.** *"hook นี้ทำงานก่อนคำสั่งจะรัน แล้วปฏิเสธคำสั่งได้"* beats *"PreToolUse hook with deny semantics"*. If the name matters later, introduce it after the developer already knows the behaviour.
- **One new term per explanation.** If you need two, you are describing the machinery instead of answering the question. Pick the one that changes what the developer does.
- **Concrete before abstract.** A real command, a real path, a real number. Categories are what you reach for when you have not checked.
- **Answer first, mechanism second.** The developer asked whether it works, not how it is built.

## Sounding like a person

Thai written by translating an English sentence stays technically correct and reads wrong. Common tells, and what to write instead:

| Instead of | Write |
|---|---|
| "สิ่งนี้ทำให้เกิดปัญหาที่ว่า…" | "ผลคือ…" |
| "ขออนุญาตแจ้งว่าได้ทำการตรวจสอบแล้ว" | "ตรวจแล้ว" |
| "จากการที่ได้ทำการวิเคราะห์พบว่า" | "ดูแล้วเจอว่า" |
| "มันถูกเรียกใช้โดย…" | "…เป็นตัวเรียกมัน" |
| "ในการที่จะทำให้ X ทำงานได้" | "จะให้ X ทำงาน ต้อง…" |

Also:

- **Do not restate the question before answering it.**
- **Do not narrate what you are about to do at length** — do it, then say what happened.
- **Structure only when the content is structured.** A table for genuinely tabular facts; otherwise sentences. Bolding everything is the same as bolding nothing.
- **No filler register** — *"หวังว่าจะเป็นประโยชน์"*, *"ยินดีช่วยเหลือครับ"*, an apology in front of every correction.

### The shape is part of the register, and it is the part that slips first

Measured on 2026-08-12: an agent handed this skill and asked four questions about a repository answered with four `##` headings, two tables, and bold on most lines. Every word-level rule held — identifiers exact, concepts in Thai, hedges kept. The shape rule did not. It was a bullet, and everything else here is an example.

| Asked | Wrong shape | Right shape |
|---|---|---|
| "gate บล็อกอะไรได้บ้าง" | `##` หัวข้อ + ตารางสามคอลัมน์ + ตัวหนาทุกบรรทัด | ย่อหน้าเดียวบอกว่ามันทำงานตอนไหน แล้วรายการสั้น ๆ สี่ข้อ |
| "อันนี้เสร็จยัง" | ตารางสถานะ | "เสร็จแล้ว · เหลือ `README.en.md`" |
| "ทำไมมันพัง" | หัวข้อ Problem / Root cause / Fix | สามประโยค |

**Default to prose.** A heading is for an answer the developer will *navigate*; a table is for facts that genuinely share columns; bold is for the one thing they must not miss. Three headings in a four-paragraph answer means none of them is doing anything.

## Before → after

Real sentences from this repo's own sessions, with what they should have been.

| Before | After |
|---|---|
| "กฎคัดกรอง: เปลี่ยนสิ่งที่ harness/guard ทำ = คุ้ม · เปลี่ยนแค่สิ่งที่ skill พูด = รับมรดกความล้มเหลวเดิม" | "กฎคัดกรอง: ถ้าแก้แล้ว **ตัวตรวจอัตโนมัติทำงานต่างไป** คุ้มที่จะแก้ · ถ้าแก้แค่ **ข้อความใน skill** มันก็เจอปัญหาเดิม คือ agent อ่านแล้วไม่ทำ" |
| "ตัวเลขนี้ไม่มี exposure denominator" | "ตัวเลขนี้ใช้ไม่ได้ เพราะเรานับเฉพาะครั้งที่พลาด ไม่รู้ว่าจากทั้งหมดกี่ครั้ง เลยคิดเป็นอัตราส่วนไม่ได้" |
| "hook enforce ได้แค่ checkable action ไม่ใช่ process discipline" | "hook ตรวจได้แค่สิ่งที่ตรวจได้จริง เช่น PR อ้าง issue ไหม, test ผ่านไหม · มันดูไม่ออกว่า review ลึกหรือลวก" |
| "`.claude/t4.json` ไม่อยู่บน `main` ทำให้ marker guard ทำให้ทุก hook exit silently" | "`.claude/t4.json` ไม่มีบน `main` · ทุก hook เช็คไฟล์นี้ก่อน ไม่เจอก็ออกเงียบๆ เท่ากับไม่มี gate เลยสักตัว" |
| "ผมได้ทำการรวมโค้ดจากสาขานี้เข้าสู่สาขาหลักเรียบร้อยแล้ว" | "merge เข้า `main` แล้ว" |
| "แก้เสร็จแล้วครับ" (จริง ๆ แก้ 3 จาก 5 จุด) | "แก้ไป 3 จาก 5 จุด · เหลือ `README.en.md` กับ `plugin.json`" |

The fifth row is the over-correction: `merge` and `main` are the developer's own words, so translating them made the sentence worse. Plainness is not the same as avoiding English.

## Red flags

These thoughts mean stop and rewrite the sentence:

| Thought | Reality |
|---|---|
| "ศัพท์นี้แม่นกว่า" | แม่นกว่าสำหรับคุณ · ถ้า dev ต้องเดา มันไม่ได้สื่ออะไรเลย |
| "เดี๋ยวอธิบายทีหลัง" | ทีหลังไม่มา · อธิบายในประโยคเดียวกัน หรือไม่ก็อย่าใช้คำนั้น |
| "เขาเป็น dev น่าจะรู้" | รู้ `merge` ไม่ได้แปลว่ารู้ `observational equivalence` |
| "พูดง่ายๆ แล้วเดี๋ยวไม่ครบ" | ตัดศัพท์ ไม่ใช่ตัดความจริง · ถ้าง่ายแล้วผิด ให้ใช้คำเดิมแล้วอธิบาย |
| "ใส่ตารางไว้ดูเป็นระเบียบดี" | ตารางที่ข้อมูลไม่ได้เป็นตาราง คือย่อหน้าที่อ่านยากขึ้น |
| "เขียนอังกฤษเร็วกว่า" | ความเร็วของคุณไม่ใช่เหตุผล · ภาษาที่ใช้คือภาษาของ dev |
| "ต้องแปลทุกคำให้เป็นไทย" | ผิดอีกด้าน · identifier และคำที่ dev ใช้เอง ห้ามแปล |

## What this does not touch

This skill governs **prose the developer reads**. It changes nothing about:

- **Identifiers** — paths, commands, symbols, labels, branch and PR names stay English and byte-exact (`t4-dev-workflow`).
- **Code, commit messages and inline comments** — English, unchanged.
- **Tracker bodies** — issue, PRD and PR bodies stay **bilingual**, English plus a full Thai mirror of the same depth (`t4-dev-workflow`). A mirror is not a summary, and this skill is not licence to shorten one.
- **The shipped skills and docs in this repository** — they are written in English for a public audience.
- **Accuracy, evidence and every gate.** Register is the last thing you decide, after the answer is already true.

## Cross-skill

- Which language, and the bilingual tracker rule → **`t4-dev-workflow`**.
- The claim registers this skill must never soften (verified / hypothesis / unknown) → **`t4-dev-workflow`**, *No verdict before evidence*.
- Reporting an unattended batch in one digest → **`t4-afk`**; the digest is prose the developer reads, so this register applies to it.
