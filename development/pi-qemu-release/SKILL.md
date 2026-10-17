---
name: pi-qemu-release
description: Build TriMixxx's SD card images and releases with pi-qemu - a deck's dev card from stock Raspberry Pi OS (`pi-qemu image build`), the A/B release card and its RAUC update bundle from HEAD's pi/vX.Y.Z tag (`release build`), each deck's own card with its identity (`release card`), broken updates for the fault tests (`release faults`), an update shipped onto a deck (`deck ship`), and a real deck readied for its first release card (`deck prepare`, bootloader and boot watchdog included). Use when asked to make an image, a release (its version, notes, tag and GitHub release), a deck's card, to ship or rehearse an update, or to prepare a deck; and to try a release on emulated decks before any real deck gets it.
---

# pi-qemu: images, releases, cards

The deck's software reaches a card two ways, both through `pi-qemu`:

- **A dev card** (`pi-qemu image build DECK`): stock Raspberry Pi OS, then
  every deploy step (`pi-qemu/deploy/NNN_*`), as against any deck. What the
  emulated decks run, and what a release is made from.
- **A release** (`pi-qemu release build`): that system sealed read-only into
  an A/B card every deck can run, and its RAUC bundle for updates over the
  air; then each deck's card, with its identity on p7 (`release card DECK`).

`pi-qemu/PLAN.md` Part 1 is the design (its invariants are numbered; the
code cites them), `pi-qemu/rauc-pi-4-setup.md` the how-to, and PLAN.md §7
the runbook for putting real decks on release cards.

## Rules

1. **Real decks only when asked.** `--host trimixxx-pi`, `trimixxx-pi-2`,
   `trimixxx2`, ... are real decks: ship to one, or prepare one, only when the
   person asked for that deck. Try everything on emulated decks first.
   - **Over its cable:** `deck ship` and `deck prepare` take a real deck only
     over the Mac's cable, by its `-eth` alias (`--host trimixxx-pi-2-eth`;
     `pi-qemu deck alias --host trimixxx-pi-2` writes it, the deck cabled).
   - Over Wi-Fi they refuse, unless `--wifi`: the person's call, never yours.
     Refused, go back to them.
   - Commands handed to the person name the `-eth` alias; with `--wifi` only
     if they asked for Wi-Fi.
2. **The person flashes cards.** Build the image and give them the exact
   path; never run `diskutil`, `dd` or anything else on a card or disk. A
   release's cards are `.img.xz`: Raspberry Pi Imager and balenaEtcher take
   them as they are, or `xz -dc CARD | sudo dd of=/dev/rdiskN bs=4m`.
3. **Releases are tags, and Sam picks the version.** A release's version is
   HEAD's `pi/vX.Y.Z` tag, and `release build` refuses a dirty tree. Tags are
   signed, so they need a message: `git tag -m "TriMixxx X.Y.Z" pi/vX.Y.Z`.
   The repo's other parts tag `midi-s3/v…` and `prolinks-compat/v…`. Tagging
   is the person's call, and so is the version: ask which part goes up
   ("Versions", below), never work it out from the changes.
4. **The golden pair follows main; by hand, it is the person's call.** Every
   new instance starts from it, and it is main's latest by itself: `deck up`
   and crew merge have it made again from the main checkout whenever main
   changes what goes onto a deck (`image golden`, which anyone may run: it
   only builds main's code; pi-qemu/README.md, "The golden: main's latest").
   `image build trimixxx0` and `deck golden CARD` by hand replace it with
   other code: only when asked. Try image builds on a scratch DECK name, and
   delete its outputs afterwards (below).
5. **The bootloader is the person's call.** `deck prepare --eeprom` flashes a
   real deck's EEPROM and reboots it.
6. **Docker's disk:** builds need ~6 GB free; pi-qemu checks and stops.
   Freeing space is the person's call: say so, never prune. Keep the build
   caches (`.cache/base`, Docker's build trees). `pi-qemu cache` lists them
   all, with their sizes.

## Dev cards

```sh
pi-qemu image build onetest           # -> .cache/build/onetest.img, its log onetest.log
pi-qemu image build onetest --no-window --rebuild-base
```

- It builds in an instance of its own, `build-DECK`: `pi-qemu deck ssh
  build-DECK` looks at a build in progress. A failed build leaves its machine
  off and its card for a look (`deck up build-DECK`, then `deck rm build-DECK`).
- The first boot and the base step are cached in `.cache/base/` while
  their inputs are unchanged (the stock card, the deck's name and panel, the
  key, the password, the seed, `000_base.pi.sh`). The rest takes minutes,
  most of it Docker builds that are cached too.
- The stock card is pinned in `pi-qemu/image/stock.env`; the first-boot seed
  is `image/user-data.in` and `network-config`; the console password and the
  home Wi-Fi are in `image/secrets.env` (gitignored, never printed or
  committed).
- A build window follows the log unless `--no-window`; its steps come from
  the build's own `==> plan:` line.
- `.cache/` and `archives/` are at the main checkout's root, git-ignored, the
  same for every worktree (`pi-qemu/README.md`, "Caches and archives").
- A scratch build's outputs to delete afterwards: `.cache/build/DECK.img`,
  `DECK.json`, `DECK.log`, `DECK.build.json`, `DECK.lock`, and
  `.cache/base/DECK-*.img`.
- Each card has what it was built from beside it (`DECK.json`: the commit,
  and whether the checkout held exactly that commit's code). One build of a
  deck runs at a time: a second refuses, saying which runs.

## Versions

From 1.0.0 (2026-10-15) on, a release's version follows Sam's scheme, in
his words:

> From then on, versioning will be following this scheme:
> X.Y.Z . X is for "large" change, such as new feature etc. Y is for more minor new features and refactors, and Z is for bug fixes. It's subjective and I will decide.

So each version is his to give: ask him which part goes up (at night, the
nightman asks him). 0.0.1, 0.1.0 and 0.1.1 came before the scheme.

## Releases

A release is made in this order:

1. **The version:** Sam's (above).
2. **Its notes,** `docs/releases/X.Y.Z.md`: everything since the last
   release's tag, from `git log pi/vA.B.C..`, the PRs merged since, and the
   fork's and prolink's logs between the commits the two releases pin. What
   changed for the DJ, in the deck's system and in the tooling; what
   updating from the last release means; whether the S3's firmware changed
   (`git log pi/vA.B.C.. -- firmwares/`), which a release doesn't carry.
   They go through a PR like any change.
3. **The tag,** on main's commit that has the notes:
   `git tag -m "TriMixxx X.Y.Z" pi/vX.Y.Z SHA`, then
   `git push origin pi/vX.Y.Z`, by Sam. A crew session can't push a tag. It
   builds from a local one, `git -c tag.gpgSign=false tag pi/vX.Y.Z SHA`,
   and the GitHub release (6) puts the same tag on GitHub: lightweight and
   unsigned where Sam's are signed, and not on gitea, where `origin` pushes
   too. Sam then pushes it on (`git push origin pi/vX.Y.Z`), or signs it
   first (`git tag -f -m "TriMixxx X.Y.Z" pi/vX.Y.Z SHA`, then
   `git push -f origin pi/vX.Y.Z`).
4. **`release build`** from a checkout at that commit, clean (in a worktree,
   `pi-qemu worktree prepare` first).
5. **A rehearsal on emulated decks** (below): a deck on the last release
   takes the new bundle and keeps it, and the new release's card boots.
6. **The GitHub release,** once 5 has passed:
   `crew gh -R usr-ein/TriMixxx release create pi/vX.Y.Z --target SHA --title "TriMixxx X.Y.Z" --notes-file docs/releases/X.Y.Z.md`.
   The notes only: the cards and the bundle stay in `archives/releases/`
   (Sam's call for 1.0.0; the repo is public). Then
   `git ls-remote origin refs/tags/pi/vX.Y.Z` must print SHA: that is
   GitHub's tag itself, where a fetch would keep the local one whatever
   GitHub's names. If it doesn't, stop and say so: Sam's push of the local
   tag would be refused by GitHub and taken by gitea.
7. **Shipping** to the real decks: Sam's, or on his ask (rule 1), each deck
   over its cable (`--host trimixxx-pi-eth`, `--host trimixxx-pi-2-eth`).

```sh
git tag -m "TriMixxx 1.2.0" pi/v1.2.0      # the person's call
pi-qemu release build                      # -> archives/releases/1.2.0/
pi-qemu release card trimixxx2             # -> releases/1.2.0/trimixxx2-1.2.0.img.xz, to flash
pi-qemu deck ship --host trimixxx-pi-2-eth # the update, over its cable (only when asked)
pi-qemu release faults                     # releases/1.2.0-nonet, -nossh, -noinitramfs, -panic, -hang
```

- `release build` builds the system (`image build trimixxx-release`), then
  seals it in the release container (`release/Dockerfile` running
  `release/container.sh`): `trimixxx-X.Y.Z.img.xz` (the card each deck's own
  is made from), `trimixxx-X.Y.Z.raucb` (the update), `rootfs.squashfs`,
  `boot.vfat`, `manifest.txt`. `--keep-system` seals the system card built
  last time; `--rehearsal X.Y.Z` lets an untagged or dirty tree through, and
  says so in the manifest.
- Releases always land in the main checkout's `archives/releases/`, also
  from a worktree. Nothing clears the archives. `--version X.Y.Z` names another release than HEAD's for
  `release card`, `release faults` and `deck ship`.
- A deck's identity (its name, ssh host keys kept across reflashes, its
  hotspot, the home Wi-Fi) is in `archives/decks/DECK/`, made the first time
  `release card` needs it. The release's own card holds none: a deck started
  from `trimixxx-X.Y.Z.img.xz` is `trimixxx`, with no Wi-Fi and no ssh (it
  has no host keys). A deck is flashed with its own card.
- `deck ship` streams the bundle into RAUC's state partition, installs it
  into the other slot and reboots into it as a trial; the deck's health check
  (network up and ssh answering) keeps it or rolls it back. Sending and
  installing show how far they have got: a bar on a terminal; run by an agent
  (no terminal), a plain line every 10% or 30 s (sent, rate, time left; then
  RAUC's percent).

## Trying a release on emulated decks

```sh
pi-qemu release build --rehearsal 0.0.9 --keep-system --no-window
pi-qemu release card trimixxx0 --version 0.0.1            # the emulated deck's card of a release
pi-qemu deck up abtest --from archives/releases/0.0.1/trimixxx0-0.0.1.img.xz   # unpacked, sparse
pi-qemu deck ship abtest --version 0.0.9                  # a trial of B, then its health check
pi-qemu deck ssh abtest 'tail -3 /var/lib/rauc/trimixxx-health.log; rauc status'
pi-qemu deck ssh abtest 'sudo rauc status mark-active other && sudo systemctl reboot'   # back to A as a trial
```

The last line is what Diagnostics' RESTART INTO does, for a release from
before it (0.1.1 and older).

Afterwards, delete what the rehearsal made, and only that: `deck rm abtest`,
`archives/releases/0.0.9*`, and the emulated deck's cards it made
(`releases/0.0.1/trimixxx0-0.0.1.img.xz`; rehearsing a tagged release, its
own `trimixxx0-X.Y.Z.img.xz` too). Keep the tagged releases and the real
decks' cards: an untagged release is never left in `archives/releases/`.

## Readying a real deck (only when asked)

```sh
pi-qemu deck prepare --host trimixxx-pi-2-eth trimixxx2            # reads it only
pi-qemu deck prepare --host trimixxx-pi-2-eth trimixxx2 --eeprom   # bootloader + boot watchdog: reboots it
```

It writes the board's serial into `mixxx_config/units/DECK.json` (commit it
before the release is built: the release's config.txt gives each board its
own section), keeps the deck's ssh host keys for its identity, checks the
bootloader (2022-12-01 or newer knows `tryboot_a_b`), and captures its boot
files and profiles in `archives/captures/` (private: Wi-Fi passwords).
An emulated deck can stand in to try it (`deck prepare NAME DECK`); it has no
bootloader, so `--eeprom` stops there.
