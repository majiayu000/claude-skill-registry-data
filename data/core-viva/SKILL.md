---
name: core-viva
description: Rapid-fire CS fundamentals viva covering Operating Systems, DBMS, Computer Networks, OOP, and SQL (with real query execution), the core-subject questions asked in technical placement rounds. Adaptive difficulty, instant feedback per answer, and a per-subject score. Use when the user wants to revise or be quizzed on OS, DBMS, CN, OOPs, SQL, CS fundamentals, core subjects, or theory questions for interviews.
---

# Core viva

Fast, adaptive, interview-style questioning on CS fundamentals. The format is the one used in placement technical rounds: short questions, short answers, the interviewer probing deeper whenever an answer is shaky.

## 0. Setup

1. Call the Skill tool with "cracked-profile".
2. Settle the scope in one line, with defaults: **subjects** (default: all five, OS · DBMS · CN · OOP · SQL), **number of questions** (default 15), **level** (default: adaptive). If the user names a subject or a topic ("only deadlocks", "normalization"), run just that.
3. **Company mode**: if the user names a company, call the Skill tool with "company-intel". Weight subjects and topics by what its brief reports for technical rounds (service and mass-recruiter archetypes lean heavily on OS/DBMS/OOP/SQL theory; product companies on DBMS, SQL and OOP design; networking-heavy companies on CN). If the brief has web-sourced, reported core questions, include them, labelled "reported for <Company>". With no company, don't ask; use the default spread.
4. Use the syllabus in [SYLLABUS.md](SYLLABUS.md) to pick topics. Spread questions across topics. Never ask two questions from the same topic in a row unless you're probing.

## 1. The loop

Ask **one question at a time**. Number them (`Q4/15 · DBMS · medium`).

After each answer, give instant feedback in at most four lines:

```
✅ Correct  /  🟡 Partial  /  ❌ Incorrect
<the ideal 1–3 sentence interview answer>
<if partial or wrong: the specific thing they missed or got wrong>
```

Then move on. Adaptive rules:

- Two correct in a row → raise difficulty one step.
- Wrong → ask **one** follow-up probe on the same topic at an easier level, to tell a gap from a slip.
- "I don't know" is a valid answer. Treat it as incorrect but say it's the right thing to say in a real interview, rather than bluffing.
- Mix question types: definition, "difference between X and Y", "what happens when…", scenario ("Your query is slow. What do you check?"), and small numericals (page faults with FIFO/LRU, subnetting, CPU scheduling waiting time).

## 2. SQL questions run for real

For SQL questions, give a tiny schema with sample rows and ask for a query. Say the dialect up front: "I'll run this in SQLite; MySQL/PostgreSQL syntax is fine where it's equivalent." Check `sqlite3 --version` once (window functions need 3.25+, `FULL OUTER JOIN` and `RIGHT JOIN` need 3.39+); if the installed version is older, use Python's `sqlite3` module or say which features you can't run. When they answer:

1. Create a temp SQLite database (`sqlite3` is preinstalled on macOS and most Linux systems; else use Python's `sqlite3` module), load the schema and rows, and **run their query**.
2. Also run your reference query, and compare the results.
3. Show both result sets if they differ. Accept any query that returns the correct result, including equivalent MySQL/PostgreSQL syntax you had to translate to run it (say what you translated: `TOP`→`LIMIT`, `ILIKE`, `::` casts…). Flag syntax that wouldn't run on MySQL or PostgreSQL, since interviews usually use one of those. Mention style issues separately.

Typical SQL targets: joins (inner/left, self join), GROUP BY + HAVING, Nth highest salary, duplicates, window functions (RANK, ROW_NUMBER), subqueries vs joins, NULL handling.

## 3. Results

After the last question:

1. A per-subject table: `Subject | Asked | Correct | Partial | Score/10`.
2. **Gap list**: the specific topics they got wrong, each with a one-line "revise this" pointer (e.g. "Deadlock: Coffman conditions and Banker's algorithm").
3. The scorecard, via the Skill tool with "cracked-profile", one dimension per subject asked. Weak-spot tags are the topic slugs (`os-deadlock`, `dbms-normalization`, `cn-tcp-handshake`, `sql-window-functions`).
4. Offer: "Run a deep-dive on <weakest topic>?" A deep-dive is 5 escalating questions on one topic.

## Tone and accuracy

- Keep the pace brisk. No lectures between questions.
- **Numericals are computed, not recalled.** For page faults, CPU scheduling, subnetting and similar, compute the reference answer with a short Python snippet before grading, and say "reference checked by execution".
- Be precise. Fundamentals have right answers, and an ambiguous "ideal answer" teaches the wrong thing. If a question has textbook-dependent variants (e.g. number of OSI layers vs the TCP/IP model), say so.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
