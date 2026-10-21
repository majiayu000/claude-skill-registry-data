---
name: profile
description: Fill profile.md from the person's existing CV and an interview for the gaps; record their corrections as rules.
disable-model-invocation: true
---

# /profile

Files: `templates/`, `scripts/`, `docs/`, `examples/` and `routines/` are in the method root, `${CLAUDE_PLUGIN_ROOT}` (the clone holding this skill when that is not replaced by a path); every other relative path is in the workspace, the current folder. Before acting on the person's behalf, read `profile.md`, `docs/rules.md` and the workspace `rules.md`; the workspace one wins on conflict.

This skill fills `profile.md` by asking questions, in the person's language, a few at a time. The skill is done when every field of `templates/profile.md` is filled and confirmed, or empty with the skill that needs it named to the person.

Modes:
- `/profile` with an empty or template `profile.md`: step 0, then the interview.
- `/profile` with a filled one: show what is missing or stale and update only that.
- `/profile add rule <text>`: record it as `docs/rules.md` "Setup and corrections" says.

## 0. Start from the CV they already have

If `cv/old/` holds a CV (PDF, DOCX, Markdown, or a LinkedIn "Save to PDF" export), use it. Otherwise ask:

1. Drop your current CV into `cv/old/` or point me at it; I fill in everything it contains and ask only for what is missing (recommended: ten minutes instead of forty)
2. No CV yet, interview from a blank profile

With a CV:

- A file the person points at is copied into `cv/old/` under its original name; never modify the original.
- Extract the text into `cv/old/<name>.txt` (`/cv` builds the CV from it). PDF: read the file directly and write out its text. DOCX: `unzip -p file.docx word/document.xml | sed 's#</w:p>#\n#g; s/<[^>]*>//g'`. Markdown or text: as is.
- Fill `profile.md` from it, field by field:
  - Identity: everything the CV states (name, email, phone, address or city, LinkedIn, GitHub, date of birth, citizenship, work authorization, availability, highest education, languages with levels). Copy as written; keep names, levels and spellings as the CV has them.
  - Stack: every technology the CV names, in the CV's order for now. Years come from the job entries that list the technology: sum the spans, round down, mark the number as derived. A technology named only in a skills line, with no job behind it, gets `?` in Years.
  - Target: roles and levels read off the title line and the most recent jobs, written as a proposal and marked as derived.
  - Interview facts: team setup and last-job facts the CV states (team size, what they owned). Everything else stays empty.
  - Files: the imported file under `cv/old/`.
- Show one short list back, in two parts: "Taken from your CV" (facts copied as written) and "Derived, please check" (years per technology, roles, levels, stack order). Copied facts stand unless they correct them; derived values need a yes. Apply their corrections.
- Then run the interview below, skipping every field that is filled and confirmed. Say at the start how many fields are left.

The import never lowers anything: if the CV undersells a language level or years with a technology, ask before writing the CV's number. If the CV and the person disagree on a date, the person wins and the CV gets fixed in `/cv`.

## Interview

Ask in blocks, only the fields still empty after step 0, proposing each block's defaults. Confirm each block back in two lines before moving on.

0. **Agent settings.** Report language; default: the language the person writes to the agent in (recommended), else English. Style notes, optional.
1. **Identity.** Name, date of birth, the one email address to use everywhere, phone, address, LinkedIn, GitHub, citizenships, work authorization per country with the exact wording for forms, visa sponsorship, availability, highest degree, languages with CEFR levels. On languages: push gently against underselling; the level they claim in forms is the one they can defend on a call. Default for the email: one address, firstname.lastname style (recommended); whatever they use now.
2. **Target.** Roles, levels, work modes, markets and platforms, hard skip filters, growth targets, differentiators. Ask what they would never want to be applied to. Ask which adjacent roles they would take on purpose. Defaults:
   - Levels applied to: the current level and one above (recommended); the current level only.
   - Work modes: remote plus hybrid in the home city (recommended); remote only; onsite included.
   - Hard skip filters: the template's defaults (consulting with client-site work, stacks they will not work in, internships, lead and staff titles, freelance only) (recommended); a shorter list.
   - Growth targets: adjacent roles in the same stack one level down (recommended); none.
3. **Stack.** Build the table: the order they want technologies presented, and years per technology. Tell them this order is used everywhere, including the first sentence of every message. Then the title level claimed in free text. Defaults:
   - Stack order: the technology they use daily and want to be hired for first, everything else after (recommended); alphabetical or by years.
   - Title level claimed in free text: none, the title line carries role and stack (recommended: keeps mid and senior roles both open); the level they hold now.
4. **Location by market.** Default city and phone, then exceptions per market or platform. Make sure city, "about" text and phone agree inside one market. Default: the real city everywhere (recommended); a local city on regional platforms where a foreign city gets applications dropped before a human sees them (then phone and "about" text must agree).
5. **Salary.** One figure per market, annual, in the local currency. Tell them a range gets the bottom of the range. Default: one number per market in the upper half of the local range for the role (recommended); the person's own number.
6. **Interview facts.** Write the self-introduction script with them in the structure of A1 in `docs/interview-method.md`: who I am and my core stack, what I own now or most recently with one number, where I started (short), one memorable personal detail, languages once. The intro is done when the person has read it aloud once and it runs 60 to 90 seconds, about 150 to 220 words. Then: why the last job ended (external reason, no blame, two or three sentences), team setup at the last job (never overclaim ownership), the one story for hardest problem / proud of / under pressure, strength and its flip-side weakness with the system against it, questions they always ask at the end.
7. **Files.** Default CV version, per-market versions, photo path, the imported CV under `cv/old/` if there is one.

## After writing

- Re-read `profile.md` and check it against `docs/rules.md` "Writing on my behalf".
- Push the search preferences to JobCubby: `update_preferences` (target role, seniority, work modes, locations, salary, job types, industries). Read the existing preferences first and send only what changed. The JobCubby profile itself is written by `/cv` from the approved CV.
- If `.data.git/` exists, run `"${CLAUDE_PLUGIN_ROOT}/scripts/data" save "profile <name>"`.
- Tell the person what is still empty and which skill will ask for it.
- Close with the next step: `/cv` when no approved CV exists yet or a fact the CV carries changed (it re-approves the CV); otherwise `/profiles` when a contact fact or the location table changed.
