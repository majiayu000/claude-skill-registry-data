---
name: entity-store
kind: pattern
rule: entity-conventions
description: Pattern of rule entity-conventions. Load when creating or editing an admin store — the ready-made heir of the shared list store base, the mutate harness, method names from the action, an action with its own busy flag. Not for the panel — that is pattern entity-aside.
---
<!-- rt-kit v0.34.0 · patterns/entity-store.md · 2da27b552d92 · правится надстройкой, не здесь -->

# The entity store

Pattern of the rule `entity-conventions`. What must be true — the law
`docs/constitution/entity-editing.md`.

## When to use

- An `<entity>.store.ts` is created.
- The load or save method of an existing store is edited.

## The heir declares its own in four lines

```typescript
@Injectable()
export class PromoCodesStore extends BaseListStoreService<
    IPromoCodesState,
    string,
    IPromoCode.State,
    EPromoCodeSortProperty,
    EPromoCodeFilterProperty,
    IPromoCode.Draft
> {
    protected override readonly apiService: PromoCodeApiService = inject(PromoCodeApiService);
    protected override readonly listErrorKey: string = 'promoCodesLoadFailed';

    constructor() {
        super({ ...INITIAL_STATE.LIST }, { name: 'PromoCodesStore' });

        this.setConfig({ usePagination: true, useSorting: true, useFiltering: true, useSearch: true });
    }

    protected override mutationErrorKeyOf(error: unknown): string {
        return promoRejectionKey(error);
    }
}
```

The config decides what goes into the query. With everything off there is no query at all, and
the server returns the whole list. From the base come loading and re-reading, changing the page,
the order, the filter conditions and the search string, loading the next page, editing one record
in the list and resetting the query.

The file is called `<entity>.store.ts`: the name `<entity>-store.service.ts` takes it out of both
the linter rule and the rule gate.

## The save method returns a stream

```typescript
public save(draft: IPromoCode.Draft): Observable<IPromoCode.State | null> {
    return this.mutate(this.apiService.save(draft));
}
```

`mutate` holds the busy state, clearing the previous error, re-reading the list after success
and the refusal key. A mutation ends with a **re-read list**, not with a sent request: the panel
closes on the stream's value, and a list re-read after closing would show the previous value.

## Names — from the action, not from the domain

| ✗                                    | ✓          |
| ------------------------------------ | ---------- |
| `createBooking()`, `updateBooking()` | `save()`   |
| `deleteBooking()`, `removeFeed()`    | `remove()` |
| `loadBookings()`, `fetchFeeds()`     | `load()`   |

The domain name is already in the store name and in its alias.

## An action with a busy state of its own

Goes past `mutate`: calendar subscription polling keeps `pollingId`, because the panel is not
frozen for the minute of polling, and the refusal key is put by `setErrorKey`.

## Common misses

- A boolean answer from the save method: it loses both the saved record and the reason of the
  refusal — the panel learns only "it did not work".
- An own busy-and-error harness around the service call: all of that is in `mutate`.
- Own signals of records, busy state and refusal: they are in the shared base.
- A subscription to the load refusal signal: the signal is shared by the list and the panel, and
  one refusal would show twice. The load refusal goes as a separate stream.
- A second sort field: the query has one order — neither the table, nor the contract, nor the
  parsing on the server accepts a second one.
- A tail with `EMPTY` glued to a mutation: it is handled by `defaultIfEmpty`, otherwise a refusal
  of the glued stream turns a successful save into an endless spinner.
