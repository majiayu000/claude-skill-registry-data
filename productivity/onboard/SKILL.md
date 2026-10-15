---
name: onboard
description: Onboard or refresh the AI OS context by interviewing the user with the 7-question intake. Populates context/, seeds connections.md, and logs the run in decisions/log.md. NEVER auto-fills identity from session environment — all PII fields require explicit user input. Triggered by /onboard or when the user explicitly asks to onboard / re-onboard / refresh context.
disable-model-invocation: true
---

# /onboard — AI OS Onboarding

> Personal/business context layer. Adapted from AIS-OS (Nate Herk).

## When to use
- The user runs `/onboard` (default invocation)
- The user explicitly asks to "onboard," "set up the AI OS," "refresh context," or "redo the intake"
- A new fork of this repo lands and the operator has not yet populated `context/`

## When NOT to use
- The user is asking what's loaded — use `/session-bootstrap` instead
- The user wants to add a single fact to memory — write directly to the relevant file in `memory/`
- The user is mid-task and wants to keep working — defer onboarding

---

## Hard rules (non-negotiable)

### Privacy guard
1. **Never auto-fill identity fields from session environment.** Specifically: do NOT read `userEmail`, `gitStatus.user`, `os.username`, OS environment vars, or any system-reminder injection to populate `context/About Me.md` snapshot fields like Name, Email, Handle.
2. **Always show the privacy warning first** (from `aios-intake.md` § "Privacy warning — read before answering") before asking the first question.
3. **If the user types content that looks like a credential** (matches `sk_live_`, `Bearer `, `xoxb-`, JWT pattern, base64 token, email + colon + secret pattern), refuse to write it and ask them to redact.
4. **If the user pastes an email address into a free-form answer**, ask once: "I noticed an email address in your answer. Public repo — keep, generalize, or remove?" Default to remove if no answer.

### Scope guard
- Write only to: `context/*.md`, `connections.md`, `decisions/log.md`.
- Never modify `settings.json`, install MCP servers, install plugins, or run shell commands beyond `git status` to confirm clean working state.
- Never make outbound network calls from this skill.

### Idempotency
- If `context/*.md` already has non-placeholder content for a section, ASK before overwriting.
- Always preserve previous content as a moved block in `archives/<date>-pre-onboard/` when overwriting.

---

## Inputs
- None required. The skill is fully interactive.
- Optional flag (passed as text by the user): `--quick` runs questions 1-2 + 7 only; the rest stay placeholders.

## Outputs
- Updated `context/About Me.md` (snapshot fields blank unless user typed them; role/style/depth filled from prose)
- Updated `context/About Business.md`
- Updated `context/Priorities.md` (this-week populated from question 6 constraint)
- Updated `context/Voice Sample.md` (if user provided sample text in question 5)
- Updated `context/Operating Preferences.md`
- Updated `connections.md` Tier-4 rows from question 3
- New entry in `decisions/log.md` with date, automation candidates, and "what to focus on this week"

## Steps

1. **Pre-flight checks:**
   - `git status --short` — warn if there are uncommitted changes that would mix with onboarding edits
   - Check whether `context/About Me.md` is still placeholder (if not → ASK before overwriting)
   - Show the privacy warning from `aios-intake.md`

2. **Confirm intent:**
   > "I'm about to ask 7 questions. Answers go into the repo's `context/` files. Privacy: do not paste credentials, customer PII, or anything you wouldn't share publicly. Proceed?"

3. **Ask the 7 questions** (one at a time, wait for answer, do not batch):
   - Q1: Who you are
   - Q2: Projects and responsibilities
   - Q3: Current tool stack (use the table format from `aios-intake.md`)
   - Q4: Repeated work (3-7 examples)
   - Q5: Operating preferences + voice sample (optional)
   - Q6: 10x question (the constraint)
   - Q7: Hard limits

4. **PII scan** on each answer before saving. If a credential pattern or email is detected, pause and ask.

5. **Distill** answers into the file structure. Preserve user's actual wording in voice-relevant sections (Q5 voice sample, Q4 examples). Generalize where structure helps (Q3 → table, Q6 → priority).

6. **Diff preview**: show each new file's diff before writing. The user can accept, edit, or skip.

7. **Save** the accepted files. Move any overwritten content to `archives/<YYYY-MM-DD>-pre-onboard/`.

8. **Log** the run in `decisions/log.md`:

   ```markdown
   ## YYYY-MM-DD — Onboarding completed (or refreshed)

   **Decision:** Populated context/* from intake. <N> automation candidates surfaced.

   **Automation candidates:**
   - <Q4 item 1>
   - <Q4 item 2>
   - ...

   **Constraint identified:** <Q6 answer condensed>

   **Status:** Active.
   **Follow-up:** Run `/level-up` next Friday to pick which candidate to build first.
   ```

9. **Validation question** — END WITH:
   > "What should I focus on this week?"
   >
   > If the OS routes correctly using your answers, onboarding worked. If not, tell me what's missing and I'll update the relevant context file."

---

## Failure modes and recovery

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| User answers are very short ("idk") | Bad time to onboard, or user doesn't have answers | Suggest: "Skip onboarding for now; come back when you have 20 quiet minutes." Do not write half-answers. |
| User pastes a credential | They didn't read the privacy warning carefully | Refuse to save, redact, restate the warning, continue |
| Existing `context/*.md` has rich content | Re-onboarding | ASK explicitly. Default to merge, not overwrite. |
| Skill mid-flight, session dies | Lost answers | On next run, check for `state/onboard-progress.json` (if you implement that) |

---

## Reference files
- `aios-intake.md` — the canonical 7-question interview
- `references/3ms-framework.md` — the operator mindset this skill assumes
- `references/four-cs-framework.md` — what the four context files map to
- `connections.md` — where Q3 lands

## Improvement loop
After every `/onboard` run:
1. Did the user need to correct the same field twice? → that field's prompt is unclear, fix in this skill
2. Did the user paste a credential? → strengthen the PII detector pattern
3. Did the validation question reveal missing routing? → that's a `/level-up` candidate, not an onboarding problem

Update this skill when failures repeat. Failure-to-learning is the rule (`docs/RUNBOOK.md`).
