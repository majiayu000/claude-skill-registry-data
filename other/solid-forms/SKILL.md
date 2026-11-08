---
name: solid-forms
description: The rules for editable form controls in this Solid.js frontend — inputs that keep focus while you type, numbers that can be emptied and can hold a decimal, values rounded so HTML5 step validation cannot block a save, months picked without scrolling through years, and a refused save said under the field it is about instead of in a toast. Read BEFORE writing or reviewing any component with an <input>, a <select>, or a <For> over editable rows. These are shipped bugs, each found by a user, each cheap to reintroduce.
---

# Editable controls in this frontend

Five bugs keep coming back. Every one of them ships looking fine and fails only when a
real person types into it, which is why none of them are caught by reading the diff.

## 1. A list of editable rows uses `<Index>`, never `<For>`

**The bug the user sees:** the field loses focus after every single character. Type "4500"
and you get "4", then the caret is gone.

**Why:** `<For>` is keyed _by reference_. The standard update is

```tsx
setRows(rows().map((r, j) => (j === i ? { ...r, amount: n } : r)));
```

which creates a **new object** for the edited row. `<For>` compares references, sees a
different one, disposes that row's DOM and builds it again — so the `<input>` the caret was
in no longer exists.

**The fix:** `<Index>` keys by position. The DOM node is stable; only the value updates.

```tsx
// Wrong — rebuilds the row on every keystroke
<For each={settings().incomeSteps}>
  {(step, i) => <input value={step.monthlyAmount} onInput={...i()...} />}
</For>

// Right — the row survives, the value changes
<Index each={settings().incomeSteps}>
  {(step, i) => <input value={step().monthlyAmount} onInput={...i...} />}
</Index>
```

Mind the flipped signature: in `<Index>` the **item is an accessor** (`step()`) and the
**index is a plain number** (`i`, not `i()`).

`<For>` remains correct for read-only lists, where nothing holds a caret.

**Rule of thumb:** does a row contain an `<input>`, `<select>` or `<textarea>`? Then
`<Index>`. Otherwise `<For>`.

## 2. Never write to a focused field

**The bug the user sees:** the box cannot be emptied — clear it and "0" reappears under the
caret. Or a decimal is impossible, because the keystroke that makes the text "3." is eaten.

**Why:** `value={someNumber}` compiles to an effect that writes to the element whenever the
model changes — including the changes this very field just caused. And a partly-typed
number is not a number: while the text reads `3.` or `-`, `<input type="number">` reports
`value === ''` and enters its bad-input state. Anything that writes to `value` at that
instant discards the text the user can still see.

**The fix:** use `frontend/src/components/NumberField.tsx`. It renders the value once
untracked and syncs from the model only when the element does not have focus. Do not
hand-roll `value={n}` + `onInput={e => set(Number(e.currentTarget.value))}` — that is the
bug, written out.

```tsx
<NumberField
  step="0.01"
  class={styles.formControl}
  testId="retirement-input-networth"
  value={settings().netWorth}
  onChange={(v) => update('netWorth', v)}
/>
```

## 3. Round every derived number, or the form will refuse to save

**The bug the user sees:** an auto-filled field reads `7.292500000001382`, and clicking
Save does nothing.

**Why:** an average is a division, and a division of money produces float noise. HTML5
marks a value that is not a whole multiple of `step` **invalid**, and one invalid field
blocks the entire `<form>` from submitting — the browser puts a validation bubble on a
number the user never typed and cannot fix.

**The fix:** round at every point a number is _produced_, not where it is displayed.
`shared/retirementSettings.ts` exports `round(value, decimals = 2)`; `num()` applies it to
every stored field. Round the averages, and round again after arithmetic on them — a
difference of two 2dp numbers is not itself 2dp.

Match precision to the control:

| Field kind                            | `step`   | decimals |
| ------------------------------------- | -------- | -------- |
| money                                 | `"0.01"` | 2        |
| percentages                           | `"0.01"` | 2        |
| whole things (age, %s of a portfolio) | `"1"`    | 0        |

A `step="0.1"` on a field holding two decimals is the same bug in a smaller coat.

## 4. `<input type="month">` and `type="date"` are not acceptable for anything historical

**The bug the user sees:** picking a birth month means clicking back through thirty years,
one year at a time.

**Why:** Chromium's month picker is a day-calendar with the days removed and steps the year
one click at a time; Firefox offers no picker at all.

**The fix:** use `frontend/src/components/MonthPicker.tsx` — a month `<select>` and a year
`<select>`, styled as one control. Any year is one gesture away and type-ahead works
("1990"). It emits and accepts the same `YYYY-MM` string, so storage is unchanged.

```tsx
<MonthPicker
  class={styles.monthPicker}
  ariaLabel="Date of birth"
  fromYear={NOW_YEAR - 120}
  toYear={NOW_YEAR}
  allowEmpty
  value={settings().birthMonth}
  onChange={(v) => update('birthMonth', v)}
/>
```

A month value has no day in it, so it needs no calendar at all.

## 5. A refused save is said in the form, under the field it is about

**The bug the user sees:** a toast in the corner says "Validation failed", or "Failed to save
category", and the dialog is still open with nothing in it marked. Or the browser's own bubble
says "Please fill out this field." in the browser's words. The reason existed: the server sent
it, field by field, and the form's `catch` threw it away.

**Why:** every form caught the refusal and toasted it. A toast is the wrong place for it: it is
away from the field, it goes on its own, and a screen reader hears it out of context. And
`err instanceof Error ? err.message : '…'` prints whatever the error says, which is as often
"Failed to fetch" or a `TypeError` as anything a person can act on.

**The fix:** build the form from the kit in `frontend/src/components/form/`.

```tsx
const form = createForm({
  initial: { name: '', icon: '' },
  check: (values) => fieldErrorsOf(checkCategoryCreate(values)), // {} when it can be sent
  send: (values) => apiPost('/api/categories', values), // throws ApiError, with the server's fields
  saved: () => close(), // only while this is still the form that sent
  failure: "Couldn't save the category. Try again.", // for an error with no words of its own
});
```

```tsx
<form {...form.attrs}>
  <FormNotice form={form} />
  <Field form={form} name="name" label="Category Name">
    {(control) => (
      <input
        {...control}
        required
        value={form.values.name}
        onInput={(e) => form.set('name', e.currentTarget.value)}
      />
    )}
  </Field>
  <SubmitButton busy={form.submitting()} busyLabel="Adding…">
    Add Category
  </SubmitButton>
</form>
```

- `form.attrs` gives the form `novalidate`, the submit, and `aria-busy` while it sends. With
  `required` kept on the control, the browser stops swallowing the submit and assistive
  technology still hears "required".
- `SubmitButton`, never `disabled={form.submitting()}`: while the form sends it reads "Saving…"
  (or the form's own verb, `busyLabel`) and is `aria-disabled`, so it keeps focus. A `disabled`
  button drops a keyboard user at the top of the page.
- The success toast goes in `send`, after the write: the save happened whatever the dialog does
  next, so it is said even when the dialog was cancelled and opened again while the save was out.
  Closing the dialog goes in `saved`, never after the `await` in `send`. The kit runs `saved` only
  while the form is still the one that sent: a dialog opened again has been reset, and a late save
  closing it throws away what the person is typing.
- The check is the entity's schema in `shared/`, the one the local-first router and the Worker
  also run, so the form and the server refuse the same values in the same words.
- An edit checks only what it changes (`checkCategoryEdit(values, opened)`), as the server does:
  a row saved under older rules has to save with its own values sent back unchanged.
- The kit marks the field (`aria-invalid`, the message under it via `aria-describedby`), moves
  focus to the first marked field, re-checks a marked field as it changes, and maps the server's
  `fields` onto the same fields. What belongs to no field goes in the `role="alert"` notice.
- No failure toast from a form. Toasts are for success, undo, and work with no form in front of
  the person; that failure goes through `plainMessage(err, fallback)`, never `err.message`.
  `frontend/src/__tests__/toastErrorMessages.test.ts` fails on a new one.
- Something a field offers besides typing into it (the Transactions form's "Create a Cash
  account" button, under the account field) says its failure there with
  `form.mark(name, plainMessage(err, fallback))`. A mark behaves like a server's: it goes on the
  field's next change, on the next submit or reset, and focus stays where the person is.
- An InfoTip beside a label goes in `Field`'s `tip`, never inside the label: inside a `<label>`
  its whole explanation becomes the control's accessible name.
- A submit button outside the `<form>` (a dialog footer) is `<SubmitButton form="<the form's id>">`.
- A list of editable rows (a loan's rate periods) is one value, a list, set whole with `form.set`.
  Each row's field is a `Field` named `<list>.<index>.<field>` (`rate_periods.0.rate`), the name
  both runtimes give it in a refusal, inside an `<Index>`. Its marks follow the row when a row
  before it is removed.

Worked examples: `frontend/src/features/categoryForm.ts`, used by the four category dialogs, with
its test `frontend/src/features/__tests__/categoryForms.test.tsx`; `accountForm.ts` (a form object
the page opens for a new or an existing row) with `accountForm.test.tsx`; and `transactionForm.ts`,
the Transactions form's values, body and check, which `Transactions.tsx` builds the form from,
with `transactionForm.test.tsx`.

## Testing this

None of these are visible in a snapshot — all five pass a test that only checks values.
Assert the behaviour instead:

```tsx
// Focus survival: the same DOM node, still focused, after several keystrokes.
const field = labelled('Monthly income from then');
field.focus();
for (const text of ['4', '45', '450', '4500']) {
  await type(labelled('Monthly income from then'), text);
  expect(document.activeElement).toBe(field); // <For> puts <body> here
}

// Step validity: the guard that actually blocks the save.
expect(field.checkValidity()).toBe(true);
expect(field.closest('form')!.checkValidity()).toBe(true);
```

Make the test helper **focus the input before typing** — these controls deliberately behave
differently while focused, so a helper that does not focus tests the wrong path.

```tsx
// A refused save: the field is marked, says why, has focus, and nothing was sent.
submitDialog();
expect(name.getAttribute('aria-invalid')).toBe('true');
expect(describedBy(name)).toContain('Give the category a name.');
expect(document.activeElement).toBe(name);
expect(await storedNames()).toEqual(['Groceries']);
```

Worked examples: `frontend/src/features/__tests__/retirementPlanner.test.tsx`, in the
`describe('the controls behave like controls')` block.

## Reviewing a diff

Nine greps that catch all of it:

```sh
grep -n '<For each' <file>            # any editable row in there? -> <Index>
grep -n 'type="number"' <file>        # -> NumberField
grep -n 'type="month"\|type="date"' <file>   # -> MonthPicker
grep -n 'Number(e.currentTarget.value)' <file>  # hand-rolled, always wrong
grep -n 'step="0.1"' <file>           # will 2dp values live here?
grep -n '<form' <file>                # -> components/form: {...form.attrs}
grep -n 'disabled={.*ubmitting' <file>  # a busy submit button -> SubmitButton, keeps focus
grep -n 'err.message\|error.message' <file>  # in a toast? -> the form kit, or plainMessage
grep -n 'InfoTip' <file>              # inside a <label>? -> Field's tip
```
