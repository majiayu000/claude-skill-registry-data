---
name: tam-headshot-source
description: Surgically acquire one verified headshot per movement leader — official sources first, identity checks, direct download, manifest line — without bulk scraping or image-search roulette. Use when building TAM avatars, profile media, or filling knowledge leader folders.
disable-model-invocation: true
---

# TAM Headshot Source: One Verified Photo per Leader

Acquire a **single best headshot** for a named leader with **minimal wrong-person risk** and **minimal legal/process overhead**. This skill is about **finding and saving a source file**, not about AI retouching (use `asset-headshot` / platform headshot skills **after** you have a good source image).

## Invocation

```
/tam-headshot-source $ARGUMENTS
```

**Arguments:**
- **Required:** Leader full name as in the TAM list (e.g. `Danielle Strickland`)
- **Optional:** `slug` if known (e.g. `danielle-strickland`); otherwise derive from name
- **Optional:** `dry-run` — only list the ranked source URLs to try, do not download

---

## What This Is Not

| Approach | Why avoid for “surgical” TAM use |
|----------|----------------------------------|
| Google Images / Bing image search as first step | High rate of wrong person, old photo, or rights-unknown images |
| Social scrapers / automated LinkedIn mass download | ToS issues; brittle; often low-res |
| Saving any image from Wikipedia without checking the **file page** | License and attribution requirements vary; sometimes wrong image |
| Batch “download all photos from directory listing” | Scope creep; hard to audit |

---

## Source Priority (try in order; stop when satisfied)

Use **one primary identity anchor** before trusting any face (see Identity gate below).

1. **Employer / ministry “Staff” or “Team” page** — photo in context with name, title, org (best for disambiguation).
2. **Publisher author page** (IVP, Zondervan, etc.) — official marketing headshot when present.
3. **Conference speaker page** (Exponential, Verge, etc.) — often a recent PR headshot.
4. **Personal site About page** — when clearly maintained and single-subject.
5. **Wikipedia / Wikimedia Commons** — **only** if the person has an article and the infobox image is them: open the image **file description page**, confirm identity, note license (often CC BY-SA — attribution may be required for publication).
6. **Amazon Author page** — when it shows a clear solo headshot (not cover collage).

**LinkedIn profile photo:** usable as a last resort for identity verification *if* you can open the profile in a browser and confirm it is the same person; prefer downloading via a **direct image URL** the user pastes, or manual save — do not rely on undocumented scraping.

---

## Identity Gate (mandatory)

Before saving any file:

1. **Name collision check** — if the name is common, cross-check org + book + geography from `09-PLAUSIBLE-TAM-ALPHABETIZED.md` or the leader’s profile notes.
2. **Same-person signals** — match at least two independent signals (e.g. org + book cover photo + city) when the image is not on an official bio page.
3. **Reject** — group shots where the target is ambiguous, event stage shots where the face is tiny, obvious thumbnails under ~150px unless nothing else exists (then flag `low-res` in manifest).

If identity cannot be verified, **do not download**; record `status: unverified` and the candidate URLs for human review.

---

## Surgical Download Procedure

1. **Pick one page** from the priority list above (highest that has a usable solo headshot).
2. **Get a direct image URL** — prefer `<img src>` or `og:image` from that page’s HTML; avoid tracker redirects where possible.
3. **Download once:**

```bash
curl -fsSL -o "intelligence/leader-research/profiles/SLUG/media/headshot/SLUG-source.EXT" "DIRECT_IMAGE_URL"
```

Use the response `Content-Type` or magic bytes to choose `.jpg`, `.png`, or `.webp`. If format is odd, save bytes and rename after inspection.

4. **Record provenance** — append one line to the manifest (next section).
5. **Optional next step** — hand off to `asset-headshot` with the saved path for cropped/branded sizes (platform work), not part of this skill’s core output.

---

## Output Layout

Default paths (create directories if missing):

```
intelligence/leader-research/profiles/{slug}/media/headshot/
  {slug}-source.{jpg|png|webp}    # one canonical source file
```

Shared manifest (create if missing):

```
intelligence/leader-research/tam-search/HEADSHOT-MANIFEST.csv
```

**CSV columns (header row once):**

`slug,display_name,status,source_url,retrieved_utc,file_rel_path,license_note,notes`

- **status:** `ok` | `low-res` | `unverified` | `not-found`
- **license_note:** e.g. `org PR assumed` | `CC BY-SA 4.0 — see Wikipedia file page` | `unknown — internal use only`

---

## Relationship to Other Skills

| Skill | Role |
|-------|------|
| `tam-profile` | Broad research; may surface site URLs where a headshot lives |
| `tam-headshot-source` (this) | **Acquire** one source image + manifest line |
| `asset-headshot` / repo `headshot` | **Polish** or resize from an **existing** file |

### Optional Wikipedia batch script

`intelligence/leader-research/tam-search/fetch-wiki-headshots.py` can download **English Wikipedia** summary thumbnails into `profiles/<slug>/media/headshot/` and append `tam-search/HEADSHOT-MANIFEST.csv`. It uses last-name **word boundaries** (avoids e.g. “Roberts” matching “Robertson”), first-name checks, and ministry/author keyword heuristics. **Many names still yield `not-found`**, and **every `ok` row needs a human identity + license check** before publication. Run: `python3 fetch-wiki-headshots.py` (optional `--limit N`). When in doubt, use the manual source priority above.

---

## Headshot Status for the Alphabetized List

The file `intelligence/leader-research/tam-search/09-PLAUSIBLE-TAM-ALPHABETIZED.md` does **not** track image inventory. **Authoritative progress tracking** is `HEADSHOT-MANIFEST.csv` once you start filling it. You can grep the manifest for `slug` to see who already has `ok`.

---

## Checklist (per leader)

- [ ] Identity verified against TAM context
- [ ] Single primary source URL chosen from priority list
- [ ] One file saved under `profiles/{slug}/media/headshot/`
- [ ] Manifest row appended
- [ ] If publishing publicly, license/attribution reviewed (especially Wikipedia/Commons)
