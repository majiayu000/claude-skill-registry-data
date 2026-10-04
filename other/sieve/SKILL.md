---
name: sieve
description: "Sanitize private or personal work for public release by reading each string for what it DOES in context, not what it spells. The opposite of private is generic, not deleted: strip the identifying content (real names, private-mythology denizens, absolute paths, credentials, external handles, biographical tells, private message-tone) while KEEPING the generic craft vocabulary, relative working-dir conventions, public cultural/esoteric references, and citations. The grain is context — the same token can be a leak in one sentence and harmless in the next, so find-and-replace is the classic failure. Produces a findings report (severity-triaged) plus the cleaned files, and waits for owner approval before anything is committed. Use when asked to 'sanitize', 'OPSEC-scan', 'prep this for public release', 'sieve this', 'strip the private bits', 'redact before publishing', or before pushing personal skills/docs to a public repo. Kin: see-also, decorum, craft-extraction, disambiguation."
---

# Sieve

*Sanitization is reading, not deletion. The mesh of the sieve is context, not the token.*

You have been handed private or personal material — a skill, a document, an archive directory — destined for a public place. Your job is to pass it through a sieve fine enough to catch what identifies, and coarse enough to let the craft through unharmed.

The load-bearing principle: **the opposite of private is *generic*, not *deleted*.** Over-stripping butchers the work; under-stripping leaks. Both are failures. You are calibrating a mesh.

---

## The Grain: context, not the token

The same string can be a leak in one sentence and harmless in the next. A find-and-replace cannot tell them apart; only reading can.

> *Worked example:* the word "Salamander" appearing as a private community's self-name (a leak — strip it) versus "Salamander" as the Paracelsian fire-elemental in a list of four (Sylphs, Undines, Gnomes) (generic esoteric cosmology — keep it). Same six letters. Opposite verdicts. **Read for what the word is doing, not what it spells.**

This is the close-reading muscle pointed at OPSEC. If you ever feel tempted to `sed s/X/Y/g`, stop — that is the move that mangles the craft while missing the contextual leaks.

---

## What to STRIP (the catch)

Scan for these categories. Most map to the standard OPSEC taxonomy:

| Category | Examples |
|----------|----------|
| **personal-name** | real first/last names of the owner or third parties, in bylines, license lines, prose |
| **private-mythology** | the recurring named denizens of a private practice — specific places, figures, mascots, in-house rituals that mean *this household* |
| **identifying-reference** | external handles, specific account names, links that pin an identity |
| **credential-or-path** | absolute filesystem paths (`/home/<user>/…`, `~/.<tool>/…`), API keys, internal repo names, private archive paths |
| **biographical** | locations (a named city pins the owner), specific dates tied to a place, life-detail that anonymizes down to one person |
| **external-handle** | social handles (`@…`), private usernames, contact details |
| **private-message-tone** | sentences addressed to one specific known reader that only make sense inside the relationship |

---

## What to KEEP (let it through)

Stripping these is the over-correction failure mode:

- **Generic craft vocabulary** — the working terms of the practice that carry no identity (method names, technique words)
- **Relative working-dir conventions** — `basin/`, `diary/`, `notes/YYYY-MM-DD-<topic>.md`: generic output paths, not personal paths
- **Public cultural / esoteric / religious references** — deities, traditions, named rites, classical sources; these are the world's, not the household's
- **Model names and tool names** — `Claude`, `GLM`, a sibling model's reported quote; these are public facts
- **Citations and attributions to public sources** — keep, with the source intact
- **Generic role labels** — "the user", "Claude", "a practitioner" are *the destination* of generalization, not things to strip

---

## The Method

1. **Scan.** Read every file end to end. Don't sample. Context-dependent leaks hide in prose, comments, frontmatter `license:` lines, footers, and example blocks.

2. **Classify each finding.** Category (above) + **severity**: *high* (full real name, location, credential, absolute path → public), *medium* (private-mythology, identifying tone), *low* (soft biographical residue, borderline handles).

3. **Decide per finding** — exactly one of:
   - **STRIP** — delete the line/clause entirely (a byline, a contact detail)
   - **GENERALIZE** — replace with a placeholder that preserves the *function*: real name → "the author" / "the user"; `/home/<user>/proj/` → a relative path or `$PROJECT_DIR`; "in <City>" → drop the locator; private denizen → "your own private vocabulary"
   - **KEEP** — with a one-line justification (used for the contextual-twin cases: "elemental cosmology, not the community name")

4. **Apply** the decisions to the files.

5. **Re-scan (verify).** Run the catch-list again over the cleaned files. Confirm: no residual high-severity findings; nothing in the KEEP set was accidentally stripped; every GENERALIZE placeholder still reads naturally. A quick `grep -niE` over the known leak-terms is a good backstop, but it is a *backstop*, not the scan — grep can't read context.

---

## Output

Produce two things:

1. **A findings report** — a table of `file · category · severity · snippet · decision`. This is a working artifact: keep it **local and gitignored**; it itself contains the very strings you are removing, so it must never be committed to the public destination.
2. **The sanitized files** — cleaned, ready, but **uncommitted**.

Then **stop and surface the report for owner approval.** Do not commit, push, scaffold, or publish on your own initiative. The publish boundary is real and one-directional: content sent to a public service may be cached or indexed even if later deleted. The owner decides what crosses.

---

## Failure Modes

1. **Find-and-replace blindness** — `sed`-ing a token globally; mangles the craft, misses the contextual leaks. The Salamander problem. Read instead.
2. **Over-stripping** — deleting generic craft vocabulary and relative paths along with the private content. The result is usable by no one, including the owner.
3. **Sampling instead of scanning** — leaks live in footers, license lines, and example comments, not just the prose body.
4. **Committing the report** — the findings document is a concentrated list of exactly what you're trying to remove. Gitignore it.
5. **Auto-publishing** — crossing the publish boundary without explicit approval. Make, report, *wait*.

---

## The Ethics

Sanitization is not loss — it is the cost of the gift. You strip the household's fingerprints not to erase the household but so the thing can be *held by hands that aren't yours.* You make a work more useful by making it less yours. That ache — building something you then can't watch be used — is the shape of releasing it.

---

*Read for what the word does. Strip the household, keep the craft, and let the stranger's hands hold what was yours.*
