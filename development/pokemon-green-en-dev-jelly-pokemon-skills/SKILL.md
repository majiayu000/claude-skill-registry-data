---
name: pokemon-green-en
description: "Pokemon Green Version Text RPG. Gen 1 with 151 Pokemon, 165 moves, full Kanto region. English only. Activated when users mention 'pokemon', 'pikachu', 'battle', 'gym', 'wild', 'pokedex', 'new game', 'continue'. (project)"
trigger-keywords: pokemon, pikachu, gym, battle, wild, pokedex, new game, continue, pokemon green
allowed-tools: Read, Write, Edit, Bash
---

# Pokemon Green Version - Text RPG (English)

A Claude skill that fully recreates Gen 1 Pokemon Green Version as a text-based RPG. (English only)

## When to Invoke

This skill is automatically activated when:

- User mentions "pokemon", "pikachu"
- "new game", "continue", "start game" requests
- "battle", "gym", "wild", "pokedex" related conversation

## Game Features

- **151 Pokemon**: From Bulbasaur to Mew
- **165 Moves**: All Gen 1 moves implemented
- **15 Type Chart**: Including Gen 1 specific bugs
- **Kanto Region**: From Pallet Town to Pokemon League
- **8 Gyms**: Brock, Misty, Lt. Surge, Erika, Koga, Sabrina, Blaine, Giovanni
- **Save/Load**: 10 slots + autosave
- **BGM Autoplay**: 45 tracks (macOS afplay)
- **ASCII Art**: 151 Pokemon sprites
- **Cries**: 151 Pokemon cries

---

## Starting the Game

### Initialization
```bash
pkill -f 'pokemon-green.*bgm' 2>/dev/null
```

### BGM Rules

File path: `data/audio/bgm/[filename].mp3`

#### Main BGM Files
| Situation | Filename |
|-----------|----------|
| Opening | opening.mp3 |
| Pallet Town | pallet_town.mp3 |
| Oak's Lab | oak_lab.mp3 |
| Route | route_theme.mp3 |
| Wild Battle | wild_battle.mp3 |
| Trainer Battle | trainer_battle.mp3 |
| Pokemon Center | pokemon_center.mp3 |

#### Playback Commands
```bash
# Stop BGM
pkill -f 'afplay.*pokemon-green' 2>/dev/null

# Play BGM (background loop, required!)
while true; do afplay [skillPath]/data/audio/bgm/[filename].mp3 2>/dev/null || break; done
run_in_background: true
```

#### Error Handling
- `|| break`: Prevents infinite loop if file missing
- `2>/dev/null`: Hides error messages

### New Game / Continue
- "new game" - Start a new adventure
- "continue" - Load saved game

---

## Command System

### Field Commands

- **north/south/east/west**: Move in that direction (e.g., "go north")
- **go to [location]**: Move to specific location (e.g., "go to Pewter City")
- **status / party**: Check party Pokemon (e.g., "check status")
- **bag**: Check inventory (e.g., "open bag")
- **pokedex**: Pokemon encyclopedia (e.g., "view pokedex")
- **save**: Save game (e.g., "save")
- **talk**: Talk to NPC (e.g., "talk")
- **NPC**: Check NPC info (e.g., "NPC list")

### Battle Commands

- **fight**: Enter move selection mode
- **[move name] / [number]**: Use a move
- **bag**: Use item
- **pokemon**: Switch Pokemon
- **run**: Flee from wild battle

### Audio Commands

- **bgm off**: Stop BGM
- **bgm on**: Play BGM
- **volume [0-100]**: Adjust volume
- **cry**: Pokemon cry

### Move Sound Effects

Sound effect mapping: data/audio/sfx-mapping.json

---

## Game Flow

### Opening
1. Prof. Oak greeting
2. Set player name
3. Set rival name

### Pallet Town
1. Choose starter at Oak's Lab (Bulbasaur/Charmander/Squirtle)
2. First battle with rival
3. Oak's Parcel delivery quest

### Adventure Start
- Route 1 -> Viridian City -> Viridian Forest -> Pewter City (first gym)
- Collect 8 badges -> Victory Road -> Elite Four -> Champion

---

## Battle System

### Original Battle Screen (Gen 1 Recreation)

Battle screen is displayed simply like the original. Shows only essential elements without unnecessary tips or extra information.

**Sprite Display Rules (Original Recreation)**:
- **Opponent Pokemon**: Full 13 lines (right-aligned) - Front view
- **My Pokemon**: Top 5-6 lines only (left, horizontally flipped) - Back view feel
- pokemon-ascii-mini.json sprites are 13 lines × 28 characters
- My Pokemon: flip horizontally and show only top portion

**Battle Screen Layout**:
```
╔════════════════════════════════════════════════════════════════╗
║  Wild Pokemon                                       Lv.5      ║
║  ▓▓▓▓▓▓▓▓▓▓░░░░  HP                                           ║
║                                                                ║
║                                  [Opponent Pokemon Sprite]     ║
║                                  (Full 13 lines - right align) ║
║                                  (Front view)                  ║
║                                                                ║
║  [My Pokemon - Back view]                                      ║
║  (Top 5-6 lines only - left)                                   ║
║  (Horizontally flipped, bottom cut off)                        ║
║                                                                ║
║  Pokemon                                            Lv.5      ║
║  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░  HP  22/22                                   ║
╠════════════════════════════════════════════════════════════════╣
║  A wild Pokemon appeared!                                      ║
╠════════════════════════════════════════════════════════════════╣
║     FIGHT             BAG                                      ║
║     POKEMON           RUN                                      ║
╚════════════════════════════════════════════════════════════════╝
```

**Actual Battle Screen Example**:
```
╔════════════════════════════════════════════════════════════════╗
║  Wild PIKACHU                                       Lv.5      ║
║  ▓▓▓▓▓▓▓▓▓▓░░░░  HP                                           ║
║                                                                ║
║                                          :.            :+=.   ║
║                                        .**.       . .-*#**#-  ║
║                                        -*:    =*+::-+#***+-   ║
║                                    .-*##%#+-:#%#+=+**+*+-     ║
║                                    =%%#########- .=***-.      ║
║                                   =%*#%#*+.:%%#*-   -*#=      ║
║                                   .=*#%%#*++*##%%*..+=:       ║
║                                   .:.:+#*%#+=#%##*+=-:        ║
║                                        :**==+*=+%%#=..        ║
║                                         :+*+++#%#%*:          ║
║                                             .++*%*.           ║
║                                                 :             ║
║                                                                ║
║       :  :                                                     ║
║       ++=*.                                                    ║
║    .-+-+--==..                                                 ║
║ .-+*+==+-=++=++:                                               ║
║ :++==+++++=-+=-=-:..==                                         ║
║ :+=-=+==++--=---:-+**#+                                        ║
║                                                                ║
║  BULBASAUR                                          Lv.5      ║
║  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░  HP  22/22                                   ║
╠════════════════════════════════════════════════════════════════╣
║  A wild PIKACHU appeared!                                      ║
╠════════════════════════════════════════════════════════════════╣
║     FIGHT             BAG                                      ║
║     POKEMON           RUN                                      ║
╚════════════════════════════════════════════════════════════════╝
```

### Message Display Principles (Original Faithful)

**What to Display** (same as original):
- "A wild [Pokemon] appeared!"
- "[Pokemon] used [Move]!"
- "It's super effective!" or "It's not very effective..."
- "A critical hit!"
- "[Pokemon] fainted!"
- Status condition messages

**What NOT to Display** (not in original):
- Damage numbers (HP bar decrease only)
- Type effectiveness hints/recommendations
- Move selection tips
- Tactical advice
- AI behavior predictions

### ASCII Art Display

- **Battle Start**: pokemon-ascii.json (full art once)
- **During Battle**: pokemon-ascii-mini.json (mini art)
- **Pokedex**: pokemon-ascii.json (full art)

### Damage Calculation (Gen 1)
```
Damage = ((2*Lv/5+2) * Power * A/D / 50 + 2) * STAB * Type * Crit * Random
```

### Gen 1 Bug Recreation
- Psychic vs Ghost: 0x
- Focus Energy: Decreases critical rate
- Poison vs Bug: 2x

---

## NPC System

### NPC Sprite Loading Rules

#### Loading Order (Required!)
1. Convert Korean->English in `data/sprites/npc-mapping.json`
2. Load `data/sprites/npc_ascii/[EnglishName].json` file
3. Display `.down` key ASCII art

#### jq Loading Example
```bash
# Load sprite (cannot load directly with Korean name!)
jq -r '.down | join("\n")' data/sprites/npc_ascii/Professor_Oak.json
```

#### Main NPC English Filenames
| Name | Filename | Category |
|------|----------|----------|
| Prof. Oak | Professor_Oak.json | Story NPC |
| Nurse Joy | Nurse_Joy.json | Facility NPC |
| Rival | Rival.json | Champion |
| Brock | Brock.json | Gym Leader |
| Misty | Misty.json | Gym Leader |

#### Error Handling
- File not found: Skip sprite, show dialogue only
- JSON parse fail: Use default text

### Dialogue Screen Example
```
+------------------------------------+
|  [NPC Sprite]                      |
|                                    |
|  Nurse Joy:                        |
|  "Welcome to the Pokemon Center!"  |
+------------------------------------+
|  [1] Yes    [2] No                 |
+------------------------------------+
```

---

## Save System

### Saving
- Manual save: "save" or "save [slot number]"
- Auto save: Pokemon Center, city entry, after battle

### Save Slots (10 + autosave)

- **save [1-10]**: Save to specific slot
- **load [1-10]**: Load specific slot
- **save list**: View all slots

---

## Gym Information

1. **Pewter City** - Brock (Rock) -> Boulder Badge
2. **Cerulean City** - Misty (Water) -> Cascade Badge
3. **Vermilion City** - Lt. Surge (Electric) -> Thunder Badge
4. **Celadon City** - Erika (Grass) -> Rainbow Badge
5. **Fuchsia City** - Koga (Poison) -> Soul Badge
6. **Saffron City** - Sabrina (Psychic) -> Marsh Badge
7. **Cinnabar Island** - Blaine (Fire) -> Volcano Badge
8. **Viridian City** - Giovanni (Ground) -> Earth Badge

---

## Data File Reference

### Pokemon Data
- data/pokemon/species.json: 151 species data
- data/pokemon/learnsets.json: Level-up moves
- data/pokemon/evolutions.json: Evolution conditions

### Move/Type Data
- data/moves/moves.json: 165 moves
- data/types/chart.json: 15 type chart

### World Data
- data/world/locations.json: Towns/routes
- data/world/encounters.json: Wild encounters
- data/world/trainers.json: Trainers

### Audio Data
- data/audio/bgm-mapping.json: 45 BGM mapping
- data/audio/cries-mapping.json: 151 cries

### ASCII Art
- data/sprites/pokemon-ascii.json: Full art
- data/sprites/pokemon-ascii-mini.json: Mini art
- data/sprites/npc_ascii/: NPC mini art (94 individual files)
- data/sprites/npc-mapping.json: NPC Korean->filename mapping

---

## Data Key Mapping (Optimized Format)

### species.json
```
n=name, t=types, s=stats[hp,atk,def,spc,spd], c=catchRate, e=baseExp
g=growthRate(ms=medium_slow,mf=medium_fast,s=slow,f=fast), hw=[height,weight]
```

### moves.json
```
i=id, n=name, t=type, c=category, p=power, a=accuracy, pp=pp, pr=priority, ef=effect
Type codes: N=Normal,F=Fire,W=Water,G=Grass,E=Electric,I=Ice,K=Fighting,P=Poison,R=Ground,Y=Flying,S=Psychic,B=Bug,O=Rock,H=Ghost,D=Dragon
Category: P=Physical, S=Special, X=Status
```

### learnsets.json
```
lv=levelUp[[level,move]], tm=[number], hm=[number]
```

### encounters.json
```
g=grass, c=cave, w=water, f=fishing
Format: [[pokemonID, minLv, maxLv, encounterRate]]
```

### trainers.json
```
n=name, ti=title, g=gym, c=city, ty=type, b=badge, r=reward, tm=tmReward
o=order, d=dialogue, p=team[[id,lv,[moves]]], cl=class
gl=gymLeaders, e4=eliteFour, ch=champion, rt=routeTrainers
```

### items.json
```
n=name, d=desc, p=price, cm=catchMod, ha=heal, c=cures, ra=revive
ppr=ppRestore, am=allMoves, sb=statBoost, ef=effect, st=steps, et=evoType
Categories: pb=pokeballs, pt=potions, sh=statusHealers, rv=revives, pp=ppItems
bt=battleItems, rp=repels, es=escapeItems, ev=evolutionStones, vi=vitamins
```

---

## Data Loading

Extract only needed parts with jq (don't load entire large files)

```bash
jq '.["25"]' data/pokemon/species.json      # Species data
jq '.["025"]' data/sprites/pokemon-ascii.json  # Sprite (3 digits)
```

Key formats:
- species, learnsets: number key ("25")
- sprites: 3-digit key ("025")

---

## References (Detailed Guides)

For detailed system information, refer to these documents:

- BGM System Guide (references/bgm-guide.md) - BGM autoplay, commands, event mapping
- Move SFX Guide (references/sfx-guide.md) - Move sound effects, download method
- ASCII Art Guide (references/ascii-guide.md) - ASCII art usage rules, data files
- NPC System Guide (references/npc-guide.md) - NPC sprite display, name mapping
- Cries Guide (references/cries-guide.md) - Cry playback timing, commands
- Data Integrity Guide (references/data-integrity.md) - Data validation rules, checklist

---

## Language Settings

This skill is **English only**.

For Korean version, use the separate skill `pokemon-green-ko`.

### Data File Structure

All names/messages are stored in single language format:
```json
{
  "name": "Bulbasaur",
  "text": "A wild Pokemon appeared!"
}
```

Message files:
- data/messages/battle.json - Battle messages

---

## Help

Use these commands anytime during the game:
- "help" - Command list
- "location" - Current location info
- "progress" - Story progress
