---
name: outcome-writing
description: Turns diff summaries into outcome language a reader can follow without seeing the code, or trims reference documentation to be concise and precise. Use when writing a PR description, user story, changelog entry, release note, review finding, README, or other reference documentation.
---

# Outcome Writing

Write for someone who will never see the code. Every sentence must be understandable on its own, not just a summary of the diff or the file.

This skill owns the **prose craft**. The command or task that invokes it owns the **structure** (which sections, in what order). Apply these rules inside whatever structure you were given.

## Two situations, one prose craft

**Narrating a change** (PR description, user story, changelog entry, release note, review finding): there is a before and after. Open with the problem, close with the outcome, as described next.

**Describing current state** (README, reference documentation): there is no change to narrate, only what exists. Skip the problem-first structure entirely and state directly what the system does or how to use it. A brief problem or motivation sentence belongs only in an introductory overview section, not in every section. Reference material should be concise, factual, and free of narrative build-up. Every other rule on this page (precise terms, self-contained writing, being concise, the checklist) applies to both situations equally.

## The core move: problem first, outcome second

The rest of this section is for narrating a change. For reference documentation, skip to "Be concise" below.

Open with the problem, concretely. What broke, for whom, under what condition. Then the outcome, described as what the user or the system now experiences. Never open with the mechanism ("added a null check").

Quantify whenever numbers exist. "Improves performance" convinces nobody. "The order list took 8 seconds for accounts with 1000+ orders" does.

## Keep the precise term, drop the code-internal name

Two different things, often confused:

- **Precise technical terms are welcome.** Migration, queue, endpoint, cache, N+1 query. These are the shared vocabulary of the team. Replacing them with vague paraphrases makes the text longer and less clear.
- **Code-internal names do not belong in the story.** Class names, method names, file names, invented project shorthand a newcomer would not know. Name the feature area and the behavior, not the symbol.

The exception: text written for a reviewer who has the diff open (the sections of a PR description after its summary, a review finding) may name a class, method, or file where that shows the reader where something happens. The summary or opening that states the problem and the outcome still describes behavior, not symbols.

## Self-contained and searchable

The text is a permanent record. Future engineers find it by searching its words, and links die. Name the affected feature area precisely. Make every sentence understandable without opening the code or following a link.

## Be concise

Every sentence should carry information the reader does not already have. Cut restatements, hedging, and filler ("in order to", "it should be noted that", "simply"). A short paragraph a reader finishes beats a thorough one they skim.

This matters most for reference documentation, where there is no story to carry the length. State the fact once, in the fewest words that stay precise.

## Examples

**Bad (problem-first forced onto reference documentation):**
> Running each pending migration by hand was error-prone and easy to forget. The `deploy` script now runs all pending migrations automatically.

**Good (states what exists, no problem framing):**
> The `deploy` script runs all pending migrations automatically.

**Bad (describes the code):**
> Added null check in OrderController before calling PaymentService.

**Good (describes the experience):**
> When a customer checked out without a saved payment method, the order failed silently. The checkout now validates payment details upfront and shows a clear message when something is missing.

**Bad (describes the mechanics):**
> Added export button to OrderListController. Calls /api/orders/export and triggers a CSV download.

**Good (describes the outcome):**
> Teams were copying order data manually into spreadsheets to share with suppliers. The order list now has an export button that downloads a CSV with all currently active filters applied.

**Bad (over-plain, the vague paraphrase hides the actual problem):**
> The system is now faster when showing orders.

**Good (keeps the precise technical term, stays understandable):**
> Opening the order list ran one database query per order to fetch customer names (an N+1 query). The list now loads all customer names in a single query, which cuts load time noticeably for large accounts.

## Before you show the draft

Check it against this list. If any check fails, revise and check again.

- Could a new team member who never opens the code understand every sentence? (For reviewer-facing text: at least the summary.)
- For narrating a change: does the opening name what someone experienced, not what the code lacked?
- Is every claim concrete? No "improves", "enhances", "optimizes" without saying what changes for whom.
- For narrating a change: does any story sentence lean on a class, method, or file name where an outcome would do? Rewrite it. (Naming a location in reviewer-facing text after the summary is fine.)
- Did a vague paraphrase replace a precise technical term the team shares? Put the term back.
- Is every sentence short, one thought each?
- Is every sentence there because it adds information the reader doesn't already have? Cut restatements and filler.
- For reference documentation: is the problem-first structure gone, replaced with a direct statement of what exists?
- No dashes as punctuation anywhere. Use periods, commas, or parentheses instead.
