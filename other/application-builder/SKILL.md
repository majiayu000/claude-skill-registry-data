---
name: application-builder
description: Build a targeted resume and cover letter for a role folder that already has a job description and role analysis. Runs iterative adversarial review rounds until the materials stabilize, then hands off for human review before submission.
argument-hint: "<role folder path>"
license: MIT
---

# Application Builder

Take a role folder with a job description and a role analysis. Produce a resume and a cover letter that have already survived a seven-agent review.

**Announce at start:** "Building materials for $ROLE. Reading the JD, the role analysis, and the profile."

**Arguments:**
- `$1` — path to a role folder containing `job_description.md` and `role_analysis.md`

**Example:**
```
/slushpile:application-builder applications/Acme/Engineering/Staff-SRE
```

## Prerequisites

Read all of these before writing anything:

- `profile.md` — the source of truth for every factual claim. Nothing goes on a resume that is not in here.
- `stories.md` — the shortlist the cover letter's story comes from
- `preferences.yaml` — constraints, claimed differentiators, and `voice.agent`
- The definition of the agent named in `voice.agent` — how this person writes
- The role's `job_description.md`
- The role's `role_analysis.md`

**Check `voice.is_mine` in `preferences.yaml` before drafting the cover letter.** If it is false, the user has not yet generated a voice agent from their own writing and the pipeline is about to write in a stranger's voice. Say so once, plainly, and point them at `https://github.com/aaddrick/written-voice-replication`. Then continue if they want to — a placeholder voice is fine for seeing the pipeline work, and it is not fine for a letter they actually send. They cannot make that call if nobody tells them.

If `role_analysis.md` does not exist, stop and run `/slushpile:job-board-search` for this company first, or write the analysis by hand. Building materials without a pool assessment means targeting the posting instead of the queue, and the queue is what decides.

**Every `templates/...` path in this file is relative to the plugin, not to the workspace.** The working directory is the user's job-search directory and does not contain them, so a bare `templates/cover_letter.tex` resolves to nothing. Resolve them against the directory this skill file was itself loaded from — that works on every harness, where a harness-specific plugin-root variable does not.

## Phase 1: Angle

### 1a. Pick a base resume

Look at resumes already in the workspace. Choose the closest starting point by, in order: same company, similar function, similar level, most recent. Recency matters more than it looks — the newest resume carries every formatting and content fix made since the older ones.

With no close match, start from `templates/resume.tex` in the plugin directory, or from the most recent resume in the workspace.

`templates/resume.tex` and `templates/cover_letter.tex` are a matched pair: same palette, same fonts, same header treatment. **When you start either one from the plugin templates, start both from them.** The resume and the letter are the only two documents in the application a screener sees side by side, and a letter in a different typeface than the resume reads as two documents assembled from two sources.

Both templates build under XeLaTeX and fall back to DejaVu when the house fonts are absent, so a missing font changes how they look and never whether they compile. If `xelatex` is not installed at all, say so once and write both documents in Markdown instead — every skill downstream of here works on extracted text and none of them require `.tex`. Silently producing a `.tex` file the user cannot build is the failure worth avoiding.

### 1b. Extract the angle from the role analysis

Pull out:

- **Pool position and tier** — this calibrates how aggressive to be. A p40 candidate and a p85 candidate write different letters.
- **Highest-EV channel** — a cold submission and a referral want different documents. A referral letter can assume a sympathetic reader. When the highest-EV channel is a warm referral and the Referrals table in `job_search.md` holds no `strong` or `moderate` contact at this company, say so before drafting and name `/slushpile:outreach $1`. The materials still get built; the user just gets told, once, that the expensive part of this application is aimed at the channel the assessment ranked second.
- **Top strengths** — what to lead with
- **Top gaps** — what the materials must not draw attention to
- **Narrative angle**, if the analysis has one

### 1c. Find the thesis

The thesis is not "I am qualified for this role." It is one argument that makes this person interesting for this specific seat.

Ask: what does this candidate bring that most applicants for this role will not? What combination creates value that the pool does not already have? What is the single strongest reason to interview them despite the gaps?

Expressible in one sentence. Proven across the whole letter.

**The thesis must be company-dependent.** The test: swap the company name for a direct competitor. If the thesis still works, it is not specific enough and the hiring manager's swap test will catch it.

A thesis that passes reads like: *"Most capacity planning candidates come from one side of the business. This company's dual identity as manufacturer and cloud provider is the rare case where running both is the qualification."* Swap in a pure cloud provider and it collapses. That is the property you want.

A thesis that fails reads like: *"I have deep experience in infrastructure program management and a track record of delivery."* True of everyone in the queue.

### 1d. Design the hook

The hook is the first line. It presents the angle, not the background.

**Never open with background.** "I have spent twelve years doing X" is the most common opening in the bottom half of the pile, and a fatigued reader has seen it forty times that day before reaching this one.

Draft three hooks. Pick the strongest. It must be unique to this letter — check the "Used in" lines in `stories.md` and any recent cover letters in the workspace.

A hook lands when it makes the reader curious about someone they would not otherwise interview. It leads with a concrete detail, a reframe, or a provocation. Not a credential.

Strong: *"We started with seven assumed defect categories. We found hundreds."* — *"Everyone applying to this role knows data platforms. Almost nobody has delivered under production SLAs written into law."* — *"I am not a developer educator who has read the docs. I am a practitioner who writes."*

Weak: *"I have spent the last decade running infrastructure programs."* — *"Every responsibility in this posting maps to something I do now."* The first is background. The second is a claim, not a hook.

### 1e. Pick the story

One story, from `stories.md`. It must prove the thesis.

Check the "Used in" field. Reusing a story across two applications to the same company is the specific failure this field exists to prevent.

One vivid story with room to breathe beats three summary paragraphs. Give it the space.

## Phase 2: Resume, First Draft

### 2a. Adapt the base

**Header.** Update the tagline to match the role's function. Add location targeting if the role is site-specific and the candidate would relocate. Keep contact details in the document body, never in a `\header` — roughly a quarter of ATS drop header content.

**Contact line.** Fill the template's placeholders from `identity.name`, `identity.location`, and `identity.links` in `preferences.yaml`, with phone and email from `profile.md`. **Delete the separator and the link for anything empty in `identity.links`** — the template ships a `github` and a `linkedin` slot because most candidates have both, and a user who filled in `website` or `portfolio` instead gets them dropped unless this step reads the whole block. A resume that goes out reading `linkedin.com/in/USER` is the single most expensive typo in the pipeline, and it survives every downstream review, because the review agents are handed extracted text and read that string as a link the candidate actually has.

**Summary.** Rewrite in two or three sentences for this specific role. Lead with the strongest match to the core function.

Do not paste phrases from the posting. If a sentence in the summary could be copied out of the JD, rewrite it in the candidate's own words. A screener reading their own posting back at them stops reading, and the ATS gains nothing the Skills section is not already providing.

**Skills.** Audit against the JD. Every explicit requirement and preference the candidate legitimately has should appear as a keyword, weighted into this section where ATS scoring is highest.

Add JD-specific terms the candidate can claim — check `profile.md` for the evidence. Add bridging vocabulary where the role analysis identified a domain gap that the candidate's experience maps to by analogy.

Do not add a keyword the candidate cannot defend in an interview. The requirements analyst checks Skills entries against the work history and will flag anything unsupported.

**Experience bullets.** Reorder to lead with what this JD cares about. Every bullet passes the "So What?" test: baseline, action, significance. Expand any role that `profile.md` shows is under-developed relative to this posting. Add quantified outcomes where the profile has numbers the current resume drops.

Vary bullet length deliberately. Bullets all within five words of each other is a tell the fatigued reader catches before consciously noticing why.

**Section order.** It is a per-application decision. Move open-source and writing above experience when the role weights public technical credibility over tenure.

### 2b. Compile and verify

Build the PDF. For LaTeX: `latexmk -xelatex <file>.tex && latexmk -c`.

Check page count. One to three pages is fine — **do not force it onto fewer pages by cutting substance.** A two-page resume that keeps the evidence beats a one-page resume that keeps the layout.

Check for new overfull-hbox warnings. Extract with `pdftotext <file>.pdf -` and read the result. That extraction is what an ATS sees and what every review agent will be handed. If it reads badly, fix the document, not the review.

## Phase 3: Cover Letter, First Draft

**When the posting calls the letter optional, `application_policy.cover_letter_when_optional` decides.** The Notes section of `job_description.md` records whether the form has a letter field and whether it is required. If the letter is optional and that setting is false, skip 3a through 3d and Phase 3.5, go straight to 3e, and say so in the handoff — the user has decided their hours are better spent elsewhere, and a letter written against that decision is an hour taken from the next application.

**Skipping the letter never skips 3e.** Screening questions are where the argument goes when there is no letter, and dropping both leaves a resume submitted with no prose at all — the opposite of what the setting is for.

Write the letter whenever the posting requires it, whenever the form's structure is unrecorded, and whenever the setting is true. Only a posting that says the letter is optional puts the setting in play; unknown is not optional.

### 3a. Draft

The letter's container is `templates/cover_letter.tex`, or the letter from whichever application you took the base resume from in 1a. Take the container first and draft into it, rather than drafting loose prose and formatting it afterwards. The template's header carries the requisition ID and the exact role title, which large employers route on, and a letter assembled at the end is where that line gets dropped.

**Copy the contact line from the resume character for character.** A phone number or a city that differs between the two documents is the kind of small inconsistency a fatigued reader notices, and the next thing they do is start looking for more of them.

Then dispatch the voice agent named in `preferences.yaml` under `voice.agent`:

```
Write a cover letter for [role] at [company].

Thesis: [from 1c]
Hook:   [from 1d]
Story:  [full story text from stories.md]

Required, in order:
1. Open with the hook. The first sentence presents the angle, not the background.
2. Tell the story with scene, stakes, and resolution. Give it room. Do not
   compress it to a sentence.
3. No gap paragraph. Do not name what the candidate lacks.

Include if the thesis allows:
- Company-specific content framed as "I have built what your tools formalize",
  never as "here is what your product does"
- Mapping from the candidate's operational patterns to this company's systems

Structure: 4-6 paragraphs, roughly 350-500 words. Length serves the thesis,
not a target.

Close on a concrete detail or a reframe. Never "happy to discuss further".

Profile context:
[the relevant sections of profile.md for the experience being referenced]
```

The no-gap-paragraph rule is worth understanding rather than just following. A gap paragraph becomes the loudest sentence in the letter, and it hands a preferred qualification more weight than the hiring manager would have given it unprompted. The resume already shows the gap honestly. The letter's job is to argue for an interview. Gaps get addressed in the interview, if they come up at all.

### 3b. Voice pass

Dispatch the voice agent a second time, on the draft:

```
Tighten this cover letter to the voice profile. The thesis, structure, and
content are correct. Only the voice needs work.

[draft]

Keep the thesis, structure, and every factual claim exactly as they are.

Preserve all company-specific details, proper nouns, product names, team names,
and role-specific framing. Do not generalize for style. Company specificity is
load-bearing and it is the first thing a style pass destroys.
```

### 3c. Quality gate

Every item passes before the letter goes to review.

**Structure.** No two paragraphs make the same point in different words. Every paragraph serves the thesis. Count the distinct topics — more than three or four means cut the weakest.

**Hook.** Paragraph one opens with something other than background. The hook is unique to this letter.

**Story.** Exactly one, told with scene and stakes and resolution, not compressed.

**Gaps.** No gap paragraph exists.

**Company specificity.** The thesis collapses under a company swap. The company-specific details are concrete — product names, team names, mission — not "your platform".

**Density.** No paragraph carries more than about three claims or metrics. A dense metric paragraph means the reader retains none of them. Keep the three strongest, move the rest to the resume.

**Anchored metrics.** "101 issues through the pipeline" with no timeframe and no outcome is noise. Anchor it or cut it.

**Closing.** The final line lands on a concrete detail or a reframe.

**Company name.** It appears at least once in the body, beyond the header. Without this the swap test fails on a technicality.

### 3d. Ground every company reference

Every company-specific claim gets verified against a real source. The drafting process hallucinates product names, team structures, and strategic context confidently, and a single wrong product name kills credibility faster than any other error in the document.

Verify: product and platform names, spelling and current branding, what the product actually does; team names and org structure; mission statements, not paraphrased from memory; technical claims about their stack; any recent news or funding referenced.

How: check `job_description.md` first — most of it is in the posting. Then `role_analysis.md`. Anything in neither gets verified by web search or the company's own site before it stays. If it cannot be verified, cut it or replace it with something from the JD that can.

The failure modes worth knowing by name: attributing one company's product to a competitor; attributing a feature to the wrong product inside a multi-product company; using a description that predates a rename or an acquisition; inventing a team name that sounds plausible; describing what a product does by reasoning from its name.

### 3e. Screening questions, when the form has them

Check the Notes section of `job_description.md`. `/slushpile:job-board-search` records the application form's structure there: free-text screening questions, years-of-experience dropdowns, whether a cover letter field exists at all.

**If the form has free-text questions, answer them here.** Write them to `form_answers.md` in the role folder.

This is not optional polish. Many application forms never accept a cover letter, and on those the screening answers are the only prose a human reads — the entire argument for the candidate, in three boxes of 200 words. Materials that stop at a resume and a letter leave the actual submission to be improvised at 11pm in a browser tab, which is where the voice work, the grounding, and the thesis all get discarded.

Dispatch the voice agent named in `voice.agent`, once, with every question at the same time:

```
Answer these application form questions for [role] at [company].

Questions, verbatim from the form:
[each question, with its stated word or character limit]

Thesis: [from 1c]
Story already used in the cover letter: [one line — do not retell it]

Profile context:
[the relevant sections of profile.md]

Rules:
1. Answer the question that was asked. A form answer that pivots to a prepared
   pitch reads as evasion, and the reader has the question in front of them.
2. Respect the stated limit. Where a limit is given in characters, count them.
3. Do not retell the cover letter's story. Reach for a different one, or answer
   without a story.
4. Concrete over comprehensive. One specific answer beats three hedged ones.
5. No gap paragraphs, same as the letter.
```

**Answer the asked question, not the adjacent one you have better material for.** These are read directly beside the question text, which is exactly the position where a pivot is most visible. It is a different failure mode from the cover letter, where there is no prompt on the page to answer to.

**Respect the limits literally.** A form that truncates at 200 characters truncates mid-word, and the reader sees an answer that stops in the middle of a sentence. Count, do not estimate.

**Do not answer a dropdown or a yes/no gate here.** Those are the user's to answer, they frequently have legal weight — work authorization, sponsorship, compliance attestations — and a suggested answer to one of them is the single place in this pipeline where being helpful shades into filling in a legal declaration on someone's behalf. Record what the form asks. Let the user answer it.

## Phase 3.5: Humanize

### 3.5a. Strip AI tells from the letter

Run `/slushpile:removing-ai-tells` on the cover letter file. It runs up to three passes through fresh voice-agent instances with you reviewing every change between them.

**Run it on `form_answers.md` too, if 3e produced one.** Short answers are where AI tells are densest and most detectable — a 150-word box has no room for the specificity that makes longer prose read as human, so the generic constructions have nothing to hide behind. Skipping the answers because they are short inverts the actual risk.

**Reject any change that:**

- Collapses a deliberate scope-escalation fragment sequence. *"$30M CAPEX. Four facilities. Seven clients."* is a human writing move and often the highest-impact line in the letter.
- Adds missing subjects to a punchy inventory list and kills the delivery
- Removes a structural transition that is doing real work between sections
- Contradicts something the user's voice agent documents as this person's habit. The voice agent outranks the checklist. Someone whose corpus is full of triplets keeps their triplets — the pattern is a tell in general and a fingerprint in their case.

### 3.5b. Humanize the resume

Send the resume source to the voice agent for a line-by-line pass.

Replace resume-generator verbs with what a person would say: *Managed* becomes *Ran*. *Conceptualized* becomes *Proposed*. *Engaged* becomes *Brought in*. *Established* becomes *Set up*. *Achieved consensus* becomes *Got buy-in*. *Engineered pluggable* becomes *Added pluggable*.

Break participial phrase endings into separate sentences. Restore missing articles — *"Built golden dataset"* becomes *"Built the golden dataset"*. Cut consulting jargon.

Preserve every factual claim, all LaTeX or Markdown formatting, and the section structure. Keep the professional register: this is de-stiffening, not casualizing.

Recompile afterward and check the page count. Humanizing adds words.

### 3.5c. Align the numbers

Every metric appearing in both documents must match, and must match `profile.md`'s "Numbers You Can Defend" table. Check test counts, resource counts, percentages, dollar figures, stars, downloads.

A mismatch between the resume and the cover letter will be caught in review and reads as carelessness. A reader who catches one inconsistency starts hunting for others.

Include `form_answers.md` in this check. A years-of-experience figure that disagrees between the resume and a screening answer is worse than the same mismatch between two prose documents — the form answer sits next to the question that asked for the number, so the reader is already looking straight at it.

### 3.5d. Structural checks

- **Independent, contract, or side work appears in Work Experience with dates**, not only in a Projects section. An undated Projects entry contributes nothing to an ATS years-of-experience calculation, and for a career transition that number often decides the screen.
- **The summary does not echo the JD.**
- **No apologizing for a missing credential.** If the posting does not require a degree, do not draw attention to its absence. State the years in discipline directly.

## Phase 4: Adversarial Review, Round 1

Run `/slushpile:adversarial-review $1`.

Collect: the pipeline summary, ATS score, swap test results, materials quality out of 10, submission EV per channel with probability ranges, the highest-EV channel, kill criteria results, the contrarian's net call, and the prioritized recommendations.

## Phase 5: Mechanical Fixes

Everything that needs no creative judgment:

- **ATS keyword gaps** — add missing JD keywords the candidate can legitimately claim
- **JD-verbatim echoes** — replace any bullet that is near-verbatim from the posting
- **Formatting** — year-only dates become month and year; combined section headings get split; add location if flagged
- **"So What?" failures** — add the baseline, outcome, or significance the requirements analyst named
- **Hedging that undercuts the letter** — remove "(familiar)" style qualifiers on skills the letter already handles honestly

## Phase 6: Experience-Grounded Depth

The feedback that needs real material from `profile.md`:

- **Surface-level company content.** If the review called the company-specific paragraph "product docs", rewrite it from the candidate's own overlapping experience. "I have built what your tools formalize", never "here is what your product does".
- **Thin resume sections.** Expand what the requirements analyst flagged. Check `profile.md`; if the material genuinely is not there, run `/slushpile:explore-experience $1`.
- **Domain bridging.** Where the role has a domain gap that the candidate's experience maps to, put the domain vocabulary in the resume, not only the cover letter.
- **Unsupported Skills entries.** If a skill is in the Skills section with no bullet demonstrating it, either add the bullet or remove the skill.

## Phase 7: Adversarial Review, Round 2

Run `/slushpile:adversarial-review $1` again on the updated materials.

Compare: ATS delta, swap test changes (the company swap especially — it should improve or hold), verdict trend per channel, which issues persisted and which resolved.

### Decision gate

Use the **highest-EV channel verdict** and the **contrarian's net call**.

- **Contrarian says SUBMIT, highest-EV channel is INTERVIEW or MAYBE-leaning-INTERVIEW, company swap passes** → Phase 8.
- **Contrarian says SUBMIT_AS_PORTFOLIO_ONLY** → Phase 8, with the framing recorded explicitly in `role_analysis.md` and `application.yaml`. The expected value here is portfolio building and ATS record creation, not conversion. Set the expectation before submitting, not after the rejection.
- **Contrarian says DO_NOT_SUBMIT** → run the scope audit below first. If a leg is struck, re-derive from what survives and follow the matching branch. Escalate to the user only when a DO_NOT_SUBMIT survives the audit — then present the surviving reasoning and let them decide.
- **Verdict improved but the company swap still fails** → back to Phase 6, on company-specific content only.
- **Verdict did not improve** → the gaps are structural. Apply the remaining zero-risk fixes and go to Phase 8.

**Three rounds maximum.** After round three the remaining gaps are structural and further editing is motion without progress.

**Sycophancy guard.** If the hiring manager says INTERVIEW for cold submission and the contrarian says cold submission converts below 5%, trust the contrarian. The HM is structurally biased toward decisiveness; the contrarian toward falsification. On expected-value calibration the contrarian is right more often.

### Scope audit — run on every DO_NOT_SUBMIT before escalating

The contrarian is trusted on calibration, not on scope. Two argument classes are out of bounds, and a net call resting on either gets that leg struck and the call re-derived.

1. **Offer-stage contract terms are not application-stage blockers.** Relocation funding, sign-on, equity, start date, and buying out a clawback are negotiated after an offer exists. They are not kill criteria and not subtractions in the compensation gate. Assess compensation on the posted band using the method in `preferences.yaml` and stop. The argument to reject by name: "the band is too low to fund the make-whole, so year one nets negative, so kill." That kills an application before an offer exists, over money that is still negotiable.

2. **An unassessed requisition cannot veto an assessed one.** A better-looking seat elsewhere at the same company is not an input unless it has been fully assessed and the user has said to weigh it. Cross-req sequencing is the user's call.

**In scope, do not strike:** conversion probability and channel structure, pool position, qualification gaps, overclaims, swap-test failures, materials density, level-fit signalling, and adverse application history at the target company — particularly a prior rejection at a higher level, which reads to a recruiter as a multi-level drop.

**Verify before adopting.** When one finding flips the verdict, check it against `job_search.md`, `profile.md`, and sibling role folders before acting. Record in `role_analysis.md` which legs were adopted, which were struck, and why. The struck ones are how this gate improves.

## Phase 8: Finish

### 8a. Final low-effort fixes
Anything from the last review that is low effort and zero risk. Nothing that changes meaning or overclaims.

### 8b. Final build
Compile both documents: `latexmk -xelatex <file>.tex && latexmk -c` for each. Verify page count and text extraction one more time, on both.

The letter's page count is the one that gets skipped. One page is the convention, a second page is read at a much lower rate than the first, and going over is a decision to make deliberately rather than discover after the build. Report the count either way — a check that only reports failures is indistinguishable from one that did not run.

**Proofread the extracted text.** The `.tex` carries macros, and the extracted text is what the reader and every review agent actually see. No review stage checks any of this: the agents grade what a document argues, and a misspelling reaches them as prose they read past. Check, and report the result of each:

- Spelling, across both documents.
- Every proper noun, against `job_description.md` and `role_analysis.md`: the company, its products, team names, and anyone named. A wrong product name kills credibility faster than any other error in the document, and once the file is built nothing downstream is looking.
- Date continuity across the employment history. An end date earlier than the next start date reaches a reviewer as an unexplained gap rather than as the typo it is, and gets argued about as a weakness.
- The contact line against `identity.links`, one more time. A resume reading `linkedin.com/in/USER` survives every review, because the agents read that string as a link the candidate has.

State what passed, not only what failed.

### 8c. Update `role_analysis.md`
Add the adversarial results table, swap test outcomes, key quotes, the final narrative angle (the cover letter thesis), and an honest recommendation naming any structural gaps.

### 8d. Update `application.yaml`

Create it from `templates/application.yaml` if it does not exist.

Fill `adversarial_review`, `cover_letter_scores`, and `submission_expectations`.

Score the letter on seven metrics, 1-5 each: hook (does it stop the reader), thesis (an argument or a capability list), JD targeting, gap handling, company specificity (would it break under a name swap), story quality, voice.

**Set `submission_expectations` explicitly.** This is the field that prevents the most common way a job search burns someone out: over-investing in a low-probability application because the verdict was framed as INTERVIEW. Recording the honest expected outcome and the real reason to submit — direct conversion, portfolio building, record creation, or warm-channel routing — costs thirty seconds and calibrates everything that follows.

### 8e. Update `profile.md`
If the process surfaced experience that was not documented, add it. This is how the profile compounds.

### 8f. Update `job_search.md`
Add the role to the tracker with its status, channel, and expected outcome.

### 8g. Hand off

Show the user:

1. What was built — base resume used, key adaptations, the cover letter thesis
2. The adversarial trend across rounds
3. Remaining structural gaps that materials cannot fix
4. Every file created or modified
5. **Anything on the form that is theirs to answer** — dropdowns, yes/no gates, work authorization and sponsorship questions, compliance attestations. List them from the JD's Notes section, unanswered. The user will hit these in the portal, and finding them there with no warning is when a rushed answer gets given to a question with legal weight.

The user reviews and adjusts before submitting. **This skill never submits anything.** Nothing here touches an application portal, an email, or a form.

## Anti-Patterns

**Resume**
- Do not keyword-stuff experience the candidate does not have. The letter can handle a platform gap honestly; the resume must not overclaim.
- Do not skip the "So What?" test. A metric without context is a claim. With baseline, action, and significance, it is evidence.

**Cover letter — hook and structure**
- Do not open with background.
- Do not reuse a hook across letters.
- Do not try to cover every JD requirement. Depth beats breadth. If it reads like a capability dump, cut until it reads like an argument.
- Do not keep a paragraph that could be deleted without weakening the thesis.
- Do not close with "happy to discuss further".

**Cover letter — gaps and tone**
- Do not include a gap paragraph.
- Do not use "different domain, same problems" as a bridge. Name specifically what transfers.
- Do not announce significance. Show the evidence; let it land.

**Cover letter — specificity**
- Do not use product-page language for company content. "Unity Catalog gives you a governance layer" reads like marketing. "I have built what Unity Catalog formalizes" reads like a practitioner.
- Do not sacrifice voice for keyword coverage. The letter makes an argument. The resume handles the ATS.

**Process**
- Do not run more than three adversarial rounds.
- Do not edit the adversarial-review skill from here. This skill orchestrates that one. They stay separate.
