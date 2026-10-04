---
name: ability-pools
description: >
  An ability pool is built by walking **up** the evolution chain, never
  across the family and never forwards. An ability exclusive to an
  evolution is out of reach of every stage below it. Applies whenever
  writing or reviewing code that asks what abilities a species can
  have, and whenever filling in a species' ability data.
---

A pokemon's ability pool is what it and its **pre-evolutions** can be born with. Nothing else.

The rule that decides the shape is one-directional: **an ability exclusive to a stage is out of reach of every stage below it.** A Magikarp cannot reach Intimidate because Gyarados has it. The reverse is fine and is how the mainline works anyway: an evolution keeps what its line was born with, so Charizard reaches Blaze and Solar Power through Charmander.

## The two helpers

[`getSpeciesAbilities`](../../../src/data/species/__create.ts) walks `evolvesFrom` upwards and unions each stage's `abilities` and `hiddenAbilities`. It answers both what this stage could have been born with and what it could ever come to have, and it is what anything offering a pokemon a new ability must ask.

[`getSpeciesAbilityPools`](../../../src/data/species/__create.ts) is the same walk split into a regular list and a hidden list, since a **birth roll** treats the two differently. It is what [`encounter.ts`](../../../src/overworld/encounter.ts) and [`breeding.ts`](../../../src/overworld/breeding.ts) read. How it splits them is the next section.

There is deliberately no helper that unions a whole `family`. One existed briefly and was wrong: it let a Magikarp reach a Gyarados ability. If a new pool is needed, walk upwards.

## What a stage inherits is rare

**An ability exclusive to a pre-evolution is hidden on the stages above it.** Only a species' own `abilities` are ordinary for that species; anything it reaches only through a stage below is rolled out of the narrow hidden band instead. A Persian is born Limber or Technician, and a Persian carrying a Meowth's Pickup is the uncommon one. So is a Gyarados with Magikarp's Swift Swim, a Butterfree with Caterpie's Shield Dust, and a Vaporeon with Eevee's Adaptability.

A pre-evolution's hidden ability was already rare and stays rare. Nothing is written down for this: it falls out of the pools walk, so a line's data says what each stage has and the split follows.

## Mega abilities

A species carries no record of what its Mega form's ability would be. The `latent` field that held them is gone, so a Mega ability is simply not in the data until Megas themselves are.

## Filling it in

Check the ability against PokeAPI rather than writing it from recall.

**A species that is a final evolution in this registry is not necessarily terminal in canon.** Kanto is all that is registered, so Golbat, Onix, Chansey, Scyther, Porygon, Tangela, Electabuzz, Magmar, Rhydon, Magneton, Lickitung, Seadra, Primeape, Farfetch'd and Mr. Mime all look final here and gain an evolution in a later generation. Giving one of them an ability today creates a violation of this rule the day that evolution lands, so leave them alone.

**Regional forms are not a source.** An Alolan Marowak's Cursed Body is out of reach of a Kantonian Marowak, and the same goes for every Alolan, Galarian, Hisuian and Paldean form. They are a different pokemon wearing the same name, not a stage of this one.

## Inventing a filler ability

**A newly added final evolution that cannot reach four abilities gets filler suggestions before it is written down:** as many as it is short, plus one alternative to choose from. Count what it reaches by walking up the chain, with Megas and alternate forms left out of the count, and count against every generation rather than the one being written.

A species short of four abilities can be given one the mainline never gave it. It goes in `hiddenAbilities`, never in `abilities`: an invented ability should be rare to hatch, and the hidden band is what makes it rare. The band does not widen with the list, so a species with three hidden abilities rolls hidden as often as one with a single one and splits the band between them.

**Suggest from every generation, not from the enum.** The candidates are all the abilities the mainline has ever printed, and most of them are not in `src/data/ids/abilities.ts` yet. An unregistered one is a normal answer: taking it means adding the id, a registry entry with its player-facing description, and the battle implementation, which is what Plus and Magic Bounce each cost when the Johto lines landed. Say what a suggestion would cost, and let that weigh on the recommendation rather than shorten the list.

### Count what a later generation already gives it

**Read the species' whole dex entry, not the generation being written.** A pokemon added here in its Gen 2 shape still carries every ability the mainline has given it since: Sentret has Frisk because Gen 5 handed out hidden abilities wholesale, not because Gen 2 had them. PokeAPI's ability list is the current generation's, so it is already the right answer; ask it before counting anything short.

A species is only short of four once that whole list is in hand. Most of the ones that look short are not.

### Three kinds of slot are already spoken for

None of them may be spent, and each is a reason to leave a species alone rather than fill it. All three are stages of the same line, because a stage is the only thing that shares a pool.

**What a future baby pre-evolution carries.** A baby stage added in a later generation sits below the species and its abilities walk straight up. Tyrogue brings Guts, Steadfast and Vital Spirit to both Hitmons, Smoochum brings Hydration to Jynx, Munchlax brings Pickup to Snorlax, Happiny brings Friend Guard to Chansey, Mime Jr. brings its set to Mr. Mime, Cleffa and Igglybuff bring Friend Guard to their lines. Those species fill themselves up and need nothing invented.

That holds only where the baby brings something new. Bonsly, Wynaut and Mantyke each carry exactly their adult's list, so Sudowoodo, Wobbuffet and Mantine gain nothing the day those babies land and would stay short forever. Read the baby's own abilities before deciding a slot is spoken for; where they match, the species is filled now. It is safe because pools walk **up** only: a filler on the adult can never leak down to the baby, and a baby is a first stage rather than a final evolution, so it never has to reach four itself.

**What a future evolution carries.** A species that gains an evolution in a later generation is not a final evolution and is not filled at all: that is the same rule as the Kanto caveat above. Handing Gligar a Poison Heal because Gliscor will have it breaks the pool the day Gliscor lands, since a pre-evolution's abilities walk up and the exclusivity is gone.

**What that future evolution will itself need filling with.** An evolution added later may be short of four on its own, and whatever is invented for it then has to be an ability the stage below cannot already reach. Spending a good fit on the pre-evolution today takes it off the table twice.

### A form reserves nothing

A Mega Evolution or a regional form is **not** one of those slots, and it never lowers the number of fillers a species is owed. A Mega's ability is not stored on the base species at all, so there is nothing there to keep free: Ampharos reaches Static and Plus, and is short **two**, with Mega Ampharos' Mold Breaker counting for nothing.

The one thing a form forbids is narrow: do not hand the base species that form's own ability early. Charizard is not given Tough Claws before Mega Charizard X exists, and a Kantonian Marowak is never given an Alolan Marowak's Cursed Body. Everything else is fair, and the species still has to reach four.

### How to check

Ask PokeAPI for the species and read three things: its **current abilities**, which is every generation's; its **varieties**, which names any Mega, regional or convergent form; and its **evolution chain**, which says whether anything was added above or below it. Varieties only rule specific abilities out, so the count comes from the ability list and the chain: a species with nothing new above or below and three abilities is short of one, and one with two is short of two. Something added above or below it is the reason to stop.
