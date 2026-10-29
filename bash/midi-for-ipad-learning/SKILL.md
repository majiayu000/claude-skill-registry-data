---
name: midi-for-ipad-learning
description: >
  Find a piano MIDI for a song, transpose it to white keys only (C major / A minor),
  split it into its repeated parts (riff, verse, chorus loops) as separate MIDI files,
  and save them in an iCloud Drive folder named `<song>-midi` for piano learning on iPad
  with midee.app. Use when the user asks for piano MIDI files of a song, white-keys or
  C major versions, song parts to learn one by one, or MIDI for midee.
---

# midi-for-ipad-learning

Goal: for each song, the full MIDI plus one MIDI per **unique part**, white keys only, in iCloud Drive. The user loads them on iPad in **midee.app** (https://midee.app). midee splits hands itself, so keep both hands in every file.

```
~/Library/Mobile Documents/com~apple~CloudDocs/golden-brown-midi/
  golden-brown-00-full.mid
  golden-brown-01-riff-bars-1-6.mid        # riff with all its repeats, as in the song
  golden-brown-04-verse-bars-13-20.mid
  ...
```

`<song>` is kebab-case. The `-midi` folder suffix lets the user find the folders.

## 1. find a piano MIDI on MuseScore

MuseScore has the most **piano solo** arrangements. curl gets 403 (Cloudflare), so use playwriter (load the `playwriter` skill first). `scripts/musescore.mjs` searches and downloads the MIDI without login.

```bash
playwriter session new   # then use its id with -s
playwriter -s <id> --timeout 120000 -e '
const m = await import("/Users/morse/.config/opencode/skills/midi-for-ipad-learning/scripts/musescore.mjs")
state.page ??= await context.newPage()
const r = await m.searchMusescore({ page: state.page, query: "golden brown stranglers piano solo" })
console.log(r.slice(0, 10).map(x => (x.official ? "[OFFICIAL] " : "") + x.url + " | " + x.title).join("\n"))'
```

Pick a result:

- skip `[OFFICIAL]` scores (paid) and duets, vocal or other instrument versions
- prefer titles with "piano", "piano solo"; "easy" when the user is a beginner
- for ambiguous names, pick the version that fits the other songs (e.g. "Love Story" = Indila)

```bash
playwriter -s <id> --timeout 120000 -e '
const m = await import("/Users/morse/.config/opencode/skills/midi-for-ipad-learning/scripts/musescore.mjs")
await m.downloadMusescoreMidi({ page: state.page, url: "https://musescore.com/user/34400169/scores/7209879", outputPath: "/tmp/midi/golden-brown.mid" })'
```

Fallback: https://freemidi.org (band arrangements, not piano). Page `/download3-<id>-<slug>`, file `/getter-<id>` with the page as referer and a cookie jar. bitmidi.com is often down. GitHub code search does not index `.mid` files.

## 2. transpose to white keys

```bash
uv run /Users/morse/.config/opencode/skills/midi-for-ipad-learning/scripts/white-keys.py /tmp/midi/golden-brown.mid --out /tmp/midi/w/golden-brown.mid
```

It tries every shift from -6 to +5 semitones and keeps the one with most notes on white keys (C major or A minor). Leftover black keys move one semitone down (G# to G); it prints how many. `--no-snap` keeps them. Tracks, tempo, time signatures and pedal stay as they are.

## 3. find the parts

No CLI finds repeated sections in symbolic MIDI (pychorus, allin1 work on audio only), so `scripts/parts.py` prints the song as text and you choose the parts.

```bash
P=/Users/morse/.config/opencode/skills/midi-for-ipad-learning/scripts/parts.py
uv run $P show w/golden-brown.mid --no-notes             # bar letters + repeated runs
uv run $P show w/golden-brown.mid --no-notes --phrase 4  # also 4-bar phrases (try 8 for slow songs)
uv run $P show w/golden-brown.mid --from 9 --to 20       # notes of some bars
```

```
labels: A B A B A B A C D D D D E F E~ F~ G G G~ H ...
runs (unit x repeats, bars that do not repeat are grouped):
  bars   1-6   0:00.0  (A B) x3
  bars   9-12  0:17.3  (D) x4
    9 D   6/8 0:17.3 | 1:D2 1.5:A3.D4.F4 2.5:F2 3:A3.D4.F4 3.5:A2 4:G2 5:E2.C4.E4.G4
```

- bars come from the MIDI time signatures (6/8 and 7/8 changes work)
- same letter = same bar; `~` = small variation (up to 2 notes differ), treat it as the same bar
- `(A B) x3` = a loop repeated 3 times (bars 1-6)
- phrases: `P2 (~P1)` means only 1 bar differs from P1; usually skip it

Choose parts:

1. one part per section: loop, verse, chorus, bridge, outro
2. a loop keeps its repeats, like in the song: cut its longest run. `(A B) x3` at bars 1-6 and `(A B) x2` at 47-50 gives one part with bars 1-6
3. skip sections that repeat an earlier part, also with small variations
4. name parts by role when clear (`riff`, `verse`, `chorus`, `bridge`, `outro`), else `part`

## 4. cut and save to iCloud

```bash
D=~/Library/Mobile\ Documents/com~apple~CloudDocs/golden-brown-midi
mkdir -p "$D" && cp w/golden-brown.mid "$D/golden-brown-00-full.mid"
uv run $P cut w/golden-brown.mid --out "$D" --name golden-brown \
  --part riff:1-6 --part verse:13-20 --part chorus:37-42 --part outro:51-66
```

Files are `<song>-NN-<part>-bars-<from>-<to>.mid`. Each keeps tempo, time signature, key and pedal at its start. `cut` skips a part whose bar letters equal an earlier part and prints `skip ...`.

## 5. report

Per song: MuseScore source URL, semitone shift, snapped notes, and the parts list with bars. Remind the user to open the files in **midee.app** on iPad from the Files app (iCloud Drive).
