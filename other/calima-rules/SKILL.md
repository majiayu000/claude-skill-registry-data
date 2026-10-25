---
name: calima-rules"
description: Hard rules and silent failure modes of the Calima ERP Contábil web system — what breaks, what it looks like when it does, and the fix. Use whenever an action on Calima appears to do nothing, a save seems to fail, a field rejects its value, a dropdown will not open, or a result must be confirmed before reporting it. Also holds the authorisation ceiling (L0–L5) and the standing 2FA instruction.
allowed-tools: browser Read Grep Glob Shell
user-invocable: true
---

> Companion to `calima-navigation` (how to drive the screen) and `calima-register`
> (what to do, in what order).
>
> Every entry here produced a **confidently wrong conclusion**, not a visible
> error. That is what makes them worth a separate file: none of them announce
> themselves.

## The authorisation ceiling

From `calima-erp`, restated here because every rule below is bounded by it.

| Level | Touches | Status |
|---|---|---|
| **L0** read | navigation, expand/collapse, filters, screenshots | free |
| **L1** inspect | opening a detail, reading a form, dropdown options | free |
| **L2** fill | typing, **without saving** | allowed — announce the block first |
| **L3** save | `Salvar` on a cadastro | allowed — one block at a time |
| **L4** generate | `Calcular folha`, `Carga inicial`, answering *yes* to generating an S-2200 | **not authorised** |
| **L5** transmit | `Enviar`, `Excluir`, `Reabrir`, DCTFWeb | **not authorised** |

**L4 and L5 are out of scope even with per-block approval.** L3 is the ceiling.
Transmitting is a legal act with fiscal consequence.

At L2 and L3, always state the block before acting: what you touch, on which
screen, and that you are not transmitting.

## Standing instruction: dismiss the 2FA when the screen loads

**Click `Ativar depois` as soon as the modal appears when the screen loads.**
This is the user's standing instruction — do it first, not as a step before
saving.

The modal reads *"Sua conta está vulnerável… Detectamos que você ainda não
ativou a autenticação de dois fatores"* and carries exactly three buttons:
`Mais informações`, `Ativar 2FA agora`, `Ativar depois`. There is **no** `×` and
no backdrop dismissal.

Search **any** element, not just `button` — on some screens the dismissal is
an `<a>`, and a `button`-only lookup misses it and leaves the overlay in
place while the rest of the script believes it was dismissed.

```js
const m2fa = [...document.querySelectorAll('a, button, span, div')]
  .filter(x => x.offsetParent !== null && /^Ativar depois$/i.test((x.innerText || '').trim()))
  .sort((a, b) => a.innerText.length - b.innerText.length)[0];
if (m2fa) m2fa.click();
```

### Why it has to be immediate

The modal is positioned **over** the save button.

```js
document.elementFromPoint(cx, cy)
// -> div.modal fade show  "Sua conta está vulnerável..."
// ponto esta DENTRO do botao? NAO
```

The click never reaches the handler and **no POST appears in the network log**
at all — no error, no toast, nothing in the console. It reads exactly like a
broken form.

### The cost, and why timing matters

Dismissing it **closes the form**. Dismiss it right after the screen loads, not
after filling: at that point nothing has been typed yet, so closing costs
nothing.

### Never

`Ativar 2FA agora` changes account security. It is not covered by any
fill-and-save authorisation. Never click it without asking.

---

# Silent failure modes

## 1. Stale DOM read — "it did not save"

**Symptom.** Clicked `Salvar`, read the grid, got `Nenhum registro encontrado`.
Reported the save as failed.

**Truth.** It had succeeded. React re-renders asynchronously and the read landed
on the pre-render state.

**Cost.** Two grids were wrongly reported failed. Retrying a save that had
already worked produced a **duplicate** — the phone grid ended up with two
identical rows, and the extra survived several steps unnoticed.

**Fix.** Screenshot after every mutating click. The DOM is not the source of
truth here; the screen is.

## 2. Phantom modal — `getBoundingClientRect().height > 0`

**Symptom.** Reported "the modal is still open" while the user saw nothing.

**Truth.** Hidden `.modal-content` elements keep a non-zero box. Several sit in
the DOM that way permanently.

**Fix.**

```js
[...document.querySelectorAll('.modal-content')]
  .filter(x => x.getBoundingClientRect().width > 0 &&
               getComputedStyle(x).visibility !== 'hidden')
```

## 3. Digits-only masks

| Field | Document says | Must be entered |
|---|---|---|
| `I.E.` | `14.004.67-0` | `14004670` |
| `rg` | `1146.2734-2` | `114627342` |
| `numIdentOrgao` (NIRE) | `33.2.1309333-0` | `33213093330` |

Error: `Somente são permitidos números.` The stored value loses its formatting —
that is the app's choice. Do not restore the punctuation afterwards.

### `cnaefDesmembramento` is capped at two characters

```js
document.querySelector('[name=cnaefDesmembramento]').maxLength  // -> 2
```

It cannot hold CNAE codes. Error: `Campo deve ter no máximo 2 caracteres`.
Leave it empty and record the real secondary CNAEs in the manual — an invented
value is worse than none.

## 4. Masked inputs ignore programmatic clearing

Setting a masked field to `''` and firing `input` did not clear it — the mask
restored the previous value and the save wrote back a **stale number**. Use
`browser.fill` with an empty string on the dialog's ref.

## 5. react-select ignores synthetic events

`mousedown` dispatched from JS opens the menu with **zero options**, or does not
open it. The snapshot → fill → click route works.

A stale menu from a previous interaction lingers in the DOM, and a naive
`querySelector` reads it instead of the one just opened. Always close first:

```js
const menus = () => [...document.querySelectorAll('[class*="__menu"]')]
  .filter(x => x.offsetParent !== null);
const fechar = () => {
  for (let i = 0; i < 8 && menus().length; i++) {
    document.querySelectorAll('[class*="__control"]')
      .forEach(c => c.dispatchEvent(new MouseEvent('mousedown',
        { bubbles: true, cancelable: true })));
    document.dispatchEvent(new KeyboardEvent('keydown',
      { key: 'Escape', keyCode: 27, which: 27, bubbles: true, cancelable: true }));
  }
};
```

Search matching is loose and inconsistent. `'W'` finds a contador that
`'WELLINGTON'` does not; `'282'` finds a CEP that `'28230000'` does not. Start
short.

**The main cadastro form exposes only buttons in the accessibility snapshot.**
Field textboxes appear only while a **dialog** is open. So the snapshot route
works for modals, not for the top-level form.

## 6. Truncated option lists

Some selects render about ten entries and **do not scroll**; scrolling the menu
list yields nothing new. Seen on the address street-type select, where
`Avenida` was unreachable behind `10ª Travessa … 1ª Travessa da Rodovia`.

If the value you need is absent it is not hidden — it is not there. Say so in
the report rather than forcing a wrong one.

## 7. CEP auto-fill picks the wrong bairro

Selecting a CEP fills street type, UF, Cidade and **Bairro** from that CEP's
dominant entry, which may belong to someone else.

**Observed.** The company is at Av. Vereador Edenites da Silva Viana, 227,
**CENTRO**. CEP 28.230-000 auto-filled `Volta Redonda` — the sole partner's
personal address, from the shareholders' clause of the contract social.

**Fix.** After picking the CEP, read Bairro and compare against the contract
social before saving. Correcting it needs `fill` + a real click.

## 8. `Principal` is disabled on the first phone

`tipoTelefonePrincipal` ships `disabled`; the label does nothing.

**Fix.** Save the phone with any type (e.g. `Celular`). The app promotes it to
`Principal` automatically — the saved row reads `Celular, Principal`.

The address `Principal` checkbox is enabled, so it can be checked directly.

## 9. The save button is not the save button

A modal and the form can both carry a `Salvar`. Clicking the wrong one is
silent. Scope the query to the dialog:

```js
const m = [...document.querySelectorAll('.modal-content')]
  .filter(x => x.getBoundingClientRect().width > 0)[0];
const b = [...m.querySelectorAll('button')]
  .find(x => /^Salvar$/i.test(x.innerText.trim()));
```

Grid toolbars act on the **selected** row, not on a row you merely look at.
Select with a click — the row takes the class `gt-tr active`.

## 10. Accordion sections ship collapsed

`addButton-*` elements exist in the DOM with zero size because an ancestor
`div.collapse` is `display: none`. `offsetParent` is `null` and the click has
nowhere to land.

```js
const add = document.getElementById('addButton-tributacoes');
const col = add.closest('.collapse');
if (getComputedStyle(col).display === 'none') {
  col.classList.add('show'); col.style.display = 'block';
}
add.click();
```

## 11. Fields outside `.form-group`

`Código`, `CNPJ` and `Razão social` sit above the tab panes, outside any
`.form-group`. A helper locating fields by label returns nothing for them.
Address them by `name`: `input[name="cnpjFmt"]`, `input[name="razaoSocial"]`,
`input[name="codigo"]`.

## 12. Pagination only advances between calls

Clicking page 2 and reading in the **same** `evaluate` call returns page 1.
Read in a follow-up call.

## 13. Select ids renumber on every tab switch and reload

An id captured earlier now points at a different field, or at nothing. Look
fields up by label or `name` inside the active pane, never by a remembered id.

## 14. Alert modals live outside `.modal-content`

**Symptom.** A dialog loop that handles `CTPS` and `Incluir vínculo` finds
nothing, the save button reads `Aguarde...`, and the three vínculo buttons
appear loose on the page with no dialog around them.

**Truth.** Alert dialogs use `.modal-dialog.alertContainer-modal` and sit
**outside** `.modal-content`. Filters on `.modal-content`, or on `.modal`
with an `offsetParent` test, never match them — and the `.modal` wrapper has
`height: 0`, so geometry-based checks fail too.

```js
const alerta = () => [...document.querySelectorAll('.modal-dialog.alertContainer-modal')]
  .find(x => x.getBoundingClientRect().width > 0);
```

**Also.** After a write, `Salvar` becomes `Aguarde...` while the request is
in flight. That is normal, not a hang. `Incluir vínculo`, `Incluir
dependente` and `Concluir` then appear **loose on the page**, outside any
modal — click `Concluir` there to end the flow. Wait for `Salvar` to return
before reading the result.

## 15. `custom-switch` needs the input, not the wrapper

**Symptom.** A phone row saves as `Celular` instead of `Celular, Principal`,
and clicking the switch does nothing.

**Truth.** The checkbox is a `div.custom-switch > input.custom-control-input`
with its content clipped. Clicking the wrapper does not toggle; only a
direct `.click()` on the input marks it. Saving without marking it produces a
row missing its type — and repeated attempts produce **duplicate rows**.

Removing one: select the `tr` so it takes `gt-tr active`, click
`removeButton-<grid>`, then confirm with `Sim`.

## 16. Never navigate by URL

Typing a route into the address bar has dropped the Calima session twice, and
the session then demands re-login. Click a link already in the DOM.

## 17. The tab id changes between calls

```js
const l = await tools.browser.tabs.list();
const id = l.tabs.find(t => (t.url || '').includes('calima'))?.id || l.tabs[0].id;
```

Never reuse an id captured earlier in the session.

## 18. `input-money` only commits on blur

**Symptom.** A `Valor do salário` / `Saldo FGTS` field shows the right figure in
the DOM (`1.860,00`), yet the save is rejected with *"Valor deve ser maior que
zero"*.

**Truth.** The component keeps numeric state in an attribute that a
programmatic `value` write does not touch. The input's `value` reads
`1.860,00` while its `value` **attribute** stays `0`. Type with real key events
and then **blur it** — `Tab` is what commits:

```js
// after browser.press for each digit:
await tools.browser.press({ tabID, key: 'Tab' });
// then: el.value === '1.860,00' AND el.getAttribute('value') === '1860'
```

**Digits, not separators.** The mask wants **cents**: typing `185000` yields
`1.850,00`. Typing `1.850,00` gives `100.850,00`, and `1850` gives
`1.008,50`. Verify `getAttribute('value')` before saving.

`salarioMinimo` is the escape hatch — checking *"Preencher o salário com o valor
do salário mínimo"* writes a valid figure from the server's own minimum-wage
table, which is also how to read the current minimum for a reference date.

## 19. Grid rows need a click on the `<td>`, not the `<tr>`

Inside a modal list (picking a quadro de horário for a vínculo), clicking the
row does not mark it. Click the first cell:

```js
tr.querySelector('td').click();   // now: class="gt-tr active"
```

A `tr.click()` may appear to work and still leave nothing selected — verify
`/active/.test(tr.className)` before pressing `Salvar`.

## 20. react-select: type, don't press ArrowDown

`ArrowDown` opens an empty menu in most of these selects and the field looks
broken. Typing into the input and letting the component filter is the method
that opens the list. If it still returns nothing, check the **column** — see 21.

## 21. A `d-none col` field is not a field

**Symptom.** A dropdown reports `0 results available for search term X`, the
input has zero size, and no amount of typing or `ArrowDown` helps. `focus()`
reports success but `document.activeElement` is never the input.

**Truth.** Some columns ship with Bootstrap's `d-none`. The input inside has
`rect=0x0`, never receives focus, and cannot be typed into. The backend query
that fires anyway returns `{"content":[],"total":0}` — which looks exactly
like "no matches" and sends you hunting in the wrong place.

**Diagnose by geometry, not by the response.** Walk up from the input to
`.form-group` and read `getBoundingClientRect().width` at each level; the
culprit is the ancestor with `class` containing `d-none` and width `0`.

```js
let p = el;
for (let i = 0; i < 6 && p; i++, p = p.parentElement) {
  const r = p.getBoundingClientRect();
  console.log(i, p.tagName, p.className, r.width);   // 0 0 = d-none column
}
```

Removing the class makes the field work, but that is a patch on a screen that
writes official event configuration — flag it to the user, do not do it
unasked.

## 22. "Sincronização de eventos" pushes, it does not pull

Under *eSocial › Importação*, the checkbox reads *"Sincronizar vínculos"*. It
**sends** Calima vínculos to the portal; the list is your own vínculos with
`Vínculo sincronizado: Não`. It cannot import an event that Calima does not
have. To bring in an existing portal event use *Importar XML dos eventos do
eSocial* (accepts `.xml`/`.zip`, up to 120 files, events S-1000 → S-2306).

### Getting a file into the wizard

The drop zone's `<input type=file>` is **invisible to the axe tree** and
`files.upload` rejects it (`Node is not a file input element`). Make it
visible and hand `files.drop` a ref to it:

```js
const inp = document.getElementById('fileSelectorInput-arquivos');
inp.removeAttribute('hidden');
inp.style.display = 'block';        // <-- the part that matters
inp.style.cssText = 'position:fixed;top:300px;left:500px;width:320px;height:48px;opacity:0.02;z-index:999999';
inp.setAttribute('aria-label', 'Upload');
document.querySelector('.app-sidebar').style.display = 'none';  // keep the ref near the top
```

Then `browser.snapshot()` and pass the `Upload` ref to `files.drop`. Without
`display:block` the input has `display:none` and never gets a ref — this is the
single most common cause of "upload won't attach".

### Two switches act beyond the import

On the configuration step, both default to **on**:

- **Criar automaticamente no monitor de eventos do eSocial eventos pendentes
  após a importação** — queues a new event for transmission.
- **Realizar configuração do eSocial na empresa caso a mesma não possua** —
  rewrites the company's eSocial configuration.

Turning either off is not cosmetic. And `Salvar` refuses outright with
*"É necessário que a(s) empresa(s) pendente(s) de informação seja(m)
preenchida(s) antes de enviar"* — the company row must be marked first, which
opens a form demanding nationality, marital status, **admission date, CBO and
RG of the worker**: identity data typed into an event-configuration screen.
Fields the company considers "already imported" may be rendered in a `d-none`
column (see 21), so the form can demand data it will not let you see.

**Buttons may carry `undefined` in their id** (`buttonProcessViewTextundefined`)
when the backend omits the company identifier — a sign the same endpoint is
returning an incomplete payload, and that lookups from inside these modals will
come back empty while the same table works from its maintenance screen.

## 23. Lotação tributária: o que é, de onde vem, e como criar

**O que é.** A lotação tributária (S-1020) define como a empresa recolhe INSS
por estabelecimento. Não é campo de texto: é um cadastro à parte (*Folha ›
Manutenção › Configurações › Lotação tributária*) que informa:

- `codLotacao` — código interno do estabelecimento (ex.: `VARLANCH`)
- `tpLotacao` — tipo de lotação (tabela 23 do eSocial; `01` = estabelecimento
  matriz/próprio)
- `fpas` — código FPAS (ex.: 515 = comércio varejista de lanches)
- `codTercs` — terceiros (0000 = sem terceiros)
- `iniValid` — competência de vigência

**De onde vem.** Não vem do S-1000; é um evento separado (S-1020) que a
empresa já transmitiu antes. Se o Calima não tem, a validação da Carga Inicial
falha: *"É obrigatório o preenchimento da Lotação Tributária"*.

**Como criar no Calima.** *Folha › Manutenção › Configurações › Lotação
tributária > Incluir*:

| Campo | Valor (ex.: Varanda) |
|---|---|
| Código | `VARLANCH` |
| Descrição | `Estabelecimento Matriz` ou o que a empresa usa |
| Tipo de lotação | `01 - Estabelecimento matriz / PJ que trabalha por conta própria` |
| FPAS | `515` (comércio varejista de lanches) |
| Terceiros | `0000` |
| Vigência | competência de início (ex.: 09/2026) |

O tipo `01` corresponde a *"Classificação da atividade econômica exercida pela
Pessoa Jurídica para fins de atribuição de código FPAS, inclusive obras de
construção civil própria"* (tipo `OBRA_PROPRIA` no backend). É o tipo padrão
para uma empresa que opera em nome próprio, sem obra de construção civil nem
tomadora de serviços.

**Validação da Carga Inicial.** Se o dropdown *Lotação tributária* do passo 2
da Carga Inicial não encontra nada, é porque não existe registro. Não adianta
digitar no campo — o backend devolve `{"content":[],"total":0}`. Criar o
registro na manutenção, depois voltar ao wizard, revalidar e prosseguir.

**Regra prática.** Se a empresa já transmitiu S-1020 (procure no Drive ou no
portal), use os mesmos valores do XML. Não invente FPAS nem `tpLotacao`.

## 24. Masked fields need real keys — the native setter writes a value the form never saw

**Symptom.** `cpfFmt` reads `177.795.697-80` in the DOM and is still rejected
with *"CPF inválido"*. `dataNascimento` reads `24/03/1994` and is still
*"Campo não pode estar em branco"*. Re-reading the field shows the value sitting
right there. Nothing the DOM says is true.

**Truth.** The mask and the validator are driven by the real `input`/`change`
event stream. `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,
'value').set` + a synthetic `input` event updates the DOM and React's state,
but the mask's own formatting step and the field's validator never run. The
field is, as far as the form is concerned, still empty — and it says so on
save.

**Fields that need real key events** (`browser.press`, one character at a
time, then `Tab`):

`cpfFmt` · `cnpjFmt` · `dataNascimento` · `identidadeDataEmissao` ·
`dataAdmissao` · `dataOpcaoFgts` · `refInicioVigenciaFmt` · `refFimVigenciaFmt` ·
`dataInclusaoSalarioAtual` · `numeroFmt` · `valorFmt` · `reajusteFmt` ·
`horaEntrada` · `horaSaida`

**The native setter is correct** for unmasked text: `nome`, `nomeMae`,
`logradouro`, `numero`, `complemento`, `descricao`, `motivo`,
`identidadeOrgaoExpedidor`, `pis`, `codigo`, `orgaoRegistro`.

The trap is asymmetric: the setter *appears* to work on both, so the mask
looks like a validation bug rather than an event bug.

## 25. Backspace on a collapsed react-select input erases the wrong field

**Symptom.** Clearing a select before retyping wipes `dataNascimento` and
`cpfFmt` instead. The values were there a minute earlier.

**Truth.** A react-select input with a value selected renders at `rect=2x21`.
`focus()` on it reports success, but the node never genuinely takes focus, so
the keystrokes land on whatever *was* focused — commonly the masked field
behind it. `Backspace` × 18 does the damage.

```js
// gate before any destructive keystroke
const ok = await evaluate(
  "(() => { const e = document.querySelector('#someDropDown input');" +
  " e.focus(); return document.activeElement === e ? 'FOCO_OK' : 'FALHOU'; })()");
if (ok !== 'FOCO_OK') → do not type; the field cannot take input
```

Prefer not to clear at all: on a fresh form the field is already empty. Only
clear when focus was confirmed. See also 21 (`d-none` columns) — same symptom,
same discipline.

## 26. Option lists often need a second look, not a second idea

A react-select that returns `0 results available` on the first read frequently
has the option rendered a moment later. Re-read the same menu **before** retrying
with different text — and retry the *identical* search if the second read is
still empty. Typing a different word changes the result set and hides the
problem.

```js
// read once
opts = [...document.querySelectorAll('[class*="__menu"] [class*="__option"]')].filter(visible)
// read again, same search term, no new keystrokes
// only then: retry, or Escape and retype
```

Working example: `naturalidadeUF` needed `ArrowDown` to open at all, then `rj`
— but the first read after typing returned `[]` and the second returned `[RJ]`.

## 27. `react-input-date` time fields: `HH:MM:SS`, and disabled until the parent select is set

**Symptom.** `horaEntrada` / `horaSaida` reject `focus()`; typing `08:00` leaves
the mask reading `08:00:__`.

**Truth.** Two separate facts. The fields are `disabled=true` until the
enclosing select (e.g. the turno) is chosen — set the select first. And the
mask is `HH:MM:SS`: `08:00` fills hour and minute and leaves seconds as `__`.
Type the full `08:00:00`.

```js
e.focus();                       // only after disabled === false
for (const ch of "08:00:00") press(ch);
press("Tab");
```

## 28. A `disabled` panel is a display, not a broken form

**Symptom.** An entire panel of fields is permanently `disabled=true`, with no
error anywhere, and the record cannot be saved because one of those values is
"not informed".

**Truth.** The panel renders the current state; the entry point is a separate
grid in the same pane. Reading it as a defect sends you looking for a
permission problem or a browser quirk.

Verified instance: the vínculo's `Salário atual` panel
(`tipoSalarioAtual`, `dataInclusaoSalarioAtual`, `valorSalarioAtual`,
`numHorasContratadasSalarioAtual`) is display-only. The salary is entered via
the **`Histórico de salários` grid's `addButton-<grid>`** in the same pane. See
`calima-register-vinculo`.

Before assuming a field is an input, read `disabled` and then look for a grid
in the same pane:

```js
[...pane.querySelectorAll('[id^="addButton-"]')]
// addButton-salarios, addButton-quadrosHorarios, addButton-enderecos, …
```

## 29. `warning-tab` is the save gate, and it fails silently

Supersedes nothing in 1–23 but generalises it. Count the incomplete tabs before
every `Salvar`:

```js
[...document.querySelectorAll('.warning-tab')].filter(x => x.offsetParent !== null)
```

Any result means the save **will not fire a request at all** — no POST, no
error toast, no console message. It reads exactly like a button that does
nothing. Verified on the company form (`Dados complementares` incomplete →
zero network traffic) and on the worker form.

Corollary: after a failed save, **re-open the record rather than retrying**.
Some fields latch to `disabled` on failure and a retry writes a partial record
or duplicates a grid row.

## 30. A validation error does not cancel the save

The largest rule in this file, and it is counter to every other ERP.

```
POST persistence/persist  →  200
```

…arrives at the same moment a red *"Existem informações inválidas"* modal is on
screen. **The record is written.** The server validates the payload it received,
not the state the modal is complaining about.

Clicking `Salvar` a second time after that modal — which is the natural reaction
— creates a **duplicate record for the same subject**. The tell is the next
attempt's modal changing to *"Já existe outro [vínculo] ativo cadastrado para
este trabalhador, deseja continuar?"* That question is proof the first click
already wrote something.

**Treat every Calima save as one-shot.** Verify readiness *before* the click:

- required grids populated (`Registros: 1`, walking the parents — see rule 31)
- required react-selects committed (rule 32)

If a modal appears anyway: assume it was saved, verify with a **fresh** list
read (rule 33), and never press `Salvar` again on that form.

## 31. `closest('.tab-pane')` returns the wrong grid's record count

`Registros: N` lives in a card above each grid, and one card hosts several
grids. `button.closest('.tab-pane')` resolves to the tab, so you read a
sibling's count — a real false negative where a populated horário grid reported
`Registros: 0`.

```js
let p = document.getElementById('addButton-salarios'), n = '?';
for (let i = 0; i < 6 && p; i++, p = p.parentElement) {
  const m = p.innerText.match(/Registros: ([0-9]+)/);
  if (m) { n = m[1]; break; }
}
```

Always climb to the **nearest** ancestor carrying `Registros:`, never to the tab.

## 32. A react-select's `innerText` reads the open menu, not the selection

`wrapper.innerText` after `Enter` returns
`option 01 / 101 - Empregado, selected` — for a field that is in fact **empty**.
The text belongs to the dropdown overlay, not to the value.

```js
const w = document.querySelector('#idcategoria');
w.querySelector('[class*="__single-value"]')?.innerText   // absent ⇒ nothing selected
w.querySelector('input[type="hidden"]').value              // the bound value
```

The hidden input is the ground truth and holds the enum the server receives
(`EMPREGADO`, `PRAZO_INDETERMINADO`, `NORMAL`, `PRIMEIRO_EMPREGO`). An unset
select renders only a placeholder — no `__single-value`, empty hidden — and a
dump filtered by `offsetParent` hides it entirely. **Hidden defaults exist:**
`idtipoAdmissao` ships as `TRANSFERÊNCIA` while staying invisible in the visible
field list.

## 33. A list read immediately after a save reports "nothing found"

After `Salvar` returns `200`, the grid still renders *"Nenhum registro
encontrado"* and *"Registros: 0"*. The data is there. Navigate away and back
before reading — the same list then shows the record.

This has produced **two** false reports of "the save failed". Note the
distinction from rule 30: a real 500 empties the form and the record is absent
after a reload; a stale read shows the record on the next load.

Corollary for grids that follow a save inside a modal: the modal closing is
itself evidence. And `Cargo` duplicates are a genuine 500 — see below.

## 34. A duplicate code is a silent `POST 500`; a `<textarea>` hides one field

Two more save-time traps in master tables:

- **Duplicate code** → `POST persistence/persist 500`, no modal, no highlighted
  field, and the form **empties itself**. It reads as a transient failure and
  invites a retry with the same value, which fails identically. Check existing
  codes first.
- **`<textarea>` inside a custom wrapper** does not appear in an
  `input[name]` enumeration. In the Cargo form, `Descrição` lives in
  `#iddescricao textarea`; leaving it empty yields *"Descrição Campo não pode
  estar em branco"* with nothing visibly red.

## 35. `elementFromPoint` can return a *sibling* button, not an overlay

**Symptom.** The click-guard from `calima-navigation` rule 2 reports
`livre === false` on `Salvar`, which by that skill means an overlay swallowed
the click. Nothing is on screen. The record **was** saved.

**Truth.** Two buttons can sit at identical coordinates — e.g. the form's
`Salvar` (`button.btn-success`) inside `div.float-right > div.process-bar`, and
another `Salvar` elsewhere in the DOM. `elementFromPoint` legitimately returns
the *other* button, so `b.contains(alvo)` is false while nothing is covering
anything.

**Do not conclude "blocked" from this reading alone.** Walk the chain of the
returned element before acting:

```js
const alvo = document.elementFromPoint(cx, cy);
let p = alvo, chain = [];
for (let i = 0; i < 6 && p; i++, p = p.parentElement)
  chain.push(p.tagName + '.' + String(p.className).slice(0, 40) +
             ' z=' + getComputedStyle(p).zIndex);
// a real overlay carries a modal/toast ancestor and a high z-index
```

**The reliable save signal is the Toastify toast**, not the geometry:

```js
[...document.querySelectorAll('.Toastify__toast-body')]
  .map(t => (t.innerText || '').replace(/\s+/g, ' ').trim())
// -> "Sucesso Registro salvo com sucesso!"
```

Then confirm from a fresh list read (rule 33) — never by pressing `Salvar` a
second time (rule 30).

## 36. The CEP catalogue holds only the CEPs this office already uses

**Symptom.** A react-select CEP returns *"Nenhum resultado encontrado"* for a
perfectly valid CEP that the company's own documents carry.

**Truth.** The list is not a nationwide catalogue. Verified 08/10/2026 — the
whole CEP react-select held **11 entries**:

```
21330680 · 21750080 · 21815205 · 23880000 · 26011380 · 26135570
26250100 · 26250320 · 28030002 · 28030002 · 28230000
```

A company's real CEP is absent unless another client already introduced it.

**Options.** Either pick an existing CEP (then **say so in the report** — the
address is no longer the documented one), or add the CEP first at *Módulo
Principal › Manutenção › CEP*. Do not silently swap a documented CEP for one
that merely exists in the catalogue.

The select auto-fills `Tipo`, `UF`, `Cidade`, `Bairro` **and `Logradouro`** from
the CEP's dominant entry. Re-read `Bairro` and `Logradouro` afterwards: they
belong to whatever that CEP dominates, which may not be the company
(see rule 7).

## 37. The CEP / select search is async — type in one call, read in the next

**Symptom.** After typing into a select, the menu reads
`["Loading...", "Loading...", "Loading..."]`, and sweeping several search terms
inside one `evaluate` returns empty for every one of them.

**Truth.** The option list is fetched per keystroke and resolves on a later
tick. Multiple searches inside a single call all observe the *pending* state.

```js
// call 1 — type
(() => { const i = document.getElementById('react-select-29-input');
         i.focus();
         const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;
         s.call(i, '21730'); i.dispatchEvent(new Event('input', { bubbles: true }));
         return 'typed'; })()
// call 2 — read   (the call boundary is the wait)
[...document.querySelectorAll('[class*="__option"]')]
  .filter(o => o.offsetParent !== null).map(o => o.innerText.trim())
```

Stale menus accumulate — several `[class*="__menu"]` may be visible at once, and
a query reads whichever is on top. Close first with the `fechar()` recipe in
rule 5, then search once.

**Note.** On the responsável form, the native setter + synthetic `input` **does**
open the menu with options — unlike rule 5's "synthetic events open it with zero
options". Both are true on different forms; read the menu rather than assuming.

## 38. The `Tipo` de logradouro table has no plain "Rua" — and it blocks the save

**Symptom.** `Manutenção › CEP › Logradouro › Incluir`, everything filled —
Nome, UF, Cidade, Bairro, CEP correctly masked — `warning-tab` is **0**, and
`Salvar` produces **no `POST persistence/persist`** at all. Silent. Nothing in
the UI.

Searching `Rua` in `Tipo` returns only `10ª Rua, 11ª Rua, 12ª Rua, 1ª Rua, 2ª
Rua, 3ª Rua …` — **ten entries, truncated, and there is no bare `Rua`.** Same
table drives the CEP `Tipo` in the responsável and empresa address grids.

**Truth.** Two independent facts:

1. An unset `Tipo` is an **invisible save gate**, exactly like the `Responsável`
   selector on the empresa form and `Data início atividade` in *Registro da
   empresa*. `warning-tab` does **not** report it — it counts 0 while the form
   silently refuses to persist.
2. The table's plain `Rua` is unreachable, because the list renders the first
   ten matches in alphabetical order and `10ª Rua` sorts before `Rua`.

**Do not satisfy the gate with `3ª Rua`.** It is false data in a fiscal system,
and it silently mis-labels the street type on a client's registered address.

**Confirm the block by the absence of the POST**, never by the absence of a
toast:

```js
const b = [...document.querySelectorAll('button')]
  .find(x => /^Salvar$/i.test(x.innerText.trim()));
b.click();
// then:
const n = await tools.browser.network.list({ tabID });
n.requests.some(r => /persistence\/persist/.test(r.url))   // false ⇒ nothing was written
```

**Workaround that does not lie — use `Importar dados da RF`.** Do **not** drill
*Manutenção › CEP* to register a company's address. On the empresa form, typing
the CNPJ and clicking **`Importar dados da RF`** creates the `Endereços` row
directly, **bypassing the local catalogue and its broken `Tipo` table
altogether**:

```js
const b = [...document.querySelectorAll('button')]
  .find(x => /Importar dados da RF/i.test(x.innerText) && x.offsetParent !== null);
b.click();   // -> "SÃO LUIZ GONZAGA | 777 | 21.730-710 | Realengo | Rio de Janeiro | Principal"
```

Verified 08/10/2026 on CNPJ `31.310.873/0001-24`. It also fills razão social,
nome fantasia, telefone, e-mail, natureza jurídica and data de início de
atividade, and it satisfies the "at least one address marked Principal" gate by
itself. **Do this first, before typing anything** — it overwrites.

It settles address conflicts too: for BAZAR the 2025 contrato social says
**São Cristóvão** while the CNPJ card says **Realengo**. Same street, number and
CEP. **Take the CNPJ card** and record the divergence — it is the registered
address, and the older instrument was superseded.

The manual drill-down (País › UF › Cidade › Bairro › Logradouro) remains the
only route for a *partner's personal* address, where no CNPJ exists to import
from. **And for a personal address the blocker stands** — there is no `Rua` in
the `Tipo` table, so a partner whose bairro is missing cannot be registered until
Calima fixes the table.

## 41. The `0100` record in the MANAD backup is the vendor, not a worker

**Symptom.** The payroll exports at `MANAD-BCKP/*.txt` carry a `0100|` record
that looks exactly like an employee — name, cargo, PIS, two phones, an e-mail:

```
0100|SUPERSOFT SISTEMAS|Diretor|30121899||68243096000152|06731292842|(19) 3522-1200|(19)3522-8301|desenvolvimento@supersoft.com.br
```

It is **identical in all 90 files**, across unrelated companies. Reading it as
"this company has one worker named Supersoft" fabricates an employee in a live
payroll system.

**Truth.** `SUPERSOFT SISTEMAS`, CNPJ `68.243.096/0001-52`, is the **payroll
software vendor**. Its record is stamped into every export by the generating
system. It is not employment data.

**Real CPFs do appear** in these files, as bare 11-digit runs, mixed among PIS
and CNPJ. In `VARLANCH2026.txt`:

```
14190226793 · 16424495711 · 16446052790 · 16674365077 · 16674367835
```

matching the four Varanda workers already documented in
`calima-register-worker`. Separate them from PIS and CNPJ by **validating the
check digit** — never by assuming a fixed column.

**A company absent from the backup has no worker data at all.** `BAZAR E
MERCEARIA MOURARIA LTDA` has no file, and `trabalhador_vinculo.xls` is an empty
template — 54 UTF-16 strings, every one of them a column header, zero data
rows. For such a company even the **headcount is unknown**, so the trabalhador
registration cannot even be scoped. That is not a gap to fill: inventing a
workforce fabricates people with valid CPF and PIS in a live fiscal system.
Report and stop — see `calima-register-worker`, *"Deliberate gaps to report,
never to invent"*, and `calima-erp` hard rule 3.

**Blast radius.** The `Tipo` table is shared by *CEP › Logradouro* and by the
address grids in the responsável and empresa forms. A missing entry therefore
blocks the **address** of any company whose street type is not already in the
table — not just this one record.

## 39. `Estado Civil` has only the masculine form

Searching `Cas` in `estadoCivil` returns **`Casado`** and nothing else — there
is no `Casada`. The stored value is `CASADO` for a woman.

That is wrong for the eSocial: `estadoCivil` in S-2300 distinguishes the sex of
the spouse, and a wrong value produces a wrong event. The same applies to
`sexo` on the trabalhador form, where `Sexo` exists but `ficha de registro` has
no column for it.

Report it as a data-quality finding on the record, and confirm with the contador
before any event is generated. Do not silently accept masculine for feminine.

## 40. `Salvar` stuck on `Aguarde...` does not mean the save failed

**Symptom.** `POST persistence/persist` goes out, the toast never appears, the
alert list is empty, and `Salvar` stays reading **`Aguarde...`** across several
polls. Rule 14 says to wait for `Salvar` to return before reading the result —
so the form appears permanently stuck.

**Truth.** The record **was written**. The button label is a stale UI state; the
request completed. Verified 08/10/2026 on BAZAR E MERCEARIA MOURARIA LTDA,
`Registros: 7 → 8`, confirmed by list read and by reopening the record.

**Decide from the list, never from the button.**

```js
const a = [...document.querySelectorAll('a')]
  .find(x => x.getAttribute('href') === '/ger/empresaSearchView');
a.click();
// then, in the next call: read Registros and the row
```

**Never press `Salvar` again because the button reads `Aguarde...`.** Combined
with rule 30 that is the exact recipe for a duplicate company record. If the
list shows the row, it is done — close the form with `Fechar`.

Poll the button at most once or twice. Rule 14's *"wait for `Salvar` to
return"* is about not reading the DOM mid-flight, not about a label that never
resets.

## 42. A react-select can hold its value in the hidden input and still block the save

**Symptom.** On the responsável form, `nacionalidade` and `estadoCivil` read
`BRASILEIRO` / `CASADO` in their hidden inputs, every visible field is filled,
and `warning-tab` reports **0**. `Salvar` dispatches **nothing** — no
`persistence/persist`, no toast, no modal. Re-reading the list shows the record
was **not** written (`Registros` unchanged). Then, after a tab switch, the same
count reads **1**, on `Dados Pessoais`.

**Truth.** Two things, both silent:

1. **The displayed selection is gone.** `querySelectorAll('[class*="__single-value"]')`
   returns `[]` for that pane even though the hidden input still holds the enum.
   The control holds the value but React's state for it did not survive the
   re-render, so the form's completeness check sees the field as empty. This is
   the mirror image of rule 32: there the *visible* text lied; here the
   *hidden* value lies.
2. **`warning-tab` is not stable across renders.** It read `0` in one call and
   `1` in the next, with nothing changed in between.

**Read the gate and click in the same expression.** Any separate call gives the
SPA time to re-render and change the answer:

```js
(() => {
  const warns = [...document.querySelectorAll('.warning-tab')]
    .filter(w => w.offsetParent !== null);
  if (warns.length) return 'ABORT: ' + warns.map(w => w.innerText.trim()).join(',');
  const b = [...document.querySelectorAll('button')]
    .find(x => /^Salvar$/i.test(x.innerText.trim()));
  b.click();
  return 'warning-tabs=0, clicked';
})()
```

**Verify the selection, not the hidden input.** After selecting an option, assert
the `__single-value` exists *in the pane you are about to save from*:

```js
[...document.querySelectorAll('.tab-pane.active [class*="__single-value"]')]
  .map(s => s.innerText.trim())     // [] ⇒ the select is empty to the form
```

Re-select the option when this is empty; do not trust the hidden input.

**Note.** The snapshot route from `calima-navigation` cannot be used on this
form at all — a fresh `browser.snapshot` of the top-level cadastro exposes only
buttons and links (`Salvar`, `Fechar`, the three tab links), **no textboxes**.
Only fields inside an open dialog are exposed. So on the top-level forms the
native setter is the only route, and its selections need re-asserting after any
re-render.

## 43. An invalid CPF blocks the save with **zero** feedback

**Symptom.** Everything filled, `warning-tab` = 0, selects showing their values,
`Salvar` clicked — and nothing happens. No `persistence/persist`, no toast, no
modal, no console error, no red field. The list count does not move. Repeating
the whole form changes nothing.

**Truth.** `cpfFmt` carries a client-side CPF validator. When the check digits
fail, the field is invalid **and** the form refuses to submit — without marking
the field or raising anything. It is the only silent gate found that
`warning-tab` does not report.

Verified 08/10/2026 on REGINALDO MARTINS AZEVEDO: three full attempts with CPF
`529.347.861-35` all failed silently; re-issuing `529.347.861-37` saved on the
first click (`Registros: 12 → 13`).

**Validate the CPF before clicking `Salvar`, and validate it correctly.** The
obvious formula for the second digit is wrong:

```js
// WRONG — mixes a 9-digit weighted sum with a 10th digit
const d2 = 11 - ((s9 * 10 + d1) % 11);

// RIGHT — sum the first TEN digits with weights 11..2
const d2 = () => {
  let s = 0;
  for (let i = 0; i < 9; i++) s += +c[i] * (11 - i);
  s += d1 * 2;
  const r = 11 - (s % 11);
  return r >= 10 ? 0 : r;
};
```

Always reject repeated digits (`111.111.111-11` and its variants pass naive
modulo). Sanity-check the generator against a **known-good** CPF before trusting
it — `048.558.687-87` and `014.360.067-24` both validate `true`. A generator that
disagrees with a real document is the generator that is wrong.

Apply the same discipline to `cnpjFmt` and to `pis` — validate the check digit
of every number before the save, never after.

## 44. `Importar dados da RF` no-ops on the first click — systematically

**Symptom.** Type the CNPJ, click **Importar dados da RF**, and nothing is
populated: `razaoSocial` stays empty, no grid row appears, **no error, no
alert, no toast**. Click again and everything fills at once.

**This is not a defect and not company-specific.** Verified 09/10/2026 on two
unrelated companies: SALGADERIA DA NIQUE (no-op once, populated on the second
click) and R. V. LEITE ÓTICA (no-op once, populated on the second click).
A third company took two clicks as well. Earlier successes took one.

**Never assume the first click worked.** The mandatory pattern:

```js
const imp = [...document.querySelectorAll('button')]
  .find(b => /Importar dados da RF/i.test(b.innerText) && b.offsetParent !== null);
imp.click();
// then, in the NEXT call:
document.querySelector('input[name="razaoSocial"]').value;   // empty → click again
```

Budget two calls for this, always. Reading `razaoSocial` is the only reliable
success test — there is no other feedback.

## 45. A grid dialog commits **asynchronously**, showing a false error while it does

**Symptom.** In the *Telefones* / *Endereços* / *Vigências* dialog, clicking
`Salvar` leaves the dialog **open** and displays
**"Campo não pode estar em branco"** on a field you demonstrably filled. The
dialog then closes a moment later and the row is in the grid.

**Truth.** The row commits on a delayed round-trip. The validation message is
transient noise from the still-pending state, not a real rejection.

The cost is real and it was paid: navigating to the list during that window
**loses the row**, and the company then fails to save later for a reason that
has nothing to do with the phone. Two full company attempts (R. V. LEITE ÓTICA,
09/10/2026) were burned chasing a phantom "missing phone" gate.

**After saving a grid row, re-read the grid before doing anything else:**

```js
const a = document.getElementById('addButton-telefones');
const col = a.closest('.collapse');
if (getComputedStyle(col).display === 'none') { col.classList.add('show'); col.style.display = 'block'; }
[...a.closest('.card').querySelectorAll('table tr')]
  .map(tr => [...tr.querySelectorAll('td')].map(c => c.innerText.trim()).join(' | '));
```

Trust the grid, never the dialog's open/closed state and never the error text.

## 46. `cnpjFmt` rejects a programmatic value — same shape as rule 43

**Symptom.** `cnpjFmt` filled with the native setter shows the right masked
string, but **Importar dados da RF** answers *"O campo CNPJ não pode estar em
branco ou incompleto!"* — with the field displaying a perfectly complete CNPJ,
no red border, no toast.

**Truth.** Same client-side validation trap as the CPF in rule 43. The React
state never saw the value.

Digit it for real, one character at a time:

```js
const S = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
const cnpj = document.querySelector('input[name="cnpjFmt"]');
cnpj.focus(); cnpj.select();
S.call(cnpj, ''); cnpj.dispatchEvent(new Event('input', { bubbles: true }));
for (const ch of '03116103000100') {
  cnpj.dispatchEvent(new KeyboardEvent('keydown',  { key: ch, bubbles: true }));
  S.call(cnpj, cnpj.value + ch);
  cnpj.dispatchEvent(new KeyboardEvent('keypress',{ key: ch, bubbles: true, charCode: ch.charCodeAt(0) }));
  cnpj.dispatchEvent(new Event('input', { bubbles: true }));
  cnpj.dispatchEvent(new KeyboardEvent('keyup',   { key: ch, bubbles: true }));
}
cnpj.dispatchEvent(new Event('change', { bubbles: true }));
cnpj.blur();
```

The same applies to every masked field that validates on the client —
`numeroFmt` in the phone dialog included.

## 47. The `Responsável` selector rejects a short prefix; `Contador` accepts one

**Truth.** The company form's `responsavel` select matches on (near) full name.
`REGI` returns **zero options**; `REGINALDO` and `REGINALDO MARTINS AZEVEDO` both
return the person. The `Contador` select in the same tab does accept a short
prefix, and so do `Nacionalidade` and `Estado Civil` on the responsável form.

Verified 09/10/2026 on REGINALDO MARTINS AZEVEDO (`REGI` → `[]`, `REGINALDO` →
one option) and on RONALDO VIEIRA LEITE (same result).

Always type the responsible's **full name**. Two calls are needed — the option
list renders on the following call.

The field is the form-group **immediately before** *Contador* and carries **no
label**; the ids renumber on every re-render (rule 13), so locate it
positionally, never by id:

```js
const groups = [...document.querySelector('.tab-pane.active')
  .querySelectorAll('.form-group')].filter(g => g.offsetParent !== null);
const ci = groups.findIndex(g =>
  (g.querySelector('label')?.innerText || '').trim() === 'Contador');
groups[ci - 1].querySelector('input[id^="react-select-"]');   // responsável
groups[ci].querySelector('input[id^="react-select-"]');       // contador
```

## 48. Five company-form selects resolve in a single `evaluate`

**Truth.** In *Dados complementares*, the option list is present in the same
tick the filter text is set, so `Incidência tributária`, `Tipo de contribuição`,
`Qualificação da PJ`, `Natureza jurídica` and the `tipoEmpresa*` checkbox can
all be set inside one evaluate — re-querying each form-group by label after the
previous `click()`, because ids renumber (rule 13).

This collapses the complementares tab from ~11 calls to 3 and is what makes a
company cost ~13 calls instead of ~30. `responsavel` and `contador` each need
their own follow-up call (rule 47).

```js
const pick = t => [...document.querySelectorAll('[class*="__option"]')]
  .find(o => o.offsetParent !== null && o.innerText.trim() === t);
const sel = lab => { /* form-group by label, visible, width > 0 → its input */ };
const doSel = (lab, q, exact) => {
  const i = sel(lab); if (!i) return lab + ':NAOVIS';
  i.focus(); S.call(i, q); i.dispatchEvent(new Event('input', { bubbles: true }));
  const o = pick(exact); if (!o) return lab + ':NAOOPCAO';
  o.click(); return lab + ':ok';
};
const com = document.querySelector('input[name="tipoEmpresaComercio"]');
if (com && !com.checked) com.click();
[doSel('Incidência tributária',   'Não',      'Não Cumulativo'),
 doSel('Tipo de contribuição',    'Alíquota', 'Alíquota Básica'),
 doSel('Qualificação da PJ',      'Geral',    'PJ em Geral'),
 doSel('Natureza jurídica',       '206',      '206-2 - Sociedade Empresaria Limitada')]
  .forEach(x => out.push(x));
```

## 49. `refInicioVigenciaFmt` needs the **formatted** string, not a digit stream

Feeding `'122016'` character by character produces `"1_/____"` and a hidden
`refInicioVigencia` of `""`. Set the masked value whole (`'12/2016'`) with the
native setter, then `blur` — the hidden field then reads `201612`.

Leave `refFimVigenciaFmt` **empty**; the gate demands exactly one vigência with a
blank end date.

## 50. Trabalhador — two sequential save dialogs, both must be answered

Saving a worker opens two dialogs **in sequence**:

| Dialog | Answer | Why |
|---|---|---|
| `A CTPS é necessária… Deseja salvar mesmo assim?` | **Sim** | only if CTPS fields are empty; advisory, not blocking |
| `Deseja incluir um vínculo ou dependente agora?` | **Concluir** | we register the worker first; vínculo is separate |

Both live in `.modal-dialog.alertContainer-modal`, outside `.modal-content`
(rule 14). Answer **both** in the same session — navigating away between them
leaves the worker unsaved.

## 51. Trabalhador — four save gates, reported together

The save is refused with one modal listing all unmet gates:

1. **At least one address**, marked Principal — lives in `Dados complementares`
2. **At least one phone**, marked Principal — same tab
3. **RG emission date** (`identidadeDataEmissao`) — mandatory, often absent from acervo
4. **Naturalidade** — `naturalidadeUF` **and** `naturalidadeCidade`, both mandatory; UF alone is not enough

Gates 3 and 4 are Calima's own requirements — eSocial does not require RG
emission date. RG emission date for workers 2–4 can be copied from worker 1
as placeholder (report it).

## 52. Naturalidade selects — two that fight each other

`naturalidadeUF` and `naturalidadeCidade` behave differently from all other
selects:

1. **Typing does not open the menu.** Focus the input, then `ArrowDown`. Only
   then do options appear. Typing first returns `0 results available`.
2. **Selecting the UF clears the city.** Set UF first, then city — never
   the other way round.
3. **The city list is short** and does not contain every IBGE municipality.
   Sweep by letter (`ArrowDown` + filter `A`..`W`). Recreio/MG = IBGE
   `3154101` (not 3154600).

Missing municipalities are added at *Módulo Principal › Manutenção › CEP ›
Cidade* and become selectable immediately.

## 53. Vínculo — error modal does NOT block the save; it writes anyway

The save gate modal lists three items:

```
Salário não informado
Nenhum cargo foi informado
Quadro de horários não informado
```

**But the `POST persistence/persist` returns 200 and writes the vínculo
anyway.** Clicking `Salvar` again after the error creates a **duplicate
vínculo** (the first click already wrote). The re-render also resets selects
and grids to empty — a rejected save destroys the work since the last grid
save.

**Therefore: `Salvar` exactly once, and only when all three grids read
`Registros: 1` and every required select's hidden input is populated.**

Verify before saving, never after. If the modal appears, the vínculo already
exists — do NOT click `Salvar` again.

## 54. Vínculo — `idtipoAdmissao` defaults to `TRANSFERÊNCIA`, must be set to `1º Emprego`

`idtipoAdmissao` ships defaulted to `TRANSFERÊNCIA` and is not in the visible
`Gerais` dump. Left alone, `Salvar` fails with:

> "Para o tipo de admissão TRANSFERÊNCIA é necessário informar a data de
> transferência"

Options: `1º Emprego` · `Reemprego` · `Reintegração` · `Transferência`.
For first registration, pick **`1º Emprego`** (filter `1`, `Enter`; hidden
becomes `PRIMEIRO_EMPREGO`). **Set it on every vínculo**, including existing
ones — open edit form, set it, `Salvar`.

## 55. Salary and Cargo — the panels are displays; the grids are the inputs

Both `Salário atual` and `Cargo atual` panels ship `disabled=true` and stay
that way. The real entry points are the grids:

- **Salary** → aba `Salários` → `addButton-salarios` → modal with `tipoPagamento`
  (defaults `MENSAL`), `data`, `valorFmt` (type cents, then `Tab`),
  `numeroHorasContratuais`, `motivo` (`ADMISSAO`).
- **Cargo** → aba `Cargos` → `addButton-cargos` → modal with `idcargo`,
  `dataAlteracao` (override today with admission date), `motivo` (`ADMISSAO`).

`cargoAtual` and `valorSalarioAtual` panels stay empty until the vínculo is
saved; the grids are what matters.

## 56. Quadro de horário — global record, then link

Two distinct objects. The vínculo grid only **links**; it never defines.

1. **Create globally** → *Módulo Folha › Manutenção › Quadro de horário*:
   `codigo`, `descricao`, `idtipoJornada` (e.g. *"Jornada com horário diário
   fixo e folga fixa (no domingo)"*), then `addButton-quadroHorarioDia`:
   `turnodropDown` (must set first), day checkboxes, `horaEntrada`/
   `horaSaida` (`HH:MM:SS`).
2. **Link to vínculo** → aba `Horários` → `addButton-quadrosHorarios` → pick
   schedule → `Salvar` → `Salvar` vínculo.

On a fresh vínculo, `addButton-quadrosHorarios` may raise *"Não foi
encontrado nenhum vínculo… Deseja cadastrar agora?"*. Clicking **`Não`**
navigates to dashboard and **discards the entire vínculo form** — re-enter
from `Incluir`.

## 57. Selects — read the hidden input, not `innerText`

`react-select` `innerText` shows the **open dropdown menu**, not the selected
value. Two reliable reads:

```js
// 1. selected label
el.querySelector('[class*="__single-value"]')?.innerText   // absent = NOTHING selected

// 2. bound value (ground truth)
el.querySelector('input[type="hidden"]').value             // "EMPREGADO", "PRIMEIRO_EMPREGO", etc.
```

Assert **hidden input non-empty** for every required select before `Salvar`.

## 58. CBO — search by 4-digit code prefix, not name

CBO labels differ from the client's XML and are virtualised (no scrollbar,
`ArrowDown` walks past visible window). Search by **4-digit code prefix**
(`7152`, `7170`) rather than name:

| Client XML | Calima CBO | Code |
|---|---|---|
| Assistente administrativo | *Assistente administrativo* | `411010` |
| Pedreiro | *Pedreiro de edificações* | `715230` |
| Pintor de obras | *Pintor de obras* | `716610` |
| Ajudante de pedreiro | *Ajudante de obras* | `717020` |

`ArrowDown` repeatedly walks past the visible window. Give up after ~20
presses (list wraps). If a code search returns a set without the expected
entry, the CBO simply does not exist under that label.

## 59. Cargo table is shared — duplicate code = silent `POST 500`

*Folha › Manutenção › Tabelas › Cargo* is **not scoped per company**.
Duplicate cargo code fails as silent `POST 500` on `persistence/persist` —
no modal, no highlighted field, form empties itself. Pick next free code.

`Descrição` is a `<textarea>` inside `#iddescricao` — not an `input[name]`,
easy to miss. Empty description ⇒ *"Descrição Campo não pode estar em
branco"`:

```js
el = document.querySelector('#iddescricao textarea')   // ← not input[name=descricao]
```

## 60. Grid record count — `closest('.tab-pane')` picks the wrong pane

Every grid renders `Registros: N` in a card above it. `b.closest('.tab-pane')`
resolves to the containing tab which hosts several grids. Walk up until text
matches:

```js
let p = document.getElementById('addButton-quadrosHorarios'), found = '?';
for (let i = 0; i < 6 && p; i++, p = p.parentElement) {
  const m = p.innerText.match(/Registros: ([0-9]+)/);
  if (m) { found = m[1]; break; }
}
```

Verified: `addButton-cargos` → Histórico de cargos; `addButton-salarios` →
Histórico de salários; `addButton-quadrosHorarios` → Histórico de quadros
de horários.

## 61. Vínculo schedule link — click the row, no checkbox

`aba Horários` → `addButton-quadrosHorarios` grid has one row per schedule.
**Select by clicking the row** (marks `class="gt-tr active"`), then `Salvar`.
Re-read class before saving; if not `active`, click didn't register.

Modal shows *"Carregando…"* first. Poll for schedule description (e.g.
`ISAPED 44H - …`) before touching the row — clicking during load hits empty
grid.

## 62. Removing a vínculo — broken in the UI

`actionColumnRemoveButton-<n>` opens *"Confirmar remoção"*. `Confirmar` fires:

```
POST mfp/podeExcluirVinculo/<id>      → 200
POST mfp/podeGerarS3000Vinculo        → 200
```

**No delete request is issued.** Row survives full page reload under default
*Situação: Ativos* filter. Confirmed on both duplicates. **Cannot be
removed from the application.** Escalate to Calima support.

## 64. On the **trabalhador** form, `warning-tab` is always 0 — count `.is-invalid` instead

**Symptom.** Everything filled, `Salvar` clicked, **and nothing happens**: no
modal, no toast, no console error, the form silently resets. The list count
does not move. Repeating the whole form changes nothing.

**Truth.** The `trabalhador` form does not use `warning-tab` at all — it is
structurally **always 0** there, and it means nothing. (On the *empresa* form it
is the real gate — rule 29.) The actual gate is Bootstrap's `.is-invalid`
class, which the app never surfaces as a message:

```js
[...document.querySelectorAll('.is-invalid')].filter(e => e.offsetParent !== null)
  .map(e => (e.closest('.form-group')?.querySelector('label')?.innerText || '').trim());
```

Read that **before** `Salvar`. Verified 09/10/2026 on EMANUEL DA COSTA PEREIRA:
three refused saves, each with `warning-tab = 0` and zero modals, until the
`.is-invalid` list was read directly.

This is the same silent-refusal family as rule 43 (invalid CPF): the button
accepts the click, the form refuses, nothing is displayed.

### The eight mandatory fields the `.is-invalid` list exposes

None of them appear in the skill's "four gates":

| Label | Note |
|---|---|
| **Data de nascimento** | `react-date` — needs the **formatted** value + `blur` (rule 49) |
| **Data de emissão** | same, RG emission date |
| **Estado civil** | a react-select at `#estadoCivildropDown`, **not** an `input[name=estadoCivilFmt]` |
| **Nome da mãe** | plain text |
| **UF** | see below — there are **two** |

### There are TWO `UF` form-groups, and clicking one option can clear the other

The page carries `UF` twice: **naturalidade** (first) and **identidade**
(second, `#identidadeUF`). Chaining both in one evaluate — type the second,
then click whatever `RJ` option is visible — sets the **first** one, because
the visible option belongs to the still-open menu of the first. Result: one
`UF` left `.is-invalid` with no message.

Set them in separate calls, addressing them **positionally**:

```js
const gs = [...document.querySelectorAll('.form-group')].filter(g => g.offsetParent !== null);
const uf = gs.filter(g => (g.querySelector('label')?.innerText || '').trim() === 'UF');
uf[0].querySelector('input[id^="react-select-"]');   // naturalidade
uf[uf.length - 1].querySelector('input[id^="react-select-"]');   // identidade
```

Naturalidade's `Cidade` must be set **after** its `UF` — selecting the UF
clears the city, as documented in the worker skill.

## 65. The two post-save dialogs must be answered by **content**, not by button text

After `Salvar` on a trabalhador, two dialogs appear in sequence. Each exists
**twice** in the DOM (a visible instance and a hidden twin), so a query by text
returns two matches. Clicking the wrong one silently does nothing and the
record is lost.

Match on the dialog's own content and click inside that dialog:

```js
const m = [...document.querySelectorAll('.modal,.modal-dialog,[role=alert]')]
  .filter(x => getComputedStyle(x).display !== 'none')
  .find(x => /CTPS/.test(x.innerText));
[...m.querySelectorAll('button')].find(b => /^Sim$/i.test(b.innerText.trim())).click();
```

Then `/vínculo ou dependente/ → Concluir`.

**Click `Sim` exactly once per save.** Clicking it twice submits twice and the
second submission is refused — verified 09/10/2026 on NELSON RIBEIRO DE OLIVEIRA
JUNIOR, which then needed the whole form rebuilt.

## 66. A date field can capture a later click and swallow it

After `.blur()` on a `react-date` field the calendar may stay mounted. A
subsequent `Concluir` click then lands on a **day cell** — the page filled with
`1 | 2 | 3 … 31` rows that are not a table at all, and the save is lost.

If a grid read returns bare numbers in rows, a calendar is open. Close it and
re-click:

```js
document.querySelectorAll('.rdtCalendar').forEach(c => { c.style.display = 'none'; });
```

Filter those noise rows when reading a list:

```js
.filter(x => x && !/^\d+( \| \d+)+$/.test(x))
```

## 67. The worker list is scoped to the company in the header

`/mfp/trabalhadorSearchView` shows **only the workers of the company selected
in the header**, so `Registros: N` is not a global total. Switching company:

```js
document.getElementById('companySelectorPopover').click();
// filter input inside the popover, then click the OPTION element — not the row
const p = [...document.querySelectorAll('.popover')].filter(x => x.offsetParent !== null)[0];
const inp = p.querySelector('input[id^="react-select-"]');
inp.focus(); S.call(inp, 'ALUSTEEL'); inp.dispatchEvent(new Event('input', { bubbles: true }));
// next call:
const el = [...p.querySelectorAll('*')].find(x => /ALUSTEEL/i.test(x.innerText) && x.children.length === 0);
el.closest('div[class*="option"]').click();
```

Clicking the `SPAN.title` or its `.header-company-option` parent closes the
popover **without switching** — the react-select option node is the clickable
one. Confirm via `document.querySelector('.company-box').innerText`.

**After switching, navigate to `/mfp/trabalhadorSearchView` before clicking
`Incluir`** — `Incluir` acts on whatever page is loaded, and from
`/mfp/dashboard` it opens nothing.

## 68. The whole trabalhador form fits in ONE async `evaluate` — `setTimeout` is awaited

The manual flow costs ~16 tool calls per worker. It does not have to.

`browser.evaluate` **awaits a Promise returned by the page**, so an async IIFE
with `await wait(ms)` between renders collapses the entire form into one
evaluate. `execute` accepts many sequential `browser.evaluate` calls, so a
whole company fits in one tool call:

```js
(() => {
const wait = ms => new Promise(r => setTimeout(r, ms));
return (async () => {
  // type, await wait(560), ArrowDown, await wait(520), pick option, click
  return out.join(' | ');
})();
})()
```

Verified 09/10/2026: 10 workers registered in 4 `execute` calls.

**The rule that makes it work — React needs real time between an `input`
event and reading the DOM.** Without the waits everything fails *silently*:
options never render, `pick()` returns undefined, and the script reports
`NAO VIS` with no error. Chunking the calls without awaiting real time is
worse than not chunking at all.

## 69. The UF / Cidade / CEP selects need `ArrowDown`, and it must come **after** the input settles

`Sexo`, `Estado civil`, `Raça`, `Grau de instrução` and `Nacionalidade` open
their menu from the `input` event alone. **Naturalidade UF, naturalidade
Cidade, identidade UF and the address CEP do not** — they only open on
`ArrowDown`.

And the two events must be separated in time:

```js
// WRONG — both in the same tick, menu never opens
i.focus(); setter.call(i, 'RJ'); i.dispatchEvent(new Event('input', {bubbles:true}));
AD(i);

// RIGHT — React processes the filter, then the key opens the menu
i.focus(); setter.call(i, 'RJ'); i.dispatchEvent(new Event('input', {bubbles:true}));
await wait(560);
AD(i);                       // ArrowDown keydown, keyCode 40
await wait(520);
```

Measured on the naturalidade UF: type → wait 700ms → **no options**;
then `ArrowDown` → wait 700ms → `RJ` present. The key does not open the menu
until the component has re-rendered with the filtered options.

Retry once with another `ArrowDown` before declaring failure — the option
list is sometimes still settling.

## 70. `.is-invalid` lies about untouched fields — verify the two UFs by their displayed value

Rule 64 says read `.is-invalid` before `Salvar`. That is necessary but **not
sufficient**: an untouched required field never gets the class, so a form
submitted with an empty naturalidade UF and identidade UF reports
`invalids=[]`, `Salvar` is clicked, and **Calima refuses the save in total
silence** — no modal, no toast. Verified 09/10/2026 on THAIZ PEREIRA SANCHES
SILVA: three attempts lost this way.

So after filling, assert the value actually landed, rather than trusting the
absence of `.is-invalid`:

```js
const ufList = () => gs().filter(g => lt(q(g, 'label')) === 'UF');
ufList().map(g => lt(q(g, '[class*="__single-value"]')))   // must be ["RJ","RJ"]
```

First `UF` group is naturalidade, last is identidade. A `""` here is a silent
save-refusal even with `invalids=[]`.

## 71. Removing a trabalhador: the dialog demands the CPF, typed digit by digit

`button[id^=actionColumnRemoveButton-<i>]` opens *"Confirmar remoção — ATENÇÃO:
Este procedimento é irreversível! Trabalhador: N — NOME"*. **`Confirmar` does
nothing** unless the `input[name="cpfFmt"]` inside that dialog carries the
worker's CPF. No message, no toast, the counter never moves — the click is
simply swallowed.

```
remove -> dialog: "…Trabalhador: 2 - MUNIQUE DO NASCIMENTO BARBOZA | CPF | Campo não pode estar em branco | Confirmar | Cancelar"
```

That `Campo não pode estar em branco` line appears **only after** the first
`Confirmar`. A text dump truncated at 200 chars cuts it off, which is how it
survived two failed rounds on 09/10/2026.

Fill it exactly like `numeroFmt` (rule 43) — real keystrokes, not the native
setter:

```js
const inp = modal.querySelector('input[name="cpfFmt"]');
inp.focus(); inp.select(); setter.call(inp, '');
for (const ch of '10651654718') {
  inp.dispatchEvent(new KeyboardEvent('keydown', {key: ch, bubbles: true}));
  setter.call(inp, inp.value + ch);
  inp.dispatchEvent(new KeyboardEvent('keypress', {key: ch, bubbles: true, charCode: ch.charCodeAt(0)}));
  inp.dispatchEvent(new Event('input', {bubbles: true}));
  inp.dispatchEvent(new KeyboardEvent('keyup', {key: ch, bubbles: true}));
}
```

**Always select the row by name, never by the index suffix** — the id is the
row position and shifts after every removal. And re-read the dialog's own text
to confirm it names the intended person before clicking `Confirmar`; the
dialog is duplicated in the DOM (rule 65) and a stale one from a previous
removal is still clickable.

## 72. The 2FA nag overlay steals `modals[0]` — filter modals by content

A full-screen modal — *"Sua conta está vulnerável. Proteja seus dados
 agora. Detectamos que você ainda não ativou a autenticação de dois fatores
(2FA)"* — appears over the page and is **the first visible `.modal` in the
DOM**. Any helper written as `querySelectorAll('.modal')[0]` silently grabs it
instead of the dialog you just opened, and every field lookup returns `null`.

Dismiss it with **`Ativar depois`** (`button.atarivar-depois`) — this does not
enable 2FA, it only clears the nag. Then match modals by content:

```js
const visM = re => [...document.querySelectorAll('.modal,.modal-dialog')]
  .filter(x => getComputedStyle(x).display !== 'none' && re.test(x.innerText || ''))[0];
```

## 73. A `<textarea>` needs its own native setter

`HTMLInputElement.prototype.value`'s setter throws **`TypeError: Illegal
invocation`** on a textarea. `motivo` in the vínculo **Cargo** modal is a
textarea, and it is **required** — an empty one blocks the save with
`.is-invalid` on the field.

```js
const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
```

## 74. `K250` carries cargo, CBO **and salary** — the data is in the backup

`K050` is only the worker's identity. The payroll record sits in **`K250`**,
once per competência:

```
K250|CNPJ|1||F0000000002|052026|05062026|317210| |TECNICO DE SUPORTE EM TI |00|00|000000000001485,00|…
       → matricula · competencia · data · CBO · descricao_cargo · valor
```

Latest per matrícula gives the reference salary. Verified 09/10/2026:

| Empresa | Matrícula | CBO | Cargo | Salário |
|---|---|---|---|---|
| PERAINS ON | F0000000001 | 411010 | AUXILIAR ADMINISTRATIVO | R$ 1.800,00 |
| PERAINS ON | F0000000002 | 317210 | TECNICO DE SUPORTE EM TI | R$ 1.650,00 |
| DMC | F0000000001 | 411010 | ASSISTENTE ADMINISTRATIVO | R$ 2.093,00 |
| SALGADERIA | F0000000004 | 513435 | ATENDENTE | R$ 1.650,00 |
| NOEL / BRASTECH | F0000000001 | 914405 | RETIFICADOR DE MOTORES AUTOMOTIVOS | R$ 2.200,00 |

`K150` is the payroll **event catalogue** (e001 = Salário Base, e002 = Salário
Proporcional …), not per-worker data. `K300` is the calculated amounts
(INSS/FGTS/IRRF lines) — never enter those by hand.

**Do not declare salary "missing" before reading `K250`.** I asserted exactly
that and was wrong.

## 75. Category `11` in `K050` is a sócio — never a trabalhador

`K050` field 7 is the category: `01` = empregado, **`11` = sócio /
contribuinte individual**. Sócios are registered in `Manutenção ›
Responsável` and reach the company through the vínculo, **not** through the
worker list.

Registering a `11` as trabalhador pollutes the folha and breaks the
`S-2200`. Corrected 09/10/2026: 7 records removed (BRUNO BORGES DA SILVA,
LAUCIANO MANSO DE SOUZA, CARLOS HENRIQUE PEREIRA DA SILVA, MUNIQUE DO
NASCIMENTO BARBOZA, LUKAS ALBERTO DA SILVA DE OLIVEIRA, EMERSON LUIZ FERREIRA
DE OLIVEIRA, EDSON RANGEL NUNES).

## 76. In the vínculo, some selects return **nothing until you type**

`Cargo` in `Gerais` and `Cargo` in the **Cargos** grid both open with **zero
options** on an empty input and only populate on a non-empty query. Empty
input looks exactly like "the list is broken" — it isn't.

Also: the cargo list is filtered by the **CBO chosen in `Gerais`**. Picking a
CBO no cargo carries empties the select and silently blocks the save.

`Cargo` also **ignores the vínculo's own CBO** in the grid modal — it offers
all 12 company cargos.

## 77. The vínculo will not save without a salary — and `Motivo` is required too

`Salvar` on the vínculo opens the salary modal itself with **"Preencher o
salário"** when the `Salários` grid is empty. That is a hard gate: cargo and
schedule alone will not persist the vínculo.

The `Cargos` grid modal requires `Motivo` (textarea, rule 73) — an empty one
leaves the modal open with no error.

`addButton-<grid>` is the pattern for every vínculo grid:
`addButton-cargos`, `addButton-salarios`, `addButton-quadrosHorarios`,
`addButton-valesTransporte`, `addButton-planos`, … Only the active tab's
button is visible, so click the tab first.

## 78. Saving a **cargo** succeeds in silence — re-read the list to confirm

`Folha › Manutenção › Cargo` (`/mfp/cargoSearchView`) posts to
`…/spring/persistence/persist` and the record **is created**, but the page
does not navigate, shows no toast, and the grid you came from is not
refreshed. Reading the form right after `Salvar` looks exactly like a failure.

**Only a fresh navigation proves it.** Verified 09/10/2026: 12 → 13 rows, with
`13 | TECNICO DE SUPORTE EM TI | 317210` appearing.

Navigate to `/cargoSearchView/edit` directly for a new record and the page
does not open a blank form — go to the list first, wait, then click `Incluir`.

The `Código` field is a plain text input that accepts real keystrokes; there
are only three controls (`codigo`, CBO react-select, `descricao` textarea).

**Pick the CBO by its exact option label.** Searching `chapeiro` and matching
`indexOf('chapeiro')` stored CBO `724415`, not the `513435` that the existing
`Chapeiro` cargo carries. Verify the code in the list afterwards.

## 79. `valorFmt` takes **reais × 10**, no Tab — and a human must type it

`calima-register-vinculo` says *"type cents, then Tab — `180000` → `1.800,00`"*.
**Both halves are wrong.** Measured 10/10/2026 by the user:

> *"digitar 18000 não precisou do tab"*

For **R$ 1.800,00 you type `18000`** — the reais value with **one extra zero**,
not the cents value. The mask formats as you type and **needs no `Tab`**:

| Salário | Digitar |
|---|---|
| R$ 1.800,00 | `18000` |
| R$ 2.093,00 | `20930` |
| R$ 1.650,00 | `16500` |
| R$ 2.200,00 | `22000` |

**Automation cannot do this field.** Three methods, all measured:

| Method | Result |
|---|---|
| Keystroke-by-keystroke + `setter.call(el, el.value + ch)` | **`100.800,00`** — the mask reformats mid-typing and the incremental append compounds it |
| `execCommand('insertText', false, '180000')` | **`180000`** unformatted — bypasses the mask entirely |
| Native setter with the final string + `Tab` + `blur` | displays correctly, **but the form still refuses** and no request is sent |

With `valorFmt` empty, `Salvar` the vínculo asks *"o valor do salário informado
é inferior ao salário mínimo… Salvar mesmo assim?"*, then *"Valor deve ser maior
que zero"*, and **the vínculo is NOT written** — the list stays at
`Registros: 0`. This contradicts `calima-register-vinculo`, which claims the
partial payload persists with a `200`; that is **unverified for the
salary-missing case**.

So: prepare the rest of the modal, hand over, and let a human type reais × 10.
**Never fake it** with `0,00` or `salarioMinimo` — that records a false base for
INSS/FGTS/IRRF of a real employee.

Same mask family on `data`: keystroke entry leaves `_0/__/____`. The
**formatted setter** (`'04/05/2026'` + `change` + `keyup` + `blur`) *does* work
for `dataAdmissao`, `dataOpcaoFgts` and `dataAlteracao`.

## 80. What *is* drivable on the vínculo, verified end to end

Everything except the money field:

- `Gerais` — complete, `invalids=[]`, and every hidden input populated with
  the enum the server expects: `EMPREGADO`, `DEDUCOES_LEGAIS`,
  `PRAZO_INDETERMINADO`, `NORMAL`, `PRIMEIRO_EMPREGO`,
  `NAO_EXPOSICAO_A_AGENTE_NOCIVO`. **Assert the hidden inputs, not the visible
  text** (`calima-register-vinculo`).
- `matriculaEsocial` / `matricula` — **`matricula` must be left EMPTY.** The
  eSocial matrícula (`F0000000001`) is 10 characters and `matricula` is capped
  at **8**, so copying the eSocial code into it raises *"Matrícula: máximo 8
  caracteres"* and the save is refused. Set `matriculaEsocial` only; leave
  `matricula` blank. A first pass that filled both made a vínculo refuse to
  save three times before the cause was found.
- `Cargos` grid — saves cleanly. Use the **admission date** for
  `dataAlteracao` (it pre-fills with today, which makes the history a lie) and
  `motivo: ADMISSAO`.
- Dates — formatted setter only.
- `Horários` grid — links an existing quadro by **clicking the row** (no
  checkbox); the row must take `class="gt-tr active"` before `Salvar`.
  The list shows *"Carregando…"* first — poll for the description before
  clicking, or the click hits an empty grid.

## 81. A quadro de horário needs a turno **before** the header can be saved

`Manutenção › Quadro de horário` refuses to save the header with
*"É necessário o cadastro de pelo menos um horário"* until at least one turno
exists. Build order:

1. Fill `codigo`, `descricao`, `tipoJornada`
   (`Jornada com horário diário fixo e folga fixa (no domingo)` →
   hidden `HORARIO_FIXO_FOLGA_FIXA_DOMINGO`)
2. `addButton-quadroHorarioDia` → **Turno modal**:
   - `turnodropDown` **first** — `1º Turno` / `2º Turno`; `horaEntrada` and
     `horaSaida` are `disabled` until it is set
   - day checkboxes `segundaSelecionado` … `sextaSelecionado`
   - `horaEntrada`, `horaSaida` — formatted setter with **`HH:MM:SS`** works
   - `Salvar` in the modal (this one **does** save via automation)
3. Add the second turno the same way
4. **Then** `Salvar` the header

Verified 10/10/2026: with both turnos in the grid (`Registros: 2`,
`Total de horas: 45:00h`), the header saved and the list showed
`Registros: 1`.

## 63. Deliberate gaps — report, never invent

Four fields are placeholders or left blank by decision; each must be
reported:

- **RG emission date** on workers 2–4 copied from worker 1 (client had not
  produced RGs)
- **Phone** same company number on all — no worker phone in any document
- **PIS** empty on worker 1 — RG prints `00000000000` (never issued)
- **Sexo** supplied by client, not derived from name

**Report these gaps; do not invent.** Sexo is mandatory in eSocial (S-2200)
and absent from ficha de registro — must come from the client.

## 82. The login page is `www.calima.app` — `stable.calima.app` aborts

**Symptom.** `tabs.open({ url: 'https://stable.calima.app' })` returns
`ERR_ABORTED (-3) loading 'https://calima.app/'`, the tab stays on
`www.calima.app`, and the login form is right there in the DOM.

**Truth.** That is not a failure. `www.calima.app` **is** the login page, and a
successful login lands on `https://stable.calima.app/mfp/dashboard`. Do not
retry the navigation — the abort message names the redirect target.

The form is a plain `<form>`: `input[name=username]`, `input[name=password]`,
and the visible submit button reading `Entrar`. There is a second button,
`Cadastre-se`, and several hidden ones (`Autenticar`, `Voltar`, `Sim`, `Não`,
`Enviar`, `Confirmar`) — filter on `offsetParent !== null` or the wrong one fires.

```js
const setVal = (el, v) => {
  const setter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value').set;
  setter.call(el, v);
  el.dispatchEvent(new Event('input',  { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
};
setVal(document.querySelector('input[name=username]'), user);
setVal(document.querySelector('input[name=password]'), pass);
[...document.querySelectorAll('button')]
  .find(b => /^Entrar$/i.test((b.innerText || '').trim()) && b.offsetParent !== null)
  .click();
```

**Never write the credentials into a skill, a script or a note.** Reference
`{env:CALIMA_USER}` / `{env:CALIMA_PASS}` and keep the literal out of every
artifact.

## 83. The lists belong to the company in the header, not to the account

**Symptom.** `trabalhadorSearchView` reports `Registros: 0` for a company the
worker list is known to have. Or a count changes and it is unclear why.

**Truth.** `Manutenção › Trabalhador`, `Vínculo`, `Dependente`, `Férias` and the
Monitor are all scoped to the **company selected in the top header**, which
persists across modules. The sidebar shows it as
`4 - VARANDA LANCHE E PIZZARIA LTDA` next to the reference date.

**Switching it** (three calls, in this order):

```js
document.querySelector('.company-box').click();                 // 1. open
```

```js
const input = [...document.querySelectorAll('input[type=search], input.form-control')]
  .find(i => i.offsetParent !== null);
input.focus();                                                   // 2. filter
const setter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype, 'value').set;
setter.call(input, 'CARLOS CAR');
input.dispatchEvent(new Event('input', { bubbles: true }));
```

```js
[...document.querySelectorAll('.header-company-option, [class*=option]')]
  .filter(x => x.offsetParent !== null && /CARLOS CAR/i.test(x.innerText || ''))[0]
  .click();                                                      // 3. pick
```

The picker is a modal whose search box has **no `placeholder` attribute** —
look it up by `input[type=search]`, not by its "Selecione uma empresa…" text.
Matches land in a `css-1pk5d4b-option` node **and** a `.header-company-option`
node; either clicks.

**Read the company name back after switching**, in the same call that reads the
grid. A count without the company name is unattributable.

## 84. The Monitor's "no digital certificate" modal lies — and "Configurar depois" navigates

**Symptom.** An `Atenção` dialog over the Monitor de Eventos reading *"A empresa
não possui Certificado Digital. Acesse: Módulo Principal > Configurações >
Certificado Digital"*, with **Configurar agora** / **Configurar depois**.

**Two separate traps, both verified 11/10/2026.**

### 84a. The modal does not mean what it says

**Truth (ISAPED, code 5).** The Monitor raised this exact modal, and
`/ger/certificadoDigitalView` showed a certificate **already installed**:
`150257-5-28.04.2027.pfx`, password field filled, valid to 28/04/2027, with
*Remover certificado* and *Baixar certificado (A1)* available. The filename
carries the company code (`150257` = the office, `-5-` = ISAPED).

**Never conclude "no certificate" from the Monitor.** Read
`/ger/certificadoDigitalView` for the company in the header — and **take a
screenshot**. The first DOM read of that screen came back as the empty upload
form because the certificate block had not rendered yet; the same screen,
screenshot, showed it loaded. That is rule 1 producing a false negative on a
credential question.

### 84b. "Configurar depois" is a navigation, not a dismissal

Clicking it **closes the modal and navigates to
`/ger/certificadoDigitalView`**. The route changes with no toast and no error.
Any read in progress is now pointed at a different screen. After clicking it,
**re-read `location.href` and the company in the header** before continuing.

`Configurar agora` opens the certificate wizard — that is L5-adjacent (it ends
in installing a credential) and is not covered by a fill-and-save approval.

Do not treat either button as a dead end: the missing-certificate question is a
per-company fact worth recording, and the cadastro work continues regardless.

## 86. On the eSocial config screen, the S-1299 modal cancels the **entire** save

**Symptom.** On `/mfp/empresaEsocialConfigView`, set *Tipo de ambiente* to
`Ambiente oficial` (hidden input flips to `PRODUCAO`), click `Salvar`. An
`Atenção` dialog appears:

> *Ao desabilitar o envio do evento S-1299 de fechamento da folha com regras de
> validação, poderão ocorrer erros no envio… Concorda com o envio do S-1299 sem
> regras de validação?* → **Sim** | **Não**

Answer **Não** — the right instinct, it refuses the downgrade — and the field
still reads `PRODUCAO`, the Save button disappears…

…and **nothing was saved**. Navigate away, come back: the hidden input is
`PRODUCAO_RESTRITA` again. Verified 11/10/2026 on ISAPED.

**Truth.** `Não` cancels the whole screen save, not just the S-1299 clause. The
modal only appears when the switch *"Processamento do S-1299 com regras de
validação"* is **off**, so a company with it off cannot save this screen without
either that modal or that switch.

**The reference company has it on.** Varanda (code 4) — the known-good
registration — carries S-1299 validation **on**, which is why it saves silently.

**Correct order:** check/turn **on** the S-1299 validation switch *first* (the
safe direction — validation on, matching the reference), *then* change the
environment, *then* save. Never answer **Sim** to buy a silent save: that accepts
sending the payroll-closing event with **no validation**, which is a fiscal
downgrade, not a convenience.

**Confirm by re-reading, never by the form.** This screen gives no success
toast. The proof is: leave to another screen, come back, read
`input[name=tipoAmbiente]`. Secondary signal — the Monitor's banner *"Você está
no ambiente de testes"* must disappear once `PRODUCAO` actually persisted.

**Reading the switch states.** They live **outside** any `.form-group`, so a
`.form-group` walk misses them entirely:

```js
[...document.querySelectorAll('input[type=checkbox]')]
  .map((c, ix) => ({ ix, marcado: c.checked,
                     rotulo: (c.closest('.form-group')?.innerText || '').slice(0, 60) }))
  .filter(s => s.rotulo.length > 8);
```

## 87. Match a switch by its `id`/`label[for]` — never by a substring of its text

**Symptom.** On the eSocial config screen, toggling "the S-1299 switch" left
`validarEventoFechamento` untouched, turned an unrelated switch **on**, and the
S-1299 modal kept appearing. It looked exactly like "the click does not register
in React state" — and cost two save cycles chasing the wrong theory.

**Truth.** Five switches on that screen mention **S-1299**. A locator like

```js
.find(c => /S-1299/.test(c.closest('.form-group')?.innerText || ''))   // WRONG
```

takes the **first** match, which is
`check-enviarDCTFWebAutomatica` — *"Solicitação de transmissão imediata da
DCTFWeb marcada para a geração do evento S-1299"* — a different setting. The
intended one is `check-validarEventoFechamento`.

Every switch there has a stable `id` and a `label[for]`. Use them:

```js
[...document.querySelectorAll('input[type=checkbox]')]
  .map(c => ({ id: c.id, name: c.name, marcado: c.checked,
               rotulo: (document.querySelector(`label[for="${c.id}"]`)?.innerText || '')
                        .replace(/\s+/g, ' ').slice(0, 70) }))
  .filter(s => s.rotulo);
```

| `id` | Meaning |
|---|---|
| `check-enviarDCTFWebAutomatica` | immediate DCTFWeb transmission on S-1299 |
| `check-emitirRelatorioResultado` | eSocial result report after sending |
| **`check-validarEventoFechamento`** | **S-1299 with validation rules** — this is the one the modal is about |
| `check-enviarEventosTabelaNaoPeriodicos` | auto-send table / non-periodic events |
| `check-enviarEventosPeriodicos` | auto-send periodic (monthly payroll) |
| `check-enviarDecimoTerceiro` | auto-send 13th-salary events |

**Rule 15 still holds** — a direct `.click()` on the `input.custom-control-input`
does register in React. The failure was the *locator*, not the event.

**Read every switch before and after**, and if a toggle appears not to take
effect, suspect the target before suspecting the framework. Then **revert
anything you toggled by mistake in the same block** — a stray `true` on an
auto-send switch is transmission behaviour nobody approved.

**Verified fix sequence (ISAPED, 11/10/2026):** locate by `id` → revert the
wrong one → toggle `check-validarEventoFechamento` → set *Tipo de ambiente* →
`Salvar` → **no modal appears** → leave and return → both persisted.

## 88. The certificate modal cannot be dismissed — it blocks `Salvar`, and the "dismiss" navigates

**Symptom.** Mid-change on `/mfp/empresaEsocialConfigView`, the *"A empresa não
possui Certificado Digital"* dialog (rule 84) appears **over the Save button**.
`elementFromPoint` on `Salvar` returns `div.modal fade show`, the save cannot be
clicked, and the form is half-edited.

**Both obvious dismissals fail.** Verified on Farinha Itabapoanense, 11/10/2026:

- `Escape` → modal still there.
- `.modal-backdrop.click()` → modal still there.

The only two buttons are `Configurar agora` and `Configurar depois`, and per
rule 84b **"Configurar depois" navigates to the certificate screen** — which
throws away the unsaved edit. `Configurar agora` opens the wizard (L5-adjacent).

**What works: reload the page and redo the edit.**

```js
window.location.reload();   // then: dismiss 2FA, re-read, redo, save
```

The reload also re-fetches from the server, so it doubles as the
**persistence check** the save screens never give you (§86). After a reload the
certificate modal is gone and the half-finished edit is simply re-done — it is
two fields.

**Read the company name after every reload.** A reload keeps the header company,
but the 2FA modal reappears on every load and must be dismissed first.

### `#toggle-processos` is not a reload button

The sidebar icon that looks like a refresh (`#toggle-processos`, a `redo-alt`
glyph) opens the **Utilitários › Processos** modal. Clicking it does **not**
re-read the server — it gave a clean-looking "persisted" read of values that were
only ever in the DOM. Use a real reload or a leave-and-return to confirm a save.

## 89. react-select accepts a real `mousedown` on the option — two calls, not four

Rule 20 says type-don't-press-ArrowDown, and rule 5 says synthetic events do not
open the menu. Both stay true for **opening**. But once a real `ArrowDown` has
opened the menu, the option itself can be chosen programmatically:

```js
// 1. focus the select input in an evaluate, then press ArrowDown for real
// 2. then:
const alvo = [...document.querySelectorAll('[class*=__option], [role=option]')]
  .filter(x => x.offsetParent !== null)
  .find(o => /Ambiente oficial/i.test(o.innerText || ''));
alvo.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
alvo.click();
```

That replaces `ArrowUp` + `Enter` and, more importantly, replaces **reading the
option list to confirm which one is focused** — you assert on the option's
*text* instead. Verify with the hidden input afterwards:
`g.querySelector('input[type=hidden]').value === 'PRODUCAO'`.

## 90. The company picker's search box is a react-select — only the first 10 companies exist in the DOM

**Symptom.** Switching to company 11+ appears impossible. The picker lists only
companies 1–10, typing in the visible search box changes nothing, the list
container refuses to scroll, and `ArrowDown` (real *or* synthetic) does not move
the window. The obvious conclusion — "the picker is broken, I can only reach ten
companies" — is wrong.

**Two things are being conflated.** The `input[type=search]` sitting at the top
of the dialog is `#idheader-search-input` — the **global app search**
(Ctrl+Space). Typing in it, even with real key events, does **not** filter the
company list.

**The real filter is the picker's own react-select input:**

```js
const opt  = [...document.querySelectorAll('.header-company-option')]
               .find(x => x.offsetParent !== null);
const cont = opt.closest('.css-2b097c-container')
          || opt.parentElement.parentElement.parentElement;   // mindscape
const inp  = cont.querySelector('input');                     // id renumbers each open
inp.focus();
```

Then **type with real key events** — `browser.press`, one character at a time.
Synthetic `input` events do not reach this controlled component:

```js
for (const ch of ['e', 'w']) await tools.browser.press({ tabID, key: ch });
```

**Read the options in a *separate* call.** The filter applies asynchronously;
reading in the same call returns the unfiltered list and you conclude the typing
failed. The next call returns exactly one match — then click it.

**Why `ArrowDown` looks broken.** The list is virtualised
(`.css-11unzgr`, `scrollHeight 610` / `clientHeight 300`). Setting `scrollTop`
and dispatching a synthetic `scroll` does nothing — the virtualiser re-renders
from its own state, not from the scroll position you set. Use the text filter;
do not fight the virtualiser.

**Verified 11/10/2026** reaching companies 11 and 12 this way, after the
scroll and ArrowDown routes failed on all of them.

## 91. The auto-send switches are `disabled` unless the company has a digital certificate

**Symptom.** On `/mfp/empresaEsocialConfigView`, the three *Opções de automação
de envio* switches — `check-enviarEventosTabelaNaoPeriodicos`,
`check-enviarEventosPeriodicos`, `check-enviarDecimoTerceiro` — will not turn on:

```js
document.getElementById('check-enviarEventosTabelaNaoPeriodicos').click();
// checked === false
```

The input carries `disabled=""`. `label.click()` does nothing either, and the
dependent `tempoEnvioEventosTabelaNaoPeriodicos` field is disabled with it.

**This is not a bug and not a UI trick.** It is the application's rule: **no
certificate, no automatic sending.** Verified 11/10/2026:

| Company | Certificate (`/ger/certificadoDigitalView`) | Auto-send switches |
|---|---|---|
| ISAPED (5) | `150257-5-28.04.2027.pfx`, *Remover certificado* present | enabled — toggled and persisted |
| Perains On (6) | — | `disabled` |
| Bazar (7) | empty upload form, password blank, **no** *Remover certificado* | `disabled` |

**Always check `disabled` before concluding a toggle "did not register".** The
failure looks exactly like rule 15 (the click not reaching React) and costs a
wasted save cycle chasing the wrong theory — the same class of mistake as rule
87.

```js
const c = document.getElementById('check-enviarEventosTabelaNaoPeriodicos');
{ checked: c.checked, disabled: c.disabled }   // disabled === true → certificate missing
```

**Consequence for planning.** The certificate is not merely a transmission
prerequisite — it gates the *configuration* of automatic sending. A company
without one cannot even be set up to auto-send; the certificate must be
installed first (L5-adjacent: it uploads a credential).

### Reading whether a certificate is installed

The screen has two shapes, and **only a screenshot distinguishes them** (rule 1
again — the first DOM read returned the empty form before render):

- *Has one:* a filename (`150257-5-28.04.2027.pfx`), a filled password field, and
  **Remover certificado** + **Baixar certificado (A1)**.
- *Has none:* a drop zone (*Selecione um arquivo*), an empty password field,
  `Salvar` / `Fechar`.

The Monitor's *"a empresa não possui Certificado Digital"* modal is **not** a
reliable signal either way — see rule 84a.

### Never reload in the same call that clicks Save

Clicking `Salvar` and then calling `window.location.reload()` **in the same
`evaluate`** aborts the in-flight `POST`: the form comes back with the old
values and the save silently never happened. Split them across calls — click
Save, read the result in the *next* call, then reload.

### Installing a certificate — the file input is invisible to the a11y tree

`/ger/certificadoDigitalView` has `<input id="arquivos" accept=".pfx">` nested
inside `<label for="arquivos">`. `files.upload` and `files.drop` both need a
**ref from a snapshot**, and the input is not in the tree — not even after
`display: block`. Styling alone is not enough; **it has to leave the label**:

```js
const inp = document.getElementById('arquivos');
const cap = document.createElement('label');
cap.textContent = 'UploadCertificado';
cap.setAttribute('for', 'arquivos');
cap.style.cssText = 'position:fixed;top:180px;left:380px;z-index:999999;background:#ff0';
document.body.appendChild(cap);
document.body.appendChild(inp);                    // <- the part that matters
inp.style.cssText = 'position:fixed;top:210px;left:380px;width:360px;'
                  + 'height:48px;opacity:1;z-index:999999;';
```

Now it appears as `[button] "UploadCertificado"` and `files.upload` attaches
the file. Take the **snapshot in the same call** as the upload — refs go stale
between calls and every attempt then fails with *"Element ref is stale"*.

**`inp.files.length` reads 0 even on success.** The app consumes the file and
resets the input immediately. Verify by the **filename rendered on the page**,
not by the input:

```js
/WELLINGTON/i.test(document.body.innerText)   // true == attached
```

Sequence: attach → type the password into `input[name=senhaCertificadoDigital]`
→ `Salvar` → the screen must show a filename, a filled password and
**Remover certificado**. Then reload and confirm it survived.

### Calima renames the certificate per company

An installed certificate is stored as
`<officeCode>-<companyCode>-<expiry>.pfx` — e.g. `150257-7-28.04.2027.pfx` on
Bazar, `150257-5-28.04.2027.pfx` on ISAPED. **The same `.pfx` uploaded on two
companies yields two differently-named copies.** Do not read a different
filename as a different certificate — and note this also means ISAPED's
"company" certificate is very likely the contador's own, not a separate one.

### The certificate unlocks the auto-send switches — verified end to end

Installing the certificate on Bazar (7) flipped the three auto-send inputs from
`disabled=""` to usable, and they then toggled and persisted. That is the whole
dependency chain in one observation:

```
certificate  →  auto-send switches become enabled  →  automations can be set
```

So a company that reports "I want automatic sending enabled" is blocked on the
certificate first — not on the automation settings.

## 85. `Tipo de ambiente` — the hidden input is the truth, and "teste" voids everything

**Where.** `Módulo Folha › eSocial › Configurações › Geral` →
`/mfp/empresaEsocialConfigView`. Field `Tipo de ambiente`, hidden input
`name=tipoAmbiente`.

| Visible label | Hidden value | Meaning |
|---|---|---|
| `Ambiente oficial` | `PRODUCAO` | sent data has legal effect |
| `Ambiente de teste` | `PRODUCAO_RESTRITA` | **nothing sent has legal effect** |

**Read the hidden input, never the label** — same failure as rule 20 on the
vínculo selects. The select opens with `focus()` + a real `ArrowDown`, not a
synthetic `mousedown` (rule 5).

**The consequence is the part that matters.** With `PRODUCAO_RESTRITA` the
Monitor shows *"Você está no ambiente de testes. Os dados gerados não são
considerados como valores oficiais para o eSocial"* and the semáforo line
reports *"Não foi possível buscar as informações do semáforo do eSocial"*. So an
empty pending list there is **not** evidence that there is nothing to send.

**Verified 11/10/2026 (build 5.4.8.1.12):** Varanda Lanche (code 4) is
`PRODUCAO`; Carlos Car (code 9) — registered days later, same way — is
`PRODUCAO_RESTRITA`. Environment is **per company** and is **not** replicated by
saving a cadastro: it has to be set company by company, and `Replicar as
configurações` must stay on `Somente a empresa atual` so the reference company
is not caught by the change.

Official procedure (help centre, *"Como alterar o eSocial para o Ambiente
Oficial?"*, updated 04/05/2026): the same screen, field `Tipo de ambiente` →
`Ambiente Oficial` → `Salvar`.

---

## 92. The CBO lives in the **shared cargo catalog**, never on the vínculo

**The mistake that starts all of this.** The cargo grid in a vínculo stores a
*cargo record id*. The CBO is a property of that catalog row, not of the
vínculo and not of the worker. Editing `Relação de cargos e salários` cannot
change a CBO — it can only point the worker at a *different* cargo.

| Layer | Screen | Holds |
|---|---|---|
| Worker | `/mfp/vinculoSearchView/edit/<id>` | which cargo applies from which date |
| Catalog | `/mfp/cargoSearchView` | `código \| descrição \| código CBO` |
| Authority | `/mfp/cboSearchView` | the CBO table Calima validates against |

**The catalog is shared across companies.** Verified 12/10/2026 — Perains On
(code 6) shows the identical row `10 \| PEDREIRO \| 715230` that ISAPED
(code 5) shows. Treat any catalog edit as affecting every company until
proven otherwise.

So "correct one worker's CBO" is really "edit a row several workers, in
several companies, point at". **Say this before doing it** — the blast radius
is almost never what the request implies.

### The cargo select filters by CBO code, and only while you type

In the cargo modal the checkbox set is `codigo`, `descricao`, **`cbo_codigo`**.
Typing `715210` with all three checked returns *"Nenhum resultado
encontrado"* when no catalog row carries that CBO — which is the answer. The
catalog list is the ground truth; do not fight the select.

## 93. A CBO code covers **several** occupations — compare codes, not names

`/mfp/cboSearchView` is not one code = one job. Verified 12/10/2026:

| Code | Occupations sharing it |
|---|---|
| **715210** | Pedreiro · de acabamento · de concreto · de fachada · de manutenção e conservação · de reforma geral · Entaipador · Entijolador · Estucador |
| **715230** | Pedreiro de edificações · de alvenaria · Alvanel · Alvaner |
| **717020** | Servente (construção civil) · Servente de obras · Servente de pedreiro |

**This dissolves most "divergences" before they become work.** A ficha saying
*Servente*, a payroll `K250` saying *Ajudante de pedreiro* and Calima saying
*AJUDANTE DE PEDREIRO* can be the **same code** — 717020 — under three names.
Check the code first; only escalate to a decision when the *codes* differ.

A legacy-looking catalog label is not evidence of a wrong CBO, and neither is a
ficha's plain-language job title. Only the code settles it.

**To search the CBO table.** `buttonFilterSearch-<n>` opens the filter, tick
`codigo---n` / `descricao---n`, type into the `input.form-control-sm`, then
click `buttonCustomSearchRefresh-<n>`. The `<n>` is positional and changes per
page render — read it, never hardcode it. **The search input needs real
keystrokes after `focus()`**; setting `.value` synthetically fires no query.

## 94. `naoCalcularRescisao` **masks** the validation error behind a dead spinner

**This cost a full save cycle and looked like a hang.** Sequence, 12/10/2026:

1. Rescisão form with `naoCalcularRescisao` on, `#arquivos` populated.
2. `Salvar` → modal *"Deseja incluir as férias que o colaborador tem direito no
   cálculo da rescisão?"* → `Sim`.
3. A spinner **"Aguarde processando..."** appears — **no buttons, no backdrop
   dismiss**.
4. It never resolves. `vinculoSearchView` shows the rescisão **not saved**.

**There was no POST at all.** `browser.network.list` showed no
`persistence/persist` — only `definirAvisoPrevio` and `obterFeriasRescisao`,
both 200. The same save **without the file attached** returned the real error
immediately: *"Data do pagamento não pode estar em branco."*

Two lessons, both hard-won:

- **A spinner with no buttons is not "processing".** Verify
  `persistence/persist` in the network list before believing any save. If it
  never fired, nothing happened — reload and redo rather than waiting.
- **Moving a file input out of its `<label>` orphans the multipart upload.**
  That trick is for *reading* the control (rule: certificate upload), not for
  saving. If a save hangs while a file is attached, detach it first.

## 95. On the rescisão form, selecting the worker **resets** the form

Choosing the trabalhador in `react-select-404` re-renders the whole form:
`naoCalcularRescisao` returns to `false` and the dates clear. Tick the checkbox
**after** the worker is selected, never before.

`dtPagamento` is **required** (*"Data do pagamento não pode estar em branco"*).
The TRCT has **no payment-date field** — it carries 24 Admissão, 25 Aviso
Prévio, 26 Afastamento and stops. A payment date therefore has to come from
elsewhere (document metadata, bank statement) and is an **inference** whenever
you derive it. Flag it as such; never present a derived date as document data.

## 96. The aviso prévio flags contradict each other unless you fix them

Marking `avisoPrevioIndenizado` **auto-checks** `jaRecebeuAvisoPrevioTrabalhado`
— the form then claims the notice was both paid out and worked. Uncheck the
latter explicitly.

`duracaoAviso` recalculates from admissão → afastamento (02/12/2024 → 15/01/2026
= **33** days), so it is derived, not typed.

The férias modal is asked **even with `naoCalcularRescisao` on**. It is inert
then — answer `Sim` (rule 65: advisory dialogs, `Sim`).

## 97. Saving a rescisão **generates the pending S-2300 for you**

`mfp/gerarPendenteRescisaoSemCalculo/<uuid>/<empresa>/undefined/false` → 200,
alongside `persistence/persist` and `mfp/rescisaoCalculada`.

Queued as **pending**; nothing is transmitted. Transmission stays L5.

**A rescindido vínculo disappears from `/mfp/vinculoSearchView`.** That
absence *is* the success signal — not a bug, not a lost record. Verify by
re-reading the worker list, exactly as rule 78 requires for a saved cargo.

## 98. The Monitor only ever shows the **current** reference period

`referenciaEvtPendenteFmt` (`idreferenciaEvtPendentefmt`) is `MM/YYYY` and
defaults to the current month. A rescisão dated 15/01/2026 will **not** appear
while the field reads `10/2026`, no matter that the event exists.

Typing into the field is not enough on its own — dispatch `change` and let the
list refresh. But if the event still does not surface, that is a real gap worth
reporting, not a filter artefact to wave away.

**An empty pending list is never proof that nothing was generated** — the same
family of error as rule 85, and it has the opposite direction: there you were
looking at a void environment, here you are looking at the wrong month.

## 99. On the trabalhador form, the `.tab-pane` desyncs from React's `active`

Clicking a `.nav-link` tab with a synthetic click sets `active` on the nav but
leaves the matching `.tab-pane` at `display:none` — Bootstrap swaps it on a real
click. The fields then report `offsetParent === null` and look **absent** from
the DOM dump, which reads as "this form has no such field".

```js
const pane = [...document.querySelectorAll('.tab-pane')]
  .find(p => p.querySelector('input[name=carteiraTrabalhoNumero]'));
document.querySelectorAll('.tab-pane')
  .forEach(p => { p.style.display = (p === pane) ? 'block' : 'none'; });
```

React's state already agrees with this — you are fixing CSS, not faking UI
state. Note the CTPS lives in **"Dados principais"**, *not* in "Dados
complementares", despite the name.

## 100. The CTPS lives in a per-record accordion — `data-testid` is positional

The accordion headers are `button[data-testid="accordion-item-N"]` where **N is
positional and changes between records**. Never hardcode `-3`; find it by its
text inside the pane:

```js
const btn = [...pane.querySelectorAll('button[data-testid]')]
  .find(b => /Carteira de trabalho/i.test(b.innerText));
```

| Field | Name | Max |
|---|---|---|
| CTPS nº | `carteiraTrabalhoNumero` | 11 |
| CTPS série | `carteiraTrabalhoSerie` | 5 |
| CTPS emissão | `carteiraTrabalhoDataEmissao` | — |

Saving a CTPS without its emission date raises the advisory *"A CTPS é
necessária na emissão de arquivos digitais como SEFIP e GRRF..."* → `Sim`. That
modal is the reason a CTPS-only save appears to fail.

Título de eleitor is a **sibling** accordion: `tituloEleitor`, `secaoEleitoral`,
`zonaEleitoral`. Brazilian títulos are **13 digits** (12 sequential + check
digit). A source that shows 10 or 12 has been **truncated** — do not write a
partial legal identifier. Leave it empty and flag it.

## 101. `Salvar` reads as COVERED right after `scrollIntoView`

Calling `scrollIntoView()` and `getBoundingClientRect()` in the **same**
`evaluate` returns stale coordinates. The hit test then fails and the button
reports as covered when nothing is over it — the same false "COBERTO" as rule
66. Read the rect in a **second** call, or hit-test against the rect you just
measured, once the position has settled.

## 102. Read scanned fichas at 400 dpi and crop the field — 150 dpi lies

A 150 dpi render of a handwritten ficha produced a **wrong legal identifier**:
ALAN's PIS read as `16035183811` when the document says `16035183841`, which
briefly looked like a transcription error in the ficha.

```sh
pdftoppm -r 400 -png -f 1 -l 1 ficha.pdf hi_NOME
magick hi_NOME-1.png -crop 3300x1500+0+500 +repage -resize 1800x crop_NOME.png
magick hi_NOME-1.png -crop 3000x260+0+1050 +repage -normalize campo.png
```

Crop the single field band and read it alone — context costs resolution.
Identity cards at this resolution round-trip cleanly: `30.611.252-5` was
misread as 8 digits at 150 dpi and is unambiguous at 400 dpi.
