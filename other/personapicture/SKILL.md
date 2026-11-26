---
name: personaPicture
description: Draw random personas from the warm-up datasets, store them in media/personas/personas.jsonl with each one's characteristics and image prompt, generate each one's profile picture in the low-angle selfie style through treg, and have SubQ check it matches the persona, regenerating until it does. Use when the owner asks for personas, profile pictures for personas, or more of them.
---

# personaPicture

A persona here is just a person, not a buyer persona: who they are, drawn from
the same datasets the Reels warm-up uses (`src/warmup/persona`,
`~/.logCli/datasets`). Code: `src/media/persona`, run by
`scripts/media/personaPictures.ts`.

Only adults are drawn (`PERSONA_MIN_AGE`, 18). The doomscrolling dataset has
teenagers in it, and they are filtered out before the draw.

## What's stored

`media/personas/personas.jsonl` holds one line per persona:

- `personaId`, `seed`, `country`
- `characteristics`: age, gender, occupation, education, when and why they
  scroll, mood, sleep, device and the rest of the draw's summary
- `sources`: the dataset rows it came from
- `prompt`, `avoid`, `size`, `resolution`, `generatedWith`: what is fed to the
  image model
- `attempts`: every generation, with its task, URL, credits, the prompt used and
  SubQ's scores
- `profilePicture`, `matched`

Each picture is at `media/personas/<personaId>/profilePicture.png`.

## The style

It is read from the owner's two example photos, which are kept in
`~/.logCli/personaExamples` and are never committed, because they are real
people:

- the camera held low, below the chin, pointing up at the face, with the
  ceiling behind the head: an unflattering angle
- the arm holding the camera out of the frame: an arm in the picture looks
  wrong and unnatural (the owner, 2026-10-24)
- a flat, unsmiling expression and ordinary clothes
- bad light: a blown-out ceiling light, or a dark room lit from below
- old front-camera quality: soft focus, noise, washed-out colours

The place comes from the persona's `profession` in the social behaviour dataset
(Engineer, Teacher, Marketer, Researcher, Entrepreneur, Student, Freelancer,
Doctor, Designer, Other), or `Unemployed` from the occupation. Each has three
places in `BACKGROUNDS`, and no two personas in a draw get the same one
(`backgroundOf`), because the owner said the pictures can't all look the same. The
light comes from the time of day they scroll. The prompt never says phone, iPhone or screen (`listingCreative`), and
it carries no text or logos.

Generation is done only from the prompt. The owner's photos are never passed to the
image model, so no real face is copied. They go only to SubQ, as the style to
judge against.

## The check

SubQ (Decisions API) gets the picture as image 1 and the examples as images 2
and 3. It is asked about image 1 only:

- `matchesPersona` (must reach 0.7)
- `ageFits`, `genderFits`, `lifeFits`, `selfieStyle`, `looksReal`, `noText`
  (each must reach 0.6)
- `armHidden`: the arm holding the camera is out of the picture or under 20% of
  it (must reach 0.6)
- `lowAngle`: the camera is below the face pointing up at it (must reach 0.6)
- `unflattering`: an unflattering, careless shot, not posed or attractive (must
  reach 0.6)

When any of them is low, it regenerates. The first prompt already carries the
fixes for selfieStyle, noText, armHidden, lowAngle and unflattering, because
first attempts missed them. Each later prompt adds a fix for every check that
has failed so far. It tries at most 5 times, then keeps the closest attempt and
sets `matched: false`.

- `likeReference`: taken the same way as the style reference, the picture the owner
  liked best (`--styleFrom <id>`, now freelancerSelfEmployedMale36). It is SubQ's
  fourth image, after the picture and the owner's two examples.
- `backgroundDistinct`: a second SubQ call shows the picture beside the other
  personas' pictures (three at a time) and asks whether its kind of room
  differs from every one of theirs. Only the kind of room counts, because a
  classroom and an office failed for sharing ceiling tiles. When it fails, the
  persona moves to the next place for its profession (`nextBackground`,
  `backgroundsTried`) before the retry.

Every image sent to SubQ is shrunk to a 768 px JPEG first (`shrinkImage`), because
SubQ refuses more than 8 MiB of images in one call.

## The accounts' own personas

`--accounts` gives every new Facebook account (`needsLogin`, no `profilePhoto`)
a persona of its own:

- It is drawn in the account's country with `seedOf(accountName)`, the seed the
  Reels warm-up uses, and written to `~/.logCli/personas/<account>.json` when
  that file is missing. The picture and the warm-up are the same person.
- The id starts with the city (`kamloopsPartTimeEmployeeFemale18`), the prompt
  names the home ("from Kamloops, Canada"), and the record keeps `account`
  (accountName, homeCity, homeCountry).
- The background check compares each picture with the last three pictures from
  the same country.
- A picture goes into Twenty only when it passes every check:
  `socialAccounts.profilePhoto` is set to its path (`saveProfilePhoto`), the
  field the host's profile step uploads from.

`--accountsRedo` re-checks every account picture that isn't approved against
the current checks and regenerates whichever fail. An account whose last
attempts never passed moves to another place first, and an account with no
picture yet is generated.

Clothing checks (the owner, 2026-10-24):

- `noStonewashedHoodie`: no stonewashed, acid-washed or faded washed-out
  hoodie or sweatshirt.
- `clothingFits`: casual clothes that suit the home and the place, not formal
  and not a plain t-shirt.

`backgroundDistinct` passes at 0.25 (`PERSONA_BACKGROUND_PASS`). Places are
unique when they are assigned, and SubQ scored different rooms as low as 0.11,
so a higher bar only burned tries. A picture kept after failing keeps the
background it was taken in.

On 2026-10-24 all 20 accounts (10 in Pennsylvania, 10 around Kamloops) matched,
and each one's picture is its profilePhoto in Twenty.

## The owner's verdict comes first

- `--approve <id,id>` locks pictures the owner likes (`approved`). They are never
  rechecked or regenerated, and `--redo` refuses them.
- `--redo <id>` rejects one picture (it is kept in `rejected`, with its
  attempts) and regenerates it.
- `--recheck` checks every picture that isn't approved against the current
  checks, and regenerates whichever fail.

The owner approved fullTimeEmployeeMale30, fullTimeEmployeeMale26 and
freelancerSelfEmployedMale36 ("perfect") and rejected studentFemale25
(2026-10-24).

## Running

```bash
bun scripts/media/personaPictures.ts --count 5 --country US
```

Run it live through Monitor (rule 26). It costs $0.034 an image through
`reapi.image-gen.gemini-3-pro-image`, plus one SubQ call per image (rule 41:
only as many as the owner asked for). A new run replaces `personas.jsonl`.
