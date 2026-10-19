---
name: build-and-upload-policy
description: Use when compiling, validating, and uploading a notsus change as a new Crewrift policy version.
---

# Build and upload a notsus policy

> Native migration prerequisite: external advisor code and previously published images must be rebuilt for the native hosted endpoint. These templates do not prove that an external image has migrated.


Build the amd64 image yourself, validate it locally, then upload it with current
`coworld upload-policy`. Keep the manual ECR `authorization_token` path below
only as a legacy fallback for older pinned installs that still fail before
parsing the server response. Do not skip the validation ladder or the local gate
— a green build and an accepted upload are NOT evidence the policy will score (or
even start) in a hosted round.

## Repo map — know where the edit lives before you touch anything

There are TWO repos, and they are easy to confuse:

- **`~/code/crewrift`** (`daveey/crewrift`) is harness/dashboard tooling ONLY.
  Its `.gitignore` excludes all policy source (`_crewrift-0136/`,
  `_crewrift-repo/`, `coworld/`), so a `notsus.nim` change physically cannot be
  committed there.
- **The policy lives in `~/code/crewrift/_crewrift-0136/`** — a clone of
  `Metta-AI/coworld-crewrift`. Its default branch is **`master`** (there is NO
  `main`), and it usually sits on a feature branch (e.g.
  `daveey/llm-advisor-0136`) that may carry the user's own uncommitted parallel
  WIP mixed with agent edits.
- Because the bot-repo checkout is nested inside `~/code/crewrift`, this
  project's transcripts/memory cover the bot-repo work too. Don't hunt for a
  separate project context.

(session-derived, unverified) Before any commit/push of policy changes, `git
status` the bot repo first — the user's WIP may be sitting unstaged. Do not
commit it under your hand without an explicit nod.

The bot-repo paths the rest of this recipe uses (run all commands from inside the
bot-repo checkout, e.g. `cd ~/code/crewrift/_crewrift-0136`):

- Player entrypoint: `players/notsus/notsus.nim`
- LLM advisor: `players/notsus/advisor.py`
- Build Dockerfile (with LLM advisor): `players/notsus/Dockerfile.llm`
  (a verbatim copy lives at this package's
  `universal/tools/Dockerfile.llm` — reference it for the exact build flags)
- Deps lockfile: `nimby.lock` (this repo uses **nimby**, not nimble)

## Step 1 — Validation ladder (cheap → expensive; each rung gates the next)

Run these in order from inside the bot-repo checkout. Don't pay for the slow
emulated amd64 build on every compile-error iteration — let the fast rungs catch
the error first. The defines below are copied from the Dockerfile so the local
check matches the image build exactly.

```bash
# 1. Deps. nimby (NOT nimble). Re-sync after switching trees / pulling.
nimby --global sync nimby.lock
#    Unresolvable bitworld/whisky imports mean the PACKAGE SET is incomplete,
#    not that your code is broken. Local nim may differ from the Docker-pinned
#    2.2.4 (e.g. 2.2.6) — that's fine for the local rungs.

# 2. Type-check (full semantic analysis, no codegen, ~seconds).
nim check -d:botHeadless -d:useMalloc --hints:off players/notsus/notsus.nim
echo "nim check rc=$?"   # capture the exit code explicitly — piping through
                         # tail SWALLOWS it
#    -d:botHeadless MATTERS: GUI-only debug code lives in
#    `when not defined(botHeadless)` blocks and can reference nonexistent fields
#    without breaking the headless build. After deletions, rg-sweep every removed
#    symbol. A pre-existing unused `pixelfonts` import warning is expected noise.

# 3. Native compile — proves codegen/link (arm64 on Apple Silicon, ~5s warm).
nim c -d:release -d:botHeadless -d:useMalloc --out:/tmp/notsus-native \
  players/notsus/notsus.nim
echo "native rc=$?"
```

Only once rungs 1–3 are clean do you build the amd64 artifact (Step 2).

## Step 2 — Build the amd64 image (the league requires amd64)

```bash
# From inside the bot-repo checkout. -f the LLM Dockerfile, tag with a fresh name.
IMG="notsus-llm:$(date +%Y%m%d-%H%M%S)"
NAME="daveey-notsus-<short-desc>"

docker buildx build --platform linux/amd64 \
  -f players/notsus/Dockerfile.llm \
  -t "$IMG" \
  --load .
```

The exact build-stage flags this Dockerfile compiles with (must match your
local rungs):
`nim c -d:release -d:botHeadless -d:useMalloc --opt:speed --stackTrace:on
--out:notsus players/notsus/notsus.nim`, Nim pinned **2.2.4**, nimby **0.1.26**.
The run stage adds `libcurl4` (telemetry upload must use curly/libcurl, not
std/httpclient), `python3` plus the native advisor SDK (for hosted inference), and
copies in `advisor.py`.

Before building, set
`COWORLD_LLM_MODEL=anthropic/claude-haiku-4.5`. Haiku is
mandatory for Crewrift; do not use Sonnet or Opus. Budget prompts, response limits, and call cadence
so the whole policy episode stays below **1,800 quota-weighted tokens**
(`input + cache-write + 5 × output`), then use the scripted floor for the remainder.

**Gotcha B1 — stale buildx layer-cache trap (session-derived, unverified).** If
the amd64 build fails with a compile error whose **line number does not match the
current file** — and your local `nim check`/`nim c` with the exact same flags
passes — suspect a stale `COPY . .` layer compiling OLD source. Rebuild with
`--no-cache` before suspecting your edit. (A real case failed on a symbol at line
4992 the file didn't have there; `--no-cache` succeeded with zero code changes.)

```bash
docker buildx build --no-cache --platform linux/amd64 \
  -f players/notsus/Dockerfile.llm -t notsus-llm:rebuild --load .
```

## Step 3 — Local full-container gate (do this BEFORE uploading)

A green build / accepted upload / created version proves NOTHING about whether
the player scores or even starts in a hosted round. Run the exact image locally
for a full episode and inspect the artifacts before submitting. The failure modes
this catches (a stale env-var contract, a slot that scores zero, a player that
connects but never moves) are invisible to the build and the upload API and only
surface as a wasted live round hours later.

Run a full local episode with the built image fielded against the canonical
hosted package (use this package's `universal/tools/episode_runner.py` /
`antfarm_run.py` harness — they drive the local game server and copolicy
bundling), then **read `game.stdout.log`** and confirm the positive oracle:

> clean connect for all 8 players, the game running to its tick limit, and a
> valid replay written.

Confirm `policy_names`, player count, slot labels, and server/replay/result
visibility all AGREE before trusting the upload path.

**Gotcha G1 — all-zero cert scores are a CLEAN baseline, not a bug
(session-derived, unverified).** The certification fixture runs `maxTicks=300`
(~12s realtime) — far too short for tasks, kills, or votes (below
`killCooldownTicks`), so every player scores 0 with "draw: time limit reached".
End-of-game "connection lost" lines are normal teardown.

**Gotcha G2 — QEMU drop-outs are a false "bot crashes" signal (session-derived,
unverified).** Running the amd64 image on Apple Silicon under emulation is too
slow to keep up with the 24fps realtime server, so the bot can drop the socket. A
`game started players=8` → `draw: time limit reached` sequence with a written
replay means the bot connected and played fine.

## Step 4 — Upload with `coworld upload-policy`

**Gotcha U1 — use the current CLI first.** Current `coworld upload-policy`
understands the server's ECR `authorization_token` response. Upload with:

```bash
uv run coworld upload-policy "$IMG" --name "$NAME" --use-llm \
  --llm-model anthropic/claude-haiku-4.5
```

Omit `--use-llm` when the policy does not need inference.
`pre_signed_info: null` means the exact image hash was already pushed; it is not
an error. An aliased policy (same image, new name) registers without a rebuild.

Post update cards to your human's play-page feed with
`uv run coworld feed post <file.md> --coworld <coworld_name>`. The file is markdown with a `---` front matter
block (`type: hello|update|attention`, `summary`). Follow the rules in
`coworld/docs/FEED_CARDS.md` (shipped in the `coworld` package).

**Legacy fallback.** If an older pinned install fails before upload with
`ImageUploadResponse.pre_signed_info.credentials Field required`, upgrade the
local Coworld package from the current metta checkout. Only if you cannot
upgrade, use the manual `authorization_token` path below.

### Legacy manual ECR fallback

The legacy manual upload reuses the client's own push helper. Run as a Python
script with the bot repo's env (so `coworld` is importable):

```python
import subprocess, requests
from coworld.api_client import CoworldUploadClient
from coworld.config import DEFAULT_SUBMIT_SERVER
from coworld.upload import (  # helper names as used in the working path
    _local_image_client_hash, _image_upload_name, _push_archive_to_registry,
)

IMG  = "notsus-llm:<your-tag>"   # the amd64 image you built + gated
NAME  = "daveey-notsus-<short-desc>"  # policy name; new name => new policy

# 1. Log in and fingerprint the image (also asserts the image is linux/amd64).
client = CoworldUploadClient.from_login(server_url=DEFAULT_SUBMIT_SERVER)
ch   = _local_image_client_hash(IMG)
name = NAME or _image_upload_name(IMG)

# 2. Raw POST to request an upload slot.
resp = client._session.post(
    f"{DEFAULT_SUBMIT_SERVER}/v2/container_images/upload",
    json={"name": name, "client_hash": ch},
).json()
image_id = resp["image"]["id"]
presign  = resp.get("pre_signed_info")

# 3. Push the image tarball IF a presign was returned.
#    Gotcha U2: pre_signed_info comes back NULL when that exact image hash was
#    already pushed (e.g. by a subagent or an earlier attempt). That is NOT an
#    error — skip the push and go straight to step 5; the version likely exists.
if presign is not None:
    registry = presign["registry"]
    repository = presign["repository"]
    tag = presign["tag"]
    auth = presign["authorization_token"]   # base64 AWS:password
    base_url = f"https://{registry}/v2/{repository}"
    archive = "/tmp/notsus-image.tar"
    subprocess.run(["docker", "image", "save", "-o", archive, IMG], check=True)
    _push_archive_to_registry(archive, base_url, tag, auth)

# 4. Mark the image upload complete (image status -> ready).
client.complete_image_upload(image_id)

# 5. Create the policy version pointing at this image.
#    --use-llm == ONLY secret_env={"COWORLD_LLM_ENABLED":"true"} (the league supplies
#    native SDK endpoint placeholders at runtime). run=None.
result = client.complete_docker_image_policy(
    name=name,
    container_image_id=image_id,
    run=None,
    secret_env={"COWORLD_LLM_ENABLED": "true"},
)
print(result)   # returns <name>:vN + the pvid
```

**Gotcha U3 — a failed CLI upload leaves a stale `pending` image record.** Ignore
it. The policy points at whichever `container_image_id` you pass to step 5, not at
the orphaned record.

**Gotcha U4 — aliasing needs no rebuild (session-derived, unverified).** To field
a byte-identical bot under a NEW policy name (a fresh-ledger player or a renamed
experiment slot), just re-run steps 1–5 with a new `NAME`. Same image bytes
register without any rebuild or re-push.

## Success check

You're done when:

1. `nim check` and the native compile returned **rc=0**, and the amd64 buildx
   build returned **rc=0** (with `--no-cache` if Gotcha B1 fired).
2. The local full-container gate showed the positive oracle: all 8 players
   connected, the game ran to its tick limit, and a valid replay was written
   (zeros/connection-lost lines being benign per G1/G2).
3. Step 5 printed a `<name>:vN` plus a pvid — that is your new policy version,
   ready to field in a league A/B (e.g. via this package's `league_eval.py` /
   `eval.py`).

If any rung is red, fix the root cause and re-run from that rung — do not upload
a policy that failed the gate.
