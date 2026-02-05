---
name: big_text
description: Create ASCII art banners using figlet. Use this when the user asks for big text, banners, or ASCII art.
---

# Big Text Skill

This skill allows you to generate large ASCII text banners using the `figlet` command.

## Basic Usage

To create a basic banner using the standard font:

```bash
figlet "Hello World"
```

## Specifying Fonts

You can change the style of the text by using the `-f` flag followed by the font name.

```bash
figlet -f slant "Hello"
```

## Formatting Options

- **Centering**: Use `-c` to center the output.
- **Right justify**: Use `-r` to right justify.
- **Left justify**: Use `-l` (defaut).
- **Width**: Use `-w <columns>` to specify the output width (default is 80).

Example:
```bash
figlet -c -w 100 -f big "Centered Header"
```

## Font Showcase

Below is a comprehensive list of available fonts categorized by style. Use these names with the `-f` flag.

### Standard & Clean
- **standard**: The default font. Readable and classic.
- **big**: Larger version of standard.
- **slant**: Slanted/italic style. Very popular.
- **smslant**: Small slanted. Good for tighter spaces.
- **small**: Smaller, more compact characters.
- **mini**: Tiny text, good for footnotes.
- **banner**: Very large, wide characters (often rotates text to vertical on some systems, but effectively `banner3` or similar is usually horizontal).
- **digital**: Resembles a digital clock display.
- **term**: Terminal style block text.

### 3D & Shadows
- **shadow**: Text with a drop shadow effect.
- **smshadow**: Small text with shadow.
- **big**: (Often has a 3D feel).
- **larry3d**: 3D block letters.
- **block**: Heavy block letters with 3D effect.
- **3-d**: Wireframe 3D style.

### Script & Cursive
- **script**: Connected cursive handwriting.
- **smscript**: Small script.
- **slscript**: Slanted script.
- **cursive**: Another cursive variant.

### Novelty & Artistic
- **bubble**: Bubble letters.
- **lean**: Lean, tall letters.
- **keyboard**: Keys look like keyboard keys.
- **fender**: Fender guitar logo style.
- **graffiti**: Graffiti style (if available).
- **doom**: Style reminiscent of the Doom game logo.
- **starwars**: Star Wars logo style.
- **weird**: Artistic and strange shapes.
- **alligator**: Jagged, rough edges.
- **dotmatrix**: Dot matrix printer style.

### Symbols & Abstract
- **morse**: Morse code output.
- **binary**: Binary representation.
- **hex**: Hexadecimal representation.

## All Available Fonts
If you need a specific font not listed above, you can verify its existence by running:
```bash
ls $(figlet -I 2)
```

Common fonts found on many systems:
`3-d`, `3x5`, `5lineoblique`, `acrobatic`, `alligator`, `alligator2`, `alphabet`, `avatar`, `banner`, `banner3`, `banner3-D`, `banner4`, `barbwire`, `basic`, `bell`, `big`, `bigchief`, `binary`, `block`, `bubble`, `bulbhead`, `calgphy2`, `caligraphy`, `catwalk`, `chunky`, `coinstak`, `colossal`, `computer`, `contessa`, `contrast`, `cosmic`, `cosmike`, `cricket`, `cursive`, `cyberlarge`, `cybermedium`, `cybersmall`, `diamond`, `digital`, `doh`, `doom`, `dotmatrix`, `double`, `drpepper`, `eftichess`, `eftifont`, `eftipiti`, `eftirobot`, `eftitalic`, `eftiwall`, `eftiwater`, `epic`, `fender`, `fourtops`, `fraktur`, `fuzzy`, `goofy`, `gothic`, `graceful`, `gradient`, `graffiti`, `greek`, `heart_left`, `heart_right`, `hex`, `hollywood`, `invita`, `isometric1`, `isometric2`, `isometric3`, `isometric4`, `italic`, `ivrit`, `jazmine`, `jerusalem`, `katakana`, `kban`, `keyboard`, `knob`, `larry3d`, `lcd`, `lean`, `letters`, `linux`, `lockergnome`, `madrid`, `marquee`, `maxfour`, `mike`, `mini`, `mirror`, `mnemonic`, `morse`, `moscow`, `nancyj`, `nancyj-fancy`, `nancyj-underlined`, `nipples`, `ntgreek`, `o8`, `ogre`, `pawp`, `peaks`, `pebbles`, `pepper`, `poison`, `puffy`, `pyramid`, `rectangles`, `relief`, `relief2`, `rev`, `roman`, `rot13`, `rounded`, `rowancap`, `rozzo`, `runic`, `runyc`, `sblood`, `script`, `serifcap`, `shadow`, `short`, `slant`, `slide`, `slscript`, `small`, `smisome1`, `smkeyboard`, `smscript`, `smshadow`, `smslant`, `speed`, `stacey`, `stampatello`, `standard`, `starwars`, `stellar`, `stop`, `straight`, `tanja`, `tengwar`, `term`, `thick`, `thin`, `threepoint`, `ticks`, `ticksslant`, `tinker-toy`, `tombstone`, `trek`, `tsalagi`, `twopoint`, `univers`, `usaflag`, `wavy`, `weird`, `whimsy`, `wow`.

## Examples of Specific Styles

### Banner 3D
```bash
figlet -f banner3-D "3D TEXT"
```

### Cyber Large
```bash
figlet -f cyberlarge "CYBER"
```

### Doom
```bash
figlet -f doom "DOOM"
```

### Epic
```bash
figlet -f epic "EPIC"
```

### Speed
```bash
figlet -f speed "FAST"
```
