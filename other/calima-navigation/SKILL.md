---
name: calima-navigation"
description: Drive the Calima ERP Contábil browser UI reliably — finding routes, switching modules, opening and closing modals, filling masked fields, operating react-select dropdowns, and telling a real save from a phantom one. Use whenever a task on Calima involves moving around the screen, opening a cadastro, filling a form, or verifying that a Salvar actually persisted. Contains the traps that silently produce wrong results (stale DOM reads, the 2FA overlay, truncated dropdowns, digits-only masks).
allowed-tools: browser Read Grep Glob Shell
user-invocable: true
---

> Companion to `calima-erp`, which owns the **authorisation ladder (L0–L5)**.
> This skill owns **how to drive the screen**. Read the ladder there before
> acting; this file assumes you already know your ceiling.

## When to use

- Any Calima task that needs navigation, a form, or a verification.
- Before writing any automation against Calima — the traps below are silent,
  and two of them produce confidently wrong reports.

## The three rules that matter most

### 1. The DOM is not the source of truth. Take a screenshot.

React re-renders asynchronously. Reading a table immediately after a click can
return the pre-click state, and you will conclude that a save failed when it
succeeded. This is not hypothetical: on 06/10/2026 an agent reported "the
address did not save" and "the phone did not save" — **both had saved**. The
phone had in fact saved *twice*, and the duplicate went unnoticed for several
steps.

```
await browser.click(...)            // fire and forget
await browser.screenshot({ tabID }) // ask the screen, not the DOM
```

Read the screenshot yourself. It is the only authoritative view.

Corollary for modals: **never** detect one with
`getBoundingClientRect().height > 0` — a hidden modal reports a non-zero box.
Require `getComputedStyle(x).visibility !== 'hidden'`, or just look at the
screenshot.

### 2. Verify that a click reached the button.

Two independent checks, because they fail differently:

```js
// (a) is something covering it?
const rr = b.getBoundingClientRect();
const alvo = document.elementFromPoint(
  Math.round(rr.left + rr.width / 2), Math.round(rr.top + rr.height / 2));
const livre = alvo === b || b.contains(alvo);

// (b) did it produce a request?
const n = await tools.browser.network.list({ tabID });
const postou = n.requests.some(r => r.method === 'POST');
```

`livre === false` means an overlay swallowed the click — see the 2FA rule below.

### 3. The 2FA nag must be dismissed when the screen loads.

`Ativar depois` is the user's standing instruction. Do it **as soon as the modal
appears on page load**, before typing anything — see `calima-rules` for why the
timing is what makes it free.

The "Sua conta está vulnerável" modal is positioned **over** the save button.
`elementFromPoint` on `Salvar` returns the modal, the click never fires, and
**no POST appears in the network log**. The failure is completely silent: no
error, no toast, nothing in the console.

```js
const m2fa = [...document.querySelectorAll('button')]
  .find(x => x.offsetParent !== null && /Ativar depois/i.test(x.innerText));
if (m2fa) m2fa.click();   // then, and only then, click Salvar
```

**Known cost:** dismissing it closes the form — so do it on load, not at the
end. Nothing is typed yet, so closing costs nothing.

`Ativar 2FA agora` changes account security. Never click it without asking —
it is not covered by any fill-and-save authorisation.

## Tab discipline

The tab id **changes between calls**. Always resolve it fresh:

```js
const l = await tools.browser.tabs.list();
const id = l.tabs.find(t => (t.url || '').includes('calima'))?.id || l.tabs[0].id;
```

Never reuse an id captured earlier in the session.

## Never navigate by URL

Typing a route into the address bar has dropped the Calima session twice, and
the session then demands re-login. Click a link that is already in the DOM.

## Route discovery without guessing

The whole menu is in the DOM even while collapsed. This is how routes were
found, and it never drops the session:

```js
[...document.querySelectorAll('a')]
  .map(a => (a.getAttribute('href') || '') + ' :: ' +
            (a.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 44))
  .filter(s => s.startsWith('/ger'))
  .join('\n')
```

Verified routes are listed in `references/rotas.md`.

## Switching modules

The module switcher is `#sidebar-menu-modulos-label`. The sidebar also carries
a bare dashboard anchor per module (`/ger/dashboard`, `/mfp/dashboard`, …),
which is simpler: click that anchor.

The company cadastro is in **`/ger`** (Módulo Principal › Manutenção ›
Empresa). The eSocial classification (`[01]/[02]/[03]/[04]`) lives there too,
**not** in the Folha module. Do not hunt for it under `/mfp`.

## Switching the company in the header

Modules do not own the company. The **header** does, and it persists across
modules — `Manutenção › Trabalhador`, `Vínculo`, `Dependente`, `Férias`, the
Monitor and the payroll screens all read **the company shown in the header**,
not the one you were last looking at. A `Registros: 0` that contradicts what you
know is a header-state problem far more often than a data problem.

The header shows it inside `.company-box` as `4 - VARANDA LANCHE E PIZZARIA
LTDA` plus the current reference date. Three calls, in order:

```js
document.querySelector('.company-box').click();                     // 1. open
```

```js
const input = [...document.querySelectorAll('input[type=search], input.form-control')]
  .find(i => i.offsetParent !== null);
input.focus();
const setter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype, 'value').set;
setter.call(input, 'CARLOS CAR');                                  // 2. filter
input.dispatchEvent(new Event('input', { bubbles: true }));
```

```js
[...document.querySelectorAll('.header-company-option, [class*=option]')]
  .filter(x => x.offsetParent !== null && /CARLOS CAR/i.test(x.innerText || ''))[0]
  .click();                                                        // 3. pick
```

Two details that each cost a call:

- The picker's search box has **no `placeholder`** — its "Selecione uma
  empresa…" text is not an attribute, so a placeholder lookup returns nothing.
  Match on `input[type=search]`.
- The match appears twice, as a `css-1pk5d4b-option` and a
  `.header-company-option`. Either one clicks; do not click both.

**Always read the company name back** alongside whatever you are counting:

```js
const empresa = (document.querySelector('.company-box')?.innerText || '')
  .replace(/\s+/g, ' ').slice(0, 60);
```

A count without the company name attached is unattributable, and the switcher
survives page loads, so it silently serves the wrong company for the rest of
the session. Full detail in `calima-rules` rule 83.

Switching modules can trigger the 2FA nag on arrival — rule 3 applies to every
page load, not only the first.

## Filling a field

The app uses controlled React inputs, so a plain `el.value = x` is discarded.
Dispatch through the native setter:

```js
const setVal = (el, v) => {
  const setter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value').set;
  setter.call(el, v);
  el.dispatchEvent(new Event('input',  { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
  el.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true })); // masks run here
};
```

The `keyup` is not optional — the date and phone masks format on it. Without it
the raw value stays unformatted and the field rejects on save.

**Masks reject punctuation.** See `calima-rules`.

## react-select dropdowns

**Two variants exist and they behave differently.** The `Motivo` select on the
rescisão form is a `react-select-dropdown`; the cargo/trabalhador selects are
plain `react-select`. The option element class differs
(`.react-select-dropdown__option` vs `.react-select__option`) and so does the
value-container class — a `closest('.react-select__value-container')` on a
dropdown returns `null` and reads as "nothing selected" when it is selected.

Synthetic events open the menu with **zero options**. The combination that
works is the accessibility tree plus real input:

```
await browser.snapshot({ tabID, depth: 20 })   // find the textbox ref
await browser.fill({ tabID, ref: '@eNNNN', text: 'CEN' })
await browser.snapshot({ tabID, depth: 20 })   // options now appear
await browser.click({ tabID, ref: '@eMMMM' })
```

Two limits worth knowing before you waste a step on them:

- The **main form does not expose its textboxes** in the snapshot — only
  buttons. Fields inside an open **dialog** are exposed. So the snapshot route
  works reliably for modals, not for the top-level cadastro.
- Some option lists render only ~10 entries and do not scroll. If the value you
  need is absent, it is not hidden — it is not there.

Search terms are matched loosely and inconsistently. A long term can return
nothing where a short one works (`'W'` finds a contador that `'WELLINGTON'`
does not).

## Opening and closing modals

Open: the trigger button, usually by `id`.

```js
const add = document.getElementById('addButton-telefones');
const col = add.closest('.collapse');
if (getComputedStyle(col).display === 'none') {   // section ships collapsed
  col.classList.add('show'); col.style.display = 'block';
}
add.click();
```

Close, in order of preference: the `×` in the header, then `Cancelar`. `Salvar`
inside a modal is easy to confuse with the form's own `Salvar` — scope it:

```js
const m = [...document.querySelectorAll('.modal-content')]
  .filter(x => x.getBoundingClientRect().width > 0)[0];
const b = [...m.querySelectorAll('button')]
  .find(x => /^Salvar$/i.test(x.innerText.trim()));   // the modal's, not the form's
```

Grids (endereços, telefones, e-mails, tribulações) have their add/edit/remove
buttons in a **toolbar above the grid**, not in the row. Rows are selectable:
click one and it takes the class `gt-tr active`, then the toolbar acts on it.

## Deleting a grid row

Select the row, click the remove button, then confirm in the modal. Confirming
is a separate click — do not assume the first click deleted anything.

```js
tr.click();                                   // tr must gain 'active'
document.getElementById('removeButton-telefones').click();
// then find "Sim" in the confirmation and click it
```

## Tabs and accordions — the fields may exist and still read as absent

A synthetic click on a `.nav-link` tab sets `active` on the nav but leaves the
matching `.tab-pane` at `display:none`; Bootstrap swaps it on a real click. Every
field in that pane then reports `offsetParent === null`, and a DOM dump looks
like the form has no such field at all. Fix the display against the pane that
actually holds the field:

```js
const pane = [...document.querySelectorAll('.tab-pane')]
  .find(p => p.querySelector('input[name=carteiraTrabalhoNumero]'));
document.querySelectorAll('.tab-pane')
  .forEach(p => { p.style.display = (p === pane) ? 'block' : 'none'; });
```

Inside a pane, sections are accordions whose buttons are
`button[data-testid="accordion-item-N"]`. **N is positional and changes per
record** — never hardcode it; find the button by its text inside the pane.

## Dead spinners mean "no request was made"

"Aguarde processando..." with **no buttons** is not a progress indicator. On
12/10/2026 it appeared, never resolved, and `browser.network.list` showed **no
`persistence/persist` at all** — the save had not been attempted. Verify the POST
exists before believing any save; reload and redo rather than waiting on it.

## `scrollIntoView` then measure = stale hit test

Calling `scrollIntoView()` and `getBoundingClientRect()` in the same `evaluate`
returns coordinates from before the scroll settled, so the `elementFromPoint`
check reports `Salvar` as covered when nothing covers it. Measure in a **second**
call. (Same family as "a date field can capture a later click".)

## Pagination

The grid pager **only changes between separate `evaluate` calls**. Clicking
page 2 and reading in the same call returns page 1. Read in a follow-up call.

## Reference

- `references/rotas.md` — verified routes and the catalogs already read
- `calima-rules` — the silent traps, the authorisation ceiling, and the 2FA
  instruction. **Read it before any Calima task**; every rule here is bounded
  by the ladder it holds.
