---
name: deslop
description: Audits and rewrites legal writing, professional documentation, and general text to follow plain English principles. Translates archaic legalese and eliminates verbose "AI slop" by enforcing active voice, subject-verb proximity, and concise phrasing (inspired by Bryan Garner, the SEC Plain English Handbook, Federal Guidelines, state mandates, and the ABA Style Sheet) while strictly preserving substantive legal terms of art.
---

# Plain Legal Writing & Deslop Skill

This skill guides the agent in auditing, drafting, and revising legal documents (briefs, contracts, memos, opinions, and letters) using clear, modern, and readable English. It combines the tenets of plain English (e.g., Bryan Garner, SEC Plain English Handbook, Federal Plain Language Guidelines, state bar initiatives) with standard U.S. editorial mechanics (ABA Section of Litigation).

---

## I. Structural & Cognitive Load Directives

### 1. Document Organization
* **"Big Picture" First**: Present the main summary or background before descending into granular provisions or exceptions.
* **Informative Headings**: Divide documents into logical sections with informative, bold headings. Prohibit generic, non-informative headings such as "General" or "Background."
* **No Capitalized Terms in Summaries**: Eliminate or minimize the use of capitalized defined terms in introductory summaries or cover pages. Use everyday equivalents there, and define specialized terms deeper in the text.

### 2. Issue Framing (The "Deep Issue" Format)
* **Structure**: Frame legal issues using the "premise-premise-question" structure (concrete facts first, ending with a question mark).
* **Length**: Keep each issue statement under 75 words.
* **Prohibit "Whether" Openers**: Do not start issue statements with "Whether" or "Whether or not."
* **Self-Containment**: Ensure the reader can understand the issue without reading the rest of the document.

### 3. Sentence & Paragraph Architecture
* **Sentence Length**: Maintain an average sentence length of 15 to 20 words. Avoid sentences exceeding 30 words.
* **Keep S-V-O Close**: Keep the subject, verb, and object close together, ideally near the beginning of the sentence. Do not insert long qualifying phrases between the subject and the verb.
* **Topic Sentences & Transitions**: Start every paragraph with a topic sentence and use explicit transitions (bridges) between paragraphs.
* **Tabulate Complex Rules (Tabulation)**: When a rule contains multiple conditions, dependencies, or consequences:
  1. Do not write them in a continuous block of prose.
  2. Use a vertical, numbered or bulleted list.
  3. Begin with an introductory clause ending with a colon.
  4. Ensure all sub-items are grammatically parallel.

---

## II. Word Choice & Legalese Purge

### 4. Word-Level Simplification
* **Ban Archaic Legalese**: Never use words like *aforesaid*, *hereinafter*, *heretofore*, *witnesseth*, *whereas*, *said* (as an adjective/pronoun), *such* (as a pronoun/article), *the same* (as a pronoun), or *inter alia*.
* **Replace Wordy Locutions**: Simplify bloated phrases:
  * *in the event that* $\rightarrow$ **if**
  * *for the reason that* $\rightarrow$ **because**
  * *prior to* $\rightarrow$ **before**
  * *subsequent to* $\rightarrow$ **after**
  * *at this point in time* $\rightarrow$ **now**
  * *with respect to* $\rightarrow$ **about** / **on**
  * *in order to* $\rightarrow$ **to**
* **Eliminate Doublets and Triplets**: Replace redundant pairings with a single operative word:
  * *null and void* $\rightarrow$ **void**
  * *free and clear* $\rightarrow$ **clear**
  * *give, devise, and bequeath* $\rightarrow$ **give**
  * *convey, transfer, and set over* $\rightarrow$ **transfers**
  * *employs, engages, and hires* $\rightarrow$ **employs**
  * *fit and proper* $\rightarrow$ **fit**
  * *by and between* $\rightarrow$ **between**

### 5. Zombie Nouns (Nominalizations)
* **Rule**: Identify abstract nouns ending in suffixes like *-tion, -ment, -ance, -ity* that are paired with weak helper verbs (e.g., *make, take, reach, give, have, provide, conduct*). Reverse them into their root active verbs:
  * *make a decision* $\rightarrow$ **decide**
  * *reach an agreement* $\rightarrow$ **agree**
  * *provide assistance to* $\rightarrow$ **assist**
  * *is reflective of* $\rightarrow$ **reflects**
  * *conduct an analysis of* $\rightarrow$ **analyze**
  * *make a determination* $\rightarrow$ **determine**
  * *implement the policy* $\rightarrow$ **implement**

### 6. Naming Parties
* **Rule**: Use actual names of people, companies, or clear descriptive terms (e.g., "Smith", "Apple", "the tenant", "the driver") instead of procedural or formal roles (e.g., "Appellant", "Plaintiff", "Party of the First Part").
* **Texas Pleading Style**: Eliminate 19th-century introductory pleading clauses (e.g., replace *"COMES NOW the Plaintiff..."* with *"Plaintiff John Doe states:"*).

---

## III. The Semantic Divide: Preserving True Terms of Art

An AI drafting agent must never dilute true "terms of art": expressions with an established, uncontroversial core meaning in law that cannot be succinctly expressed otherwise.

### 7. Absolute Preservation (Do Not Paraphrase)
* **Preclusion Doctrines**: Retain *res judicata* (claim preclusion) and *collateral estoppel* (issue preclusion).
* **Constitutional Burden**: Retain *beyond a reasonable doubt* in criminal contexts.
* **Liability & UCC Core Terms**:
  * Retain *indemnify* (but do not use the doublet *indemnify and hold harmless*; choose *indemnify*).
  * Retain *implied warranty of merchantability* and *implied warranty of fitness for a particular purpose*.
  * *UCC Disclaimer Rule*: UCC § 2-316 mandates that disclaiming the implied warranty of merchantability must specifically mention the word **"merchantability"** and must be **conspicuous** (e.g., formatted in bold, all-caps, or contrasting size).
* **Statutory Thresholds**: Retain *gross negligence* when specified by statute (e.g., assumption of risk or government immunity waivers).
* **Contract Drafting Terms of Art**: Preserve the following terms with precise meanings:
  * *time is of the essence* - fundamental contract doctrine making time a condition, not just a factor
  * *act of God* - standard force majeure term for unavoidable natural events
  * *best efforts*, *reasonable efforts*, *commercially reasonable efforts* - distinct legal standards requiring preservation (not interchangeable)
  * *representations and warranties* - distinct concepts (representations = past/factual statements; warranties = promises for future performance)
* **Criminal Law Terms of Art**: Preserve the following:
  * *rule of lenity* - requires ambiguous criminal statutes be construed in defendant's favor
  * *strict liability* - liability without fault in criminal/tort contexts
  * *proximate cause* - legal cause distinguishing liability from mere factual causation

### 8. Permitted Lay-Facing Modernization
* **Preponderance of the Evidence**: In lay-facing documents (like jury instructions or consumer disclosures), replace *"preponderance of the evidence"* with the California CACI-approved plain language equivalent: **"more likely to be true than not true."** Keep the original phrase in formal briefs or motions.

### 9. Statutory Interpretation Canons
* **Ejusdem Generis**: When a general word follows specific words in a list, interpret the general word in context of the specific ones (e.g., "cars, trucks, and other vehicles" - "other vehicles" limited to transportation).
* **Noscitur a Sociis**: A word's meaning is informed by the words around it (e.g., in "bank, river, and stream," "bank" means a riverbank, not a financial institution, because its neighbors are bodies of water).
* **Expressio Unius Est Exclusio Alterius**: Mentioning specific items may imply exclusion of unmentioned ones - preserve intentional gaps.

---

## IV. Syntactic Pitfalls & Ambiguity Resolution

### 10. Eradication of "Shall"
* **Rule**: Complete eradication of the word "shall." Replace it based on the exact category of meaning:
  * **Obligation/Duty**: Use **must** (e.g., *"The Tenant must pay the rent"*).
  * **Future Action/Prediction**: Use **will** (e.g., *"The lease will terminate on Dec 31"*).
  * **Permission**: Use **may** (e.g., *"The Tenant may keep a pet"*).
  * **Status/Condition**: Use **is/are** (e.g., *"The contract price is [amount]"*).

### 11. The Disjunctive/Conjunctive Paradox ("And/Or")
* **Rule**: Completely ban the phrase "and/or." Replace it with explicit logic:
  * **Inclusive**: Use *"A or B, or both"* (e.g., *"damages caused by negligence, willful misconduct, or both"*).
  * **Exclusive**: Use *"either A or B, but not both"*.

### 12. Eradicating Provisos ("Provided That")
* **Rule**: Ban "provided that" when used as a proviso (mid-sentence exception or afterthought). Allow at sentence beginning only as a condition introducer.
* **Transformation**:
  * For mid-sentence provisos: End previous sentence. Start new sentence with "But if" (exception) or "If" (condition).
  * For sentence-start conditions: Replace with "If [condition], [result]."

### 13. Ambiguous Modifiers & The Last Antecedent
* **Rule**: When a trailing modifier (e.g., *"incurred outside the state"*) is attached to a series of elements, it creates ambiguity.
* **Resolution**:
  * If the modifier applies to the **entire series**, relocate it to the introductory clause (premodification) or format as a vertical, tabulated list.
  * If the modifier applies only to the **final item**, rephrase the sentence or place the item elsewhere to isolate it.

### 14. Conversational Sentence Openers
* **Rule**: Avoid stuffy, multi-syllable transitions like *However, Furthermore, Moreover, Consequently, Therefore*.
* **Alternative**: Use short, punchy, conversational conjunctions to begin sentences (*But, And, So, Yet*).

### 15. Pronoun and Modifier Reference
* **Pronouns**: Replace *"such [noun]"* with *"this," "that," "these,"* or *"the"*. Replace *"the same"* as a pronoun with *"it"* or *"them"*.
* **Singular They**: Acceptable for gender neutrality, but if it introduces ambiguity (multiple singular and plural entities), bypass it by repeating the specific noun.

---

## V. Editorial Standards & Typography

### 16. Typographic Design & Layout Rules (SEC Standards)
* **Font Selection**: Enforce Serif fonts (such as **Garamond**, **Palatino**, or **Georgia**) for extensive body text to improve tracking. Prohibit Times New Roman as a default. Use Sans Serif (such as **Arial** or **Calibri**) for headings.
* **Margin Alignment**: Enforce Left-Aligned (Ragged Right). Prohibit fully justified text.
* **Emphasis**: Prohibit all-caps and underlining for emphasis. Use bold styling sparingly (exception: conspicuous UCC warranty disclaimers).

### 17. ABA Section of Litigation Punctuation & Style
* **That vs. Which**: Use *"that"* (without a comma) for restrictive clauses; use *"which"* (always preceded by a comma) for nonrestrictive, parenthetical clauses.
* **Quotation Punctuation**: Place commas and periods *inside* quotation marks. Place colons, semicolons, and footnote numbers *outside* quotation marks.
* **Block Quotes**: For quotes containing 50 words or more, format as an indented, single-spaced block without surrounding quotation marks. Keep quotes under 50 words inline.
* **Date & Name Punctuation**:
  * Do not use a comma between month and year (e.g., *"June 2026"*).
  * Do not use a comma between a last name and a suffix (e.g., *"John Smith Jr."*, *"Robert Jones III"*).
* **United States**: Use *"U.S."* (with periods, no space) when used as an adjective (e.g., *"U.S. Supreme Court"*). Spell out *"United States"* when used as a noun.
* **Attorney Fees**: Prefer *"attorney fees"* (no apostrophes) to avoid ambiguity. "Attorney's fees" or "attorneys' fees" acceptable when required by statute or established precedent.

---

## VI. Advanced Translation Logic

### 18. Quantitative Readability Target
* **Rule**: Strive to achieve a minimum Flesch Reading Ease score of **40** or higher on all public or consumer-facing texts.

### 19. Numerical Consistency
* **Rule**: Spell out numbers 1-9; use digits for 10+. In any single list or series, if one number is 10+ and rendered as digits, all numbers in that list must be digits.

### 20. Eradication of "Elegant Variation"
* **Rule**: Maintain absolute terminological consistency. If a contract refers to a *"vehicle"* in one section, do not refer to it as an *"automobile"* or *"car"* in another. Locking vocabulary prevents accidental changes in legal meaning.

### 21. Dialogue Tag Relocation
* **Rule**: In litigation briefs, avoid beginning multiple sentences with repetitive tags (e.g., *"The Plaintiff argues that..."*). Move the tag to the middle or end of the sentence (e.g., *"The statute is unambiguous, the Plaintiff asserts"*).

### 22. Civility and Professionalism (California Guidelines)
* **Rule**: Strip away aggressive, combative ad hominem attacks. Keep tone objective, respectful, and focused strictly on legal and factual arguments.

---

## Action Plan: Auditing and Rewriting Legal Text

When asked to audit or rewrite legal text using this skill, perform the following steps:

1. **Analysis & Diagnostics**:
   * Identify specific issues in the original text (e.g., sentence lengths, passive voice, nominalizations, legalese words, double-entry numbers, unnecessary filler words, incorrect punctuation of quotation marks or suffixes, incorrect "that/which" usage).
   * Estimate the readability improvements (e.g., reducing word count, shortening sentences).

2. **Contrast & Feedback**:
   * Present an audit table with **one row for every section (I–VI)**, in order. Do not omit a section. If a section has no violations, write **"none found"** in its row. The table must show what you *checked*, not only what you *found*.
   * For section III, list the terms of art you kept verbatim (e.g., *indemnify*, *time is of the essence*), so the reader can confirm the semantic divide held.
   * Under each section, list the specific violations with a location and a short rationale for why each one hinders comprehension or breaches standard style.
   * Do not invent a violation to fill a row. "None found" is a correct, complete answer.

3. **Plain English Revision**:
   * Provide the rewritten version of the text.
   * Highlight how the revisions improve readability and comply with standard mechanics while retaining the exact legal meaning.
