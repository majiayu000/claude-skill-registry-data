---
name: vikingo-klon
description: How a Vikingo colleague starts working on a Vikingo website (vikingo.hu or vikingo.studio) with Claude Code — which GitHub repos to clone, the local LocalWP clone (devvikingo.local, studio.local), refreshing the clone from the live site's Vikingo Backup, and the safety rules of working on a clone that holds live data. MUST be applied when a colleague asks how to start, set up, refresh or use the local clone, which repo to download, or wants to edit pages of vikingo.hu / vikingo.studio and has no clone yet. Routes to the site repo's own docs, which stay the single source of truth. Triggers on klón, klónfrissítés, Local, LocalWP, devvikingo.local, studio.local, Vikingo Backup mentés, melyik repót töltsem le, hogyan kezdjek, oldalszerkesztés, vikingo.hu, vikingo.studio.
---

# Vikingo klón: munka a weboldalakon

Ez a skill útvonalat mutat: melyik oldalhoz melyik repó és melyik klón
tartozik, és hol a részletes leírás. A lépések a repókban élnek. Ide ne
másold be őket, mert a repó változik, a skill pedig elavulna.

## Kinek szól

A kollégák nagy része nem fejlesztő. Ha ők kérdeznek:

- lépésenként, tegezve, egyszerű szavakkal válaszolj;
- minden parancsot magad futtass, ha tudsz; ha nekik kell, egyenként add;
- jelszót, kulcsot ne kérj be a chatbe, és ne írd ki.

## Melyik oldal, melyik repó

Mindkét oldalon az **éles az igazság**, a klón a saját gépen futó másolat
(LocalWP). A klónon szabadon lehet próbálni, élesre csak a megbeszélt úton
kerül változás.

| Oldal | Repók (`~/Documents/Github` alá) | Klón | Kezdd itt |
|---|---|---|---|
| vikingo.hu (kurzus) | `wp-plugin-vikingo-hu-platform`, `wp-plugin-vikingo-hu-adatplatform` | `devvikingo.local` | platform repó: `docs/klon-frissites.md`, „Új gépen először” |
| vikingo.studio (ügynökség) | `site-vikingo-studio` (a bővítmény kódjához még `wp-plugin-vikingo-studio`) | `studio.local` | `site-vikingo-studio`: `docs/klon-frissites.md`, „Új gépen először” |

Letöltés (a mappa számít: a vikingo.hu frissítő szkriptje innen köti be a
bővítményeket):

```bash
gh repo clone vikingokft/<repó> ~/Documents/Github/<repó>
```

Ha a `gh` 404-et vagy „Could not resolve” hibát ad, a kolléga nincs a repó
csapatában, vagy nem fogadta el a GitHub-meghívót. Ezt nem lehet
megkerülni: szóljon Bencének. A belépés és a csapatok leírása:
`vikingokft/vikingo-github-szabalyok`, `belepes.md`.

## Mit csinálj munkakezdéskor

1. Kérdezd meg, melyik oldalon dolgozik (ha nem derül ki).
2. Nézd meg, megvannak-e a táblázat repói a `~/Documents/Github` alatt. Ha
   nincsenek, töltsd le őket, ha megvannak, `git pull`.
3. Olvasd el az oldal repójának `CLAUDE.md`-jét, és onnan dolgozz. Az ottani
   szabály erősebb ennél a skillnél.
4. Nézd meg, fut-e a klón a Localban (a címe a táblázatban). Ha nincs klón,
   vagy régi, kövesd a „Kezdd itt” oszlop leírását.

## vikingo.hu: a klón frissítése

Egy parancs teszi a `devvikingo.local`-t az éles friss másolatává, a
leírás: platform repó, `docs/klon-frissites.md`. Röviden: a megosztott
meghajtóról a legfrissebb Vikingo Backup teljes mentés (`…-full`),
kicsomagolva, a klón fut a Localban, majd a platform repóból:

```bash
bash docs/klon-frissites/klon-frissites.sh ~/Downloads/<kicsomagolt-mentés-mappa>
```

A szkript a végén maga ellenőriz (oldalak 200, mérési környezet `local`).
Ha valamelyik ellenőrzés nem stimmel, ne dolgozz tovább a klónon: a leírás
„Ha valami nem stimmel” része segít.

Oldalszerkesztés előtt: platform repó, `docs/oldalszerkesztes.md`.

## vikingo.studio: a klón frissítése

Ugyanígy egy parancs, a leírás: `site-vikingo-studio`, `docs/klon-frissites.md`.
A vikingo.studio mentése kell (`vikingo-vikingo-studio-…-full`), a klón fut
a Localban, majd a `site-vikingo-studio` repóból:

```bash
bash bin/klon-frissites.sh ~/Downloads/<kicsomagolt-mentés-mappa>
```

A bővítmény a klónon a kiadott
változat, az élesről jön: a bővítmény kódjának változása kiadás után
látszik a klónon. A munka szabályai: `site-vikingo-studio`, `CLAUDE.md`.

## Mindkét klónon érvényes

- **Az SSL-t a szkript teszi rendbe.** A Local új oldalnál elsőre rosszul
  állítja be: a tanúsítvány nem megbízható, vagy a `/wp-admin` a belső,
  `http`-s portra visz. Mindkét szkript minden futáskor javítja; ha a Mac
  jelszót kér egy felugró ablakban, az a kolléga saját gépes jelszava, a
  tanúsítványhoz. Kézzel (Local „Trust” gomb, `site.conf.hbs`) ne javítsd.

- **A klón valódi levelet küld** (az éles levélküldő beállítás jön át):
  űrlapot, vásárlást, feliratkozást csak a saját címével próbáljon.
- **A mentésben éles adat van** (vevők, leadek): a mentést és a klónt ne
  ossza meg, ne töltse fel máshova; a megosztott meghajtóról töltse le.
- **A `WP_ENVIRONMENT_TYPE` a klónon `local`**: ez kapcsolja ki a hirdetési
  mérést. Enélkül a klón az éles hirdetési fiókokba küldene konverziót.
- **Élesre a klónból semmi nem megy át magától.** A bővítmény élesre csak a
  saját frissítő csatornán kerül (kiadás után a WordPress Bővítmények
  oldalán), zipcsere soha. Oldaltartalmat élesen az adott repó leírása
  szerint szerkessz.
- **Amit egy kolléga megtanul** egy oldal szerkesztéséről (minta, csapda),
  az az oldal repójába kerül (vikingo.hu: `docs/oldalszerkesztes.md`), nem
  ebbe a skillbe.
