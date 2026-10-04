---
name: grid-cards
description: A square in a grid says what it is in a tooltip, and gets a hover card only where it offers more than one thing to do. Applies whenever adding a square to an item or candy tray, or giving one of those squares something to press.
---

**One action is a tooltip. Two is a hover card.**

A square in a tray is a picture. What it is has to be readable without
pressing anything, and a hover card is a window that covers the tray being read
from, so a square says its name and its line in a `TooltipHost`.

A card earns its place only when the square offers a **choice**. One thing to do
is the square's own press and needs no buttons; two have to be pressed
separately, and a tooltip cannot hold a button because it goes the moment the
pointer leaves the trigger.

## How a tray says which it wants

`ItemGrid` counts, so a caller never picks. An `ItemCell` lists what it offers in
`actions`:

```ts
{
  item: auction.item,
  actions: [
    { label: describeSeller(auction), onPress: () => game.setVisiting(auction.seller) },
    { label: 'Bid', tone: 'primary', onPress: () => setBidding(id) },
  ],
}
```

- **No actions**: a tooltip, and the tray's own `onPress` runs the square.
- **One action**: a tooltip, and pressing the square does that action.
- **Two or more**: a hover card, with the actions drawn as buttons in its foot.

A cell that lists `actions` has said what its square does, so the tray's
`onPress` and `cardOnly` no longer reach it.

## What this means for the card body

Anything pressable inside a card body is an action and has to be counted, or it
becomes unreachable the day the square drops to one action and turns into a
tooltip. The auction board's seller name used to be an inline link in the card;
it is an action now, which is what keeps that card a card.

## Where it does not apply

The pokemon box is not covered. A catch square carries a record rather than a
name, and its card is the record.
