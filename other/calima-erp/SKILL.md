---
name: calima-erp"
description: Navigate, read, and diagnose the Calima ERP Contábil web system through the browser — eSocial event monitor, company registration, worker/vínculo registration, payroll, certificates. Use when the user asks to inspect or fix Calima, troubleshoot eSocial events (S-1200, S-1210, S-1299, S-2200), diagnose why payroll generates no events, or walk through a Calima registration. Includes a supervised-write protocol and a catalog of irreversible UI actions that must never be clicked without explicit approval.
allowed-tools: browser Read Grep Glob Shell
user-invocable: true
---

> ⚠️ **PRODUCTION SYSTEM WITH REAL CLIENT DATA.** Calima holds CPF, salary, health
> and bank data for the whole client portfolio. Transmitting to eSocial is a
> **legal act with fiscal consequence** — it cannot be undone, only excluded
> (S-3000) and reopened (S-1298), and every step is logged by the Receita
> Federal. This skill defaults to **read-only**. Escalation to writes requires
> explicit human approval per block. See `references/riscos.md`.

## When to use

- "Why is the S-1200 / S-1210 not being generated?"
- "Check Gilberto's / this company's registration in Calima"
- "The monitor shows the event pending but nothing happens"
- "Validate the worker cadastro before sending the admission event"
- Any request to navigate Calima on behalf of the accountant

## What is authorised, and what is not

Standing authorisation from the accountant, granted 05/10/2026:

| Level | What it touches | Status |
|---|---|---|
| **L0 — read** | Navigation, expand/collapse, filters, screenshots | **free** |
| **L1 — inspect** | Opening a detail view, reading a form, dropdown options | **free** |
| **L2 — fill** | Typing into fields, **without saving** | **allowed**, state the block first |
| **L3 — save** | `Salvar` on a cadastro (reversible by editing again) | **allowed**, one block at a time |
| **L4 — generate** | `Calcular folha`, `Carga inicial`, answering *yes* to generate an S-2200 | **not authorised** |
| **L5 — transmit** | `Enviar`, `Excluir`, `Reabrir`, DCTFWeb | **not authorised** |

**L4 and L5 are out of scope even with per-block approval.** Generating an event
puts it in the portal queue; transmitting is a legal act with fiscal
consequence. L3 is the ceiling.

At L2 and L3, always announce the block before acting — company, screen, the
exact fields, and what you will *not* touch — and report what the screen said
afterwards. Approval for one block is not approval for the next, and never
approval for the same screen later in the session.

## Hard rules

1. **Never transmit, and never generate an event.** No `Enviar selecionados`,
   no `Enviar todos`, no `Enviar fechamento`, no `Excluir`, no
   `Confirmar cálculo`, no `Carga inicial`, and never answering *yes* to
   "Deseja gerar o evento S-2200?". Saving a vínculo is L3 and allowed; the
   *yes* that follows it is L4 and is not.
2. **Never click an arrow-up action in the Monitor's "Eventos já enviados"
   tab.** It is not "view details": it opens *"o protocolo será eliminado do
   sistema... IRREVERSÍVEL"* and deletes the record if the protocol is gone from
   the portal. The XML is the **arrow-down** button. See `references/riscos.md`.
3. **Never invent a tax figure.** Classification ([01]/[02]/[03]/[04]),
   `anexoSimplesNacional`, `indSimples` — read them from the screen or from the
   client's documents. A plausible number typed here becomes a fiscal filing.
4. **Never create a duplicate worker registration.** Before proposing to
   generate an S-2200, check whether the eSocial portal already has one. A
   DCTFWeb or a payroll document from another origin is proof that the portal
   received the data — a manual payroll done by someone else still had to be
   transmitted. Undoing a duplicate needs S-2299 plus S-3000.
5. **Never leave a modal open.** Every `Sim` in Calima is a decision. Read the
   whole dialog before answering it. If unsure, close with `Não`/`Fechar`.
6. **Read the official doc before asserting.** The help center
   (`ajuda.calimaerp.com`) **overrides the training videos** — they contradict
   each other in at least three places (reopening payroll, matrix-only closing,
   carga inicial reference). Where they conflict, follow the doc and say so.

## Record every reading

After each diagnostic block, write the readings to disk — otherwise the next
session cannot tell what an event looked like last month, and "it was working"
becomes unfalsifiable:

```
.venv/bin/python -m ferramentas.calima leituras --slug gilberto --registrar
```

Compare against the previous month before claiming anything changed:

```
.venv/bin/python -m ferramentas.calima leituras --slug gilberto --comparar
```

## Method: reading is the deliverable

The most valuable output is usually **not** an action — it is a correct diagnosis.
The classic trap is acting on an unverified theory and creating the original
problem. Follow `references/diagnostico.md`: five ordered readings, then a
conclusion, then a proposal.

**The one-line rule that decides the path:**

> Empty in *"Eventos pendentes"* = the event was **never generated** → problem is
> in the calculation or the cadastro.
> Pending with a **rejection status** = it was generated and refused → problem is
> in the data.

Transmission errors always leave a trace. A missing event is an event that was
never born.

## Technical notes that will save you time

- `browser.evaluate` takes a **`script`** argument holding an **expression**, not
  a function: `{ tabID, script: "(() => { ...; return 'ok' })()" }`. Passing
  `expression` fails with `script: Missing key`, and `() => 1+1` returns `{}` —
  wrap side effects in an IIFE.
- `setTimeout` is **not available** inside `evaluate`. A script that ends with
  `await new Promise(r => setTimeout(r, 4000))` throws *Unknown identifier* —
  **after** the clicks before it have already fired. Split waiting into a
  separate call and re-read the DOM there; never assume a thrown script rolled
  back.
- **Log in at `https://www.calima.app`.** That is the login page; a successful
  login lands on `https://stable.calima.app/mfp/dashboard`. Opening
  `stable.calima.app` directly aborts with `ERR_ABORTED (-3) loading
  'https://calima.app/'` and is not worth retrying — see rule 82. Credentials
  live in `{env:CALIMA_USER}` / `{env:CALIMA_PASS}` and must never be written
  into a skill, a script or a note.
- **Direct URLs work** for the main screens — see `references/rotas.md`. Guessing
  a route gets a 404; the real routes are odd (`monitorEventoEsocialProcessView`).
- The SPA re-mounts the DOM constantly: `getElementById` can return `null` in
  one call and find the node in the next. Find **and act in the same
  expression**.
- Accordeons collapse on their own after a re-render. Read the tables in the
  *same* expression that expands them, and **do not filter by visibility** —
  hidden panels hold real data.
- The accessibility tree exposes almost nothing of Calima's content (mostly the
  chrome). Drive the DOM by text; verify with a screenshot.
- The page-size dropdown is an Ant Design `rc-select` rendered in a portal —
  read options off-screen or page through instead.
- PDFs inside Calima may use Type 3 fonts: `pdftotext` returns garbage, so
  render to PNG (`pdftoppm -r 150`) and read the image.

## References

- `references/rotas.md` — verified routes and how to reach each screen
- `references/leitura-dom.md` — copy-paste DOM recipes for each screen
- `references/riscos.md` — catalog of irreversible actions and how to spot them
- `references/diagnostico.md` — the payroll/event diagnostic procedure
