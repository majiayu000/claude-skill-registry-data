---
name: resource-suspense
description: >
  A component that calls `createResource` must not read it. The
  declaration lives in one component body and every read of the data
  signal lives in a child, wrapped in `Suspense`. A signal filled in by
  an effect that only loads something is a resource written out
  longhand. Applies whenever adding a resource to a component, writing
  a new component that reads one, or writing an effect that loads.
---

Reading a resource that is still loading **throws**. The throw happens in the body that read it, and the boundary that catches it is the nearest `Suspense` **above** that body — so a component that both declares a resource and reads it is caught by whatever wraps the component itself, which in this app is the boundary around the whole page in [`app.tsx`](../../../src/app.tsx). A `Suspense` written inside that same body is below the throw and never sees it.

So the declaring body is kept clean of reads, and the reading body is a child that the declaring body wraps in `Suspense`. The child can suspend as much as it likes: the boundary is above it, its parent holds still, and the resource survives.

## A signal an effect only loads into is a resource

A `createSignal` and a `createEffect` whose whole purpose is to fetch something and put it in the signal is `createResource` written out longhand, and worse in every part: the loading and error states have to be kept by hand, an answer that arrives after the question changed has to be dropped by hand, and nothing tells `Suspense` anything.

```tsx
// Longhand
const [data, setData] = createSignal<Thing | null>(null);

createEffect(() => {
  let live = true;

  onCleanup(() => {
    live = false;
  });
  load(props.id).then((got) => {
    if (live) {
      setData(got);
    }
  });
});

// The same thing, with the states and the stale-answer guard included
const [data] = createResource(() => props.id, load);
```

**Gate the source on [`createClientSignal`](../../../src/components/app/client-signal.ts)** where the load is the browser's alone: a fetch of the player's own data, anything reading storage or measuring the window. A resource runs its fetcher during the server render otherwise, and holds the page up waiting for it.

```tsx
const client = createClientSignal();
const [data] = createResource(() => client() && props.id, load);
```

A source that answers `false`, `null` or `undefined` does not call the fetcher and does not suspend — the reader draws its empty state instead — so the server pass and the hydrating pass both go straight through, and the load starts on the first effect. Once the gate opens the resource suspends normally, so the reading body still belongs under a boundary.

Keep the longhand where the effect does more than load, or where the signal is not the load's alone: where the effect also writes something else, where the value is seeded by a load and then written again as the player acts, or where the same signal is set by both a load and a press.

Reading the loaded value in the declaring body is **not** a reason to keep it, and drawing a missing answer rather than waiting is not either. Both are what `answered` is for.

## Illegal — all of these read the signal in the declaring body

```tsx
const [data] = createResource(...);

const foo = createMemo(() => data());   // illegal

createEffect(() => {
  data();                               // illegal
});

const bar = () => data();

createEffect(() => {
  bar();                                // also illegal — bar reads it
});

return <h1>{data()}</h1>;               // illegal
```

A helper does not launder it. Anything the declaring body calls that reaches `data()` is a read in the declaring body. The one exception is `answered`, below, which cannot suspend and so cannot reach a boundary.

## Legal — split into two components

```tsx
function Outer(): JSX.Element {
  const [data] = createResource(() => props.player, listThings);

  return (
    <Suspense fallback={<Note>Loading…</Note>}>
      <Inner data={data} />
    </Suspense>
  );
}

function Inner(props: { data: Resource<Thing[]> }): JSX.Element {
  const shown = createMemo(() => props.data().filter(...));

  return <For each={shown()}>{(thing) => <Row thing={thing} />}</For>;
}
```

The resource is handed down as the accessor itself, not as a value — passing `data()` would be a read in the outer body.

## A refetch suspends too

`refetch()` puts the resource back into a loading state, and a read of a loading resource suspends. So a child that reads the plain accessor is swapped out for the fallback on every refetch and put back when the answer lands: the panel showing the previous answer disappears and the fallback flashes in its place, however briefly. Where the child is the game's canvas that reads as the world reloading over whatever prompted the refetch.

## The two reads, and which body they belong in

Both live in [`resource-reads.ts`](../../../src/components/app/resource-reads.ts). Which one to use is entirely about where the read is.

[`settled`](../../../src/components/app/resource-reads.ts) waits once and then holds: it suspends while the first answer is in the air, which is what the fallback is for, and leaves the last answer standing through every refetch after. It is for a **child** under a boundary, which is the shape the split above leaves.

```tsx
// Rebuilt from nothing on every refetch
const fled = (): Set<string> | undefined => props.fled();

// Waits once, then holds
const fled = (): Set<string> | undefined => settled(props.fled);
```

[`answered`](../../../src/components/app/resource-reads.ts) never waits: `undefined` until the first answer lands, the last answer through every refetch after. It is for a body that **declares its own resource**, and for anywhere the caller would rather draw its empty state than hold the screen.

```tsx
const [selling] = createResource(() => client() && props.player, listAuctionsBy);
// The declaring body, so nothing here may wait
const lots = (): Lot[] => answered(selling) ?? [];
```

## Why a body may read its own resource at all

The split exists because a read that finds a promise in the air tells the nearest `Suspense` **above the component** to put its fallback up, and that boundary is found through the owner tree — so a body reading its own resource reaches whatever wraps the body itself. The rule is about reads that can suspend, not about reads.

`answered` cannot: it asks `state` and hands back `latest` only once there is an answer, so it never reaches the read and can never reach a boundary. A body may declare a resource and read it that way. Everything else in the split stands.

**`resource.latest` on its own is not that exemption.** Until the resource has resolved once, `latest` *is* the ordinary read — Solid's own getter falls straight through to it — so a body reading its own resource that way suspends on the first load and only stops afterwards. It is the trap that looks like the fix, and the first load is exactly when it matters.

## Around it

- `refetch` belongs to the outer body, and is handed down like the accessor when the child is what acts.
- [`TabPane`](../../../src/components/styled/tabs.tsx) carries a boundary, so a panel it renders is already a child of one.
- The house [`Dialog`](../../../src/components/styled/dialog.tsx) carries a boundary around its panel, with no fallback, so a read inside a panel holds the panel rather than the page. A headless dialog carries none: portalled markup keeps its owner, so a read inside one reaches whatever boundary is above the component and closes the dialog on the way out.

## Which side of the boundary a computation goes

The split is not only about reads. Two kinds of computation have a side of their own.

**Derived signals go outside.** A memo or an accessor over props, plain signals or anything else that cannot suspend belongs in the declaring body, above the boundary, and is handed down. Kept inside, it is recomputed under a subtree that stops while the data is in the air, and the parent cannot read it at all.

```tsx
function Outer(props: { player: string }): JSX.Element {
  const [search, setSearch] = createSignal('');
  const [data] = createResource(() => props.player, listThings);
  // Derived from a signal, not from the resource: it stays here
  const wanted = createMemo(() => search().trim().toLowerCase());

  return (
    <>
      <SearchBox value={search()} onChange={setSearch} />
      <Suspense>
        <Inner data={data} wanted={wanted} />
      </Suspense>
    </>
  );
}
```

**Effects that read go inside.** A `createEffect` reading the resource — or reading anything that reaches it — belongs in the child, under the boundary. In the declaring body it throws past every boundary in the component and takes the page down with it, and it runs while the data is still coming.

```tsx
function Inner(props: { data: Resource<Thing[]>; wanted: () => string }): JSX.Element {
  // Under the boundary: it may suspend, and it runs when there is
  // something to run on
  createEffect(() => {
    report(props.data().length, props.wanted());
  });

  return <For each={props.data()}>{(thing) => <Row thing={thing} />}</For>;
}
```

An effect that writes a signal the outer body owns still lives inside; it is handed the setter.
