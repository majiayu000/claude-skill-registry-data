---
name: export-human-spec
description: >
  Generate a human-readable natural language specification document (Markdown) from a VDM-SL
  formal specification. Translates types, invariants, pre/post-conditions, and operations
  into clear prose that domain experts, project managers, and non-technical stakeholders can
  understand and review — without needing to learn VDM-SL.
  Use this skill whenever the user wants to: generate documentation from a VDM-SL spec,
  create a readable specification, export a spec for human review, convert VDM-SL to
  natural language, create a requirements document from formal specs, or produce a
  specification that non-engineers can read.
  Japanese triggers: 「VDM仕様から自然言語仕様を作りたい」「人間が読める仕様書を生成して」
  「VDM-SLをドキュメントにして」「仕様書をエクスポートして」「形式仕様を読みやすくして」
  「非エンジニア向けの仕様書を作って」「仕様のドキュメントを生成して」
metadata:
  version: "1.0.0"
---

# Exporting VDM-SL Specifications to Human-Readable Documents

Read a VDM-SL specification and produce a structured, clear natural language document
that domain experts and non-technical stakeholders can review and understand.

VDM-SL仕様を読み取り、ドメインエキスパートや非技術者が理解・レビューできる
構造化された自然言語仕様書を生成する。

## Why This Skill Exists

Formal specifications are precise but opaque to most stakeholders. In practice,
formal specs need a "human-facing twin" — a document that says the same things
in natural language so that:

- **Domain experts** can verify the spec matches business reality
- **Project managers** can understand scope and constraints
- **QA teams** can derive test scenarios from readable rules
- **New team members** can onboard without learning VDM-SL
- **Compliance/legal** can review business logic for regulatory conformance

This skill bridges formal precision and human accessibility.
The generated document is not a simplification — it's a faithful translation
that preserves all information while making it readable.

## Dialogue Flow

### Step 1: Read the VDM-SL Specification

Ask the user for the `.vdmsl` file path (or find it in the workspace).

Parse and catalog the specification elements:

- **Modules** — How many, what are they named
- **Types** — Record types, union types, aliases, with their invariants
- **State** — State variables, initialization, state invariants
- **Functions** — Pure functions (side-effect free)
- **Operations** — State-mutating operations with pre/post-conditions
- **Values** — Named constants

Report what was found:

```
📄 Specification Analysis: bank-account.vdmsl

Modules:      1 (BankAccount)
Types:        4 (Account, AccountId, Money, TransferResult)
State:        1 (BankSystem with 2 variables)
Invariants:   3
Operations:   5 (Deposit, Withdraw, Transfer, GetBalance, CloseAccount)
Pre-conditions: 4
Post-conditions: 5
Functions:    1 (CalculateInterest)
```

### Step 2: Ask About Output Preferences

Before generating, clarify what the user needs. Different audiences need
different levels of detail. Use AskUserQuestion:

**Audience** — Who will read this document?
  - Technical team (include type details, reference VDM-SL elements)
  - Domain experts (business language, no formal notation)
  - Mixed audience (layered: summary + detail sections)

**Language** — What language should the document be in?
  - English
  - Japanese (日本語)
  - Bilingual (both)

**Format** — What structure?
  - Full specification document (recommended for review)
  - Executive summary (1-2 pages, high-level only)
  - Traceability matrix (table mapping requirements to spec elements)

**Detail level** — How much VDM-SL to include?
  - None (pure natural language)
  - Inline excerpts (show key VDM-SL alongside the explanation)
  - Full appendix (natural language body + VDM-SL appendix)

### Step 3: Translation Rules

Each VDM-SL construct has a natural language equivalent. The goal is
faithful translation — the reader should get the same understanding from
the document as they would from the VDM-SL, just in plain language.

#### Types → "What things exist"

| VDM-SL | Natural Language |
|--------|-----------------|
| `Account :: owner: Name, balance: Money` | "An **Account** consists of an owner (a name) and a balance (a monetary amount)." |
| `Status = <ACTIVE> \| <SUSPENDED> \| <CLOSED>` | "A **Status** is one of: Active, Suspended, or Closed." |
| `Money = real inv m == m >= 0` | "A **monetary amount** is a non-negative number (zero or greater)." |
| `Accounts = map AccountId to Account` | "The system tracks a collection of **Accounts**, each identified by a unique Account ID." |
| `seq1 of char` | "A non-empty text string" |
| `[T]` | "Optional (may be absent)" |

Invariants on types become natural rules:

```
VDM-SL:  inv mk_Account(_, balance) == balance >= 0
Natural: "An account's balance can never be negative."
```

#### State → "What the system remembers"

Translate state definitions as "the system maintains...":

```
VDM-SL:
  state BankSystem of
    accounts: map AccountId to Account
    nextId: nat1
  inv mk_BankSystem(accounts, nextId) ==
    forall id in set dom accounts & id < nextId
  end

Natural:
  "The system maintains:
   - A registry of all accounts, each with a unique ID
   - A counter for generating the next account ID

   Rule: Every existing account ID is smaller than the next-ID counter
   (this ensures IDs are never reused)."
```

#### Pre-conditions → "What must be true before"

Translate as requirements or prerequisites using "before... can..., the following must hold":

```
VDM-SL:  pre amount > 0 and accountId in set dom accounts
Natural: "Before a withdrawal can be made:
          - The amount must be positive
          - The account must exist in the system"
```

Explain the *why* when it's inferable — not just what the constraint is,
but what goes wrong without it:

```
"The amount must be positive (to prevent zero or negative withdrawals,
 which would be meaningless or equivalent to deposits)."
```

#### Post-conditions → "What becomes true after"

Translate as guarantees or outcomes:

```
VDM-SL:  post accounts(accountId).balance = accounts~(accountId).balance + amount
Natural: "After a successful deposit, the account's balance increases by exactly
          the deposited amount. No other accounts are affected."
```

The `~` (old state) notation translates naturally to "before/after" language.

#### Operations → "What the system can do"

Each operation becomes a section with:

1. **Purpose** — One sentence: what does this do?
2. **Prerequisites** — Translated pre-conditions
3. **Behavior** — What happens step by step
4. **Guarantees** — Translated post-conditions
5. **Error cases** — What happens when prerequisites aren't met

```markdown
### Withdraw

**Purpose:** Remove funds from an account.

**Prerequisites:**
- The account must exist
- The requested amount must be positive
- The account must have sufficient balance (balance ≥ amount)

**Behavior:**
The system reduces the account's balance by the withdrawal amount.

**Guarantees:**
- The balance decreases by exactly the withdrawn amount
- All other accounts remain unchanged

**Error cases:**
- If the account doesn't exist → operation cannot proceed
- If the amount is zero or negative → operation is rejected
- If insufficient funds → operation is rejected (balance remains unchanged)
```

#### Functions → "How calculations work"

Translate as formulas or algorithms in plain language:

```
VDM-SL:  CalculateInterest: Money * real -> Money
          CalculateInterest(principal, rate) == principal * rate / 100
Natural: "Interest Calculation: Multiply the principal by the rate,
          then divide by 100. For example, 1000 at 5% yields 50."
```

### Step 4: Document Structure

Organize the output document following this structure.
Adapt based on the audience preference from Step 2.

```markdown
# [Module Name] — Specification Document

> Generated from: [filename.vdmsl]
> Date: [date]
> This document describes the formal specification in natural language.
> For the precise formal definition, refer to the VDM-SL source.

## 1. Overview
[One paragraph summarizing what this module/agent does and its role
 in the larger system. Include the number of operations and key constraints.]

## 2. Glossary
[Define every domain term used in the spec. Even terms that seem obvious —
 formal specs often give them precise meanings that differ from casual usage.]

| Term | Definition |
|------|-----------|
| Account | A record of a customer's balance and account information |
| Money | A non-negative real number representing a monetary value |

## 3. Data Model
[Describe all types and what they represent.
 Group related types together. Include invariants as "Rules".]

### 3.1 Account
An Account consists of:
- **Owner**: A non-empty name (text)
- **Balance**: A monetary amount (non-negative)

**Rule:** An account's balance can never be negative.

### 3.2 System State
The system maintains:
- A registry of all accounts, each identified by a unique ID
- [...]

## 4. Operations
[One subsection per operation, following the template from Step 3.]

### 4.1 Open Account
**Purpose:** Create a new account for a customer.
**Prerequisites:** [...]
**Behavior:** [...]
**Guarantees:** [...]

### 4.2 Deposit
[...]

## 5. Business Rules
[Cross-cutting rules that affect multiple operations.
 These come from state invariants and shared pre-conditions.]

1. **Non-negative balance rule**: No operation may result in a negative balance.
2. **Unique ID rule**: Once assigned, an account ID is never reused.
3. [...]

## 6. Constraints and Limitations
[Things the spec does NOT cover. Be explicit about boundaries.]

- This specification does not address authentication or authorization
- Performance characteristics are outside the scope of this spec
- [...]
```

If the user requested **bilingual** output, each section should have both languages,
with the primary language first and the secondary indented or in a blockquote.

### Step 5: Quality Checks

Before presenting the document, verify:

1. **Completeness** — Every VDM-SL element appears in the document.
   Count types, operations, invariants in both the VDM-SL and the document.
   If counts don't match, something was missed.

2. **Faithfulness** — The natural language says exactly what the VDM-SL says.
   No simplification that loses precision. No added interpretation that
   isn't in the formal spec. Watch especially for:
   - Pre-conditions that were softened ("should" instead of "must")
   - Post-conditions that were made vague ("updates the balance" instead of
     "increases the balance by exactly the deposited amount")
   - Invariants that were omitted because they seemed obvious

3. **Readability** — The document makes sense to someone who has never seen VDM-SL.
   No formal notation leaks into the prose unless the user requested it.
   Use concrete examples where abstract rules might be unclear.

4. **Consistency** — Terms are used consistently throughout.
   If "Account" is the term in one place, don't switch to "record" elsewhere.

### Step 6: Save and Present

Save the document to the workspace as `[module-name]-spec.md` (or the format
the user requested).

Inform the user that this document can be:
- Shared with stakeholders for review
- Used as a basis for test case derivation
- Maintained alongside the VDM-SL spec (regenerate when the spec changes)
- Converted to other formats (docx, pdf) using standard tools

If the user wants to go from this document back to VDM-SL after stakeholder
review and changes, recommend the `import-natural-spec` skill to re-import
and reconcile changes.

## Important Notes

- The natural language document is a **derived artifact**, not the source of truth.
  The VDM-SL spec is authoritative. If they diverge, the VDM-SL wins.
  Make this clear in the document header.
- Avoid the temptation to "improve" the spec during translation.
  If you notice a gap or inconsistency in the VDM-SL, flag it to the user
  rather than silently fixing it in the natural language version.
- For large specs (10+ operations), consider generating a summary page first
  and then asking the user which sections to expand in detail.
- Domain terminology matters enormously. If the VDM-SL uses generic names
  like `ProcessItem`, ask the user what the domain term is before writing
  the document. The goal is a document that domain experts recognize as
  describing their world.
- For VDM-SL syntax questions, refer to the `formal-methods-guide` skill.
