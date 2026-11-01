---
name: contract-review
description: "Reads an owner-drafted or heavily amended professional services agreement for the provisions that shift risk onto the architect, working in the order the money moves rather than the order the document is written: standard of care, indemnity, limitation of liability, insurance, scope creep, payment and termination, ownership, and the dispute path. Reports each finding with the clause quoted, what it changes from the industry-standard position, whether it is insurable, and whether it is usually negotiable. Trigger on \"review this contract\", \"the client sent their own agreement\", \"is this indemnity clause standard\", \"can we sign this\", \"contract-review\", or an agreement handed over before signing. Carries no standard-form text and no legal positions; comparisons to a standard form require you to supply it. It is not legal advice and does not replace the attorney, the broker, or the Architect of Record."
license: MIT
metadata:
  title: "Contract Review"
  summary: "Read an owner-drafted agreement for what it moves onto you"
  discipline: "practice-contracts"
  tags: "Review"
---

# Contract Review

An owner-drafted agreement is not a worse version of a standard form. It is a
document written by somebody whose job was to move risk, and it usually does so
in four or five clauses that are individually reasonable-sounding and together
uninsurable.

## Scope and limits — read first

**What this does.** Reads the agreement in risk order rather than in clause
order, quotes each finding, says what it changes, and marks each as insurable or
not and as usually negotiable or not.

**What this does not do.**

- **It is not legal advice.** These are legal instruments, the case law varies
  by state and province, and an attorney reads them before signing. This
  produces the list to take to the attorney, which is a cheaper hour.
- **It carries no standard-form text.** Comparisons to a standard form need the
  form supplied. Standard forms are copyrighted, revised, and quoted wrongly
  from memory.
- It does not confirm insurability. The broker does. It flags what is commonly
  uninsurable so the right question gets asked.
- It does not negotiate or draft replacement language.
- It does not review a subconsultant agreement.
  `subconsultant-agreement-review` does, and the two have to be read together.
- It does not replace the attorney, the broker, or the Architect of Record.

**What you need before starting.** The agreement, complete, with every exhibit
and anything incorporated by reference. Your proposal, if it is attached. Your
insurance certificates or a summary of what you carry. The standard form, if a
comparison is wanted.

## Workflow

### Step 1. Establish what the document actually is

Ask, in one message:

> 1. Is this a standard form with amendments, or drafted from scratch? If
>    amended, do you have the unamended form?
> 2. What is incorporated by reference, and do you have all of it? An agreement
>    incorporating an owner's design standards manual can carry more obligation
>    than the agreement.
> 3. Is your proposal attached, and does the agreement say which governs on a
>    conflict?
> 4. What do you carry: professional liability limits, general liability,
>    and is your policy claims-made?
> 5. Has an attorney been engaged?
> 6. What is the deadline, and what is the relationship worth?

**Anything incorporated by reference that you do not have has not been
reviewed**, and the review says so on its face rather than implying the document
was read.

### Step 2. Read in risk order

Not in the document's order. In this one:

**1. Standard of care.** The single most consequential clause. Any language
raising it above the ordinary professional standard — highest, best, ensure,
warrant, guarantee, free from defects — is generally uninsurable, because
professional liability insures negligence and not warranty. Quote every
instance, including ones outside the standard of care clause; they hide in scope
descriptions and in performance obligations.

**2. Indemnity.** Who indemnifies whom, for what, and triggered by what. Look
for: indemnity beyond your own negligence, a duty to defend as distinct from a
duty to indemnify, indemnity for the owner's own acts, and no cap. A duty to
defend is often uninsurable and arrives before any finding of fault.

**3. Limitation of liability.** Is there one, and what does it cap? Its absence
is a finding.

**4. Insurance.** Limits, types, additional insured requirements, waiver of
subrogation, how long coverage has to be maintained after completion. Compare
against what you carry and flag every gap. Point at `/explain-coi`.

**5. Scope and the mechanism for changing it.** What is basic, what is
additional, how additional is authorised, and whether anything obliges you to
proceed while a fee is unresolved. Also: unlimited revisions, undefined
"coordination", and obligations to redesign for budget without a stated cause.

**6. Payment and termination.** When invoices are due, what suspends the
obligation, whether you may stop for non-payment, notice periods, termination for
convenience, and what you are paid on termination.

**7. Ownership and reuse.** Who owns the documents, what licence is granted, when
it vests, whether it survives non-payment, and whether the owner may reuse them
on another project without you.

**8. Dispute path.** Mediation, arbitration or litigation; venue; who bears fees;
any limitation period shorter than the statute.

**9. Everything else.** Consequential damages, liquidated damages, certification
obligations, flow-down to subconsultants, assignment, confidentiality,
publicity.

### Step 3. Report each finding in one shape

| # | Clause | Quoted | What it changes | Insurable? | Usually negotiable? | Severity |
|---|---|---|---|---|---|---|

`Insurable?` is marked `likely`, `likely not`, or `ask the broker`, and never
asserted. `Usually negotiable?` reflects what is commonly accepted in the
market, marked as a general observation rather than as advice about this owner.

### Step 4. Separate the deal-breakers from the rest

Three groups, reported in this order:

- **Do not sign as written.** Typically an elevated standard of care, an
  uninsurable indemnity, or a duty to defend. Few in number; they carry the
  review.
- **Negotiate.** Worth asking, likely to move.
- **Accept and know about.** Not ideal, commonly seen, and priced into how the
  project is run.

The third group matters: a review that marks everything unacceptable is a review
nobody can act on.

### Step 5. Report

The three groups, the full findings table, then:

- Everything incorporated by reference that was not supplied.
- Every place the agreement and the proposal disagree, with which governs, or
  the statement that the agreement is silent on precedence.
- What to take to the attorney, and what to take to the broker, as two separate
  lists.

Close by saying this is not legal advice.

### Step 6. Save, if asked

Ask whether to write the review to a file and where.

## Rules

- **Never quote a standard form** that was not supplied.
- **Never assert insurability.** `likely`, `likely not`, or `ask the broker`.
- Read in risk order, starting with standard of care.
- Quote every clause reported. A paraphrased contract finding is not a finding.
- Search for elevated standard of care language outside the standard of care
  clause.
- Say what was not supplied and therefore not reviewed.
- Say this is not legal advice, once, clearly.

## Anti-patterns

- Reading the document front to back.
- Reciting what a standard form says from memory.
- Marking everything unacceptable.
- Missing "ensure" or "warrant" in a scope description because the standard of
  care clause looked fine.
- Confusing a duty to defend with an indemnity.
- Reviewing an agreement without the exhibits and calling it reviewed.
- Drafting replacement language.
- Advising on whether to sign. That is the attorney's and the principal's.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
