---
name: trimixxx0
description: Run your own emulated TriMixxx deck (trimixxx0, a Raspberry Pi 4 under QEMU) with `pi-qemu deck` to test deck software without the hardware - up in ~3 s from a snapshot of main's latest, screenshots of its screen (headless), buttons/jog/encoder/fader over the virtual S3, touches, LEDs, Mixxx's recorder, ssh, Mixxx's logs, and deploying your own Mixxx build, Mixxx config/skin/mapping, pi_config or launcher changes onto it with the numbered deploy steps. Use whenever a change to mixxx/, mixxx_config/, pi_config/, trimixxx-launcher/, ttymidi, pi-qemu/deploy/ or the S3 MIDI contract should be checked on a running deck. Many agents can each run their own at once.
---

# trimixxx0: your own emulated deck

`pi-qemu deck` gives you a deck of your own: its own copy of the card, ssh
port, ssh alias and control socket. It is headless and silent. **It starts in
about 3 s** from a snapshot, already booted with Mixxx running; a cold boot
takes about 7 s. That snapshot, the golden, is **main's latest**: it is made
again whenever main changes what goes onto a deck, so a new deck runs what
main has now, and your own changes are what you deploy on top. Other agents
may be running theirs at the same time, and the person at the laptop may be
running their own (with windows). Yours touches none of them.

`pi-qemu` is the one tool for decks (`pi-qemu help`, `pi-qemu deck`,
`pi-qemu deck VERB --help`). Every verb names its deck: your instance's NAME,
or `--host ALIAS` for a real deck. There is no default deck. For anything
not covered here (running a card of your own, USB sticks, troubleshooting),
read `pi-qemu/README.md`.

Run it from your checkout (or worktree): pi-qemu deploys the code of the
checkout it runs in, and finds the built QEMU and the golden card in the main
checkout by itself. In a git worktree, read "Working from a git worktree"
below first.

## Rules

1. **Pick one NAME and only ever touch that instance.** Make it unique to
   your task, e.g. `fix-sync-meter`.
   - Never `pkill` qemu, pi-qemu or docker.
   - Never `deck rm|kill|stop|down` a NAME you did not create.
   - Never `deck golden` or `image build trimixxx0` unless asked: they
     replace the golden pair everyone's instances start from. `image golden`
     is fine: it only ever makes it from main's code.
2. **Never `--host` a real deck** (`trimixxx-pi`, `trimixxx-pi-2`,
   `trimixxx2`, ...) unless the person asked you to, for that deck.
3. **No sound on the Mac, ever.** Never pass `--audio speakers`. To check
   audio, record it to a WAV file and analyse the file (see below).
4. **Reuse, do not restart.** `deck up NAME` on a running instance only
   reports it, so call it at the start of every step. To change how it runs
   (`--fresh`, `--boot`, `-- --audio ...`), `rm` it first: on a running
   instance `up` refuses options rather than ignore them.
5. **Clean up, or say what is left.** See "Before you finish". Not optional.

## Start (or reuse) your deck

```sh
pi-qemu deck list                    # "no instances", or what runs (yours may already)
pi-qemu deck up NAME                 # ~3 s from the golden snapshot; reports it if running
```

The instance lives in `~/.pi-qemu/instances/NAME/`. Each one needs 2 GB of
RAM; if `list` already shows about 4 running, ask before starting another.

- **Main's latest first.** `up` ends by saying where its card came from
  (`from 5f0b01a of 2026-10-16 15:20: main's latest`). When main has just
  moved on, `up` first waits for the golden to be made again: a few minutes,
  more when much of Mixxx is rebuilt, with its steps as they go. Give it a
  long timeout (10 min, or run it in the background); if your shell gives up
  first, run `up` again: it waits for the same remake. When the golden can't
  be made (main doesn't build, the main checkout isn't at main, a remake that
  looks stuck), `up` says so and starts from the last golden: say so in your
  results, and tell the nightman (or Sam) about a stuck one; stopping it is
  theirs.
- **A stopped deck may start fresh.** If main moved on while your deck was
  stopped, its next `up` starts it from the new golden, saying first what it
  loses: what you deployed, files you put on it, its saved state. Deploy your
  changes again then. A running deck is never replaced (`up` only says it is
  behind); a deck from `up --from CARD` never is.
- `up NAME --fresh`: start again from the golden snapshot; your card's
  changes are lost.
- `up NAME --boot`: boot instead of restoring (~7 s), e.g. to test the boot
  itself. Then `deck ready NAME`.
- `up NAME --from CARD`: boot a card of your own (a clone of it), e.g. a
  release card.
- `stop NAME`: suspend (~5 s; leaves a ~1 GB snapshot until the next `up`,
  which resumes it in ~3 s, on a new ssh port that `deck ssh` follows;
  unless main moved on meanwhile: then it starts fresh, as above).
- `up NAME --window`: also shows its screen and panel on the Mac, but only
  when the person wants to watch.

## Look at it

```sh
pi-qemu deck shot NAME "$TMPDIR/NAME-1.png"   # the 1280x800 screen, headless; Read the PNG
pi-qemu deck leds NAME                        # the S3's LEDs as JSON: play, cue, loopIn/Out, ringA/ringB
pi-qemu deck status NAME                      # Pi running, S3 link, ssh port, run dir
pi-qemu deck ssh NAME 'tail -50 /tmp/mixxx/mixxx.log'   # Mixxx (also stderr.log; .1 = previous run)
pi-qemu deck ssh NAME 'tail -f /tmp/mixxx/stderr.log'    # the same lines as they happen, without times
pi-qemu deck ssh NAME 'journalctl -b -u trimixxx-launchd -n 50'
```

`mixxx.log` is written in batches (Mixxx flushes it at `critical`), so its
last minutes may not be there yet; `stderr.log` has every line at once. To
time something, stamp `stderr.log` as it grows (a `tail -F` into a small
Python loop on the deck) and read that.

Put screenshots in a temp or scratch directory, not in the repo. Take one
after anything you expect to change the screen, and look at it before you
conclude. The deck's clock is UK time (Europe/London), which may differ from
the Mac's: mind the offset when matching its logs with output on the Mac.

## Poke it like a DJ

These go through the virtual S3 as MIDI on the Pi's UART, exactly as the real
board sends them, on trimixxx0's wiring (`mixxx_config/units/trimixxx0.json`):

```sh
pi-qemu deck press NAME play              # press+release, 80 ms; `press NAME cue 600` holds
pi-qemu deck down NAME cue                # ... `deck up NAME cue` releases
pi-qemu deck jog NAME 3240                # +clockwise, 12960 ticks per turn
pi-qemu deck touch NAME on                # platter touch (scratch); `touch NAME off`
pi-qemu deck browse NAME -2               # the track encoder, + is up (50 at most at once: more loses detents)
pi-qemu deck press NAME push              # encoder push: opens the library, then activates the selection
pi-qemu deck tempo NAME center            # fader 0..16383, 8192 (center) the middle
pi-qemu deck midi NAME 90 3C 7F           # raw bytes, for anything else
pi-qemu deck stick NAME insert SAM3       # a rekordbox stick image, from archives/sticks/ (read-only); `stick NAME list`
pi-qemu deck stick NAME insert /some/dir  # a folder as a FAT32 stick, nothing copied (or a .stick file)
pi-qemu deck stick NAME insert-rw X.img   # an image file the deck may write to ("Record set")
pi-qemu deck input NAME set.wav           # the sound card's line input hears it (16-bit stereo 44.1 kHz); none: silence
```

Controls: `tempo-range keylock loop8 loop4 loop-double loop-halve back hotcue1
hotcue2 hotcue3 hotcue4 slip sort play cue loop-in loop-out reloop push
jog-touch`. The S3's MIDI contract is `firmwares/trimixxx-midi/lib/PiLink/MidiMap.hpp`.

The touchscreen, with xdotool on the deck's X display (a faithful touch: Qt
gets its taps as pointer events; a hover it cannot make, by design):

```sh
pi-qemu deck tap NAME 130 331             # a fingertip on that pixel
pi-qemu deck longpress NAME 500 300       # held 800 ms, past the long press
pi-qemu deck swipe NAME 100 300 700 300   # left to right: BACK
pi-qemu deck flick NAME 500 500 500 200   # a kinetic scroll
pi-qemu deck key NAME Down Return         # X key events
pi-qemu deck where NAME                   # the pointer's position
```

- **A copy of a real stick** (a DJ's files on an external drive): insert
  its folder, or a `.stick` file that also gives the real stick's layout,
  boot sector and size. See "A folder as a stick" in `pi-qemu/README.md`.
- **The line input** (what "Record set" records) is on the same card as the
  output, `hw:CARD=CODEC,DEV=0`, as on the real UCA222. A deck restored from a
  golden snapshot older than QEMU patch 20 has no input: `deck up NAME --boot`.
  It hears silence again after `deck stop` and `up`: give it the file again.
  "A stick the deck writes to" and "The line input" in `pi-qemu/README.md`
  have the rest.
- **A slow stick:** `stick NAME speed ID 4M` (or `4M/300` for reads a
  second too, `full` to lift it), before or while it is in. Sticks range
  from ~3 MB/s to over 100, so try what you change at a few speeds.
  `stick NAME reads ID [reset]` says what the Pi read off a folder stick, by
  file.
- **Load a track:** `stick NAME insert SAM3`, `press NAME push`, then browse
  and push until it loads, with a screenshot between steps. With no track
  loaded, most presses change nothing visible.
- **Check that bytes reached the Pi:**
  `pi-qemu deck ssh NAME 'sudo grep ^0: /proc/tty/driver/ttyAMA'`.
  - `rx:` counts what the S3 sent. It grows by 6 per `press` (note on and
    note off), 3 per `down`, `up`, `touch` or `browse` step, 6 per `tempo`,
    and 3 per 63 ticks of `jog`.
  - `tx:` is what Mixxx sent back to the S3 (the LEDs). It growing after a
    press shows Mixxx handled it.

## Several decks on one network (Pro DJ Link)

Decks started with the same `--link NET` share a network on their eth0s, as
CDJs in a booth share a switch: they see each other over Pro DJ Link, browse
each other's sticks, and load and play each other's tracks. Without `--link`
a deck's eth0 is on an empty switch.

```sh
pi-qemu deck up NAME-a --link NAME-net      # says: NAME-a: player 4 at 169.254.x.y, MAC on link NAME-net
pi-qemu deck up NAME-b --link NAME-net      # NAME-b: player 3 (it saw NAME-a holding 4)
pi-qemu link devices NAME-net               # the players heard on it: number, name, address, MAC, deck
pi-qemu deck stick NAME-a insert SANDISK-E02C   # a rekordbox stick in NAME-a...
pi-qemu deck press NAME-b push               # ...is "4 <label>" in NAME-b's library: push, browse, push to load
pi-qemu deck link NAME-a                    # what it announces, who else is on its link
pi-qemu deck link NAME-a unplug             # pull its cable (the Pi sees its link go down); plug puts it back
pi-qemu link capture NAME-net out.pcap 30   # every frame on the link for 30 s, for Wireshark or `prolink pcap`
```

- **A link's name is global on the Mac**, like a deck's: name it after your
  task, put only your own decks on it, and never `--link` a name another agent
  uses (`pi-qemu link list` shows every link and its decks).
- `up --link` takes about 15-35 s: a restored deck takes its own MAC, waits
  its turn on the link, and claims a player number; `up` waits for that and
  prints it. Decks on one link may be started in parallel.
- The link stays with the deck through `stop`/`up`; `up NAME --link none`
  (on a stopped deck) takes it off.
- A plain stick (no rekordbox export, e.g. a folder of MP3s) is served as a
  CDJ serves one: a CDJ's LINK shows its FOLDER category, and another deck
  lists it as a Folders source. A rekordbox stick such as `SANDISK-E02C`
  (read-only, nothing copied) is served with its whole library.
- `rm` your decks when done: each takes its socket off the link with it.

### A CDJ on your deck's link

An emulated CDJ-2000NXS, on Pioneer's own firmware, can join the link: a
"real" CDJ to test Pro DJ Link against. `pi-qemu/README.md`, "Emulated CDJs",
has the rest.

```sh
pi-qemu cdj build                              # once per checkout (~1.5 min); in a worktree, after prepare
pi-qemu cdj firmware ~/Downloads/C2KNXS.UPD    # once per Mac: into archives/ (git-ignored), never in git
pi-qemu cdj up NAME-cdj --link NAME-net        # ~25 s: "NAME-cdj: player 1 at 169.254.x.y, ... on link NAME-net"
pi-qemu link devices NAME-net 10               # 10 s: with a deck there, a CDJ re-claims and keep-alives up to ~5 s apart
pi-qemu cdj shot NAME-cdj cdj.png              # its 480x234 screen; `cdj press NAME-cdj link` a key
pi-qemu cdj lamps NAME-cdj                     # the lamps its firmware lit, by name: PLAY_PAUSE, MASTER, ...
pi-qemu cdj rm NAME-cdj                        # when done: `deck rm` doesn't know CDJs
```

`cdj window NAME-cdj` (or `up --window`) opens its screen and panel, lit as
its firmware lights it: for Sam, not for an agent, which reads `cdj shot` and
`cdj lamps`.

- **Expensive:** a CDJ takes about two cores from boot on, idle or not (one
  with `--dsp-model`), and its logs grow ~0.5 GB an hour until `cdj rm`. It
  runs at a real NXS's speed (keep-alives every 2.0 s), but a loaded track
  plays only with `cdj up --dsp-model` (the emulator's behavioural DSP:
  beats at the track's tempo, no audio). It then plays the moment it loads,
  with no cue and no PLAY, and with no master on the link it takes master;
  CUE does nothing in play until it has been stopped and cued once.
- **Centre its TEMPO slider before testing tempo or sync:** an emulated NXS
  says pitch -100% until its slider first moves. From `cdj2000-emulator/`,
  `.venv/bin/python -m tools.cdj_main.panel_control --port P analog 3 32768`,
  then the same with `analog 2 32768` (P: `endpoints.panel_port` in
  `~/.pi-qemu/cdj/NAME/run/run.json`). `analog 2 V` moves the slider: 0 is
  -10%, 65535 +10%. `mixxx/lib/prolink/emu-captures/README.md` names what
  else an emulated CDJ does differently.
- **In the crew,** a minion's CDJs are `BRANCH-a` and `BRANCH-b`, as its
  decks are `BRANCH` and `BRANCH-b`: the guard refuses other names,
  `crew resources --for cdj` counts them, and `crew clean` removes them. On
  one link a deck and a CDJ can't share a name, so `BRANCH-b` is one or the
  other there.
- **Never put its firmware or its screenshots in git:** both are Pioneer's.
  The website's few, shown with a disclaimer, live in usr-ein/static-resources.

## Deploy your own code onto it

```sh
pi-qemu deck deploy NAME config     # 005: mixxx_config: mapping, scripts, skin, fonts, mixxx.cfg (~10 s)
pi-qemu deck deploy NAME mixxx      # 004: the Mixxx fork: Docker arm64 build, swaps /usr/bin/mixxx
pi-qemu deck deploy NAME system     # 002: pi_config: units, session, splash, eth0, hotspot, dj-usb
pi-qemu deck deploy NAME launcher   # 003: trimixxx-launcher
pi-qemu deck deploy NAME ttymidi    # 001: the serial<->MIDI bridge
pi-qemu deck deploy NAME            # every step, in number order
```

The steps are `pi-qemu/deploy/NNN_name.sh` (on the Mac, reaching the deck as
`ssh deck`) and `NNN_name.pi.sh` (on the deck, as root); `lib.sh` there has
their contract. Name a step as `mixxx`, `004` or `004_mixxx`. A new step is
a new number. A step that changed the boot flags has the deck reboot before
the next one; one that restarted the MIDI bridge or the launcher has the
session restarted at the end (Mixxx only opens their ports at start). After
a session restart `deploy` waits until Mixxx is ready and says
`NAME: Mixxx is ready (sound open, the S3 connected)`. That means Mixxx is
running with its sound output and the deck's controller open, not that a
track plays; a screenshot is meaningful straight away. `deck ready NAME`
checks the same on its own.

Typical times: `config` ~10 s, `system` ~20 s, `mixxx` ~25 s for a changed
file or two (~75 s the first time in a worktree), plus any wait behind
another agent's Mixxx build. `ttymidi`, `launcher` and `mixxx` leave the deck
alone when their new binary is the same as the deck's.

`ttymidi`, `launcher` and `mixxx` build in Docker. `deploy` stops early if
Docker's disk has less than 6 GB free. Freeing it is the person's call: tell
them, do not prune.

Mixxx builds go by content: each checkout's build tree keeps its own copy of
the sources, and a build recompiles exactly the files whose content changed
since that tree's last build (`deploy`'s output says how many:
`tree-sync: N change(s)`). File timestamps, git checkouts and other agents'
builds do not affect it.

For a shell or script of your own that uses plain `ssh`/`scp`:
`eval "$(pi-qemu deck env NAME)"` makes `ssh NAME` and `ssh deck` reach it.

## Working from a git worktree

Agents usually work in their own git worktree (the root `CLAUDE.md` has the
whole workflow). For the deck:

1. **`pi-qemu worktree prepare`** first. A new worktree's submodules
   (`mixxx/`, its `lib/prolink`, `mixxx_config/ttymidi`) are empty
   directories. `prepare` makes them linked worktrees of the main checkout's
   repositories, in seconds, without downloading anything. `deploy` runs it
   by itself, but you need it before editing Mixxx. Never
   `git submodule update`: its clones die with the worktree, and any commits
   in them with it.
2. **Changing Mixxx:** `git -C mixxx switch -c NAME` before committing there.
   The branch and its commits are then in the main checkout's `mixxx/` too.
   Commit the bump in this repo as well (`git add mixxx`).
3. **`deck deploy NAME mixxx`** builds *your worktree's* Mixxx in its own
   Docker build tree, then swaps it onto your deck.
   - The first build in a worktree starts from a copy of the main checkout's
     tree and recompiles only what differs (~75 s in all).
   - After that, each build recompiles only what changed, by content (~25 s).
   - Mixxx builds queue: one compiles at a time across all agents, which
     keeps Docker's memory in bounds.
4. **Changing the S3's MIDI table** (`firmwares/trimixxx-midi/lib/PiLink/MidiMap.hpp`)
   **or pi-qemu itself:** the virtual S3 is compiled into pi-qemu, so build
   your own, `pi-qemu/build.sh app`, and run it by its path,
   `pi-qemu/app/build/pi-qemu deck ...`, for every call that should use it.
   Then `deck rm` and `deck up` your deck so it runs on it. Your build never
   makes everyone's golden again (main's does, on PATH): to try a change to
   how it is made, give it a scratch one, `PI_QEMU_CACHE=/tmp/x
   PI_QEMU_INSTANCES=/tmp/x/i`, seeded with clones of `.cache/stock` and
   `.cache/base` (`cp -c`).

## When ssh does not answer

```sh
pi-qemu deck console NAME 'systemctl --failed' 'ip -br a' 'dmesg | tail -30'   # the serial console
```

`~/.pi-qemu/instances/NAME/card.run/console.log` has the boot from the first
kernel line after `up --boot`. After a restore it only has what came after
the restore.

If `ready` says Mixxx started before the MIDI bridge restarted, the S3 no
longer reaches it. Do what the message says: restart the session
(`sudo systemctl restart getty@tty1`), then `ready` again.

## Check audio without sound

Mixxx's own recording of its main mix, fetched to the Mac:

```sh
pi-qemu deck record NAME 10 "$TMPDIR/NAME.wav"   # 10 s; make the deck play first
```

Or everything the deck's sound card plays, from QEMU, for a new instance
(`rm` an old one first): `pi-qemu deck up NAME -- --audio "wav:$TMPDIR/NAME.wav"`;
the file is valid at any moment.

The WAVs are 16-bit stereo at 44.1 kHz. Python's `wave` module reads them.
Measure the peak, the length of the loud part, and the frequency from zero
crossings.

A tone without Mixxx:
`pi-qemu deck ssh NAME 'sudo systemctl stop getty@tty1; timeout 3 speaker-test -D plughw:0,0 -c 1 -r 44100 -t sine -f 440'`.
- `-c 1`: one tone on both channels at once (`-c 2` plays left, then right).
- Exit code 124 is `timeout` ending it, which is normal.
- Stopping the session takes ~5 s. Afterwards bring Mixxx back with
  `pi-qemu deck ssh NAME 'sudo systemctl start getty@tty1'`, then
  `pi-qemu deck ready NAME`.

## Before you finish

Every time you end your work, whether it succeeded, failed or stopped part way:

1. Run `pi-qemu deck list`, and `pi-qemu cdj list` if you ran CDJs.
2. For each instance **you** started (`cdj rm NAME` for a CDJ):
   - **Remove it** (`pi-qemu deck rm NAME`) when nobody needs to look at it.
   - **Or keep it, and say so in your final message:** its name, whether it
     is still running or suspended, and the exact command to remove it.
     `pi-qemu deck stop NAME` suspends one you will come back to; that costs
     disk, not RAM, and `up` resumes it in ~3 s.
3. Working in a git worktree that is going away: **`pi-qemu worktree release`**.
   It gives back the worktree's Docker build tree (~2 GB) and its submodule
   checkouts. It refuses while they hold uncommitted work, or commits that no
   branch has. Leave the worktree in place if the person may still want it,
   and say so.
4. Your final message always ends with a line like
   `Emulated decks: removed fix-sync-meter.` or
   `Emulated decks: fix-sync-meter still running - pi-qemu deck rm fix-sync-meter when done.`
