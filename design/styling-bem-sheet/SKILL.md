---
name: styling-bem-sheet
kind: pattern
rule: styling-bem
description: Pattern of rule styling-bem. Load when creating or editing a sheet, a dialog or a full-screen view over the page — what opens it, what is passed inside, how it slides in from below, what checks it. Not for the record edit panel in the admin — that is pattern entity-aside.
---
<!-- rt-kit v0.34.0 · patterns/styling-bem-sheet.md · 9749533b17f6 · правится надстройкой, не здесь -->

# The sheet and the window above the page

Pattern of the rule `styling-bem`. What must be true — the law
`docs/constitution/frontend-application.md`.

## When to use

- A sheet is created for the phone: choosing a language, a currency, dates.
- A window or a full-screen view above the page is created.
- Something covers the sheet or the window, and raising their `z-index` looks tempting.

The record edit panel in the admin is a different thing: there it is a route in its own outlet,
pattern `entity-aside`.

## A service opens it, not markup next to the button

The sheet component is an ordinary markup element. It is drawn where it is written, so its
`z-index` compares only with the neighbours of that place. A sticky header blurs the background
under itself — and everything written inside the header is locked in its layer.

The sheet is opened by the kit's window service — the same call opens a full-screen view. The
markup moves to `<body>`, and there is nothing left to compare it with.

```typescript
readonly #dialog: RtDialogService = inject(RtDialogService);

readonly #sheetOpenedSource: Subject<RtDialogRef<string>> = new Subject<RtDialogRef<string>>();
#sheetRef: RtDialogRef<string> | null = null;

protected openLocalePicker(): void {
    if (this.#sheetRef) {
        return;
    }

    const data: ILocalePickerData = { locales: this.locales, value: this.currentLocale };
    const ref: RtDialogRef<string> = this.#dialog.open<LocalePickerComponent, ILocalePickerData, string>(
        LocalePickerComponent,
        { data, panelClass: 'locale-picker-panel', backdropClass: 'locale-picker-backdrop' }
    );
    this.#sheetRef = ref;
    this.#sheetOpenedSource.next(ref);
}
```

The sheet's answer is awaited by a subscription from the constructor — subscribing in a method
is forbidden by `angular-patterns`:

```typescript
this.#sheetOpenedSource
    .pipe(
        mergeMap((ref: RtDialogRef<string>): Observable<string | undefined> => ref.afterClosed()),
        takeUntilDestroyed(this.#destroyRef)
    )
    .subscribe((code: string | undefined): void => {
        this.#sheetRef = null;
        if (code) {
            this.onLocaleChange(code);
        }
    });
```

The reference is cleared here, not in the button handler: the sheet is also closed by a swipe
down and by a tap outside, and both paths bypass the button.

## Inside the sheet — only the sheet itself

What to show arrives by a token. What was chosen leaves together with the close. The sheet has
no button of its own: the button is held by whoever opens the sheet.

```typescript
export interface ILocalePickerData {
    readonly locales: readonly ISiteLocale[];
    readonly value: string;
}

readonly #data: ILocalePickerData = inject<ILocalePickerData>(RT_DIALOG_DATA);
readonly #dialogRef: RtDialogRef<string> = inject<RtDialogRef<string>>(RtDialogRef);

protected confirm(): void {
    this.#dialogRef.close(this.centeredLocale());
}

/** Closed without confirming: they changed their mind — the value is left as is */
protected onOpenChange(open: boolean): void {
    this.open.set(open);
    if (!open) {
        this.#dialogRef.close();
    }
}
```

## The sheet slides in from below

The service raises it already open, and the kit has nothing to animate: instead of movement the
guest sees the screen swapped. So it is opened one frame later:

```typescript
protected readonly open: WritableSignal<boolean> = signal<boolean>(false);

constructor() {
    afterNextRender((): void => {
        this.open.set(true);
    });
}
```

`afterNextRender`, not `ngAfterViewInit`: the page is served by the server, and the markup
appears later.

## The backdrop

The sheet dims the background itself and catches the tap outside itself. The window's backdrop
above it would give a second dimming — the background would be twice as dark as next to a
neighbouring sheet. So it is made transparent. The rule is written into the application's shared
layer: the sheet has moved to `<body>`, and the component's styles file does not reach it.

```scss
/* the application's shared layer; the class name carries the tree's prefix */
.locale-picker-backdrop {
    background: transparent;
}
```

It still catches the tap — closing on it is done by the window itself.

## What checks it

A screenshot does not help here: a covered sheet looks whole, and the build and the lint are
silent. The point is asked — who gets the tap:

```javascript
const rect = button.getBoundingClientRect();
document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
```

The answer must be the button itself. Measure on the stand from the production build and on a
narrow screen — pattern `browser-verification-measure`.

In an end-to-end test, before the measurement, wait until the sheet has arrived: a visible button
may still be moving, and a frame later the coordinates will differ.

```typescript
await page.locator('[qa-dataid="locale-picker-sheet"] [qa-dataid="bottom-sheet-panel"]').evaluate(
    (panel: Element): Promise<void> =>
        new Promise<void>((resolve: () => void): void => {
            if (panel.getBoundingClientRect().bottom <= window.innerHeight) {
                resolve();

                return;
            }
            panel.addEventListener('transitionend', (): void => resolve(), { once: true });
        })
);
```

## Common misses

- **The sheet is written next to its button in the header.** The header blurs the background,
  and the sheet is locked in its layer. That is how the bottom bar covered the sheet together
  with the confirm button, and the value could no longer be changed on the phone.
- **The header got a higher layer number.** The defect goes away, the sheet stays locked in a
  foreign layer: the next neighbour with a higher number covers it again.
- **The sheet was moved to another place in the markup.** The same thing: it works until someone
  puts a `transform`, a `filter` or a `z-index` of their own above the new place.
- **The backdrop rule was put into the component's styles.** The backdrop has moved to `<body>`,
  and the rule does not reach it — it has to be written into the application's shared layer.
- **The reference to the open sheet was cleared in the button handler.** Closing by a swipe and
  by a tap outside bypasses it, and the sheet does not open a second time.
- **The test measured right after the visibility check.** The sheet is still moving,
  `elementFromPoint` returns `null`, and the test goes red on working code.
- **The sample was searched by the names of the library the kit is built on.** It lies inside
  the kit, its names are not in the tree — search by the kit's names.
