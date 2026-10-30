---
name: narrow
description: The house style for EVERY file in this repo — source, tests, docs, configs. ~50-column lines (they fit Michael's phone preview pane), 2-space indent, flat structure, and rich explanatory comments that define every acronym. Load this before writing or editing any file.
---

# narrow — the house style

Applies to **all files**: source, documentation,
tests, configs, mailbox messages. No file type
is exempt; only unbreakable tokens are (below).

## 1. The rule, verbatim

> Source lines <= ~50 columns (they fit his
> phone preview pane). 2-space indent. Deep
> nesting is a design smell — flatten or
> extract.

And its two companions, also verbatim:

> Define every acronym at its definition site
> in a comment the first time it appears
> (RPN = Reverse Polish Notation, TTS = Text
> To Speech, DHT = Distributed Hash Table,
> DI = Dependency Injection, etc.).

> Comments are rich and explanatory on
> purpose — he loves reading the code. Match
> that voice.

## 2. Interpreting "~50"

- Aim at **50**. The `~` is a small grace, not
  a loophole: the working checker in this repo
  flags anything past **52**:

  ```
  awk 'length > 52 {print FILENAME":"FNR}' *.js
  ```

- Unbreakable tokens are exempt: a long URL, a
  base58 program id, a JSON string value, a
  markdown table row. Put the token on its own
  line; keep the prose around it narrow.
- WHY 50: lines fit a phone preview pane. The
  code is read on a phone more often than on a
  monitor. If it wraps there, it's wrong here.

## 3. Wrapping patterns (examples)

Break after operators/commas, indent the
continuation 2 spaces (or align into the call):

```js
// BAD — 80 wide, unreadable on the phone
const e = { ...ev, _seq: seq, _at: ev._at || now(), _id: ev._id || nodeId + ':' + seq };

// GOOD — the same object, narrow
const e = {
  ...ev, _seq: seq,
  _at: ev._at || now(),
  _id: ev._id || nodeId + ':' + seq,
};
```

```js
// GOOD — conditions split before operators
if (top.kind !== 'op') break;
if (tp > p || (tp === p && a === 'L'))
  out.push(st.pop());
```

```rust
// GOOD — rust chains break at the dot
ben.balance = ben
  .balance
  .checked_add(amount)
  .ok_or(LedgerError::Overflow)?;
```

Flatten instead of nesting: early-return, or
extract a named helper. Three indent levels is
the smell threshold.

```js
// BAD — nesting as control flow
if (a.type === 'KEY') {
  if (k === 'C') {
    return [{ type: 'Cleared' }];
  } else { ... }
}

// GOOD — guards, one level
if (action.type !== 'KEY') return [];
if (k === 'C') return [{ type: 'Cleared' }];
```

## 4. Comments — where they go

**File header banner** (every source file): a
framed block stating what the file IS, the
philosophy it carries, and any diagram worth
drawing. Pattern:

```js
/* ==============================================
 * NAME — one-line role     (<=50 col house)
 * ----------------------------------------------
 * Several sentences of real explanation. Why
 * this exists, what doctrine it enforces, what
 * the reader must not break.
 * ============================================ */
```

**Section rules** split a file into named parts:

```js
// -- the event tape -----------------------
// ---- instruction contexts -------------------
```

**Block comments ABOVE the code** they explain —
a short paragraph before a function or a tricky
region, never a novel inside it:

```js
// fold one event, notify, return its effects.
// an event carries identity (_id) and origin
// (_origin = the node that first decided it) so
// sync can dedup and avoid echo loops.
function commit(ev) { ... }
```

**Trailing comments** only for tiny labels that
fit the same line:

```js
const log = [];         // append-only facts
const RATE: u64 = 100;  // tokens per cent
```

## 5. Comments — the voice

- **Rich and explanatory on purpose.** The
  comments teach; the reader is here for
  pleasure as much as reference. Explain WHY
  and the doctrine, not what the next line
  syntactically does.
- **Define every acronym at first use**, in a
  comment, at its definition site: `PDA =
  Program Derived Address`, `SBF = Solana
  Bytecode Format`.
- State invariants in CAPS where they matter:
  `THE LOG IS NEVER REWRITTEN.`
- It's fine — encouraged — for a comment to
  carry personality ("a browser is enemy
  territory for secrets"), as long as it's
  also precise.

## 6. Tests and docs too

- Test files open with the same banner, and it
  lists the numbered claims the file proves.
  Test names are sentences: `ok('log keeps
  originals — never rewritten', ...)`.
- Markdown prose wraps at ~50 like everything
  else; long links/table rows are the exempt
  tokens. Headers small and frequent; tables
  for status, prose for reasoning.
- 2-space indent everywhere, including YAML,
  JSON (where formatting is ours to choose),
  and shell.
