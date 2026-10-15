---
name: build-product-ontology
description: Build or extend the product ontology — the agreed, human-readable map of the kinds of things a product is made of, what each holds, how they connect, and what must always be true — one kind at a time, with the person. Follows the classic seven-step method (scope by questions, reuse, terms, kinds, properties, rules, instances) and writes the ontology in the canonical format, checked by a script. Use when a play or a person needs a new kind of thing in the product model (for example the Business Intent), or needs an existing kind changed, before anything writes instances of it.
user-invocable: true
model: opus
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# build-product-ontology

**Meta-utility skill.** It builds Garura's own product ontology — the framework's map of
what a product is made of — so it is invoked by a person in a Garura harness repo
(`/build-product-ontology`), not by agents or plays, and it is never installed into a
product project (see `docs/components/skills.md`, Meta-Utility Skills).

The product ontology is the agreed map of a product's world: the **kinds** of things in it,
their **properties**, how they **relate**, the **rules** that must always hold, and real
**examples**. A database stores things; the ontology says what they mean, so people and
agents use the same words for the same things.

It grows **one kind at a time**. Each run adds or changes the kinds a piece of work needs,
and leaves the rest alone. A kind that a person reads — a Business Intent — is written so a
business reader understands it with no other document open.

You build the ontology **with the person**. You propose; they decide. Nothing you propose is
written as agreed until they say so.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `need` | yes | What the work needs, in plain words — e.g. "the Business Intent, human-facing, as `/intent` will write it" |
| `ontology_path` | yes | The ontology document. Default: `~/.garura/core/memory/standards/schemas/product-os/ontology.md` (source: `core/components/memory/standards/schemas/product-os/ontology.md`) |
| `template_path` | no | The format. Default: `~/.garura/core/memory/standards/templates/product-ontology.md` |
| `sources` | no | Paths to read for reuse — existing schemas, doctrine, decision records, issues |
| `report_path` | yes | Where the check report is written |

## Process

Read the format at `template_path` first, and the ontology at `ontology_path` if it exists.
Then run the seven steps for the kinds `need` touches. Each step that needs a decision ends
with a plain question to the person; record their answer before moving on.

### 1. Scope it with questions

Write the questions the ontology must be able to answer for this `need` — plain, testable
questions a person would actually ask ("Given a business intent, which pieces of work
served it?"). Start from questions the sources already state (an issue's "how this will be
judged", an ADR's open questions). **Ask the person to confirm or change them — one
question at a time, each with a plain example.** Every later step is tested against these
questions.

A question belongs here only if a person would ask it to *find something out* about their
own things ("which work served this intent?"). Two look-alikes do not: a **quality bar**
("can a business reader read it?") becomes a rule at step 6, and a **design choice about the
kind** ("what stages can it be in?") is worked out by you at step 6 from the sources and
shown to the person to confirm. Write each question the way its example reads — plain and
concrete.

### 2. Reuse what exists

Read the `sources` and the existing product model schemas. List every existing kind,
property or relationship the need can reuse, and every place the need would clash with
something that exists (the same word meaning two things, for example). Reuse before you
invent; never redefine an existing kind silently.

### 3. List the terms

List every word people use in this part of the world — nouns (candidate kinds and
properties) and verbs (candidate relationships). Keep the person's words.

### 4. Decide the kinds

Group the terms into kinds. For each, one or two plain sentences: what it is, and who reads
it (person, agent, or both). Name what it is NOT when a similar word exists. **Ask the
person to confirm the kinds.**

### 5. Give each kind its properties

For each kind, the properties it holds — each with a plain description and whether it is
required. A person-facing kind holds what a person needs to understand it, in their words,
not an agent's working fields.

### 6. Connect and constrain

For each kind: its relationships (direction, the other kind, how many, and what the link
means) and its rules (what must always be true). Add states if it moves through a life.
Every kind a relationship names must be defined, or listed under **Not yet defined** with
one line. **Ask the person to confirm the relationships and rules.**

### 7. Make a real example and test it

Write one real, filled-in example of each kind, the way its reader will see it. Then go back
to step 1: mark each question **answered**, **partly** or **not yet**, with what answers it.
A question that leans on a kind not yet defined is never marked answered.

### Write and check

Write the agreed result into `ontology_path` in the canonical format: bump `version`, set
`updated`, add one dated log line saying what changed and why. Then run the check — it is
deterministic: no git, no network, no judgment:

```bash
python3 <skill-dir>/scripts/check_ontology.py --ontology <ontology_path> --out <report_path>
```

Exit `0` — valid. Exit `2` — not valid: the report lists every problem; fix them and re-run.
Exit `3` — the file cannot be read. Its tests: `python3 <skill-dir>/scripts/test_check_ontology.py`.

## Output

The ontology at `ontology_path`, and the check report at `report_path`. Return their paths —
never the content:

```yaml
ontology_path: <path>
report_path: <path>
```

## Constraints

- **The person decides.** Steps 1, 4 and 6 end with their confirmation; nothing is written as agreed without it.
- **One need at a time.** Add or change only the kinds the need touches.
- **Reuse before invent**, and never redefine an existing kind without saying so in the log.
- **Readable by its reader.** A person-facing kind is written in plain words, with a plain example.
- **The script decides valid.** Not you.
