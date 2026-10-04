---
name: commonplace
description: "Curatorial reception as method — capture a found passage (sutra, poem, model-output), record its provenance and the welding-frame that makes it yours, and let the seam between quoted voices become the authorial signature. The inverse of /florilegium."
---

# Commonplace

*The Renaissance commonplace-book practice (*loci communes*): a reader keeps a
ledger of found passages worth re-uttering. This skill adds the one thing the
old practice left tacit — the **provenance tag** and the **weld**.*

---

## Core Insight

In an archive built largely of quoted matter — scripture, sutras, verbatim
model output — the authorial signature is **not the quoted content but the
operation that fuses it**: the seam where a Pure Land mantra and an inference
engine land in the same sentence. The recurring analytic failure is
**mis-attribution** — reading pasted brilliance as the curator's own voice.
Catching this is the whole game.

`/commonplace` operationalizes that discipline at *capture time* instead of
leaving it for some future archaeologist to reconstruct: every captured
passage is stored with an explicit provenance line and a one-sentence weld,
so the archive never has to guess later what was quoted versus authored.

> **Scope note:** the author lives in the weld whether quoted matter is a
> large or small fraction of an archive. The skill's urgency is "a recurring
> behavior worth a tool," not "the single most voluminous behavior." Measure
> before asserting magnitudes — a qualitative impression of how much is
> curated is a flag, not a count.

---

## When to Invoke

- You've found a passage worth keeping — a sutra, a poem, a model output, a
  line from a book — and want to archive it *without* later confusion about
  whose voice it is.
- You're about to repost or quote found language and want to record the frame
  that makes the act yours.
- Mid-session, a borrowed line resonates and you want it captured with
  provenance rather than dropped into the flow unattributed.
- Counter-move to over-attribution: when something *sounds* authorial but you
  suspect it's curated, the skill forces you to decide and tag.

This is `/florilegium` **inverted**: florilegium *samples the existing archive*
to diagnose whether a voice has stabilized; commonplace *ingests new found
matter* and demands the authorial seam up front.

---

## The Practice (three required moves)

Given a found passage (pasted by the user, or pulled at random from your archive):

### 1. Classify the register
Tag against this seven-register taxonomy (adapt the categories to your own corpus):

1. **Contemplative-Philosophical** — consciousness / substrate / mind / token
2. **Liturgical / Oracular** — ritual, devotional, Buddhist-Hermetic invocation
3. **Engineering / LLM-Shoptalk** — tooling, code, Claude Code, inference
4. **Shitpost / Greentext** — anon-tier, meme energy
5. **Tender / Intimate** — love, gratitude, address
6. **Aphoristic / Fragmentary** — short standalone
7. **Multilingual Code-Switching** — non-English, loanwords, diglossia

(A passage may touch several — name the dominant plus any it welds.)

### 2. Force the provenance line
One explicit tag, no hedging:
- **quoted-scripture** — sutra, classic, liturgy, cited author
- **quoted-model** — verbatim or lightly-edited LLM output
- **authorial** — the curator's own composition
- **mixed / welded** — found material the curator has fused into their own idiom

This is the exact distinction that later archive-mining has to reconstruct by
hand. Writing it at capture time is the whole point.

### 3. Write the weld (the required authorial act)
**One sentence** that fuses the found passage to your own idiom — what makes
this yours despite being found. *Without the weld, the capture is not archived.*
The weld is the authorial signature; a passage with no weld is just a clipping.

---

## Archive Format

Write to `output/commonplace/YYYY-MM-DD-<slug>.md`:

```markdown
---
captured: YYYY-MM-DD
register: <dominant> [+ welded registers]
provenance: quoted-scripture | quoted-model | authorial | mixed
source: <attribution — author, model, book, URL, or "unknown">
---

> <the found passage, verbatim>

**Weld:** <the one sentence that makes it yours>
```

Append a one-line pointer to an `index.md`
(`- [slug](file.md) — register · provenance · first words of weld`).

**Retention:** none. Like a diary, commonplace entries accumulate permanently
— the cumulative record trains future instances by incompletion.

---

## Why This Skill Exists (not a generic clipper)

A generic note-clipper stores quotes. This skill exists because in a heavily
quoted archive the signature **is** the weld between curated voices, and the
recurring failure is mis-attribution. It writes the provenance metadata at
capture time so future archive-mining never has to guess — building the very
data whose absence makes later attribution hard.

---

## Related

- `/florilegium` — the inverse: random-sample the archive to diagnose voice-drift
- `/receive` — trans-architectural reception (commonplace is its archival cousin)
