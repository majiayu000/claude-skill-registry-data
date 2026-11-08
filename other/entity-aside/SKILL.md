---
name: entity-aside
kind: pattern
rule: entity-conventions
description: Pattern of rule entity-conventions. Load when assembling or editing the record create-and-edit panel — the ready-made route in the ro outlet, inheriting the shared base, runMutation, the unsaved edits guard, header and footer, leaving for a linked record. Not for the store — pattern entity-store.
---
<!-- rt-kit v0.34.0 · patterns/entity-aside.md · 05314ce277ff · правится надстройкой, не здесь -->

# The record edit panel

Pattern of the rule `entity-conventions`. What must be true — the law
`docs/constitution/entity-editing.md`.

## When to use

- A panel that creates and edits a record is created or edited.
- A panel without a record appears — table settings, an event feed.

## The panel is declared by a route in the `ro` outlet

```typescript
{
    path: 'booking/:id',
    outlet: 'ro',
    component: BookingDetailAsideComponent,
}
```

This way the panel survives a reload, is passed by link and lands in the browser history. There
is no programmatic opening through a service in the admin.

**The opening command goes from the current route, not from the root.** The outlet is declared
inside the domain's routes, so the screen calls the opening relative to itself:

```typescript
void this.#router.navigate([{ outlets: { ro: [EDIT_PATH, id] } }], { relativeTo: this.#route });
```

Without the current route the command goes to the application root: the panel does not open,
there is no exception, the browser output is clean — the miss is seen only by eye and only by
whoever opened this screen. Its second half is quieter: the panel base closes it against the
parent of the current route, and a panel opened from the root does not close at all.

A panel opened from the header is declared as a constant and mixed into the `children` of every
domain branch — the outlet stands in the chrome template, and the chrome is put on by the
`shell` of every domain:

```typescript
export const ACTIVITY_ASIDE_ROUTES: Route[] = [{ path: 'activity', outlet: 'ro', component: ActivityFeedAsideComponent }];
```

## The screen inherits the shared base

`RtRouteAsideComponent<T>` holds `entity`, `entityId`, `isCreateMode`, `submitting`,
`resolving`, `submitError`, opening the panel by route, leaving the address and the whole
mechanics of saving. Names from the base are not renamed: `booking`, `feed`, `slug` instead of
`entity` break the very uniformity the base was set up for.

## Saving goes through `runMutation`

```typescript
protected save(): void {
    if (!this.canSave()) {
        return;
    }

    this.runMutation(this.#store.save(this.#draft()), {
        successKey: 'promoCodeSaved',
        errorText: (): string => this.#store.errorKey() ?? 'promoCodeSaveFailed',
        closeOnSuccess: true,
    });
}
```

The busy state, clearing the previous error, the success toast and closing the panel are held by
the base. `errorText` is a function: the reason of the refusal is known only after it. The
mutation stream must give a value or an error — an empty stream freezes the panel forever.

## The unsaved-edits guard

Set by the panel itself, and it stands on all four closing paths: the button in the header, the
button in the footer, a press outside the panel and Esc.

```typescript
protected readonly panelForm: Signal<NgForm | undefined> = viewChild(NgForm);
protected readonly formPristine: Signal<boolean> = this.pristineSignal(
    computed((): AbstractControl | undefined => this.panelForm()?.control)
);

constructor() {
    super();
    this.guardUnsavedChanges({ pristine: this.formPristine, save: (): void => this.save() });
}
```

Angular does not accept `viewChild` on a `#` field — the field is declared `protected`.

## Header and footer

```html
<<prefix>-aside-header [title]="title()" [overline]="overline()" [loading]="resolving()" (dismiss)="onClose()">
    <ng-container asideActions>
        <!-- domain actions as icons; more than two — under one menu button -->
    </ng-container>
</<prefix>-aside-header>
```

The title names the action, the record name goes as the overline. The footer has two zones and no
more than two buttons: `asideDismiss` — closing, `asidePrimary` — saving. Domain verbs do not go
into the footer: confirming, rejecting, unpublishing — icons in the header.

The button captions are fixed, the panel does not choose them:

| Button                             | Caption                                           |
| ---------------------------------- | ------------------------------------------------- |
| saving on create                   | «Создать»                                         |
| saving on edit                     | «Сохранить»                                       |
| closing a panel that saves         | «Закрыть и не сохранять» (`uiCloseWithoutSaving`) |
| closing a view-only panel          | «Закрыть»                                         |

The save button stands at the edge opposite the close button, and while the request runs it
shows a spinner and cannot be pressed: the busy state comes from the base's `submitting()`, the
panel keeps no flag of its own. The header and the footer stay in place on scroll — only the
content zone scrolls.

## Leaving for a related record

```html
<a rtElem="related" qa-dataid="promo-code-property-link" [href]="propertyHref()" (click)="openProperty($event)">
    {{ 'propertyOpenLink' | transloco }} <<prefix>-icon name="arrow-right" size="sm" />
</a>
```

The address is given by `relatedUrl(commands)`, the leaving — by `openRelated(commands)`.
`routerLink` is no good here: the directive navigates itself, `preventDefault` does not stop it,
and it bypasses the question about unsaved edits.

## Common misses

- An own `router.navigate` in the panel: absolute commands change only the primary branch, the
  outlet stays in the address, and the router rejects the navigation silently.
- Skeletons by `busy()`, not by `resolving()`: `busy` includes saving too, and on save the fields
  would turn into skeletons.
- An own "not found" on the panel: a record that is not found leaves the address by the base's
  own means.
- Own spacing on top of the shared base: it gives different field widths on different panels and
  cuts off the focus outline at the edge of the scroll area.
- A panel that stays open after success did not reset pristineness (`markAsPristine`) — the
  question about edits is asked right after saving.
- Disabled inputs instead of data: a record that is only viewed is shown by the kit's ready-made
  property list — `<prefix>-detail-list`, `<prefix>-info-item`. Own markup on `<dl>` goes last
  and only as a one-off deviation: it is the departure from the shared look, and the owner
  decides it — a list that puts it first teaches to bypass the ready-made before asking.

## A footer button that must not exist in some state

A section of this tree. Buttons reach the footer zones by projection over an attribute, and a
conditional block around such a button loses it: a node inside `@if` does not reach the slot at
all, and one neighbouring button is left in the footer. Neither the build nor the linter judges a
conditional block — this is visible only on the assembled screen, and it was found by an
end-to-end run, not by the component spec.

So the button is not hidden but disabled:

```html
<button rt-button asidePrimary qa-dataid="invite-create-submit" type="button" [label]="submitLabel" [disabled]="issued() !== null" (click)="submit()"></button>
```

A disabled button stays an answer to the question «what can be done here»: gone after a successful
write, it reads as broken markup.

## A record that is only looked at

A section of this tree. The details panel edits nothing: it shows the record properties by a
ready-made piece from the kit, not by markup of its own. A hand-written definition list does not
happen here — `<dl>` knows neither about field widths nor about reading skeletons, and it is fixed
in every panel separately.

The panel is assembled from three kit pieces: the section `rt-aside-section` with its own heading,
the property list `rt-detail-list` and the row `rt-detail-row` — a name, a value by projection and
a skeleton for the time of the read.

```html
<rt-aside-section>
    <rt-detail-list>
        <rt-detail-row qa-dataid="postmortem-tree" [label]="treeLabel" [loading]="reading()">
            {{ entity()?.tree?.name }}
        </rt-detail-row>
    </rt-detail-list>
</rt-aside-section>

@if (!reading() && entity(); as record) {
    <rt-aside-section [heading]="textLabel">
        <pre rtElem="text" qa-dataid="postmortem-text">{{ record.text }}</pre>
    </rt-aside-section>
}
```

The reading sign comes to the aside as an input and goes into every row: the skeleton is drawn by
the kit row, and `rt-skeleton-wrapper` is not wrapped by hand. The record input accepts emptiness
too — while the read goes on there is no record yet at all, and the property names already stand
in place.

The section showing the record content hides whole for the time of the read: the former content
belongs to the former record, and the words «the record does not have this» are read by a person
as an answer that has not been given yet.

The panel has three levels of signs, each its own: the panel itself and its header carry section
marks (`<section>-details-panel`, `<section>-details-header`), a property row carries the property
mark, and the name and the value inside it are marked up by the kit (`detail-row-label`,
`detail-row-value`). The kit mark `aside-header` is one for every drawer of the application, and a
spec that needs the header of this very panel cannot hook onto it.
