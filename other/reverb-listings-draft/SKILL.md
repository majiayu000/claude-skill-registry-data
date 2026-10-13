---
name: reverb-listings-draft
description: "Reverb: Create a listing in draft state."
metadata:
  version: 0.1.0-alpha.2
  openclaw:
    category: "productivity"
    requires:
      bins:
        - revcli
      skills:
        - reverb-listings
    cliHelp: "revcli listings +draft --help"
---

# listings +draft

> **PREREQUISITE:** Read `../reverb-listings/SKILL.md` for auth, global flags, and available methods.

Create a new listing in draft state with guided flags.

## Usage

```bash
revcli listings +draft --make <MAKE> --model <MODEL> --price <PRICE> --condition <CONDITION>
```

## Flags

| Flag          | Required | Default | Description                            |
|---------------|----------|---------|----------------------------------------|
| `--make`      | ✓        | —       | Instrument make (e.g. `Fender`)        |
| `--model`     | ✓        | —       | Instrument model (e.g. `Stratocaster`) |
| `--price`     | ✓        | —       | Listing price in USD (e.g. `999.00`)   |
| `--condition` | ✓        | —       | Item condition (see values below)      |

### Condition Values

| Value             | Description                       |
|-------------------|-----------------------------------|
| `mint`            | Brand new, never played           |
| `excellent`       | Barely played, like new           |
| `very-good`       | Light play wear                   |
| `good`            | Some play wear and cosmetic marks |
| `fair`            | Heavy wear, fully functional      |
| `poor`            | Significant damage or heavy wear  |
| `non-functioning` | For parts only                    |

## Examples

```bash
revcli listings +draft --make Fender --model Stratocaster --price 999.00 --condition excellent
revcli listings +draft --make Gibson --model 'Les Paul Standard' --price 2499.00 --condition very-good
revcli listings +draft --make Martin --model 'D-28' --price 1799.00 --condition mint
```

## Tips

- Draft listings are not publicly visible until published.
- To publish after creating: `revcli listings update --params '{"id":"<ID>"}' --json '{"state":"live"}'`
- To review all your listings: `revcli listings list --format table`

> [!CAUTION]
> This is a **write** command — confirm with the user before executing.

## See Also

- [reverb-listings](../reverb-listings/SKILL.md) — All listings methods and global flags
