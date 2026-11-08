---
name: entity-models-new
kind: pattern
rule: entity-models
description: Pattern of rule entity-models. Load when declaring a new entity model and its mapper — the ready-made I<Entity> namespace with Api, State and Draft, short and full levels, a BaseMapper heir with typeCast, what to do after editing .proto.
---
<!-- rt-kit v0.34.0 · patterns/entity-models-new.md · 0fa05e84bb7c · правится надстройкой, не здесь -->

# Declaring an entity model and its translation

Pattern of the rule `entity-models`. What must be true — the law
`docs/constitution/entity-models.md`.

## When to use

- A new admin entity is created.
- An existing one gets a short level.
- The mapper or the contract of this entity is edited.

## The model — a namespace in the domain's `util`

The file `libs/<family>/<domain>/util/src/lib/models/<entity>.model.ts`:

```typescript
export namespace IPromoCode {
    export namespace Short {
        export type Api = PromoCodeListItem;

        export interface State {
            readonly id: string;
            readonly code: string;
        }
    }

    export type Api = PromoCodeInfo;

    export interface State extends Short.State {
        readonly usageCount: number;
        /** Empty = the code applies to any property of the owner */
        readonly propertyId: string;
        /** 0 = no limit */
        readonly usageLimit: number;
    }

    /** What goes to the server on save: an empty id — the code is new */
    export interface Draft {
        readonly id: string;
        readonly code: string;
    }
}

export enum EPromoDiscountKind {
    Percent = 'percent',
    Amount = 'amount',
}
```

The domain's enums lie in the same file, but **outside** the namespace. No deeper than two levels
of nesting: `IPromoCode.Short.State` reads, a third level no longer does.

The query aliases are declared in the same place:

```typescript
export type Query = IList.Query.State<EPromoCodeSortProperty, EPromoCodeFilterProperty>;
export type ListResult = IList.Result.State<IPromoCode.State, EPromoCodeSortProperty, EPromoCodeFilterProperty>;
```

## The mapper — in the domain's `api`, one per level

The file `libs/<family>/<domain>/api/src/lib/mappers/<entity>-model.mapper.ts`:

```typescript
export class PromoCodeModelMapper extends BaseMapper<IPromoCode.State> {
    public override mapFrom(raw: IPromoCode.Api): IPromoCode.State {
        return {
            id: this.typeCast.getAsString(raw?.id),
            code: this.typeCast.getAsString(raw?.code),
            usageCount: this.typeCast.getAsNumber(raw?.usageCount),
            usageLimit: this.typeCast.getAsNumber(raw?.usageLimit),
        };
    }
}
```

The mapper has no state and no DI:

```typescript
readonly #mapper: PromoCodeModelMapper = new PromoCodeModelMapper();
```

One class per level: `PromoCodeShortModelMapper` and `PromoCodeModelMapper`.

## A string field with a finite set is checked explicitly

`getAsType` accepts no default: a value outside the set it writes to the console and returns as
the string `'unknown'`.

```typescript
kind: promoDiscountKindOf(raw?.kind) ?? EPromoDiscountKind.Percent,
```

## After editing the contract

```bash
cd libs/common/proto && npx buf lint
npm run proto:generate
```

Neither `buf lint` nor `buf breaking` is part of `check:all` or CI — they are run by hand. The
generated types lie in the repository, and without regeneration the divergence surfaces in the
build of another application.

A removed field is marked `reserved` with its number and name.

## Common misses

- `Api` rewritten by hand instead of an alias — diverges from the contract silently.
- `??` instead of `typeCast` — the contract returns default values, and a check for `undefined`
  catches nothing.
- `as Type` in a mapper — forbidden by rule `typescript-conventions`.
- `null` or `undefined` in `State` — empty is expressed by an empty string or zero, and the
  meaning of zero is explained by a comment next to the field.
- A `readonly` array handed to a request: the message's init type demands a mutable one, the
  model hands out a copy.
- A shared type for the admin and the site — the guest has its own short shape of the record.
